#!/usr/bin/env python3
"""Exact visible-coordinate composability audit for Run180/181 cells.

The prior certificates close estimator and tracking target normals.  This
checker asks the separate graph question: does ``d+=e+-eta+`` enter the same
centered visible box used to define the advertised target source cell?
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

from check_mode0_miss_lifted_cell import mode0_miss_certificate
from check_mode4_unknown_branch_lifted_cell import mode4_unknown_branch_certificate
from check_vertical_joint_predecessor import H, OBSERVATION_HALFWIDTHS


ROOT = Path(__file__).resolve().parents[1]


def _edge_row(source_mode, target_mode, edge_label, d_position_support, d_velocity_support):
    target_position, target_velocity = OBSERVATION_HALFWIDTHS
    position_excess = d_position_support - target_position
    velocity_excess = d_velocity_support - target_velocity
    return {
        "source_mode": source_mode,
        "target_mode": target_mode,
        "edge_label": edge_label,
        "d_position_support": d_position_support,
        "d_velocity_support": d_velocity_support,
        "target_d_position_halfwidth": target_position,
        "target_d_velocity_halfwidth": target_velocity,
        "position_excess_over_target_cell": position_excess,
        "velocity_excess_over_target_cell": velocity_excess,
        "contained_in_equal_centered_target_d_cell": (
            position_excess <= 0 and velocity_excess <= 0
        ),
    }


def _visible_support_from_joint_columns(columns):
    position = sum(abs(column["vector"][2] - column["vector"][0]) for column in columns)
    velocity = sum(abs(column["vector"][3] - column["vector"][1]) for column in columns)
    return position, velocity


def composability_certificate():
    run180 = mode0_miss_certificate()
    run181 = mode4_unknown_branch_certificate()
    d_position, d_velocity = OBSERVATION_HALFWIDTHS

    edges = [
        _edge_row(
            0,
            1,
            "miss",
            d_position + H * d_velocity,
            d_velocity,
        )
    ]
    for branch in run181["branches"]:
        supports = _visible_support_from_joint_columns(branch["joint_primitive_columns"])
        edges.append(_edge_row(4, branch["target_mode"], branch["edge_label"], *supports))

    if any(row["contained_in_equal_centered_target_d_cell"] for row in edges):
        raise AssertionError("the expected three noncontainment rows were not all reproduced")

    return {
        "source_visible_cell": "|d_p|<=1/5, |d_v|<=1/4",
        "visible_relation": "d=e-eta",
        "run180_local_target_normals_closed": run180["one_edge_closed"],
        "run181_local_target_normals_closed": run181["both_unknown_branches_closed"],
        "edges": edges,
        "existing_cells_form_a_composable_graph": False,
    }


def run():
    return {
        "status": "pass",
        "claim": "run180_and_run181_local_cells_do_not_compose_under_their_equal_centered_d_box",
        **composability_certificate(),
        "evidence_level": "exact_visible_successor_support_noncontainment_certificate",
        "finite_cell_cover_impossible": False,
        "translated_or_larger_cells_ruled_out": False,
        "piecewise_affine_policy_ruled_out": False,
        "terminal_family_closed": False,
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
        "verification/check_lifted_cell_composability.py",
        "verification/test_lifted_cell_composability.py",
        "verification/check_mode0_miss_lifted_cell.py",
        "verification/check_mode4_unknown_branch_lifted_cell.py",
        "verification/check_vertical_joint_predecessor.py",
        "configs/planar_baseline.json",
        "docs/learning/116_lifted_cell_composability_gap.md",
        "docs/literature/READ_PAPERS.md",
        "docs/research/run182_literature_gate.md",
        "docs/research/run182_research_log.md",
    ]
    result["source_sha256"] = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in sources
    }
    encoded = _encode(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(encoded, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "status": encoded["status"],
        "claim": encoded["claim"],
        "edge_supports": [
            {
                "edge": [row["source_mode"], row["target_mode"], row["edge_label"]],
                "d_position_support": row["d_position_support"],
                "d_velocity_support": row["d_velocity_support"],
            }
            for row in encoded["edges"]
        ],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
