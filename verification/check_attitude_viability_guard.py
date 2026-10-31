#!/usr/bin/env python3
"""Run210: exact necessary attitude viability guard on reachable SMF rollouts.

The guard checks a *necessary* condition for existence of future bounded
controls, not a controlled invariant set or a sufficient safety certificate.
It is combined with Run208's independent, finite-horizon backup audit.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as Q
from pathlib import Path
import check_reachable_smf_backup_rollout as m
import check_two_stage_causal_backup as prior

Z=Q(0)

def attitude_min(phi, omega, n):
    """Exact minimal future angle at step n under all admissible torques."""
    assert n>=1
    return phi+n*m.H*omega-(m.H*m.H/m.J)*m.UMAX*n*(n-1)/2

def attitude_max(phi, omega, n):
    assert n>=1
    return phi+n*m.H*omega+(m.H*m.H/m.J)*m.UMAX*n*(n-1)/2

def necessary_at_state(box, horizon):
    """Check a necessary viability condition for every point in an outer box.

    If false, at least one state in the box is nonviable, but this point may
    be spurious when the box is an overapproximation. In the tested attitude
    channel the posterior is singleton, avoiding this ambiguity.
    """
    assert horizon>=1
    phi,omega=box[2],box[3]
    for n in range(1,horizon+1):
        if attitude_min(phi[1],omega[1],n)>m.LIMITS[2]:return False,n,'upper'
        if attitude_max(phi[0],omega[0],n)<-m.LIMITS[2]:return False,n,'lower'
    return True,None,None

def guard_interval(box, horizon):
    """Necessary (not sufficient) current torque interval for H-step viability.

    Same u0 must work for both signs, but later controls may be chosen
    differently for each horizon and each initial state. Thus nonempty does
    not imply an actual viable causal policy.
    """
    assert horizon>=2
    phi,omega=box[2],box[3]
    lo,hi=-m.UMAX,m.UMAX
    c=m.H*m.H/m.J
    for n in range(1,horizon+1):
        if n==1:
            if phi[1]+m.H*omega[1]>m.LIMITS[2] or phi[0]+m.H*omega[0]<-m.LIMITS[2]:
                return Q(1),Q(0)
            continue
        d=c*(n-1)
        free=c*m.UMAX*(n-1)*(n-2)/2
        upper=(m.LIMITS[2]-phi[1]-n*m.H*omega[1]+free)/d
        lower=(-m.LIMITS[2]-phi[0]-n*m.H*omega[0]-free)/d
        lo=max(lo,lower);hi=min(hi,upper)
    return lo,hi

def projected_guarded_torque(box,t,horizon):
    backup=prior.two_stage_audit(box,t)
    if not backup['feasible']:return None,'two_stage_refusal'
    gl,gh=guard_interval(box,horizon)
    lo=max(gl,Q(backup['lower']));hi=min(gh,Q(backup['upper']))
    if lo>hi:return None,'necessary_viability_guard_refusal'
    return max(lo,min(hi,m.proposed(box))),'admitted'

def replay(scenario='alternating_high',steps=100,horizon=6,guarded=False,brake_gain=Z):
    """Actual reachable deterministic rollout, preserving Run208 SMF contract."""
    x=(Z,)*4;box=m.initial_box();prev_p=box[0];accels=[]
    accepted=0;first_refusal=None;first_warning=None;first_next_warning=None
    interventions=0;max_angle=Z;max_rate=Z
    trace=[]
    for k in range(steps):
        assert all(a<=z<=b for (a,b),z in zip(box,x))
        assert all(abs(z)<=lim for z,lim in zip(x,m.LIMITS))
        t=m.thrust(scenario,k)
        baseline,basecert=prior.two_stage_filter(box,t)
        if baseline is None:
            first_refusal={'tick':k+1,'cause':'two_stage_refusal'}
            break
        now_ok,n,side=necessary_at_state(box,horizon-1)
        if not now_ok and first_warning is None:
            first_warning={'tick':k+1,'unavoidable_by':k+n,'side':side}
        baseline_next=m.predict(box,t,baseline)
        next_ok,nn,ns=necessary_at_state(baseline_next,horizon-1)
        if not next_ok and first_next_warning is None:
            first_next_warning={'tick':k+1,'unavoidable_by':k+1+nn,'side':ns}
        if guarded:
            u,cause=projected_guarded_torque(box,t,horizon)
            if u is None:
                first_refusal={'tick':k+1,'cause':cause};break
        else:u=baseline
        if u is not None and brake_gain:
            target=m.proposed(box)-brake_gain*m.mid(box[3])
            interval=guard_interval(box,horizon) if guarded else (-m.UMAX,m.UMAX)
            lo=max(Q(basecert['lower']),interval[0]);hi=min(Q(basecert['upper']),interval[1])
            assert lo<=hi
            u=max(lo,min(hi,target))
        interventions+=u!=baseline
        if k+1 in (1,30,60,85,90,91,92,93,94,95,96,100):
            trace.append({'tick':k+1,'phi':float(x[2]),'omega':float(x[3]),
                          'torque':float(u),'baseline_torque':float(baseline),
                          'baseline_next_viable_necessary':next_ok})
        old_phi=box[2]
        accels.append(m.add(m.scale(old_phi,-t),(-m.rad(t),m.rad(t))))
        x=m.step(x,t,u,m.residual(scenario,k,t))
        box=m.predict(box,t,u)
        packet=(k+1)%15==0
        box=m.observe(box,x,packet,m.measurement_noise(scenario,k))
        if packet:
            box=(box[0],m.intersect(box[1],m.velocity_from_packets(prev_p,box[0],accels)),box[2],box[3])
            prev_p=box[0];accels=[]
        assert all(a<=z<=b for (a,b),z in zip(box,x))
        assert all(abs(z)<=lim for z,lim in zip(x,m.LIMITS))
        accepted+=1
        max_angle=max(max_angle,abs(x[2]));max_rate=max(max_rate,abs(x[3]))
    return {'scenario':scenario,'horizon':horizon,'guarded':guarded,'brake_gain':str(brake_gain),
            'accepted_ticks':accepted,'first_refusal':first_refusal,
            'first_state_nonviability_warning':first_warning,
            'first_baseline_next_state_warning':first_next_warning,
            'guard_interventions':interventions,'max_abs_phi':float(max_angle),
            'max_abs_omega':float(max_rate),'trace':trace}

def run():
    rows=[]
    for scenario in ('alternating_high','positive_high','switch_positive'):
        rows.append({'scenario':scenario,
                     'run208':replay(scenario,steps=200,horizon=8),
                     'braking_guard':replay(scenario,steps=200,horizon=8,guarded=True,brake_gain=Q(1,5))})
    guard_only=replay('alternating_high',steps=100,horizon=8,guarded=True)
    return {'run':'210','scope':'four-state Euler proxy, exact rational decisions, deterministic reachable traces',
            'evidence':'NECESSARY_ATTITUDE_VIABILITY_FILTER_PLUS_FINITE_BACKUP',
            'guard_only_alternating_high':{'accepted_ticks':guard_only['accepted_ticks'],
                'first_refusal':guard_only['first_refusal']},
            'rows':rows,'gate_A':'blocked',
            'caveats':['Necessary viability is not sufficient for a safe policy or recursive feasibility',
                       'Outer-box endpoints can be spurious if posterior is not singleton',
                       'Run208 backup certificate is only finite horizon',
                       'No MPC optimizer, no terminal invariant set, no full six-state model']}

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path)
    args=p.parse_args();s=json.dumps(run(),indent=2,ensure_ascii=False)+'\n'
    if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(s)
    else:print(s,end='')
if __name__=='__main__':main()
