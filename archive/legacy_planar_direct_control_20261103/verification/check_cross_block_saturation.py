"""Run218: exact witness for saturation of a cross-block outer support.

A maximizing point of P=(P_pv x P_phiomega) that satisfies every valid
cross-block history strip is also a maximizer over the intersection.  This
is an exact, inexpensive *no-gain* certificate for one support direction;
it does not establish full posterior membership, plant viability, or MPC
feasibility.  All inequalities are evaluated with Fraction, no tolerance.
"""
from fractions import Fraction as Q

Z = Q(0)

def dot(a, b):
    if len(a) != len(b):
        raise ValueError('dimension mismatch')
    return sum((Q(x) * Q(y) for x, y in zip(a, b)), Z)

def support_saturation(pv, ao, direction, strips):
    """Return a sufficient exact witness that all strips leave support intact.

    The product polygons must be nonempty and supplied with their vertices;
    strips are (4D coefficients, center, nonnegative radius).  An absent
    witness is *inconclusive*; it is not an infeasibility certificate.
    """
    if not pv or not ao or len(direction) != 4:
        raise ValueError('invalid product/direction')
    if any(len(v) != 2 for v in pv) or any(len(v) != 2 for v in ao):
        raise ValueError('polygon dimension mismatch')
    for c, d, r in strips:
        if len(c) != 4 or Q(r) < 0:
            raise ValueError('invalid strip')
    pmax = max(dot(direction[:2], v) for v in pv)
    amax = max(dot(direction[2:], v) for v in ao)
    candidates = (tuple(p) + tuple(a)
                  for p in pv if dot(direction[:2], p) == pmax
                  for a in ao if dot(direction[2:], a) == amax)
    for x in candidates:
        margins = tuple(Q(r) - abs(dot(c, x) - Q(d)) for c, d, r in strips)
        if all(s >= 0 for s in margins):
            return {'saturated': True, 'product_support': pmax + amax,
                    'witness': x, 'strip_margins': margins,
                    'joint_support': pmax + amax}
    return {'saturated': False, 'product_support': pmax + amax,
            'witness': None, 'strip_margins': None,
            'joint_support': None}

def audit_tick193():
    """Actual repository integration, replaying only causal data through k=192.

    The full checkout must be importable with PYTHONPATH=verification.  The
    returned exact support equality covers only the six specified historical
    cross-block strips and the Run216 product H outer approximation.
    """
    import check_rolling_history_support as prior
    import check_joint_history_strips as hist
    import check_joint_support_backup as joint
    import check_cross_block_history_support as cross
    box, truth, positions, attitudes, thrusts, torques = prior.replay_to_193(return_controls=True)
    vb, _ = prior.rolling_support(positions, attitudes, thrusts, 192, 6)
    pb = hist.position_support_three_packets(
        tuple((i, positions[i]) for i in (105, 165, 180)),
        attitudes, thrusts, 192, Q(7, 3))
    pv, ao = joint.history_polygons(box, positions, attitudes, thrusts, torques,
                                   192, position_bound=pb, velocity_bound=vb)
    packets = sorted(t for t in positions if t < 192)[-6:]
    strips = tuple(cross.cross_block_packet_strip(t, positions[t], 192,
                                                  thrusts, torques) for t in packets)
    if not all(cross.strip_residual(truth, s) <= 0 for s in strips):
        raise AssertionError('true state not contained in history strips')
    basis = [tuple(Q(int(i == j)) for i in range(4)) for j in range(4)]
    for _ in range(5):
        basis = [joint.step(v, joint.TMAX) for v in basis]
    direction = tuple(-basis[j][1] for j in range(4))
    result = support_saturation(pv, ao, direction, strips)
    obstruction = joint.obstruction_witness(pv, ao)
    if obstruction['physical_step'] != 5 or obstruction['state_index'] != 1:
        raise AssertionError('critical Run216 row has changed')
    if not result['saturated']:
        raise AssertionError('saturation witness not reproduced; investigate before merging')
    if Q(obstruction['best_case_slack_exact']) >= 0:
        raise AssertionError('previous finite-backup obstruction not reproduced')
    # Cross-check the independent one-strip exact LP dual for every packet.
    for strip in strips:
        bound = cross.one_strip_dual(pv, ao, direction, strip)
        if bound['upper'] != result['product_support']:
            raise AssertionError('one-strip dual disagrees with saturation witness')
    return {'tick': 193, 'packets': packets, 'pv_vertices': len(pv),
            'attitude_vertices': len(ao), 'critical_direction': list(map(str, direction)),
            'product_support_exact': str(result['product_support']),
            'joint_six_strip_support_exact': str(result['joint_support']),
            'support_gain_exact': '0', 'maximizing_point_exact': list(map(str, result['witness'])),
            'strip_margins_exact': list(map(str, result['strip_margins'])),
            'strip_margins_approx': list(map(lambda v: float(v), result['strip_margins'])),
            'old_best_case_slack_exact': obstruction['best_case_slack_exact'],
            'old_best_case_slack_approx': obstruction['best_case_slack_approx'],
            'conclusion': 'Six historical cross-block strips cannot improve this critical support row',
            'scope': 'four-state frozen Euler proxy; exact finite outer certificate; not complete SMF/CZ posterior'}

if __name__ == '__main__':
    import json
    print(json.dumps(audit_tick193(), indent=2))
