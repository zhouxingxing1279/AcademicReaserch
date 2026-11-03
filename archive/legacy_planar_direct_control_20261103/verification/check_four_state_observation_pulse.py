#!/usr/bin/env python3
"""Run241: exact rational one-packet, observation-dependent torque pulse.

Frozen Euler p,v,phi,omega; two-point Run236 fiber, fixed thrust 9.81 N.
At a successful noisy position packet after n=5/10/15 zero-torque ticks,
commit to a 15-tick torque schedule tau_j = gain*y*shape_j. This is a
finite-horizon shared-information backup, NOT a recursive SMF/MPC terminal.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

H, J, T = F(1, 50), F(1, 50), F(981, 100)
R = F(47, 25) + F(243, 16000) * T
D = R + T * F(9, 20)**3 / 6
NOISE = F(1, 50)
GAIN = F(2, 3)  # Nm per metre of observed position
SHAPE = (1,)*3 + (-1,)*6 + (1,)*3 + (0,)*3
LIMITS = (F(5), F(3), F(9, 20), F(2))
TAU_MAX = F(2, 25)
MODES = (5, 10, 15)


def prior_generators(n):
    if n not in MODES:
        raise ValueError('unsupported packet mode')
    return [(n*H*H*D, H*D)] + [(H*H*R*(n-1-j), H*R) for j in range(n)]


def angle_coefficients():
    """phi_j=c_j*y and omega_j=d_j*y, with Euler update ordering."""
    phi = omega = F(0)
    angles, rates = [], []
    for a in SHAPE:
        angles.append(phi)
        rates.append(omega)
        phi, omega = phi + H*omega, omega + H/J*GAIN*a
    assert phi == omega == 0
    return angles + [phi], rates + [omega]


def linear_effect(t, angles):
    """Linearized sin(phi) feedback shifts: v -= alpha*y, p -= beta*y."""
    alpha = H*T*sum(angles[:t], F(0))
    beta = H*H*T*sum(((t-1-j)*angles[j] for j in range(t)), F(0))
    return alpha, beta


def taylor_error(t, angles, y_abs):
    # Rigorous for every real z: |sin(z)-z| <= |z|^3/6.
    ev = H*T*sum((abs(c)**3 for c in angles[:t]), F(0))*y_abs**3/6
    ep = H*H*T*sum(((t-1-j)*abs(angles[j])**3 for j in range(t)), F(0))*y_abs**3/6
    return ep, ev


def bounds(n, t):
    """Universal exact-rational outer bounds over all prior signs, r and noise."""
    if t < 0 or t > len(SHAPE):
        raise ValueError('recovery horizon out of range')
    gs = prior_generators(n)
    angles, rates = angle_coefficients()
    y_abs = sum((abs(p) for p, _ in gs), F(0)) + NOISE
    alpha, beta = linear_effect(t, angles)
    ep, ev = taylor_error(t, angles, y_abs)
    future_p = H*H*R*t*(t-1)/2
    future_v = t*H*R
    # Exact support of correlated (p_n,v_n) zonotope and independent n_y.
    baseline_p = sum((abs(p+t*H*v) for p,v in gs), F(0)) + future_p
    baseline_v = sum((abs(v) for p,v in gs), F(0)) + future_v
    pulse_p = sum((abs((1-beta)*p+t*H*v) for p,v in gs), F(0)) + abs(beta)*NOISE + future_p + ep
    pulse_v = sum((abs(v-alpha*p) for p,v in gs), F(0)) + abs(alpha)*NOISE + future_v + ev
    # Independent, simple all-tick outer bound: |sin(phi)|<=|phi|.
    safe_p = baseline_p + H*H*T*y_abs*sum(((t-1-j)*abs(angles[j]) for j in range(t)), F(0))
    safe_v = baseline_v + H*T*y_abs*sum((abs(c) for c in angles[:t]), F(0))
    return {'y_abs':y_abs,'alpha':alpha,'beta':beta,'taylor_p':ep,'taylor_v':ev,
            'baseline_p':baseline_p,'baseline_v':baseline_v,'pulse_p':pulse_p,'pulse_v':pulse_v,
            'safe_p':safe_p,'safe_v':safe_v,'phi':abs(angles[t])*y_abs,'omega':abs(rates[t])*y_abs,
            'torque':GAIN*y_abs*abs(SHAPE[t]) if t < len(SHAPE) else F(0)}


def verify(root=None):
    if root is not None:
        cfg = json.loads((Path(root)/'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics']=='defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s']))==H
        assert F(str(cfg['plant']['inertia_kg_m2']))==J
        assert F(str(cfg['sensing']['observed_noise_halfwidth']['px']))==NOISE
        assert cfg['sensing']['position_period_ticks']==5
        assert cfg['sensing']['max_consecutive_missed_packets']==2
        assert cfg['sensing']['position_indices']==[0,1]
        assert cfg['sensing']['always_observed_indices']==[4,5]
        assert tuple(F(str(cfg['domain']['state_upper'][i])) for i in (0,2,4,5))==LIMITS
        assert F(str(cfg['domain']['input_lower'][0]))<=T<=F(str(cfg['domain']['input_upper'][0]))
        assert F(str(cfg['domain']['input_lower'][1]))<=-TAU_MAX
        assert F(str(cfg['domain']['input_upper'][1]))>=TAU_MAX
    angles, rates = angle_coefficients()
    assert len(angles)==len(SHAPE)+1
    modes = []
    for n in MODES:
        all_ticks = [bounds(n,t) for t in range(len(SHAPE)+1)]
        assert all(x['safe_p'] < LIMITS[0] and x['safe_v'] < LIMITS[1] and
                   x['phi'] < LIMITS[2] and x['omega'] < LIMITS[3] and
                   x['torque'] <= TAU_MAX for x in all_ticks)
        final = all_ticks[-1]
        assert final['phi']==final['omega']==0
        assert (final['pulse_p']<final['baseline_p'])==(n in (10,15))
        assert (final['pulse_v']<final['baseline_v'])==(n in (10,15))
        modes.append({'packet_after_ticks':n,'max_observation_m':str(final['y_abs']),
                      'baseline_terminal_position_m':str(final['baseline_p']),
                      'pulse_terminal_position_bound_m':str(final['pulse_p']),
                      'baseline_terminal_speed_m_s':str(final['baseline_v']),
                      'pulse_terminal_speed_bound_m_s':str(final['pulse_v']),
                      'position_improvement_lower_m':str(final['baseline_p']-final['pulse_p']),
                      'speed_improvement_lower_m_s':str(final['baseline_v']-final['pulse_v']),
                      'strict_both_improved':n in (10,15),
                      'all_intermediate_hard_constraints':True,
                      'terminal_angle_and_rate_exactly_zero':True})
    return {'run':241,'evidence':'EXACT_RATIONAL_OBSERVATION_CONDITIONED_FINITE_HORIZON_OUTER_BOUND',
            'scope':'Run236 two-point fiber; fixed thrust, frozen four-state Euler, all bounded residual/noise histories; one successful packet after 5/10/15 ticks',
            'policy':'tau_j=(2/3)*y_px*shape_j, shape=[+1]*3+[-1]*6+[+1]*3+[0]*3, committed open-loop after the packet',
            'shape':list(SHAPE),'gain_Nm_per_m':str(GAIN),'packet_noise_halfwidth_m':str(NOISE),
            'residual_halfwidth_m_s2':str(R),'modes':modes,
            'sine_remainder':'|sin(z)-z|<=|z|^3/6; global measurement magnitude bounds the remainder',
            'five_tick_noise_dominance_negative_result':True,
            'recursive_invariance_certified':False,'smf_mpc_closed_loop_certified':False,
            'gate_A':'blocked_for_output_feedback_SMF_MPC',
            'limitations':['One successful packet and one committed recovery pulse only; not a repeated causal mode policy',
                           'Two-point initial fiber, not the full initial prior or general CZ posterior',
                           'Robust terminal bounds are conservative outer bounds, not exact nonlinear supports',
                           'No recursive information-state invariant set, MPC optimizer, six-state safety or 20ms timing certificate']}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--root',type=Path)
    p.add_argument('--output',type=Path)
    a=p.parse_args()
    s=json.dumps(verify(a.root),sort_keys=True,indent=2,ensure_ascii=False)+'\n'
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(s)
    else:print(s,end='')

if __name__=='__main__':main()
