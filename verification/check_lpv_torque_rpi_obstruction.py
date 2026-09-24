#!/usr/bin/env python3
"""Finite-reachable-set obstruction for the semantic LPV ancillary candidate.

A fixed thrust is an admissible scheduling path. For such a path, every RPI
set containing the origin must contain each finite disturbance reachable set.
Therefore a finite-horizon support larger than the torque limit is already a
rigorous impossibility certificate; no infinite-tail approximation is needed.
"""
import argparse, json, sys
from pathlib import Path
import numpy as np
import scipy

H=0.02; PHI=0.45
K=np.array([0.1425749515,0.2006738212,-1.1714620252,-0.2286054551])
T_VALUES=[4.905,9.81,14.715]
TAU_LIMIT=0.08

def closed_loop(T):
    A=np.eye(4); A[0,1]=H; A[1,2]=-H*T; A[2,3]=H
    B=np.array([[0.0],[0.0],[0.0],[1.0]])  # h/J = 1
    return A+B@K[None,:]

def finite_reachable_support(T,dx,nmax=1000):
    M=closed_loop(T); w=np.array([0.0,H*dx,0.0,0.0]); p=K.copy()
    vals=[]; s=0.0; crossing=None
    for n in range(1,nmax+1):
        s += abs(float(p@w)); vals.append(s)
        if crossing is None and s > TAU_LIMIT: crossing=n
        p=M.T@p
    return {
        'support_after_terms': {str(n):vals[n-1] for n in (10,25,50,69,100,1000)},
        'first_term_count_exceeding_tau_limit':crossing,
        'max_support_checked':vals[-1],
    }

def run():
    dx_aero=1.880
    dx_full=1.880+14.715*PHI**3/6
    cases={}
    for name,dx in [('aero_only_lower_bound',dx_aero),('semantic_full_residual',dx_full)]:
        cases[name]={'dx':dx,'vertices':{str(T):finite_reachable_support(T,dx) for T in T_VALUES}}
    return {
        'scope':'4-state semantic LPV ancillary torque reachable-set obstruction',
        'state_order':['px','vx','phi','omega'],'K':K.tolist(),'tau_limit':TAU_LIMIT,
        'disturbance_injection':'w=[0,h*r_x,0,0], |r_x|<=dx; fixed T is an admissible scheduling path',
        'cases':cases,
        'logic':'Any RPI set containing the origin must contain every finite disturbance reachable set. At T=14.715 the finite reachable support in direction K exceeds 0.08, so no RPI tube for this fixed K and stated disturbance contract can satisfy |K e|<=0.08. This is a lower-bound obstruction and needs no tail approximation.',
        'conclusion':'Candidate K is rejected as a robust ancillary controller under the current global residual contract. Full residual crosses at 50 terms; even aero-only dx=1.880 crosses at 69 terms at T=14.715.',
        'versions':{'python':sys.version.split()[0],'numpy':np.__version__,'scipy':scipy.__version__},
    }

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,required=True); a=ap.parse_args()
    if a.output.exists(): ap.error('output must not already exist')
    out=run(); a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
