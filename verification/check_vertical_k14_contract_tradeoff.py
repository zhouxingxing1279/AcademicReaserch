#!/usr/bin/env python3
"""Exact necessary k=14 trade-off for the fixed J14 vertical contract."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

from check_cycle_lifted_zonotope import problem_data
from check_vertical_affine_rescue import _support
from check_vertical_multi_return_template import multi_return_template_certificate


POSITION_LIMIT = F(1)
H = F(1, 50)
ROOT = Path(__file__).resolve().parents[1]


def directional_half_diameter(positive_support, negative_support):
    """Return half the width of a set in a direction from its two supports."""
    return (positive_support + negative_support) / 2


def k14_tradeoff_certificate():
    miss_count = 14
    coefficient_sum = F(miss_count * (miss_count - 1), 2)
    template = multi_return_template_certificate()
    config, _, _, _, success_generators, _ = problem_data()
    generators = template["return_seeds"][14]["generators_by_row"]
    residual_column = success_generators[3][1]
    correction_limit = F(str(config["mpc"]["ancillary_correction_upper"][0]))

    seed_direction_support = _support([
        generators[2][column] + miss_count * H * generators[3][column]
        for column in range(len(generators[0]))
    ])
    residual_budget = coefficient_sum * H * residual_column
    input_budget = coefficient_sum * H * H * correction_limit
    if residual_budget != input_budget:
        raise AssertionError("baseline residual/input cancellation changed")
    residual_and_input_budget = residual_budget

    maximum_seed_scale = POSITION_LIMIT / seed_direction_support
    maximum_residual_scale = (
        POSITION_LIMIT - seed_direction_support + residual_and_input_budget
    ) / residual_and_input_budget
    minimum_input_scale = (
        seed_direction_support + residual_and_input_budget - POSITION_LIMIT
    ) / residual_and_input_budget
    return {
        "miss_count": miss_count,
        "seed_direction": "e_p+14h*e_v",
        "seed_direction_support": seed_direction_support,
        "residual_budget": residual_budget,
        "input_budget": input_budget,
        "residual_equals_h_times_input_authority": True,
        "residual_and_input_budget": residual_and_input_budget,
        "maximum_seed_scale": maximum_seed_scale,
        "minimum_seed_support_reduction": F(1) - maximum_seed_scale,
        "maximum_residual_scale": maximum_residual_scale,
        "minimum_residual_reduction": F(1) - maximum_residual_scale,
        "minimum_input_scale": minimum_input_scale,
        "minimum_input_increase": minimum_input_scale - F(1),
    }


def lower_bound(seed_scale, residual_scale, input_scale):
    result = k14_tradeoff_certificate()
    return (
        seed_scale * result["seed_direction_support"]
        + (residual_scale - input_scale) * result["residual_and_input_budget"]
    )


def run():
    return {
        "status": "pass",
        "claim": "exact_k14_three_factor_necessary_tradeoff",
        **k14_tradeoff_certificate(),
        "online_smf_directly_changes": (
            "realized_state_seed_directional_half_diameter"
        ),
        "online_smf_directly_changes_future_residual_set": False,
        "online_smf_changes_physical_input_authority": False,
        "necessary_condition_is_sufficient": False,
        "recursive_feasibility_certified": False,
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
        "verification/check_vertical_k14_contract_tradeoff.py",
        "verification/test_vertical_k14_contract_tradeoff.py",
        "verification/check_cycle_lifted_zonotope.py",
        "verification/check_vertical_affine_rescue.py",
        "verification/check_vertical_multi_return_template.py",
        "verification/check_vertical_correlated_return_seed.py",
        "verification/check_mode_radius.py",
        "verification/check_mode_nestedness.py",
        "verification/check_vertical_joint_predecessor.py",
        "verification/check_intermittent_metric.py",
        "configs/planar_baseline.json",
        "docs/learning/97_vertical_k14_contract_tradeoff.md",
        "docs/literature/READ_PAPERS.md",
        "docs/research/run161_literature_gate.md",
        "docs/research/run161_research_log.md",
    ]
    result["source_sha256"] = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in sources
    }
    encoded = _encode(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(encoded, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "status": encoded["status"],
        "claim": encoded["claim"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
