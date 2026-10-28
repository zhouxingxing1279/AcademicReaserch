#!/usr/bin/env python3
"""Audit robust predecessor quantifiers when current thrust is measured.

Fraction arithmetic constructs every endpoint and Fourier--Motzkin row.
SciPy/HiGHS is used only for redundancy and mutual-containment checks, so the
finite-layer polytope comparisons are NUMERIC_CHECK evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import runpy
from fractions import Fraction as F
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import linprog


Row = tuple[tuple[F, ...], F]
InputRow = tuple[tuple[F, ...], F, F]


def _row_times_matrix(row: tuple[F, ...], matrix: list[list[F]]) -> tuple[F, ...]:
    return tuple(
        sum(row[k] * matrix[k][j] for k in range(4)) for j in range(4)
    )


def _canonical(row: tuple[F, ...], rhs: F) -> Row:
    first = next((value for value in row if value), None)
    if first is None:
        return row, rhs
    scale = abs(first)
    return tuple(value / scale for value in row), rhs / scale


def _deduplicate(rows: list[Row]) -> list[Row]:
    tightest: dict[tuple[F, ...], F] = {}
    for row, rhs in rows:
        canonical_row, canonical_rhs = _canonical(row, rhs)
        if canonical_row not in tightest or canonical_rhs < tightest[canonical_row]:
            tightest[canonical_row] = canonical_rhs
    return list(tightest.items())


def _scaled_arrays(rows: list[Row]) -> tuple[np.ndarray, np.ndarray]:
    matrix, vector = [], []
    for row, rhs in rows:
        floating_row = np.asarray([float(value) for value in row])
        floating_rhs = float(rhs)
        scale = max(float(np.max(np.abs(floating_row))), abs(floating_rhs), 1e-12)
        matrix.append(floating_row / scale)
        vector.append(floating_rhs / scale)
    return np.asarray(matrix), np.asarray(vector)


def _remove_redundant(rows: list[Row], tolerance: float = 1e-8) -> list[Row]:
    rows = _deduplicate(rows)
    matrix, vector = _scaled_arrays(rows)
    feasible = linprog(
        np.zeros(4),
        A_ub=matrix,
        b_ub=vector,
        bounds=[(None, None)] * 4,
        method="highs",
    )
    if not feasible.success:
        raise RuntimeError("candidate predecessor is infeasible")
    retained = []
    for index, item in enumerate(rows):
        mask = np.arange(len(rows)) != index
        optimum = linprog(
            -matrix[index],
            A_ub=matrix[mask],
            b_ub=vector[mask],
            bounds=[(None, None)] * 4,
            method="highs",
        )
        if (not optimum.success) or (-optimum.fun > vector[index] + tolerance):
            retained.append(item)
    return retained


def _eliminate_one_input(rows: list[InputRow], torque_bound: F) -> list[Row]:
    zero: list[InputRow] = []
    lower: list[InputRow] = []
    upper: list[InputRow] = []
    for item in rows:
        (zero if item[1] == 0 else upper if item[1] > 0 else lower).append(item)

    state_zero = (F(0),) * 4
    upper.append((state_zero, F(1), torque_bound))
    lower.append((state_zero, F(-1), torque_bound))
    projected = [(row, rhs) for row, _, rhs in zero]
    for lower_row, lower_beta, lower_rhs in lower:
        for upper_row, upper_beta, upper_rhs in upper:
            projected.append(
                (
                    tuple(
                        upper_beta * lower_row[index]
                        - lower_beta * upper_row[index]
                        for index in range(4)
                    ),
                    upper_beta * lower_rhs - lower_beta * upper_rhs,
                )
            )
    return projected


def project_scalar_input(
    rows_by_endpoint: dict[str, list[InputRow]],
    torque_bound: F,
    *,
    endpoint_conditioned: bool,
) -> list[Row]:
    """Project torque with either endpoint-local or shared quantifiers."""
    if endpoint_conditioned:
        projected: list[Row] = []
        for endpoint_rows in rows_by_endpoint.values():
            projected.extend(_eliminate_one_input(endpoint_rows, torque_bound))
        return projected
    endpoint_rows = list(rows_by_endpoint.values())
    if len({len(rows) for rows in endpoint_rows}) != 1:
        raise ValueError("shared-input projection requires aligned endpoint rows")
    # Use a deterministic target-row/endpoint ordering.  The exact projected
    # row set is order independent, while the later floating redundancy audit
    # can select different representatives from a degenerate facet family.
    shared_rows = [
        endpoint_rows[endpoint][index]
        for index in range(len(endpoint_rows[0]))
        for endpoint in range(len(endpoint_rows))
    ]
    return _eliminate_one_input(shared_rows, torque_bound)


def _maximum_violation(source: list[Row], target: list[Row]) -> float:
    source_matrix, source_vector = _scaled_arrays(source)
    target_matrix, target_vector = _scaled_arrays(target)
    maximum = -np.inf
    for row, rhs in zip(target_matrix, target_vector):
        optimum = linprog(
            -row,
            A_ub=source_matrix,
            b_ub=source_vector,
            bounds=[(None, None)] * 4,
            method="highs",
        )
        if not optimum.success:
            return float("inf")
        maximum = max(maximum, float(-optimum.fun - rhs))
    return maximum


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(root: Path, max_depth: int = 4) -> dict:
    config_path = root / "configs/planar_baseline.json"
    config = json.loads(config_path.read_text())
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
        positive = [F(0)] * 4
        positive[index] = F(1)
        hard_box.append((tuple(positive), bound))
        negative = [F(0)] * 4
        negative[index] = F(-1)
        hard_box.append((tuple(negative), bound))

    endpoints = {"low": thrust_low, "high": thrust_high}

    def endpoint_rows(target: list[Row]) -> dict[str, list[InputRow]]:
        result: dict[str, list[InputRow]] = {}
        for label, thrust in endpoints.items():
            rows = []
            for normal, rhs in target:
                state_row = _row_times_matrix(normal, dynamics(thrust))
                input_coefficient = sum(
                    normal[index] * input_vector[index] for index in range(4)
                )
                disturbance_support = abs(
                    sum(normal[index] * disturbance_vector[index] for index in range(4))
                ) * (residual_constant + residual_slope * thrust)
                rows.append((state_row, input_coefficient, rhs - disturbance_support))
            result[label] = rows
        return result

    layers = {"common": [], "visible": []}
    retained_by_depth: dict[str, list[list[Row]]] = {"common": [], "visible": []}
    # Run each recursion as an uninterrupted sequence.  Interleaving two
    # sequences changes which equivalent rows HiGHS retains in degenerate
    # redundancy LPs and breaks reproduction of the archived common-input
    # baseline, even though the exact candidate row sets are unchanged.
    for mode, endpoint_conditioned in (("common", False), ("visible", True)):
        current = hard_box
        for depth in range(1, max_depth + 1):
            projected = project_scalar_input(
                endpoint_rows(current),
                torque_bound,
                endpoint_conditioned=endpoint_conditioned,
            )
            raw = hard_box + projected
            unique = _deduplicate(raw)
            retained = _remove_redundant(raw)
            current = retained
            retained_by_depth[mode].append(retained)
            layers[mode].append(
                {
                    "depth": depth,
                    "unique_candidates": len(unique),
                    "nonredundant_facets": len(retained),
                    "origin_feasible": all(rhs >= 0 for _, rhs in retained),
                }
            )

    comparison = []
    tolerance = 1e-7
    for depth in range(max_depth):
        common = retained_by_depth["common"][depth]
        visible = retained_by_depth["visible"][depth]
        common_in_visible = _maximum_violation(common, visible)
        visible_in_common = _maximum_violation(visible, common)
        comparison.append(
            {
                "depth": depth + 1,
                "common_subset_visible_max_violation": common_in_visible,
                "visible_subset_common_max_violation": visible_in_common,
                "same_polytope_numerical": (
                    common_in_visible <= tolerance and visible_in_common <= tolerance
                ),
            }
        )

    legacy_path = root / "verification/check_projected_predecessor_layers.py"
    legacy_namespace = runpy.run_path(str(legacy_path))
    legacy_row, _ = legacy_namespace["canon"](
        (1, F(1, 50), F(0), F(0)), F(5)
    )
    legacy_result_path = root / "results/projected_predecessor_layers_20260924/checks.json"
    legacy_result = json.loads(legacy_result_path.read_text())
    archived_facet_counts = [
        layer["nonredundant_facets"] for layer in legacy_result["layers"]
    ]
    corrected_facet_counts = [
        layer["nonredundant_facets"] for layer in layers["common"]
    ]
    corrected_fraction_construction = all(
        isinstance(coefficient, F) and isinstance(rhs, F)
        for mode_layers in retained_by_depth.values()
        for layer in mode_layers
        for row, rhs in layer
        for coefficient in row
    )

    dependencies = [
        "configs/planar_baseline.json",
        "verification/check_scheduling_visible_predecessor.py",
        "verification/test_scheduling_visible_predecessor.py",
        "verification/check_projected_predecessor_layers.py",
        "results/projected_predecessor_layers_20260924/checks.json",
    ]
    return {
        "claim": "scheduling-visible and common-torque predecessor comparison over finite layers",
        "scope": "four-state reduced lateral-attitude benchmark only",
        "evidence_level": "NUMERIC_CHECK",
        "contract": {
            "current_thrust_measured_before_torque": True,
            "future_thrust": "arbitrary_jump_in_interval",
            "thrust_endpoints_N": [str(thrust_low), str(thrust_high)],
            "torque_limit_Nm": str(torque_bound),
            "state_bounds_px_vx_phi_omega": [str(value) for value in state_bounds],
            "residual_halfwidth": "47/25 + T*(9/20)^3/6",
        },
        "quantifiers": {
            "common_torque": "exists tau(x) before forall current T",
            "scheduling_visible": "forall measured current T exists tau(x,T)",
            "interior_thrust_policy": "affine interpolation of endpoint controls is admissible for the affine plant/input and affine disturbance support",
        },
        "common_torque_layers": layers["common"],
        "scheduling_visible_layers": layers["visible"],
        "layer_comparison": comparison,
        "legacy_checker_audit": {
            "fraction_leak_detected": any(isinstance(value, float) for value in legacy_row),
            "canonicalized_unit_coefficient_type": type(legacy_row[0]).__name__,
            "effect": "the legacy checker did not preserve Fraction arithmetic after canonicalizing integer hard-box normals",
            "archived_nonredundant_facet_counts": archived_facet_counts,
            "corrected_nonredundant_facet_counts": corrected_facet_counts,
            "legacy_nonredundant_facet_counts_still_match_corrected_counts": (
                archived_facet_counts == corrected_facet_counts
            ),
        },
        "corrected_fraction_construction": corrected_fraction_construction,
        "redundancy_and_containment_tolerance": tolerance,
        "is_rci_certificate": False,
        "proves_all_depths_equal": False,
        "proves_six_state_safety": False,
        "gate_A_status": "blocked",
        "interpretation": [
            "The old common-torque projection is semantically stronger than the frozen measured-current-thrust contract.",
            "For the first audited layers, endpoint-local torque projection changes candidate inequalities but not the retained polytopes within numerical LP tolerance.",
            "Finite-layer equality neither proves equality at all depths nor supplies an invariant set or controller certificate.",
        ],
        "dependencies_sha256": {
            relative: _sha256(root / relative) for relative in dependencies
        },
        "versions": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
        "next_problem": "obtain a sufficient scheduling-visible correlated controller/RCI certificate, or a controller/set-class-specific counterexample, without reverting to local configuration-cone enumeration",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--max-depth", type=int, default=4)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output must not already exist")
    result = audit(args.root, max_depth=args.max_depth)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
