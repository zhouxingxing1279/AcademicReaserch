#!/usr/bin/env python3
"""Run226: exact rational three-step robust predecessor witnesses.

Frozen Run224/225 full-state Euler plant, independent Run208/210 residual.
The inclusion is a sufficient interval certificate for fixed open-loop inputs;
the exclusion holds for ALL causal state-feedback controls, because the
adversarial disturbance can defeat even the best allowable thrust/torque.
No invariant terminal set or output-feedback guarantee is claimed.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as Q
from pathlib import Path

from check_four_state_one_step_predecessor import (
    H, TMAX, R0, RT, VMAX, PMAX, PHIMAX, OMAX,
    TAUMAX, INERTIA, sine_bounds, config_contract,
)

PHI=Q(3,20)
BAD_OMEGA=Q(-2,5)


def interval_rollout(sign, omega, torques):
    """Outward rational enclosures for every disturbance realization.

    Position and velocity are interval enclosures, not a joint exact reachable
    set. Angular state is deterministic under the stated zero-noise contract.
    """
    assert sign in (-1,1)
    p=(Q(0),Q(0)); v=(sign*VMAX,sign*VMAX)
    phi=sign*PHI; w=sign*omega
    records=[]
    for tau in torques:
        assert -TAUMAX<=tau<=TAUMAX
        slo,shi=sine_bounds(phi)
        rad=R0+RT*TMAX
        dv=(H*(-TMAX*shi-rad),H*(-TMAX*slo+rad))
        new_p=(p[0]+H*v[0],p[1]+H*v[1])
        new_v=(v[0]+dv[0],v[1]+dv[1])
        phi,w=phi+H*w,w+H*tau/INERTIA
        p,v=new_p,new_v
        assert -PMAX<=p[0]<=p[1]<=PMAX
        assert -VMAX<=v[0]<=v[1]<=VMAX
        assert abs(phi)<=PHIMAX and abs(w)<=OMAX
        records.append({'p':[str(z) for z in p],
                        'v':[str(z) for z in v],
                        'phi':str(phi),'omega':str(w)})
    return records


def positive_three_step(sign):
    # Fixed open-loop control is sufficient for the stronger
    # forall r0 forall r1 forall r2 requirement.
    return {'state':[str(z) for z in (Q(0),sign*VMAX,sign*PHI,Q(0))],
            'inputs':[[str(TMAX),'0']]*3,
            'enclosures':interval_rollout(sign,Q(0),[Q(0)]*3),
            'in_Pre3_X_sufficient':True}


def two_step_but_not_three(sign):
    """x=(0,sign*3,sign*.15,-sign*.4) is in Pre²(X) but not Pre³(X)."""
    assert sign in (-1,1)
    # Two-step constructive policy, even stronger than causal feedback.
    torques=[sign*TAUMAX,Q(0)]
    boxes=interval_rollout(sign,BAD_OMEGA,torques)
    return {'state':[str(z) for z in (Q(0),sign*VMAX,sign*PHI,sign*BAD_OMEGA)],
            'two_step_inputs':[[str(TMAX),str(t)] for t in torques],
            'two_step_enclosures':boxes,
            'in_Pre2_X_sufficient':True,
            'excluded_from_Pre3_X':True}


def third_step_gap():
    """Exact strict lower bound on v3-3 under a causal adversary.

    For positive boundary x=(0,3,.15,-.4), phi0=.15, phi1=.142.
    phi2=.134 +/- .0016, hence phi2 <= .1356 for any tau0.
    All three phi values are positive with sin(phi)>RT, so each
    adversarial increment R0 + T*(RT-sin(phi)) is minimized at TMAX.
    With r_i=+R(T_i) and the sine upper bound, v3-3 >= gap > 0.
    Negative boundary follows by exact odd symmetry.
    """
    phi0=PHI
    phi1=phi0+H*BAD_OMEGA
    phi2_min=phi0+2*H*BAD_OMEGA-H*H*TAUMAX/INERTIA
    phi2_max=phi0+2*H*BAD_OMEGA+H*H*TAUMAX/INERTIA
    assert Q(0)<phi2_min<=phi2_max<=PHIMAX
    assert all(sine_bounds(phi)[0]>RT for phi in (phi0,phi1,phi2_min))
    gap=H*(3*(R0+RT*TMAX)-TMAX*sum(sine_bounds(phi)[1] for phi in (phi0,phi1,phi2_max)))
    assert gap>0
    return {'phi0':str(phi0),'phi1':str(phi1),
            'phi2_min':str(phi2_min),'phi2_max':str(phi2_max),
            'lower_bound_on_adversarial_v3_minus_3':str(gap),
            'positive':True}


def verify(root=None):
    if root is not None: config_contract(root)
    good=[positive_three_step(s) for s in (1,-1)]
    bad=[two_step_but_not_three(s) for s in (1,-1)]
    good=[{'state':x['state'], 'third_step_velocity':x['enclosures'][-1]['v'],
           'in_Pre3_X_sufficient':True} for x in good]
    bad=[{'state':x['state'], 'second_step_velocity':x['two_step_enclosures'][-1]['v'],
          'in_Pre2_X_sufficient':True,'excluded_from_Pre3_X':True} for x in bad]
    return {
        'run':'226',
        'base':'Run224/225 frozen four-state Euler; Run208/210 independently selectable lateral residual',
        'quantifiers':'Pre3(X): exists u0 forall r0 exists u1(x1) forall r1 exists u2(x2) forall r2; intermediate states in X',
        'certificate':'EXACT_RATIONAL_TAYLOR_THREE_STEP_INCLUSION_AND_STRICT_EXCLUSION',
        'three_step_inclusions':good,
        'two_step_but_not_three_step':bad,
        'three_step_adversarial_gap':third_step_gap(),
        'adversary':'r_i=sign*R(T_i), i=0,1,2; any causal thrust/torque',
        'gate_A':'blocked',
        'limitations':[
            'Finite-horizon full-state predecessor witnesses only; not a robust controlled invariant terminal set.',
            'Strict exclusion assumes the independently adversarial Run208/210 residual envelope.',
            'No four-state SMF output-feedback MPC, recursive feasibility, stability, or six-state safety proof.',
            'No 20ms worst-case execution-time certification.'
        ]
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--root',type=Path)
    p.add_argument('--output',type=Path)
    a=p.parse_args()
    result=json.dumps(verify(a.root),indent=2,sort_keys=True,ensure_ascii=False)+'\n'
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(result)
    else:
        print(result,end='')

if __name__=='__main__':
    main()
