#!/usr/bin/env python3
"""Exact-rational audit for Chapter 41 endpoint predecessor reduction."""
from __future__ import annotations
import argparse, json
from fractions import Fraction as F
from pathlib import Path

H = F(1, 50)
TL = F(981, 200)
TU = F(2943, 200)
D0 = F(47, 25)  # 1.880
C = F(243, 16000)  # 0.45^3/6


def pullback(r, T):
    a, b, c, d = r
    return (a, a * H + b, c - b * H * T, c * H + d)


def frac(x):
    return f"{x.numerator}/{x.denominator}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output")
    args = ap.parse_args()

    # Exact affine identity: r A((TL+TU)/2) equals midpoint of endpoint pullbacks.
    probes = [
        (F(1), F(0), F(0), F(0)),
        (F(0), F(1), F(0), F(0)),
        (F(2), F(-3), F(5), F(7)),
    ]
    tm = (TL + TU) / 2
    for r in probes:
        mid = pullback(r, tm)
        chord = tuple((a + b) / 2 for a, b in zip(pullback(r, TL), pullback(r, TU)))
        assert mid == chord

    # dbar is affine, so its midpoint is exactly the endpoint chord midpoint.
    dbar = lambda T: D0 + C * T
    assert dbar(tm) == (dbar(TL) + dbar(TU)) / 2

    rows = {
        (F(1), F(0), F(0), F(0)),
        (F(0), F(1), F(0), F(0)),
        (F(0), F(0), F(1), F(0)),
        (F(0), F(0), F(0), F(1)),
    }
    counts = []
    samples = {}
    for depth in range(1, 7):
        rows = {pullback(r, T) for r in rows for T in (TL, TU)}
        counts.append(len(rows))
        samples[str(depth)] = [[frac(v) for v in r] for r in sorted(rows)[:3]]

    assert counts == [5, 8, 14, 25, 44, 76]
    result = {
        "status": "PASS",
        "exact_parameters": {"h": frac(H), "T_L": frac(TL), "T_U": frac(TU), "d0": frac(D0), "c": frac(C)},
        "affine_pullback_midpoint_identity": True,
        "affine_disturbance_radius_midpoint_identity": True,
        "raw_positive_normal_counts_depth_1_to_6": counts,
        "sample_normals": samples,
        "scope": "Raw row pullbacks only; counts are not projected/redundancy-eliminated predecessor facet counts."
    }
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
