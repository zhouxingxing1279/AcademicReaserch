#!/usr/bin/env python3
"""Run304 exhaustive timestamp automaton and exact finite-difference vertex checks."""
from collections import deque
from fractions import Fraction as F
from itertools import product
import csv
import sys
from pathlib import Path


def explore(M: int, L: int) -> dict:
    K, H, D = 2 * (M + 1) + L - 1, M + L, M + max(1, L)
    initial = (0, (), None, None, 0)  # misses, pending ages, newest, second-newest, phase
    seen, queue = {initial}, deque([initial])
    edges = max_age = max_span = 0
    while queue:
        miss, pending, a1, a2, phase = queue.popleft()
        for success in (False, True):
            if not success and miss >= M:
                continue
            samples = tuple(a + 1 for a in pending) + ((0,) if success else ())
            old = [a + 1 for a in (a1, a2) if a is not None]
            for mask in range(1 << len(samples)):
                if any(a >= L and not ((mask >> i) & 1) for i, a in enumerate(samples)):
                    continue
                delivered = [a for i, a in enumerate(samples) if (mask >> i) & 1]
                remains = tuple(sorted(a for i, a in enumerate(samples) if not ((mask >> i) & 1)))
                received = sorted(set(old + delivered))
                n1 = received[0] if received else None
                n2 = received[1] if len(received) > 1 else None
                if phase >= K:
                    assert n1 is not None and n2 is not None
                    assert n1 <= H
                    span = n2 - n1
                    assert span <= D
                    max_age, max_span = max(max_age, n1), max(max_span, span)
                ns = (0 if success else miss + 1, remains, n1, n2, min(phase + 1, K + 1))
                edges += 1
                if ns not in seen:
                    seen.add(ns)
                    queue.append(ns)
    return dict(M=M, L=L, warmup_K=K, H_age_bound=H, D_span_bound=D,
                reachable_states=len(seen), transitions=edges,
                max_observed_age=max_age, max_observed_span=max_span)


def exact_fd_velocity():
    T, A, N = F(1, 10), F(1, 5), F(1, 20)
    rows, total = [], 0
    for d in range(1, 7):
        worst = F(0)
        count = 0
        for acc in product((-A, A), repeat=d):
            for n0, n1 in product((-N, N), repeat=2):
                p = v = F(0)
                for a in acc:
                    p += T * v
                    v += T * a
                worst = max(worst, abs((p + n1 - n0) / (d * T)))
                count += 1
        bound = 2 * N / (d * T) + F(d - 1, 2) * T * A
        assert worst == bound
        rows.append(dict(test="velocity_at_oldest_timestamp", d=d, h="",
                         vertex_cases=count, max_exact_error=str(worst),
                         analytic_bound=str(bound)))
        total += count
    return rows, total


def exact_fd_position_velocity():
    T, A, N = F(1, 10), F(1, 5), F(1, 20)
    rows, total = [], 0
    for d in range(1, 5):
        for h in range(4):
            worst_v = worst_p = F(0)
            count = 0
            for ws in product((-A, A), repeat=d+h):
                for n0, n1 in product((-N, N), repeat=2):
                    p = v = F(0)
                    y0 = p + n0
                    pd = None
                    for i, w in enumerate(ws):
                        if i == d:
                            pd = p
                        p += T * v
                        v += T * w
                    if pd is None:
                        pd = p
                    y1 = pd + n1
                    vhat0 = (y1 - y0) / (d * T)
                    vhat1 = vhat0  # known input u=0 for this exact vertex test
                    phat = y1 + h * T * vhat1
                    gamma = 2 * N / (d * T) + F(d + 1, 2) * T * A
                    beta_v = gamma + h * T * A
                    beta_p = N + h*T*gamma + F(h*(h-1), 2)*T*T*A
                    worst_v, worst_p = max(worst_v, abs(v-vhat1)), max(worst_p, abs(p-phat))
                    assert abs(v-vhat1) <= beta_v
                    assert abs(p-phat) <= beta_p
                    count += 1
            rows.append(dict(test="current_position_velocity_box", d=d, h=h,
                             vertex_cases=count, max_exact_error=f"v={worst_v};p={worst_p}",
                             analytic_bound=f"v={beta_v};p={beta_p}"))
            total += count
    assert total == 1800
    return rows, total


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    rows = [explore(M, L) for M in range(6) for L in range(6)]
    for r in rows:
        assert r["max_observed_age"] == r["H_age_bound"]
        assert r["max_observed_span"] == r["D_span_bound"]
    states = sum(r["reachable_states"] for r in rows)
    edges = sum(r["transitions"] for r in rows)
    assert (states, edges) == (53580, 572957)
    fdv, nv = exact_fd_velocity()
    fdp, npv = exact_fd_position_velocity()
    assert nv == 504 and npv == 1800

    root = Path(__file__).resolve().parents[1]
    write_csv(root / "experiments/results/run304_joint_timestamp_automaton.csv", rows)
    write_csv(root / "experiments/results/run304_finite_difference_vertices.csv", fdv + fdp)
    print(f"Python {sys.version.split()[0]}; standard library only; no solver or RNG")
    print(f"automaton: pairs={len(rows)} states={states} transitions={edges}")
    print(f"finite-difference exact vertices: velocity={nv} position_velocity={npv}")
    print("PASS: timestamp automaton and exact rational finite-difference checks")


if __name__ == "__main__":
    main()
