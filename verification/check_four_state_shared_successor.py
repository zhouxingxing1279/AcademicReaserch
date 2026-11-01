#!/usr/bin/env python3
"""Run237: exact support separation for a shared output-fiber terminal torque.

For the two Run236 indistinguishable states, no common torque can keep
all legal one-step successors in the Run235 finite RPI F. This is a
local output-feedback obstruction, NOT a proof against every SMF tube.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as Q
from pathlib import Path
import check_four_state_finite_rpi as rpi

N = 800
ELL = (Q(13939,100000), Q(55667,100000), -Q(252917,100000), -Q(1))
THRESHOLD = Q(181,10000)


def certificate(root=None):
    if root is not None:
        rpi.verify(root)
        cfg = json.loads((Path(root)/'configs/planar_baseline.json').read_text())
        assert cfg['sensing']['always_observed_indices'] == [4,5]
        assert cfg['sensing']['position_indices'] == [0,1]
    assert rpi.N == N and rpi.H == Q(1,50) and rpi.T == Q(981,100)
    assert rpi.B == (Q(0),rpi.H,Q(0),Q(0))
    assert rpi.A[3][1] == Q(247,500)
    assert rpi.K[1] == -Q(247,500)
    v = rpi.B
    columns = [tuple(Q(int(i==j)) for i in range(4)) for j in range(4)]
    p_support = Q(0)
    q_support = Q(0)
    for _ in range(N):
        p_support += abs(rpi.dot(ELL,v))
        q_support += sum((abs(rpi.dot(ELL,c)) for c in columns),Q(0))
        v = rpi.mv(v)
        columns = [rpi.mv(c) for c in columns]
    power = tuple(tuple(columns[j][i] for j in range(4)) for i in range(4))
    rho = max(sum(map(abs,row),Q(0)) for row in power)
    assert rho < 1
    eps = rpi.D*max(map(abs,v))
    scale = eps/(1-rho)
    support = rpi.D*p_support + scale*q_support
    # Physical Euler successor for x+=(0,hD,0,0), r=+R, shared tau=u:
    # (h^2 D, h(D+R), 0, h/J*u), where h/J=1.
    target = (rpi.H*rpi.H*rpi.D, rpi.H*(rpi.D+rpi.R),Q(0),Q(0))
    value = rpi.dot(ELL,target)
    gap = value-support
    assert gap > THRESHOLD
    # F is centrally symmetric: positive fiber needs u>=gap,
    # negative fiber with r=-R needs u<=-gap. Contradiction.
    return {
        'run':237,
        'evidence':'EXACT_RATIONAL_SUPPORT_SEPARATION',
        'scope':'Run235 fixed-thrust frozen four-state Euler, initial Run236 two-state observation fiber',
        'normal':[str(a) for a in ELL],
        'states':['(0,+hD,0,0)','(0,-hD,0,0)'],
        'disturbances':['+R','-R'],
        'thrust':str(rpi.T),'h':str(rpi.H),'D':str(rpi.D),'R':str(rpi.R),
        'finite_generators':5*N,
        'support_upper_rounded':rpi.ceil_decimal(support,9),
        'positive_successor_projection_rounded':rpi.ceil_decimal(value,9),
        'strict_gap_lower':str(THRESHOLD),
        'positive_fiber_requires':'tau > 0.0181 Nm',
        'negative_fiber_requires':'tau < -0.0181 Nm',
        'shared_torque_feasible':False,
        'limitations':['Only this two-state posterior fiber, not every SMF posterior',
                       'Does not refute the full-state F invariance proof',
                       'Does not establish four-state output-feedback MPC feasibility or impossibility'],
        'gate_A':'blocked_for_output_feedback_SMF_MPC'
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',type=Path)
    ap.add_argument('--output',type=Path)
    a=ap.parse_args()
    data=json.dumps(certificate(a.root),ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(data)
    else: print(data,end='')

if __name__=='__main__': main()
