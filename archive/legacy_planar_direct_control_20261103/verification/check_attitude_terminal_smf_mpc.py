#!/usr/bin/env python3
"""Run221: exact-rational attitude-channel SMF + terminal-tube MPC pilot.

Frozen Euler phi/omega channel only. The full lateral/vertical, thrust-scheduled,
intermittent-position, six-state Gate A contract is NOT certified by this pilot.
The finite-grid nominal optimizer always carries a feasible shifted candidate.
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
from fractions import Fraction as Q
from pathlib import Path

H = J = Q(1, 50)
SIGMA = (Q(1, 200), Q(1, 100))  # phi, omega measurements EVERY tick
PHI_LIMIT, OMEGA_LIMIT, TAU_LIMIT = Q(9, 20), Q(2), Q(2, 25)
K = (-Q(8, 25), -Q(4, 25))
R = Q(23, 25)
E_PHI, E_S = Q(1, 100), Q(1, 25)  # |e_phi|, |e_omega+4e_phi|
ZF_PHI, ZF_S = Q(1, 20), Q(1, 5)  # nominal terminal transformed rectangle
N = 3
GRID = tuple(Q(k, 100) for k in (-6, -3, 0, 3, 6))
TARGET = Q(1, 25)
ZERO = Q(0)


def feedback(state):
    return K[0] * state[0] + K[1] * state[1]


def nominal_step(state, v):
    return state[0] + H * state[1], state[1] + (H / J) * v


def state_step(state, u):
    # Frozen physical angular Euler dynamics; zero angular process disturbance.
    return nominal_step(state, u)


def transformed(state):
    return state[0], state[1] + 4 * state[0]


def inside_terminal(z):
    phi, s = transformed(z)
    return abs(phi) <= ZF_PHI and abs(s) <= ZF_S


def inside_error(e):
    phi, s = transformed(e)
    return abs(phi) <= E_PHI and abs(s) <= E_S


def support_k_on_rectangle(phi_radius, s_radius):
    # K*(phi, s-4phi) = (K_phi-4K_omega)*phi + K_omega*s.
    return abs(K[0] - 4*K[1]) * phi_radius + abs(K[1]) * s_radius


def exact_certificate():
    # In transformed coordinates, M=A+BK becomes [[R,H],[0,R]].
    feedback_noise = abs(K[0])*SIGMA[0] + abs(K[1])*SIGMA[1]
    error_phi_image = R*E_PHI + H*E_S
    error_s_image = R*E_S + feedback_noise
    terminal_phi_image = R*ZF_PHI + H*ZF_S
    terminal_s_image = R*ZF_S
    error_omega_support = E_S + 4*E_PHI
    correction = support_k_on_rectangle(E_PHI, E_S) + feedback_noise
    tightened_input = TAU_LIMIT - correction
    terminal_input = support_k_on_rectangle(ZF_PHI, ZF_S)
    tightened_phi = PHI_LIMIT - E_PHI
    tightened_omega = OMEGA_LIMIT - error_omega_support
    assert error_phi_image <= E_PHI and error_s_image <= E_S
    assert terminal_phi_image <= ZF_PHI and terminal_s_image <= ZF_S
    assert tightened_input > 0 and terminal_input <= tightened_input
    assert ZF_PHI <= tightened_phi and ZF_S+4*ZF_PHI <= tightened_omega
    assert all(abs(v) <= tightened_input for v in GRID)
    return dict(error_image=[error_phi_image,error_s_image],
                error_radii=[E_PHI,E_S],terminal_image=[terminal_phi_image,terminal_s_image],
                terminal_radii=[ZF_PHI,ZF_S],
                feedback_noise=feedback_noise, correction=correction,
                terminal_nominal_input_support=terminal_input,
                nominal_input_limit=tightened_input,
                nominal_state_limits=[tightened_phi,tightened_omega],
                actual_state_limits=[PHI_LIMIT,OMEGA_LIMIT],actual_input_limit=TAU_LIMIT)


def nominal_admissible(z, cert):
    return abs(z[0]) <= cert['nominal_state_limits'][0] and abs(z[1]) <= cert['nominal_state_limits'][1]


def feasible(z, plan, cert=None):
    if cert is None: cert=exact_certificate()
    if len(plan) != N or not nominal_admissible(z,cert):return False
    for v in plan:
        if abs(v)>cert['nominal_input_limit']:return False
        z=nominal_step(z,v)
        if not nominal_admissible(z,cert):return False
    return inside_terminal(z)


def tail(z,plan):
    assert len(plan)==N
    terminal=z
    for v in plan:terminal=nominal_step(terminal,v)
    return tuple(plan[1:])+(feedback(terminal),)


def objective(z,plan):
    cost=ZERO
    for v in plan:
        z=nominal_step(z,v)
        cost+=Q(1000)*(z[0]-TARGET)**2+z[1]**2/Q(20)+v**2/Q(50)
    return cost


def optimize(z,fallback,cert):
    if not feasible(z,fallback,cert):
        raise ValueError('No certified feasible shifted candidate; fail closed')
    best=tuple(fallback)
    best_key=(objective(z,best),best)
    candidates=0
    for plan in itertools.product(GRID,repeat=N):
        if feasible(z,plan,cert):
            candidates+=1
            key=(objective(z,plan),plan)
            if key<best_key:best,best_key=plan,key
    return best,candidates


def intersect(a,b):
    out=max(a[0],b[0]),min(a[1],b[1])
    if out[0]>out[1]:raise ValueError('Inconsistent measurement and predicted SMF')
    return out


def smf_predict(posterior,u):
    phi,omega=posterior
    return (phi[0]+H*omega[0],phi[1]+H*omega[1]),(omega[0]+u,omega[1]+u)


def smf_observe(predicted,measurement):
    if measurement is None:return predicted
    return tuple(intersect(interval,(y-s,y+s)) for interval,y,s in zip(predicted,measurement,SIGMA))


def midpoint(posterior):
    return tuple((a+b)/2 for a,b in posterior)


def halfwidth(posterior):
    return tuple((b-a)/2 for a,b in posterior)


def inside_posterior(posterior,x):
    return all(a<=v<=b for (a,b),v in zip(posterior,x))


def certified_midpoint(posterior):
    if any(w>s for w,s in zip(halfwidth(posterior),SIGMA)):
        raise ValueError('SMF midpoint uncertainty exceeds fixed terminal tube contract')
    return midpoint(posterior)


def measurement_noise(k,case):
    # Deterministic admissible sensor noise, not stochastic confidence bounds.
    if case=='positive':return SIGMA
    if case=='negative':return tuple(-s for s in SIGMA)
    if case=='alternating':return tuple(s if (k+i)%2 else -s for i,s in enumerate(SIGMA))
    if case=='cycling':return tuple(s*Q(((3*k+2*i)%5)-2,2) for i,s in enumerate(SIGMA))
    raise ValueError(case)


def replay_case(x0,case,steps=48,policy="mpc"):
    cert=exact_certificate()
    z=(ZERO,ZERO)
    x=tuple(x0)
    prior=((-SIGMA[0],SIGMA[0]),(-SIGMA[1],SIGMA[1]))
    assert inside_posterior(prior,x) and inside_error(x)
    n0=measurement_noise(0,case)
    posterior=smf_observe(prior,tuple(xi+ni for xi,ni in zip(x,n0)))
    fallback=(ZERO,)*N
    assert feasible(z,fallback,cert)
    max_abs_phi=max_abs_omega=max_abs_tau=ZERO
    max_halfwidth=[ZERO,ZERO]
    error_max=[ZERO,ZERO]
    changes=received=0
    sum_tracking_squared=ZERO
    for k in range(steps):
        assert inside_posterior(posterior,x)
        hat=certified_midpoint(posterior)
        if policy=="mpc":
            plan,_=optimize(z,fallback,cert)
        elif policy=="terminal_only":
            plan=[]
            zz=z
            for _ in range(N):
                v=feedback(zz)
                plan.append(v)
                zz=nominal_step(zz,v)
            plan=tuple(plan)
        else:raise ValueError(policy)
        changes+=plan!=fallback
        assert feasible(z,plan,cert)
        u=plan[0]+feedback(tuple(hat[i]-z[i] for i in range(2)))
        assert abs(u)<=TAU_LIMIT
        x_next=state_step(x,u)
        z_next=nominal_step(z,plan[0])
        assert inside_error(tuple(x_next[i]-z_next[i] for i in range(2)))
        assert abs(x_next[0])<=PHI_LIMIT and abs(x_next[1])<=OMEGA_LIMIT
        predicted=smf_predict(posterior,u)
        noise=measurement_noise(k+1,case)
        y=tuple(x_next[i]+noise[i] for i in range(2))
        new_post=smf_observe(predicted,y)
        assert inside_posterior(new_post,x_next)
        next_fallback=tail(z,plan)
        assert feasible(z_next,next_fallback,cert)
        max_abs_phi=max(max_abs_phi,abs(x_next[0]));max_abs_omega=max(max_abs_omega,abs(x_next[1]))
        max_abs_tau=max(max_abs_tau,abs(u))
        for i,w in enumerate(halfwidth(new_post)):
            max_halfwidth[i]=max(max_halfwidth[i],w)
        for i,v in enumerate(tuple(x_next[i]-z_next[i] for i in range(2))):
            error_max[i]=max(error_max[i],abs(v))
        sum_tracking_squared+=(x_next[0]-TARGET)**2
        x,z,posterior,fallback=x_next,z_next,new_post,next_fallback
        received+=1
    return dict(steps=steps,measurement_packets=received,optimizer_changes=changes,
                constraint_violations=0,smf_coverage=steps+1,
                max_abs_phi=max_abs_phi,max_abs_omega=max_abs_omega,max_abs_tau=max_abs_tau,
                max_posterior_halfwidth=max_halfwidth,max_error_coordinates=error_max,
                tracking_rmse=math.sqrt(float(sum_tracking_squared/steps)))


def config_contract(root):
    config=json.loads((Path(root)/'configs/planar_baseline.json').read_text(),parse_float=Q)
    assert config['plant']['truth_semantics']=='defined_discrete_euler'
    assert Q(config['plant']['dt_s'])==H and Q(config['plant']['inertia_kg_m2'])==J
    assert Q(config['domain']['state_upper'][4])==PHI_LIMIT
    assert Q(config['domain']['state_upper'][5])==OMEGA_LIMIT
    assert Q(config['domain']['input_upper'][1])==TAU_LIMIT
    assert tuple(config['sensing']['always_observed_indices'])==(4,5)
    assert Q(config['sensing']['observed_noise_halfwidth']['phi'])==SIGMA[0]
    assert Q(config['sensing']['observed_noise_halfwidth']['omega'])==SIGMA[1]
    assert all(Q(config['plant']['external_process_halfwidth'][i])==0 for i in (4,5))
    return True


def run(root=None):
    if root is not None:config_contract(root)
    cert=exact_certificate()
    starts=list(itertools.product((-SIGMA[0],SIGMA[0]),(-SIGMA[1],SIGMA[1])))
    rows=[dict(start=list(x),noise_case=case,policy=policy,**replay_case(x,case,policy=policy))
          for policy in ('mpc','terminal_only') for x in starts
          for case in ('positive','negative','alternating','cycling')]
    mpc_rows=[r for r in rows if r['policy']=='mpc']
    baseline_rows=[r for r in rows if r['policy']=='terminal_only']
    compact_rows=[{k:r[k] for k in ('policy','noise_case','start','steps','tracking_rmse','optimizer_changes','smf_coverage','constraint_violations')} for r in rows]
    return dict(run='221',scope='isolated frozen 2-state UAV attitude channel; always-measured phi/omega; zero angular process disturbance',
                evidence='EXACT_RATIONAL_INVARIANCE_AND_SHIFT_PROOF_PLUS_FINITE_REPLAY',
                certificate=cert,episodes=len(rows),total_steps=sum(r['steps'] for r in rows),
                violations=sum(r['constraint_violations'] for r in rows),
                optimizer_changed_steps=sum(r['optimizer_changes'] for r in rows),
                mpc_mean_tracking_rmse=sum(r['tracking_rmse'] for r in mpc_rows)/len(mpc_rows),
                terminal_only_mean_tracking_rmse=sum(r['tracking_rmse'] for r in baseline_rows)/len(baseline_rows),
                worst_tracking_rmse=max(r['tracking_rmse'] for r in rows),
                max_abs_phi=max(r['max_abs_phi'] for r in rows),
                max_abs_omega=max(r['max_abs_omega'] for r in rows),
                max_abs_tau=max(r['max_abs_tau'] for r in rows),
                rows=compact_rows,gate_A='blocked',
                limitations=['This is NOT the 4-state lateral or six-state UAV terminal invariant set.',
                             'Position dropouts, thrust jumps, lateral/vertical disturbances and constraints are outside this certificate.',
                             'Finite-grid candidate optimization is not a continuous-QP optimum.',
                             'No wall-clock worst-case 20ms guarantee; no proof of target convergence.',
                             'If attitude measurement width exceeds sigma, controller fails closed rather than claiming safety.'])


def stringify(v):
    if isinstance(v,Q):return str(v)
    if isinstance(v,dict):return {k:stringify(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)):return [stringify(x) for x in v]
    return v


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=stringify(run(args.root))
    data=json.dumps(result,indent=2,ensure_ascii=False,sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(data)
    else:print(data,end='')


if __name__=='__main__':main()
