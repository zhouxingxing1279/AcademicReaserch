#!/usr/bin/env python3
"""Test recentering on control normals already certified in the repository.

Important negative result: the existing certified attitude terminal/input normals do
not reproduce the random mixed-direction violations from chapter 23. This script
therefore prevents promoting that geometric phenomenon to an MPC contribution
before a translational feedback/terminal certificate exists.
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

def midpoint(cz):
    z=np.zeros(6)
    for i in range(6):
        e=np.eye(6)[i]; z[i]=(support(cz,e)-support(cz,-e))/2
    return z

def run():
    cfg=json.loads((ROOT/'configs/planar_baseline.json').read_text())
    dt=cfg['plant']['dt_s']; gravity=cfg['plant']['gravity_m_s2']
    f=np.eye(6); f[0,2]=f[1,3]=f[4,5]=dt; f[2,4]=-dt*gravity
    dx=1.880+4.905*.45+14.715*.45**3/6; dz=2.086+14.715*.45**2/2
    w=np.zeros((6,2)); w[2,0]=dt*dx; w[3,1]=dt*dz
    cz=CZ([0]*6,np.diag(cfg['initial_set']['halfwidth']))
    truth=np.array([.015,-.012,.04,-.03,.003,-.006])
    # State box normals plus the exact finite attitude terminal faces H=[±(1,0), ±(4,1)]
    # from theory/05, and torque-correction normal ±K with K=[8/25,4/25].
    dirs=list(np.vstack([np.eye(6),-np.eye(6)]))
    labels=[f'+e{i}' for i in range(6)]+[f'-e{i}' for i in range(6)]
    extra=[([0,0,0,0,1,0],'terminal +phi'),([0,0,0,0,-1,0],'terminal -phi'),
           ([0,0,0,0,4,1],'terminal +(4phi+omega)'),([0,0,0,0,-4,-1],'terminal -(4phi+omega)'),
           ([0,0,0,0,8/25,4/25],'input +K attitude error'),
           ([0,0,0,0,-8/25,-4/25],'input -K attitude error')]
    for p,name in extra: dirs.append(p); labels.append(name)
    dirs=np.asarray(dirs,float)
    noise_map=cfg['sensing']['observed_noise_halfwidth']; names=cfg['state_order']
    records=[]; total=0; bad_ticks=0; max_growth=0.0
    for tick in range(26):
        if tick:
            cz=cz.predict(np.asarray(f,dtype=object),np.asarray(w,dtype=object)); truth=f@truth
        zpre=midpoint(cz); old=np.array([support(cz,p)-p@zpre for p in dirs])
        indices=[4,5]+([0,1] if tick%5==0 else [])
        noise=np.array([noise_map[names[i]] for i in indices],float)
        y=truth[indices]+np.array([.3*noise[j]*((-1)**(tick+j)) for j in range(len(indices))])
        cz=cz.observe(indices,y.tolist(),noise.tolist())
        zpost=midpoint(cz); post=np.array([support(cz,p)-p@zpost for p in dirs])
        growth=post-old; bad=np.where(growth>1e-8)[0]
        total+=len(bad); bad_ticks+=bool(len(bad)); max_growth=max(max_growth,float(np.max(growth)))
        records.append({'tick':tick,'violations':[labels[i] for i in bad],
                        'max_growth':float(max(0,np.max(growth)))})
    return {'status':'negative_result_existing_certified_normals_do_not_exhibit_recenter_failure',
            'ticks':26,'directions':len(dirs),'violation_ticks':bad_ticks,
            'direction_violations':total,'max_growth':max_growth,
            'normals':['12 signed state-box normals','4 finite attitude terminal normals','2 attitude torque-feedback normals'],
            'key_limitation':'planar_baseline.json still has K=null and terminal_certificate=null; no certified translational feedback/input normals exist yet',
            'interpretation':'chapter-23 random mixed-direction counterexamples are geometric stress tests, not yet a demonstrated MPC recursive-feasibility failure',
            'records':records}

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,required=True); args=ap.parse_args()
    if args.output.exists(): ap.error('output must not already exist')
    r=run(); args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='records'},indent=2))
