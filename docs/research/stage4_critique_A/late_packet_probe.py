"""Stage-4 review probe. One illustrative word, zero readouts, scalar ZOH.

Fraction witnesses and analytic support upper bounds establish the six radii.
An independent HiGHS trajectory LP cross-checks them in floating point.
Run from the repository root with .venv/Scripts/python -B path/to/this_file.
"""
from fractions import Fraction as Q

import numpy as np
from scipy.optimize import linprog

T, A_MAX, N = Q(1, 2), Q(1, 50), Q(1, 200)
V0 = Q(1, 100)
# Even stamps are absent; after 9 the word may continue with on-time packets.
DELIVERY = {1: 1, 3: 5, 5: 7, 7: 9, 9: 9}


def available(k, keep):
    return tuple(s for s, t in DELIVERY.items()
                 if t <= k and (keep or t <= 4 * (s // 4 + 1)))


def radius_bound(k, stamps):
    # v(k) from the initial velocity or from any two observed positions.
    bounds = [V0 + k * T * A_MAX]
    for s in stamps:
        for t in stamps:
            if s < t:
                span = (t - s) * T
                bounds.append(2 * N / span + span * A_MAX / 2 + (k - t) * T * A_MAX)
    return min(bounds)


def extremal_path(k, stamps):
    # Attaining trajectories for the positive support; reflections attain its negative.
    if stamps == (1,):
        p, v, ws = -N, V0, [A_MAX] * k
    elif stamps == (1, 3):
        p, v, ws = -N, Q(0), [Q(0)] + [A_MAX] * (k - 1)
    elif stamps == (1, 5):
        p, v, ws = Q(1, 800), -V0, [-V0] + [A_MAX] * (k - 1)
    elif stamps == (1, 3, 5):
        p, v, ws = -N, Q(0), [Q(0)] * 3 + [A_MAX] * (k - 3)
    else:
        raise ValueError(stamps)
    assert abs(p) <= N and abs(v) <= V0
    for s, w in enumerate(ws, 1):
        assert abs(w) <= A_MAX
        p, v = p + T * v + T**2 * w / 2, v + T * w
        if s in stamps:
            assert abs(p) <= N  # y_s=0 is attained by nu_s=-p.
    return v


def trajectory_lp(k, stamps):
    # Independent lifted path coordinates (p_i,v_i,w_i), exact ZOH equalities.
    state_count = 2 * (k + 1)
    dim = state_count + k
    eq = np.zeros((2 * k, dim))
    for i in range(k):
        p, v, w = 2*i, 2*i+1, state_count+i
        eq[2*i, [p+2, p, v, w]] = [1, -1, -T, -T**2/2]
        eq[2*i+1, [v+2, v, w]] = [1, -1, -T]
    bounds = [(None, None)] * state_count + [(-A_MAX, A_MAX)] * k
    bounds[:2] = [(-N, N), (-V0, V0)]
    for s in stamps:
        bounds[2*s] = (-N, N)
    objective = np.zeros(dim)
    objective[2*k+1] = -1
    result = linprog(objective, A_eq=eq, b_eq=np.zeros(2*k), bounds=bounds, method="highs")
    assert result.success, result.message
    return -result.fun


if __name__ == "__main__":
    assert all(s <= t <= s+2 for s, t in DELIVERY.items())
    assert all({s, s+1} & DELIVERY.keys() for s in range(9))
    for k in (4, 5, 8):
        for keep in (False, True):
            stamps = available(k, keep)
            bound = radius_bound(k, stamps)
            assert extremal_path(k, stamps) == bound
            numeric = trajectory_lp(k, stamps)
            assert abs(float(bound) - numeric) <= 1e-10
            print(k, "keep" if keep else "drop", stamps, str(bound), f"{numeric:.6f}")
