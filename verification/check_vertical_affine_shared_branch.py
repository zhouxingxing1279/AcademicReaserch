#!/usr/bin/env python3
"""Exact shared success/miss safety witness after the Run157 rescue."""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

from check_cycle_lifted_zonotope import problem_data
from check_vertical_affine_rescue import _support
from check_vertical_joint_predecessor import critical_mode_predecessors
from check_vertical_multi_return_template import multi_return_template_certificate
from check_vertical_translated_template_obstruction import _miss_image


ROOT = Path(__file__).resolve().parents[1]
H = F(1, 50)
POSITION_GAIN = F(9, 2)
TRACKING_LIMITS = (F(1), F(11, 4))


def _feedback_miss(generators, gain, residual_column):
    rows = [[], [], [], []]
    for column in range(len(generators[0])):
        eta_p, eta_v, e_p, e_v = (
            generators[row][column] for row in range(4)
        )
        d_v = e_v - eta_v
        values = (
            eta_p + H * eta_v,
            eta_v,
            e_p + H * e_v,
            e_v + H * gain * d_v,
        )
        for row, value in enumerate(values):
            rows[row].append(value)
    for row, value in enumerate((F(0), residual_column, F(0), residual_column)):
        rows[row].append(value)
    return rows


def _branch_image(generators, gain, residual_column, noise_column, label):
    success = label == "success"
    rows = [[], [], [], []]
    for column in range(len(generators[0])):
        eta_p, eta_v, e_p, e_v = (
            generators[row][column] for row in range(4)
        )
        d_v = e_v - eta_v
        values = (
            F(0) if success else eta_p + H * eta_v,
            (
                -POSITION_GAIN * eta_p
                + (1 - POSITION_GAIN * H) * eta_v
                if success else eta_v
            ),
            e_p + H * e_v,
            e_v + H * gain * d_v,
        )
        for row, value in enumerate(values):
            rows[row].append(value)
    for row, value in enumerate((F(0), residual_column, F(0), residual_column)):
        rows[row].append(value)
    if success:
        for row, value in enumerate((noise_column[0], noise_column[1], F(0), F(0))):
            rows[row].append(value)
    return rows


def shared_branch_certificate():
    template = multi_return_template_certificate()
    config, _, _, _, success_generators, _ = problem_data()
    residual_column = success_generators[3][1]
    noise_column = (success_generators[1][4], success_generators[3][4])
    correction_limit = F(str(config["mpc"]["ancillary_correction_upper"][0]))

    generators = template["return_seeds"][14]["generators_by_row"]
    for _ in range(8):
        generators = _miss_image(generators, residual_column)
    first_visible_velocity = [
        generators[3][column] - generators[1][column]
        for column in range(len(generators[0]))
    ]
    first_gain = -correction_limit / _support(first_visible_velocity)
    mode_nine = _feedback_miss(generators, first_gain, residual_column)

    visible_velocity = [
        mode_nine[3][column] - mode_nine[1][column]
        for column in range(len(mode_nine[0]))
    ]
    visible_velocity_halfwidth = _support(visible_velocity)
    velocity_gain = -correction_limit / visible_velocity_halfwidth
    input_support = _support([velocity_gain * value for value in visible_velocity])

    full_envelope_edges = {
        edge["label"]: edge
        for edge in critical_mode_predecessors()["modes"][9]["edges"]
    }
    branches = {}
    for label in ("miss", "success"):
        image = _branch_image(
            mode_nine,
            velocity_gain,
            residual_column,
            noise_column,
            label,
        )
        tracking_halfwidths = (_support(image[2]), _support(image[3]))
        edge = full_envelope_edges[label]
        branches[label] = {
            "target_mode": edge["target"],
            "tracking_position_halfwidth": tracking_halfwidths[0],
            "tracking_velocity_halfwidth": tracking_halfwidths[1],
            "tracking_hard_box_satisfied": all(
                support <= limit
                for support, limit in zip(tracking_halfwidths, TRACKING_LIMITS)
            ),
            "estimator_target_contained": edge["eta_target_contained"],
            "estimator_containment_inherited_from_full_mode_nine_envelope": True,
        }

    if not (
        input_support == correction_limit
        and all(row["tracking_hard_box_satisfied"] for row in branches.values())
        and all(row["estimator_target_contained"] for row in branches.values())
        and branches["miss"]["tracking_position_halfwidth"]
        == branches["success"]["tracking_position_halfwidth"]
        and branches["miss"]["tracking_velocity_halfwidth"]
        == branches["success"]["tracking_velocity_halfwidth"]
    ):
        raise AssertionError("shared branch witness changed")
    return {
        "source_label": (9, 15),
        "position_gain": F(0),
        "velocity_gain": velocity_gain,
        "visible_velocity_halfwidth": visible_velocity_halfwidth,
        "input_support": input_support,
        "correction_limit": correction_limit,
        "branch_policy_count": 1,
        "branches": branches,
    }


def run():
    return {
        "status": "pass",
        "claim": "rescued_mode_nine_set_has_one_affine_policy_safe_for_success_and_miss",
        **shared_branch_certificate(),
        "evidence_level": (
            "exact_one_step_shared_success_miss_safety_witness_after_affine_rescue"
        ),
        "shared_branch_state_input_safety_certified": True,
        "recurrent_target_inclusion_certified": False,
        "gain_optimality_claimed": False,
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
        "verification/check_vertical_affine_shared_branch.py",
        "verification/test_vertical_affine_shared_branch.py",
        "verification/check_vertical_affine_rescue.py",
        "verification/check_vertical_joint_predecessor.py",
        "verification/check_vertical_multi_return_template.py",
        "configs/planar_baseline.json",
        "docs/learning/94_vertical_affine_shared_branch.md",
        "docs/literature/READ_PAPERS.md",
        "docs/research/run158_literature_gate.md",
        "docs/research/run158_research_log.md",
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
