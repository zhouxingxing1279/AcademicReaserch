"""Verify one causal posterior-update / MPC-candidate shift for Run 119.

The new posterior is formed by predicting the complete 601-latent posterior,
adding one fresh disturbance latent, and intersecting with a new position
measurement.  Its error coordinates are anchored at the old nominal
successor.  The old nominal plan is shifted and zero is appended.

This is a numerical baseline for one transition of the frozen four-state
model.  It is not a proof for arbitrary recentering or the nonlinear vehicle.
"""

from __future__ import annotations

import json
from functools import lru_cache
import os
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verification.check_run122_run119_reproduction import (
    A,
    B,
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
    _build_facets,
    _nominal_maps,
    _powers,
    _solve_baseline,
    _tube_support,
)


NEXT_MEASUREMENT_RESIDUAL = 0.014


class LiftedPosteriorSupport:
    """Support oracle for a generator image cut by measurement strips."""

    def __init__(
        self,
        generators: np.ndarray,
        measurement_rows: np.ndarray,
        measurements: np.ndarray,
        radius: float,
    ) -> None:
        self.generators = generators
        self.measurement_rows = measurement_rows
        self.measurements = measurements
        self.radius = radius

    def _inequalities(self) -> tuple[np.ndarray, np.ndarray]:
        return (
            np.vstack([self.measurement_rows, -self.measurement_rows]),
            np.r_[
                self.measurements + self.radius,
                -self.measurements + self.radius,
            ],
        )

    @lru_cache(maxsize=None)
    def _support_cached(self, direction: tuple[float, ...]) -> float:
        inequalities, bounds = self._inequalities()
        result = linprog(
            -(np.asarray(direction) @ self.generators),
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

    def support(self, direction: np.ndarray, _rows: tuple[int, ...] = ()) -> float:
        return self._support_cached(tuple(float(x) for x in direction))

    def is_nonempty(self) -> bool:
        inequalities, bounds = self._inequalities()
        result = linprog(
            np.zeros(self.generators.shape[1]),
            A_ub=inequalities,
            b_ub=bounds,
            bounds=[(-1.0, 1.0)] * self.generators.shape[1],
            method=HIGHS_METHOD,
            options={
                "primal_feasibility_tolerance": HIGHS_PRIMAL_FEASIBILITY_TOLERANCE,
                "dual_feasibility_tolerance": HIGHS_DUAL_FEASIBILITY_TOLERANCE,
            },
        )
        return bool(result.success)


def _next_posterior(old: PosteriorSupport) -> LiftedPosteriorSupport:
    generators = np.column_stack([F @ old.generators, D0 * G])
    inherited_rows = np.column_stack(
        [old.measurement_rows, np.zeros(old.measurement_rows.shape[0])]
    )
    position = np.array([1.0, 0.0, 0.0, 0.0])
    measurement_rows = np.vstack([inherited_rows, position @ generators])
    measurements = np.r_[old.measurements, NEXT_MEASUREMENT_RESIDUAL]
    return LiftedPosteriorSupport(
        generators, measurement_rows, measurements, old.radius
    )


def _nominal_trajectory(initial: np.ndarray, inputs: np.ndarray) -> np.ndarray:
    states = [initial]
    for nominal_input in inputs:
        states.append(A @ states[-1] + B * nominal_input)
    return np.asarray(states)


def _controller_directions() -> list[np.ndarray]:
    directions: list[np.ndarray] = []
    for basis in np.eye(4):
        directions.extend([basis, -basis])
    directions.extend([-K, K])
    return directions


def verify_two_time_shift() -> dict[str, object]:
    old = PosteriorSupport()
    new = _next_posterior(old)
    f_powers = _powers(F, HORIZON + 1)
    expected_prediction_generators = np.column_stack([F @ old.generators, D0 * G])
    expected_inherited_rows = np.column_stack(
        [old.measurement_rows, np.zeros(old.measurement_rows.shape[0])]
    )
    position = np.array([1.0, 0.0, 0.0, 0.0])
    prediction_generators_match = bool(
        np.allclose(
            new.generators, expected_prediction_generators, rtol=0.0, atol=1e-14
        )
    )
    inherited_measurement_rows_match = bool(
        np.allclose(
            new.measurement_rows[:-1], expected_inherited_rows, rtol=0.0, atol=1e-14
        )
    )
    new_measurement_row_matches_prediction = bool(
        np.allclose(
            new.measurement_rows[-1],
            position @ expected_prediction_generators,
            rtol=0.0,
            atol=1e-14,
        )
    )
    impulse_powers = _powers(F, 601)
    expected_new_generators = np.column_stack(
        [D0 * impulse_powers[power] @ G for power in range(2, 602)]
        + [D0 * impulse_powers[1] @ G, D0 * G]
    )
    is_complete_impulse_prefix = bool(
        np.allclose(new.generators, expected_new_generators, rtol=0.0, atol=1e-14)
    )

    old_facets = _build_facets(old, f_powers)
    old_inputs, old_candidate = _solve_baseline(old_facets)
    offsets, maps = _nominal_maps()
    old_states = np.asarray(
        [offsets[i] + maps[i] @ old_inputs for i in range(HORIZON + 1)]
    )
    nominal_successor_position = float(old_states[1, 0])

    shifted_inputs = np.r_[old_inputs[1:], 0.0]
    shifted_states = _nominal_trajectory(old_states[1], shifted_inputs)

    support_excesses = []
    for stage in range(HORIZON):
        for direction in _controller_directions():
            new_support = _tube_support(new, direction, stage, f_powers, ())
            old_support = _tube_support(old, direction, stage + 1, f_powers)
            support_excesses.append(new_support - old_support)

    robust_slacks = []
    for stage in range(HORIZON):
        for state_index, basis in enumerate(np.eye(4)):
            for direction in (basis, -basis):
                robust_slacks.append(
                    STATE_LIMITS[state_index]
                    - direction @ shifted_states[stage]
                    - _tube_support(new, direction, stage, f_powers, ())
                )
        robust_slacks.append(
            INPUT_LIMIT
            - shifted_inputs[stage]
            - _tube_support(new, -K, stage, f_powers, ())
        )
        robust_slacks.append(
            INPUT_LIMIT
            + shifted_inputs[stage]
            - _tube_support(new, K, stage, f_powers, ())
        )

    old_terminal_zero = np.max(np.abs(old_states[-1])) < 1e-12
    shifted_terminal_zero = np.max(np.abs(shifted_states[-1])) < 1e-12
    terminal_append_covered = bool(
        old_terminal_zero
        and shifted_terminal_zero
        and shifted_inputs[-1] == 0.0
        and is_complete_impulse_prefix
    )

    return {
        "evidence_level": "one_step_numerical_baseline",
        "model": "frozen Run-93/119 four-state linear abstraction",
        "causal_posterior": {
            "old_latent_dimension": int(old.generators.shape[1]),
            "new_latent_dimension": int(new.generators.shape[1]),
            "impulse_prefix_max_power": 601,
            "is_complete_impulse_prefix": is_complete_impulse_prefix,
            "prediction_generators_match": prediction_generators_match,
            "inherited_measurement_rows_match": inherited_measurement_rows_match,
            "new_measurement_row_matches_prediction": (
                new_measurement_row_matches_prediction
            ),
            "measurement_row_rank": int(np.linalg.matrix_rank(new.measurement_rows)),
            "position_measurement_residual": NEXT_MEASUREMENT_RESIDUAL,
            "nominal_successor_position": nominal_successor_position,
            "absolute_position_measurement": (
                nominal_successor_position + NEXT_MEASUREMENT_RESIDUAL
            ),
            "measurement_radius": float(new.radius),
            "nonempty": new.is_nonempty(),
        },
        "old_candidate": old_candidate,
        "set_transfer": {
            "alignment": "old_nominal_successor",
            "checked_direction_count": len(support_excesses),
            "maximum_support_excess": float(max(support_excesses)),
            "minimum_support_excess": float(min(support_excesses)),
        },
        "shifted_candidate": {
            "appended_nominal_input": float(shifted_inputs[-1]),
            "terminal_inf_norm": float(np.max(np.abs(shifted_states[-1]))),
            "minimum_robust_slack": float(min(robust_slacks)),
            "terminal_append_covered_by_run121_rpi": terminal_append_covered,
        },
        "scope_warning": (
            "This verifies one aligned-center numerical transition only; it is not a "
            "recursive-feasibility proof for arbitrary recentering, compression, model "
            "changes, packet loss, or the nonlinear quadrotor."
        ),
    }


def main() -> None:
    result = verify_two_time_shift()
    if os.environ.get("ACADEMIC_RESEARCH_NO_WRITE") != "1":
        output = Path(
            "results/controller_direction_closure_20260928/run123_two_time_shift.json"
        )
        output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
