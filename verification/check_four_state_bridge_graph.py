#!/usr/bin/env python3
"""Run228: sound rational interval-cell graph audit; no four-state RCI claimed.

Frozen Run224 full-state Euler dynamics, independent control-dependent
Run208/210 residual. A cell action is certified only when its entire
outward successor box is covered by the union of candidate cells.
An uncertified action is INCONCLUSIVE, not an impossibility result.
"""
from __future__ import annotations
import argparse
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path

H=Q(1,50); TMIN=Q(981,200); TMAX=Q(2943,200)
R0=Q(47,25); RT=Q(243,16000); INERTIA=Q(1,50)
PMAX=Q(5); VMAX=Q(3); PHIMAX=Q(9,20); OMAX=Q(2); TAUMAX=Q(2,25)
LIMITS=(PMAX,VMAX,PHIMAX,OMAX)


def sine_bounds(phi):
    """s7 <= sin(phi) <= s5 for phi>=0, odd-reflected for phi<0."""
    if abs(phi)>PHIMAX: raise ValueError('sine argument outside domain')
    r=abs(phi)
    s5=r-r**3/6+r**5/120
    s7=s5-r**7/5040
    return (s7,s5) if phi>=0 else (-s5,-s7)


def make_box(*bounds):
    b=tuple((Q(lo),Q(hi)) for lo,hi in bounds)
    if len(b)!=4 or any(lo>hi for lo,hi in b): raise ValueError('invalid box')
    return b


def within_domain(box):
    return all(-lim<=lo<=hi<=lim for (lo,hi),lim in zip(box,LIMITS))


def outer_successor(box,thrust,torque):
    """Guaranteed enclosure for ALL x in box and ALL |r|<=R(thrust)."""
    if not within_domain(box): raise ValueError('cell outside physical domain')
    if not (TMIN<=thrust<=TMAX and -TAUMAX<=torque<=TAUMAX):
        raise ValueError('input outside bounds')
    (pl,pu),(vl,vu),(fl,fu),(wl,wu)=box
    sl=sine_bounds(fl)[0]; su=sine_bounds(fu)[1]
    rad=R0+RT*thrust
    return make_box((pl+H*vl,pu+H*vu),
                    (vl+H*(-thrust*su-rad),vu+H*(-thrust*sl+rad)),
                    (fl+H*wl,fu+H*wu),
                    (wl+H*torque/INERTIA,wu+H*torque/INERTIA))


def contains(box,point):
    return all(lo<=x<=hi for (lo,hi),x in zip(box,point))


def union_covers(target,boxes):
    """Exact closed-box union inclusion, including boundaries and holes.

    Split each axis at every intersecting cell endpoint. Box membership is
    constant on each open stratum, so testing all endpoints and midpoints
    of the resulting 1-D strata gives an exact decision in any dimension.
    Returns (covered, uncovered_grid_point). No floating point arithmetic.
    """
    if not boxes: return False,tuple((lo+hi)/2 for lo,hi in target)
    reps=[]
    for axis,(lo,hi) in enumerate(target):
        cuts={lo,hi}
        for b in boxes:
            for end in b[axis]:
                if lo<end<hi: cuts.add(end)
        cuts=sorted(cuts)
        points=set(cuts)
        points.update((a+b)/2 for a,b in zip(cuts,cuts[1:]))
        reps.append(sorted(points))
    for point in itertools.product(*reps):
        if not any(contains(b,point) for b in boxes):
            return False,point
    return True,None


def candidate_cells(bridge_velocity=Q(3,100)):
    b=bridge_velocity
    if not Q(0)<b<=VMAX: raise ValueError('invalid bridge width')
    return {
        'bridge':make_box((-1,1),(-b,b),(-Q(1,50),Q(1,50)),(-Q(1,10),Q(1,10))),
        'positive':make_box((-4,4),(0,3),(Q(3,20),Q(1,4)),(-1,1)),
        'negative':make_box((-4,4),(-3,0),(-Q(1,4),-Q(3,20)),(-1,1)),
    }


def center_obstruction(bridge_velocity):
    """Exact all-control witness at x=(0,0,0,0) for b<h*R(TMIN).

    For every T and torque, phi+=0 and choosing r=+R(T) gives
    v+=h*R(T)>=h*R(TMIN). Other modes exclude phi=0.
    """
    min_speed=H*(R0+RT*TMIN)
    return {'certified_noninvariant':bridge_velocity<min_speed,
            'bridge_velocity_limit':str(bridge_velocity),
            'minimum_adversarial_next_speed':str(min_speed),
            'strict_gap_if_positive':str(min_speed-bridge_velocity),
            'state':['0']*4,'adversary':'r=+R(T), all T and tau',
            'reason':'phi_next=0 for every input; only bridge mode admits phi=0'}


def scan(cells):
    for box in cells.values():
        assert within_domain(box)
    menu=[(t,tau) for t in (TMIN,(TMIN+TMAX)/2,TMAX)
          for tau in (-TAUMAX,Q(0),TAUMAX)]
    out={}
    for name,box in cells.items():
        valid=[]; first_failure=None
        for t,tau in menu:
            successor=outer_successor(box,t,tau)
            covered,point=union_covers(successor,list(cells.values()))
            if covered: valid.append([str(t),str(tau)])
            elif first_failure is None:
                first_failure={'input':[str(t),str(tau)],
                               'uncovered_outer_point':[str(x) for x in point]}
        out[name]={'menu_actions_tested':len(menu),
                   'certified_actions':valid,
                   'first_uncovered_outer_point_not_a_reachable_witness':first_failure}
    return out


def config_contract(root):
    c=json.loads((Path(root)/'configs/planar_baseline.json').read_text(),parse_float=Q)
    assert c['plant']['truth_semantics']=='defined_discrete_euler'
    assert Q(c['plant']['dt_s'])==H
    assert Q(c['plant']['inertia_kg_m2'])==INERTIA
    assert [Q(x) for x in c['domain']['input_lower']]==[TMIN,-TAUMAX]
    assert [Q(x) for x in c['domain']['input_upper']]==[TMAX,TAUMAX]
    assert [Q(c['domain']['state_upper'][i]) for i in (0,2,4,5)]==list(LIMITS)
    return True


def verify(root=None):
    if root is not None: config_contract(root)
    narrow=Q(3,100); wide=Q(1,20)
    assert center_obstruction(narrow)['certified_noninvariant']
    assert not center_obstruction(wide)['certified_noninvariant']
    cases={}
    for label,b in [('narrow',narrow),('expanded',wide)]:
        cells=candidate_cells(b)
        cases[label]={'bridge_velocity_limit':str(b),
                      'center_obstruction':center_obstruction(b),
                      'cell_policy_scan':scan(cells)}
    return {'run':'228','model':'Run224 frozen full-state Euler, Run208/210 independent control-dependent residual',
            'base_main':'2d25c3736bc987edf2b4b3d53e0dc155e9263810',
            'method':'Fraction interval outer successors and exact finite union coverage',
            'input_menu':'3 thrust x 3 torque; fixed input per cell; no continuous-input completeness',
            'cases':cases,'gate_A':'blocked',
            'limitations':['A missing menu action is INCONCLUSIVE, not a proof no state feedback can work.',
                           'Uncovered outer-box points may be unreachable; only the center obstruction is an all-control physical witness.',
                           'No four-state RCI, output-feedback SMF MPC, recursive feasibility, stability, six-state safety or 20ms guarantee.']}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path);ap.add_argument('--output',type=Path)
    args=ap.parse_args();s=json.dumps(verify(args.root),ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(s)
    else:print(s,end='')

if __name__=='__main__':main()
