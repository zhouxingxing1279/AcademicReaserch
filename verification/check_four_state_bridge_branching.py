#!/usr/bin/env python3
"""Run229: certified two-step finite DAG of robust four-state interval transitions.

This is a finite-horizon, full-state-feedback enclosure, NOT an invariant
terminal graph or a partial-observation MPC safety certificate.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as Q
from pathlib import Path
import check_four_state_bridge_graph as prior

BASE_MAIN = '20bf13cdfb1de57ffddacae58ecda5b11ded69cb'

def seed_cell():
    return prior.make_box((-Q(1,1000),Q(1,1000)),
                          (-Q(1,200),Q(1,200)),
                          (-Q(1,1000),Q(1,1000)),
                          (-Q(1,100),Q(1,100)))

def split_velocity(box):
    lo,hi=box[1]
    if not lo<0<hi: raise ValueError('velocity interval must straddle zero')
    return (tuple(box[i] if i!=1 else (lo,Q(0)) for i in range(4)),
            tuple(box[i] if i!=1 else (Q(0),hi) for i in range(4)))

def build_graph():
    u=(prior.TMIN,Q(0))
    initial=seed_cell()
    first=prior.outer_successor(initial,*u)
    neg,pos=split_velocity(first)
    nodes={'seed':initial,'velocity_negative':neg,'velocity_positive':pos,
           'next_negative':prior.outer_successor(neg,*u),
           'next_positive':prior.outer_successor(pos,*u)}
    edges=[('seed',['velocity_negative','velocity_positive']),
           ('velocity_negative',['next_negative']),
           ('velocity_positive',['next_positive'])]
    for name,cell in nodes.items():
        assert prior.within_domain(cell),name
    for source,destinations in edges:
        outer=prior.outer_successor(nodes[source],*u)
        assert prior.union_covers(outer,[nodes[n] for n in destinations])[0],source
    assert nodes['next_negative'][0][0]<nodes['next_positive'][0][0]
    assert nodes['next_negative'][0][1]<nodes['next_positive'][0][1]
    return nodes,edges,u

def box_json(box):
    return [[str(lo),str(hi)] for lo,hi in box]

def verify(root=None):
    if root is not None: prior.config_contract(root)
    nodes,edges,u=build_graph()
    first=prior.outer_successor(nodes['seed'],*u)
    missing_negative=prior.union_covers(first,[nodes['velocity_positive']])
    missing_positive=prior.union_covers(first,[nodes['velocity_negative']])
    assert not missing_negative[0] and not missing_positive[0]
    center_min=prior.H*(prior.R0+prior.RT*prior.TMIN)
    assert center_min==Q(6254383,160000000)
    assert first[1][0]<-center_min and first[1][1]>center_min
    return {
        'run':'229','base_main':BASE_MAIN,
        'model':'Run224 full-state Euler with independent Run208/210 bounded residual',
        'method':'Fraction outward interval successors; exact closed-box union inclusion',
        'control':{'thrust_N':str(u[0]),'torque_Nm':str(u[1]),
                   'quantifiers':'one fixed admissible action per source cell, for all states and all residuals'},
        'nodes':{name:box_json(cell) for name,cell in nodes.items()},
        'certified_edges':[{'source':source,'destinations':destinations,
                             'robust_covered':True} for source,destinations in edges],
        'two_step_branching':{'seed_successor_velocity_halfwidth':str(first[1][1]),
                              'center_adversarial_velocity_magnitude':str(center_min),
                              'each_single_sign_destination_insufficient':True,
                              'distinct_second_step_position_intervals':True},
        'gate_A':'blocked',
        'limitations':['Finite two-step acyclic graph only: no terminal RCI, no recursive feasibility.',
                       'All-state feedback and fixed input; no SMF, dropout, MPC optimizer, or six-state coupling.',
                       'Interval hulls are sufficient enclosures, not exact reachable sets.',
                       'No worst-case 20 ms timing guarantee or whole-repository regression.']}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',type=Path)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    data=json.dumps(verify(args.root),ensure_ascii=False,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(data)
    else: print(data,end='')
if __name__=='__main__':main()
