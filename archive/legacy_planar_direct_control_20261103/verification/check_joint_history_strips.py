"""Run215: causal exact-rational joint outer strips for the four-state Euler proxy.

This is an intersection of a state box and valid linear inequalities, NOT an
exact history-consistent posterior or a certified MPC controller. All strips
are necessary conditions; passing a strip does not establish attainability.
"""
from __future__ import annotations
from fractions import Fraction as Q

ZERO = Q(0)


def position_velocity_strip(packet_tick, packet_position, end_tick, attitudes, thrusts,
                            h=Q(1, 50), position_noise=Q(1, 50),
                            attitude_noise=Q(1, 200), residual_radius=None):
    """Return center,radius of p_k - (k-a)h*v_k using data available at k.

    Euler: p+ = p+h*v, v+ = v+h*(-T*phi+r).
    The prior packet is y_a=p_a+e_a, |e_a|<=position_noise.
    Each attitude observation y_i=phi_i+e_i, |e_i|<=attitude_noise.
    Disturbance r_i lies in [-residual_radius(T_i),residual_radius(T_i)].
    All uncertainties are independently relaxed, hence this is a safe OUTER
    strip even if true state/measurement errors are correlated across time.
    """
    if not (0 <= packet_tick < end_tick):
        raise ValueError('packet must precede current decision')
    if residual_radius is None:
        residual_radius = lambda t: Q(47, 25) + Q(243, 16000) * t
    center = Q(packet_position)
    radius = Q(position_noise)
    for i in range(packet_tick, end_tick):
        if i not in attitudes or i not in thrusts:
            raise ValueError('missing causal attitude/thrust history')
        t = Q(thrusts[i]); y = Q(attitudes[i]); w = (i-packet_tick+1)*h*h
        if t < 0: raise ValueError('negative thrust')
        center += w*t*y
        radius += w*(t*attitude_noise + residual_radius(t))
    return center, radius


def attitude_rate_strip(last_attitude, last_torque, h=Q(1, 50),
                        inertia=Q(1, 50), attitude_noise=Q(1, 200)):
    """Return center,radius of phi_k - h*omega_k from phi_{k-1} measurement.

    phi_k-h*omega_k=phi_{k-1}-(h*h/J)*u_{k-1} exactly.
    The applied u_{k-1} must be from the logged causal controller, not truth.
    """
    return Q(last_attitude) - h*h/inertia*Q(last_torque), Q(attitude_noise)


def residual(value, strip):
    center, radius = strip
    return abs(Q(value)-center)-radius


def audit_corner(box, positions, attitudes, thrusts, torques, end_tick,
                 max_packets=6, h=Q(1, 50)):
    """Audit Run214's adverse joint box corner against necessary history strips.

    box=(p,v,phi,omega) intervals, using (p_lo,v_lo,phi_hi,omega_hi).
    Returns exact rational signed margins: positive means mathematically
    EXCLUDED by historical observations and the assumed Euler model.
    Nonpositive means inconclusive (not a feasibility certificate).
    """
    if end_tick <= 0 or end_tick-1 not in torques or end_tick-1 not in attitudes:
        raise ValueError('missing most recent applied torque or attitude')
    corner = (box[0][0], box[1][0], box[2][1], box[3][1])
    packet_ticks = sorted(t for t in positions if t < end_tick)[-max_packets:]
    p_margins = []
    for a in packet_ticks:
        strip = position_velocity_strip(a, positions[a], end_tick, attitudes, thrusts, h=h)
        lhs = corner[0] - (end_tick-a)*h*corner[1]
        p_margins.append((a, residual(lhs, strip)))
    ar = attitude_rate_strip(attitudes[end_tick-1], torques[end_tick-1], h=h)
    ar_margin = residual(corner[2]-h*corner[3], ar)
    excluded = any(margin > 0 for _, margin in p_margins) or ar_margin > 0
    return {'excluded': excluded, 'corner': tuple(map(str, corner)),
            'position_velocity_margins': [(a, str(v)) for a, v in p_margins],
            'attitude_rate_margin': str(ar_margin),
            'status': 'excluded_by_necessary_history_strip' if excluded else 'inconclusive'}


def position_support_three_packets(packets, attitudes, thrusts, end_tick, q,
                                   h=Q(1, 50), position_noise=Q(1, 50),
                                   attitude_noise=Q(1, 200), residual_radius=None):
    """Exact OUTER support for p_k from three historical position packets.

    The coefficient family satisfies sum c_j=1 and sum c_j*(j-a)=k-a.
    A chosen rational q is a valid certificate; optimizing q is optional.
    This bound is not an exact posterior and relaxes disturbance correlations.
    """
    (a, pa), (b, pb), (c, pc) = packets
    if not (0 <= a < b < c <= end_tick):
        raise ValueError('invalid packet order')
    if residual_radius is None:
        residual_radius = lambda t: Q(47, 25) + Q(243, 16000) * t
    q = Q(q)
    cb = (Q(end_tick-a)-(c-a)*q)/(b-a)
    ca = Q(1)-cb-q
    center = ca*Q(pa)+cb*Q(pb)+q*Q(pc)
    radius = position_noise*(abs(ca)+abs(cb)+abs(q))
    for i in range(a, end_tick):
        if i not in attitudes or i not in thrusts:
            raise ValueError('missing causal history')
        t = Q(thrusts[i]); y = Q(attitudes[i])
        if t < 0: raise ValueError('negative thrust')
        w = h*h*(max(end_tick-1-i,0)-cb*max(b-1-i,0)-q*max(c-1-i,0))
        center -= w*t*y
        radius += abs(w)*(t*attitude_noise+residual_radius(t))
    return center-radius, center+radius


def audit_reachable_run214():
    """Full-repository integration: Run214 exact history, no future data.

    Run214 must expose the logged causal torques via return_controls=True.
    All findings are conditional on that frozen four-state model/history.
    """
    import check_rolling_history_support as previous
    import check_nominal_short_mpc as base
    import check_reachable_smf_backup_rollout as m
    box, truth, positions, attitudes, thrusts, torques = previous.replay_to_193(return_controls=True)
    assert all(a <= z <= b for (a, b), z in zip(box, truth))
    original_corner = audit_corner(box, positions, attitudes, thrusts, torques, 192)
    p_bound = position_support_three_packets(
        tuple((i, positions[i]) for i in (105, 165, 180)),
        attitudes, thrusts, 192, Q(7, 3))
    assert p_bound[0] > box[0][0]
    assert p_bound[0] <= truth[0] <= p_bound[1]
    refined = ((p_bound[0], min(box[0][1],p_bound[1])), box[1], box[2], box[3])
    # Independent re-audit uses the existing box-reset controller, not a new
    # joint-polytope optimizer. This intentionally retains its conservatism.
    allowed, reason = base.interval(refined, m.TMAX)
    assert allowed is None
    for a in sorted(positions)[-6:]:
        strip = position_velocity_strip(a, positions[a], 192, attitudes, thrusts)
        assert residual(truth[0] - (192-a)*Q(1,50)*truth[1], strip) <= 0
    ar = attitude_rate_strip(attitudes[191], torques[191])
    assert residual(truth[2]-Q(1,50)*truth[3], ar) <= 0
    return {'position_lower_improvement_exact':str(p_bound[0]-box[0][0]),
            'position_lower_improvement_m':float(p_bound[0]-box[0][0]),
            'original_corner_excluded_by_position_support':box[0][0]<p_bound[0],
            'original_corner_strip_audit':original_corner,
            'refined_backup_feasible':allowed is not None,
            'refined_backup_reason':reason,
            'truth_contained':True,
            'interpretation':'exact historical outer exclusion; not exact CZ, not recursive feasibility'}


if __name__ == '__main__':
    import json
    print(json.dumps(audit_reachable_run214(), indent=2))
