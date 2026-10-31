#!/usr/bin/env python3
"""Run227: exact obstructions to naive four-state terminal candidates.

Only frozen Run224 Euler/full-state feedback and Run208/210 independently
adversarial lateral residual. No RCI existence or output-feedback claim.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as Q
from pathlib import Path
from check_four_state_one_step_predecessor import (
    H, OMAX, R0, RT, TMIN, TMAX, VMAX, PHIMAX, PMAX,
    sine_bounds, config_contract,
)

A = Q(3, 20)       # 0.15 rad: two separated tilt modes
LAMBDA = Q(1, 2)  # seconds: coupled p+lambda*v corridor


def in_two_mode_candidate(x):
    """Nonempty coupled candidate, NOT asserted invariant.

    |p+lambda*v|<=5, |phi|>=0.15, phi*v>=0, and physical box X.
    """
    p,v,phi,omega=x
    return (abs(p)<=PMAX and abs(v)<=VMAX and abs(phi)<=PHIMAX
            and abs(omega)<=OMAX and abs(p+LAMBDA*v)<=PMAX
            and abs(phi)>=A and phi*v>=0)


def exact_bridge_obstruction(a=A):
    """Any nonempty RCI subset of {|phi|>=a} is impossible if 2a>h*omega_max.

    Invariance forbids crossing the angular gap in one step; a trajectory
    must stay in one sign component. An allowed fixed-sign disturbance then
    forces velocity out of [-3,3] in at most N steps for every causal policy.
    """
    if not Q(0)<a<=PHIMAX:
        raise ValueError('a outside certified positive-angle range')
    max_angle_jump=H*OMAX
    if 2*a<=max_angle_jump:
        return {'proved':False,'reason':'one-step crossing not excluded'}
    sin_lower=sine_bounds(a)[0]
    assert sin_lower>0
    drift=H*(R0+TMIN*(RT+sin_lower))
    n=(2*VMAX//drift)+1
    assert (n-1)*drift<=2*VMAX<n*drift
    return {'proved':True,'a':str(a),'max_one_step_angle_jump':str(max_angle_jump),
            'forbidden_mode_gap':str(2*a), 'adverse_velocity_drift_per_tick_lower':str(drift),
            'latest_strict_exit_tick':int(n),'velocity_overshoot_lower':str(n*drift-2*VMAX),
            'adversary':'r=-R(T) in positive-angle mode; r=+R(T) in negative-angle mode'}


def one_step_candidate_counterexample():
    """At (0,0,a,0), r=-R(T) makes v+<0 while phi+=a for ALL controls."""
    x=(Q(0),Q(0),A,Q(0))
    assert in_two_mode_candidate(x)
    upper_next_v=-H*(R0+TMIN*(sine_bounds(A)[0]+RT))
    assert upper_next_v<0
    return {'state':[str(z) for z in x], 'adversary':'r=-R(T)',
            'all_legal_inputs_next_phi':str(A),
            'all_legal_inputs_next_v_upper':str(upper_next_v),
            'violated_constraint':'phi*v>=0 (positive phi, negative next v)',
            'excluded_from_Pre_C':True}


def cartesian_box_obstruction():
    """No nonempty axis-aligned P x V x Phi x Omega box can be RCI.

    Position endpoints force V={0}; two allowed residual extremes force
    distinct next velocities, so neither control can keep V={0}.
    """
    velocity_successor_separation_min=2*H*(R0+RT*TMIN)
    assert velocity_successor_separation_min>0
    return {'proved':True,'forced_velocity_interval':'[0,0]',
            'min_successor_velocity_separation':str(velocity_successor_separation_min),
            'reason':'p+=p+h*v at both position endpoints; r=+/-R(T) prevents V={0}'}


def verify(root=None):
    if root is not None: config_contract(root)
    plus=(Q(0),VMAX,A,Q(0)); minus=(Q(0),-VMAX,-A,Q(0))
    assert in_two_mode_candidate(plus) and in_two_mode_candidate(minus)
    bridge=exact_bridge_obstruction()
    assert bridge['proved'] and bridge['latest_strict_exit_tick']==112
    return {'run':'227','base_main':'4817403c2ac4dae7c1abe348f0096b3e21bcf5ff',
            'model':'Run224 frozen four-state Euler; Run208/210 independent lateral residual',
            'candidate':'|p+v/2|<=5, |phi|>=3/20, phi*v>=0, x in X',
            'candidate_nonempty_witnesses':[[str(z) for z in plus],[str(z) for z in minus]],
            'candidate_one_step_exclusion':one_step_candidate_counterexample(),
            'no_two_disconnected_tilt_bands':bridge,
            'no_axis_aligned_terminal_box':cartesian_box_obstruction(),
            'global_necessary_condition':'Every nonempty four-state RCI C subset X intersects |phi|<=1/50 rad',
            'certificate':'EXACT_RATIONAL_KINEMATIC_GAP_AND_ADVERSARIAL_DRIFT',
            'gate_A':'blocked',
            'limitations':['These are necessary geometry restrictions and explicit negative candidate results; no nonempty four-state RCI constructed.',
                           'Full-state feedback and independently adversarial residual, not output-feedback SMF.',
                           'No four-state MPC recursive feasibility, Lyapunov stability, six-state safety or 20ms bound.']}


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
    s=json.dumps(verify(a.root),indent=2,sort_keys=True,ensure_ascii=False)+'\n'
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    else:print(s,end='')

if __name__=='__main__':main()
