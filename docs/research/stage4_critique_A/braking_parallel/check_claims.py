"""Verify independent research claims and audit a streaming, sufficient discard rule."""

import json
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path

from brake_oracle import CONTRACT_SHA, K, exact_oracle, language, latest, position_row

HERE = Path(__file__).resolve().parent


def check_lower_bounds(masks):
    # Residuals use units of 1/400 m. Both paths have upper initial velocity
    # and upper acceleration. Their positions differ by exactly 1/100 m.
    mid = [2 * s + s * s for s in range(5)]
    high = exact_oracle(mid)
    Bmax = Q(12, 5) + Q(mid[4] + 2, 400) + Q(25, 199) * Q(5, 4) ** 2
    pairs = []
    for r in range(5):
        low_values = mid.copy()
        low_values[r] -= 4
        low = exact_oracle(low_values)
        for m in masks:
            if m & (1 << r):
                kept = m & ~(1 << r)
                assert low[kept][0] == high[kept][0] == high[m][0] == Bmax
                assert low[m][0] == Bmax - Q(1, 100)
                pairs.append((m, r))
    # An independently derived inner witness (adversary report), with all
    # readouts inside the panels' nominal noise envelope, but distinct histories.
    a = exact_oracle([-2] * 5)
    b = exact_oracle([2, -2, -2, -2, -2])
    assert a[31][0] == b[30][0] == Q(51481, 19900)
    assert b[31][0] == Q(10088569, 3900400)
    assert b[31][0] < Q("2.58675") < b[30][0]
    # W4 loses data only when all five stamps have arrived, so stamps 2 and
    # 4 remain. For any two suffix-compatible trajectories the bounds below
    # follow from the measured positions one second apart and bounded acceleration.
    dp = 2 * Q(1, 200)
    dv = 4 * Q(1, 200) + Q(1, 50)
    vmax = Q(5, 4)
    upper = dp + (vmax**2 - (vmax - dv) ** 2) / (2 * Q(199, 50))
    assert upper == Q(89, 3980) and Q(1, 100) <= upper
    return dict(
        checked_mask_stamp_pairs=len(pairs),
        upper_peak=str(Bmax),
        lower_peak=str(Bmax - Q(1, 100)),
        indistinguishable_gap="1/100",
        W4_all_data_extra_distance_bounds_m=["1/100", str(upper)],
        adversary_pair=[str(a[31][0]), str(b[31][0])],
    )


def events():
    unique = set()
    for delays in product((-1, 0, 1, 2), repeat=5):
        if any(a == b == -1 for a, b in zip(delays, delays[1:])):
            continue
        unique.add(tuple(sorted((s + d, s) for s, d in enumerate(delays) if d >= 0 and s + d <= 4)))
    return sorted(unique)


def suffix_loss_bound(available, budget):
    """Readout-independent upper bound on B(W_j)-B(F) at decision four."""
    retained = latest(available, budget)
    if retained == available:
        return Q(0)
    stamps = [s for s in range(5) if retained & (1 << s)]
    T = Q(1, 2)
    delta_a = Q(1, 25)  # difference of two admissible process accelerations
    dp0, dv0 = Q(1, 100), Q(1, 50)
    elapsed = K * T
    dp = dp0 + elapsed * dv0 + delta_a * elapsed**2 / 2
    dv = dv0 + delta_a * elapsed
    for t in stamps:
        # Relative endpoint velocity from the chord between two retained stamps.
        dv_t = dv0 + delta_a * t * T
        for s in stamps:
            if s < t:
                span = (t - s) * T
                dv_t = min(dv_t, 2 * dp0 / span + delta_a * span / 2)
        age = (K - t) * T
        dv = min(dv, dv_t + delta_a * age)
        dp = min(dp, dp0 + dv_t * age + delta_a * age**2 / 2)
    vmax = Q(5, 4)
    return dp + (vmax**2 - (vmax - dv) ** 2) / (2 * Q(199, 50))


def discardable(old, kept, ys, box_only):
    # Every candidate interval individually contains P_old x for every x
    # satisfying the retained strips and prior. Intersect before testing inclusion.
    row = position_row(old)
    radius = sum(map(abs, row))
    lower, upper = -radius, radius
    weights = [] if box_only else [((s, 1),) for s in kept]
    if not box_only:
        for a, b in combinations(kept, 2):
            t = Q(old - a, b - a)
            weights.append(((a, 1 - t), (b, t)))
    for terms in weights:
        center = sum(l * ys[s] for s, l in terms)
        error = 2 * sum(abs(l) for _, l in terms)
        error += sum(
            abs(v - sum(l * position_row(s)[i] for s, l in terms)) for i, v in enumerate(row)
        )
        lower = max(lower, center - error)
        upper = min(upper, center + error)
    return ys[old] - 2 <= lower and upper <= ys[old] + 2


def stream_audit(ys, best, box_only):
    tally = Counter()
    for prefix in events():
        kept = []
        peak_after = peak_during = 0
        for _, s in prefix:
            kept.append(s)
            kept.sort()
            peak_during = max(peak_during, len(kept))
            while kept and discardable(kept[0], kept[1:], ys, box_only):
                kept.pop(0)
            peak_after = max(peak_after, len(kept))
        F = sum(1 << s for _, s in prefix)
        R = sum(1 << s for s in kept)
        assert best[F][0] == best[R][0]
        tally["records"] += 1
        tally["reduced_final_records"] += int(R != F)
        tally["stored_values_final_sum"] += len(kept)
        tally["full_values_final_sum"] += len(prefix)
        tally["worst_persistent_values"] = max(tally["worst_persistent_values"], peak_after)
        tally["worst_with_incoming"] = max(tally["worst_with_incoming"], peak_during)
    return dict(tally)


def main():
    _, _, masks = language()
    result = dict(contract_sha256=CONTRACT_SHA, lower_bound=check_lower_bounds(masks), stream={})
    bounds = {mask: [suffix_loss_bound(mask, j) for j in range(6)] for mask in masks}
    result["tolerance_certificate"] = {
        "per_stamp_mask_upper_m": {str(m): list(map(str, v)) for m, v in sorted(bounds.items())},
        "all_masks_upper_m": [str(max(v[j] for v in bounds.values())) for j in range(6)],
        "fixed_four_upper_m": str(max(v[4] for v in bounds.values())),
    }
    assert max(v[4] for v in bounds.values()) == Q(89, 3980)
    for name, ys in [("H0", [0] * 5), ("H1", [2, -2, 2, -2, 2])]:
        best = exact_oracle(ys)
        result["stream"][name] = {
            rule: stream_audit(ys, best, rule == "prior_only")
            for rule in ("prior_only", "one_two_stamp")
        }
        for mask in masks:
            assert best[mask][0] <= best[latest(mask, 0)][0]
            for j in range(6):
                assert 0 <= best[latest(mask, j)][0] - best[mask][0] <= bounds[mask][j]
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
