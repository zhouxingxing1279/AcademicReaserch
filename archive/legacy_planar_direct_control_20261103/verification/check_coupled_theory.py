#!/usr/bin/env python3
"""Exact arithmetic for the six-state finite-horizon proof in theory/04.

This checks analytic enclosure coefficients, not sampled plant trajectories.
No online controller, learned model or optimization solver is executed.
"""

import argparse
from fractions import Fraction as F
import hashlib
import json
from math import comb
from pathlib import Path

from check_invariance_theory import verify as verify_attitude


ROOT = Path(__file__).resolve().parents[1]
CONFIG_SHA = "d7ecd17199b9976f3b1083e63a3b5957dfb9f34cc83841bf228f17b145b6e753"
PLANT_SHA = "86f9a9411835958af2f4df73cca1ffcd6433ac8701ac575e27625692c3f88208"


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def strings(values):
    return [str(value) for value in values]


def verify():
    config_path = ROOT / "configs/planar_baseline.json"
    plant_path = ROOT / "src/smf_mpc/plant.py"
    require(sha256(config_path) == CONFIG_SHA, "Frozen configuration changed")
    require(sha256(plant_path) == PLANT_SHA, "Frozen benchmark formula changed")
    config = json.loads(config_path.read_text(), parse_float=F, parse_int=F)
    require(config["plant"]["truth_semantics"] == "defined_discrete_euler", "Euler semantics required")
    require(config["plant"]["external_process_halfwidth"] == [0] * 6, "Zero external increments required")
    attitude = verify_attitude()
    e_phi, e_rate = map(F, attitude["invariant_set_outer_box"])
    correction = F(attitude["torque_upper_bound"])
    h, g = F(1, 50), F(981, 100)
    d_x, d_z = F(47, 25), F(1043, 500)

    # Rational majorant for sqrt(3.5^2 + .04). No floating sqrt is used.
    relative_speed = F(7, 2)
    root_majorant = F(17529, 5000)
    require(root_majorant**2 >= relative_speed**2 + F(1, 25), "Invalid square-root majorant")
    aero_x_global = F(3, 25) * relative_speed * root_majorant + F(3, 100) * relative_speed**2 + F(1, 25)
    aero_z_global = F(3, 20) * relative_speed * root_majorant + F(1, 50) * relative_speed**2
    require(aero_x_global <= d_x and aero_z_global <= d_z, "Contract bounds not justified")

    n, magnitude = 20, F(1, 40)
    horizon = 2 * n

    def reference(k):
        if k <= n:
            return h * magnitude * k * (k - 1) / 2, magnitude * k
        s = k - n
        return (
            h * magnitude * (F(n * (n - 1), 2) + n * s - F(s * (s - 1), 2)),
            magnitude * (n - s),
        )

    psi = [reference(k)[0] for k in range(horizon + 1)]
    rate = [reference(k)[1] for k in range(horizon + 1)]
    require((psi[-1], rate[-1]) == (F(1, 5), 0), "Reference endpoint differs")
    for k in range(horizon):
        mu = magnitude if k < n else -magnitude
        require(psi[k + 1] == psi[k] + h * rate[k], "Reference angle identity failed")
        require(rate[k + 1] == rate[k] + mu, "Reference rate identity failed")
    angle_sum = sum(psi[:-1], F(0))
    weighted_angle_sum = sum(((horizon - 1 - k) * psi[k] for k in range(horizon)), F(0))
    require(angle_sum == h * magnitude * n**2 * (n - 1) == F(19, 5), "Angle sum differs")
    require(weighted_angle_sum == h * magnitude * (comb(2 * n, 4) - 2 * comb(n, 4)) == F(817, 20), "Weighted angle sum differs")

    # |sin(phi)| <= |phi|, 0 <= 1-cos(phi) <= phi^2/2.
    alpha_x = [g * (value + e_phi) + d_x for value in psi[:-1]]
    phi_max = max(psi) + e_phi
    alpha_z = g * phi_max**2 / 2 + d_z
    initial_position, initial_velocity = F(1, 50), F(1, 10)
    rows = []
    for k in range(horizon + 1):
        rxv = initial_velocity + h * sum(alpha_x[:k], F(0))
        rxp = initial_position + k * h * initial_velocity + h**2 * sum(
            ((k - 1 - j) * alpha_x[j] for j in range(k)), F(0)
        )
        rzv = initial_velocity + k * h * alpha_z
        rzp = initial_position + k * h * initial_velocity + h**2 * k * (k - 1) * alpha_z / 2
        bounds = [rxp, rzp, rxv, rzv, psi[k] + e_phi, rate[k] + e_rate]
        limits = [F(5), F(3, 2), F(3), F(3), F(9, 20), F(2)]
        require(all(value < limit for value, limit in zip(bounds, limits)), f"Domain bound failed at k={k}")
        if rows:
            previous = list(map(F, rows[-1]["absolute_bounds_relative_to_hover"]))
            require(rxp == previous[0] + h * previous[2], "Horizontal position radius recurrence failed")
            require(rzp == previous[1] + h * previous[3], "Vertical position radius recurrence failed")
            require(rxv == previous[2] + h * alpha_x[k - 1], "Horizontal velocity radius recurrence failed")
            require(rzv == previous[3] + h * alpha_z, "Vertical velocity radius recurrence failed")
        rows.append({
            "tick": k, "time_s": str(k * h),
            "reference": strings([psi[k], rate[k]]),
            "absolute_bounds_relative_to_hover": strings(bounds),
        })
    final = list(map(F, rows[-1]["absolute_bounds_relative_to_hover"]))
    require(final[:4] == list(map(F, [".9157216", ".82659438475", "2.52614", "1.963062525"])), "Six-state enclosure numbers differ")
    torque_bound = magnitude + correction
    require(torque_bound == F(".0546") < F(".08"), "Torque bound failed")

    # Offline benchmark comparison only; these signs are NOT inferred from a
    # symmetric acceleration-box information contract alone.
    low = F(5, 2)
    ax_min = -F(3, 25) * relative_speed * root_majorant - F(3, 100) * relative_speed**2
    ax_max = -(F(3, 25) + F(3, 100)) * low**2
    az_min = -F(3, 20) * relative_speed * root_majorant
    az_max = -F(3, 20) * low**2 + F(1, 50) * relative_speed**2
    vx_next = [3 + h * (-g * F(1, 5) + ax_min), 3 + h * ax_max]
    vz_next = [3 + h * (-g * F(1, 50) + az_min), 3 + h * az_max]
    require(-3 < vx_next[0] <= vx_next[1] < 3, "Structured horizontal witness failed")
    require(-3 < vz_next[0] <= vz_next[1] < 3, "Structured vertical witness failed")
    box_thrust_lower = d_x / F(1, 5)
    box_thrust_upper = (g - d_z) / F(49, 50)
    require(box_thrust_lower > box_thrust_upper, "Box infeasibility witness failed")

    # Fixed-tilt continuation: one admissible zero-wind, zero-angle-noise world.
    require(F(301, 100)**2 >= 9 + F(1, 25), "Invalid zero-wind square-root majorant")
    drag_upper = F(3, 25) * 3 * F(301, 100) + F(3, 100) * 9
    sine_lower = F(1, 5) - F(1, 5)**3 / 6
    decrease = h * (g * sine_lower - drag_upper)
    require(decrease == F(".0119064") > 0, "Fixed-tilt decrease failed")
    ratio = F(6) / decrease
    exit_steps = ratio.numerator // ratio.denominator + 1
    require(exit_steps == 504 and exit_steps * decrease > 6, "Exit horizon failed")

    return {
        "status": "EXACT_FINITE_HORIZON_SIX_STATE_ARITHMETIC_PASSED",
        "scope": "Written robust set-containment induction for ticks 0..40; exact finite coefficients only",
        "state_order": config["state_order"],
        "position_reference": ["0", "2"],
        "horizon_ticks": horizon, "duration_s": str(h * horizon),
        "actuation": {"constant_T": str(g), "mu_magnitude": str(magnitude), "ticks_per_phase": n,
                      "feedback_correction_bound": str(correction), "torque_bound": str(torque_bound)},
        "global_aero_majorants": strings([aero_x_global, aero_z_global]),
        "contract_aero_bounds": strings([d_x, d_z]),
        "reference_angle_sum": str(angle_sum), "reference_weighted_angle_sum": str(weighted_angle_sum),
        "vertical_acceleration_bound": str(alpha_z),
        "uniform_bounds_relative_to_hover": strings(final[:4] + [max(psi) + e_phi, max(rate) + e_rate]),
        "uniform_height_interval": strings([2 - final[1], 2 + final[1]]),
        "per_tick_enclosures": rows,
        "structured_benchmark_one_step_witness": {
            "knowledge_scope": "Offline analytic benchmark only; additional signed structure must be certified and supplied equally to all online baselines",
            "aero_x_interval": strings([ax_min, ax_max]), "aero_z_interval": strings([az_min, az_max]),
            "next_vx_interval": strings(vx_next), "next_vz_interval": strings(vz_next),
            "independent_box_thrust_necessary_bounds": strings([box_thrust_lower, box_thrust_upper]),
        },
        "invalid_fixed_tilt_terminal_policy": {
            "world": "Zero wind, zero angle measurement noise, zero initial angular error",
            "velocity_decrease_per_tick": str(decrease), "exit_within_additional_ticks": exit_steps,
            "exit_by_total_tick": horizon + exit_steps,
        },
        "full_six_state_infinite_horizon_invariance_proved": False,
        "neural_superiority_proved": False,
        "controller_implementation_executed": False,
        "config_sha256": CONFIG_SHA, "plant_source_sha256": PLANT_SHA,
        "attitude_checker_sha256": attitude["checker_sha256"],
        "checker_sha256": sha256(Path(__file__)),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output and args.output.exists():
        parser.error("Use a new output file")
    result = verify()
    payload = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload)
    print(json.dumps({key: value for key, value in result.items() if key != "per_tick_enclosures"}, indent=2))


if __name__ == "__main__":
    main()
