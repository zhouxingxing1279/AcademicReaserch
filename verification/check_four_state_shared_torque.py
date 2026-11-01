#!/usr/bin/env python3
"""Run236: exact observation-fiber obstruction for the Run235 terminal feedback.

Shows the specific full-state law is not measurable from the permitted outputs.
Does NOT rule out alternative shared controls or prove F is non-invariant under them.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as F
from pathlib import Path
import check_four_state_finite_rpi as rpi

ZERO = F(0)
ONE = F(1)
SUPPORT_PREFIX = 100


def certificate(root=None):
    if root is not None:
        c=json.loads((Path(root)/'configs/planar_baseline.json').read_text())
        assert c['sensing']['always_observed_indices']==[4,5]
        assert c['sensing']['position_indices']==[0,1]
        assert c['sensing']['position_period_ticks']==5
        assert c['sensing']['max_consecutive_missed_packets']==2
        assert F(str(c['sensing']['observed_noise_halfwidth']['px']))==F(1,50)
        assert F(str(c['sensing']['observed_noise_halfwidth']['phi']))==F(1,200)
        assert F(str(c['sensing']['observed_noise_halfwidth']['omega']))==F(1,100)
        assert F(str(c['initial_set']['halfwidth'][2]))==F(1,10)
        assert F(str(c['initial_set']['center'][2]))==ZERO
        assert F(str(c['initial_set']['center'][0]))==ZERO
        assert F(str(c['initial_set']['center'][4]))==ZERO
        assert F(str(c['initial_set']['center'][5]))==ZERO
    # First Run235 finite-zonotope generator: D*B, exactly in F (one coefficient=1).
    g=tuple(rpi.D*b for b in rpi.B)
    xplus=g
    xminus=tuple(-v for v in g)
    assert xplus[0]==xminus[0]==ZERO
    assert xplus[2:]==xminus[2:]==(ZERO,ZERO)
    assert abs(g[1])<=F(1,10)  # both are in the configured initial velocity prior
    uplus=-rpi.dot(rpi.K,xplus)
    uminus=-rpi.dot(rpi.K,xminus)
    delta=abs(uplus-uminus)/2
    assert uplus==-uminus and delta>ZERO
    assert abs(uplus)<rpi.TAU_MAX
    # For every common u: max(|u-uplus|, |u-uminus|) >= delta.
    # Angular-rate next-step mismatch equals h/J times that torque error = delta.
    assert rpi.H==F(1,50)
    assert rpi.H/F(1,50)==ONE
    # A sufficient actuator tightening based on sup_F|Kx| + error_budget fails
    # for every error_budget >= delta.  The prefix support is a rigorous LOWER
    # bound for sup_F|Kx| because P_100 is a Minkowski summand of F.
    v=rpi.B
    prefix=ZERO
    for _ in range(SUPPORT_PREFIX):
        prefix+=rpi.D*abs(rpi.dot(rpi.K,v))
        v=rpi.mv(v)
    assert prefix+delta>rpi.TAU_MAX
    return {
        'run':236,
        'evidence':'EXACT_RATIONAL_INFORMATION_FIBER_COUNTEREXAMPLE',
        'scope':'Run235 frozen Euler 4-state, fixed thrust, full-state K, Run221 sensing at initial position packet',
        'main_theorem':'two distinct states in F and initial prior have identical available observation, but require distinct Run235 feedback torques',
        'state_plus':[str(v) for v in xplus],
        'state_minus':[str(v) for v in xminus],
        'common_observation_p_phi_omega':['0','0','0'],
        'torque_fullstate_plus':str(uplus),
        'torque_fullstate_minus':str(uminus),
        'minimax_common_torque_error_lower':str(delta),
        'minimax_omega_successor_error_lower':str(delta),
        'prefix_terms':SUPPORT_PREFIX,
        'terminal_torque_support_lower':str(prefix),
        'support_plus_error_exceeds_limit':prefix+delta>rpi.TAU_MAX,
        'torque_limit':str(rpi.TAU_MAX),
        'conclusion':'Full-state terminal law is not output-measurable; naive global additive-error tightening with budget >= minimax error cannot certify the torque limit',
        'limitations':['Does not show that no shared torque keeps both successors in F',
                       'Does not show that F is unsuitable for all output-feedback designs',
                       'No SMF-MPC recursive feasibility, stability, or six-state guarantee'],
        'gate_A':'blocked_for_output_feedback_SMF_MPC'
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',type=Path)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    s=json.dumps(certificate(args.root),indent=2,sort_keys=True,ensure_ascii=False)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(s)
    else:
        print(s,end='')

if __name__=='__main__':
    main()
