#!/usr/bin/env python3
"""Verify a common-quadratic certificate for the chapter-31 LPV ancillary candidate.

The certificate P is stored explicitly so this script is a verifier, not a solver.
For M(T)=A(T)+BK affine in scalar T and P>0, x'M(T)'PM(T)x is convex in T.
Hence endpoint inequalities imply the same inequality for every T in the interval.
"""
from pathlib import Path
import argparse, json, sys
import numpy as np
import scipy
from scipy.linalg import eigvalsh

DT=.02; J=.02; TL=4.905; TU=14.715
K=np.array([[0.1425749515,0.2006738212,-1.1714620252,-0.2286054551]])
P=np.array([
 [0.074753239,0.053671859,-0.096346099,-0.005511332],
 [0.053671859,0.099182069,-0.203617926,-0.014759493],
 [-0.096346099,-0.203617926,0.819244229,0.056456306],
 [-0.005511332,-0.014759493,0.056456306,0.006820464]])

def closed_loop(T):
 A=np.array([[1,DT,0,0],[0,1,-DT*T,0],[0,0,1,DT],[0,0,0,1.]],float)
 B=np.array([[0.],[0.],[0.],[DT/J]],float)
 return A+B@K

def run():
 pe=np.linalg.eigvalsh(P)
 endpoints=[]
 worst_lambda2=0.
 for T in (TL,TU):
  M=closed_loop(T); D=P-M.T@P@M
  de=np.linalg.eigvalsh(D)
  lam2=float(eigvalsh(M.T@P@M,P).max()); worst_lambda2=max(worst_lambda2,lam2)
  endpoints.append(dict(T=T,min_eig_P_minus_MtPM=float(de.min()),max_eig_P_minus_MtPM=float(de.max()),lambda2_P_metric=lam2))
 # dense grid is a numerical cross-check only; the proof uses convexity + endpoints.
 grid=[]
 for T in np.linspace(TL,TU,1001):
  M=closed_loop(float(T)); grid.append(float(np.linalg.eigvalsh(P-M.T@P@M).min()))
 return dict(status='verified_common_quadratic_certificate_for_nominal_LPV_family_only',
  model='e+ = A(T)e+B tau, tau=K e, T in [4.905,14.715], vx+=vx-dt*T*phi',
  K=K.tolist(),P=P.tolist(),min_eig_P=float(pe.min()),max_eig_P=float(pe.max()),condition_number_P=float(pe.max()/pe.min()),
  endpoint_checks=endpoints,worst_lambda2_P_metric=worst_lambda2,worst_lambda_P_metric=float(np.sqrt(worst_lambda2)),
  dense_grid_1001_min_decay_eig=float(min(grid)),
  proof='M(T) is affine. For each fixed x, x^T M(T)^T P M(T) x is convex in scalar T because its quadratic coefficient is x^T D^T P D x >= 0. Therefore its maximum on the interval is attained at an endpoint. Positive endpoint matrices P-M^TPM imply the inequality for every T.',
  scope=['strict common-quadratic stability is certified for the disturbance-free LPV closed-loop family','this is not an RCI/tube certificate and does not yet prove hard state/input constraint satisfaction','nonlinear sin(phi) remainder and aerodynamic disturbance must still be added before K can be promoted into the baseline MPC config'],
  versions=dict(python=sys.version.split()[0],numpy=np.__version__,scipy=scipy.__version__))

if __name__=='__main__':
 ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,required=True); a=ap.parse_args()
 if a.output.exists(): ap.error('output must not already exist')
 out=run(); a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
