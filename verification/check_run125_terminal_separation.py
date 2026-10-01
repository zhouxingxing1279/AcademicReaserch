"""Certify a support separator for the Run-124 recentered terminal set.

The floating-point LP only proposes a posterior witness. All membership
checks and the final strict support comparison use ``Fraction`` arithmetic.
The mRPI support is bounded above by the Run-120 block-tail construction.
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
    HIGHS_DUAL_FEASIBILITY_TOLERANCE,
    HIGHS_METHOD,
    HIGHS_PRIMAL_FEASIBILITY_TOLERANCE,
)
from verification.check_run124_recenter_compression import _shifted_candidate


SEPARATOR = np.array([-0.13945649, -0.00417764, -0.39679891, -0.90724035])
HEAD_LENGTH = 600
BLOCK_LENGTH = 139


def _q(value: float) -> Q:
    numerator, denominator = float(value).as_integer_ratio()
    return Q(numerator, denominator)


def _mv(matrix: list[list[Q]], vector: list[Q]) -> list[Q]:
    return [sum(row[j] * vector[j] for j in range(len(vector))) for row in matrix]


def _mm(left: list[list[Q]], right: list[list[Q]]) -> list[list[Q]]:
    return [
        [
            sum(left[i][k] * right[k][j] for k in range(len(right)))
            for j in range(len(right[0]))
        ]
        for i in range(len(left))
    ]


def _matrix_power(matrix: list[list[Q]], exponent: int) -> list[list[Q]]:
    result = [
        [Q(int(i == j)) for j in range(len(matrix))]
        for i in range(len(matrix))
    ]
    base = matrix
    while exponent:
        if exponent & 1:
            result = _mm(result, base)
        base = _mm(base, base)
        exponent //= 2
    return result


def _dot(left: list[Q], right: list[Q]) -> Q:
    return sum(a * b for a, b in zip(left, right))


def _inf_matrix_norm(matrix: list[list[Q]]) -> Q:
    return max(sum(abs(value) for value in row) for row in matrix)


def _determinant(matrix: list[list[Q]]) -> Q:
    work = [row[:] for row in matrix]
    determinant = Q(1)
    for column in range(len(work)):
        pivot_row = next(
            (row for row in range(column, len(work)) if work[row][column]), None
        )
        if pivot_row is None:
            return Q(0)
        if pivot_row != column:
            work[column], work[pivot_row] = work[pivot_row], work[column]
            determinant = -determinant
        pivot = work[column][column]
        determinant *= pivot
        for row in range(column + 1, len(work)):
            factor = work[row][column] / pivot
            for index in range(column, len(work)):
                work[row][index] -= factor * work[column][index]
    return determinant


def _transpose(matrix: list[list[Q]]) -> list[list[Q]]:
    return [list(column) for column in zip(*matrix)]


def _solve_linear(matrix: list[list[Q]], right_hand_side: list[Q]) -> list[Q]:
    augmented = [row[:] + [value] for row, value in zip(matrix, right_hand_side)]
    for column in range(len(augmented)):
        pivot_row = next(
            (row for row in range(column, len(augmented)) if augmented[row][column]),
            None,
        )
        if pivot_row is None:
            raise ValueError("singular exact linear system")
        augmented[column], augmented[pivot_row] = (
            augmented[pivot_row],
            augmented[column],
        )
        pivot = augmented[column][column]
        augmented[column] = [value / pivot for value in augmented[column]]
        for row in range(len(augmented)):
            if row == column:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(augmented[row], augmented[column])
            ]
    return [row[-1] for row in augmented]


def exact_block_tail_support_upper(
    matrix: list[list[Q]],
    generator: list[Q],
    radius: Q,
    direction: list[Q],
    *,
    head_length: int,
    block_length: int,
) -> Q:
    """Return a rational upper bound for an infinite impulse-sum support."""
    alpha = _inf_matrix_norm(_matrix_power(matrix, block_length))
    if alpha >= 1:
        raise ValueError("block power is not contractive in infinity norm")

    state = generator[:]
    head = Q(0)
    for _ in range(head_length):
        head += abs(_dot(direction, state))
        state = _mv(matrix, state)

    block = Q(0)
    tail_state = state
    for _ in range(block_length):
        block += max(abs(value) for value in tail_state)
        tail_state = _mv(matrix, tail_state)
    tail = sum(abs(value) for value in direction) * block / (1 - alpha)
    return radius * (head + tail)


def _exact_model() -> tuple[list[list[Q]], list[Q], Q]:
    h = Q(1, 50)
    gravity = Q(981, 100)
    gain = [Q(-1075, 10000), Q(-1837, 10000), Q(11637, 10000), Q(3226, 10000)]
    matrix = [
        [Q(1), h, Q(0), Q(0)],
        [Q(0), Q(1), -h * gravity, Q(0)],
        [Q(0), Q(0), Q(1), h],
        [-gain[0], -gain[1], -gain[2], Q(1) - gain[3]],
    ]
    generator = [Q(0), h, Q(0), Q(0)]
    return matrix, generator, Q(3403343, 1600000)


def exact_terminal_direction() -> tuple[list[Q], list[Q], list[Q]]:
    """Return r, q_N=F^{-NT}r, and the exact equation residual."""
    from verification.check_run122_run119_reproduction import HORIZON

    matrix, _, _ = _exact_model()
    direction = [_q(value) for value in SEPARATOR]
    transpose_power = _transpose(_matrix_power(matrix, HORIZON))
    terminal_direction = _solve_linear(transpose_power, direction)
    residual = [
        value - target
        for value, target in zip(_mv(transpose_power, terminal_direction), direction)
    ]
    return direction, terminal_direction, residual


def _exact_contract_posterior() -> tuple[list[list[Q]], list[list[Q]], list[Q]]:
    """Return the intended rational posterior contract in Run-123 latent order."""
    matrix, generator, radius = _exact_model()
    impulses: list[list[Q]] = []
    state = generator[:]
    for _ in range(602):
        impulses.append([radius * value for value in state])
        state = _mv(matrix, state)

    # Run 123 ordering: powers 2..601, followed by powers 1 and 0.
    generators = [impulses[power] for power in range(2, 602)] + [
        impulses[1],
        impulses[0],
    ]
    # The oldest strip predates two prediction lifts; preserve its latent
    # coefficients rather than recomputing it from the current generators.
    first_row = [impulses[power][0] for power in range(600)] + [Q(0), Q(0)]
    second_row = [impulses[power][0] for power in range(1, 601)] + [
        impulses[0][0],
        Q(0),
    ]
    third_row = [column[0] for column in generators]
    measurement_rows = [first_row, second_row, third_row]
    measurements = [Q(1, 100), Q(3, 250), Q(7, 500)]
    strip_radius = Q(1, 50)
    inequalities = measurement_rows + [
        [-value for value in row] for row in measurement_rows
    ]
    bounds = [value + strip_radius for value in measurements] + [
        -value + strip_radius for value in measurements
    ]
    generator_rows = [
        [generators[column][state_index] for column in range(len(generators))]
        for state_index in range(4)
    ]
    return generator_rows, inequalities, bounds


def _scale_witness_exactly_feasible(
    witness: np.ndarray, inequalities: list[list[Q]], bounds: list[Q]
) -> tuple[list[Q], Q, Q, Q]:
    exact = [_q(value) for value in witness]
    scale = Q(1)
    for value in exact:
        if abs(value) > 1:
            scale = min(scale, 1 / abs(value))
    for row, bound in zip(inequalities, bounds):
        activity = _dot(row, exact)
        if activity > 0:
            scale = min(scale, bound / activity)
    # Zero is strictly feasible; move toward it after clipping the proposal.
    scale *= 1 - Q(1, 2**48)
    scaled = [scale * value for value in exact]
    inequality_excess = max(
        _dot(row, scaled) - bound for row, bound in zip(inequalities, bounds)
    )
    box_excess = max(abs(value) - 1 for value in scaled)
    return scaled, scale, inequality_excess, box_excess


def _posterior_witness(direction: np.ndarray) -> np.ndarray:
    posterior, *_ = _shifted_candidate()
    inequalities, bounds = posterior._inequalities()
    objective = direction @ posterior.generators
    result = linprog(
        -objective,
        A_ub=inequalities,
        b_ub=bounds,
        bounds=[(-1.0, 1.0)] * posterior.generators.shape[1],
        method=HIGHS_METHOD,
        options={
            "primal_feasibility_tolerance": HIGHS_PRIMAL_FEASIBILITY_TOLERANCE,
            "dual_feasibility_tolerance": HIGHS_DUAL_FEASIBILITY_TOLERANCE,
        },
    )
    if not result.success:
        raise RuntimeError(f"separator witness LP failed: {result.message}")
    return result.x


def verify_terminal_separation() -> dict[str, object]:
    generator_rows, inequalities, bounds = _exact_contract_posterior()
    exact_direction = [_q(value) for value in SEPARATOR]
    raw_witness = _posterior_witness(SEPARATOR)
    witness, witness_scale, inequality_excess, box_excess = (
        _scale_witness_exactly_feasible(
            raw_witness, inequalities, bounds
        )
    )
    posterior_point = [
        _dot(generator_row, witness) for generator_row in generator_rows
    ]
    posterior_support_lower = _dot(exact_direction, posterior_point)

    artifact = json.loads(
        (
            ROOT
            / "results/controller_direction_closure_20260928/run124_recenter_compression.json"
        ).read_text()
    )
    recenter = [_q(value) for value in artifact["recenter"]["initial_shift"]]
    translation = _dot(exact_direction, recenter)

    matrix, generator, radius = _exact_model()
    mrpi_support_upper = exact_block_tail_support_upper(
        matrix,
        generator,
        radius,
        exact_direction,
        head_length=HEAD_LENGTH,
        block_length=BLOCK_LENGTH,
    )
    gap = posterior_support_lower - translation - mrpi_support_upper

    # F is nonsingular (Run 124). For q_N=F^{-NT}r, support additivity gives
    # h_E_N(q_N)-h_S(q_N)=h_C(r)-r'd0-h_S(r), exactly.
    closed_loop_determinant = _determinant(matrix)
    _, terminal_direction, direction_identity_residual = exact_terminal_direction()
    posterior, *_ = _shifted_candidate()
    float_inequalities, float_bounds = posterior._inequalities()
    rational_generators = np.asarray(generator_rows, dtype=float)
    rational_inequalities = np.asarray(inequalities, dtype=float)
    rational_bounds = np.asarray(bounds, dtype=float)
    certified = bool(
        gap > 0
        and inequality_excess <= 0
        and box_excess <= 0
        and closed_loop_determinant != 0
    )
    return {
        "evidence_level": "exact_rational_support_separation",
        "scope": (
            "Run-124 recorded binary64 recenter applied to the intended exact-rational "
            "Run-123 posterior contract and frozen model"
        ),
        "implementation_alignment": {
            "maximum_generator_absolute_difference": float(
                np.max(np.abs(rational_generators - posterior.generators))
            ),
            "maximum_measurement_inequality_absolute_difference": float(
                np.max(np.abs(rational_inequalities - float_inequalities))
            ),
            "maximum_measurement_bound_absolute_difference": float(
                np.max(np.abs(rational_bounds - float_bounds))
            ),
            "role": (
                "diagnostic only; the exact certificate is evaluated on the "
                "explicit rational contract, not on an assumed bit-identical replay"
            ),
        },
        "separation_certificate": {
            "direction": SEPARATOR.tolist(),
            "witness_scale": float(witness_scale),
            "posterior_support_lower": float(posterior_support_lower),
            "translation_inner_product": float(translation),
            "mrpi_support_upper": float(mrpi_support_upper),
            "exact_gap": float(gap),
            "exact_gap_sign": 1 if gap > 0 else (-1 if gap < 0 else 0),
            "exact_gap_numerator_bits": gap.numerator.bit_length(),
            "exact_gap_denominator_bits": gap.denominator.bit_length(),
            "exact_witness_max_inequality_excess": float(inequality_excess),
            "exact_witness_max_box_excess": float(box_excess),
            "certified_noncontainment": certified,
        },
        "terminal_implication": {
            "identity": (
                "for q_N=F^{-NT}r, h_E_N(q_N)-h_S(q_N) "
                "= h_C(r)-r^T d0-h_S(r)"
            ),
            "exact_closed_loop_determinant": float(closed_loop_determinant),
            "terminal_direction": [float(value) for value in terminal_direction],
            "exact_direction_identity_residual_inf_norm": float(
                max(abs(value) for value in direction_identity_residual)
            ),
            "exact_support_gap": float(gap),
            "terminal_containment": False if certified else "unresolved",
        },
        "interpretation": (
            "The Run-124 stage-admitted nonzero recenter is strictly outside "
            "the fixed Run-121 mRPI terminal contract. This rejects that "
            "candidate; it is not a general impossibility theorem for all recentering."
        ),
        "replay_archive": {
            "raw_witness_float_hex": [float(value).hex() for value in raw_witness],
            "direction_float_hex": [float(value).hex() for value in SEPARATOR],
            "recenter_float_hex": [
                float(value).hex() for value in artifact["recenter"]["initial_shift"]
            ],
            "checker": "replay_archived_certificate",
            "requires_optimization_solver": False,
        },
    }


def _certificate_from_archived_values(
    raw_witness: np.ndarray, direction_values: np.ndarray, recenter_values: np.ndarray
) -> dict[str, object]:
    generator_rows, inequalities, bounds = _exact_contract_posterior()
    witness, _, inequality_excess, box_excess = _scale_witness_exactly_feasible(
        raw_witness, inequalities, bounds
    )
    direction = [_q(value) for value in direction_values]
    recenter = [_q(value) for value in recenter_values]
    posterior_point = [
        _dot(generator_row, witness) for generator_row in generator_rows
    ]
    posterior_support_lower = _dot(direction, posterior_point)
    matrix, generator, radius = _exact_model()
    mrpi_support_upper = exact_block_tail_support_upper(
        matrix,
        generator,
        radius,
        direction,
        head_length=HEAD_LENGTH,
        block_length=BLOCK_LENGTH,
    )
    gap = posterior_support_lower - _dot(direction, recenter) - mrpi_support_upper
    certified = bool(gap > 0 and inequality_excess <= 0 and box_excess <= 0)
    determinant = _determinant(matrix)
    _, _, terminal_identity_residual = exact_terminal_direction()
    terminal_certified = bool(
        certified
        and determinant != 0
        and all(value == 0 for value in terminal_identity_residual)
    )
    return {
        "certified_noncontainment": certified,
        "certified_terminal_noncontainment": terminal_certified,
        "exact_gap": float(gap),
        "exact_gap_sign": 1 if gap > 0 else (-1 if gap < 0 else 0),
        "exact_witness_max_inequality_excess": float(inequality_excess),
        "exact_witness_max_box_excess": float(box_excess),
    }


def replay_archived_certificate(
    path: Path | None = None,
) -> dict[str, object]:
    """Replay the persisted exact certificate without calling an optimizer."""
    if path is None:
        path = (
            ROOT
            / "results/controller_direction_closure_20260928/run125_terminal_separation.json"
        )
    archive = json.loads(path.read_text())["replay_archive"]
    raw_witness = np.asarray(
        [float.fromhex(value) for value in archive["raw_witness_float_hex"]]
    )
    direction = np.asarray(
        [float.fromhex(value) for value in archive["direction_float_hex"]]
    )
    recenter = np.asarray(
        [float.fromhex(value) for value in archive["recenter_float_hex"]]
    )
    return _certificate_from_archived_values(raw_witness, direction, recenter)


def main() -> None:
    result = verify_terminal_separation()
    output = (
        ROOT
        / "results/controller_direction_closure_20260928/run125_terminal_separation.json"
    )
    output.write_text(json.dumps(result, indent=2) + "\n")
    replay = replay_archived_certificate(output)
    if not replay["certified_terminal_noncontainment"]:
        raise RuntimeError("solver-free archive replay failed")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
