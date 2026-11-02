#!/usr/bin/env python3
"""Run264: sound 60->75 common zero-torque backup for Run260 frozen histories.

A finite, measurement-independent robust bridge, NOT a terminal RCI or SMF-MPC.
The 60 outer boxes are imported from Run260's exact archived certificate when
--root is provided, and pinned below for standalone deterministic reproduction.
"""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

H = J = F(1, 50)
T = F(981, 100)
R = F(3246383, 1600000)
GRID = 10**10
LIMIT = {'p': F(5), 'v': F(3), 'phi': F(9, 20), 'omega': F(2)}
START = {
    'SMM': {
        'p': ('-665412229/1250000000', '1330275107/2500000000'),
        'v': ('-7841778593/5000000000', '15679162373/10000000000'),
        'phi': ('-1/125', '1/125'),
        'omega': ('-1/100', '1/100'),
    },
    'MMS': {
        'p': ('-2474339699/10000000000', '2473900217/10000000000'),
        'v': ('-2187058727/2000000000', '5466914349/5000000000'),
        'phi': ('-1/125', '1/125'),
        'omega': ('-1/100', '1/100'),
    },
}

def down(x):
    return F((x.numerator * GRID)//x.denominator, GRID)

def outward(a, b):
    return down(a), -down(-b)

def sin_bounds(x):
    assert abs(x) <= LIMIT['phi']
    if x < 0:
        lo, hi = sin_bounds(-x)
        return -hi, -lo
    lo = x - x**3/F(6)
    return lo, lo + x**5/F(120)

def step(s):
    p,v,phi,omega = (s[k] for k in ('p','v','phi','omega'))
    sin_lo = sin_bounds(phi[0])[0]
    sin_hi = sin_bounds(phi[1])[1]
    return {
        'p': outward(p[0]+H*v[0], p[1]+H*v[1]),
        'v': outward(v[0]-H*(T*sin_hi+R), v[1]+H*(R-T*sin_lo)),
        'phi': outward(phi[0]+H*omega[0], phi[1]+H*omega[1]),
        'omega': omega,  # tau=0; h/J=1
    }

def safe(s):
    return all(-LIMIT[k] <= a <= b <= LIMIT[k] for k,(a,b) in s.items())

def serial(s):
    return {k:[str(a),str(b)] for k,(a,b) in s.items()}

def certificate(root=None):
    if root is not None:
        root = Path(root)
        prior = json.loads((root/'results/run260_conditional_shared_bridge_20261102/checks.json').read_text())
        assert prior['certified_last_tick']==60
        assert prior['shared_control_ticks_45_to_59']=={'actual_thrust_N':str(T),'torque_Nm':'0'}
        for mode in START:
            assert prior['branches'][mode]['tick60_outer'] == {k:list(v) for k,v in START[mode].items()}
        cfg=json.loads((root/'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics']=='defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s']))==H
        assert F(str(cfg['plant']['inertia_kg_m2']))==J
        assert F(str(cfg['plant']['gravity_m_s2']))==T
        assert F(str(cfg['domain']['input_upper'][1]))==F(2,25)
        assert cfg['sensing']['position_period_ticks']==5
        assert cfg['sensing']['max_consecutive_missed_packets']==2
    branches={}
    for mode in ('SMM','MMS'):
        s={k:tuple(F(v) for v in bounds) for k,bounds in START[mode].items()}
        rows=[s]
        for _ in range(15):
            rows.append(step(rows[-1]))
        assert len(rows)==16 and all(safe(q) for q in rows)
        margins={k:min(LIMIT[k]-max(abs(q[k][0]),abs(q[k][1])) for q in rows) for k in LIMIT}
        assert all(x>0 for x in margins.values())
        branches[mode]={
            'tick60_outer':serial(rows[0]),
            'tick75_outer':serial(rows[-1]),
            'min_hard_constraint_margin_60_to_75':{k:str(margins[k]) for k in ('p','v','phi','omega')},
            'all_16_boxes_safe':True,
        }
    return {
        'run':264,
        'evidence':'EXACT_RATIONAL_FINITE_SHARED_BACKUP_FROM_ALL_NONEMPTY_RUN260_TICK60_POSTERIORS',
        'scope':'only Run260 fixed zero-reading histories SMM/MMS through tick45, frozen 4-state Euler T=9.81, and all legal future bounded-noise readings and packet outcomes; not arbitrary histories',
        'start_tick':60,
        'last_certified_tick':75,
        'total_fixed_history_bridge_ticks_45_to_75':30,
        'backup_actual_thrust_N':str(T),
        'backup_torque_Nm':'0',
        'future_measurement_handling':'ignored; any nonempty measurement-conditioned posterior is a subset of the unconditioned outer propagation',
        'branches':branches,
        'not_certified':['terminal information-state RCI','feedback terminal policy','recursive feasibility','closed-loop stability','six-state quadrotor safety','20ms WCET'],
        'gate_A':'blocked',
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--root',type=Path)
    p.add_argument('--output',type=Path)
    a=p.parse_args()
    result=json.dumps(certificate(a.root),sort_keys=True,indent=2,ensure_ascii=False)+'\n'
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(result)
    else:
        print(result,end='')

if __name__=='__main__': main()
