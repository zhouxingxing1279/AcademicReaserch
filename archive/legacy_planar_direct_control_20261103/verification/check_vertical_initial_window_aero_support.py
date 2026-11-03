#!/usr/bin/env python3
"""Exact support bound for the first 15-step nonlinear benchmark window."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = F(89401829, 65520000)


def certificate():
    config = json.loads((ROOT / "configs/planar_baseline.json").read_text())
    h = F(str(config["plant"]["dt_s"]))
    gravity = F(str(config["plant"]["gravity_m_s2"]))
    inertia = F(str(config["plant"]["inertia_kg_m2"]))
    thrust_max = F(str(config["domain"]["input_upper"][0]))
    torque_max = F(str(config["domain"]["input_upper"][1]))
    initial = config["initial_set"]
    phi0 = F(str(initial["halfwidth"][4]))
    omega0 = F(str(initial["halfwidth"][5]))
    velocity0 = F(str(initial["halfwidth"][2]))
    steps = 15

    # Exact double-integrator support for arbitrary torque signs.
    angular_acceleration = torque_max / inertia
    pitch_upper = (
        phi0
        + steps * h * omega0
        + h * h * angular_acceleration * steps * (steps - 1) / 2
    )

    # A deliberately simple horizontal acceleration envelope.  The global
    # state/wind domain is used only inside the nonlinear aerodynamic terms;
    # the small pitch bound is retained in thrust and attitude terms.
    relative_global = F(7, 2)
    sqrt_global_upper = F(351, 100)
    thrust_term = thrust_max * pitch_upper  # |sin(phi)| <= |phi|
    x_drag_term = F(3, 25) * relative_global * sqrt_global_upper
    cross_term = F(3, 100) * relative_global * relative_global
    thrust_ratio_deviation = F(1, 2)
    attitude_term = F(2, 25) * (2 * pitch_upper) * thrust_ratio_deviation
    horizontal_acceleration_upper = thrust_term + x_drag_term + cross_term + attitude_term
    horizontal_velocity_upper = velocity0 + steps * h * horizontal_acceleration_upper
    reachable_relative_x_upper = horizontal_velocity_upper + F(1, 2)

    # Import Run172's exact vertical projection value as an independently
    # checked arithmetic fact, then certify a rational square-root upper bound.
    vertical_velocity_lower = F(-90859, 40000)
    negative_relative_z_magnitude = F(1, 2) - vertical_velocity_lower
    vertical_sqrt_upper = F(139, 50)
    sqrt_bound = (
        negative_relative_z_magnitude**2 + F(1, 25)
        < vertical_sqrt_upper**2
    )
    vertical_aero_upper = (
        F(3, 20) * negative_relative_z_magnitude * vertical_sqrt_upper
        + F(1, 50) * reachable_relative_x_upper**2
    )

    expected = (
        pitch_upper == F(22, 125)
        and horizontal_acceleration_upper == F(222281, 50000)
        and horizontal_velocity_upper == F(716843, 500000)
        and reachable_relative_x_upper == F(966843, 500000)
        and negative_relative_z_magnitude == F(110859, 40000)
        and sqrt_bound
        and vertical_aero_upper == F(15381098824149, 12500000000000)
        and TARGET - vertical_aero_upper == F(1371915844271969, 10237500000000000)
        and vertical_aero_upper < TARGET
        and thrust_max / gravity == F(3, 2)
    )
    if not expected:
        raise AssertionError("initial-window aerodynamic support certificate changed")

    return {
        "pitch_projection": {
            "absolute_upper_through_step_15": pitch_upper,
            "angular_acceleration_absolute_upper": angular_acceleration,
            "covers_every_admissible_torque_history": True,
        },
        "horizontal_velocity_projection": {
            "global_relative_speed_bound_used_inside_aerodynamics": relative_global,
            "global_sqrt_upper": sqrt_global_upper,
            "acceleration_absolute_upper": horizontal_acceleration_upper,
            "velocity_absolute_upper_through_step_15": horizontal_velocity_upper,
            "relative_x_absolute_upper": reachable_relative_x_upper,
        },
        "vertical_aerodynamic_support": {
            "vertical_velocity_lower_from_run172": vertical_velocity_lower,
            "negative_relative_z_magnitude_upper": negative_relative_z_magnitude,
            "vertical_sqrt_upper": vertical_sqrt_upper,
            "vertical_sqrt_bound_exact": sqrt_bound,
            "upper": vertical_aero_upper,
            "run168_target": TARGET,
            "strict_margin": TARGET - vertical_aero_upper,
            "strictly_below_run168_target": vertical_aero_upper < TARGET,
        },
    }


def run():
    return {
        "status": "pass",
        "claim": "initial_fifteen_step_reachable_projection_certifies_vertical_aerodynamic_support_below_run168_target",
        **certificate(),
        "initial_fifteen_step_window_aero_support_certified": True,
        "measurement_conditioned_reset_closure_proved": False,
        "recursive_tube_invariance_proved": False,
        "is_recursive_feasibility_proof": False,
        "is_full_six_state_guarantee": False,
    }


def _encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _encode(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_encode(item) for item in value]
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    result = run()
    sources = [
        "verification/check_vertical_initial_window_aero_support.py",
        "verification/test_vertical_initial_window_aero_support.py",
        "verification/check_vertical_cross_time_velocity_exclusion.py",
        "src/smf_mpc/plant.py",
        "configs/planar_baseline.json",
        "docs/learning/108_vertical_initial_window_aero_support.md",
        "docs/literature/READ_PAPERS.md",
        "docs/research/run173_literature_gate.md",
        "docs/research/run173_research_log.md",
    ]
    result["source_sha256"] = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in sources
    }
    encoded = _encode(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(encoded, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": encoded["status"], "claim": encoded["claim"]}, indent=2))


if __name__ == "__main__":
    main()
