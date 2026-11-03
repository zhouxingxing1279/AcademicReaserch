#!/usr/bin/env python3
"""Exact correlated return seed for the required initialization path.

The contract initializes mode 0 with ``d = e - eta = 0``.  Fourteen
consecutive miss edges therefore preserve one common visible offset while the
full hidden estimator-error zonotope reaches mode 14.  This checker maps that
entire fiber through the forced ``14 -> 0`` success edge while preserving the
shared residual and measurement-noise primitives in ``(eta, e)`` coordinates.

The result is a necessary reachable seed, not a controlled-invariant set.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

from check_cycle_lifted_zonotope import (
    CYCLE_LENGTHS,
    age_zonotopes,
    diagonal,
    least_mode_zero_box,
    lift_cycle,
    problem_data,
)
from check_mode_radius import propagate_generators
from check_vertical_joint_first_sweep import first_sweep_inner_certificates
from check_vertical_joint_predecessor import H, POSITION_GAIN, _tracking_limits
from check_vertical_joint_second_sweep import _q_halfwidth


ROOT = Path(__file__).resolve().parents[1]


def _row_support(row):
    return sum((abs(value) for value in row), F(0))


def _matrix_rank(matrix):
    """Exact Gaussian-elimination rank over the rationals."""
    work = [list(map(F, row)) for row in matrix]
    rows = len(work)
    columns = len(work[0]) if work else 0
    rank = 0
    for column in range(columns):
        pivot = next(
            (row for row in range(rank, rows) if work[row][column]), None
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][column]
        work[rank] = [value / scale for value in work[rank]]
        for row in range(rows):
            if row == rank or not work[row][column]:
                continue
            scale = work[row][column]
            work[row] = [
                value - scale * pivot_value
                for value, pivot_value in zip(work[row], work[rank])
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def _independent_generator_indices(rows):
    selected = []
    current_rank = 0
    for column in range(len(rows[0])):
        candidate = selected + [column]
        candidate_rank = _matrix_rank(
            [[row[index] for index in candidate] for row in rows]
        )
        if candidate_rank > current_rank:
            selected.append(column)
            current_rank = candidate_rank
        if current_rank == len(rows):
            break
    return tuple(selected)


def _return_generators(mode14, success_noise_column, success_residual_column):
    """Return exact columns in coordinates ``(eta_p, eta_v, e_p, e_v)``."""
    columns = []
    for column in range(len(mode14[0])):
        eta_p = mode14[1][column]
        eta_v = mode14[3][column]
        columns.append((
            F(0),
            -POSITION_GAIN * eta_p + (1 - POSITION_GAIN * H) * eta_v,
            eta_p + H * eta_v,
            eta_v,
        ))

    # The same physical residual realization enters eta_v+ and e_v+.
    columns.append((F(0), success_residual_column, F(0), success_residual_column))
    # The same next measurement noise enters both estimator coordinates and
    # cancels from the true tracking error.
    columns.append((
        success_noise_column[0],
        success_noise_column[1],
        F(0),
        F(0),
    ))
    return [list(row) for row in zip(*columns)]


def correlated_return_seed():
    config, A0, G0, A1, G1, _ = problem_data()
    cycles = [lift_cycle(length, A0, G0, A1, G1) for length in CYCLE_LENGTHS]
    mode_zero_box = least_mode_zero_box(cycles)
    zonotopes = age_zonotopes(mode_zero_box, A0, G0)

    reached = diagonal(mode_zero_box)
    for _ in range(14):
        reached = propagate_generators(A0, reached, G0)
    mode14_reached_exactly = reached == zonotopes[14]

    graph = config["mpc"]["ancillary_rci_contract"]["mode_graph"]["edges"]
    miss_chain = [(source, target, label) for source, target, label in graph
                  if source < 14 and target == source + 1 and label == "miss"]
    forced_return = (14, 0, "success") in [tuple(edge) for edge in graph]

    noise_column = (G1[1][4], G1[3][4])
    residual_column = G1[3][1]
    rows = _return_generators(zonotopes[14], noise_column, residual_column)
    eta_support = tuple(_row_support(row) for row in rows[:2])
    tracking_support = tuple(_row_support(row) for row in rows[2:])
    d_rows = [
        [rows[2][column] - rows[0][column] for column in range(len(rows[0]))],
        [rows[3][column] - rows[1][column] for column in range(len(rows[0]))],
    ]
    d_support = tuple(_row_support(row) for row in d_rows)

    eta_limits = (mode_zero_box[1], mode_zero_box[3])
    tracking_limits = _tracking_limits(config)
    eta_slack = tuple(limit - support for limit, support in zip(eta_limits, eta_support))
    tracking_slack = tuple(
        limit - support for limit, support in zip(tracking_limits, tracking_support)
    )

    product_velocity_limit = max(
        abs(vertex[1])
        for vertex in first_sweep_inner_certificates()["modes"][0][
            "observation_projection_vertices"
        ]
    )
    strict_excess = d_support[1] - product_velocity_limit
    rank = _matrix_rank(rows)
    independent = _independent_generator_indices(rows)
    shared_line_relation = all(
        d_rows[1][column] == POSITION_GAIN * d_rows[0][column]
        for column in range(len(rows[0]))
    )

    if not (
        len(miss_chain) == 14
        and forced_return
        and mode14_reached_exactly
        and all(slack >= 0 for slack in eta_slack)
        and all(slack >= 0 for slack in tracking_slack)
        and rank == 3
        and len(independent) == 3
        and shared_line_relation
        and strict_excess > 0
    ):
        raise AssertionError("correlated return-seed certificate changed")

    return {
        "initialization_reachability": {
            "initial_mode": 0,
            "initial_visible_offset": F(0),
            "miss_edge_count": len(miss_chain),
            "forced_return_edge_present": forced_return,
            "mode14_zonotope_reached_exactly": mode14_reached_exactly,
            "visible_offset_independent_of_hidden_eta": True,
            "mode14_q_halfwidth": _q_halfwidth(zonotopes[14]),
        },
        "return_seed": {
            "coordinates": ("eta_p", "eta_v", "e_p", "e_v"),
            "source_generator_count": len(zonotopes[14][0]),
            "generator_count": len(rows[0]),
            "generators_by_row": rows,
            "affine_hull_dimension": rank,
            "independent_generator_indices": independent,
            "shared_residual_primitive": (
                rows[1][-2] == rows[3][-2] == residual_column
            ),
            "shared_measurement_primitive": (
                rows[0][-1] == noise_column[0]
                and rows[1][-1] == noise_column[1]
                and rows[2][-1] == rows[3][-1] == 0
            ),
            "all_generators_satisfy_dv_equals_L_dp": shared_line_relation,
            "eta_support": eta_support,
            "eta_mode0_vertical_limits": eta_limits,
            "eta_mode0_slack": eta_slack,
            "tracking_error_support": tracking_support,
            "tracking_error_limits": tracking_limits,
            "tracking_error_slack": tracking_slack,
            "eta_projection_in_mode0_vertical_box": all(
                slack >= 0 for slack in eta_slack
            ),
            "tracking_error_projection_in_hard_box": all(
                slack >= 0 for slack in tracking_slack
            ),
        },
        "product_target_comparison": {
            "return_d_support": d_support,
            "run146_product_d0_velocity_halfwidth": product_velocity_limit,
            "strict_velocity_excess": strict_excess,
            "violates_run146_product_d0_velocity_bound": strict_excess > 0,
            "accepted_by_correlated_true_error_target": all(
                slack >= 0 for slack in tracking_slack
            ),
        },
    }


def run():
    certificate = correlated_return_seed()
    return {
        "status": "pass",
        "claim": "required_initialization_path_has_an_exact_rank_three_correlated_return_seed",
        **certificate,
        "evidence_level": (
            "exact_rank_three_correlated_return_seed_for_required_initialization_path"
        ),
        "run146_next_problem_rejected_as_duplicate": True,
        "required_return_seed_certified": True,
        "is_rci_certificate": False,
        "full_six_state_guarantee": False,
        "limitations": [
            "the certificate covers only the vertical projection of one required return path",
            "the rank-three reachable seed is not a positive-volume four-dimensional candidate",
            "no controlled predecessor or invariant fixed point is synthesized",
            "horizontal, attitude, torque, terminal, shift, and recursive MPC feasibility remain open",
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
        "verification/check_vertical_correlated_return_seed.py",
        "verification/test_vertical_correlated_return_seed.py",
        "verification/check_vertical_joint_second_sweep.py",
        "verification/check_vertical_joint_first_sweep.py",
        "verification/check_vertical_joint_predecessor.py",
        "verification/check_cycle_lifted_zonotope.py",
        "verification/check_mode_nestedness.py",
        "verification/check_mode_radius.py",
        "configs/planar_baseline.json",
        "docs/learning/84_vertical_correlated_return_seed.md",
        "docs/literature/READ_PAPERS.md",
        "docs/research/run147_literature_gate.md",
        "docs/research/run147_research_log.md",
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
        "affine_hull_dimension": encoded["return_seed"]["affine_hull_dimension"],
        "evidence_level": encoded["evidence_level"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
