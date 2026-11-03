#!/usr/bin/env python3
"""Exact C1 checks for the intermittent-measurement observer interface.

This script proves two complementary facts for the translational observer:
1. A single fixed positive-definite quadratic metric cannot strictly contract
   on every missed-measurement tick, because the miss map has an invariant
   position-error direction.
2. A mode/age-dependent quadratic metric can contract uniformly over the
   finite dropout automaton. The construction is exact and uses only Fraction
   arithmetic.

Usage:
    python verification/check_intermittent_metric.py --output /tmp/intermittent_metric.json
"""

from __future__ import annotations

import argparse
import json
from fractions import Fraction as F
from pathlib import Path


H = F(1, 50)
ETA0 = F(19, 20)
ETA_ROBUST = F(99, 100)
YOUNG_EPS = ETA_ROBUST / ETA0 - 1
YOUNG_NOISE_MULTIPLIER = 1 + 1 / YOUNG_EPS
L_VALUES = (5, 10, 15)

AXES = {
    "x": {"ell": F(5, 1), "p": F(120, 1)},
    "z": {"ell": F(9, 2), "p": F(60, 1)},
}


def q(x: F) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def matmul(a, b):
    return [
        [sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))]
        for i in range(len(a))
    ]


def transpose(a):
    return [list(row) for row in zip(*a)]


def matsub(a, b):
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def matscale(c, a):
    return [[c * x for x in row] for row in a]


def det2(a):
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def psd2(a):
    return a[0][0] >= 0 and a[1][1] >= 0 and det2(a) >= 0


def pd2(a):
    return a[0][0] > 0 and det2(a) > 0


def a0():
    return [[F(1), H], [F(0), F(1)]]


def a0_power(j: int):
    return [[F(1), F(j) * H], [F(0), F(1)]]


def a0_inv_power(j: int):
    return [[F(1), -F(j) * H], [F(0), F(1)]]


def a1(ell: F):
    return [[F(0), F(0)], [-ell, F(1) - ell * H]]


def p0(p: F):
    return [[p, F(0)], [F(0), F(1)]]


def p_age(p: F, j: int):
    inv = a0_inv_power(j)
    return matscale(ETA0 ** j, matmul(transpose(inv), matmul(p0(p), inv)))


def matrix_to_exact(a):
    return [[q(x) for x in row] for row in a]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    output = Path(args.output)
    if output.exists():
        raise FileExistsError(f"refusing to overwrite existing output: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)

    v = [[F(1)], [F(0)]]
    fixed_metric_obstruction = matmul(a0(), v) == v

    axes_results = {}
    all_checks = [fixed_metric_obstruction]

    for axis, cfg in AXES.items():
        ell, p = cfg["ell"], cfg["p"]
        p_mats = [p_age(p, j) for j in range(15)]
        pd_modes = all(pd2(P) for P in p_mats)

        no_success_equalities = []
        for j in range(14):
            lhs = matmul(transpose(a0()), matmul(p_mats[j + 1], a0()))
            rhs = matscale(ETA0, p_mats[j])
            no_success_equalities.append(lhs == rhs)

        success_checks = []
        for L in L_VALUES:
            j = L - 1
            lhs_edge = matmul(transpose(a1(ell)), matmul(p_mats[0], a1(ell)))
            rhs_edge = matscale(ETA0, p_mats[j])
            edge_margin = matsub(rhs_edge, lhs_edge)

            M = matmul(a1(ell), a0_power(L - 1))
            lhs_lift = matmul(transpose(M), matmul(p_mats[0], M))
            rhs_lift = matscale(ETA0 ** L, p_mats[0])
            lift_margin = matsub(rhs_lift, lhs_lift)

            aL = F(1) - ell * F(L) * H
            scalar_margin = p * (ETA0 ** L - aL * aL) - ell * ell
            success_checks.append({
                "L": L,
                "a_L": q(aL),
                "edge_margin_psd": psd2(edge_margin),
                "lift_margin_psd": psd2(lift_margin),
                "scalar_margin": q(scalar_margin),
                "scalar_margin_decimal": float(scalar_margin),
                "lift_margin_det": q(det2(lift_margin)),
                "lift_margin_det_decimal": float(det2(lift_margin)),
            })

        axis_pass = (
            pd_modes
            and all(no_success_equalities)
            and all(
                item["edge_margin_psd"]
                and item["lift_margin_psd"]
                and F(item["scalar_margin"]) > 0
                for item in success_checks
            )
        )
        all_checks.append(axis_pass)
        axes_results[axis] = {
            "ell": q(ell),
            "p0": matrix_to_exact(p_mats[0]),
            "mode_metric_formula": "P_j=eta0^j A0^{-jT} P0 A0^{-j}, j=0,...,14",
            "all_mode_metrics_pd": pd_modes,
            "all_no_success_edges_exact_eta0_equalities": all(no_success_equalities),
            "success_edges": success_checks,
            "pass": axis_pass,
        }

    young_identity = (1 + YOUNG_EPS) * ETA0 == ETA_ROBUST
    all_checks.append(young_identity)

    result = {
        "status": "pass" if all(all_checks) else "fail",
        "fixed_quadratic_metric_direct_fit": {
            "possible": False,
            "reason": "on a missed-measurement tick A0*[1,0]^T=[1,0]^T, so no fixed PD quadratic V can satisfy V(A0 e)<=eta V(e) for all e with eta<1",
            "exact_obstruction_verified": fixed_metric_obstruction,
        },
        "mode_dependent_metric": {
            "eta0": q(ETA0),
            "eta0_decimal": float(ETA0),
            "age_mapping": "j=5*m+r for mode (r,m), hence j in {0,...,14}",
            "axes": axes_results,
        },
        "robust_extension": {
            "eta_robust": q(ETA_ROBUST),
            "young_epsilon": q(YOUNG_EPS),
            "noise_multiplier": q(YOUNG_NOISE_MULTIPLIER),
            "identity_verified": young_identity,
            "bound": "V_next <= eta_robust V + (99/4)*||G_sigma d||_{P_next}^2; finite modes imply a finite uniform sigma_4 after bounding d",
        },
        "interpretation": {
            "direct_original_fixed_metric_assumption": "blocked",
            "uniform_mode_dependent_scalar_recursion": "constructively feasible for the homogeneous translational observer, with robust additive extension by Young inequality",
            "remaining_issue": "the MPC/set-membership proof must explicitly carry the mode-dependent metric (or a mode-robust envelope); full six-state and terminal/control assumptions remain separate",
        },
    }

    if result["status"] != "pass":
        raise AssertionError("C1 exact checks failed")

    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
