#!/usr/bin/env python3
"""Run246: exact necessary viability guard for Run245's reachable tick-30 state.

Frozen 4-state Euler and fixed thrust only. The adverse -R trajectory is
allowed by the configured residual contract. Post-30 torque is arbitrary,
even full-state/noncausal; this is NOT a general SMF-MPC impossibility.
"""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path
import check_four_state_tilt_authority as prior

H,J,T,R,U=prior.H,prior.J,prior.T,prior.R,prior.TAU_MAX
INIT=(prior.INIT['p'][0],prior.INIT['v'][0],
      prior.INIT['phi'][0],prior.INIT['omega'][0])
FUTURE=13


def reachable_corner():
    """Exact pitch/rate and rational sine enclosure of one true trajectory."""
    p=(INIT[0],)*2
    v=(INIT[1],)*2
    phi,omega=INIT[2:]
    rows=[(p,v,phi,omega)]
    for tau in prior.TORQUES:
        sl,su=prior.sin_bounds(phi)
        p_new=(p[0]+H*v[0],p[1]+H*v[1])
        v_new=(v[0]-H*(T*su+R),v[1]-H*(T*sl+R))
        phi,omega=phi+H*omega,omega+(H/J)*tau
        p,v=p_new,v_new
        rows.append((p,v,phi,omega))
    return rows


def pitch_bounds(phi,omega,j):
    # Euler phi uses omega BEFORE torque at each tick; j(j-1)/2, not j(j+1)/2.
    spread=H*(H/J)*U*j*(j-1)/2
    center=phi+H*j*omega
    return center-spread,center+spread


def verify(root=None):
    if root is not None:
        prior.verify(root)  # checks exact model, sensing, constraints, initial box
    assert len(prior.TORQUES)==30 and R==F(3246383,1600000)
    rows=reachable_corner()
    for p,v,phi,omega in rows:
        assert max(map(abs,p))<prior.P_MAX
        assert max(map(abs,v))<prior.V_MAX
        assert abs(phi)<prior.PHI_MAX and abs(omega)<prior.OMEGA_MAX
    p30,v30,phi30,omega30=rows[30]
    assert (phi30,omega30)==(F(1097,5000),F(-1,100))
    upper=v30[1]
    min_pitch=None
    for j in range(FUTURE):
        lo,hi=pitch_bounds(phi30,omega30,j)
        assert 0<lo<=hi<prior.PHI_MAX
        min_pitch=lo
        sin_lower=prior.sin_bounds(lo)[0]
        upper-=H*(R+T*sin_lower)
    margin=-prior.V_MAX-upper
    assert margin>0
    floor=-prior.V_MAX+(v30[1]-upper)
    assert v30[1]<floor
    return {
        'run':246,'base_run':245,
        'evidence':'EXACT_RATIONAL_REACHABLE_TERMINAL_NONVIABILITY',
        'model':'frozen four-state Euler; fixed thrust 9.81N; |tau|<=0.08Nm',
        'initial_corner':list(map(str,INIT)),
        'adverse_disturbance':'r_k=-3246383/1600000 m/s^2 for every tick',
        'first30_control':'Run245 fixed +U x12, -U x12, 0 x6',
        'tick30_position_enclosure':list(map(str,p30)),
        'tick30_velocity_enclosure':list(map(str,v30)),
        'tick30_phi_exact':str(phi30),
        'tick30_omega_exact':str(omega30),
        'future_pitch_lower_bound':'phi30+H*j*omega30-H*(H/J)*U*j*(j-1)/2',
        'last_future_pitch_lower_bound':str(min_pitch),
        'post30_torque_quantifier':'all admissible torque policies, including full-state/noncausal',
        'unavoidable_violation_tick':30+FUTURE,
        'velocity_upper_bound_at_tick43':str(upper),
        'necessary_velocity_floor_at_tick30':str(floor),
        'strict_velocity_violation_margin':str(margin),
        'one_reachable_terminal_state_outside_robust_viability_kernel':True,
        'all_terminal_states_nonviable':False,
        'general_smf_mpc_impossible':False,
        'recursive_feasibility_proved':False,
        'gate_A':'blocked'
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',type=Path)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    content=json.dumps(verify(args.root),ensure_ascii=False,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(content)
    else:
        print(content,end='')


if __name__=='__main__':
    main()
