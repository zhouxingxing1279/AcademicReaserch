"""Run219: exact shared-residual history certificate for a critical support row.

For a fixed current state x_k and logged torques, eliminate past attitudes.
Every historical position packet is affine in the SAME residual variables r_j.
A weighted packet combination is a valid halfspace in x_k after taking the
support of those shared residuals. This is a necessary outer constraint, NOT
an exact CZ posterior or a recursive MPC safety certificate.
"""
from fractions import Fraction as Q

Z = Q(0)
H = J = Q(1, 50)
SIGMA_P = Q(1, 50)


def dot(a, b):
    return sum((Q(x) * Q(y) for x, y in zip(a, b)), Z)


def rad(t):
    return Q(47, 25) + Q(243, 16000) * Q(t)


def shared_packet_form(weights, positions, thrusts, torques, k,
                       h=H, inertia=J, sigma=SIGMA_P, radius=rad):
    """Return (c,C,B) such that |C+c@x_k|<=B for every legal history.

    x_k=(p,v,phi,omega), Euler p+=p+h*v, v+=v+h*(-T*phi+r),
    phi+=phi+h*omega, omega+=omega+h*u/J. Position packet y_a=p_a+e_a.
    All known applied torques and thrusts must be indexed before k.
    The same r_j is used for every packet, before the absolute-value bound.
    """
    if not weights or not isinstance(k, int) or not (h > 0 and inertia > 0 and sigma >= 0):
        raise ValueError('invalid history or model')
    weights = {int(a): Q(v) for a, v in weights.items() if Q(v)}
    if not weights or min(weights) < 1 or max(weights) >= k:
        raise ValueError('packets must be observed before the decision')
    a0 = min(weights)
    if any(a not in positions for a in weights):
        raise ValueError('missing packet')
    if any(j not in thrusts or j not in torques for j in range(a0, k)):
        raise ValueError('missing applied history')
    offsets = {}
    phi = omega = Z
    for j in range(k - 1, a0 - 1, -1):
        prev_omega = omega - h * Q(torques[j]) / inertia
        phi, omega = phi - h * prev_omega, prev_omega
        offsets[j] = phi
    cp = -sum(weights.values(), Z)
    cv = h * sum((Q(k - a) * w for a, w in weights.items()), Z)
    cphi = comega = Z
    constant = sum((w * Q(positions[a]) for a, w in weights.items()), Z)
    bound = sigma * sum((abs(w) for w in weights.values()), Z)
    for j in range(a0, k):
        w = sum((v * Q(j - a + 1) for a, v in weights.items() if a <= j), Z)
        if not w:
            continue
        t = Q(thrusts[j])
        if t < 0:
            raise ValueError('negative thrust')
        coeff = h * h * w * t
        cphi += coeff
        comega -= coeff * Q(k - j) * h
        constant += coeff * offsets[j]
        bound += h * h * abs(w) * Q(radius(t))
    return (cp, cv, cphi, comega), constant, bound


def product_support(pv, ao, direction):
    if not pv or not ao or len(direction) != 4:
        raise ValueError('invalid product or direction')
    return max(dot(direction[:2], v) for v in pv) + max(dot(direction[2:], v) for v in ao)


def clipped_product_support(pv, ao, direction, c, rhs):
    """Exact support of (polygon_pv x polygon_ao) intersect {c@x<=rhs}.

    A vertex of the clipped 4D product lies at an original product vertex
    or at the intersection of its boundary with a product edge. Enumerate
    both edge families; do not use floating point or discard failed rows.
    """
    if not pv or not ao or len(direction) != 4 or len(c) != 4:
        raise ValueError('invalid polytope')
    candidates = []
    for p in pv:
        for a in ao:
            x = tuple(p) + tuple(a)
            if dot(c, x) <= rhs:
                candidates.append(x)
    edges = []
    for i, p in enumerate(pv):
        for a in ao:
            edges.append((tuple(p) + tuple(a), tuple(pv[(i + 1) % len(pv)]) + tuple(a)))
    for i, a in enumerate(ao):
        for p in pv:
            edges.append((tuple(p) + tuple(a), tuple(p) + tuple(ao[(i + 1) % len(ao)])))
    for x, y in edges:
        fx, fy = dot(c, x) - rhs, dot(c, y) - rhs
        if fx * fy < 0:
            t = fx / (fx - fy)
            z = tuple(u + t * (v - u) for u, v in zip(x, y))
            assert dot(c, z) == rhs
            candidates.append(z)
    if not candidates:
        raise ValueError('empty clipped product')
    return max((dot(direction, x) for x in candidates)), len(candidates)


def certify_direction(pv, ao, direction, form, truth=None):
    """Exclude all original maximizers and quantify gain using one valid row.

    Failure to exclude a maximizer is inconclusive, not proof of feasibility.
    The clipped support is an UPPER bound for the full-history posterior.
    """
    c, constant, bound = form
    old = product_support(pv, ao, direction)
    maximizers = [tuple(p) + tuple(a) for p in pv for a in ao
                  if dot(direction, tuple(p) + tuple(a)) == old]
    values = [constant + dot(c, x) for x in maximizers]
    sign = Q(1) if values[0] > bound else Q(-1)
    if not all(sign * v > bound for v in values):
        return {'all_maximizers_excluded': False, 'old_support': old,
                'new_support_upper': None, 'gain_lower': None}
    signed_c = tuple(sign * z for z in c)
    rhs = bound - sign * constant
    if truth is not None and dot(signed_c, truth) > rhs:
        raise AssertionError('true state excluded: history or model inconsistent')
    new, count = clipped_product_support(pv, ao, direction, signed_c, rhs)
    assert new < old
    return {'all_maximizers_excluded': True, 'old_support': old,
            'new_support_upper': new, 'gain_lower': old - new,
            'exclusion_margin_min': min(sign * v - bound for v in values),
            'maximizer_count': len(maximizers), 'clipped_candidates': count,
            'signed_row': signed_c, 'signed_rhs': rhs}


def audit_tick193():
    """Optional full-checkout integration; replay uses only causal data."""
    import check_rolling_history_support as prior
    import check_joint_history_strips as hist
    import check_joint_support_backup as joint
    box, truth, positions, attitudes, thrusts, torques = prior.replay_to_193(return_controls=True)
    vb, _ = prior.rolling_support(positions, attitudes, thrusts, 192, 6)
    pb = hist.position_support_three_packets(
        tuple((i, positions[i]) for i in (105, 165, 180)),
        attitudes, thrusts, 192, Q(7, 3))
    pv, ao = joint.history_polygons(box, positions, attitudes, thrusts, torques,
                                   192, position_bound=pb, velocity_bound=vb)
    direction = (Z, Q(-1), Q(2943, 2000), Q(2943, 50000))
    weights = {135: Q(1), 165: Q(-6), 180: Q(5)}
    form = shared_packet_form(weights, positions, thrusts, torques, 192)
    result = certify_direction(pv, ao, direction, form, truth)
    if not result['all_maximizers_excluded']:
        raise AssertionError('history exclusion no longer reproduces')
    if result['exclusion_margin_min'] != Q(5212367, 500000000):
        raise AssertionError('shared-residual exact margin changed')
    if result['gain_lower'] != Q(5212367, 450000000):
        raise AssertionError('exact support improvement changed')
    obstruction = joint.obstruction_witness(pv, ao)
    remaining = Q(obstruction['best_case_slack_exact']) + result['gain_lower']
    if remaining >= 0:
        raise AssertionError('unexpected certificate recovery; re-audit all rows')
    return {'decision_tick': 193, 'packets': list(weights),
            'shared_residual_exclusion_exact': str(result['exclusion_margin_min']),
            'critical_support_gain_exact': str(result['gain_lower']),
            'critical_support_gain_approx': float(result['gain_lower']),
            'remaining_single_row_slack_exact': str(remaining),
            'remaining_single_row_slack_approx': float(remaining),
            'all_original_support_maximizers_excluded': True,
            'truth_contained': True, 'gate_A': 'blocked',
            'scope': 'necessary shared-residual halfspace, not full posterior or terminal MPC'}


if __name__ == '__main__':
    import json
    print(json.dumps(audit_tick193(), indent=2))
