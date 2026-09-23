#!/usr/bin/env python3
"""Audit the exact/McCormick/independent-box support gap for q=dT*phi.

The floating LP is only used to verify the analytic convex-hull statement.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import numpy as np
import scipy
from scipy.optimize import linprog

DT=4.905
PHI=0.45
G=9.81

def exact_support(c, a=DT, b=PHI):
    # A linear functional of (d,p,dp) is bilinear/affine on a rectangle;
    # its maximum is attained at a corner.
    return max(c[0]*d+c[1]*p+c[2]*d*p for d in (-a,a) for p in (-b,b))

def independent_support(c, a=DT, b=PHI):
    return abs(c[0])*a+abs(c[1])*b+abs(c[2])*a*b

def mccormick_support(c, a=DT, b=PHI):
    lx,ux=-a,a; ly,uy=-b,b
    A=np.array([[ly,lx,-1],[uy,ux,-1],[-uy,-lx,1],[-ly,-ux,1]],float)
    B=np.array([lx*ly,ux*uy,-lx*uy,-ux*ly],float)
    r=linprog(-np.asarray(c,float),A_ub=A,b_ub=B,
              bounds=[(lx,ux),(ly,uy),(None,None)],method='highs')
    if not r.success:
        raise RuntimeError(r.message)
    return -float(r.fun)

def analytic_gap(c, a=DT, b=PHI):
    vals=[abs(c[0])*a,abs(c[1])*b,abs(c[2])*a*b]
    if any(v==0 for v in vals):
        return 0.0
    # desired independent signs are compatible with q=d*p iff their product is positive
    return 0.0 if c[0]*c[1]*c[2]>0 else 2.0*min(vals)

def run(seed=20260924,cases=10000):
    rng=np.random.default_rng(seed)
    max_mcc_err=0.0; max_gap_formula_err=0.0; positive=0; gaps=[]
    for _ in range(cases):
        c=rng.normal(size=3)
        ex=exact_support(c); mc=mccormick_support(c); ind=independent_support(c)
        gap=ind-ex
        max_mcc_err=max(max_mcc_err,abs(mc-ex))
        max_gap_formula_err=max(max_gap_formula_err,abs(gap-analytic_gap(c)))
        positive += gap>1e-10
        gaps.append(gap)
    physical={}
    # y=[dT, -g*phi-dT*phi]; support in direction (rz,rx)
    for rz,rx in [(1,1),(-1,1),(1,-1),(-1,-1),(0,1)]:
        c=np.array([rz,-G*rx,-rx],float)
        ex=exact_support(c); ind=independent_support(c)
        physical[f'{rz},{rx}']={'exact':ex,'independent':ind,'gap':ind-ex}
    return {
      'scope':'single bilinear graph q=dT*phi over symmetric thrust-attitude box',
      'bounds':{'abs_deltaT':DT,'abs_phi':PHI,'g':G},
      'seed':seed,'random_directions':cases,
      'max_abs_mccormick_vs_exact_support_error':max_mcc_err,
      'max_abs_analytic_gap_formula_error':max_gap_formula_err,
      'directions_with_strict_independent_box_gap':positive,
      'mean_independent_box_support_gap':float(np.mean(gaps)),
      'max_independent_box_support_gap':float(np.max(gaps)),
      'physical_output_direction_examples':physical,
      'versions':{'python':sys.version.split()[0],'numpy':np.__version__,'scipy':scipy.__version__},
      'interpretation':[
        'For one bilinear term on a rectangle, the McCormick polytope is the convex hull for linear support queries.',
        'A constrained zonotope can represent the same bounded polytope, but cannot improve its linear support merely by changing representation.',
        'The independent q-box is strictly conservative only in sign-incompatible joint directions; pure horizontal vx direction has zero gap.',
        'Any further advantage must come from a tighter nonrectangular SMF domain, multiple shared products across time, or nonlinear/nonconvex objectives—not from CZ naming alone.'
      ]}

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--seed',type=int,default=20260924); ap.add_argument('--cases',type=int,default=10000)
    args=ap.parse_args(); out=run(args.seed,args.cases)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
