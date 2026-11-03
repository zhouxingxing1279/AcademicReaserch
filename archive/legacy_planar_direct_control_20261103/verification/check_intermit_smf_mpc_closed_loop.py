#!/usr/bin/env python3
"""Exact-rational intermittent-measurement SMF + finite-grid robust MPC pilot.

This is a one-state teaching/control baseline, NOT the six-state UAV model.
The terminal set gives recursive feasibility for the frozen scalar contract.
"""
import argparse
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path

A = Q(1, 2)
W = Q(1, 20)
V = Q(1, 10)
X = Q(2)
U = Q(3, 5)
TERMINAL = Q(1, 2)
HORIZON = 3
GRID = (Q(-1, 2), Q(-1, 4), Q(0), Q(1, 4), Q(1, 2))


def predict(interval, control):
    lo, hi = interval
    if lo > hi or abs(control) > U:
        raise ValueError("invalid belief or control")
    return (A * lo + control - W, A * hi + control + W)


def update(prior, measurement):
    """A missing packet is None; otherwise intersect with [y-V,y+V]."""
    if measurement is None:
        return prior
    lo = max(prior[0], measurement - V)
    hi = min(prior[1], measurement + V)
    if lo > hi:
        raise ValueError("inconsistent measurement")
    return (lo, hi)


def contains(interval, x):
    return interval[0] <= x <= interval[1]


def feasible(interval, plan):
    if len(plan) != HORIZON or interval[0] < -X or interval[1] > X:
        return False
    reach = interval
    for u in plan:
        if abs(u) > U:
            return False
        reach = predict(reach, u)
        if reach[0] < -X or reach[1] > X:
            return False
    return reach[0] >= -TERMINAL and reach[1] <= TERMINAL


def cost(interval, plan):
    """Nominal midpoint quadratic objective; feasibility uses full intervals."""
    mid = (interval[0] + interval[1]) / 2
    total = Q(0)
    for u in plan:
        mid = A * mid + u
        total += mid * mid + u * u / 10
    return total


def optimize(interval, fallback):
    if not feasible(interval, fallback):
        raise ValueError("certified shifted fallback not feasible")
    best = tuple(fallback)
    best_key = (cost(interval, best), best)
    feasible_count = 0
    for plan in itertools.product(GRID, repeat=HORIZON):
        if feasible(interval, plan):
            feasible_count += 1
            key = (cost(interval, plan), plan)
            if key < best_key:
                best, best_key = plan, key
    assert feasible_count >= 1
    return best, feasible_count


def shift(plan):
    return tuple(plan[1:]) + (Q(0),)


def terminal_invariant():
    return A * TERMINAL + W <= TERMINAL and Q(0) in GRID


def run_case(initial, case, steps=24):
    x = initial
    belief = (Q(-1), Q(1))
    if case != "all_missing":
        belief = update(belief, x + V)
    plan = (Q(0),) * HORIZON
    assert feasible(belief, plan) and terminal_invariant()
    violations = misses = receptions = optimizer_changes = 0
    max_width = Q(0)
    max_abs_x = abs(x)
    max_abs_u = Q(0)
    for t in range(steps):
        assert contains(belief, x)
        assert feasible(belief, plan)
        selected, _ = optimize(belief, plan)
        optimizer_changes += selected != plan
        assert feasible(belief, selected)
        u = selected[0]  # chosen BEFORE the next disturbance or packet outcome
        w = W if (t + case.count("e")) % 2 else -W
        x_next = A * x + u + w
        predicted = predict(belief, u)
        receive = (case == "all_received" or
                   (case == "alternating" and t % 2 == 0) or
                   (case == "sparse" and t % 5 == 0))
        y = x_next + (V if t % 3 else -V) if receive else None
        new_belief = update(predicted, y)
        new_plan = shift(selected)
        assert contains(new_belief, x_next)
        assert feasible(new_belief, new_plan)
        assert abs(x_next) <= X and abs(u) <= U
        violations += int(abs(x_next) > X or abs(u) > U)
        receptions += int(receive)
        misses += int(not receive)
        max_width = max(max_width, new_belief[1] - new_belief[0])
        max_abs_x = max(max_abs_x, abs(x_next))
        max_abs_u = max(max_abs_u, abs(u))
        x, belief, plan = x_next, new_belief, new_plan
    return dict(steps=steps, violations=violations, missed=misses,
                received=receptions, optimizer_changes=optimizer_changes,
                max_width=str(max_width), max_abs_x=str(max_abs_x),
                max_abs_u=str(max_abs_u))


def run():
    cases = ("all_received", "alternating", "sparse", "all_missing")
    starts = (Q(-9, 10), Q(-3, 10), Q(3, 10), Q(9, 10))
    records = [run_case(x, case) for case in cases for x in starts]
    return {
        "status": "PASS", "evidence_level": "EXACT_SCALAR_CONTRACT_PLUS_FINITE_REPLAY",
        "scope": "scalar stable proxy; not planar/6-state quadrotor or Gate A RCI",
        "model": {"a": str(A), "w_halfwidth": str(W),
                  "measurement_halfwidth": str(V), "state_bound": str(X),
                  "input_bound": str(U), "terminal_bound": str(TERMINAL),
                  "horizon": HORIZON, "grid": [str(u) for u in GRID]},
        "terminal_invariant": terminal_invariant(),
        "initial_zero_plan_feasible": feasible((Q(-1), Q(1)), (Q(0),) * HORIZON),
        "episodes": len(records), "steps": sum(r["steps"] for r in records),
        "missed_packets": sum(r["missed"] for r in records),
        "received_packets": sum(r["received"] for r in records),
        "optimizer_changes": sum(r["optimizer_changes"] for r in records),
        "violations": sum(r["violations"] for r in records),
        "max_abs_x": str(max(Q(r["max_abs_x"]) for r in records)),
        "max_abs_u": str(max(Q(r["max_abs_u"]) for r in records)),
        "max_posterior_width": str(max(Q(r["max_width"]) for r in records)),
        "limitations": ["finite-grid optimality, not continuous QP optimality",
                        "sampled trajectories are not proof of physical UAV safety",
                        "recursive feasibility proof uses exact scalar terminal inclusion"]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    encoded = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")


if __name__ == "__main__":
    main()
