#!/usr/bin/env python3
"""Run209: exact finite-time attitude viability obstruction at reachable Run208 tick 96.

A negative certificate for the frozen four-state Euler proxy only. The
attitude channel has no thrust or residual term. Even arbitrary causal
feedback with perfect state observation cannot overcome the torque bound.
"""
from __future__ import annotations
import argparse
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path
import check_reachable_smf_backup_rollout as m
import check_two_stage_causal_backup as prior


def attitude_after(phi, omega, torques):
    """Exact Euler attitude after a supplied torque sequence."""
    for u in torques:
        assert -m.UMAX <= u <= m.UMAX
        phi, omega = phi + m.H * omega, omega + m.H * u / m.J
    return phi


def minimum_attitude(phi, omega, n):
    """Global minimum phi_{k+n} over all admissible n-step torque histories."""
    assert n >= 1
    return phi + n*m.H*omega - (m.H*m.H/m.J)*m.UMAX*n*(n-1)/2


def inspect_reachable_tick96():
    replay=prior.rollout_filter('alternating_high','two_stage',steps=100,capture_tick=96)
    assert replay['accepted_ticks']==95 and replay['capture'] is not None
    box,t0,truth=replay['capture']
    assert all(a<=v<=b for (a,b),v in zip(box,truth))
    assert box[2][0]==box[2][1]==truth[2]
    assert box[3][0]==box[3][1]==truth[3]
    assert all(abs(v)<=lim for v,lim in zip(truth,m.LIMITS))
    phi,omega=truth[2:4]
    exact=[minimum_attitude(phi,omega,n) for n in range(1,6)]
    assert exact[3]<=m.LIMITS[2] and exact[4]>m.LIMITS[2]
    assert attitude_after(phi,omega,[-m.UMAX]*5)==exact[4]
    vertex_values=[attitude_after(phi,omega,u) for u in itertools.product((-m.UMAX,m.UMAX),repeat=5)]
    assert min(vertex_values)==exact[4]
    assert not prior.two_stage_audit(box,t0)['feasible']
    assert 97%15!=0 and 97%5!=0
    for u in (-m.UMAX,m.UMAX):
        predicted=m.predict(box,t0,u)
        assert all(predicted[i][0]==predicted[i][1] for i in (2,3))
        for nphi,nomega in itertools.product((-1,0,1),repeat=2):
            noise=(m.Z,m.Z,nphi*m.SIGMA[2],nomega*m.SIGMA[3])
            updated=m.observe(predicted,tuple(m.mid(b) for b in predicted),False,noise)
            assert updated==predicted
    return {
        'run':'209','evidence':'EXACT_RATIONAL_REACHABLE_FINITE_TIME_VIABILITY_OBSTRUCTION',
        'source':'Run208 alternating_high reachable state before tick 96',
        'accepted_prior_ticks':replay['accepted_ticks'],
        'attitude_phi_exact':str(phi),'rate_omega_exact':str(omega),
        'attitude_phi_approx':float(phi),'rate_omega_approx':float(omega),
        'torque_limit':str(m.UMAX),'attitude_limit':str(m.LIMITS[2]),
        'minimum_attitude_by_n':[{'n':n,'exact':str(q),'approx':float(q)} for n,q in enumerate(exact,1)],
        'five_tick_unavoidable_excess_exact':str(exact[4]-m.LIMITS[2]),
        'five_tick_unavoidable_excess_approx':float(exact[4]-m.LIMITS[2]),
        'vertex_torque_sequences_checked':len(vertex_values),
        'next_attitude_measurement_adds_information':False,
        'run208_two_stage_feasible':False,
        'conclusion':'No bounded causal torque policy can keep phi within the hard bound through five further Euler ticks from this particular reachable state, even with perfect future observations.',
        'gate_A':'blocked',
        'limitations':['One reachable state, not a global impossibility theorem for all initial states or controllers',
                       'Defined-discrete four-state Euler attitude channel, not continuous or six-state quadrotor dynamics',
                       'The prior 95-tick controller is not a recursively safe policy; this is a counterexample to viability from its reached state',
                       'A four-tick backup remains logically compatible with inevitable violation by tick five']}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path)
    args=parser.parse_args();s=json.dumps(inspect_reachable_tick96(),indent=2,ensure_ascii=False)+'\n'
    if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(s)
    else:print(s,end='')
if __name__=='__main__':main()
