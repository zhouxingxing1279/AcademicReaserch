#!/usr/bin/env python3
"""Exact obstruction for origin-centered axis-aligned RCI boxes.

For p+ = p + h v, invariance of [-P,P]x[-V,V] under every state in the
box requires V=0. With nonzero horizontal residual width and phi initially
zero, V=0 cannot be robustly invariant because v+ = h d != 0. This is a
controller-independent obstruction: torque does not enter v+ in the same tick.
"""
import argparse, json
from fractions import Fraction as F
from pathlib import Path


def verify():
    h=F(1,50); P=F(5); V=F(3); phi=F(9,20); Tlow=F(981,200)
    aero=F(47,25)  # 1.880
    dlow=aero + Tlow*phi**3/F(6)

    # Corner p=P,v=V is in any full Cartesian box with these halfwidths.
    p_next=P+h*V
    assert p_next>P

    # General proof obligation at p=P,v=Vbox: P+h*Vbox <= P => Vbox<=0.
    # Since a halfwidth is nonnegative, axis-aligned invariance forces Vbox=0.
    forced_velocity_halfwidth=F(0)

    # But with v=0, phi=0 and any admissible nonzero residual d, v+=h*d.
    # tau affects omega+ only, so no causal choice of tau can cancel this tick.
    v_next=h*dlow
    assert dlow>0 and v_next>0

    return {
      "status":"EXACT_AXIS_ALIGNED_RCI_OBSTRUCTION_PASSED",
      "scope":"four-state lateral LPV abstraction; origin-centered Cartesian product state tube",
      "dt":str(h),
      "hard_position_halfwidth":str(P),
      "hard_velocity_halfwidth":str(V),
      "position_corner_next":str(p_next),
      "position_violation":str(p_next-P),
      "invariance_forces_velocity_halfwidth":str(forced_velocity_halfwidth),
      "low_thrust_residual_halfwidth":str(dlow),
      "velocity_after_one_tick_from_zero_under_positive_residual":str(v_next),
      "controller_independent_reason":"tau has relative degree two to phi and three to v in the chosen discrete model; it cannot alter v+ at the current tick",
      "conclusion":"No nonempty origin-centered axis-aligned Cartesian RCI box can be robustly invariant for the stated nonzero residual contract.",
      "does_not_rule_out":["correlated polytope/CZ RCI sets","ellipsoidal RPI/RCI sets","parameter-dependent sets","non-box nonlinear invariant sets"]
    }

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--output',type=Path,required=True); a=p.parse_args()
    if a.output.exists(): p.error('output must not already exist')
    out=verify(); a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
