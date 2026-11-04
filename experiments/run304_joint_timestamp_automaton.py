#!/usr/bin/env python3
"""Exhaustive finite-state check of joint timestamp age/span bounds.

Candidate contract:
- At most M consecutive sample-generation misses.
- Every generated sample is delivered after an arbitrary integer delay in [0, L].
- Delivery may be out of order and multiple samples may arrive in one step.
- A miss means no sample is generated; a generated sample is not permanently lost.
"""
from collections import deque
import csv
import sys
from pathlib import Path


def explore(max_misses: int, max_delay: int) -> dict:
    M, L = max_misses, max_delay
    warmup = 2 * (M + 1) + L - 1
    age_bound = M + L
    span_bound = M + max(1, L)

    # (consecutive misses, pending sample ages, newest age, second-newest age, phase)
    initial = (0, (), None, None, 0)
    seen = {initial}
    queue = deque([initial])
    edges = 0
    max_age = 0
    max_span = 0

    while queue:
        miss, pending, age1, age2, phase = queue.popleft()
        for success in (False, True):
            if not success and miss >= M:
                continue

            # Move to the current receive instant, then optionally generate a new sample.
            samples = tuple(age + 1 for age in pending) + ((0,) if success else ())
            old_received = [age + 1 for age in (age1, age2) if age is not None]

            # Enumerate every delivery subset; samples reaching age L must be delivered.
            for mask in range(1 << len(samples)):
                if any(age >= L and not ((mask >> i) & 1)
                       for i, age in enumerate(samples)):
                    continue

                delivered = [age for i, age in enumerate(samples) if (mask >> i) & 1]
                remains = tuple(sorted(
                    age for i, age in enumerate(samples) if not ((mask >> i) & 1)
                ))

                # Ages are unique because each generated timestamp is unique.
                received = sorted(set(old_received + delivered))
                new_age1 = received[0] if len(received) >= 1 else None
                new_age2 = received[1] if len(received) >= 2 else None

                if phase >= warmup:
                    assert new_age1 is not None and new_age2 is not None, (
                        M, L, phase, miss, pending, age1, age2, success, mask
                    )
                    assert new_age1 <= age_bound, (M, L, new_age1, age_bound)
                    span = new_age2 - new_age1
                    assert span <= span_bound, (M, L, span, span_bound)
                    max_age = max(max_age, new_age1)
                    max_span = max(max_span, span)

                new_phase = min(phase + 1, warmup + 1)
                new_state = (
                    0 if success else miss + 1,
                    remains,
                    new_age1,
                    new_age2,
                    new_phase,
                )
                edges += 1
                if new_state not in seen:
                    seen.add(new_state)
                    queue.append(new_state)

    return {
        "M": M,
        "L": L,
        "warmup_K": warmup,
        "H_age_bound": age_bound,
        "D_span_bound": span_bound,
        "reachable_states": len(seen),
        "transitions": edges,
        "max_observed_age": max_age,
        "max_observed_span": max_span,
    }


def main() -> None:
    rows = [explore(M, L) for M in range(6) for L in range(6)]
    for row in rows:
        # Equality is a finite-range tightness check, not the proof for all M,L.
        assert row["max_observed_age"] == row["H_age_bound"], row
        assert row["max_observed_span"] == row["D_span_bound"], row

    total_states = sum(row["reachable_states"] for row in rows)
    total_edges = sum(row["transitions"] for row in rows)
    assert total_states == 53580
    assert total_edges == 572957

    root = Path(__file__).resolve().parents[1]
    output = root / "experiments" / "results" / "run304_joint_timestamp_automaton.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Python {sys.version.split()[0]}; standard library only; no solver or RNG")
    print(f"parameter_pairs={len(rows)} reachable_states={total_states} transitions={total_edges}")
    print(f"result_csv={output.relative_to(root)}")
    print("PASS: every reachable transition satisfies the derived age/span bounds for M,L=0..5")


if __name__ == "__main__":
    main()
