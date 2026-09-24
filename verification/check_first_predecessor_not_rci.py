#!/usr/bin/env python3
"""Exact certificate that X intersect Pre(X) is not RCI for the lateral model."""
from fractions import Fraction as F
import argparse, json
from pathlib import Path

h=F(1,50); J=F(1,50); TL=F(981,200); PHI=F(9,20)
V=F(3); P=F(5); OMG=F(2); TAU=F(2,25); AERO=F(47,25)

def dbar(T): return AERO + T*PHI**3/F(6)
def q(x): return {"fraction":f"{x.numerator}/{x.denominator}","float":float(x)}

def run():
    db=dbar(TL)
    # Boundary point of X1 = X intersect robust Pre(X):
    # v=-V, phi=-db/T makes the negative worst disturbance keep v exactly at -V.
    # omega=+OMG is admissible and saturates no X1 first-step facet.
    p=P; v=-V; phi=-db/TL; omega=OMG; d=-db
    p1=p+h*v
    v1=v-h*TL*phi+h*d
    phi1=phi+h*omega
    # X1 contains the low-thrust predecessor facet
    # |v-h*T*phi| + h*dbar(T) <= V.
    lhs_next=abs(v1-h*TL*phi1)+h*db
    violation=lhs_next-V
    predicted=h*h*TL*omega
    return {
      "claim":"X1 = X intersect robust Pre(X) is not robust control invariant.",
      "exact_parameters":{"h":q(h),"T_low":q(TL),"dbar_low":q(db),"V":q(V),"Omega":q(OMG),"Tau":q(TAU)},
      "witness_state":{"p":q(p),"v":q(v),"phi":q(phi),"omega":q(omega)},
      "chosen_disturbance":q(d),
      "successor_before_torque_effect":{"p_plus":q(p1),"v_plus":q(v1),"phi_plus":q(phi1)},
      "next_X1_low_thrust_velocity_facet_lhs":q(lhs_next),
      "facet_limit":q(V),
      "strict_violation":q(violation),
      "closed_form_violation_h2_T_omega":q(predicted),
      "torque_independence":"Current tau changes only omega_plus. The violated X1 facet depends only on (v_plus,phi_plus), so no admissible or unbounded current torque can repair this one-step violation.",
      "normal_growth":"Pulling the v-phi predecessor facet back one more step introduces omega through phi_plus=phi+h*omega; equivalently the second predecessor contains a v-phi-omega mixed normal.",
      "conclusion":"The exact one-step predecessor normals from chapter 38 are necessary but not closed under repeated predecessor. A fixed template containing only p-v, v-phi, and phi-omega pairwise facets cannot be justified as predecessor-closed; deeper-chain normals or a configuration-constrained/optimized polytope are required."
    }

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--output',type=Path,required=True); args=ap.parse_args()
    if args.output.exists(): ap.error('output must not already exist')
    out=run(); assert out['strict_violation']['fraction']==out['closed_form_violation_h2_T_omega']['fraction']
    args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
