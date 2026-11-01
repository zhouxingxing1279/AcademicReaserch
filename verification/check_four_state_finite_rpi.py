#!/usr/bin/env python3
"""Run235: finite-generator exact-rational RPI for frozen full-state four-state plant.

This certifies neither output-feedback, dropout SMF, MPC, nor six-state safety.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

Z, O = F(0), F(1)
N = 800
H, T = F(1, 50), F(981, 100)
K = tuple(map(F, ('-0.123', '-0.494', '2.341', '0.933')))
A = ((O,H,Z,Z),(Z,O,-H*T,Z),(Z,Z,O,H),
     (F(123,1000),F(247,500),-F(2341,1000),F(67,1000)))
B = (Z,H,Z,Z)
LIMITS = (F(5),F(3),F(9,20),F(2))
TAU_MAX = F(2,25)
R = F(47,25)+F(243,16000)*T
D = R+T*LIMITS[2]**3/6


def dot(x,y):
    return sum((a*b for a,b in zip(x,y)), Z)


def mv(v):
    return tuple(dot(row,v) for row in A)


def ceil_decimal(q, places=8):
    scale=10**places
    n= -((-q.numerator*scale)//q.denominator)
    return f'{n//scale}.{n%scale:0{places}d}'


def certificate(n=N):
    if n < 1:
        raise ValueError('n must be positive')
    v=B
    cols=[tuple(O if i==j else Z for i in range(4)) for j in range(4)]
    p=[Z]*4
    q=[Z]*4
    p_torque=Z
    q_torque=Z
    for _ in range(n):
        p=[p[i]+abs(v[i]) for i in range(4)]
        p_torque+=abs(dot(K,v))
        for i in range(4):
            q[i]+=sum((abs(cols[j][i]) for j in range(4)),Z)
        q_torque+=sum((abs(dot(K,col)) for col in cols),Z)
        v=mv(v)
        cols=[mv(col) for col in cols]
    power=tuple(tuple(cols[j][i] for j in range(4)) for i in range(4))
    rho=max(sum(map(abs,row),Z) for row in power)
    if rho >= O:
        raise AssertionError('block contraction absent')
    eps=D*max(map(abs,v))
    # Explicit rational containment obligations (not floating-point sampling).
    assert all(D*abs(z) <= eps for z in v)  # A^n B[-D,D] subset W
    assert all(eps*sum(map(abs,row),Z) <= rho*eps for row in power)  # A^n W subset rho W
    scale=eps/(O-rho)
    states=tuple(D*p[i]+scale*q[i] for i in range(4))
    torque=D*p_torque+scale*q_torque
    if not all(x<lim for x,lim in zip(states,LIMITS)):
        raise AssertionError('finite RPI state constraint failed')
    if not torque<TAU_MAX:
        raise AssertionError('finite RPI torque constraint failed')
    return {
        'run':235,'certificate':'EXACT_RATIONAL_FINITE_GENERATOR_NONLINEAR_RCI',
        'model':'defined_discrete_euler_four_state_fixed_thrust_full_state_feedback',
        'block_length':n,'generator_count':5*n,
        'rho_upper':ceil_decimal(rho,9),
        'tail_box_halfwidth_upper':ceil_decimal(eps,10),
        'tail_scale_upper':ceil_decimal(scale,10),
        'state_abs_upper':list(map(ceil_decimal,states)),
        'torque_abs_upper':ceil_decimal(torque),
        'state_limits':[str(x) for x in LIMITS],
        'torque_limit':str(TAU_MAX),
        'thrust_N':str(T), 'gain':[str(x) for x in K],
        'disturbance_halfwidth':str(D),
        'finite_set':'F=P_n (+) Q; P_n=sum_{j=0}^{n-1} A^j B[-D,D]; W=eps[-1,1]^4; Q=(1-rho)^-1 sum_{j=0}^{n-1} A^j W',
        'proof':'A^n B[-D,D] subset W; A^n W subset rho W; A Q (+) W subset Q; A F (+) B[-D,D] subset F; F subset state and torque hard bounds; nonlinear d=r+T(phi-sin(phi)) subset [-D,D].',
        'membership':'finite 4-by-4000 generator matrix: exists xi in [-1,1]^4000 with x=G xi (LP feasibility); not benchmarked online',
        'gate_A':'blocked_for_output_feedback_SMF_MPC',
        'limitations':['No intermittent-measurement shared-information feedback','No MPC recursive feasibility or stability proof','No six-state coupled proof or 20ms bound']
    }


def finite_generators(n=N):
    """Return exactly 5*n rational generators (4 coordinates each) of F.

    Feasible membership means G xi=x with -1<=xi<=1; no online timing claim.
    """
    v=B
    cols=[tuple(O if i==j else Z for i in range(4)) for j in range(4)]
    for _ in range(n):
        v=mv(v)
        cols=[mv(col) for col in cols]
    power=tuple(tuple(cols[j][i] for j in range(4)) for i in range(4))
    rho=max(sum(map(abs,row),Z) for row in power)
    if rho>=O:
        raise AssertionError('block contraction absent')
    scale=D*max(map(abs,v))/(O-rho)
    v=B
    cols=[tuple(O if i==j else Z for i in range(4)) for j in range(4)]
    for _ in range(n):
        yield tuple(D*z for z in v)
        for col in cols:
            yield tuple(scale*z for z in col)
        v=mv(v)
        cols=[mv(col) for col in cols]


def verify(root=None):
    if root is not None:
        c=json.loads((Path(root)/'configs/planar_baseline.json').read_text())
        assert c['plant']['truth_semantics']=='defined_discrete_euler'
        assert F(str(c['plant']['dt_s']))==H
        assert F(str(c['plant']['inertia_kg_m2']))==F(1,50)
        assert tuple(F(str(x)) for x in c['domain']['input_lower'])==(F(4905,1000),-TAU_MAX)
        assert tuple(F(str(x)) for x in c['domain']['input_upper'])==(F(14715,1000),TAU_MAX)
        assert tuple(F(str(c['domain']['state_upper'][i])) for i in (0,2,4,5))==LIMITS
    return certificate()


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',type=Path)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    s=json.dumps(verify(args.root),ensure_ascii=False,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(s)
    else: print(s,end='')


if __name__=='__main__': main()
