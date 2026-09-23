#!/usr/bin/env python3
"""Rolling six-state CZ test for directional recenter budgets.

This is a numerical falsification/validation experiment, not a theorem prover.
It reuses the physical affine outer model and CZ update from
check_constrained_zonotope.py, injects nonzero truth-consistent measurements,
and compares coordinate-midpoint recentering with a budget-constrained center LP.
"""
from pathlib import Path
import argparse, json
import numpy as np
from scipy.optimize import linprog

from check_constrained_zonotope import CZ, eye, zeros

ROOT = Path(__file__).resolve().parents[1]


def exact_float_support(cz, p):
    p = np.asarray(p, dtype=float)
    f = p @ np.asarray(cz.g, dtype=float)
    kw = dict(bounds=(-1, 1), method="highs")
    if len(cz.b):
        kw.update(A_eq=np.asarray(cz.a, dtype=float), b_eq=np.asarray(cz.b, dtype=float))
    r = linprog(-f, **kw)
    if not r.success:
        raise RuntimeError(r.message)
    return float(p @ np.asarray(cz.c, dtype=float) - r.fun)


def coordinate_midpoint(cz):
    out = np.zeros(6)
    for i in range(6):
        e = np.eye(6)[i]
        out[i] = (exact_float_support(cz, e) - exact_float_support(cz, -e)) / 2
    return out


def budget_center(cz, directions, old_error_support, target):
    """Choose a member of the posterior CZ closest (Linf) to target.

    The center is c+G xi, A xi=b, |xi|<=1. Direction constraints enforce
    h_X+(p)-p'z+ <= h_E-(p). The returned LP is a numerical proposal; every
    reported directional inequality is checked again from fresh support LPs.
    """
    g = np.asarray(cz.g, dtype=float); c = np.asarray(cz.c, dtype=float)
    n = g.shape[1]; aub=[]; bub=[]; hpost=[]
    for p, hold in zip(directions, old_error_support):
        hp = exact_float_support(cz, p); hpost.append(hp)
        aub.append(np.r_[-p @ g, 0.0])
        bub.append(-(hp - hold - p @ c))
    for i in range(6):
        row=np.zeros(n+1); row[:n]=g[i]; row[-1]=-1
        aub.append(row); bub.append(target[i]-c[i])
        row=np.zeros(n+1); row[:n]=-g[i]; row[-1]=-1
        aub.append(row); bub.append(-target[i]+c[i])
    aeq=np.hstack([np.asarray(cz.a,dtype=float), np.zeros((len(cz.b),1))])
    r=linprog(np.r_[np.zeros(n),1.0], A_ub=np.asarray(aub), b_ub=np.asarray(bub),
              A_eq=aeq if len(cz.b) else None,
              b_eq=np.asarray(cz.b,dtype=float) if len(cz.b) else None,
              bounds=[(-1,1)]*n+[(0,None)], method="highs")
    if not r.success:
        raise RuntimeError(r.message)
    return c + g @ r.x[:-1], float(r.x[-1]), np.asarray(hpost)


def run(seed=20260923):
    cfg=json.loads((ROOT/'configs/planar_baseline.json').read_text())
    dt=cfg['plant']['dt_s']; gravity=cfg['plant']['gravity_m_s2']
    f=np.eye(6); f[0,2]=f[1,3]=f[4,5]=dt; f[2,4]=-dt*gravity
    dx=1.880+4.905*.45+14.715*.45**3/6
    dz=2.086+14.715*.45**2/2
    w=np.zeros((6,2)); w[2,0]=dt*dx; w[3,1]=dt*dz
    initial=np.asarray(cfg['initial_set']['halfwidth'],float)
    cz=CZ([0]*6, np.diag(initial))
    # Error coordinates: physical altitude center 2 m has already been removed.
    truth=np.array([.015,-.012,.04,-.03,.003,-.006])
    rng=np.random.default_rng(seed)
    coordinate=np.vstack([np.eye(6),-np.eye(6)])
    mixed=rng.normal(size=(50,6)); mixed/=np.linalg.norm(mixed,axis=1,keepdims=True)
    directions=np.vstack([coordinate,mixed])
    unrestricted_bad=0; bad_ticks=0; max_growth=0.; adjusted=0; max_adjustment=0.; safe_bad=0
    records=[]
    noise_map=cfg['sensing']['observed_noise_halfwidth']; names=cfg['state_order']
    for tick in range(26):
        if tick:
            cz=cz.predict(np.asarray(f,dtype=object),np.asarray(w,dtype=object)); truth=f@truth
        pre_center=coordinate_midpoint(cz)
        old=np.array([exact_float_support(cz,p)-p@pre_center for p in directions])
        indices=[4,5]+([0,1] if tick%5==0 else [])
        noise=np.array([noise_map[names[i]] for i in indices],float)
        measurement_noise=np.array([.3*noise[j]*((-1)**(tick+j)) for j in range(len(indices))])
        y=truth[indices]+measurement_noise
        cz=cz.observe(indices, y.tolist(), noise.tolist())
        target=coordinate_midpoint(cz)
        post_target=np.array([exact_float_support(cz,p)-p@target for p in directions])
        bad=np.where(post_target>old+1e-8)[0]
        if len(bad):
            bad_ticks+=1; unrestricted_bad+=len(bad); max_growth=max(max_growth,float(np.max(post_target-old)))
        safe, adjustment, hpost=budget_center(cz,directions,old,target)
        post_safe=hpost-directions@safe
        this_safe=int(np.sum(post_safe>old+1e-7)); safe_bad+=this_safe
        if adjustment>1e-10: adjusted+=1
        max_adjustment=max(max_adjustment,adjustment)
        records.append(dict(tick=tick,observed=indices,unrestricted_violations=int(len(bad)),
                            max_unrestricted_growth=float(max(0,np.max(post_target-old))),
                            center_adjustment_linf=adjustment,safe_violations=this_safe))
    return dict(status='rolling_cz_recenter_numerical_falsification_not_controller', seed=seed,
                ticks=26, protected_directions=len(directions),
                unrestricted_violation_ticks=bad_ticks,
                unrestricted_direction_violations=unrestricted_bad,
                max_unrestricted_support_growth=max_growth,
                budget_center_adjusted_ticks=adjusted,
                max_budget_center_adjustment_linf=max_adjustment,
                budget_center_direction_violations=safe_bad,
                truth_initial=truth.tolist(),
                measurement_noise_rule='0.3*halfwidth*(-1)^(tick+measurement_index)',
                limitations=['support and center LPs are floating HiGHS in this experiment',
                             'protected directions are 12 coordinate signs plus 50 seeded mixed directions',
                             'this checks same-tick measurement/recenter containment, not MPC recursive feasibility'],
                records=records)

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,required=True); ap.add_argument('--seed',type=int,default=20260923)
    args=ap.parse_args()
    if args.output.exists(): ap.error('output must not already exist')
    result=run(args.seed); args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='records'},indent=2))
