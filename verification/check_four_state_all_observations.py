#!/usr/bin/env python3
"""Run240: exact all-observation velocity interval for the Run238 two-point fiber.

Only fixed T=9.81, zero torque, frozen Euler lateral p/v, bounded independent
residuals and one noisy successful position packet after n=5/10/15 ticks.
This is not a recursive information-state RCI or an MPC controller.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

H, T, J = F(1, 50), F(981, 100), F(1, 50)
R = F(47, 25) + F(243, 16000)*T
D = R + T*F(9,20)**3/6
NOISE = F(1,50)
LIMITS = (F(5),F(3),F(9,20),F(2))
MODES = (5,10,15)


def generators(n):
    if n<1: raise ValueError('n must be positive')
    return [(n*H*H*D,H*D)] + [(H*H*R*(n-1-j),H*R) for j in range(n)]


def branch_upper(n,sign,y,noise=NOISE):
    """Exact upper support for one initial sign; primal/dual verified."""
    if sign not in (-1,1) or noise<0: raise ValueError('invalid sign/noise')
    (p0,v0),*gs=generators(n)
    total_p=sum((p for p,v in gs),F(0))
    min_p,max_p=sign*p0-total_p,sign*p0+total_p
    if y+noise<min_p or y-noise>max_p:return None
    xi=[F(1)]*len(gs)
    excess=max(F(0),max_p-(y+noise))
    for j in sorted(range(len(gs)),key=lambda i:gs[i][1]/gs[i][0] if gs[i][0] else F(10**20)):
        p,v=gs[j]
        if not p or not excess:continue
        drop=min(F(2),excess/p)
        xi[j]-=drop
        excess-=p*drop
    assert excess==0
    p=sign*p0+sum((a*x for (a,b),x in zip(gs,xi)),F(0))
    v=sign*v0+sum((b*x for (a,b),x in zip(gs,xi)),F(0))
    assert y-noise<=p<=y+noise
    assert all(-1<=x<=1 for x in xi)
    candidates={F(0)}|{b/a for a,b in gs if a}
    dual,lam=min((sign*v0+sum((abs(b-l*a) for a,b in gs),F(0)) + l*(y-sign*p0)+abs(l)*noise,l) for l in candidates)
    assert dual==v,(n,sign,y,dual,v)
    return {'upper':v,'sign':sign,'lambda':lam,'position':p,'xi':xi}


def upper(n,y):
    ws=[w for s in (-1,1) if (w:=branch_upper(n,s,y)) is not None]
    return max(ws,key=lambda w:w['upper']) if ws else None


def interval(n,y):
    hi=upper(n,y)
    lo_reflected=upper(n,-y)
    if hi is None or lo_reflected is None: return None
    lo=-lo_reflected['upper']
    assert lo<=hi['upper']
    return {'lower':lo,'upper':hi['upper'],'radius':(hi['upper']-lo)/2,'center':(hi['upper']+lo)/2,
            'upper_sign':hi['sign'],'lower_sign':-lo_reflected['sign']}


def knots(n):
    """All support affine breakpoints, including branch feasibility boundaries.

    On each open interval between knots, every feasible branch upper support
    is affine; max of affine supports is convex, so posterior interval radius
    (sum of two upper envelopes)/2 has no strict interior maximum.
    """
    (p0,v0),*gs=generators(n)
    total_p=sum((p for p,v in gs),F(0))
    order=sorted((j for j,(p,v) in enumerate(gs) if p),key=lambda i:gs[i][1]/gs[i][0])
    ks=set()
    for sign in (-1,1):
        max_p=sign*p0+total_p
        min_p=sign*p0-total_p
        ys=[min_p-NOISE,max_p+NOISE,max_p-NOISE]
        remaining=max_p
        for j in order:
            remaining-=2*gs[j][0]
            ys.append(remaining-NOISE)
        for y in ys:
            ks.add(y);ks.add(-y)
    return sorted(ks)


def mode_certificate(n):
    prior_p=sum((p for p,v in generators(n)),F(0))
    prior_v=sum((v for p,v in generators(n)),F(0))
    ks=knots(n)
    values=[(interval(n,y)['radius'],y) for y in ks if interval(n,y) is not None]
    max_radius,y_star=max(values)
    assert max_radius<=prior_v
    assert (max_radius==prior_v)==(n==5)
    assert max_radius==interval(n,F(0))['radius']
    assert interval(n,F(0)) is not None
    # Independent last disturbance r_(n-1) never changes p_n, but spans +/-hR in v_n.
    assert max_radius>=H*R
    assert interval(n,prior_p)['upper']==prior_v
    # Any admissible posterior velocity belongs to the unconditional [-prior_v,+prior_v].
    # Continue with a shared zero-torque 15-tick backup, ignoring the packet.
    additional=15
    future_v=prior_v+additional*H*R
    future_p=prior_p+additional*H*prior_v+H*H*R*additional*(additional-1)/2
    assert future_v<LIMITS[1] and future_p<LIMITS[0]
    return {'ticks':n,'candidate_knot_count':len(ks),'prior_position_radius':str(prior_p),
            'prior_velocity_radius':str(prior_v),'max_posterior_velocity_interval_radius':str(max_radius),
            'max_radius_observation':str(y_star),'zero_observation_interval_radius':str(interval(n,F(0))['radius']),
            'relative_radius_reduction':str((prior_v-max_radius)/prior_v),
            'uniform_strict_radius_reduction':max_radius<prior_v,
            'unchanged_absolute_velocity_upper_at_y_prior_p':str(interval(n,prior_p)['upper']),
            'last_disturbance_irreducible_radius':str(H*R),
            'unconditional_next_15_zero_torque_position_bound':str(future_p),
            'unconditional_next_15_zero_torque_velocity_bound':str(future_v),
            'next_15_state_and_input_safe':True}


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
    ms=[mode_certificate(n) for n in MODES]
    return {'run':240,'evidence':'EXACT_RATIONAL_ALL_SUCCESS_OBSERVATIONS_TWO_POINT_FIBER',
            'scope':'Run236 two-point initial fiber; frozen Euler p/v, fixed T=9.81 N, tau=0, independent bounded r; successful noisy position packet at tick 5/10/15',
            'noise_halfwidth':str(NOISE),'residual_halfwidth':str(R),
            'method':'Exact per-branch fractional-knapsack primal/dual support; exhaustive rational piecewise-affine knot envelope over all feasible real observations',
            'modes':ms,'all_observation_uniform_interval_radius_reduction_only_for_10_15_ticks':True,
            'five_tick_observation_no_uniform_radius_reduction':True,
            'no_uniform_absolute_velocity_bound_reduction':True,
            'every_success_observation_followed_by_15_zero_torque_ticks_safe_for_this_initial_fiber':True,
            'recursive_invariance_certified':False,'smf_mpc_closed_loop_certified':False,
            'full_prior_certified':False,'gate_A':'blocked_for_output_feedback_SMF_MPC'}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--root',type=Path)
    p.add_argument('--output',type=Path)
    args=p.parse_args()
    s=json.dumps(verify(args.root),sort_keys=True,indent=2,ensure_ascii=False)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(s)
    else:print(s,end='')

if __name__=='__main__':main()
