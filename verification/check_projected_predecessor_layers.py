#!/usr/bin/env python3
"""Audit endpoint-exact robust predecessor after scalar torque projection.

Exact Fraction arithmetic is used to build inequalities and perform
Fourier-Motzkin elimination. SciPy/HiGHS is used only for redundancy tests.
"""
from __future__ import annotations
import argparse, json
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from scipy.optimize import linprog


def mm(r, M):
    return [sum(r[k] * M[k][j] for k in range(4)) for j in range(4)]


def canon(a, b):
    first = next((x for x in a if x), None)
    if first is None:
        return tuple(a), b
    s = abs(first)
    return tuple(x / s for x in a), b / s


def dedup(H):
    out = {}
    for a, b in H:
        aa, bb = canon(a, b)
        if aa not in out or bb < out[aa]:
            out[aa] = bb
    return [(a, b) for a, b in out.items()]


def scaled_arrays(H):
    A, b = [], []
    for a, rhs in H:
        row = np.array([float(x) for x in a])
        rr = float(rhs)
        scale = max(float(np.max(np.abs(row))), abs(rr), 1e-12)
        A.append(row / scale)
        b.append(rr / scale)
    return np.asarray(A), np.asarray(b)


def remove_redundant(H, tol=1e-8):
    H = dedup(H)
    A, b = scaled_arrays(H)
    feasibility = linprog(np.zeros(4), A_ub=A, b_ub=b,
                          bounds=[(None, None)] * 4, method="highs")
    if not feasibility.success:
        raise RuntimeError("candidate polyhedron reported infeasible")
    keep = []
    for i, item in enumerate(H):
        mask = np.arange(len(H)) != i
        result = linprog(-A[i], A_ub=A[mask], b_ub=b[mask],
                         bounds=[(None, None)] * 4, method="highs")
        if (not result.success) or (-result.fun > b[i] + tol):
            keep.append(item)
    return keep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="configs/planar_baseline.json")
    ap.add_argument("--max-depth", type=int, default=4)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()
    cfg = json.loads(Path(args.config).read_text())

    h = F(str(cfg["plant"]["dt_s"]))
    J = F(str(cfg["plant"]["inertia_kg_m2"]))
    # lateral state bounds px,vx,phi,omega
    upper = cfg["domain"]["state_upper"]
    bounds = [F(str(upper[i])) for i in (0, 2, 4, 5)]
    tau_max = F(str(cfg["domain"]["input_upper"][1]))
    TL = F(str(cfg["domain"]["input_lower"][0]))
    TU = F(str(cfg["domain"]["input_upper"][0]))
    d0, c = F("1.880"), F(9, 20) ** 3 / 6

    B = [F(0), F(0), F(0), h / J]
    E = [F(0), h, F(0), F(0)]

    def Amat(T):
        return [[1, h, 0, 0], [0, 1, -h*T, 0],
                [0, 0, 1, h], [0, 0, 0, 1]]

    X = []
    for i, width in enumerate(bounds):
        e = [F(0)] * 4; e[i] = 1; X.append((tuple(e), width))
        e = [F(0)] * 4; e[i] = -1; X.append((tuple(e), width))

    def predecessor(H):
        cs = []
        for r, q in H:
            for T in (TL, TU):
                a = tuple(mm(r, Amat(T)))
                beta = sum(r[i] * B[i] for i in range(4))
                support = abs(sum(r[i] * E[i] for i in range(4))) * (d0 + c*T)
                cs.append((a, beta, q - support))
        z = (F(0),) * 4
        cs += [(z, F(1), tau_max), (z, F(-1), tau_max)]
        zero, lower, upper_c = [], [], []
        for a, beta, rhs in cs:
            (zero if beta == 0 else upper_c if beta > 0 else lower).append((a, beta, rhs))
        out = [(a, rhs) for a, _, rhs in zero]
        for al, bl, rl in lower:
            for au, bu, ru in upper_c:
                out.append((tuple(bu*al[i] - bl*au[i] for i in range(4)),
                            bu*rl - bl*ru))
        return out

    H = X
    layers = []
    for depth in range(1, args.max_depth + 1):
        raw = X + predecessor(H)
        unique = dedup(raw)
        H = remove_redundant(raw)
        if any(rhs < 0 for _, rhs in H):
            raise AssertionError("origin no longer satisfies retained H-representation")
        layers.append({"depth": depth, "unique_candidates": len(unique),
                       "nonredundant_facets": len(H), "origin_feasible": True})

    expected = [16, 28, 52, 102]
    if args.max_depth == 4:
        got = [x["nonredundant_facets"] for x in layers]
        assert got == expected, (got, expected)

    result = {
        "status": "numerically_audited_redundancy_exact_projection",
        "thrust_endpoints": [float(TL), float(TU)],
        "tau_bound": float(tau_max),
        "layers": layers,
        "torque_bound_first_nonredundant_depth": 2,
        "analytic_torque_facet": "abs(phi + 0.04*omega) <= 0.4516",
        "notes": [
            "Fraction arithmetic builds endpoint/Fourier-Motzkin inequalities exactly.",
            "HiGHS floating LPs classify redundancy after row scaling.",
            "Counts are audited numerical facts, not an exact finite-convergence theorem."
        ]
    }
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
