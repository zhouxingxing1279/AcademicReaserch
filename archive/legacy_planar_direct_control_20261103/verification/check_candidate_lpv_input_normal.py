#!/usr/bin/env python3
"""Reality-check a semantically consistent LPV ancillary *candidate*.

This does NOT certify a controller.  It forms the horizontal/attitude LPV family
with the known thrust T retained in A(T), computes the hover DARE gain, audits
frozen-vertex stability and short endpoint switching products, then asks whether
that physically generated input normal consumes correlations in the existing
rolling CZ-SMF benchmark.
"""
from pathlib import Path
from itertools import product
import argparse, json, sys
import numpy as np
import scipy
from scipy.linalg import solve_discrete_are
from check_shift_nested_scheduling_tube import CZ, support, ROOT


def ab(T, dt=.02, J=.02):
    A=np.array([[1,dt,0,0],[0,1,-dt*T,0],[0,0,1,dt],[0,0,0,1.]],float)
    B=np.array([[0.],[0.],[0.],[dt/J]],float)
    return A,B


def box_support(cz,p):
    total=0.; I=np.eye(6)
    for j,a in enumerate(np.asarray(p,float)):
        if abs(a)<1e-15: continue
        total += a*support(cz,I[j]) if a>=0 else (-a)*support(cz,-I[j])
    return total


def run(horizon=8,ticks=26,max_switch_length=12):
    cfg=json.loads((ROOT/'configs/planar_baseline.json').read_text())
    dt=cfg['plant']['dt_s']; g=cfg['plant']['gravity_m_s2']; J=cfg['plant']['inertia_kg_m2']
    Tl,Tu=cfg['domain']['input_lower'][0],cfg['domain']['input_upper'][0]
    A,B=ab(g,dt,J)
    qs=cfg['mpc']['state_cost_scale']; qd=cfg['mpc']['normalized_Q_diag']
    # horizontal/attitude order = px,vx,phi,omega; same normalized Q entries as config
    Q=np.diag([qd[0]/qs[0]**2,qd[2]/qs[2]**2,qd[4]/qs[4]**2,qd[5]/qs[5]**2])
    R=np.array([[cfg['mpc']['normalized_R_diag'][1]/cfg['mpc']['input_cost_scale'][1]**2]])
    P=solve_discrete_are(A,B,Q,R)
    K=-np.linalg.solve(R+B.T@P@B,B.T@P@A)
    vertices=[]; Ms=[]
    for T in (Tl,g,Tu):
        M=ab(T,dt,J)[0]+B@K; rho=float(max(abs(np.linalg.eigvals(M))))
        vertices.append(dict(T=T,spectral_radius=rho));
        if T in (Tl,Tu): Ms.append(M)
    switching=[]; worst=0.
    for L in range(1,max_switch_length+1):
        mx=0.
        for bits in product((0,1),repeat=L):
            M=np.eye(4)
            for bit in bits: M=Ms[bit]@M
            mx=max(mx,float(max(abs(np.linalg.eigvals(M)))**(1/L)))
        switching.append(dict(length=L,max_normalized_product_radius=mx)); worst=max(worst,mx)

    p=np.array([K[0,0],0,K[0,1],0,K[0,2],K[0,3]])
    F=np.eye(6); F[0,2]=F[1,3]=F[4,5]=dt; F[2,4]=-dt*g
    dx=1.880+4.905*.45+14.715*.45**3/6; dz=2.086+14.715*.45**2/2
    W=np.zeros((6,2)); W[2,0]=dt*dx; W[3,1]=dt*dz
    cz=CZ([0]*6,np.diag(cfg['initial_set']['halfwidth']))
    truth=np.array([.015,-.012,.04,-.03,.003,-.006]); names=cfg['state_order']; nm=cfg['sensing']['observed_noise_halfwidth']
    gaps=[]
    for tick in range(ticks):
        if tick:
            cz=cz.predict(np.asarray(F,dtype=object),np.asarray(W,dtype=object)); truth=F@truth
        idx=[4,5]+([0,1] if tick%5==0 else [])
        noise=np.array([nm[names[i]] for i in idx],float)
        meas_noise=np.array([.3*noise[j]*((-1)**(tick+j)) for j in range(len(idx))])
        cz=cz.observe(idx,(truth[idx]+meas_noise).tolist(),noise.tolist())
        z=cz
        for _ in range(horizon+1):
            for pp in (p,-p):
                exact=support(z,pp); outer=box_support(z,pp); assert outer+1e-9>=exact; gaps.append(outer-exact)
            z=z.predict(np.asarray(F,dtype=object),np.asarray(W,dtype=object))
    a=np.asarray(gaps)
    return dict(status='candidate_only_not_ancillary_or_terminal_certificate',
        model='horizontal-attitude LPV family with known thrust retained: vx+=vx-dt*T*phi; tau is the only ancillary input',
        K_horizontal_attitude=K.tolist(),input_normal_six_state=p.tolist(),vertex_frozen_stability=vertices,
        endpoint_switching_search=dict(max_length=max_switch_length,worst_normalized_product_radius=worst,records=switching,
            interpretation='finite product search is falsification evidence only, not an arbitrary-switching proof'),
        rolling_CZ_vs_coordinate_box_on_candidate_input_normal=dict(queries=int(len(a)),strict_gaps=int(np.sum(a>1e-10)),mean_gap=float(np.mean(a)),max_gap=float(np.max(a))),
        versions=dict(python=sys.version.split()[0],numpy=np.__version__,scipy=scipy.__version__),
        limitations=['K is a hover DARE candidate; no common Lyapunov/contractive terminal certificate is claimed',
                     'rolling CZ still uses the repository fixed affine outer model; this audit only asks whether the generated normal consumes posterior correlation',
                     'no additive-disturbance RPI or hard-input tube certificate is claimed'])

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,required=True); ap.add_argument('--horizon',type=int,default=8); a=ap.parse_args()
    if a.output.exists(): ap.error('output must not already exist')
    out=run(a.horizon); a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
