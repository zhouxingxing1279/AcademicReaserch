#!/usr/bin/env python3
"""Verify exact decision-conditioned support for thrust decision and SMF attitude interval."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
import numpy as np
import scipy

G=9.81
PHI_GLOBAL=0.45
DT=4.905

def endpoint_support(d, lo, hi, rz, rx):
    """Exact max of rz*d-rx*(g+d)*phi over phi in [lo,hi]."""
    return max(rz*d-rx*(G+d)*lo, rz*d-rx*(G+d)*hi)

def center_radius_support(d, lo, hi, rz, rx):
    c=0.5*(lo+hi); r=0.5*(hi-lo)
    return rz*d-rx*(G+d)*c + abs(rx*(G+d))*r

def global_box_support(d, rz, rx):
    return rz*d + abs(rx*(G+d))*PHI_GLOBAL

def run(seed=20260924, cases=10000):
    rng=np.random.default_rng(seed)
    max_err=0.0; strict=0; gaps=[]; ratios=[]
    for _ in range(cases):
        lo,hi=sorted(rng.uniform(-PHI_GLOBAL,PHI_GLOBAL,2))
        d=rng.uniform(-DT,DT)
        rz,rx=rng.normal(size=2)
        exact=endpoint_support(d,lo,hi,rz,rx)
        formula=center_radius_support(d,lo,hi,rz,rx)
        max_err=max(max_err,abs(exact-formula))
        gap=global_box_support(d,rz,rx)-exact
        if gap < -1e-10:
            raise AssertionError('posterior interval must not be worse than global box')
        strict += gap>1e-10
        gaps.append(gap)
        ratios.append((hi-lo)/(2*PHI_GLOBAL))
    return {
      'scope':'decision-conditioned robust support for thrust decision d and SMF attitude interval',
      'seed':seed,'cases':cases,
      'bounds':{'abs_deltaT':DT,'abs_phi_global':PHI_GLOBAL,'g':G},
      'max_formula_vs_endpoint_error':max_err,
      'strict_improvement_cases':strict,
      'mean_support_reduction_vs_global_phi_box':float(np.mean(gaps)),
      'max_support_reduction_vs_global_phi_box':float(np.max(gaps)),
      'min_support_reduction_vs_global_phi_box':float(np.min(gaps)),
      'mean_posterior_width_ratio':float(np.mean(ratios)),
      'versions':{'python':sys.version.split()[0],'numpy':np.__version__,'scipy':scipy.__version__},
      'interpretation':[
        'deltaT remains an MPC decision; it is never inserted into the SMF posterior.',
        'For a fixed candidate deltaT, robustification over the SMF phi interval is exact at interval endpoints.',
        'As a function of deltaT, the support is the maximum of two affine functions and therefore has an exact convex epigraph.',
        'A strict posterior interval can reduce support relative to the global phi box, but this does not by itself prove multistep recursive feasibility.'
      ]}

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--seed',type=int,default=20260924); ap.add_argument('--cases',type=int,default=10000)
    args=ap.parse_args(); out=run(args.seed,args.cases)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
