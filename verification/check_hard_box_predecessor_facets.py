#!/usr/bin/env python3
"""Exact one-step robust predecessor facets for the current lateral hard box."""
from fractions import Fraction as F
import argparse, json
from pathlib import Path

h=F(1,50); J=F(1,50); TL=F(981,200); TH=F(2943,200)
P=F(5); V=F(3); PHI=F(9,20); OMG=F(2); TAU=F(2,25); AERO=F(47,25)

def dbar(T): return AERO + T*PHI**3/F(6)
def q(x): return {"fraction":f"{x.numerator}/{x.denominator}","float":float(x)}

def run():
    thrust=[]
    for T in (TL,TH):
        db=dbar(T)
        # hard-box corner v=+V, phi=-PHI, d=+db maximizes v+
        vnext=V+h*T*PHI+h*db
        thrust.append({"T":q(T),"dbar":q(db),"h_dbar":q(h*db),
                       "worst_velocity_successor":q(vnext),
                       "velocity_violation":q(vnext-V)})
    # exact robust predecessor inequalities:
    # |p+h v|<=P
    # |v-h*T*phi| + h*dbar(T) <= V, T in {TL,TH}; endpoint suffices by convexity in T
    # |phi+h*omega|<=PHI
    # omega coordinate: exists |tau|<=TAU s.t. |omega+(h/J)tau|<=OMG
    return {
      "model":"[p,v,phi,omega], p+=p+h v, v+=v-h T phi+h d, phi+=phi+h omega, omega+=omega+(h/J)tau",
      "exact_parameters":{"h":q(h),"J":q(J),"T_low":q(TL),"T_high":q(TH),"P":q(P),"V":q(V),"Phi":q(PHI),"Omega":q(OMG),"Tau":q(TAU)},
      "robust_predecessor_facets":[
        "|p+h*v| <= P",
        "|v-h*T_low*phi| + h*dbar(T_low) <= V",
        "|v-h*T_high*phi| + h*dbar(T_high) <= V",
        "|phi+h*omega| <= Phi",
        "exists |tau|<=Tau: |omega+(h/J)*tau|<=Omega"
      ],
      "endpoint_argument":"For fixed (v,phi), |v-h*T*phi|+h*(AERO+T*Phi^3/6) is convex in scalar T; its maximum on [T_low,T_high] is attained at an endpoint.",
      "hard_box_counterexamples":{
        "position_corner":{"state":"p=P,v=V","p_successor":q(P+h*V),"violation":q(h*V)},
        "attitude_corner":{"state":"phi=Phi,omega=Omega","phi_successor":q(PHI+h*OMG),"violation":q(h*OMG)},
        "velocity_corners":thrust
      },
      "conclusion":"The first robust predecessor of the hard box necessarily introduces p-v, v-phi, and phi-omega mixed facets. A template with only p-v braking facets is not predecessor-closed for this four-state chain."
    }

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,required=True); args=ap.parse_args()
    if args.output.exists(): ap.error('output must not already exist')
    out=run(); args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
