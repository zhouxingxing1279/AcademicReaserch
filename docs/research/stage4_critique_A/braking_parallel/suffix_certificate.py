"""Independent reconstruction of the candidate team's dual suffix test."""

from fractions import Fraction as Q
from itertools import combinations
import json
from random import Random

from brake_oracle import ROWS, dot, exact_oracle, inverse_scaled, language, latest, position_row


def dual_tables():
    vel = (0, 1, 1, 1, 1, 1)
    p = position_row(4)
    queries = {"p": p, "v": vel, "both": tuple(x + y for x, y in zip(p, vel))}
    forms = {name: set() for name in queries}
    for basis in combinations(range(len(ROWS)), 6):
        inv = inverse_scaled([ROWS[i] for i in basis])
        if inv is None:
            continue
        matrix, den = inv
        for name, q in queries.items():
            coefficients = [Q(0)] * len(ROWS)
            for i, column in zip(basis, zip(*matrix), strict=True):
                coefficients[i] = Q(dot(q, column), den)
            const = sum(map(abs, coefficients[:6])) + 2 * sum(map(abs, coefficients[6:]))
            forms[name].add((const, *coefficients[6:]))
    return {
        name: [
            (sum(1 << i for i, v in enumerate(mu) if v), const, mu) for const, *mu in sorted(rows)
        ]
        for name, rows in forms.items()
    }


def scores(rows, y):
    return [(m, c + dot(mu, y)) for m, c, mu in rows]


def value(rows, available):
    return min(score for m, score in rows if not (m & ~available))


def suffix_length(rows, available):
    best = value(rows, available)
    ties = [m for m, score in rows if not (m & ~available) and score == best]
    return next(j for j in range(6) if any(not (m & ~latest(available, j)) for m in ties))


def main():
    forms = dual_tables()
    masks = language()[2]
    rng = Random(20261105)
    examples = [[0] * 5, [2, -2, 2, -2, 2]]
    for _ in range(8):
        true_cube = [rng.choice((-1, 0, 1)) for _ in range(6)]
        examples.append([dot(position_row(s), true_cube) + rng.randint(-2, 2) for s in range(5)])
    audited = 0
    for y in examples:
        best = exact_oracle(y)
        tables = {k: scores(rows, y) for k, rows in forms.items()}
        for m, (B, _) in best.items():
            p, v = value(tables["p"], m), value(tables["v"], m)
            assert value(tables["both"], m) == p + v
            assert B == Q(12, 5) + p / 400 + Q(25, 199) * (Q(6, 5) + v / 100) ** 2
            if m in masks:
                assert suffix_length(tables["both"], m) == next(
                    j for j in range(6) if best[latest(m, j)][0] == B
                )
            audited += 1
    # A hand-certified continuous family. The maximizing feasible vertex at
    # the tie has P0=-1, P4=0 and V=2.
    tie = (Q(-1, 2), -1, 0, 1, 1, 1)
    ps = [dot(position_row(s), tie) for s in range(5)]
    assert ps[0] == -1 and ps[-1] == 0 and sum(tie[1:]) == 2
    assert all(-4 <= p <= 0 for p in ps[1:])
    threshold = []
    for z0 in (Q(-2), Q(0), Q(9999, 10000), Q(1), Q(10001, 10000), Q(2)):
        y = [z0, -2, -2, -2, -2]
        t = scores(forms["both"], y)
        equal = value(t, 31) == value(t, 30)
        assert equal == (z0 <= 1)
        threshold.append([str(z0), equal])
    print(
        json.dumps(
            dict(
                distinct_forms={k: len(v) for k, v in forms.items()},
                mask_objective_checks=audited,
                minimum_suffix_checks=len(examples) * len(masks),
                readouts_400=examples,
                threshold_checks=threshold,
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
