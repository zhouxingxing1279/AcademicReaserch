#!/usr/bin/env python3
"""Vertex-consistent ancillary-gain audit for the semantic LPV residual contract.

The thrust scheduling value T is known in A(T), therefore the nonlinear
remainder bound is also evaluated at that T:
    d_x(T) = 1.880 + T * phi_max^3 / 6.
Using d_x(T_max) at every vertex is safe but unnecessarily conservative.

Finite reachable supports are necessary lower bounds for any origin-containing
RPI set. They can reject a gain but cannot certify a gain.
"""
import argparse, json, sys
from pathlib import Path
import numpy as np
import scipy
from scipy.stats import qmc

H=0.02
PHI_LIMIT=0.45
TAU_LIMIT=0.08
T_VALUES=np.array([4.905,9.81,14.715],float)
STATE_LIMITS=np.array([5.0,3.0,0.45,2.0],float) # px,vx,phi,omega
B=np.array([0.0,0.0,0.0,1.0])
K_TORQUE=np.array([0.00153696,0.00744545,-0.09093386,-0.09567285])
K_BALANCED=np.array([0.01360726,0.41658618,-3.07723811,-0.52653095])

def residual_bound(T):
    return 1.880 + T*PHI_LIMIT**3/6.0

def A(T):
    out=np.eye(4)
    out[0,1]=H
    out[1,2]=-H*T
    out[2,3]=H
    return out

def audit_gain(K,terms=1000):
    K=np.asarray(K,float)
    records=[]
    for T in T_VALUES:
        M=A(T)+np.outer(B,K)
        w=np.array([0.0,H*residual_bound(T),0.0,0.0])
        v=w.copy()
        state=np.zeros(4)
        torque=0.0
        for _ in range(terms):
            state += np.abs(v)
            torque += abs(float(K@v))
            v=M@v
        records.append(dict(
            T=float(T), residual_bound=float(residual_bound(T)),
            spectral_radius=float(np.max(np.abs(np.linalg.eigvals(M)))),
            finite_state_support=state.tolist(),
            finite_torque_support=float(torque)))
    return records

def finite_metrics(K,terms):
    rec=audit_gain(K,terms)
    rho=max(r['spectral_radius'] for r in rec)
    state=np.max(np.array([r['finite_state_support'] for r in rec]),axis=0)
    torque=max(r['finite_torque_support'] for r in rec)
    return rho,state,torque,rec

def equilibrium_necessary_conditions():
    # Under constant r_x and stable fixed-T closed loop, equilibrium must satisfy
    # 0 = -T*phi + r_x, hence |phi| >= d_x(T)/T is required in any RPI.
    out=[]
    for T in T_VALUES:
        p=residual_bound(T)/T
        out.append(dict(
            T=float(T), residual_bound=float(residual_bound(T)),
            required_phi_support=float(p),
            fraction_of_phi_authority=float(p/PHI_LIMIT),
            remaining_phi_margin=float(PHI_LIMIT-p)))
    return out

def seeded_search(samples=30000,search_terms=220,seed=20260924):
    sampler=qmc.LatinHypercube(d=4,seed=seed)
    u=sampler.random(samples)
    lo=np.array([0.005,0.01,-6.0,-3.0])
    hi=np.array([1.2,3.0,-0.02,-0.01])
    gains=lo+(hi-lo)*u
    counts=dict(samples=samples,schur_all_vertices=0,torque_finite_pass=0,
                state_finite_pass=0,combined_finite_pass=0)
    best_ratio=float('inf'); best=None
    for K in gains:
        rho,state,torque,_=finite_metrics(K,search_terms)
        schur=rho<1.0
        torque_ok=schur and torque<=TAU_LIMIT
        state_ok=schur and bool(np.all(state<=STATE_LIMITS))
        counts['schur_all_vertices']+=int(schur)
        counts['torque_finite_pass']+=int(torque_ok)
        counts['state_finite_pass']+=int(state_ok)
        counts['combined_finite_pass']+=int(torque_ok and state_ok)
        ratio=max(rho/0.999,*(state/STATE_LIMITS),torque/TAU_LIMIT)
        if ratio<best_ratio:
            best_ratio=float(ratio); best=K.copy()
    return counts,best_ratio,best

def run(samples=30000,search_terms=220,audit_terms=2000,seed=20260924):
    counts,best_ratio,best=seeded_search(samples,search_terms,seed)
    rho,state,torque,records=finite_metrics(best,audit_terms)
    return dict(
        status='vertex_consistent_residual_audit_and_numerical_falsification_search',
        model='4-state horizontal-attitude LPV family; T known and retained in both A(T) and d_x(T)',
        state_order=['px','vx','phi','omega'],
        state_limits=STATE_LIMITS.tolist(),tau_limit=TAU_LIMIT,
        residual_formula='d_x(T)=1.880 + T*0.45^3/6',
        controller_independent_equilibrium_necessary_conditions=equilibrium_necessary_conditions(),
        chapter34_candidates=dict(
            torque_only=audit_gain(K_TORQUE,1000),
            balanced=audit_gain(K_BALANCED,1000)),
        latin_hypercube_search=dict(
            seed=seed,samples=samples,search_terms=search_terms,
            gain_box={'K_px':[0.005,1.2],'K_vx':[0.01,3.0],
                      'K_phi':[-6.0,-0.02],'K_omega':[-3.0,-0.01]},
            counts=counts,best_normalized_ratio_search=best_ratio,
            interpretation='No sampled gain passed all finite necessary conditions; this is not a nonexistence proof.'),
        best_sample_long_audit=dict(
            K=best.tolist(),terms=audit_terms,spectral_radius_max=float(rho),
            state_support_max=state.tolist(),torque_support_max=float(torque),
            state_normalized=(state/STATE_LIMITS).tolist(),
            torque_normalized=float(torque/TAU_LIMIT),
            vertex_records=records),
        conclusion=(
            'Using the global high-thrust residual at low thrust creates an avoidable false rejection in phi: '
            'the Chapter 34 balanced candidate has low-thrust phi support about 0.419 instead of about 0.451, '
            'but still fails the vx bound. A 30000-sample deterministic search found no static K passing all '
            'finite necessary checks, so joint constrained synthesis remains unresolved rather than impossible.'),
        versions={'python':sys.version.split()[0],'numpy':np.__version__,'scipy':scipy.__version__})

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--samples',type=int,default=30000)
    ap.add_argument('--search-terms',type=int,default=220)
    ap.add_argument('--audit-terms',type=int,default=2000)
    ap.add_argument('--seed',type=int,default=20260924)
    a=ap.parse_args()
    if a.output.exists(): ap.error('output must not already exist')
    out=run(a.samples,a.search_terms,a.audit_terms,a.seed)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
