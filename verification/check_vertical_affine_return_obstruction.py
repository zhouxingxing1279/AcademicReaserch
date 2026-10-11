#!/usr/bin/env python3
"""Exact position-support obstruction on the rescued J14 return path."""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

from check_cycle_lifted_zonotope import problem_data
from check_vertical_affine_rescue import _support
from check_vertical_multi_return_template import multi_return_template_certificate
from check_vertical_translated_template_obstruction import _miss_image


H = F(1, 50)
POSITION_LIMIT = F(1)
ROOT = Path(__file__).resolve().parents[1]


def return_obstruction_certificate():
    template = multi_return_template_certificate()
    config, _, _, _, success_generators, _ = problem_data()
    residual_column = success_generators[3][1]
    correction_limit = F(str(config["mpc"]["ancillary_correction_upper"][0]))

    generators = template["return_seeds"][14]["generators_by_row"]
    for _ in range(8):
        generators = _miss_image(generators, residual_column)

    # From age 8 to mode 11 there are three misses.  Corrections selected at
    # ages 8 and 9 enter position with coefficients 2 h^2 and h^2;
    # the age-10 correction cannot affect the mode-11 position yet.
    zero_position_columns = [
        generators[2][column] + 3 * H * generators[3][column]
        for column in range(len(generators[0]))
    ]
    zero_correction_position_halfwidth = (
        _support(zero_position_columns) + 3 * H * residual_column
    )
    maximum_affine_support_reduction = 3 * H * H * correction_limit
    best_case_position_lower_bound = (
        zero_correction_position_halfwidth - maximum_affine_support_reduction
    )
    strict_position_excess = best_case_position_lower_bound - POSITION_LIMIT

    if strict_position_excess <= 0:
        raise AssertionError("position obstruction disappeared")
    return {
        "source_label": (8, 15),
        "checked_target_mode": 11,
        "miss_count": 3,
        "position_limit": POSITION_LIMIT,
        "correction_limit": correction_limit,
        "zero_correction_position_halfwidth": zero_correction_position_halfwidth,
        "maximum_affine_support_reduction": maximum_affine_support_reduction,
        "best_case_position_lower_bound": best_case_position_lower_bound,
        "strict_position_excess": strict_position_excess,
        "fixed_age_eight_source_affine_policy_class_infeasible": True,
    }


def run():
    return {
        "status": "pass",
        "claim": "fixed_j14_age_eight_source_violates_mode_eleven_position_under_two_bounded_affine_corrections",
        **return_obstruction_certificate(),
        "evidence_level": "exact_three_miss_position_support_lower_bound",
        "age_eight_source_fixed_after_zero_prior_corrections": True,
        "fixed_global_residual_assumed": True,
        "centered_affine_policy_only": True,
        "earlier_feedback_ruled_out": False,
        "general_output_feedback_infeasibility": False,
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
        "verification/check_vertical_affine_return_obstruction.py",
        "verification/test_vertical_affine_return_obstruction.py",
        "verification/check_cycle_lifted_zonotope.py",
        "verification/check_vertical_affine_rescue.py",
        "verification/check_vertical_multi_return_template.py",
        "verification/check_vertical_translated_template_obstruction.py",
        "configs/planar_baseline.json",
        "docs/learning/95_vertical_affine_return_obstruction.md",
        "docs/literature/READ_PAPERS.md",
        "docs/research/run159_literature_gate.md",
        "docs/research/run159_research_log.md",
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
