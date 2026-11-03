#!/usr/bin/env python3
"""Audit the chapter-48 19-pair cone with scheduling-visible vertex torque.

The full corrected LP is a floating-point diagnostic.  The final obstruction
is a sparse Farkas circuit reconstructed with Fraction arithmetic in the
expanded space containing a separate torque at each thrust endpoint.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
from fractions import Fraction as F
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import linprog

import check_19pair_cc_seed_cone as cc


SUPPORT = [
    ("config", 15, 5, None),
    ("config", 17, 5, None),
    ("config", 60, 4, None),
    ("config", 62, 4, None),
    ("inv", 3, 5, "981/200"),
    ("inv", 20, 11, "981/200"),
    ("inv", 34, 11, "981/200"),
    ("inv", 35, 11, "981/200"),
    ("inv", 40, 4, "981/200"),
    ("inv", 48, 6, "2943/200"),
    ("inv", 48, 34, "2943/200"),
    ("inv", 65, 10, "981/200"),
    ("inv", 72, 10, "981/200"),
    ("inv", 73, 10, "981/200"),
    ("inv", 81, 6, "981/200"),
    ("inv", 81, 20, "981/200"),
    ("inv", 87, 7, "981/200"),
    ("inv", 87, 21, "981/200"),
    ("inv", 96, 7, "2943/200"),
    ("inv", 96, 25, "2943/200"),
    ("inv", 96, 35, "2943/200"),
    ("inv", 102, 6, "2943/200"),
    ("inv", 102, 24, "2943/200"),
    ("hard", 0, 3, 1),
]

MULTIPLIERS = [
    F(200, 27), F(200, 27), F(100, 27), F(100, 27), F(400, 9),
    F(2000000, 26487), F(2000000, 26487), F(1000000, 26487), F(200, 9),
    F(32, 9), F(16000000, 79461), F(1000000, 26487), F(1000000, 26487),
    F(500000, 26487), F(1, 9), F(500000, 8829), F(2, 9),
    F(1000000, 8829), F(64, 27), F(8000000, 79461), F(8000000, 79461),
    F(8, 27), F(4000000, 79461), F(1),
]

EXPECTED_ACTS = {
    0: [0, 3, 5, 6],
    3: [0, 3, 7, 11],
    15: [0, 6, 11, 19],
    17: [0, 6, 19, 33],
    20: [0, 6, 25, 35],
    34: [0, 21, 23, 25],
    35: [0, 21, 23, 33],
    40: [1, 2, 6, 10],
    48: [1, 5, 6, 34],
    60: [1, 7, 10, 18],
    62: [1, 7, 18, 32],
    65: [1, 7, 24, 34],
    72: [1, 20, 22, 24],
    73: [1, 20, 22, 32],
    81: [2, 7, 10, 30],
    87: [3, 6, 11, 31],
    96: [4, 7, 31, 35],
    102: [5, 6, 30, 34],
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _assert_frozen_contract(root: Path) -> dict:
    config = json.loads((root / "configs/planar_baseline.json").read_text())
    assert F(str(config["plant"]["dt_s"])) == cc.base.h
    assert F(str(config["plant"]["inertia_kg_m2"])) == cc.base.J
    assert F(str(config["domain"]["input_lower"][0])) == cc.base.TL
    assert F(str(config["domain"]["input_upper"][0])) == cc.base.TU
    assert F(str(config["domain"]["input_lower"][1])) == -cc.base.taum
    assert F(str(config["domain"]["input_upper"][1])) == cc.base.taum
    state_lower = config["domain"]["state_lower"]
    state_upper = config["domain"]["state_upper"]
    assert [F(str(state_lower[index])) for index in (0, 2, 4, 5)] == [
        F(-5), F(-3), F("-0.45"), F(-2)
    ]
    assert [F(str(state_upper[index])) for index in (0, 2, 4, 5)] == [
        F(5), F(3), F("0.45"), F(2)
    ]
    return config


def _seed_geometry():
    s2 = cc.build_s2()
    reps = cc.orientation_reps(s2)
    halfspaces = cc.seed_H(reps)
    c_float, q_float, vertices, active_sets = cc.enumerate_vertices(halfspaces)
    assert len(halfspaces) == 38
    assert len(vertices) == 160
    assert all(len(active) == 4 for active in active_sets)
    for vertex, expected in EXPECTED_ACTS.items():
        assert active_sets[vertex] == expected
    return halfspaces, c_float, active_sets


def build_scheduling_visible_lp(include_torque_bounds: bool) -> dict:
    """Build and solve the corrected endpoint-specific vertex-control LP."""
    halfspaces, c_float, active_sets = _seed_geometry()
    nq = len(halfspaces)
    nv = len(active_sets)
    nvar = nq + 2 * nv
    maps = []
    for active in active_sets:
        matrix = np.zeros((4, nq))
        matrix[:, active] = np.linalg.inv(c_float[active, :])
        maps.append(matrix)

    rows = []
    rhs = []
    for vertex_map in maps:
        product = c_float @ vertex_map
        for facet in range(nq):
            row = np.zeros(nvar)
            row[:nq] = product[facet]
            row[facet] -= 1.0
            rows.append(row)
            rhs.append(0.0)
    configuration_rows = len(rows)

    input_vector = np.array([float(value) for value in cc.base.B])
    disturbance_vector = np.array([float(value) for value in cc.base.E])
    endpoints = (cc.base.TL, cc.base.TU)
    for vertex, vertex_map in enumerate(maps):
        for facet in range(nq):
            normal = c_float[facet]
            input_coefficient = normal @ input_vector
            for endpoint, thrust in enumerate(endpoints):
                dynamics = np.array(
                    [[float(value) for value in matrix_row] for matrix_row in cc.base.A(thrust)]
                )
                support = abs(normal @ disturbance_vector) * float(
                    cc.base.d0 + cc.base.c * thrust
                )
                row = np.zeros(nvar)
                row[:nq] = normal @ dynamics @ vertex_map
                row[facet] -= 1.0
                row[nq + 2 * vertex + endpoint] = input_coefficient
                rows.append(row)
                rhs.append(-support)
    configuration_plus_invariance_rows = len(rows)

    for vertex_map in maps:
        for coordinate, bound in enumerate((5.0, 3.0, 0.45, 2.0)):
            for sign in (1.0, -1.0):
                normal = np.zeros(4)
                normal[coordinate] = sign
                row = np.zeros(nvar)
                row[:nq] = normal @ vertex_map
                rows.append(row)
                rhs.append(bound)

    equalities = []
    for pair in range(19):
        row = np.zeros(nvar)
        row[2 * pair] = 1.0
        row[2 * pair + 1] = -1.0
        equalities.append(row)
    torque_bound = float(cc.base.taum) if include_torque_bounds else None
    bounds = [(0.0, None)] * nq + [
        (-torque_bound, torque_bound) if torque_bound is not None else (None, None)
    ] * (2 * nv)
    solution = linprog(
        np.zeros(nvar),
        A_ub=np.array(rows),
        b_ub=np.array(rhs),
        A_eq=np.array(equalities),
        b_eq=np.zeros(19),
        bounds=bounds,
        method="highs",
    )
    return {
        "feasible": bool(solution.success),
        "solver_status": int(solution.status),
        "solver_message": solution.message,
        "offset_variables": nq,
        "state_vertices": nv,
        "torque_variables": 2 * nv,
        "variables": nvar,
        "configuration_inequalities": configuration_rows,
        "configuration_plus_invariance_inequalities": configuration_plus_invariance_rows,
        "total_inequalities_with_hard_state": len(rows),
        "pair_offset_equalities": len(equalities),
    }


def _inverse(matrix: list[list[F]]) -> list[list[F]]:
    size = len(matrix)
    augmented = [row[:] + [F(i == j) for j in range(size)] for i, row in enumerate(matrix)]
    for column in range(size):
        pivot = next(i for i in range(column, size) if augmented[i][column])
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(size):
            if row == column or not augmented[row][column]:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                augmented[row][j] - factor * augmented[column][j]
                for j in range(2 * size)
            ]
    return [row[size:] for row in augmented]


def _rank(matrix: list[list[F]]) -> int:
    work = [row[:] for row in matrix]
    rank = 0
    columns = len(work[0]) if work else 0
    for column in range(columns):
        pivot = next((i for i in range(rank, len(work)) if work[i][column]), None)
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        scale = work[rank][column]
        work[rank] = [value / scale for value in work[rank]]
        for row in range(len(work)):
            if row == rank or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [
                work[row][j] - factor * work[rank][j] for j in range(columns)
            ]
        rank += 1
        if rank == len(work):
            break
    return rank


def verify_exact_certificate() -> dict:
    halfspaces, _, active_sets = _seed_geometry()
    exact_normals = [[F(value) for value in normal] for normal, _ in halfspaces]
    nq = 38
    nv = 160
    nvar = nq + 2 * nv

    def vertex_map(vertex: int):
        active = active_sets[vertex]
        inverse = _inverse([[exact_normals[row][column] for column in range(4)] for row in active])
        point = [sum(inverse[i][j] * halfspaces[active[j]][1] for j in range(4)) for i in range(4)]
        assert all(
            sum(normal[i] * point[i] for i in range(4)) <= bound
            for normal, bound in halfspaces
        )
        return active, inverse

    def selected_row(meta):
        kind, vertex, target, endpoint_or_sign = meta
        active, inverse = vertex_map(vertex)
        row = [F(0)] * nvar
        if kind == "config":
            for coordinate in range(4):
                for local, column in enumerate(active):
                    row[column] += exact_normals[target][coordinate] * inverse[coordinate][local]
            row[target] -= 1
            bound = F(0)
        elif kind == "inv":
            thrust = F(endpoint_or_sign)
            propagated = cc.base.mm(exact_normals[target], cc.base.A(thrust))
            for coordinate in range(4):
                for local, column in enumerate(active):
                    row[column] += propagated[coordinate] * inverse[coordinate][local]
            row[target] -= 1
            endpoint = 0 if thrust == cc.base.TL else 1
            row[nq + 2 * vertex + endpoint] = sum(
                exact_normals[target][i] * cc.base.B[i] for i in range(4)
            )
            bound = -abs(
                sum(exact_normals[target][i] * cc.base.E[i] for i in range(4))
            ) * (cc.base.d0 + cc.base.c * thrust)
        else:
            coordinate = target
            sign = F(endpoint_or_sign)
            for local, column in enumerate(active):
                row[column] += sign * inverse[coordinate][local]
            bound = (F(5), F(3), F("0.45"), F(2))[coordinate]
        return row, bound

    rows = []
    bounds = []
    for metadata in SUPPORT:
        row, bound = selected_row(metadata)
        rows.append(row)
        bounds.append(bound)
    weighted_lhs = [
        sum(MULTIPLIERS[i] * rows[i][column] for i in range(len(rows)))
        for column in range(nvar)
    ]
    weighted_rhs = sum(MULTIPLIERS[i] * bounds[i] for i in range(len(rows)))
    low_residuals = weighted_lhs[nq::2]
    high_residuals = weighted_lhs[nq + 1::2]
    assert all(value > 0 for value in MULTIPLIERS)
    assert all(value == 0 for value in weighted_lhs)
    assert weighted_rhs == F(-3069803, 88290)
    return {
        "support_rows": len(rows),
        "coefficient_rank": _rank(rows),
        "all_multipliers_strictly_positive": all(value > 0 for value in MULTIPLIERS),
        "weighted_lhs_zero_exact": all(value == 0 for value in weighted_lhs),
        "nonzero_weighted_lhs_coefficients": sum(value != 0 for value in weighted_lhs),
        "weighted_rhs": str(weighted_rhs),
        "weighted_rhs_float": float(weighted_rhs),
        "endpoint_torque_coefficients_checked": len(low_residuals) + len(high_residuals),
        "nonzero_low_endpoint_torque_residuals": sum(value != 0 for value in low_residuals),
        "nonzero_high_endpoint_torque_residuals": sum(value != 0 for value in high_residuals),
        "torque_bound_rows_used": 0,
        "pair_offset_equality_rows_used": 0,
        "q_nonnegativity_rows_used": 0,
        "multipliers": [str(value) for value in MULTIPLIERS],
        "support": [
            {
                "row": list(metadata),
                "active_set": active_sets[metadata[1]],
                "multiplier": str(multiplier),
            }
            for metadata, multiplier in zip(SUPPORT, MULTIPLIERS)
        ],
    }


def build_report(root: Path) -> dict:
    _assert_frozen_contract(root)
    bounded = build_scheduling_visible_lp(include_torque_bounds=True)
    unbounded = build_scheduling_visible_lp(include_torque_bounds=False)
    certificate = verify_exact_certificate()
    dependencies = [
        "configs/planar_baseline.json",
        "verification/check_s3_minimal_normal_cover.py",
        "verification/check_19pair_cc_seed_cone.py",
        "verification/check_scheduling_visible_19pair_farkas.py",
        "verification/test_scheduling_visible_19pair_farkas.py",
        "docs/research/run195_literature_gate.md",
        "docs/superpowers/specs/2026-10-28-scheduling-visible-19pair-farkas-design.md",
    ]
    return {
        "claim": "the audited parameter-independent 19-pair configuration cone remains infeasible with separate current-thrust-visible endpoint vertex torques",
        "scope": "four-state reduced lateral-attitude benchmark and the chapter-48 audited 19-pair cone only",
        "evidence_level": "COUNTEREXAMPLE",
        "corrected_quantifier": "for each state vertex and measured current-thrust endpoint, choose a separate torque; robustly cover the corresponding disturbance set",
        "endpoint_reduction": "affine dynamics, affine endpoint-torque interpolation, and affine W(T) support make the two endpoint checks sufficient over the frozen thrust interval",
        "corrected_lp": {
            **{key: value for key, value in bounded.items() if key not in ("feasible", "solver_status", "solver_message")},
            "bounded_torque_0p08_feasible": bounded["feasible"],
            "unbounded_endpoint_torque_feasible": unbounded["feasible"],
            "bounded_solver_status": bounded["solver_status"],
            "unbounded_solver_status": unbounded["solver_status"],
            "evidence_level": "NUMERIC_CHECK",
        },
        "exact_certificate": certificate,
        "proves_general_rci_nonexistence": False,
        "proves_six_state_safety": False,
        "proves_recursive_feasibility": False,
        "gate_A_status": "blocked",
        "interpretation": [
            "The old shared-torque proof did not match the measured-current-thrust information pattern; this certificate is checked in the expanded 358-variable space.",
            "The circuit uses no torque-bound row, so actuator saturation is not the cause of this candidate's contradiction.",
            "Other normal families, parameter-dependent offsets, non-polytopic sets, and the six-state embedding remain open.",
        ],
        "dependencies_sha256": {
            relative: _sha256(root / relative) for relative in dependencies
        },
        "versions": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
        "next_problem": "formulate the smallest parameter-dependent-offset CC/RCI candidate that strictly contains the corrected information pattern, then seek an independently checkable feasibility or obstruction certificate",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output must not already exist")
    result = build_report(args.root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
