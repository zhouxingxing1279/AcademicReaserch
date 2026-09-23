#!/usr/bin/env python3
"""Audit a tempting 6-state ancillary LQR/RPI construction.

The script deliberately compares two disturbance contracts:
1) the globally consistent LTI abstraction, where -g*phi is retained and
   (T-g)*phi must remain in the additive horizontal disturbance;
2) an inconsistent optimistic calculation that uses the smaller
   input-preserving residual while still using the fixed hover LTI A matrix.

The second case is reported only to expose false feasibility; it is not a
controller certificate.
"""
import argparse, json, sys
from pathlib import Path
import numpy as np
import scipy
from scipy.linalg import solve_discrete_are, solve_discrete_lyapunov, eigvalsh

H=0.02; G=9.81; J=0.02; PHI=0.45
STATE_LIMIT=np.array([5.0,1.5,3.0,3.0,0.45,2.0])
INPUT_DEV_LIMIT=np.array([4.905,0.08])


def model():
    A=np.eye(6); A[0,2]=H; A[1,3]=H; A[2,4]=-H*G; A[4,5]=H
    B=np.zeros((6,2)); B[3,0]=H; B[5,1]=H/J
    return A,B


def lqr(A,B):
    xs=np.array([5.,3.,3.,3.,.45,2.]); us=np.array([9.81,.08])
    Q=np.diag(np.array([10.,10.,1.,1.,2.,.2])/xs**2)
    R=np.diag(np.array([.1,.1])/us**2)
    P=solve_discrete_are(A,B,Q,R)
    return -np.linalg.solve(R+B.T@P@B,B.T@P@A)


def outer_supports(Acl,K,dx,dz,N=1000):
    w=np.array([0.,0.,H*dx,H*dz,0.,0.])
    W=np.diag(w)
    P=solve_discrete_lyapunov(Acl.T,np.eye(6))
    rho=np.sqrt(max(eigvalsh(Acl.T@P@Acl,P)))
    corners=[np.array([0,0,sx*w[2],sz*w[3],0,0])
             for sx in (-1,1) for sz in (-1,1)]
    d=max(np.sqrt(v@P@v) for v in corners)
    radius=d/(1-rho)
    Pinv=np.linalg.inv(P)
    M=np.eye(6); hs=np.zeros(6); hu=np.zeros(2)
    for _ in range(N):
        hs += np.sum(np.abs(M@W),axis=1)
        hu += np.sum(np.abs(K@M@W),axis=1)
        M=Acl@M
    tail_s=np.array([radius*np.sqrt((M.T@np.eye(6)[:,i])@Pinv@(M.T@np.eye(6)[:,i])) for i in range(6)])
    tail_u=np.array([radius*np.sqrt((M.T@K[j])@Pinv@(M.T@K[j])) for j in range(2)])
    return hs+tail_s,hu+tail_u,rho,float(d),float(radius)


def run():
    A,B=model(); K=lqr(A,B); Acl=A+B@K
    dx_old=1.880+4.905*PHI+14.715*PHI**3/6
    dx_reduced=1.880+14.715*PHI**3/6
    dz=2.086+14.715*PHI**2/2
    cases={}
    for name,dx,semantics in [
        ('consistent_global_lti',dx_old,'valid for fixed hover A: includes (T-g)phi'),
        ('optimistic_mismatched',dx_reduced,'INVALID certificate: reduced residual requires retaining -T*phi, not fixed -g*phi')]:
        hs,hu,rhoP,dP,rP=outer_supports(Acl,K,dx,dz)
        cases[name]={
            'semantics':semantics,'dx':dx,'dz':dz,
            'state_support_outer':hs.tolist(),'state_margin':(STATE_LIMIT-hs).tolist(),
            'input_support_outer':hu.tolist(),'input_margin':(INPUT_DEV_LIMIT-hu).tolist(),
            'all_state_margins_positive':bool(np.all(STATE_LIMIT-hs>=0)),
            'all_input_margins_positive':bool(np.all(INPUT_DEV_LIMIT-hu>=0)),
            'lyapunov_norm_contraction':rhoP,'disturbance_P_norm':dP,'rpi_P_radius_bound':rP,
        }
    return {
        'scope':'6-state hover LQR ancillary-controller consistency audit',
        'K':K.tolist(),'closed_loop_spectral_radius':float(max(abs(np.linalg.eigvals(Acl)))),
        'state_order':['px','pz-2','vx','vz','phi','omega'],
        'input_deviation_order':['T-g','tau'],
        'limits':{'state':STATE_LIMIT.tolist(),'input_deviation':INPUT_DEV_LIMIT.tolist()},
        'finite_sum_terms':1000,'cases':cases,
        'conclusion':'The consistent global LTI abstraction violates vx, phi and tau RPI margins. The apparently feasible reduced-residual result is not a valid certificate because it mixes the -T*phi residual bound with a fixed -g*phi LTI matrix.',
        'versions':{'python':sys.version.split()[0],'numpy':np.__version__,'scipy':scipy.__version__},
    }

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--output',type=Path,required=True); a=p.parse_args()
    if a.output.exists(): p.error('output must not already exist')
    out=run(); a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
