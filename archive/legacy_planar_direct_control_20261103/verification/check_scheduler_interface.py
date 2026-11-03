#!/usr/bin/env python3
"""Exact checks for the finite verification-scheduling interface.

The toy problem is deliberately small enough to enumerate with Fraction
arithmetic. It verifies the structural point needed before any RL training:
under a hard two-query budget, myopic immediate tightening can be strictly
suboptimal because the scalar quadratic error certificate couples the two
signed support queries of one row.

Usage:
    python verification/check_scheduler_interface.py --output /tmp/scheduler_interface.json

The output path must not already exist.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from itertools import permutations
from pathlib import Path


TASKS = ("A+", "A-", "B+")
ROWS = {
    "A": ("A+", "A-"),
    "B": ("B+", "B-"),
}
BASELINE = {
    "A+": Fraction(2, 1),
    "A-": Fraction(2, 1),
    "B+": Fraction(3, 2),
    "B-": Fraction(1, 1),
}
CERTIFIED = {
    "A+": Fraction(1, 2),
    "A-": Fraction(1, 2),
    "B+": Fraction(1, 1),
}
TRUE_BOX = {
    "x1": (Fraction(-1, 2), Fraction(1, 2)),
    "x2": (Fraction(-1, 1), Fraction(1, 1)),
}
BUDGET = 2


def q(x: Fraction) -> str:
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def encode_fraction(x: Fraction) -> dict[str, object]:
    return {"exact": q(x), "decimal": float(x)}


def energy(bounds: dict[str, Fraction]) -> Fraction:
    """e_cert = sum_r max(b_r^+, b_r^-)^2 for P_o = I."""
    total = Fraction(0)
    for plus, minus in ROWS.values():
        beta = max(bounds[plus], bounds[minus])
        total += beta * beta
    return total


def apply_task(bounds: dict[str, Fraction], task: str) -> dict[str, Fraction]:
    out = dict(bounds)
    out[task] = min(out[task], CERTIFIED[task])
    return out


def run_sequence(seq: tuple[str, ...]) -> tuple[list[Fraction], dict[str, Fraction]]:
    bounds = dict(BASELINE)
    history = [energy(bounds)]
    for task in seq:
        bounds = apply_task(bounds, task)
        history.append(energy(bounds))
    return history, bounds


def immediate_gain(bounds: dict[str, Fraction], task: str) -> Fraction:
    return energy(bounds) - energy(apply_task(bounds, task))


def greedy_sequence() -> tuple[str, ...]:
    bounds = dict(BASELINE)
    remaining = list(TASKS)
    chosen: list[str] = []
    for _ in range(BUDGET):
        task = max(remaining, key=lambda t: (immediate_gain(bounds, t), -TASKS.index(t)))
        chosen.append(task)
        bounds = apply_task(bounds, task)
        remaining.remove(task)
    return tuple(chosen)


def task_is_sound(task: str) -> bool:
    lo1, hi1 = TRUE_BOX["x1"]
    _lo2, hi2 = TRUE_BOX["x2"]
    if task == "A+":
        return hi1 <= CERTIFIED[task]
    if task == "A-":
        return -lo1 <= CERTIFIED[task]
    if task == "B+":
        return hi2 <= CERTIFIED[task]
    raise ValueError(task)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    output = Path(args.output)
    if output.exists():
        raise FileExistsError(f"refusing to overwrite existing output: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)

    baseline_e = energy(BASELINE)

    enumerated = []
    best_e = baseline_e
    best_sequences: list[tuple[str, ...]] = []
    for length in range(BUDGET + 1):
        sequences = [()] if length == 0 else permutations(TASKS, length)
        for seq in sequences:
            seq = tuple(seq)
            history, _ = run_sequence(seq)
            final_e = history[-1]
            enumerated.append(
                {
                    "sequence": list(seq),
                    "energy_history": [encode_fraction(x) for x in history],
                    "final_energy": encode_fraction(final_e),
                    "total_gain": encode_fraction(baseline_e - final_e),
                }
            )
            if final_e < best_e:
                best_e = final_e
                best_sequences = [seq]
            elif final_e == best_e and seq:
                best_sequences.append(seq)

    greedy = greedy_sequence()
    greedy_history, _ = run_sequence(greedy)
    greedy_e = greedy_history[-1]
    optimal_gain = baseline_e - best_e
    greedy_gain = baseline_e - greedy_e
    gap = greedy_e - best_e

    checks = {
        "all_task_certificates_contain_true_box": all(task_is_sound(t) for t in TASKS),
        "all_transitions_nonincreasing_energy": all(
            all(b["decimal"] <= a["decimal"] for a, b in zip(
                item["energy_history"][:-1],
                item["energy_history"][1:],
            ))
            for item in enumerated
        ),
        "a_plus_alone_has_zero_immediate_gain": immediate_gain(BASELINE, "A+") == 0,
        "a_minus_alone_has_zero_immediate_gain": immediate_gain(BASELINE, "A-") == 0,
        "b_plus_has_positive_immediate_gain": immediate_gain(BASELINE, "B+") == Fraction(5, 4),
        "paired_a_queries_strictly_beat_greedy": best_e < greedy_e,
        "expected_optimal_energy": best_e == Fraction(5, 2),
        "expected_greedy_energy": greedy_e == Fraction(5, 1),
        "expected_gap": gap == Fraction(5, 2),
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise AssertionError(f"failed checks: {failed}")

    source_sha256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()

    result = {
        "status": "pass",
        "purpose": "exact finite-MDP witness for control-aligned set-verification scheduling",
        "metric": "e_cert=sum_r max(b_r_plus,b_r_minus)^2 with P_o=I_2",
        "true_error_set": {
            "x1": [q(TRUE_BOX["x1"][0]), q(TRUE_BOX["x1"][1])],
            "x2": [q(TRUE_BOX["x2"][0]), q(TRUE_BOX["x2"][1])],
        },
        "budget_queries": BUDGET,
        "baseline_energy": encode_fraction(baseline_e),
        "task_immediate_gains": {
            t: encode_fraction(immediate_gain(BASELINE, t)) for t in TASKS
        },
        "greedy": {
            "sequence": list(greedy),
            "energy_history": [encode_fraction(x) for x in greedy_history],
            "final_energy": encode_fraction(greedy_e),
            "total_gain": encode_fraction(greedy_gain),
        },
        "optimal": {
            "sequences": [list(seq) for seq in best_sequences if len(seq) == BUDGET],
            "final_energy": encode_fraction(best_e),
            "total_gain": encode_fraction(optimal_gain),
            "final_energy_gap_vs_greedy": encode_fraction(gap),
        },
        "checks": checks,
        "enumerated_sequences": enumerated,
        "script_sha256": source_sha256,
    }

    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "greedy": result["greedy"],
        "optimal": result["optimal"],
        "checks": result["checks"],
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
