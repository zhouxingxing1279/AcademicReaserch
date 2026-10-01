"""Audit terminal mRPI containment of the frozen Run-126 539-generator CZ.

The nonlinear search that found ``SEPARATOR`` is not part of the certificate.
For the fixed direction, HiGHS only proposes a CZ coefficient vector.  The
three equality variables are then recomputed with ``Fraction`` arithmetic,
so feasibility and the final comparison against a rational block-tail upper
bound on the intended mRPI are exact.

The conclusion is deliberately implementation-specific: it refutes terminal
containment for the binary64 Scott reduction produced by Run 126.  It is not
a theorem that every Scott reduction, or every 539-generator reduction, fails.
"""

from __future__ import annotations

from fractions import Fraction as Q
from functools import lru_cache
import hashlib
import itertools
import json
import os
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from verification.check_run122_run119_reproduction import HORIZON
from verification.check_run125_terminal_separation import (
    _determinant,
    _dot,
    _exact_model,
    _matrix_power,
    _mv,
    _q,
    _solve_linear,
    _transpose,
    exact_block_tail_support_upper,
)
from verification.check_run126_scott_cz_baseline import (
    HIGHS_METHOD,
    _highs_options,
    build_run123_posterior_cz,
    scott_lift_then_reduce,
)


TARGET_GENERATORS = 539
HEAD_LENGTH = 900
BLOCK_LENGTH = 139
SEPARATOR = np.array(
    [
        -0.10057934443193688,
        -0.16340010131277027,
        0.95599338253951383,
        0.22194786528659646,
    ]
)
RESULT_PATH = (
    ROOT
    / "results"
    / "controller_direction_closure_20260928"
    / "run127_terminal_cz_audit.json"
)


def _fraction_text(value) -> str:
    return f"{value.numerator}/{value.denominator}"


def _hex_fraction(value: str):
    """Decode one archived binary64 value as an exact rational."""
    return Q.from_float(float.fromhex(value))


def _exact_finite_support(
    matrix, generator, radius, direction, length: int
):
    state = generator[:]
    support = 0
    for _ in range(length):
        support += radius * abs(_dot(direction, state))
        state = _mv(matrix, state)
    return support


def exact_terminal_direction():
    """Map the separator through ``F^{-N T}`` using exact arithmetic."""
    matrix, _, _ = _exact_model()
    direction = [_q(value) for value in SEPARATOR]
    transpose_power = _transpose(_matrix_power(matrix, HORIZON))
    terminal_direction = _solve_linear(transpose_power, direction)
    residual = [
        value - target
        for value, target in zip(
            _mv(transpose_power, terminal_direction), direction
        )
    ]
    return direction, terminal_direction, residual


def _support_proposal(reduced, direction: np.ndarray):
    objective = direction @ reduced.generators
    result = linprog(
        -objective,
        A_eq=reduced.constraints,
        b_eq=reduced.rhs,
        bounds=[(-1.0, 1.0)] * reduced.generators.shape[1],
        method=HIGHS_METHOD,
        options=_highs_options(),
    )
    if not result.success:
        raise RuntimeError(f"separator support LP failed: {result.message}")
    return result


def _choose_exact_basis(constraints, proposal: np.ndarray) -> tuple[int, ...]:
    rank = len(constraints)
    free = [
        index
        for index, value in enumerate(proposal)
        if abs(value) < 1.0 - 1e-8
    ]
    for candidate in itertools.combinations(free, rank):
        square = [
            [constraints[row][column] for column in candidate]
            for row in range(rank)
        ]
        if _determinant(square) != 0:
            return candidate
    raise RuntimeError(
        "support proposal lacks a full-rank interior equality basis"
    )


def _exact_cz_witness(reduced, proposal: np.ndarray):
    constraints = [
        [_q(value) for value in row] for row in reduced.constraints
    ]
    rhs = [_q(value) for value in reduced.rhs]
    generators = [
        [_q(value) for value in row] for row in reduced.generators
    ]
    witness = [_q(value) for value in proposal]
    basis = _choose_exact_basis(constraints, proposal)
    basis_set = set(basis)
    square = [
        [constraints[row][column] for column in basis]
        for row in range(len(rhs))
    ]
    reduced_rhs = [
        rhs[row]
        - sum(
            constraints[row][column] * witness[column]
            for column in range(len(witness))
            if column not in basis_set
        )
        for row in range(len(rhs))
    ]
    exact_basis_values = _solve_linear(square, reduced_rhs)
    for column, value in zip(basis, exact_basis_values):
        witness[column] = value

    residual = [
        sum(row[column] * witness[column] for column in range(len(witness)))
        - bound
        for row, bound in zip(constraints, rhs)
    ]
    box_excess = max(abs(value) - 1 for value in witness)
    point = [
        sum(row[column] * witness[column] for column in range(len(witness)))
        for row in generators
    ]
    digest = hashlib.sha256(
        "|".join(_fraction_text(value) for value in witness).encode("ascii")
    ).hexdigest()
    return witness, basis, residual, box_excess, point, digest


def _archive_reduced_cz(reduced) -> dict[str, object]:
    """Persist the audited binary64 CZ without relying on QR replay."""
    return {
        "generators_hex": [
            [float(value).hex() for value in row]
            for row in reduced.generators
        ],
        "constraints_hex": [
            [float(value).hex() for value in row]
            for row in reduced.constraints
        ],
        "rhs_hex": [float(value).hex() for value in reduced.rhs],
    }


def _encode_exact_witness(witness, basis) -> dict[str, object]:
    basis_set = set(basis)
    signs = []
    basis_values = {}
    for index, value in enumerate(witness):
        if index in basis_set:
            signs.append("*")
            basis_values[str(index)] = _fraction_text(value)
        elif value == 1:
            signs.append("+")
        elif value == -1:
            signs.append("-")
        else:
            raise AssertionError("nonbasis support coefficient is not a box bound")
    return {
        "format": "box-sign-string-plus-exact-basis-v1",
        "box_signs": "".join(signs),
        "basis_values": basis_values,
    }


def _decode_exact_witness(encoding: dict[str, object]):
    signs = encoding["box_signs"]
    basis_values = encoding["basis_values"]
    witness = []
    for index, sign in enumerate(signs):
        if sign == "+":
            witness.append(Q(1))
        elif sign == "-":
            witness.append(Q(-1))
        elif sign == "*":
            witness.append(Q(basis_values[str(index)]))
        else:
            raise ValueError(f"unknown witness symbol {sign!r}")
    return witness


@lru_cache(maxsize=1)
def exact_separator_certificate() -> dict[str, object]:
    """Return an exact separator for the frozen binary64 reduction output."""
    _, lifted = build_run123_posterior_cz()
    reduced = scott_lift_then_reduce(
        lifted, target_generators=TARGET_GENERATORS
    )
    proposal = _support_proposal(reduced, SEPARATOR)
    witness, basis, residual, box_excess, point, digest = _exact_cz_witness(
        reduced, proposal.x
    )

    exact_direction = [_q(value) for value in SEPARATOR]
    reduced_support_lower = _dot(exact_direction, point)
    matrix, generator, radius = _exact_model()
    finite_head = _exact_finite_support(
        matrix, generator, radius, exact_direction, HEAD_LENGTH
    )
    mrpi_support_upper = exact_block_tail_support_upper(
        matrix,
        generator,
        radius,
        exact_direction,
        head_length=HEAD_LENGTH,
        block_length=BLOCK_LENGTH,
    )
    support_gap = reduced_support_lower - mrpi_support_upper
    if any(residual) or box_excess > 0 or support_gap <= 0:
        raise AssertionError("exact terminal-separation certificate failed")

    lp_equality_residual = float(
        np.max(np.abs(reduced.constraints @ proposal.x - reduced.rhs))
    )
    return {
        "target_generators": TARGET_GENERATORS,
        "separator": [float(value) for value in SEPARATOR],
        "exact_separator": [_fraction_text(value) for value in exact_direction],
        "separator_float_hex": [float(value).hex() for value in SEPARATOR],
        "free_basis_indices": list(basis),
        "witness_encoding": _encode_exact_witness(witness, basis),
        "reduced_cz_binary64": _archive_reduced_cz(reduced),
        "exact_equalities_hold": all(value == 0 for value in residual),
        "exact_box_excess": float(box_excess),
        "witness_sha256": digest,
        "lp_support": float(-proposal.fun),
        "lp_equality_residual_inf": lp_equality_residual,
        "exact_reduced_support_lower": float(reduced_support_lower),
        "exact_reduced_support_lower_fraction": _fraction_text(
            reduced_support_lower
        ),
        "finite_head_length": HEAD_LENGTH,
        "finite_head_support": float(finite_head),
        "finite_head_support_fraction": _fraction_text(finite_head),
        "block_length": BLOCK_LENGTH,
        "exact_mrpi_upper": float(mrpi_support_upper),
        "exact_mrpi_upper_fraction": _fraction_text(mrpi_support_upper),
        "exact_support_gap": float(support_gap),
        "exact_support_gap_fraction": _fraction_text(support_gap),
        "gap_is_exactly_positive": support_gap > 0,
        "exact_gap_numerator_digits": len(str(abs(support_gap.numerator))),
        "exact_gap_denominator_digits": len(str(support_gap.denominator)),
    }


def replay_artifact_certificate(report: dict[str, object]) -> dict[str, object]:
    """Replay the saved exact certificate without LP or reduction calls."""
    certificate = report["certificate"]
    archive = certificate["reduced_cz_binary64"]
    generators = [
        [_hex_fraction(value) for value in row]
        for row in archive["generators_hex"]
    ]
    constraints = [
        [_hex_fraction(value) for value in row]
        for row in archive["constraints_hex"]
    ]
    rhs = [_hex_fraction(value) for value in archive["rhs_hex"]]
    witness = _decode_exact_witness(certificate["witness_encoding"])
    direction = [Q(value) for value in certificate["exact_separator"]]
    hex_direction = [
        _hex_fraction(value) for value in certificate["separator_float_hex"]
    ]
    if direction != hex_direction:
        raise AssertionError("archived separator encodings disagree")
    if len(witness) != len(generators[0]):
        raise AssertionError("archived witness dimension mismatch")

    residual = [
        sum(row[column] * witness[column] for column in range(len(witness)))
        - bound
        for row, bound in zip(constraints, rhs)
    ]
    box_excess = max(abs(value) - 1 for value in witness)
    point = [
        sum(row[column] * witness[column] for column in range(len(witness)))
        for row in generators
    ]
    reduced_support_lower = _dot(direction, point)
    matrix, generator, radius = _exact_model()
    finite_head = _exact_finite_support(
        matrix,
        generator,
        radius,
        direction,
        int(certificate["finite_head_length"]),
    )
    mrpi_support_upper = exact_block_tail_support_upper(
        matrix,
        generator,
        radius,
        direction,
        head_length=int(certificate["finite_head_length"]),
        block_length=int(certificate["block_length"]),
    )
    support_gap = reduced_support_lower - mrpi_support_upper
    digest = hashlib.sha256(
        "|".join(_fraction_text(value) for value in witness).encode("ascii")
    ).hexdigest()
    stored_match = all(
        (
            reduced_support_lower
            == Q(certificate["exact_reduced_support_lower_fraction"]),
            finite_head == Q(certificate["finite_head_support_fraction"]),
            mrpi_support_upper
            == Q(certificate["exact_mrpi_upper_fraction"]),
            support_gap == Q(certificate["exact_support_gap_fraction"]),
            digest == certificate["witness_sha256"],
        )
    )
    if any(residual) or box_excess > 0 or support_gap <= 0 or not stored_match:
        raise AssertionError("saved exact certificate does not replay")
    return {
        "exact_equalities_hold": all(value == 0 for value in residual),
        "exact_box_excess": float(box_excess),
        "stored_exact_values_match": stored_match,
        "exact_support_gap": float(support_gap),
    }


def verify_terminal_cz_audit() -> dict[str, object]:
    certificate = exact_separator_certificate()
    matrix, _, _ = _exact_model()
    direction, terminal_direction, residual = exact_terminal_direction()
    determinant = _determinant(matrix)
    if determinant == 0 or any(residual):
        raise AssertionError("terminal direction mapping is not invertible/exact")
    return {
        "evidence_level": "implementation_counterexample",
        "scope": (
            "frozen Run-126 binary64 Scott reduction versus the intended "
            "exact-rational Run-121 mRPI"
        ),
        "terminal_containment_refuted": True,
        "claims_general_scott_failure": False,
        "claims_full_nonlinear_quadrotor_guarantee": False,
        "logical_relation": (
            "For nonsingular F, E_N(R) subset S iff R subset S; "
            "q_N=F^{-N T}r preserves the support gap."
        ),
        "exact_closed_loop_determinant": _fraction_text(determinant),
        "terminal_mapping": {
            "horizon": HORIZON,
            "source_direction": [float(value) for value in direction],
            "terminal_direction": [float(value) for value in terminal_direction],
            "exact_residual_zero": all(value == 0 for value in residual),
        },
        "certificate": certificate,
        "conclusion": (
            "The 539-generator set passes the Run-126 stage-direction budget "
            "but violates the fixed terminal mRPI by an exact positive "
            "support gap for the frozen implementation."
        ),
        "limitations": [
            "The separator is specific to the frozen four-state instance.",
            "The reduced CZ coefficients are the exact binary64 outputs of the implementation, not an abstract real-arithmetic Scott reduction.",
            "This counterexample does not establish a nonlinear six-DOF quadrotor guarantee or a general lower bound on generator count.",
        ],
    }


def main() -> None:
    report = verify_terminal_cz_audit()
    if os.environ.get("ACADEMIC_RESEARCH_NO_WRITE") != "1":
        RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
        RESULT_PATH.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
