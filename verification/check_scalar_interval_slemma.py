#!/usr/bin/env python3
"""Exact audit of a scalar interval S-lemma certificate.

For f(s)=a*s^2+b*s+c on [-1,1], the S-lemma gives the exact certificate

    f(s) = [1 s] Q [1 s]^T + lambda*(1-s^2),
    lambda >= 0, Q >= 0.

The checker does not solve the SDP.  It verifies a proposed rational
certificate using coefficient identities and exact principal minors.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
from fractions import Fraction as F
from pathlib import Path


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _text(value: F) -> str:
    return str(value)


def verify_slemma_certificate(
    a: F,
    b: F,
    c: F,
    multiplier: F,
    gram: tuple[tuple[F, F], tuple[F, F]],
) -> dict:
    """Verify one rational certificate for nonnegativity on ``[-1,1]``."""
    if len(gram) != 2 or any(len(row) != 2 for row in gram):
        raise ValueError("gram must be a 2 by 2 matrix")
    q00, q01 = gram[0]
    q10, q11 = gram[1]
    if q01 != q10:
        raise ValueError("gram must be symmetric")

    reconstructed = (q11 - multiplier, 2 * q01, q00 + multiplier)
    identity = reconstructed == (a, b, c)
    determinant = q00 * q11 - q01 * q01
    psd = q00 >= 0 and q11 >= 0 and determinant >= 0
    multiplier_nonnegative = multiplier >= 0
    return {
        "valid": identity and psd and multiplier_nonnegative,
        "coefficient_identity": identity,
        "gram_psd": psd,
        "multiplier_nonnegative": multiplier_nonnegative,
        "determinant": determinant,
        "reconstructed": reconstructed,
    }


def _json_check(check: dict) -> dict:
    return {
        key: ([_text(value) for value in item] if isinstance(item, tuple) else _text(item))
        if isinstance(item, (F, tuple))
        else item
        for key, item in check.items()
    }


def build_report(root: Path) -> dict:
    examples = {
        "one_minus_square": (
            (F(-1), F(0), F(1)),
            F(1),
            ((F(0), F(0)), (F(0), F(0))),
        ),
        "one_plus_s": (
            (F(0), F(1), F(1)),
            F(1, 2),
            ((F(1, 2), F(1, 2)), (F(1, 2), F(1, 2))),
        ),
        "run196_normalized_residual": (
            (F(1, 8), F(0), F(-1, 8)),
            F(0),
            ((F(-1, 8), F(0)), (F(0), F(1, 8))),
        ),
    }
    audited = {}
    for name, (coefficients, multiplier, gram) in examples.items():
        check = verify_slemma_certificate(*coefficients, multiplier, gram)
        audited[name] = {
            "coefficients_abc": [_text(value) for value in coefficients],
            "multiplier": _text(multiplier),
            "gram": [[_text(value) for value in row] for row in gram],
            "check": _json_check(check),
        }

    dependencies = [
        "verification/check_scalar_interval_slemma.py",
        "verification/test_scalar_interval_slemma.py",
        "docs/research/run197_literature_gate.md",
        "docs/superpowers/specs/2026-10-29-scalar-interval-exact-sdp-design.md",
    ]
    return {
        "run": 197,
        "question": "Can every scalar-thrust quadratic facet residual be represented exactly by a convex interval LMI?",
        "normalized_interval": ["-1", "1"],
        "theorem_contract": {
            "polynomial": "f(s)=a*s^2+b*s+c",
            "identity": "f(s)=[1,s]Q[1,s]^T+lambda*(1-s^2)",
            "gram": "Q=[[c-lambda,b/2],[b/2,a+lambda]]",
            "conditions": "lambda>=0 and Q positive semidefinite",
            "slater_point": "s=0 gives 1-s^2=1>0",
            "interval_condition_exact": True,
        },
        "examples": audited,
        "synthesis_contract": {
            "model_scope": "four-state reduced lateral-attitude benchmark, fixed audited active sets",
            "facets": 38,
            "vertices": 160,
            "quadratic_interval_lmis": 38 * 160,
            "affine_constraints_checked_at_endpoints": "configuration, hard state, and vertex torque bounds",
            "future_schedule": "arbitrary jump in the normalized interval",
            "successor_target": "auxiliary common-core offsets below both affine-slice endpoints",
            "common_core_is_conservative": True,
            "contains_parameter_independent_subclass": True,
            "returned_candidate_requires_run196_exact_interval_audit": True,
        },
        "evidence_level": "DERIVED",
        "full_19pair_status": "OPEN",
        "gate_A_status": "blocked",
        "proves_six_state_safety": False,
        "proves_recursive_feasibility": False,
        "dependencies_sha256": {path: _sha256(root / path) for path in dependencies},
        "runtime": {"python": platform.python_version()},
        "next_problem": "solve the fixed-cone 19-pair affine-offset SDP with all 6080 interval LMIs, then independently audit every returned quadratic over the full interval",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = build_report(args.root.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
