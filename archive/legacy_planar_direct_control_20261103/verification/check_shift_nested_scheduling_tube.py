#!/usr/bin/env python3
"""Audit shift nesting of horizon-wise phi projections from the rolling CZ-SMF.

The experiment uses the repository six-state affine outer model and truth-consistent
measurements.  It checks the exact support condition needed by a shifted MPC
candidate; it is not itself a closed-loop MPC proof.
"""
from pathlib import Path
import argparse, json
import numpy as np
from scipy.optimize import linprog
from check_constrained_zonotope import CZ

ROOT=Path(__file__).resolve().parents[1]

def support(cz,p):
    p=np.asarray(p,float); f=p@np.asarray(cz.g,float)
    kw=dict(bounds=(-1,1),method='highs')
    if len(cz.b): kw.update(A_eq=np.asarray(cz.a,float),b_eq=np.asarray(cz.b,float))
    r=linprog(-f,**kw)
    if not r.success: raise RuntimeError(r.message)
    return float(p@np.asarray(cz.c,float)-r.fun)

def phi_interval(cz):
    e=np.eye(6)[4]
    return [-support(cz,-e),support(cz,e)]

def horizon(cz,F,W,N):
    out=[]
    for _ in range(N+1):
        out.append(phi_interval(cz)); cz=cz.predict(F,W)
    return out

def run(seed=20260924,N=8,ticks=26):
    cfg=json.loads((ROOT/'configs/planar_baseline.json').read_text())
    dt=cfg['plant']['dt_s']; g=cfg['plant']['gravity_m_s2']
    F=np.eye(6); F[0,2]=F[1,3]=F[4,5]=dt; F[2,4]=-dt*g
    dx=1.880+4.905*.45+14.715*.45**3/6; dz=2.086+14.715*.45**2/2
    W=np.zeros((6,2)); W[2,0]=dt*dx; W[3,1]=dt*dz
    cz=CZ([0]*6,np.diag(cfg['initial_set']['halfwidth']))
    truth=np.array([.015,-.012,.04,-.03,.003,-.006])
    noise_map=cfg['sensing']['observed_noise_halfwidth']; names=cfg['state_order']
    previous=None; comparisons=violations=strict_endpoints=0; max_violation=0.; reductions=[]; records=[]
    for tick in range(ticks):
        if tick:
            cz=cz.predict(np.asarray(F,dtype=object),np.asarray(W,dtype=object)); truth=F@truth
        indices=[4,5]+([0,1] if tick%5==0 else [])
        noise=np.array([noise_map[names[i]] for i in indices],float)
        measurement_noise=np.array([.3*noise[j]*((-1)**(tick+j)) for j in range(len(indices))])
        cz=cz.observe(indices,(truth[indices]+measurement_noise).tolist(),noise.tolist())
        current=horizon(cz,np.asarray(F,dtype=object),np.asarray(W,dtype=object),N)
        tick_bad=0
        if previous is not None:
            for i in range(N):
                new=np.asarray(current[i]); old=np.asarray(previous[i+1])
                lower_reduction=new[0]-old[0]; upper_reduction=old[1]-new[1]
                reductions.extend([lower_reduction,upper_reduction]); comparisons+=1
                if lower_reduction < -1e-9 or upper_reduction < -1e-9:
                    violations+=1; tick_bad+=1
                    max_violation=max(max_violation,-lower_reduction,-upper_reduction)
                strict_endpoints += int(lower_reduction>1e-10)+int(upper_reduction>1e-10)
        records.append(dict(tick=tick,violations=tick_bad,phi_now=current[0]))
        previous=current
    return dict(status='shift_nested_phi_scheduling_tube_audit_not_full_mpc_proof',seed=seed,
                horizon=N,ticks=ticks,shift_interval_comparisons=comparisons,
                violations=violations,max_violation=max_violation,
                strict_endpoint_reductions=strict_endpoints,
                mean_endpoint_reduction=float(np.mean(reductions)),
                max_endpoint_reduction=float(np.max(reductions)),
                theorem_scope=('For a fixed monotone prediction map P(S)=F S (+) W and an exact '
                               'measurement update X+ subset X-, P^i(X_{k+1}) subset P^(i+1)(X_k).'),
                limitations=['floating HiGHS support audit; theorem itself follows from set inclusion',
                             'fixed affine outer model and fixed disturbance set',
                             'does not cover decision-dependent map changes or terminal append'],records=records)

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,required=True); ap.add_argument('--seed',type=int,default=20260924); ap.add_argument('--horizon',type=int,default=8)
    a=ap.parse_args()
    if a.output.exists(): ap.error('output must not already exist')
    result=run(a.seed,a.horizon); a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
