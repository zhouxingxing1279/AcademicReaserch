"""Scott-2016 constrained-zonotope reduction baseline for Run 123.

This module first rewrites the three bounded measurement strips as equality
constraints with three auxiliary unit-box variables.  It then exposes the
zonotope generator-reduction primitive used by Scott et al.'s
lift-then-reduce construction.  The full Run-126 comparison is added only
after these two contracts are covered by tests.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import json
import os
from pathlib import Path
import sys
import time

import numpy as np
from scipy.linalg import qr
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verification.check_run122_run119_reproduction import (
    D0,
    F,
    G,
    HIGHS_DUAL_FEASIBILITY_TOLERANCE,
    HIGHS_METHOD,
    HIGHS_PRIMAL_FEASIBILITY_TOLERANCE,
    HORIZON,
    INPUT_LIMIT,
    K,
    PosteriorSupport,
    STATE_LIMITS,
    _powers,
)
from verification.check_run123_two_time_shift import (
    _controller_directions,
    _next_posterior,
)
from verification.check_run124_recenter_compression import _shifted_candidate


RESULT_PATH = (
    ROOT
    / "results"
    / "controller_direction_closure_20260928"
    / "run126_scott_cz_baseline.json"
)


def _highs_options() -> dict[str, float]:
    return {
        "primal_feasibility_tolerance": HIGHS_PRIMAL_FEASIBILITY_TOLERANCE,
        "dual_feasibility_tolerance": HIGHS_DUAL_FEASIBILITY_TOLERANCE,
    }


@dataclass(eq=False)
class ConstrainedZonotope:
    generators: np.ndarray
    center: np.ndarray
    constraints: np.ndarray
    rhs: np.ndarray

    @lru_cache(maxsize=None)
    def _support_cached(self, direction: tuple[float, ...]) -> float:
        objective = np.asarray(direction) @ self.generators
        result = linprog(
            -objective,
            A_eq=self.constraints,
            b_eq=self.rhs,
            bounds=[(-1.0, 1.0)] * self.generators.shape[1],
            method=HIGHS_METHOD,
            options=_highs_options(),
        )
        if not result.success:
            raise RuntimeError(f"CZ support LP failed: {result.message}")
        return float(np.asarray(direction) @ self.center - result.fun)

    def support(self, direction: np.ndarray) -> float:
        return self._support_cached(tuple(float(value) for value in direction))


def controller_directions() -> list[np.ndarray]:
    return _controller_directions()


def build_run123_posterior_cz():
    """Return the Run-123 posterior and its exact strip-as-CZ representation."""
    source = _next_posterior(PosteriorSupport())
    measurement_count = source.measurement_rows.shape[0]
    generators = np.column_stack(
        [source.generators, np.zeros((source.generators.shape[0], measurement_count))]
    )
    constraints = np.column_stack(
        [source.measurement_rows, -source.radius * np.eye(measurement_count)]
    )
    lifted = ConstrainedZonotope(
        generators=generators,
        center=np.zeros(source.generators.shape[0]),
        constraints=constraints,
        rhs=source.measurements.copy(),
    )
    return source, lifted


def scott_reduce_zonotope(
    generators: np.ndarray, target_generators: int
) -> np.ndarray:
    """Outer-reduce a full-row-rank zonotope using Scott Appendix A.9--A.10."""
    generators = np.asarray(generators, dtype=float)
    dimension, generator_count = generators.shape
    rank = int(np.linalg.matrix_rank(generators))
    if rank != dimension:
        raise ValueError("Scott basis reduction requires full row rank")
    if not dimension <= target_generators <= generator_count:
        raise ValueError("target_generators must lie between rank and column count")

    basis, residual_coordinates = scott_basis_coordinates(generators)

    while dimension + residual_coordinates.shape[1] > target_generators:
        magnitudes = np.abs(residual_coordinates)
        volume_errors = np.prod(1.0 + magnitudes, axis=0) - (
            1.0 + np.sum(magnitudes, axis=0)
        )
        selected = int(np.argmin(volume_errors))
        scales = 1.0 + magnitudes[:, selected]
        basis = basis * scales
        residual_coordinates = np.delete(
            residual_coordinates, selected, axis=1
        ) / scales[:, None]

    if residual_coordinates.shape[1] == 0:
        return basis
    return np.column_stack([basis, basis @ residual_coordinates])


def scott_basis_coordinates(
    generators: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Choose ``[T V]`` with Scott's required ``|T^-1 V| <= 1`` property.

    Pivoted QR supplies a stable full-rank seed.  If a residual generator has
    a coordinate larger than one, exchanging it with the corresponding basis
    column increases ``|det(T)|`` by that factor.  Since there are finitely
    many column bases, these maximum-volume exchanges terminate at a basis
    with unit-bounded residual coordinates.
    """
    generators = np.asarray(generators, dtype=float)
    dimension, generator_count = generators.shape
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
            return basis.copy(), np.empty((dimension, 0))
        residual_coordinates = np.linalg.solve(
            basis, generators[:, residual_indices]
        )
        row, column = np.unravel_index(
            np.argmax(np.abs(residual_coordinates)),
            residual_coordinates.shape,
        )
        if abs(residual_coordinates[row, column]) <= 1.0 + 1e-12:
            return basis.copy(), residual_coordinates
        basis_indices[row], residual_indices[column] = (
            residual_indices[column],
            basis_indices[row],
        )


def scott_lift_then_reduce(
    zonotope: ConstrainedZonotope, target_generators: int = 7
) -> ConstrainedZonotope:
    """Apply Scott et al. (2016), equation (30), then recover a CZ."""
    lifted_generators = np.vstack(
        [zonotope.generators, zonotope.constraints]
    )
    reduced_lift = scott_reduce_zonotope(
        lifted_generators, target_generators=target_generators
    )
    state_dimension = zonotope.generators.shape[0]
    return ConstrainedZonotope(
        generators=reduced_lift[:state_dimension],
        center=zonotope.center.copy(),
        constraints=reduced_lift[state_dimension:],
        rhs=zonotope.rhs.copy(),
    )


def _disturbance_support(direction: np.ndarray, stage: int, powers) -> float:
    return float(
        sum(
            D0 * abs(direction @ powers[stage - 1 - power] @ G)
            for power in range(stage)
        )
    )


def _query_records(source, reduced: ConstrainedZonotope, powers):
    records = []
    for stage in range(HORIZON):
        for direction in controller_directions():
            query = powers[stage].T @ direction
            exact = _scaled_source_support(source, query)
            outer = reduced.support(query)
            records.append(
                {
                    "stage": stage,
                    "direction": [float(value) for value in direction],
                    "exact": exact,
                    "outer": outer,
                    "loss": outer - exact,
                }
            )
    return records


def _constraint_slacks(source, reduced, powers, inputs, states):
    exact_slacks = []
    reduced_slacks = []
    for stage in range(HORIZON):
        for state_index, basis in enumerate(np.eye(4)):
            for direction in (basis, -basis):
                future = _disturbance_support(direction, stage, powers)
                nominal = float(direction @ states[stage])
                exact_slacks.append(
                    STATE_LIMITS[state_index]
                    - nominal
                    - _scaled_source_support(source, powers[stage].T @ direction)
                    - future
                )
                reduced_slacks.append(
                    STATE_LIMITS[state_index]
                    - nominal
                    - reduced.support(powers[stage].T @ direction)
                    - future
                )
        for direction, nominal in ((-K, inputs[stage]), (K, -inputs[stage])):
            future = _disturbance_support(direction, stage, powers)
            exact_slacks.append(
                INPUT_LIMIT
                - nominal
                - _scaled_source_support(source, powers[stage].T @ direction)
                - future
            )
            reduced_slacks.append(
                INPUT_LIMIT
                - nominal
                - reduced.support(powers[stage].T @ direction)
                - future
            )
    return np.asarray(exact_slacks), np.asarray(reduced_slacks)


def _reduced_candidate_slacks(reduced, powers, inputs, states) -> np.ndarray:
    slacks = []
    for stage in range(HORIZON):
        for state_index, basis in enumerate(np.eye(4)):
            for direction in (basis, -basis):
                slacks.append(
                    STATE_LIMITS[state_index]
                    - direction @ states[stage]
                    - reduced.support(powers[stage].T @ direction)
                    - _disturbance_support(direction, stage, powers)
                )
        for direction, nominal in ((-K, inputs[stage]), (K, -inputs[stage])):
            slacks.append(
                INPUT_LIMIT
                - nominal
                - reduced.support(powers[stage].T @ direction)
                - _disturbance_support(direction, stage, powers)
            )
    return np.asarray(slacks)


def _minimum_admissible_generator_count(
    lifted, powers, inputs, states, tolerance: float = 1e-8
):
    """Binary-search one deterministic nested Scott reduction chain."""
    lower = lifted.generators.shape[0] + lifted.constraints.shape[0]
    upper = lifted.generators.shape[1]
    evaluated = {}

    def evaluate(target):
        if target not in evaluated:
            reduced = scott_lift_then_reduce(lifted, target_generators=target)
            slacks = _reduced_candidate_slacks(reduced, powers, inputs, states)
            evaluated[target] = (reduced, slacks)
        return evaluated[target]

    _, upper_slacks = evaluate(upper)
    if np.any(upper_slacks < -tolerance):
        raise RuntimeError("unreduced CZ fails the frozen admission tolerance")
    while lower < upper:
        midpoint = (lower + upper) // 2
        _, slacks = evaluate(midpoint)
        if np.any(slacks < -tolerance):
            lower = midpoint + 1
        else:
            upper = midpoint
    admitted = lower
    admitted_set, admitted_slacks = evaluate(admitted)
    predecessor = admitted - 1 if admitted > lifted.generators.shape[0] else None
    predecessor_slacks = None
    if predecessor is not None:
        _, predecessor_slacks = evaluate(predecessor)
    return (
        admitted,
        admitted_set,
        admitted_slacks,
        predecessor,
        predecessor_slacks,
    )


def _benchmark_once(target_generators: int = 7) -> tuple[float, float, float]:
    source, lifted = build_run123_posterior_cz()
    powers = _powers(F, HORIZON + 1)
    queries = [
        powers[stage].T @ direction
        for stage in range(HORIZON)
        for direction in controller_directions()
    ]
    scaled_constraints = _scaled_source_constraints(source)

    start = time.perf_counter()
    for query in queries:
        _scaled_source_support(source, query, scaled_constraints)
    exact_seconds = time.perf_counter() - start

    start = time.perf_counter()
    reduced = scott_lift_then_reduce(
        lifted, target_generators=target_generators
    )
    construction_seconds = time.perf_counter() - start
    start = time.perf_counter()
    for query in queries:
        reduced.support(query)
    reduced_query_seconds = time.perf_counter() - start
    return exact_seconds, construction_seconds, reduced_query_seconds


def _scaled_source_constraints(source) -> tuple[np.ndarray, np.ndarray]:
    """Precompute a numerically scaled but set-equivalent strip system."""
    inequalities, bounds = source._inequalities()
    row_scales = np.max(np.abs(inequalities), axis=1)
    if np.any(row_scales == 0.0):
        raise ValueError("posterior contains an all-zero measurement row")
    return inequalities / row_scales[:, None], bounds / row_scales


def _scaled_source_support(
    source,
    direction: np.ndarray,
    scaled_constraints: tuple[np.ndarray, np.ndarray] | None = None,
) -> float:
    """Solve a support LP after row scaling the small strip coefficients.

    The unscaled Run-123 inequalities have coefficients near 1e-2.  HiGHS'
    absolute feasibility tolerance then permits about 1e-8 physical position
    excess at an active strip.  Unit-infinity row scaling represents exactly
    the same polytope while making the reported primal value meaningful at the
    1e-10 comparison tolerance.
    """
    if scaled_constraints is None:
        scaled_constraints = _scaled_source_constraints(source)
    inequalities, bounds = scaled_constraints
    objective = np.asarray(direction) @ source.generators
    result = linprog(
        -objective,
        A_ub=inequalities,
        b_ub=bounds,
        bounds=[(-1.0, 1.0)] * source.generators.shape[1],
        method=HIGHS_METHOD,
        options=_highs_options(),
    )
    if not result.success:
        raise RuntimeError(f"scaled source support LP failed: {result.message}")
    return float(-result.fun)


def verify_scott_cz_baseline(repetitions: int = 3) -> dict[str, object]:
    """Compare the exact 602-latent posterior with a seven-generator CZ."""
    if repetitions < 1:
        raise ValueError("repetitions must be positive")
    source, lifted = build_run123_posterior_cz()
    admission_tolerance = 1e-8
    reduced = scott_lift_then_reduce(lifted, target_generators=7)
    powers = _powers(F, HORIZON + 1)
    records = _query_records(source, reduced, powers)
    losses = np.asarray([record["loss"] for record in records])

    shifted_source, shifted_powers, inputs, states = _shifted_candidate()
    exact_slacks, reduced_slacks = _constraint_slacks(
        shifted_source, reduced, shifted_powers, inputs, states
    )

    (
        admitted_count,
        admitted_set,
        admitted_slacks,
        predecessor_count,
        predecessor_slacks,
    ) = _minimum_admissible_generator_count(
        lifted,
        shifted_powers,
        inputs,
        states,
        tolerance=admission_tolerance,
    )
    admitted_records = _query_records(source, admitted_set, powers)
    admitted_losses = np.asarray(
        [record["loss"] for record in admitted_records]
    )

    timings = np.asarray(
        [_benchmark_once(target_generators=7) for _ in range(repetitions)]
    )
    admitted_timings = np.asarray(
        [
            _benchmark_once(target_generators=admitted_count)
            for _ in range(repetitions)
        ]
    )
    medians = np.median(timings, axis=0)
    admitted_medians = np.median(admitted_timings, axis=0)
    return {
        "evidence_level": "numerical_strong_baseline",
        "method": "Scott-2016 lift-then-reduce, no rescaling, seven-generator CZ",
        "representation": {
            "state_dimension": int(lifted.generators.shape[0]),
            "source_latents": int(source.generators.shape[1]),
            "measurement_noise_latents": int(lifted.constraints.shape[0]),
            "lifted_generators": int(lifted.generators.shape[1]),
            "equality_constraints": int(reduced.constraints.shape[0]),
            "reduced_generators": int(reduced.generators.shape[1]),
        },
        "support_comparison": {
            "direction_count": len(records),
            "max_underestimate": float(max(0.0, np.max(-losses))),
            "minimum_loss": float(np.min(losses)),
            "median_loss": float(np.median(losses)),
            "maximum_loss": float(np.max(losses)),
            "records": records,
        },
        "shifted_candidate": {
            "exact_minimum_slack": float(np.min(exact_slacks)),
            "reduced_minimum_slack": float(np.min(reduced_slacks)),
            "exact_violation_count_at_1e-8": int(np.sum(exact_slacks < -1e-8)),
            "reduced_violation_count_at_1e-8": int(
                np.sum(reduced_slacks < -1e-8)
            ),
        },
        "admission_threshold": {
            "tolerance": admission_tolerance,
            "minimum_admissible_generators": admitted_count,
            "eliminated_generators": int(
                lifted.generators.shape[1] - admitted_count
            ),
            "admissible_minimum_slack": float(np.min(admitted_slacks)),
            "admissible_violation_count_at_1e-8": int(
                np.sum(admitted_slacks < -1e-8)
            ),
            "predecessor_generators": predecessor_count,
            "predecessor_minimum_slack": (
                None
                if predecessor_slacks is None
                else float(np.min(predecessor_slacks))
            ),
            "predecessor_cutoff_gap": (
                None
                if predecessor_slacks is None
                else float(-admission_tolerance - np.min(predecessor_slacks))
            ),
            "primal_solver_tolerance": HIGHS_PRIMAL_FEASIBILITY_TOLERANCE,
            "predecessor_within_one_solver_tolerance": (
                None
                if predecessor_slacks is None
                else bool(
                    abs(-admission_tolerance - np.min(predecessor_slacks))
                    <= HIGHS_PRIMAL_FEASIBILITY_TOLERANCE
                )
            ),
            "predecessor_violation_count_at_1e-8": (
                None
                if predecessor_slacks is None
                else int(np.sum(predecessor_slacks < -1e-8))
            ),
            "minimum_loss": float(np.min(admitted_losses)),
            "median_loss": float(np.median(admitted_losses)),
            "maximum_loss": float(np.max(admitted_losses)),
            "max_underestimate": float(
                max(0.0, np.max(-admitted_losses))
            ),
            "records": admitted_records,
        },
        "timing_seconds": {
            "repetitions": repetitions,
            "reference_constraint_precomputation_excluded": True,
            "reduced_construction_reported_separately": True,
            "exact_300_support_median": float(medians[0]),
            "scott_construction_median": float(medians[1]),
            "reduced_300_support_median": float(medians[2]),
            "scott_total_median": float(medians[1] + medians[2]),
            "raw": timings.tolist(),
            "admissible_target": admitted_count,
            "admissible_construction_median": float(admitted_medians[1]),
            "admissible_300_support_median": float(admitted_medians[2]),
            "admissible_total_median": float(
                admitted_medians[1] + admitted_medians[2]
            ),
            "admissible_raw": admitted_timings.tolist(),
        },
    }


def main() -> None:
    repetitions = int(os.environ.get("RUN126_REPETITIONS", "3"))
    report = verify_scott_cz_baseline(repetitions=repetitions)
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if os.environ.get("ACADEMIC_RESEARCH_NO_WRITE") != "1":
        RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
        RESULT_PATH.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
