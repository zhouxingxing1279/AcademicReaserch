#!/usr/bin/env python3
"""Exact obstruction for homothetic copies of the frozen Run193 S4 template.

Run193's HiGHS redundancy decisions select the template.  Once selected, all
witness membership, rank, dynamics, disturbance, and torque-gap calculations
in this checker use Fraction arithmetic.
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

from check_scheduling_visible_predecessor import (
    _remove_redundant,
    _row_times_matrix,
    project_scalar_input,
)


Row = tuple[tuple[F, ...], F]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rank(rows: list[tuple[F, ...]]) -> int:
    matrix = [list(row) for row in rows]
    rank = 0
    for column in range(4):
        pivot = next(
            (index for index in range(rank, len(matrix)) if matrix[index][column]),
            None,
        )
        if pivot is None:
            continue
        matrix[rank], matrix[pivot] = matrix[pivot], matrix[rank]
        scale = matrix[rank][column]
        matrix[rank] = [value / scale for value in matrix[rank]]
        for index in range(len(matrix)):
            if index == rank or not matrix[index][column]:
                continue
            factor = matrix[index][column]
            matrix[index] = [
                matrix[index][j] - factor * matrix[rank][j] for j in range(4)
            ]
        rank += 1
    return rank


def _build_s4(config: dict) -> tuple[list[Row], dict]:
    step = F(str(config["plant"]["dt_s"]))
    inertia = F(str(config["plant"]["inertia_kg_m2"]))
    state_upper = config["domain"]["state_upper"]
    state_bounds = [F(str(state_upper[index])) for index in (0, 2, 4, 5)]
    torque_bound = F(str(config["domain"]["input_upper"][1]))
    thrust_low = F(str(config["domain"]["input_lower"][0]))
    thrust_high = F(str(config["domain"]["input_upper"][0]))
    residual_constant = F(47, 25)
    residual_slope = F(9, 20) ** 3 / 6
    input_vector = (F(0), F(0), F(0), step / inertia)
    disturbance_vector = (F(0), step, F(0), F(0))

    def dynamics(thrust: F) -> list[list[F]]:
        return [
            [F(1), step, F(0), F(0)],
            [F(0), F(1), -step * thrust, F(0)],
            [F(0), F(0), F(1), step],
            [F(0), F(0), F(0), F(1)],
        ]

    hard_box: list[Row] = []
    for index, bound in enumerate(state_bounds):
        for sign in (F(1), F(-1)):
            normal = [F(0)] * 4
            normal[index] = sign
            hard_box.append((tuple(normal), bound))

    endpoints = {"low": thrust_low, "high": thrust_high}

    def endpoint_rows(target: list[Row]):
        result = {}
        for label, thrust in endpoints.items():
            rows = []
            for normal, rhs in target:
                state_row = _row_times_matrix(normal, dynamics(thrust))
                input_coefficient = sum(
                    normal[index] * input_vector[index] for index in range(4)
                )
                support = abs(
                    sum(
                        normal[index] * disturbance_vector[index]
                        for index in range(4)
                    )
                ) * (residual_constant + residual_slope * thrust)
                rows.append((state_row, input_coefficient, rhs - support))
            result[label] = rows
        return result

    current = hard_box
    layer_counts = []
    for depth in range(1, 5):
        projected = project_scalar_input(
            endpoint_rows(current), torque_bound, endpoint_conditioned=True
        )
        current = _remove_redundant(hard_box + projected)
        layer_counts.append({"depth": depth, "nonredundant_facets": len(current)})
    contract = {
        "step": step,
        "inertia": inertia,
        "torque_bound": torque_bound,
        "thrust_low": thrust_low,
        "residual_constant": residual_constant,
        "residual_slope": residual_slope,
        "input_vector": input_vector,
        "disturbance_vector": disturbance_vector,
        "dynamics": dynamics,
        "layer_counts": layer_counts,
    }
    return current, contract


def _torque_affine_bound(
    row: Row, vertex: tuple[F, ...], contract: dict
) -> tuple[str, F, F]:
    normal, rhs = row
    thrust = contract["thrust_low"]
    state_row = _row_times_matrix(normal, contract["dynamics"](thrust))
    beta = sum(normal[i] * contract["input_vector"][i] for i in range(4))
    if beta == 0:
        raise ValueError("selected witness row has no torque coefficient")
    gamma = rhs - sum(state_row[i] * vertex[i] for i in range(4))
    support = abs(
        sum(normal[i] * contract["disturbance_vector"][i] for i in range(4))
    ) * (
        contract["residual_constant"]
        + contract["residual_slope"] * thrust
    )
    relation = "upper" if beta > 0 else "lower"
    return relation, gamma / beta, -support / beta


def audit(root: Path) -> dict:
    config_path = root / "configs/planar_baseline.json"
    config = json.loads(config_path.read_text())
    s4, contract = _build_s4(config)

    vertex = (
        F(19040871601, 4000000000),
        F(4786988769, 1600000000),
        F(13488347, 39240000),
        F(4169653, 3139200),
    )
    slacks = [rhs - sum(normal[i] * vertex[i] for i in range(4)) for normal, rhs in s4]
    active_normals = [s4[index][0] for index, slack in enumerate(slacks) if slack == 0]

    lower_row: Row = (
        (F(1), F(2, 25), F(-10791, 1000000), F(-981, 10000000)),
        F(99915044647, 20000000000),
    )
    upper_row: Row = (
        (F(0), F(-1), F(981, 2500), F(981, 100000)),
        F(569575669, 200000000),
    )
    if lower_row not in s4 or upper_row not in s4:
        raise RuntimeError("frozen torque-gap witness rows are absent from reconstructed S4")
    lower_relation, lower_slope, lower_intercept = _torque_affine_bound(
        lower_row, vertex, contract
    )
    upper_relation, upper_slope, upper_intercept = _torque_affine_bound(
        upper_row, vertex, contract
    )
    if lower_relation != "lower" or upper_relation != "upper":
        raise RuntimeError("witness torque-bound directions changed")
    gap_slope = lower_slope - upper_slope
    gap_intercept = lower_intercept - upper_intercept

    dependencies = [
        "configs/planar_baseline.json",
        "verification/check_scheduling_visible_predecessor.py",
        "verification/check_homothetic_s4_rci_gate.py",
        "verification/test_homothetic_s4_rci_gate.py",
    ]
    return {
        "claim": "no positive homothetic copy of the frozen Run193 S4 admits scheduling-visible vertex torque invariance",
        "scope": "four-state reduced lateral-attitude benchmark and frozen S4 template only",
        "evidence_level": "COUNTEREXAMPLE",
        "template": {
            "source": "Run193 scheduling-visible predecessor depth 4",
            "selection_evidence": "NUMERIC_CHECK because HiGHS selects nonredundant rows",
            "layer_counts": contract["layer_counts"],
            "nonredundant_facets": len(s4),
            "homothetic_family": "alpha*S4 for 0<alpha<=1",
        },
        "witness": {
            "vertex": [str(value) for value in vertex],
            "inside_s4_exact": all(slack >= 0 for slack in slacks),
            "minimum_slack": str(min(slacks)),
            "active_facets": len(active_normals),
            "active_normal_rank": _rank(active_normals),
        },
        "torque_gap": {
            "thrust_N": str(contract["thrust_low"]),
            "lower_slope": str(lower_slope),
            "lower_intercept_Nm": str(lower_intercept),
            "upper_slope": str(upper_slope),
            "upper_intercept_Nm": str(upper_intercept),
            "slope": str(gap_slope),
            "intercept_Nm": str(gap_intercept),
            "identity": "tau_lower(alpha)-tau_upper(alpha)=slope*alpha+intercept_Nm",
            "strict_for_all_positive_alpha": gap_slope > 0 and gap_intercept > 0,
            "uses_input_limit": False,
        },
        "exists_positive_homothetic_scale": not (
            gap_slope > 0 and gap_intercept > 0
        ),
        "proves_general_rci_nonexistence": False,
        "proves_six_state_safety": False,
        "proves_recursive_feasibility": False,
        "gate_A_status": "blocked",
        "interpretation": [
            "Even with a separate torque for the measured low-thrust endpoint, this exact S4 vertex has an empty admissible torque interval for every alpha>0.",
            "The contradiction does not use the physical torque limit, so scaling this fixed shape cannot repair it.",
            "Different normals, independently varying offsets, non-homothetic sets, and richer parameter-dependent RCI synthesis remain open.",
        ],
        "dependencies_sha256": {
            relative: _sha256(root / relative) for relative in dependencies
        },
        "versions": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
        "next_problem": "run a configuration-constrained vertex-control synthesis with independently variable offsets, then independently verify the returned RCI certificate",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output must not already exist")
    result = audit(args.root)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
