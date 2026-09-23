#!/usr/bin/env python3
"""Audit whether a control-normal support ledger improves the current rolling CZ baseline.

This intentionally uses the *actual certified attitude terminal normals* +/-[4,1]
and compares exact CZ support with the minimal coordinate-box outer approximation.
It also reports +/-[4,-1] as a non-controller diagnostic showing that correlations do
exist even when the currently certified controller does not consume them.
"""
from pathlib import Path
import argparse, json
import numpy as np
from check_shift_nested_scheduling_tube import CZ, support, ROOT


def box_support(cz, p):
    p=np.asarray(p,float); total=0.0
    for j,a in enumerate(p):
        if abs(a)<1e-15: continue
        e=np.eye(6)[j]
        total += a*support(cz,e) if a>=0 else (-a)*support(cz,-e)
    return total


def run(horizon=8,ticks=26):
    cfg=json.loads((ROOT/'configs/planar_baseline.json').read_text())
    dt=cfg['plant']['dt_s']; g=cfg['plant']['gravity_m_s2']
    F=np.eye(6); F[0,2]=F[1,3]=F[4,5]=dt; F[2,4]=-dt*g
    dx=1.880+4.905*.45+14.715*.45**3/6; dz=2.086+14.715*.45**2/2
    W=np.zeros((6,2)); W[2,0]=dt*dx; W[3,1]=dt*dz
    cz=CZ([0]*6,np.diag(cfg['initial_set']['halfwidth']))
    truth=np.array([.015,-.012,.04,-.03,.003,-.006])
    names=cfg['state_order']; noise_map=cfg['sensing']['observed_noise_halfwidth']
    normals={
      '+terminal_4_1':np.array([0,0,0,0,4.,1.]),
      '-terminal_4_1':np.array([0,0,0,0,-4.,-1.]),
      '+diagnostic_4_-1':np.array([0,0,0,0,4.,-1.]),
      '-diagnostic_4_-1':np.array([0,0,0,0,-4.,1.]),
    }
    gaps={k:[] for k in normals}; ledger_shift_violations=0; previous=None
    for tick in range(ticks):
        if tick:
            cz=cz.predict(np.asarray(F,dtype=object),np.asarray(W,dtype=object)); truth=F@truth
        indices=[4,5]+([0,1] if tick%5==0 else [])
        noise=np.array([noise_map[names[i]] for i in indices],float)
        mn=np.array([.3*noise[j]*((-1)**(tick+j)) for j in range(len(indices))])
        cz=cz.observe(indices,(truth[indices]+mn).tolist(),noise.tolist())
        horizon_support=[]; z=cz
        for i in range(horizon+1):
            row={}
            for name,p in normals.items():
                exact=support(z,p); outer=box_support(z,p)
                assert outer+1e-9>=exact
                gaps[name].append(outer-exact); row[name]=exact
            horizon_support.append(row); z=z.predict(np.asarray(F,dtype=object),np.asarray(W,dtype=object))
        if previous is not None:
            for i in range(horizon):
                for name in ('+terminal_4_1','-terminal_4_1'):
                    if horizon_support[i][name] > previous[i+1][name]+1e-9:
                        ledger_shift_violations += 1
        previous=horizon_support
    summary={}
    for name,values in gaps.items():
        a=np.asarray(values)
        summary[name]=dict(queries=len(values),strict_box_gap=int(np.sum(a>1e-10)),
                           mean_gap=float(np.mean(a)),max_gap=float(np.max(a)))
    return dict(status='rolling_control_normal_ledger_audit_not_full_mpc_proof',
                horizon=horizon,ticks=ticks,terminal_ledger_shift_violations=ledger_shift_violations,
                support_gap_vs_minimal_coordinate_box=summary,
                conclusion=('For the currently certified attitude terminal normals +/-[4,1], the minimal coordinate box is support-exact on this rolling benchmark; a separate support ledger gives no tightening benefit here. Correlation is visible on diagnostic +/-[4,-1], which is not a currently certified MPC normal.'),
                limitations=['current config has K=null, so no certified input-feedback mixed normals exist',
                             'fixed affine outer model; no terminal append or closed-loop MPC',
                             'floating HiGHS audit']))

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,required=True); ap.add_argument('--horizon',type=int,default=8); a=ap.parse_args()
    if a.output.exists(): ap.error('output must not already exist')
    out=run(a.horizon); a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
