#!/usr/bin/env python3
"""Exact graph-consistency audit for the Run169 aerodynamic witness."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TARGET = F(89401829, 65520000)


def shared_factor_graph_certificate():
    config = json.loads((ROOT / "configs/planar_baseline.json").read_text())
    vx, vz = F(3), F(-170955031, 72000000)
    wx, wz = F(-1, 2), F(1, 2)
    phi, thrust = F(0), F(981, 100)
    rx, rz = vx - wx, vz - wz

    qx = rx * rx + F(1, 25)
    qz = rz * rz + F(1, 25)
    sx_lower = abs(rx)
    sx_upper = abs(rx) + F(1, 100)
    sz_lower = abs(rz)
    sz_upper = abs(rz) + F(1, 100)
    brackets = (
        sx_lower * sx_lower < qx < sx_upper * sx_upper
        and sz_lower * sz_lower < qz < sz_upper * sz_upper
    )

    # At phi=0, cos(phi)=1 and the vertical formula has positive
    # coefficient -3*rz/20 because rz<0.
    aero_lower = -F(3, 20) * rz * sz_lower + F(1, 50) * rx * rx
    aero_upper = -F(3, 20) * rz * sz_upper + F(1, 50) * rx * rx

    state_lo = [F(str(x)) for x in config["domain"]["state_lower"]]
    state_hi = [F(str(x)) for x in config["domain"]["state_upper"]]
    input_lo = [F(str(x)) for x in config["domain"]["input_lower"]]
    input_hi = [F(str(x)) for x in config["domain"]["input_upper"]]
    wind = config["plant"]["wind_bounds_m_s"]
    domains = (
        state_lo[2] <= vx <= state_hi[2]
        and state_lo[3] <= vz <= state_hi[3]
        and state_lo[4] <= phi <= state_hi[4]
        and input_lo[0] <= thrust <= input_hi[0]
        and F(str(wind[0][0])) <= wx <= F(str(wind[0][1]))
        and F(str(wind[1][0])) <= wz <= F(str(wind[1][1]))
    )
    affine_equalities = rx == vx - wx and rz == vz - wz
    expected = (
        (rx, rz) == (F(7, 2), F(-206955031, 72000000))
        and affine_equalities and domains and brackets
        and aero_lower == F(51297584856210961, 34560000000000000)
        and aero_lower > TARGET and aero_upper > aero_lower
    )
    if not expected:
        raise AssertionError("shared aerodynamic factor graph certificate changed")

    return {
        "shared_factor_graph": {
            "state_velocity": (vx, vz),
            "wind": (wx, wz),
            "relative_velocity": (rx, rz),
            "pitch": phi,
            "thrust": thrust,
            "all_affine_factor_equalities_hold": affine_equalities,
            "state_wind_pitch_and_thrust_domains_hold": domains,
        },
        "sqrt_factors": {
            "qx": qx,
            "qz": qz,
            "sx_bracket": (sx_lower, sx_upper),
            "sz_bracket": (sz_lower, sz_upper),
        },
        "vertical_aerodynamic_image": {
            "lower": aero_lower,
            "upper": aero_upper,
            "run168_target": TARGET,
            "sqrt_brackets_are_exact": brackets,
            "lower_strictly_exceeds_target": aero_lower > TARGET,
        },
    }


def run():
    return {
        "status": "pass",
        "claim": "run169_point_survives_exact_single_step_shared_factor_graph",
        **shared_factor_graph_certificate(),
        "exact_nonlinear_graph_point_exists": True,
        "every_sound_single_step_graph_outer_approximation_must_include_its_image": True,
        "nonlinear_history_from_initial_set_proved": False,
        "cross_time_joint_reachability_remains_required": True,
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
        "verification/check_vertical_shared_factor_graph.py",
        "verification/test_vertical_shared_factor_graph.py",
        "src/smf_mpc/plant.py",
        "configs/planar_baseline.json",
        "docs/learning/106_vertical_shared_factor_graph.md",
        "docs/literature/READ_PAPERS.md",
        "docs/research/run171_literature_gate.md",
        "docs/research/run171_research_log.md",
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
