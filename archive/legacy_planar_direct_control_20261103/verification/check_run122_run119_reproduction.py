"""Reproduce the frozen Run-119 MPC/reduction-admission observation.

All set supports are recomputed with HiGHS.  SLSQP proposes the nominal
plan; every reported robust slack is then evaluated directly from that plan.
The result is numerical evidence, not a recursive-feasibility proof.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import numpy as np
from scipy.optimize import linprog, minimize


HORIZON = 30
H = 0.02
GRAVITY = 9.81
D0 = 3403343 / 1600000
K = np.array([-0.1075, -0.1837, 1.1637, 0.3226])
A = np.array(
    [
        [1.0, H, 0.0, 0.0],
        [0.0, 1.0, -H * GRAVITY, 0.0],
        [0.0, 0.0, 1.0, H],
        [0.0, 0.0, 0.0, 1.0],
    ]
)
B = np.array([0.0, 0.0, 0.0, 1.0])
F = A - np.outer(B, K)
G = np.array([0.0, H, 0.0, 0.0])
STATE_LIMITS = np.array([5.0, 3.0, 0.44, 2.0])
INPUT_LIMIT = 0.0672
HIGHS_METHOD = "highs-ds"
HIGHS_PRIMAL_FEASIBILITY_TOLERANCE = 1e-10
HIGHS_DUAL_FEASIBILITY_TOLERANCE = 1e-10
ADMISSION_TOLERANCE = 1e-8


class PosteriorSupport:
    """HiGHS support oracle for the correctly lifted two-packet posterior."""

    def __init__(self) -> None:
        old_generators = np.column_stack(
            [D0 * np.linalg.matrix_power(F, j) @ G for j in range(600)]
        )
        self.generators = np.column_stack([F @ old_generators, D0 * G])
        position = np.array([1.0, 0.0, 0.0, 0.0])
        self.measurement_rows = np.vstack(
            [np.r_[position @ old_generators, 0.0], position @ self.generators]
        )
        self.measurements = np.array([0.01, 0.012])
        self.radius = 0.02

    @lru_cache(maxsize=None)
    def _support_cached(self, direction: tuple[float, ...], rows: tuple[int, ...]) -> float:
        q = np.asarray(direction)
        selected = self.measurement_rows[list(rows)]
        values = self.measurements[list(rows)]
        inequalities = np.vstack([selected, -selected])
        bounds = np.r_[values + self.radius, -values + self.radius]
        result = linprog(
            -(q @ self.generators),
            A_ub=inequalities,
            b_ub=bounds,
            bounds=[(-1.0, 1.0)] * self.generators.shape[1],
            method=HIGHS_METHOD,
            options={
                "primal_feasibility_tolerance": HIGHS_PRIMAL_FEASIBILITY_TOLERANCE,
                "dual_feasibility_tolerance": HIGHS_DUAL_FEASIBILITY_TOLERANCE,
            },
        )
        if not result.success:
            raise RuntimeError(f"posterior support LP failed: {result.message}")
        return float(-result.fun)

    def support(self, direction: np.ndarray, rows: tuple[int, ...] = (0, 1)) -> float:
        return self._support_cached(tuple(float(x) for x in direction), rows)


def _powers(matrix: np.ndarray, maximum: int) -> list[np.ndarray]:
    powers = [np.eye(matrix.shape[0])]
    for _ in range(maximum):
        powers.append(powers[-1] @ matrix)
    return powers


def _tube_support(
    oracle: PosteriorSupport,
    direction: np.ndarray,
    stage: int,
    f_powers: list[np.ndarray],
    rows: tuple[int, ...] = (0, 1),
) -> float:
    value = oracle.support(f_powers[stage].T @ direction, rows)
    for power in range(stage):
        value += D0 * abs(direction @ f_powers[stage - 1 - power] @ G)
    return value


def _nominal_maps() -> tuple[np.ndarray, np.ndarray]:
    offsets = [np.array([0.001, 0.0, 0.0, 0.0])]
    maps = [np.zeros((4, HORIZON))]
    for stage in range(HORIZON):
        next_offset = A @ offsets[-1]
        next_map = A @ maps[-1]
        next_map[:, stage] += B
        offsets.append(next_offset)
        maps.append(next_map)
    return np.asarray(offsets), np.asarray(maps)


def _build_facets(
    oracle: PosteriorSupport, f_powers: list[np.ndarray]
) -> list[dict[str, object]]:
    facets: list[dict[str, object]] = []
    identity = np.eye(4)
    for stage in range(HORIZON):
        for state_index in range(4):
            for sign, prefix in ((1.0, "upper"), (-1.0, "lower")):
                direction = sign * identity[state_index]
                facets.append(
                    {
                        "stage": stage,
                        "facet": f"{prefix}_state_{state_index}",
                        "kind": "state",
                        "state_index": state_index,
                        "sign": sign,
                        "direction": direction,
                        "support": _tube_support(oracle, direction, stage, f_powers),
                    }
                )
        for sign, name, direction in (
            (1.0, "upper_input", -K),
            (-1.0, "lower_input", K),
        ):
            facets.append(
                {
                    "stage": stage,
                    "facet": name,
                    "kind": "input",
                    "sign": sign,
                    "direction": direction,
                    "support": _tube_support(oracle, direction, stage, f_powers),
                }
            )
    return facets


def _solve_baseline(facets: list[dict[str, object]]) -> tuple[np.ndarray, dict[str, object]]:
    offsets, maps = _nominal_maps()
    q_weight = np.diag([1.0, 0.2, 1.0, 0.1])
    r_weight = 0.05
    hessian = 2.0 * r_weight * np.eye(HORIZON)
    gradient = np.zeros(HORIZON)
    constant = 0.0
    for stage in range(HORIZON):
        hessian += 2.0 * maps[stage].T @ q_weight @ maps[stage]
        gradient += 2.0 * maps[stage].T @ q_weight @ offsets[stage]
        constant += float(offsets[stage] @ q_weight @ offsets[stage])

    bases: list[float] = []
    rows: list[np.ndarray] = []
    for facet in facets:
        stage = int(facet["stage"])
        support = float(facet["support"])
        sign = float(facet["sign"])
        if facet["kind"] == "state":
            state_index = int(facet["state_index"])
            bases.append(
                float(STATE_LIMITS[state_index] - support - sign * offsets[stage, state_index])
            )
            rows.append(-sign * maps[stage, state_index])
        else:
            bases.append(INPUT_LIMIT - support)
            input_row = np.zeros(HORIZON)
            input_row[stage] = -sign
            rows.append(input_row)
    bases_array = np.asarray(bases)
    rows_array = np.asarray(rows)

    def objective(inputs: np.ndarray) -> float:
        return float(0.5 * inputs @ hessian @ inputs + gradient @ inputs + constant)

    def objective_jacobian(inputs: np.ndarray) -> np.ndarray:
        return hessian @ inputs + gradient

    terminal_map = maps[HORIZON]
    terminal_offset = offsets[HORIZON]
    initial = np.linalg.lstsq(terminal_map, -terminal_offset, rcond=None)[0]
    result = minimize(
        objective,
        initial,
        jac=objective_jacobian,
        constraints=[
            {
                "type": "ineq",
                "fun": lambda inputs: bases_array + rows_array @ inputs,
                "jac": lambda _inputs: rows_array,
            },
            {
                "type": "eq",
                "fun": lambda inputs: terminal_offset + terminal_map @ inputs,
                "jac": lambda _inputs: terminal_map,
            },
        ],
        method="SLSQP",
        options={"ftol": 1e-12, "maxiter": 2000},
    )
    slacks = bases_array + rows_array @ result.x
    state_slacks = [
        float(slack) for slack, facet in zip(slacks, facets) if facet["kind"] == "state"
    ]
    baseline = {
        "solver_success": bool(result.success),
        "solver_message": result.message,
        "objective": float(result.fun),
        "terminal_inf_norm": float(np.max(np.abs(terminal_offset + terminal_map @ result.x))),
        "minimum_robust_slack": float(np.min(slacks)),
        "minimum_state_robust_slack": min(state_slacks),
        "minimum_nominal_input": float(np.min(result.x)),
        "maximum_nominal_input": float(np.max(result.x)),
        "nominal_inputs": result.x.tolist(),
        "robust_slacks": slacks.tolist(),
    }
    return result.x, baseline


def _evaluate_deletion(
    oracle: PosteriorSupport,
    facets: list[dict[str, object]],
    robust_slacks: list[float],
    f_powers: list[np.ndarray],
    kept_rows: tuple[int, ...],
) -> dict[str, object]:
    violations = []
    maximum_excess = -np.inf
    for facet, old_slack in zip(facets, robust_slacks):
        stage = int(facet["stage"])
        direction = np.asarray(facet["direction"])
        reduced_support = _tube_support(oracle, direction, stage, f_powers, kept_rows)
        support_loss = reduced_support - float(facet["support"])
        excess = support_loss - old_slack
        maximum_excess = max(maximum_excess, excess)
        if excess > ADMISSION_TOLERANCE:
            violations.append(
                {
                    "stage": stage,
                    "facet": facet["facet"],
                    "support_loss": float(support_loss),
                    "old_slack": float(old_slack),
                    "excess": float(excess),
                }
            )
    return {
        "admitted": not violations,
        "violation_tolerance": ADMISSION_TOLERANCE,
        "violation_count": len(violations),
        "maximum_excess": float(maximum_excess),
        "violations": violations,
    }


def reproduce_run119() -> dict[str, object]:
    oracle = PosteriorSupport()
    f_powers = _powers(F, HORIZON)
    directions = [
        np.array([0.0, 1.0, 0.0, 0.0]),
        np.array([0.0, 0.0, 1.0, 0.0]),
        K,
        np.array([0.0, -1.0, 0.0, 0.0]),
        np.array([0.0, 0.0, -1.0, 0.0]),
        -K,
    ]
    posterior_supports = [oracle.support(direction) for direction in directions]
    facets = _build_facets(oracle, f_powers)
    _inputs, baseline = _solve_baseline(facets)
    return {
        "evidence_level": "numerical_reproduction",
        "model": "frozen Run-93/119 four-state linear abstraction",
        "measurement_row_rank": int(np.linalg.matrix_rank(oracle.measurement_rows)),
        "posterior_supports": posterior_supports,
        "solver_settings": {
            "highs_method": HIGHS_METHOD,
            "primal_feasibility_tolerance": HIGHS_PRIMAL_FEASIBILITY_TOLERANCE,
            "dual_feasibility_tolerance": HIGHS_DUAL_FEASIBILITY_TOLERANCE,
            "slsqp_ftol": 1e-12,
            "admission_tolerance": ADMISSION_TOLERANCE,
        },
        "baseline": baseline,
        "delete_older_packet": _evaluate_deletion(
            oracle, facets, baseline["robust_slacks"], f_powers, (1,)
        ),
        "delete_newer_packet": _evaluate_deletion(
            oracle, facets, baseline["robust_slacks"], f_powers, (0,)
        ),
        "scope_warning": (
            "This reproduces one frozen numerical candidate-admission instance; it is not a "
            "proof of online recursive feasibility, stability, or nonlinear quadrotor safety."
        ),
    }


def main() -> None:
    result = reproduce_run119()
    output = Path("results/controller_direction_closure_20260928/run122_run119_reproduction.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
