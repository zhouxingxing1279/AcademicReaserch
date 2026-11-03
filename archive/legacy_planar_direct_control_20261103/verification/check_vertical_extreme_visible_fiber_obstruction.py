#!/usr/bin/env python3
"""Exact reachable-fiber obstruction for the current 15-tick contract."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

from check_cycle_lifted_zonotope import problem_data
from check_vertical_correlated_return_seed import correlated_return_seed


H = F(1, 50)
MISS_COUNT = 14
POSITION_LIMIT = F(1)
ROOT = Path(__file__).resolve().parents[1]


def _sign(value):
    return F(1) if value > 0 else F(-1) if value < 0 else F(0)


def extreme_visible_fiber_certificate():
    config, _, miss_generators, _, _, _ = problem_data()
    rows = correlated_return_seed()["return_seed"]["generators_by_row"]
    visible = [rows[2][i] - rows[0][i] for i in range(len(rows[0]))]
    endpoint_direction = [
        rows[2][i] + MISS_COUNT * H * rows[3][i]
        for i in range(len(rows[0]))
    ]

    visible_dp = sum((abs(value) for value in visible), F(0))
    fixed_witness = [_sign(value) for value in visible]
    visible_residual = (
        sum((value * witness for value, witness in zip(visible, fixed_witness)), F(0))
        - visible_dp
    )
    center = sum(
        (value * witness for value, witness in zip(endpoint_direction, fixed_witness)),
        F(0),
    )
    free_halfwidth = sum(
        (abs(value) for value, observation in zip(endpoint_direction, visible)
         if observation == 0),
        F(0),
    )
    lower = center - free_halfwidth
    upper = center + free_halfwidth

    residual_halfwidth = miss_generators[3][1]
    correction_limit = F(str(config["mpc"]["ancillary_correction_upper"][0]))
    triangular = F(MISS_COUNT * (MISS_COUNT - 1), 2)
    positive_residual_shift = triangular * H * residual_halfwidth
    maximum_negative_control_shift = -triangular * H * H * correction_limit
    endpoint_lower_bound = (
        upper + positive_residual_shift + maximum_negative_control_shift
    )
    violation = endpoint_lower_bound - POSITION_LIMIT

    if not (
        visible_residual == 0
        and all(abs(value) <= 1 for value in fixed_witness)
        and lower > POSITION_LIMIT
        and residual_halfwidth == H * correction_limit
        and positive_residual_shift == -maximum_negative_control_shift
        and violation > 0
    ):
        raise AssertionError("extreme visible-fiber obstruction changed")

    return {
        "extreme_fiber": {
            "visible_coordinate": "d_p=e_p-eta_p",
            "visible_dp": visible_dp,
            "witness_in_generator_box": all(abs(value) <= 1 for value in fixed_witness),
            "visible_equality_residual": visible_residual,
            "all_nonzero_visible_primitives_fixed_at_support_sign": True,
            "remaining_free_primitives_have_zero_visible_coefficient": True,
        },
        "initial_endpoint_direction_interval": {
            "direction": "e_p+14h*e_v",
            "center": center,
            "free_halfwidth": free_halfwidth,
            "lower": lower,
            "upper": upper,
        },
        "fourteen_miss_balance": {
            "miss_count": MISS_COUNT,
            "positive_residual_shift": positive_residual_shift,
            "maximum_negative_control_shift": maximum_negative_control_shift,
            "residual_equals_h_times_control_authority": True,
            "certified_endpoint_lower_bound": endpoint_lower_bound,
            "position_limit": POSITION_LIMIT,
            "strict_position_violation": violation,
        },
    }


def run():
    return {
        "status": "pass",
        "claim": "reachable_extreme_visible_fiber_fifteen_tick_obstruction",
        **extreme_visible_fiber_certificate(),
        "allows_optimistic_full_state_causal_feedback": True,
        "rules_out_current_fifteen_tick_contract": True,
        "rules_out_other_seed_or_residual_contracts": False,
        "is_recursive_feasibility_proof": False,
        "full_six_state_guarantee": False,
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
        "verification/check_vertical_extreme_visible_fiber_obstruction.py",
        "verification/test_vertical_extreme_visible_fiber_obstruction.py",
        "verification/check_vertical_visible_fiber_width.py",
        "verification/check_vertical_correlated_return_seed.py",
        "verification/check_cycle_lifted_zonotope.py",
        "configs/planar_baseline.json",
        "docs/learning/101_vertical_extreme_visible_fiber_obstruction.md",
        "docs/literature/READ_PAPERS.md",
        "docs/research/run165_literature_gate.md",
        "docs/research/run165_research_log.md",
    ]
    result["source_sha256"] = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in sources
    }
    encoded = _encode(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(encoded, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": encoded["status"], "claim": encoded["claim"]}, indent=2))


if __name__ == "__main__":
    main()
