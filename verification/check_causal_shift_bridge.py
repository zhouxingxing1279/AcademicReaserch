#!/usr/bin/env python3
"""Run207: exact one-step causal shift bridge for Run206's box-SMF proxy.

At time k choose u0 BEFORE any next measurement. For every possible next
measurement branch and every next visible thrust T1, certify that u1=0 belongs
to the next four-tick zero-tail backup interval. The certificate resets the
state to the full predicted coordinate box at k+1, deliberately discarding
cross-coordinate correlation. This is a sufficient ONE-STEP bridge, not an RCI
or infinite-horizon certificate.
"""
from __future__ import annotations
import argparse
import itertools
import json
from fractions import Fraction as Q

import check_reachable_smf_backup_rollout as m

Z=Q(0)

def bridge_audit(box,t0):
    """Exact u0 interval for first-step safety + 4-tick backup after box reset.

    Current T0 is known. Future T1..T4 may independently vary over the full
    thrust interval. Next measurement can only intersect the predicted box.
    The candidate next torque is zero, with three more zero backup torques.
    """
    assert m.TMIN<=t0<=m.TMAX
    c,r=m.box_center_radius(box)
    if any(abs(a)+b>lim for a,b,lim in zip(c,r,m.LIMITS)):
        return {'feasible':False,'reason':'current_outer_box_outside_hard_limits','inequalities':0}
    predicted=m.predict(box,t0,Z)
    x,rad=m.box_center_radius(predicted)
    coef=m.step((Z,)*4,t0,Q(1))
    allowed=(-m.UMAX,m.UMAX)
    count=0
    for i in range(4):
        allowed=m.constrain(allowed,x[i],coef[i],m.LIMITS[i]-rad[i])
        count+=1
    # Every coordinate is multi-affine in the independently varying T1..T4
    # for each fixed initial-error and disturbance primitive; checking all
    # thrust vertices is sufficient for the signed coordinate constraints.
    for future in itertools.product((m.TMIN,m.TMAX),repeat=4):
        center=x
        coefficient=coef
        generators=tuple(tuple(rad[i] if i==j else Z for i in range(4)) for j in range(4))
        for t in future:
            center=m.step(center,t,Z)
            coefficient=m.step(coefficient,t,Z)
            generators=tuple(m.step(g,t,Z) for g in generators)+((Z,m.H*m.rad(t),Z,Z),)
            for i in range(4):
                spread=sum(abs(g[i]) for g in generators)
                allowed=m.constrain(allowed,center[i],coefficient[i],m.LIMITS[i]-spread)
                count+=1
    feasible=allowed[0]<=allowed[1]
    return {'feasible':feasible,
            'reason':'one_step_shift_bridge' if feasible else 'empty_shift_bridge_interval',
            'lower':str(allowed[0]),'upper':str(allowed[1]),
            'inequalities':count,'future_thrust_vertices':16,
            'next_backup_torque':'0','next_backup_horizon':4}

def bridge_filter(box,t0):
    cert=bridge_audit(box,t0)
    if not cert['feasible']:
        return None,cert
    u=m.proposed(box)
    return max(Q(cert['lower']),min(Q(cert['upper']),u)),cert

def verify_shift(box,t0,u,t1):
    """Exact independent audit: next predicted box has u1=0 admissible."""
    nxt=m.predict(box,t0,u)
    a=m.backup_audit(nxt,t1)
    return a['feasible'] and Q(a['lower'])<=Z<=Q(a['upper'])

def bridge_rollout(scenario,steps=100,estimator='packet_velocity'):
    """Replay Run206 dynamics and assert the shift implication at every tick."""
    old=m.filter_torque
    state={'previous_bridge':False,'checked':0,'refusal_box':None,'refusal_t':None}
    def checked_filter(box,t0):
        if state['previous_bridge']:
            # Even if a new bridge is empty, a four-tick ZERO fallback must
            # still be feasible after the previous bridge action.
            a=m.backup_audit(box,t0)
            assert a['feasible'] and Q(a['lower'])<=Z<=Q(a['upper']), \
                ('causal_shift_failure',scenario,state['checked'])
            state['checked']+=1
        u,cert=bridge_filter(box,t0)
        state['previous_bridge']=u is not None
        if u is None:
            state['refusal_box']=box
            state['refusal_t']=t0
        return u,cert
    try:
        m.filter_torque=checked_filter
        r=m.rollout(scenario,steps,estimator)
    finally:
        m.filter_torque=old
    refusal=r['first_refusal']
    zero_fallback=None
    if refusal is not None:
        a=m.backup_audit(state['refusal_box'],state['refusal_t'])
        zero_fallback=(a['feasible'] and Q(a['lower'])<=Z<=Q(a['upper']))
    return {'scenario':scenario,'estimator':estimator,'accepted_ticks':r['accepted_ticks'],
            'first_refusal_tick':None if refusal is None else refusal['tick'],
            'refusal_reason':None if refusal is None else refusal['reason'],
            'next_step_zero_backup_verified':state['checked'],
            'zero_four_tick_fallback_at_bridge_refusal':zero_fallback,
            'filtered_torque_ticks':r['filtered_torque_ticks'],
            'packet_refinements':r['packet_refinements']}

def run():
    cases=[]
    for scenario in ('positive_high','alternating_high','switch_positive'):
        baseline=m.rollout(scenario,100,'packet_velocity')
        bridge=bridge_rollout(scenario,100)
        cases.append({'scenario':scenario,'four_tick_accepted':baseline['accepted_ticks'],
                      **bridge})
    box=m.initial_box()
    init=bridge_audit(box,m.TMAX)
    shift=[]
    if init['feasible']:
        for u in (Q(init['lower']),Z,Q(init['upper'])):
            if not Q(init['lower'])<=u<=Q(init['upper']):continue
            for t1 in (m.TMIN,Q(10),m.TMAX):
                shift.append({'u':str(u),'next_thrust':str(t1),
                              'four_tick_zero_admissible':verify_shift(box,m.TMAX,u,t1)})
    return {'run':'207','evidence':'EXACT_RATIONAL_ONE_STEP_SHIFT_BRIDGE',
            'initial_bridge':init,'independent_shift_checks':shift,
            'rows':cases,'gate_A':'blocked',
            'caveats':['The bridge uses a conservative full box reset and zero future torque; no observation-contingent next-step torque optimization',
                       'All legal next measurements shrink the predicted box, so the shift lemma is universal for the next step only',
                       'Bridge feasibility need not persist after a second step; no terminal set or recursive MPC feasibility',
                       'Reachable trajectories are selected examples, not an all-histories safety guarantee']}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output')
    a=ap.parse_args()
    s=json.dumps(run(),ensure_ascii=False,indent=2)+'\n'
    if a.output:
        from pathlib import Path
        p=Path(a.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
    else:print(s,end='')

if __name__=='__main__':main()
