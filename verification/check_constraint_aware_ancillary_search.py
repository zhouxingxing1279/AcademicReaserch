#!/usr/bin/env python3
"""Audit two feedback candidates after the Chapter 33 torque obstruction.

This script deliberately separates (i) torque-only feasibility from (ii) the
full state/input constrained ancillary problem.  It uses finite disturbance
reachable supports, hence every reported support is a lower bound on any RPI
set for the corresponding fixed-thrust scheduling path.

The candidates were obtained in a seeded SciPy differential-evolution search
(seed 20260924).  They are frozen here so the audit is deterministic and cheap.
No existence/non-existence theorem is inferred from the heuristic search.
"""
import argparse, json, sys
from pathlib import Path
import numpy as np
import scipy

H=0.02
DX=2.1034840625
T_VALUES=(4.905,9.81,14.715)
LIMITS={'tau':0.08,'vx':3.0,'phi':0.45}
K_TORQUE=np.array([0.00153696,0.00744545,-0.09093386,-0.09567285])
K_BALANCED=np.array([0.01360726,0.41658618,-3.07723811,-0.52653095])

def closed_loop(K,T):
    A=np.eye(4); A[0,1]=H; A[1,2]=-H*T; A[2,3]=H
    A[3,:]+=K                 # h/J = 1, same convention as Ch. 31--33
    return A

def finite_support(K,T,p0,n=1000):
    M=closed_loop(K,T); w=np.array([0.0,H*DX,0.0,0.0]); p=np.array(p0,float)
    s=0.0
    for _ in range(n):
        s += abs(float(p@w)); p=M.T@p
    return s

def audit(K):
    ans={'K':K.tolist(),'vertices':{}}
    for T in T_VALUES:
        M=closed_loop(K,T)
        ans['vertices'][str(T)]={
            'rho':float(max(abs(np.linalg.eigvals(M)))),
            'tau_support_N1000':finite_support(K,T,K),
            'vx_support_N1000':finite_support(K,T,[0,1,0,0]),
            'phi_support_N1000':finite_support(K,T,[0,0,1,0]),
        }
    return ans

def run():
    return {
      'scope':'constraint-aware ancillary feedback falsification audit',
      'seed_used_for_search':20260924,'h':H,'dx':DX,'limits':LIMITS,
      'torque_only_candidate':audit(K_TORQUE),
      'balanced_search_candidate':audit(K_BALANCED),
      'logic':'For each fixed thrust, finite reachable supports are necessary lower bounds for every origin-containing RPI set. A candidate can be rejected if any such support exceeds its hard bound. Passing finite supports is not an RPI certificate and endpoint Schur stability is not a common-Lyapunov certificate.',
      'conclusion':'Chapter 33 rejects the old hover-DARE K, but does not imply actuator-authority impossibility: a numerically stable torque-only K keeps 1000-term torque support far below 0.08. It does so by allowing large vx/phi tubes. A second balanced candidate keeps torque below 0.08 but violates low-thrust vx/phi lower bounds. Therefore the next problem is joint state/input constrained synthesis; neither existence nor impossibility is yet proved.',
      'versions':{'python':sys.version.split()[0],'numpy':np.__version__,'scipy':scipy.__version__},
    }

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,required=True); a=ap.parse_args()
    if a.output.exists(): ap.error('output must not already exist')
    out=run(); a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
