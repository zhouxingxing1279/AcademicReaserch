#!/usr/bin/env python3
"""Generic certified support queries for rational constrained zonotopes.

A floating LP is used only to propose a dual multiplier and primal point.
All accepted certificates are reconstructed and checked with Fraction arithmetic.
"""
from __future__ import annotations

from fractions import Fraction as Q
from pathlib import Path
import argparse
import hashlib
import json
import sys

import numpy as np
import scipy
from scipy.optimize import linprog


def qrank(matrix):
    a = [[Q(v) for v in row] for row in np.asarray(matrix, dtype=object).tolist()]
    m = len(a)
    n = len(a[0]) if m else 0
    rank = 0
    for col in range(n):
        pivot = next((i for i in range(rank, m) if a[i][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        p = a[rank][col]
        a[rank] = [v / p for v in a[rank]]
        for i in range(m):
            if i != rank and a[i][col]:
                factor = a[i][col]
                a[i] = [a[i][j] - factor * a[rank][j] for j in range(n)]
        rank += 1
        if rank == m:
            break
    return rank


def solve_square(matrix, rhs):
    a = [[Q(v) for v in row] for row in np.asarray(matrix, dtype=object).tolist()]
    b = [Q(v) for v in rhs]
    n = len(a)
    augmented = [a[i] + [b[i]] for i in range(n)]
    for col in range(n):
        pivot = next((i for i in range(col, n) if augmented[i][col]), None)
        if pivot is None:
            return None
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        p = augmented[col][col]
        augmented[col] = [v / p for v in augmented[col]]
        for i in range(n):
            if i != col and augmented[i][col]:
                factor = augmented[i][col]
                augmented[i] = [
                    augmented[i][j] - factor * augmented[col][j]
                    for j in range(n + 1)
                ]
    return [augmented[i][-1] for i in range(n)]


def choose_reconstruction_basis(a, proposal):
    """Choose equality-solving coordinates with the largest box slack first."""
    a = np.asarray(a, dtype=object)
    m, n = a.shape
    order = sorted(
        range(n),
        key=lambda j: (-(1.0 - abs(float(proposal[j]))), j),
    )
    basis = []
    for j in order:
        if qrank(a[:, basis + [j]]) > len(basis):
            basis.append(j)
            if len(basis) == m:
                return basis
    return None


def reconstruct_member(a, b, proposal, max_denominator=10**7):
    """Return an exactly feasible latent point or None.

    Non-basis coordinates are rationalized from the numerical proposal. Basis
    coordinates are then solved exactly from A xi = b. The result is accepted
    only after exact equality and box checks.
    """
    a = np.asarray(a, dtype=object)
    b = np.asarray(b, dtype=object)
    m, n = a.shape
    basis = choose_reconstruction_basis(a, proposal)
    if basis is None:
        return None
    nonbasis = [j for j in range(n) if j not in basis]
    xi = [None] * n
    for j in nonbasis:
        value = float(proposal[j])
        if abs(abs(value) - 1.0) <= 1e-7:
            xi[j] = Q(1 if value >= 0 else -1)
        else:
            xi[j] = Q(value).limit_denominator(max_denominator)
    rhs = [
        b[i] - sum(a[i, j] * xi[j] for j in nonbasis)
        for i in range(m)
    ]
    solved = solve_square(a[:, basis], rhs)
    if solved is None:
        return None
    for j, value in zip(basis, solved):
        xi[j] = value
    if not all(abs(value) <= 1 for value in xi):
        return None
    if not all(
        sum(a[i, j] * xi[j] for j in range(n)) == b[i]
        for i in range(m)
    ):
        return None
    return np.asarray(xi, dtype=object)


def dual_upper(c, g, a, b, direction, multiplier):
    """Weak-duality support upper bound, valid for every multiplier."""
    c = np.asarray(c, dtype=object)
    g = np.asarray(g, dtype=object)
    a = np.asarray(a, dtype=object)
    b = np.asarray(b, dtype=object)
    p = np.asarray(direction, dtype=object)
    lam = np.asarray(multiplier, dtype=object)
    return p @ c + b @ lam + sum(abs(v) for v in p @ g - lam @ a)


def certified_query(c, g, a, b, direction):
    """Return certified lower/upper support bounds and diagnostics."""
    c = np.asarray(c, dtype=object)
    g = np.asarray(g, dtype=object)
    a = np.asarray(a, dtype=object)
    b = np.asarray(b, dtype=object)
    p = np.asarray(direction, dtype=object)
    objective = p @ g
    result = linprog(
        -np.asarray(objective, dtype=float),
        A_eq=np.asarray(a, dtype=float),
        b_eq=np.asarray(b, dtype=float),
        bounds=(-1, 1),
        method="highs",
    )
    if result.success:
        multiplier = np.asarray(
            [Q(float(-v)).limit_denominator(10**9) for v in result.eqlin.marginals],
            dtype=object,
        )
        member = reconstruct_member(a, b, result.x)
    else:
        multiplier = np.asarray([Q(0)] * len(b), dtype=object)
        member = None
    upper = dual_upper(c, g, a, b, p, multiplier)
    lower = None if member is None else p @ (c + g @ member)
    if lower is not None:
        assert lower <= upper
    return lower, upper, member, result


def random_case(rng):
    latent_dim = int(rng.integers(5, 11))
    equality_dim = int(rng.integers(1, min(5, latent_dim)))
    state_dim = int(rng.integers(2, 5))
    while True:
        raw_a = rng.integers(-4, 5, size=(equality_dim, latent_dim))
        if np.linalg.matrix_rank(raw_a.astype(float)) == equality_dim:
            break
    a = np.asarray(
        [[Q(int(v), 4) for v in row] for row in raw_a],
        dtype=object,
    )
    seed_member = np.asarray(
        [Q(int(v), 10) for v in rng.integers(-8, 9, size=latent_dim)],
        dtype=object,
    )
    b = a @ seed_member
    raw_g = rng.integers(-5, 6, size=(state_dim, latent_dim))
    g = np.asarray(
        [[Q(int(v), 20) for v in row] for row in raw_g],
        dtype=object,
    )
    c = np.asarray(
        [Q(int(v), 10) for v in rng.integers(-3, 4, size=state_dim)],
        dtype=object,
    )
    p = np.asarray(
        [Q(int(v), 10) for v in rng.integers(-10, 11, size=state_dim)],
        dtype=object,
    )
    if all(v == 0 for v in p):
        p[0] = Q(1)
    return c, g, a, b, p


def run(seed=20260923, cases=600):
    rng = np.random.default_rng(seed)
    reconstructed = 0
    brackets = 0
    exact_matches = 0
    max_gap = Q(0)
    for _ in range(cases):
        c, g, a, b, p = random_case(rng)
        lower, upper, member, numerical = certified_query(c, g, a, b, p)
        assert numerical.success
        if member is not None:
            reconstructed += 1
            assert all(abs(v) <= 1 for v in member)
            assert all(a @ member == b)
            numerical_support = float(p @ c - numerical.fun)
            assert float(lower) <= numerical_support + 1e-8
            assert numerical_support <= float(upper) + 1e-8
            brackets += 1
            if lower == upper:
                exact_matches += 1
            max_gap = max(max_gap, upper - lower)
    return {
        "scope": "generic rational CZ support-certificate reconstruction stress test",
        "seed": seed,
        "cases": cases,
        "reconstructed_members": reconstructed,
        "numerically_audited_brackets": brackets,
        "zero_width_certificates": exact_matches,
        "max_certified_gap": str(max_gap),
        "versions": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
        "limitations": [
            "random rational full-row-rank equality systems, not adversarial ill-conditioned instances",
            "success of reconstruction is validated, not guaranteed for arbitrary floating proposals",
            "numerical LP optimum is used only as an audit oracle",
        ],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=20260923)
    parser.add_argument("--cases", type=int, default=600)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output must not already exist")
    result = run(seed=args.seed, cases=args.cases)
    result["source_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
