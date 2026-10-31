#!/usr/bin/env python3
"""Run225: exact rational two-step full-state robust predecessor witnesses.

Uses frozen Run224 Euler plant and independently adversarial Run208/210
lateral residual. Certificates do NOT establish an invariant terminal set.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as Q
from pathlib import Path

from check_four_state_one_step_predecessor import (
    H, TMAX, R0, RT, VMAX, PMAX, PHIMAX, OMAX, TAUMAX, INERTIA,
    sine_bounds, certified_predecessor, next_bounds, config_contract,
)

PHI = Q(3,20)
PHI_NEXT_BAD = PHI - H*OMAX  # 11/100, regardless of first torque


def signed_box(sign):
    """Robust two-step open-loop box from x=(0,sign*3,sign*.15,0)."""
    assert sign in (-1,1)
    x=(Q(0),sign*VMAX,sign*PHI,Q(0))
    assert certified_predecessor(x,TMAX,Q(0))
    slo,shi=sine_bounds(sign*PHI)
    rad=R0+RT*TMAX
    dlo=H*(-TMAX*shi-rad)
    dhi=H*(-TMAX*slo+rad)
    v1=(x[1]+dlo,x[1]+dhi)
    v2=(v1[0]+dlo,v1[1]+dhi)
    p1=(H*x[1],H*x[1])
    p2=(p1[0]+H*v1[0],p1[1]+H*v1[1])
    for lo,hi,limit in [(v1[0],v1[1],VMAX),(v2[0],v2[1],VMAX),
                         (p1[0],p1[1],PMAX),(p2[0],p2[1],PMAX)]:
        assert -limit <= lo <= hi <= limit
    assert abs(sign*PHI)<=PHIMAX
    return {'state':[str(z) for z in x], 'fixed_inputs':[[str(TMAX),'0']]*2,
            'first_velocity':[str(z) for z in v1],
            'second_velocity':[str(z) for z in v2],
            'second_position':[str(z) for z in p2],
            'in_Pre2_X_sufficient':True}


def bad_boundary_gap():
    """Strict two-step velocity violation under r_i=+R(T_i), ANY causal T_i.

    Starting x=(0,3,3/20,-2), phi_1=11/100 independently of tau_0.
    Since sin(phi_0),sin(phi_1)>RT, each adversarial velocity increment
    is minimized by TMAX. Rational s5 upper bounds give a *lower* bound
    on v_2-3. The same proof is sign symmetric for negative velocity.
    """
    assert PHI_NEXT_BAD == Q(11,100)
    for phi in (PHI,PHI_NEXT_BAD):
        assert sine_bounds(phi)[0] > RT
    gap=H*(2*R0+2*TMAX*RT - TMAX*(sine_bounds(PHI)[1]+sine_bounds(PHI_NEXT_BAD)[1]))
    assert gap > 0
    return gap


def verify(root=None):
    if root is not None: config_contract(root)
    # The 'bad' states are nevertheless in Pre(X): choose a torque that
    # moves omega from its boundary toward the interior at the first step.
    bad=[]
    for sign in (1,-1):
        x=(Q(0),sign*VMAX,sign*PHI,-sign*OMAX)
        tau=sign*TAUMAX
        assert certified_predecessor(x,TMAX,tau)
        assert next_bounds(x,TMAX,tau)['phi']==(sign*PHI_NEXT_BAD,)*2
        bad.append({'state':[str(z) for z in x],
                    'one_step_input':[str(TMAX),str(tau)],
                    'in_Pre_X':True,'excluded_from_Pre2_X':True})
    return {'run':'225',
            'base':'Run224 frozen four-state Euler; Run208/210 lateral residual envelope',
            'quantifiers':'Pre2(X): exists u0 forall r0 exists u1(x1) forall r1, all intermediate states in X',
            'certificate':'EXACT_RATIONAL_TAYLOR_TWO_STEP_INCLUSION_AND_EXCLUSION',
            'two_step_inclusions':[signed_box(1),signed_box(-1)],
            'one_step_but_not_two_step':bad,
            'adversarial_second_step_velocity_violation_lower_bound':str(bad_boundary_gap()),
            'adversary':'r0=sign*R(T0), r1=sign*R(T1), for any causal thrust/torque choices',
            'gate_A':'blocked',
            'limitations':['Only two-step full-state feedback predecessor witnesses, not an RCI terminal kernel.',
                           'Exclusion is robust to arbitrary causal controls but relies on independent adversarial residual envelope.',
                           'Does not establish output-feedback SMF feasibility, recursive feasibility, stability or six-state safety.',
                           'No 20ms worst-case execution-time certification.']}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    content=json.dumps(verify(args.root),indent=2,sort_keys=True,ensure_ascii=False)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(content)
    else:
        print(content,end='')

if __name__=='__main__':main()
