#!/usr/bin/env python3
"""Exact scalar-plant joint-error geometry; no MPC optimization or training."""
import argparse
import hashlib
import json
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path


def dot(a,b):return sum(x*y for x,y in zip(a,b))
def pull(q):return (q[0]/2+q[1]/2,q[1]/2)
def support(g,q):return sum(abs(dot(v,q)) for v in g)


def polygon_vertices(rows):
    vertices=set()
    for (a,b,c),(d,e,f) in combinations(rows,2):
        det=a*e-b*d
        if not det:continue
        p=((c*e-b*f)/det,(a*f-c*d)/det)
        if all(aa*p[0]+bb*p[1]<=cc for aa,bb,cc in rows):vertices.add(p)
    if not vertices:raise ValueError('empty or unsupported polygon')
    return vertices


def template(g,directions):
    rows=[]
    for q in directions:
        b=support(g,q)
        rows.extend([(q[0],q[1],b),(-q[0],-q[1],b)])
    return polygon_vertices(rows)


def run():
    # A=B=C=1, K=-1/2, posterior correction L=1/2.
    # Initial e in [-1,1], d=0, w in [-.1,.1], nu in [-.2,.2].
    g=[(Q(1,2),Q(1,2)),(Q(1,20),Q(1,20)),(-Q(1,10),Q(1,10))]
    sx=(Q(1),Q(1));su=(Q(0),-Q(1,2))
    axes=[(Q(1),Q(0)),(Q(0),Q(1))]
    # Separate geometric counterexample, not the posterior of the scalar fixture.
    gc=[(Q(1),-Q(2)),(Q(1),Q(1))]
    current=template(gc,axes+[sx,su])
    exact_next=support(gc,pull(sx))
    loose_next=max(dot(v,pull(sx)) for v in current)
    dirs=[]
    for q in (sx,su):
        for i in range(7):
            dirs.append(q);q=pull(q)
    protected=template(gc,axes+dirs)
    results=[]
    for index,q in enumerate(dirs):
        val=support(gc,q);out=max(dot(v,q) for v in protected)
        assert val==out
        results.append({'kind':'state' if index<7 else 'input',
                        'step':index%7,'exact':val,'protected':out})
    # Zero innovation: e+w+nu=0. Posterior e+=e+w, d+=0.
    # Every t in [-.2,.2] feasible via e=t, w=0, nu=-t.
    # Eliminate nu=-e-w and enumerate the feasible (e,w) polygon exactly.
    conditioned=polygon_vertices([(Q(1),Q(0),Q(1)),(-Q(1),Q(0),Q(1)),
        (Q(0),Q(1),Q(1,10)),(Q(0),-Q(1),Q(1,10)),
        (Q(1),Q(1),Q(1,5)),(-Q(1),-Q(1),Q(1,5))])
    posterior=[((e+w)/2-(-e-w)/2,(e+w)/2+(-e-w)/2) for e,w in conditioned]
    conditioned_e=max(abs(e) for e,d in posterior)
    conditioned_d=max(abs(d) for e,d in posterior)
    assert support(g,sx)==Q(11,10)
    assert sum(support(g,q) for q in axes)==Q(13,10)
    assert loose_next>exact_next
    # Check all generator-box corners satisfy the protected inequalities
    # via all support inequalities, without claiming a general CZ LP solver.
    for signs in __import__('itertools').product((-1,1),repeat=len(gc)):
        p=tuple(sum(s*v[j] for s,v in zip(signs,gc)) for j in range(2))
        assert all(abs(dot(p,q))<=support(gc,q) for q in axes+dirs)
    return {'status':'exact_joint_error_geometry_only',
            'first_state_joint':support(g,sx),
            'first_state_separated':sum(support(g,q) for q in axes),
            'first_input_radius':support(g,su),
            'next_state_exact':exact_next,'next_state_current_only':loose_next,
            'conditioned_e_radius':conditioned_e,'conditioned_d_radius':conditioned_d,
            'protected_equalities':len(results),'horizon':results,
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists():p.error('output must be new')
    a.output.parent.mkdir(parents=True,exist_ok=True)
    result=json.dumps(run(),default=str,indent=2)+'\n';a.output.write_text(result);print(result)
