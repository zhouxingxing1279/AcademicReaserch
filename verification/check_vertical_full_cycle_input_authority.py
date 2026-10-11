#!/usr/bin/env python3
"""Policy-independent input-authority obstruction for the J14 15-tick return."""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

from check_cycle_lifted_zonotope import problem_data
from check_vertical_affine_rescue import _support
from check_vertical_multi_return_template import multi_return_template_certificate


H = F(1, 50)
POSITION_LIMIT = F(1)
ROOT = Path(__file__).resolve().parents[1]


def full_cycle_authority_certificate():
    template = multi_return_template_certificate()
    config, _, _, _, success_generators, _ = problem_data()
    generators = template["return_seeds"][14]["generators_by_row"]
    residual_column = success_generators[3][1]
    correction_limit = F(str(config["mpc"]["ancillary_correction_upper"][0]))

    steps = {}
    for miss_count in range(1, 15):
        zero_position_halfwidth = _support([
            generators[2][column] + miss_count * H * generators[3][column]
            for column in range(len(generators[0]))
        ]) + F(miss_count * (miss_count - 1), 2) * H * residual_column

        # For two mirrored admissible trajectories, every causal policy still
        # has |u_t^+ - u_t^-| <= 2 U.  Hence input can reduce half the position
        # diameter by at most sum_{j=1}^{k-1} j h^2 U.
        maximum_policy_reduction = (
            F(miss_count * (miss_count - 1), 2)
            * H * H * correction_limit
        )
        position_lower_bound = zero_position_halfwidth - maximum_policy_reduction
        steps[miss_count] = {
            "zero_correction_position_halfwidth": zero_position_halfwidth,
            "maximum_policy_reduction": maximum_policy_reduction,
            "position_lower_bound": position_lower_bound,
            "strict_excess": position_lower_bound - POSITION_LIMIT,
            "position_necessary_condition_satisfied": (
                position_lower_bound <= POSITION_LIMIT
            ),
        }

    first_infeasible = next(
        count for count, row in steps.items()
        if not row["position_necessary_condition_satisfied"]
    )
    if first_infeasible != 13:
        raise AssertionError("full-cycle input-authority obstruction changed")
    return {
        "source_seed": "J14",
        "required_cycle_length": 15,
        "correction_limit": correction_limit,
        "position_limit": POSITION_LIMIT,
        "first_infeasible_miss_count": first_infeasible,
        "steps": steps,
    }


def run():
    return {
        "status": "pass",
        "claim": "fixed_j14_seed_cannot_survive_a_fifteen_tick_return_under_the_current_correction_box",
        **full_cycle_authority_certificate(),
        "evidence_level": (
            "exact_policy_independent_full_cycle_position_diameter_obstruction"
        ),
        "arbitrary_causal_bounded_policy_ruled_out": True,
        "full_state_feedback_relaxation_ruled_out": True,
        "different_seed_ruled_out": False,
        "scheduled_residual_ruled_out": False,
        "is_rci_certificate": False,
        "recursive_feasibility_certified": False,
        "full_six_state_guarantee": False,
    }


def _encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, tuple):
        return [_encode(item) for item in value]
    if isinstance(value, list):
        return [_encode(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _encode(item) for key, item in value.items()}
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    result = run()
    sources = [
        "verification/check_vertical_full_cycle_input_authority.py",
        "verification/test_vertical_full_cycle_input_authority.py",
        "verification/check_cycle_lifted_zonotope.py",
        "verification/check_vertical_affine_rescue.py",
        "verification/check_vertical_multi_return_template.py",
        "verification/check_vertical_correlated_return_seed.py",
        "verification/check_mode_radius.py",
        "verification/check_mode_nestedness.py",
        "verification/check_vertical_joint_predecessor.py",
        "configs/planar_baseline.json",
        "docs/learning/96_vertical_full_cycle_input_authority.md",
        "docs/literature/READ_PAPERS.md",
        "docs/research/run160_literature_gate.md",
        "docs/research/run160_research_log.md",
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
        "evidence_level": encoded["evidence_level"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
