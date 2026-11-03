"""Structure-aware terminal-containment certificates along the Scott chain.

The fixed target is the 602-generator finite mRPI prefix ``Y[-1,1]``.
For a constrained zonotope with state-generator lineage ``G = Y C``, equality
constraints permit replacing ``C`` by ``C + Q A`` and adding offset ``-Q b``
without changing any point on ``A xi = b``.  Each target coefficient row can
therefore be certified by a small independent l1 minimization.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import json
import os
from pathlib import Path
import sys

import numpy as np
from scipy.linalg import qr
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verification.check_run126_scott_cz_baseline import (
    ConstrainedZonotope,
    build_run123_posterior_cz,
)
from verification.check_run125_terminal_separation import (
    _q,
    _solve_linear,
)


RESULT_PATH = (
    ROOT
    / "results"
    / "controller_direction_closure_20260928"
    / "run129_certificate_carrying_scott.json"
)


@dataclass(frozen=True)
class RowCertificate:
    success: bool
    multiplier: np.ndarray
    adjusted_coefficients: np.ndarray
    offset: float
    budget: float
    message: str


@dataclass(frozen=True)
class LineageCandidate:
    reduced: ConstrainedZonotope
    coefficients: np.ndarray


@dataclass(frozen=True)
class RowAudit:
    row: int
    raw_budget: float
    adjusted_budget: float
    exact_dual_margin: float
    exact_dual_margin_fraction: Fraction
    exact_dual_feasible: bool
    exact_equality_residual: Fraction
    exact_box_excess: Fraction
    repair_basis: tuple[int, ...]


@dataclass(frozen=True)
class TerminalCertificateAudit:
    target_generators: int
    certified: bool
    violating_rows: tuple[int, ...]
    minimum_exact_dual_margin: float
    lineage_residual: float
    row_audits: tuple[RowAudit, ...]


def _scott_basis_with_indices(
    generators: np.ndarray,
) -> tuple[list[int], list[int], np.ndarray, np.ndarray]:
    """Replay Run 126's deterministic maximum-volume basis selection."""
    dimension = generators.shape[0]
    if np.linalg.matrix_rank(generators) != dimension:
        raise ValueError("Scott basis selection requires full row rank")
    _, _, pivots = qr(generators, mode="economic", pivoting=True)
    basis_indices = list(pivots[:dimension])
    residual_indices = list(pivots[dimension:])
    seen_bases: set[frozenset[int]] = set()
    while True:
        basis_key = frozenset(basis_indices)
        if basis_key in seen_bases:
            raise RuntimeError("maximum-volume basis exchange cycled")
        seen_bases.add(basis_key)
        basis = generators[:, basis_indices]
        if not residual_indices:
            return basis_indices, residual_indices, basis.copy(), np.empty(
                (dimension, 0)
            )
        residual_coordinates = np.linalg.solve(
            basis, generators[:, residual_indices]
        )
        row, column = np.unravel_index(
            np.argmax(np.abs(residual_coordinates)),
            residual_coordinates.shape,
        )
        if abs(residual_coordinates[row, column]) <= 1.0 + 1e-12:
            return (
                basis_indices,
                residual_indices,
                basis.copy(),
                residual_coordinates,
            )
        basis_indices[row], residual_indices[column] = (
            residual_indices[column],
            basis_indices[row],
        )


def scott_lineage_candidate(target_generators: int) -> LineageCandidate:
    """Replay Scott reduction while carrying a state map into ``S_602``."""
    source, lifted = build_run123_posterior_cz()
    lifted_generators = np.vstack([lifted.generators, lifted.constraints])
    dimension, generator_count = lifted_generators.shape
    if not dimension <= target_generators <= generator_count:
        raise ValueError("target_generators must lie between rank and column count")

    (
        basis_indices,
        residual_indices,
        basis,
        residual_coordinates,
    ) = _scott_basis_with_indices(lifted_generators)
    initial_coefficients = np.column_stack(
        [
            np.eye(source.generators.shape[1]),
            np.zeros(
                (
                    source.generators.shape[1],
                    generator_count - source.generators.shape[1],
                )
            ),
        ]
    )
    basis_coefficients = initial_coefficients[:, basis_indices].copy()
    residual_coefficients = initial_coefficients[:, residual_indices].copy()

    while dimension + residual_coordinates.shape[1] > target_generators:
        magnitudes = np.abs(residual_coordinates)
        volume_errors = np.prod(1.0 + magnitudes, axis=0) - (
            1.0 + np.sum(magnitudes, axis=0)
        )
        selected = int(np.argmin(volume_errors))
        scales = 1.0 + magnitudes[:, selected]
        basis = basis * scales
        basis_coefficients = basis_coefficients * scales
        residual_coordinates = np.delete(
            residual_coordinates, selected, axis=1
        ) / scales[:, None]
        residual_coefficients = np.delete(
            residual_coefficients, selected, axis=1
        )

    if residual_coordinates.shape[1]:
        reduced_lift = np.column_stack(
            [basis, basis @ residual_coordinates]
        )
        coefficients = np.column_stack(
            [basis_coefficients, residual_coefficients]
        )
    else:
        reduced_lift = basis
        coefficients = basis_coefficients
    state_dimension = lifted.generators.shape[0]
    reduced = ConstrainedZonotope(
        generators=reduced_lift[:state_dimension],
        center=lifted.center.copy(),
        constraints=reduced_lift[state_dimension:],
        rhs=lifted.rhs.copy(),
    )
    return LineageCandidate(reduced=reduced, coefficients=coefficients)


def equality_adjusted_row_certificate(
    coefficients: np.ndarray,
    constraints: np.ndarray,
    rhs: np.ndarray,
) -> RowCertificate:
    """Minimize ``||c + q^T A||_1 + |q^T b|`` for one target row."""
    coefficients = np.asarray(coefficients, dtype=float)
    constraints = np.asarray(constraints, dtype=float)
    rhs = np.asarray(rhs, dtype=float)
    equality_count, generator_count = constraints.shape
    if coefficients.shape != (generator_count,):
        raise ValueError("coefficient row and constraint columns must agree")
    if rhs.shape != (equality_count,):
        raise ValueError("rhs and constraint rows must agree")

    # Variables are [q (free), t >= 0, s >= 0].
    objective = np.concatenate(
        [np.zeros(equality_count), np.ones(generator_count), np.ones(1)]
    )
    zeros = np.zeros((generator_count, 1))
    upper_matrix = np.vstack(
        [
            np.column_stack([constraints.T, -np.eye(generator_count), zeros]),
            np.column_stack([-constraints.T, -np.eye(generator_count), zeros]),
            np.concatenate([rhs, np.zeros(generator_count), [-1.0]])[None, :],
            np.concatenate([-rhs, np.zeros(generator_count), [-1.0]])[None, :],
        ]
    )
    upper_rhs = np.concatenate(
        [-coefficients, coefficients, np.zeros(2)]
    )
    bounds = (
        [(None, None)] * equality_count
        + [(0.0, None)] * generator_count
        + [(0.0, None)]
    )
    result = linprog(
        objective,
        A_ub=upper_matrix,
        b_ub=upper_rhs,
        bounds=bounds,
        method="highs",
    )
    if not result.success:
        return RowCertificate(
            success=False,
            multiplier=np.full(equality_count, np.nan),
            adjusted_coefficients=np.full(generator_count, np.nan),
            offset=float("nan"),
            budget=float("inf"),
            message=result.message,
        )
    multiplier = result.x[:equality_count]
    adjusted = coefficients + multiplier @ constraints
    offset = -float(multiplier @ rhs)
    budget = float(np.sum(np.abs(adjusted)) + abs(offset))
    return RowCertificate(
        success=True,
        multiplier=multiplier,
        adjusted_coefficients=adjusted,
        offset=offset,
        budget=budget,
        message=result.message,
    )


def strictly_over_budget_rows(budgets: np.ndarray) -> tuple[int, ...]:
    """Return every row whose represented box budget is strictly above one."""
    return tuple(int(row) for row in np.flatnonzero(np.asarray(budgets) > 1.0))


def _exact_dual_witness(
    coefficients: np.ndarray,
    constraints: np.ndarray,
    rhs: np.ndarray,
) -> tuple[Fraction, Fraction, Fraction, tuple[int, ...]]:
    """Repair a floating dual proposal and check it as exact binary64 data."""
    extended_objective = np.concatenate([coefficients, np.zeros(1)])
    equality_matrix = np.column_stack([constraints, rhs])
    result = linprog(
        -extended_objective,
        A_eq=equality_matrix,
        b_eq=np.zeros(constraints.shape[0]),
        bounds=[(-1.0, 1.0)] * extended_objective.size,
        method="highs",
    )
    if not result.success:
        raise RuntimeError(f"dual row LP failed: {result.message}")

    candidates = np.flatnonzero(
        (extended_objective == 0.0) & (np.abs(result.x) < 1.0 - 1e-7)
    )
    if candidates.size < constraints.shape[0]:
        raise RuntimeError("dual proposal lacks zero-objective repair variables")
    _, _, pivots = qr(
        equality_matrix[:, candidates], mode="economic", pivoting=True
    )
    repair_basis = tuple(
        int(candidates[index]) for index in pivots[: constraints.shape[0]]
    )
    if np.linalg.matrix_rank(equality_matrix[:, repair_basis]) < constraints.shape[0]:
        raise RuntimeError("zero-objective dual repair basis is singular")

    exact_matrix = [[_q(value) for value in row] for row in equality_matrix]
    exact_witness = [_q(value) for value in result.x]
    basis_set = set(repair_basis)
    repair_matrix = [
        [exact_matrix[row][column] for column in repair_basis]
        for row in range(constraints.shape[0])
    ]
    repair_rhs = [
        -sum(
            exact_matrix[row][column] * exact_witness[column]
            for column in range(extended_objective.size)
            if column not in basis_set
        )
        for row in range(constraints.shape[0])
    ]
    repaired_values = _solve_linear(repair_matrix, repair_rhs)
    for column, value in zip(repair_basis, repaired_values):
        exact_witness[column] = value

    residuals = [
        sum(
            exact_matrix[row][column] * exact_witness[column]
            for column in range(extended_objective.size)
        )
        for row in range(constraints.shape[0])
    ]
    equality_residual = max(abs(value) for value in residuals)
    box_excess = max(abs(value) - 1 for value in exact_witness)
    objective = sum(
        _q(value) * witness
        for value, witness in zip(extended_objective, exact_witness)
    )
    return objective, equality_residual, box_excess, repair_basis


def audit_terminal_certificate(
    target_generators: int = 604,
) -> TerminalCertificateAudit:
    """Audit the carried sufficient certificate for one Scott complexity."""
    source, _ = build_run123_posterior_cz()
    candidate = scott_lineage_candidate(target_generators)
    reconstructed = source.generators @ candidate.coefficients
    lineage_residual = float(
        np.max(np.abs(reconstructed - candidate.reduced.generators))
    )
    raw_budgets = np.sum(np.abs(candidate.coefficients), axis=1)
    violating_rows = strictly_over_budget_rows(raw_budgets)
    row_audits = []
    for row in violating_rows:
        primal = equality_adjusted_row_certificate(
            candidate.coefficients[row],
            candidate.reduced.constraints,
            candidate.reduced.rhs,
        )
        objective, residual, excess, repair_basis = _exact_dual_witness(
            candidate.coefficients[row],
            candidate.reduced.constraints,
            candidate.reduced.rhs,
        )
        row_audits.append(
            RowAudit(
                row=row,
                raw_budget=float(raw_budgets[row]),
                adjusted_budget=primal.budget,
                exact_dual_margin=float(objective - 1),
                exact_dual_margin_fraction=objective - 1,
                exact_dual_feasible=(residual == 0 and excess <= 0),
                exact_equality_residual=residual,
                exact_box_excess=excess,
                repair_basis=repair_basis,
            )
        )
    certified = all(audit.adjusted_budget <= 1.0 for audit in row_audits)
    minimum_margin = min(
        (audit.exact_dual_margin for audit in row_audits), default=0.0
    )
    return TerminalCertificateAudit(
        target_generators=target_generators,
        certified=certified,
        violating_rows=violating_rows,
        minimum_exact_dual_margin=minimum_margin,
        lineage_residual=lineage_residual,
        row_audits=tuple(row_audits),
    )


def _fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def verify_certificate_carrying_scott() -> dict[str, object]:
    """Return the reproducible first-elimination audit report."""
    audit = audit_terminal_certificate(target_generators=604)
    rows = [
        {
            "row": row.row,
            "raw_budget": row.raw_budget,
            "adjusted_primal_budget": row.adjusted_budget,
            "exact_dual_margin": row.exact_dual_margin,
            "exact_dual_margin_fraction": _fraction_text(
                row.exact_dual_margin_fraction
            ),
            "exact_equality_residual": _fraction_text(
                row.exact_equality_residual
            ),
            "exact_box_excess": _fraction_text(row.exact_box_excess),
            "exact_dual_feasible": row.exact_dual_feasible,
            "repair_basis": list(row.repair_basis),
        }
        for row in audit.row_audits
    ]
    return {
        "contract": {
            "state_dimension": 4,
            "target_generators": 602,
            "equality_constraints": 3,
            "interpretation": "frozen binary64 coefficients as exact rationals",
        },
        "first_elimination": {
            "source_generators": 605,
            "target_generators": audit.target_generators,
            "certificate_feasible": audit.certified,
            "violating_rows": list(audit.violating_rows),
            "minimum_exact_dual_margin": audit.minimum_exact_dual_margin,
            "lineage_reconstruction_residual": audit.lineage_residual,
            "all_exact_dual_witnesses_feasible": all(
                row.exact_dual_feasible for row in audit.row_audits
            ),
            "rows": rows,
        },
        "evidence_level": {
            "proved": (
                "The equality-adjusted carried row-l1 certificate is "
                "infeasible after the first frozen Scott elimination."
            ),
            "not_proved": (
                "The 604-generator constrained zonotope is outside S_602."
            ),
        },
    }


def main() -> None:
    report = verify_certificate_carrying_scott()
    if os.environ.get("ACADEMIC_RESEARCH_NO_WRITE") != "1":
        RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
        RESULT_PATH.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
