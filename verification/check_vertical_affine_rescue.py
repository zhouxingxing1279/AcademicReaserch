#!/usr/bin/env python3
"""Exact one-step affine-in-visible-velocity rescue witnesses.

The two witnesses act on the predecessor immediately before the first
zero-policy velocity violation found in Run156.  They establish only robust
one-step state/input feasibility; no target-family inclusion or invariance is
claimed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

from check_cycle_lifted_zonotope import problem_data
from check_vertical_multi_return_template import multi_return_template_certificate
from check_vertical_translated_template_obstruction import _miss_image


ROOT = Path(__file__).resolve().parents[1]
H = F(1, 50)
TRUE_VELOCITY_LIMIT = F(11, 4)
CRITICAL_CASES = {9: 14, 14: 9}


def _support(values):
    return sum((abs(value) for value in values), F(0))


def affine_rescue_certificate():
    template = multi_return_template_certificate()
    config, _, _, _, success_generators, _ = problem_data()
    residual_column = success_generators[3][1]
    correction_limit = F(str(config["mpc"]["ancillary_correction_upper"][0]))

    rows = {}
    for seed_mode, failure_miss_count in CRITICAL_CASES.items():
        generators = template["return_seeds"][seed_mode]["generators_by_row"]
        predecessor_age = failure_miss_count - 1
        for _ in range(predecessor_age):
            generators = _miss_image(generators, residual_column)

        visible_velocity = [
            generators[3][column] - generators[1][column]
            for column in range(len(generators[0]))
        ]
        visible_velocity_halfwidth = _support(visible_velocity)
        velocity_gain = -correction_limit / visible_velocity_halfwidth
        input_columns = [velocity_gain * value for value in visible_velocity]
        input_support = _support(input_columns)
        successor_velocity_columns = [
            generators[3][column] + H * input_columns[column]
            for column in range(len(generators[0]))
        ]
        successor_velocity_halfwidth = (
            _support(successor_velocity_columns) + residual_column
        )
        zero_policy_successor_halfwidth = (
            _support(generators[3]) + residual_column
        )
        velocity_margin = TRUE_VELOCITY_LIMIT - successor_velocity_halfwidth

        rows[seed_mode] = {
            "failure_miss_count": failure_miss_count,
            "predecessor_age": predecessor_age,
            "edge": (predecessor_age, predecessor_age + 1, "miss"),
            "position_gain": F(0),
            "velocity_gain": velocity_gain,
            "visible_velocity_halfwidth": visible_velocity_halfwidth,
            "input_support": input_support,
            "correction_limit": correction_limit,
            "robust_input_box_satisfied": input_support <= correction_limit,
            "zero_policy_successor_velocity_halfwidth": (
                zero_policy_successor_halfwidth
            ),
            "successor_velocity_halfwidth": successor_velocity_halfwidth,
            "velocity_margin": velocity_margin,
            "successor_true_velocity_box_satisfied": velocity_margin >= 0,
        }

    if not all(
        row["input_support"] == row["correction_limit"]
        and row["zero_policy_successor_velocity_halfwidth"] > TRUE_VELOCITY_LIMIT
        and row["successor_true_velocity_box_satisfied"]
        for row in rows.values()
    ):
        raise AssertionError("affine rescue witness changed")
    return {
        "critical_predecessors": rows,
        "true_velocity_limit": TRUE_VELOCITY_LIMIT,
    }


def run():
    certificate = affine_rescue_certificate()
    return {
        "status": "pass",
        "claim": "two_critical_zero_policy_velocity_excesses_have_exact_one_step_affine_rescues",
        **certificate,
        "failure_miss_counts": dict(CRITICAL_CASES),
        "rescue_source_ages": {
            seed: count - 1 for seed, count in CRITICAL_CASES.items()
        },
        "rescue_edges_are_deterministic_miss_edges": True,
        "same_step_success_miss_branching_required": False,
        "critical_zero_policy_excess_eliminated": True,
        "evidence_level": (
            "exact_one_step_affine_in_visible_velocity_rescue_witness"
        ),
        "gain_optimality_claimed": False,
        "target_inclusion_certified": False,
        "shared_branch_successor_certified": False,
        "is_rci_certificate": False,
        "recursive_feasibility_certified": False,
        "full_six_state_guarantee": False,
        "limitations": [
            "the witnesses cover only the two predecessor sets immediately before Run156 failures",
            "the gains saturate the frozen correction box and are not claimed optimal",
            "the rescued sets are not proved contained in a recurrent target family",
            "the later mode-9 shared success/miss decision is not synthesized",
            "horizontal, attitude, terminal, and MPC shift feasibility remain open",
        ],
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
        "verification/check_vertical_affine_rescue.py",
        "verification/test_vertical_affine_rescue.py",
        "verification/check_vertical_multi_return_template.py",
        "verification/check_vertical_translated_template_obstruction.py",
        "configs/planar_baseline.json",
        "docs/learning/93_vertical_affine_rescue_witness.md",
        "docs/literature/READ_PAPERS.md",
        "docs/research/run157_literature_gate.md",
        "docs/research/run157_research_log.md",
    ]
    result["source_sha256"] = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in sources
    }
    encoded = _encode(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(encoded, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps({
        "status": encoded["status"],
        "claim": encoded["claim"],
        "evidence_level": encoded["evidence_level"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
