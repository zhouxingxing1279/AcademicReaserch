"""Audit nonzero recentering plus fixed-complexity support compression.

The 602-latent Run-123 posterior is outer-approximated by a 300-row
H-template containing one certified support halfspace for every state/input
direction used by the shifted candidate.  A linear program then maximizes a
nonzero nominal recenter while enforcing all 300 stage margins and the frozen
zero-terminal nominal equality.

Passing those finite margins is deliberately not reported as full admission:
the Run-121 terminal argument additionally needs the terminal error set inside
the fixed mRPI.  Exact translation covariance preserves that inclusion only
when the nominal correction follows F, which is incompatible with a nonzero
shift and the zero-terminal equality because F is nonsingular.
"""

from __future__ import annotations

import json
from fractions import Fraction as Q
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
    STATE_LIMITS,
    _build_facets,
    _nominal_maps,
    _powers,
    _solve_baseline,
    _tube_support,
)
from verification.check_run123_two_time_shift import (
    NEXT_MEASUREMENT_RESIDUAL,
    PosteriorSupport,
    _controller_directions,
    _next_posterior,
    _nominal_trajectory,
)


TOLERANCE = 1e-8


def _highs_options() -> dict[str, float]:
    return {
        "primal_feasibility_tolerance": HIGHS_PRIMAL_FEASIBILITY_TOLERANCE,
        "dual_feasibility_tolerance": HIGHS_DUAL_FEASIBILITY_TOLERANCE,
    }


def _as_fraction(value: float) -> Q:
    """Interpret a binary64 datum exactly, rather than decimal-rounding it."""
    numerator, denominator = float(value).as_integer_ratio()
    return Q(numerator, denominator)


def _outward_float(exact_value: Q) -> float:
    rounded = np.nextafter(float(exact_value), np.inf)
    while _as_fraction(rounded) < exact_value:
        rounded = np.nextafter(rounded, np.inf)
    return float(rounded)


def _certified_support_upper(posterior, direction):
    """Certify a support upper bound by exact weak-duality arithmetic.

    HiGHS proposes nonnegative inequality multipliers.  Any residual in the
    dual stationarity equation is paid for with the latent unit-box support,
    so optimality or exact dual feasibility of the proposal is unnecessary.
    """
    inequalities, bounds = posterior._inequalities()
    objective = np.asarray(direction) @ posterior.generators
    result = linprog(
        -objective,
        A_ub=inequalities,
        b_ub=bounds,
        bounds=[(-1.0, 1.0)] * posterior.generators.shape[1],
        method=HIGHS_METHOD,
        options=_highs_options(),
    )
    if not result.success:
        raise RuntimeError(f"support LP failed: {result.message}")

    multipliers = [max(Q(0), -_as_fraction(v)) for v in result.ineqlin.marginals]
    exact_bounds = [_as_fraction(v) for v in bounds]
    exact_objective = [_as_fraction(v) for v in objective]
    exact_inequalities = [
        [_as_fraction(v) for v in row] for row in inequalities
    ]
    residual = []
    for column, coefficient in enumerate(exact_objective):
        residual.append(
            coefficient
            - sum(
                multipliers[row] * exact_inequalities[row][column]
                for row in range(len(multipliers))
            )
        )
    exact_upper = sum(
        multiplier * bound
        for multiplier, bound in zip(multipliers, exact_bounds)
    ) + sum(abs(value) for value in residual)
    rounded_upper = _outward_float(exact_upper)
    return float(-result.fun), rounded_upper, exact_upper


def _minimum_inf_norm_posterior_member(posterior) -> tuple[np.ndarray, np.ndarray]:
    """Return a reproducible nonzero posterior member on the new strip centre."""
    inequalities, bounds = posterior._inequalities()
    latent_dimension = posterior.generators.shape[1]
    position_row = np.array([1.0, 0.0, 0.0, 0.0]) @ posterior.generators

    objective = np.r_[np.zeros(latent_dimension), 1.0]
    augmented = np.zeros((inequalities.shape[0] + 8, latent_dimension + 1))
    augmented[: inequalities.shape[0], :latent_dimension] = inequalities
    for state_index, generator_row in enumerate(posterior.generators):
        augmented[inequalities.shape[0] + 2 * state_index, :latent_dimension] = (
            generator_row
        )
        augmented[inequalities.shape[0] + 2 * state_index, -1] = -1.0
        augmented[
            inequalities.shape[0] + 2 * state_index + 1, :latent_dimension
        ] = -generator_row
        augmented[inequalities.shape[0] + 2 * state_index + 1, -1] = -1.0

    equality = np.c_[position_row[None, :], np.zeros((1, 1))]
    result = linprog(
        objective,
        A_ub=augmented,
        b_ub=np.r_[bounds, np.zeros(8)],
        A_eq=equality,
        b_eq=[NEXT_MEASUREMENT_RESIDUAL],
        bounds=[(-1.0, 1.0)] * latent_dimension + [(0.0, None)],
        method=HIGHS_METHOD,
        options=_highs_options(),
    )
    if not result.success:
        raise RuntimeError(f"posterior-member LP failed: {result.message}")
    latent = result.x[:latent_dimension]
    return posterior.generators @ latent, latent


def _shifted_candidate():
    old = PosteriorSupport()
    new = _next_posterior(old)
    powers = _powers(F, HORIZON + 1)
    old_inputs, _ = _solve_baseline(_build_facets(old, powers))
    offsets, maps = _nominal_maps()
    old_states = np.asarray(
        [offsets[stage] + maps[stage] @ old_inputs for stage in range(HORIZON + 1)]
    )
    shifted_inputs = np.r_[old_inputs[1:], 0.0]
    shifted_states = _nominal_trajectory(old_states[1], shifted_inputs)
    return new, powers, shifted_inputs, shifted_states


def _disturbance_support(direction, stage, powers):
    return sum(
        D0 * abs(direction @ powers[stage - 1 - power] @ G)
        for power in range(stage)
    )


def _base_margin_records(support_uppers, powers, inputs, states):
    records = []
    for stage in range(HORIZON):
        for state_index, basis in enumerate(np.eye(4)):
            for sign, direction in ((1.0, basis), (-1.0, -basis)):
                slack = (
                    STATE_LIMITS[state_index]
                    - direction @ states[stage]
                    - support_uppers[(stage, tuple(direction))]
                    - _disturbance_support(direction, stage, powers)
                )
                records.append(
                    dict(
                        stage=stage,
                        kind="state",
                        direction=direction,
                        nominal_sign=sign,
                        slack=float(slack),
                    )
                )
        records.append(
            dict(
                stage=stage,
                kind="upper_input",
                direction=-K,
                slack=float(
                    INPUT_LIMIT
                    - inputs[stage]
                    - support_uppers[(stage, tuple(-K))]
                    - _disturbance_support(-K, stage, powers)
                ),
            )
        )
        records.append(
            dict(
                stage=stage,
                kind="lower_input",
                direction=K,
                slack=float(
                    INPUT_LIMIT
                    + inputs[stage]
                    - support_uppers[(stage, tuple(K))]
                    - _disturbance_support(K, stage, powers)
                ),
            )
        )
    return records


def _maximize_recenter(direction, records, powers):
    """Maximize a posterior-member ray subject to all shifted margins."""
    correction_offset = 1
    input_offset = correction_offset + 4 * (HORIZON + 1)
    variable_count = input_offset + HORIZON

    equalities = []
    equality_bounds = []
    for index in range(4):
        row = np.zeros(variable_count)
        row[correction_offset + index] = 1.0
        row[0] = -direction[index]
        equalities.append(row)
        equality_bounds.append(0.0)
    for stage in range(HORIZON):
        for index in range(4):
            row = np.zeros(variable_count)
            row[correction_offset + 4 * (stage + 1) + index] = 1.0
            row[correction_offset + 4 * stage : correction_offset + 4 * stage + 4] -= A[index]
            row[input_offset + stage] = -B[index]
            equalities.append(row)
            equality_bounds.append(0.0)
    for index in range(4):
        row = np.zeros(variable_count)
        row[correction_offset + 4 * HORIZON + index] = 1.0
        equalities.append(row)
        equality_bounds.append(0.0)

    inequalities = []
    inequality_bounds = []
    for record in records:
        stage = record["stage"]
        propagated_shift = powers[stage] @ direction
        row = np.zeros(variable_count)
        if record["kind"] == "state":
            q = record["direction"]
            row[
                correction_offset + 4 * stage : correction_offset + 4 * stage + 4
            ] = q
            row[0] = -(q @ propagated_shift)
        elif record["kind"] == "upper_input":
            row[input_offset + stage] = 1.0
            row[0] = K @ propagated_shift
        else:
            row[input_offset + stage] = -1.0
            row[0] = -(K @ propagated_shift)
        inequalities.append(row)
        inequality_bounds.append(record["slack"])

    objective = np.r_[-1.0, np.zeros(variable_count - 1)]
    result = linprog(
        objective,
        A_ub=np.asarray(inequalities),
        b_ub=np.asarray(inequality_bounds),
        A_eq=np.asarray(equalities),
        b_eq=np.asarray(equality_bounds),
        bounds=[(0.0, 1.0)] + [(None, None)] * (variable_count - 1),
        method=HIGHS_METHOD,
        options=_highs_options(),
    )
    if not result.success:
        raise RuntimeError(f"recenter admission LP failed: {result.message}")
    corrections = result.x[
        correction_offset : correction_offset + 4 * (HORIZON + 1)
    ].reshape(HORIZON + 1, 4)
    input_corrections = result.x[input_offset:]
    maximum_excess = float(
        np.max(np.asarray(inequalities) @ result.x - np.asarray(inequality_bounds))
    )
    dynamics_residual = max(
        np.max(
            np.abs(
                corrections[stage + 1]
                - A @ corrections[stage]
                - B * input_corrections[stage]
            )
        )
        for stage in range(HORIZON)
    )
    return result.x[0], corrections, input_corrections, maximum_excess, dynamics_residual


def _certified_protected_supports(posterior, powers):
    rows = []
    raw_supports = []
    certified_uppers = []
    exact_uppers = []
    support_uppers = {}
    for stage in range(HORIZON):
        for direction in _controller_directions():
            row = powers[stage].T @ direction
            raw, upper, exact_upper = _certified_support_upper(posterior, row)
            rows.append(row)
            raw_supports.append(raw)
            certified_uppers.append(upper)
            exact_uppers.append(exact_upper)
            support_uppers[(stage, tuple(direction))] = upper
    return (
        np.asarray(rows),
        np.asarray(raw_supports),
        np.asarray(certified_uppers),
        np.asarray(exact_uppers, dtype=object),
        support_uppers,
    )


def _template_audit(rows, raw_supports, exact_uppers, shift):
    caps = []
    outward_gaps = []
    for row, exact_upper in zip(rows, exact_uppers):
        exact_shift = sum(
            _as_fraction(coefficient) * _as_fraction(value)
            for coefficient, value in zip(row, shift)
        )
        exact_cap = exact_upper - exact_shift
        cap = _outward_float(exact_cap)
        caps.append(cap)
        outward_gaps.append(_as_fraction(cap) - exact_cap)
    caps = np.asarray(caps)

    support_losses = []
    for row, cap, raw_support in zip(rows, caps, raw_supports):
        result = linprog(
            -row,
            A_ub=rows,
            b_ub=caps,
            bounds=[(None, None)] * 4,
            method=HIGHS_METHOD,
            options=_highs_options(),
        )
        if not result.success:
            raise RuntimeError(f"template support LP failed: {result.message}")
        exact_recentered_support = raw_support - row @ shift
        support_losses.append(float(-result.fun - exact_recentered_support))
    return rows, caps, support_losses, outward_gaps


def _direct_recentered_slacks(
    caps,
    powers,
    shifted_inputs,
    shifted_states,
    corrections,
    input_corrections,
):
    """Recompute all candidate slacks from the recentered template caps."""
    slacks = []
    cap_index = 0
    for stage in range(HORIZON):
        new_nominal_state = shifted_states[stage] + corrections[stage]
        for state_index, basis in enumerate(np.eye(4)):
            for direction in (basis, -basis):
                recentered_cap = caps[cap_index]
                cap_index += 1
                slacks.append(
                    STATE_LIMITS[state_index]
                    - direction @ new_nominal_state
                    - recentered_cap
                    - _disturbance_support(direction, stage, powers)
                )
        new_nominal_input = shifted_inputs[stage] + input_corrections[stage]
        for direction, sign in ((-K, -1.0), (K, 1.0)):
            recentered_cap = caps[cap_index]
            cap_index += 1
            slacks.append(
                INPUT_LIMIT
                + sign * new_nominal_input
                - recentered_cap
                - _disturbance_support(direction, stage, powers)
            )
    return slacks


def verify_recenter_compression() -> dict[str, object]:
    posterior, powers, shifted_inputs, shifted_states = _shifted_candidate()
    member_direction, member_latent = _minimum_inf_norm_posterior_member(posterior)
    rows, raw_supports, certified_uppers, exact_uppers, support_uppers = (
        _certified_protected_supports(posterior, powers)
    )
    records = _base_margin_records(
        support_uppers, powers, shifted_inputs, shifted_states
    )
    scale, corrections, input_corrections, maximum_excess, dynamics_residual = (
        _maximize_recenter(member_direction, records, powers)
    )
    initial_shift = scale * member_direction
    rows, caps, support_losses, translated_cap_gaps = _template_audit(
        rows, raw_supports, exact_uppers, initial_shift
    )

    closed_loop_determinant = float(np.linalg.det(F))
    consistent_terminal_shift = powers[HORIZON] @ initial_shift
    posterior_inequalities, posterior_bounds = posterior._inequalities()
    posterior_member_violation = float(
        max(
            np.max(posterior_inequalities @ member_latent - posterior_bounds),
            np.max(np.abs(member_latent)) - 1.0,
        )
    )
    strip_center_residual = float(
        abs(member_direction[0] - NEXT_MEASUREMENT_RESIDUAL)
    )
    certified_cap_gaps = certified_uppers - raw_supports
    direct_slacks = _direct_recentered_slacks(
        caps,
        powers,
        shifted_inputs,
        shifted_states,
        corrections,
        input_corrections,
    )

    return {
        "evidence_level": "conditional_proof_plus_numerical_stage_admission",
        "model": "frozen Run-93/119 four-state linear abstraction",
        "compression": {
            "type": "certified-control-direction H-template outer approximation",
            "source_latent_dimension": int(posterior.generators.shape[1]),
            "template_state_dimension": 4,
            "template_row_count": int(rows.shape[0]),
            "outer_inclusion_certificate": (
                "exact-rational weak-duality residual and recenter translation, "
                "rounded outward"
            ),
            "outer_inclusion_by_support_halfspaces": True,
            "maximum_template_minus_numerical_primal": float(max(support_losses)),
            "minimum_template_minus_numerical_primal": float(min(support_losses)),
            "maximum_certified_cap_minus_numerical_primal": float(
                max(certified_cap_gaps)
            ),
            "minimum_certified_cap_minus_numerical_primal": float(
                min(certified_cap_gaps)
            ),
            "minimum_translated_cap_outward_gap": float(
                min(translated_cap_gaps)
            ),
            "maximum_translated_cap_outward_gap": float(
                max(translated_cap_gaps)
            ),
            "minimum_cap": float(np.min(caps)),
            "maximum_cap": float(np.max(caps)),
        },
        "recenter": {
            "posterior_member_direction": member_direction.tolist(),
            "posterior_member_violation": posterior_member_violation,
            "strip_center_residual": strip_center_residual,
            "scale": float(scale),
            "initial_shift": initial_shift.tolist(),
            "initial_shift_inf_norm": float(np.max(np.abs(initial_shift))),
            "maximum_nominal_state_correction_inf_norm": float(
                np.max(np.abs(corrections))
            ),
            "minimum_input_correction": float(np.min(input_corrections)),
            "maximum_input_correction": float(np.max(input_corrections)),
        },
        "stage_admission": {
            "checked_margin_count": len(records),
            "maximum_constraint_excess": maximum_excess,
            "direct_maximum_constraint_excess": float(-min(direct_slacks)),
            "direct_minimum_robust_slack": float(min(direct_slacks)),
            "nominal_dynamics_residual_inf_norm": float(dynamics_residual),
            "terminal_nominal_correction_inf_norm": float(
                np.max(np.abs(corrections[-1]))
            ),
            "admitted": bool(maximum_excess <= TOLERANCE),
        },
        "terminal_gate": {
            "frozen_terminal_contract": "zero nominal terminal plus fixed Run-121 mRPI",
            "closed_loop_determinant": closed_loop_determinant,
            "consistent_translation_terminal_shift_inf_norm": float(
                np.max(np.abs(consistent_terminal_shift))
            ),
            "only_consistent_zero_terminal_scale": 0.0,
            "reason": (
                "Exact translation covariance requires d_i=F^i d_0.  Because "
                "det(F) is nonzero, d_N=0 implies d_0=0.  The stage-admitted "
                "correction instead drives d_N to zero with free nominal inputs, "
                "so the Run-123 terminal-set inclusion is no longer inherited."
            ),
        },
        "overall_admission": {
            "admitted": False,
            "blocker": "terminal_mrpi_containment_after_nonzero_recenter",
        },
        "scope_warning": (
            "The 300-row template proves outer containment and certified upper "
            "bounds only for the frozen candidate directions.  The positive recenter scale is "
            "not a recursive-feasibility certificate because terminal mRPI "
            "containment has not been established after the nonzero recenter."
        ),
    }


def main() -> None:
    result = verify_recenter_compression()
    output = Path(
        "results/controller_direction_closure_20260928/"
        "run124_recenter_compression.json"
    )
    output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
