#!/usr/bin/env python3
"""Counterexample audit: standard generator-box zonotope order reduction is not
monotone on nested sets, even though each reduction is an outer enclosure.

A = alpha B is represented with one generator split into s identical pieces.
Splitting does not change the set, but it can change the generator selected by
Girard-style reduction.  This isolates representation dependence from set
containment.  The mixed normal [4,1] is the same attitude-terminal normal used
in this repository's certified planar baseline; coordinate normals are also
checked as a useful negative control.
"""
import argparse, json
from pathlib import Path
import numpy as np

SEED = 20260924


def support(G, p):
    return float(np.sum(np.abs(np.asarray(p) @ G)))


def reduce_generator_box(G):
    """Keep one generator with largest l1-linf score; box all discarded ones.

    This is the classical generator-box outer-reduction pattern.  The exact
    ranking convention is recorded here so the experiment is reproducible.
    """
    scores = np.sum(np.abs(G), axis=0) - np.max(np.abs(G), axis=0)
    keep = int(np.argmax(scores))
    discarded = [j for j in range(G.shape[1]) if j != keep]
    box = np.diag(np.sum(np.abs(G[:, discarded]), axis=1))
    return np.column_stack((G[:, keep], box)), keep


def split_scaled_representation(G, alpha, split):
    # Replacing g by split copies g/split preserves exactly the same segment,
    # hence the returned zonotope is exactly alpha times the original set.
    cols = [alpha * G[:, 0] / split for _ in range(split)]
    cols += [alpha * G[:, j] for j in range(1, G.shape[1])]
    return np.column_stack(cols)


def run(pairs=10000, seed=SEED):
    rng = np.random.default_rng(seed)
    normals = {
        "+e1": np.array([1.0, 0.0]), "-e1": np.array([-1.0, 0.0]),
        "+e2": np.array([0.0, 1.0]), "-e2": np.array([0.0, -1.0]),
        "+terminal_4_1": np.array([4.0, 1.0]),
        "-terminal_4_1": np.array([-4.0, -1.0]),
    }
    counts = {k: 0 for k in normals}
    max_gap = {k: 0.0 for k in normals}
    worst = None
    pair_violations = 0

    for trial in range(pairs):
        G_B = rng.normal(size=(2, 4))
        alpha = float(rng.uniform(0.65, 0.98))
        split = int(rng.integers(2, 7))
        G_A = split_scaled_representation(G_B, alpha, split)
        R_A, keep_A = reduce_generator_box(G_A)
        R_B, keep_B = reduce_generator_box(G_B)
        violated = False
        for name, p in normals.items():
            gap = support(R_A, p) - support(R_B, p)
            if gap > 1e-10:
                counts[name] += 1
                violated = True
                if gap > max_gap[name]:
                    max_gap[name] = gap
                if worst is None or gap > worst["gap"]:
                    worst = {
                        "trial": trial, "normal": name, "p": p.tolist(),
                        "gap": gap, "alpha": alpha, "split": split,
                        "h_A": support(G_A, p), "h_B": support(G_B, p),
                        "h_RA": support(R_A, p), "h_RB": support(R_B, p),
                        "keep_A": keep_A, "keep_B": keep_B,
                        "G_B": G_B.tolist(), "G_A": G_A.tolist(),
                        "R_A": R_A.tolist(), "R_B": R_B.tolist(),
                    }
        pair_violations += int(violated)

    return {
        "seed": seed, "pairs": pairs,
        "construction": "A = alpha B exactly; first generator split only in A representation",
        "reversal_pair_count": pair_violations,
        "reversal_pair_rate": pair_violations / pairs,
        "reversal_counts_by_normal": counts,
        "max_gap_by_normal": max_gap,
        "worst_counterexample": worst,
        "interpretation": (
            "Independent generator-box outer reductions need not preserve support ordering on nested sets. "
            "Coordinate supports are preserved by this boxification and act as a negative control; mixed terminal normal [4,1] can reverse."
        ),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    out = run(args.pairs, args.seed)
    text = json.dumps(out, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    print(text)

if __name__ == "__main__":
    main()
