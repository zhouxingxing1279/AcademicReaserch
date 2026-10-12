#!/usr/bin/env python3
"""Exact scalar reachability certificate excluding the Run169 vertical speed."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def certificate():
    config = json.loads((ROOT / "configs/planar_baseline.json").read_text())
    phi_max = F(str(config["domain"]["state_upper"][4]))
    thrust_min = F(str(config["domain"]["input_lower"][0]))
    gravity = F(str(config["plant"]["gravity_m_s2"]))
    step = F(str(config["plant"]["dt_s"]))
    vz_min = F(str(config["domain"]["state_lower"][3]))
    wind_z_min = F(str(config["plant"]["wind_bounds_m_s"][1][0]))
    initial_vz_min = F(str(config["initial_set"]["center"][3])) - F(
        str(config["initial_set"]["halfwidth"][3])
    )

    # For |phi| <= 9/20, the alternating cosine series ending at -x^6/720
    # is a lower bound.  The exact polynomial is already above 9/10.
    x = phi_max
    cosine_polynomial_lower = F(1) - x**2 / 2 + x**4 / 24 - x**6 / 720
    cosine_floor = F(9, 10)

    # Domain closure gives rz=vz-wz <= 3-(-1/2)=7/2.  At positive rz the
    # vertical drag is most negative. sqrt((7/2)^2+1/25) < 351/100.
    relative_z_upper = F(str(config["domain"]["state_upper"][3])) - wind_z_min
    sqrt_argument = relative_z_upper**2 + F(1, 25)
    sqrt_upper = F(351, 100)
    aerodynamic_lower = -F(3, 20) * relative_z_upper * sqrt_upper

    # The omitted +rx^2*cos(phi)/50 term is nonnegative on this pitch domain.
    acceleration_lower = thrust_min * cosine_floor - gravity + aerodynamic_lower
    steps = 15
    reachable_vz_lower = initial_vz_min + steps * step * acceleration_lower
    run169_vz = F(-170955031, 72000000)

    elementary_ok = (
        x == F(9, 20)
        and cosine_polynomial_lower > cosine_floor
        and sqrt_argument < sqrt_upper**2
    )
    expected = (
        elementary_ok
        and relative_z_upper == F(7, 2)
        and aerodynamic_lower == F(-7371, 4000)
        and acceleration_lower == F(-28953, 4000)
        and reachable_vz_lower == F(-90859, 40000)
        and reachable_vz_lower > run169_vz
    )
    if not expected:
        raise AssertionError("cross-time vertical velocity certificate changed")

    return {
        "elementary_bounds": {
            "pitch_absolute_upper": x,
            "cosine_polynomial_lower": cosine_polynomial_lower,
            "cosine_floor_used": cosine_floor,
            "cos_9_over_20_strictly_above_9_over_10": cosine_polynomial_lower > cosine_floor,
            "sqrt_argument_at_rz_7_over_2": sqrt_argument,
            "sqrt_upper_used": sqrt_upper,
            "sqrt_1229_over_100_strictly_below_351_over_100": sqrt_argument < sqrt_upper**2,
        },
        "vertical_acceleration": {
            "relative_vertical_velocity_upper": relative_z_upper,
            "aerodynamic_lower_bound": aerodynamic_lower,
            "lower_bound": acceleration_lower,
            "valid_for_every_domain_state_input_and_wind": True,
        },
        "cross_time_projection": {
            "initial_vz_lower": initial_vz_min,
            "euler_step": step,
            "steps": steps,
            "vz_lower_after_15_steps": reachable_vz_lower,
            "run169_vz": run169_vz,
            "strict_separation": reachable_vz_lower - run169_vz,
            "run169_vz_excluded": reachable_vz_lower > run169_vz,
        },
    }


def run():
    return {
        "status": "pass",
        "claim": "run169_vertical_velocity_is_outside_the_15_step_domain_constrained_reachable_projection",
        **certificate(),
        "run169_velocity_witness_excluded_from_15_step_reachable_projection": True,
        "full_nonlinear_reachable_set_computed": False,
        "all_aerodynamic_threshold_violations_excluded": False,
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
        "verification/check_vertical_cross_time_velocity_exclusion.py",
        "verification/test_vertical_cross_time_velocity_exclusion.py",
        "src/smf_mpc/plant.py",
        "configs/planar_baseline.json",
        "docs/learning/107_vertical_cross_time_velocity_exclusion.md",
        "docs/literature/READ_PAPERS.md",
        "docs/research/run172_literature_gate.md",
        "docs/research/run172_research_log.md",
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
