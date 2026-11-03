#!/usr/bin/env python3
"""Run239: exact noisy-position SMF posterior for the Run238 two-point fiber.

Two constrained-zonotope branches are retained. This is a conditional
finite-horizon set estimate, not an invariant terminal set or MPC controller.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

H, T, J = F(1, 50), F(981, 100), F(1, 50)
R = F(47, 25) + F(243, 16000) * T
D = R + T * F(9, 20)**3 / 6
N = 15
NOISE = F(1, 50)
LIMITS = (F(5), F(3), F(9, 20), F(2))


def two_dim_generators():
    """Position/velocity generators; first is the initial velocity sign."""
    return [(N*H*H*D, H*D)] + [
        (H*H*R*(N-1-j), H*R) for j in range(N)
    ]


def branch_upper(sign: int, y: F, noise: F):
    """Exact maximum velocity for one initial sign and a noisy position strip.

    Primal: greedy fractional-knapsack witness, reducing p from the all-positive
    disturbance vertex in order of smallest lost velocity per reduced position.
    Dual: min_l sign*v0 + sum|vj-l*pj| + l*(y-sign*p0) + |l|*noise.
    Equality of exact rational primal and dual certifies the support optimum.
    """
    if sign not in (-1, 1) or noise < 0:
        raise ValueError('invalid sign/noise')
    (p0, v0), *gs = two_dim_generators()
    max_p = sign*p0 + sum((p for p, _ in gs), F(0))
    min_p = sign*p0 - sum((p for p, _ in gs), F(0))
    lower, upper = y-noise, y+noise
    if max_p < lower or min_p > upper:
        return None
    xi = [F(1)] * len(gs)
    excess = max(F(0), max_p-upper)
    for j in sorted(range(len(gs)), key=lambda i: gs[i][1]/gs[i][0] if gs[i][0] else F(10**30)):
        p, v = gs[j]
        if p == 0 or excess == 0:
            continue
        drop = min(F(2), excess/p)
        xi[j] -= drop
        excess -= p*drop
    assert excess == 0
    position = sign*p0 + sum((p*t for (p,_),t in zip(gs,xi)), F(0))
    velocity = sign*v0 + sum((v*t for (_,v),t in zip(gs,xi)), F(0))
    assert lower <= position <= upper and all(-1 <= t <= 1 for t in xi)
    candidates = {F(0)} | {v/p for p,v in gs if p}
    dual, lam = min((sign*v0 + sum((abs(v-l*p) for p,v in gs), F(0)) +
                     l*(y-sign*p0) + abs(l)*noise, l) for l in candidates)
    assert dual == velocity, (sign, y, noise, dual, velocity)
    return {'sign': sign, 'upper': velocity, 'dual_lambda': lam,
            'position_witness': position, 'disturbance_coefficients': xi}


def posterior_upper(y: F, noise: F = NOISE):
    witnesses = [w for sign in (-1,1) if (w := branch_upper(sign,y,noise)) is not None]
    if not witnesses:
        return None
    return max(witnesses, key=lambda w: w['upper'])


def verify(root=None):
    if root is not None:
        cfg=json.loads((Path(root)/'configs/planar_baseline.json').read_text())
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
        assert F(str(cfg['domain']['input_lower'][1]))<=0<=F(str(cfg['domain']['input_upper'][1]))
    assert H/J==1
    gs=two_dim_generators()
    assert len(gs)==16 and gs[-1][0]==0
    prior_p=sum((p for p,v in gs),F(0))
    prior_v=sum((v for p,v in gs),F(0))
    assert prior_p==F(78628341,800000000)
    assert prior_v==F(52180511,80000000)
    w=posterior_upper(F(0),NOISE)
    assert w is not None
    assert w['upper']==F(353411321,960000000)
    assert w['sign']==-1 and w['dual_lambda']==F(25,6)
    assert w['position_witness']==NOISE
    assert posterior_upper(F(0),F(0))['upper']==F(281453,1000000)
    assert w['upper']<prior_v
    assert posterior_upper(prior_p,NOISE)['upper']==prior_v
    assert gs[-1]==(F(0),H*R)
    future_n=N
    future_v=w['upper']+future_n*H*R
    future_p=NOISE+future_n*H*w['upper']+H*H*R*future_n*(future_n-1)/2
    assert future_p<LIMITS[0] and future_v<LIMITS[1]
    return {
        'run':239,
        'evidence':'EXACT_RATIONAL_TWO_BRANCH_NOISY_POSITION_POSTERIOR',
        'scope':'Run236 two-point initial fiber, fixed T=9.81, tau=0, 15 ticks, conditional on successful y_px=0 packet',
        'source_run238_prior_generators':len(gs),
        'posterior_representation':'union of two 16-variable constrained-zonotope branches (15 disturbances, 1 noise slack, fixed initial sign)',
        'position_measurement_y':'0',
        'position_noise_halfwidth':str(NOISE),
        'prior_position_halfwidth':str(prior_p),
        'prior_velocity_halfwidth':str(prior_v),
        'posterior_velocity_halfwidth_exact':str(w['upper']),
        'posterior_velocity_support_dual_lambda':str(w['dual_lambda']),
        'posterior_velocity_support_primal_initial_sign':w['sign'],
        'posterior_velocity_support_primal_position':str(w['position_witness']),
        'posterior_velocity_support_primal_disturbance_coefficients':[str(t) for t in w['disturbance_coefficients']],
        'noiseless_y_zero_velocity_halfwidth_exact':str(posterior_upper(F(0),F(0))['upper']),
        'unconditioned_velocity_halfwidth_at_observation_y_equal_prior_p':str(posterior_upper(prior_p,NOISE)['upper']),
        'last_disturbance_same_position_velocity_separation':str(2*H*R),
        'conditional_additional_15_tick_zero_torque_position_bound':str(future_p),
        'conditional_additional_15_tick_zero_torque_velocity_bound':str(future_v),
        'conditional_additional_15_tick_state_and_input_safe':True,
        'posterior_valid_for_all_measurements':False,
        'recursive_invariance_certified':False,
        'smf_mpc_closed_loop_certified':False,
        'gate_A':'blocked_for_output_feedback_SMF_MPC',
        'limitations':[
            'Posterior result conditional on y_px=0, not uniform across measurement outcomes',
            'Two-point initial fiber only; full initial prior and six-state coupling not covered',
            'Constrained-zonotope strip intersection is exact for frozen linear zero-angle subcase; no general nonlinear SMF update',
            'No MPC optimizer, output-feedback terminal invariant set, recursive feasibility, or 20ms worst-case guarantee'
        ]
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--root',type=Path)
    p.add_argument('--output',type=Path)
    a=p.parse_args()
    s=json.dumps(verify(a.root),indent=2,sort_keys=True,ensure_ascii=False)+'\n'
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(s)
    else:print(s,end='')


if __name__=='__main__':main()
