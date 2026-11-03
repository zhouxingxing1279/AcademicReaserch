#!/usr/bin/env python3
"""Run208: exact two-stage thrust-contingent causal backup for the four-state proxy.

At k, choose u0 using current posterior box and visible T0. At k+1, after
T1 is observed (but before the next disturbance), choose u1(T1), affine in
T1, then set u2=u3=u4=0. All possible next measurements are covered by
resetting to the entire predicted box B+, rather than exploiting the packet.
This is a ONE-STEP guarantee of a four-tick backup, not recursive feasibility.
"""
from __future__ import annotations
import argparse
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path
import check_reachable_smf_backup_rollout as m

Z=Q(0)

def clip_linear(interval,a,d):
    """Intersect exact u0 interval with a*u0 <= d."""
    lo,hi=interval
    if a>0:hi=min(hi,d/a)
    elif a<0:lo=max(lo,d/a)
    elif d<0:return Q(1),Q(0)
    return lo,hi

def endpoint_rows(predicted,t1):
    """Rows (a,b,d): a*u0+b*u1 <= d for a given endpoint T1.

    predicted is B+(u0=0). The u0 coefficient is exactly e_omega,
    because H/J=1. Full predicted-box reset discards all correlations.
    """
    x,rad=m.box_center_radius(predicted)
    u0coef=(Z,Z,Z,m.H/m.J)
    rows={(Z,Q(1)):m.UMAX,(Z,-Q(1)):m.UMAX}
    raw=0
    for future in itertools.product((m.TMIN,m.TMAX),repeat=3):
        center=x; c0=u0coef;c1=(Z,)*4
        generators=tuple(tuple(rad[i] if i==j else Z for i in range(4)) for j in range(4))
        for k,t in enumerate((t1,)+future):
            center=m.step(center,t,Z)
            c0=m.step(c0,t,Z)
            c1=m.step(c1,t,Q(1) if k==0 else Z)
            generators=tuple(m.step(g,t,Z) for g in generators)+((Z,m.H*m.rad(t),Z,Z),)
            for i in range(4):
                spread=sum(abs(g[i]) for g in generators)
                for sign in (-1,1):
                    a=sign*c0[i];b=sign*c1[i]
                    d=m.LIMITS[i]-spread-sign*center[i]
                    key=(a,b)
                    rows[key]=min(rows.get(key,d),d)
                    raw+=1
    return [(a,b,d) for (a,b),d in rows.items()],raw

def project_u1(rows,interval):
    """Exact Fourier-Motzkin elimination of u1, with slope deduplication."""
    lower={};upper={}
    for a,b,d in rows:
        if b==0:
            interval=clip_linear(interval,a,d)
        else:
            slope=-a/b; intercept=d/b
            if b>0:upper[slope]=min(upper.get(slope,intercept),intercept)
            else:lower[slope]=max(lower.get(slope,intercept),intercept)
    if not lower or not upper:raise AssertionError('missing bounded u1')
    comparisons=0
    for ls,li in lower.items():
        for us,ui in upper.items():
            interval=clip_linear(interval,ls-us,ui-li)
            comparisons+=1
    return interval,{'lower_lines':len(lower),'upper_lines':len(upper),'pairwise':comparisons}

def endpoint_u1(rows,u0):
    lo=-m.UMAX;hi=m.UMAX
    for a,b,d in rows:
        rhs=d-a*u0
        if b>0:hi=min(hi,rhs/b)
        elif b<0:lo=max(lo,rhs/b)
        elif rhs<0:return None
    return (lo,hi) if lo<=hi else None

def two_stage_audit(box,t0):
    """Exact projected u0 interval for affine u1(T1) at thrust endpoints."""
    assert m.TMIN<=t0<=m.TMAX
    x,r=m.box_center_radius(box)
    if any(abs(a)+b>lim for a,b,lim in zip(x,r,m.LIMITS)):
        return {'feasible':False,'reason':'current_outer_box_outside_hard_limits'}
    pred=m.predict(box,t0,Z)
    xp,rp=m.box_center_radius(pred)
    interval=(-m.UMAX,m.UMAX)
    # The first physical step is safe for every current disturbance.
    for i in range(4):
        coef=Q(1) if i==3 else Z
        interval=m.constrain(interval,xp[i],coef,m.LIMITS[i]-rp[i])
    details=[]
    for t1 in (m.TMIN,m.TMAX):
        rows,raw=endpoint_rows(pred,t1)
        interval,meta=project_u1(rows,interval)
        details.append({'t1':str(t1),'raw_signed_inequalities':raw,
                        'unique_linear_rows':len(rows),**meta})
    feasible=interval[0]<=interval[1]
    return {'feasible':feasible,
            'reason':'two_stage_thrust_contingent_backup' if feasible else 'empty_two_stage_interval',
            'lower':str(interval[0]),'upper':str(interval[1]),
            'endpoint_details':details,
            'future_policy':'u1(T1) linear interpolation of feasible endpoint controls; u2..u4=0',
            'measurement_policy':'ignores next measurement; all posterior subsets of B+ covered'}

def choose_endpoint_u1(box,t0,u0,t1):
    pred=m.predict(box,t0,Z)
    rows,_=endpoint_rows(pred,t1)
    allowed=endpoint_u1(rows,u0)
    if allowed is None:return None
    lo,hi=allowed
    return max(lo,min(hi,Z))

def contingent_u1(box,t0,u0,t1):
    """A causal affine-in-visible-thrust control with no packet anticipation."""
    assert m.TMIN<=t1<=m.TMAX
    lo=choose_endpoint_u1(box,t0,u0,m.TMIN)
    hi=choose_endpoint_u1(box,t0,u0,m.TMAX)
    if lo is None or hi is None:return None
    weight=(t1-m.TMIN)/(m.TMAX-m.TMIN)
    return lo+(hi-lo)*weight

def two_stage_filter(box,t0):
    cert=two_stage_audit(box,t0)
    if not cert['feasible']:return None,cert
    desired=m.proposed(box)
    return max(Q(cert['lower']),min(Q(cert['upper']),desired)),cert

def verify_next_backup(box,t0,u0,t1):
    next_box=m.predict(box,t0,u0)
    u1=contingent_u1(box,t0,u0,t1)
    if u1 is None:return False
    cert=m.backup_audit(next_box,t1)
    return cert['feasible'] and Q(cert['lower'])<=u1<=Q(cert['upper'])

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path)
    a=p.parse_args();data=json.dumps(run(),indent=2,ensure_ascii=False)+'\n'
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(data)
    else:print(data,end='')

def zero_bridge_audit(box,t0):
    """Equivalent to Run207's one-step zero-torque bridge, exact."""
    x,r=m.box_center_radius(box)
    if any(abs(a)+b>lim for a,b,lim in zip(x,r,m.LIMITS)):
        return {'feasible':False,'reason':'current_outer_box_outside_hard_limits'}
    pred=m.predict(box,t0,Z);xp,rp=m.box_center_radius(pred)
    interval=(-m.UMAX,m.UMAX)
    for i in range(4):
        interval=m.constrain(interval,xp[i],Q(1) if i==3 else Z,m.LIMITS[i]-rp[i])
    for t1 in (m.TMIN,m.TMAX):
        rows,_=endpoint_rows(pred,t1)
        for a,b,d in rows:
            if (a,b)==(Z,Q(1)) or (a,b)==(Z,-Q(1)):continue
            interval=clip_linear(interval,a,d)
    return {'feasible':interval[0]<=interval[1],'lower':str(interval[0]),'upper':str(interval[1])}

def rollout_filter(scenario,method='two_stage',steps=100,capture_tick=None):
    x=(Z,)*4;box=m.initial_box();prev_p=box[0];accels=[]
    accepted=0;last_refusal=None;sample=[];nonzero_next=0;captured=None
    for k in range(steps):
        assert all(lo<=val<=hi for (lo,hi),val in zip(box,x))
        t=m.thrust(scenario,k)
        if capture_tick==k+1:captured=(box,t,x)
        if method=='two_stage':u,a=two_stage_filter(box,t)
        elif method=='zero_bridge':
            a=zero_bridge_audit(box,t)
            u=None if not a['feasible'] else max(Q(a['lower']),min(Q(a['upper']),m.proposed(box)))
        else:raise ValueError(method)
        if u is None:
            last_refusal={'tick':k+1,'reason':a['reason'] if 'reason' in a else 'empty_zero_bridge',
                          'center':list(map(str,m.box_center_radius(box)[0])),
                          'radii':list(map(str,m.box_center_radius(box)[1]))}
            if method=='two_stage':
                # Diagnostic only; a rejection does not imply unsafe plant or no other policy.
                z=zero_bridge_audit(box,t)
                last_refusal['zero_bridge_feasible']=z['feasible']
            break
        if method=='two_stage' and k in (0,29,59,89,93,94,95):
            next_t=m.thrust(scenario,k+1)
            u1=contingent_u1(box,t,u,next_t)
            sample.append({'tick':k+1,'torque':str(u),'next_visible_thrust':str(next_t),'next_backup_torque':str(u1),
                           'next_backup_verified':verify_next_backup(box,t,u,next_t)})
            nonzero_next+=u1!=Z
        old_phi=box[2]
        accels.append(m.add(m.scale(old_phi,-t),(-m.rad(t),m.rad(t))))
        x=m.step(x,t,u,m.residual(scenario,k,t))
        box=m.predict(box,t,u)
        packet=(k+1)%15==0
        box=m.observe(box,x,packet,m.measurement_noise(scenario,k))
        if packet:
            box=(box[0],m.intersect(box[1],m.velocity_from_packets(prev_p,box[0],accels)),box[2],box[3])
            prev_p=box[0];accels=[]
        assert all(lo<=val<=hi for (lo,hi),val in zip(box,x))
        assert all(abs(val)<=lim for val,lim in zip(x,m.LIMITS))
        accepted+=1
    return {'scenario':scenario,'method':method,'accepted_ticks':accepted,'first_refusal':last_refusal,
            'sampled_next_backup_checks':sample,'sampled_nonzero_next_backup':nonzero_next,'capture':captured}


def run():
    start=m.initial_box();t0=m.TMAX
    old_interval=m.backup_audit(start,t0)
    new=two_stage_audit(start,t0)
    sample=[]
    if new['feasible']:
        for u0 in (Q(new['lower']),Z,Q(new['upper'])):
            if not Q(new['lower'])<=u0<=Q(new['upper']):continue
            for t1 in (m.TMIN,(m.TMIN+m.TMAX)/2,m.TMAX):
                sample.append({'u0':str(u0),'t1':str(t1),
                               'u1':str(contingent_u1(start,t0,u0,t1)),
                               'independent_four_tick_check':verify_next_backup(start,t0,u0,t1)})
    rows=[]
    for scenario in ('positive_high','alternating_high','switch_positive'):
        old=rollout_filter(scenario,'zero_bridge')
        current=rollout_filter(scenario,'two_stage')
        rows.append({'scenario':scenario,'run207_zero_bridge_accepted':old['accepted_ticks'],
                     'two_stage_accepted':current['accepted_ticks'],
                     'two_stage_first_refusal':None if current['first_refusal'] is None else current['first_refusal']['tick'],
                     'next_backup_checks':current['sampled_next_backup_checks']})
    box,t0,truth=rollout_filter('alternating_high','two_stage',capture_tick=95)['capture']
    zero=zero_bridge_audit(box,t0);two=two_stage_audit(box,t0)
    selected,_=two_stage_filter(box,t0)
    critical={'tick':95,'scenario':'alternating_high',
              'zero_bridge_feasible':zero['feasible'],'two_stage_feasible':two['feasible'],
              'two_stage_interval':[two['lower'],two['upper']],
              'selected_torque':str(selected),
              'true_state_approx':[format(float(v),'.8g') for v in truth],
              'posterior_center_approx':[format(float(v),'.8g') for v in m.box_center_radius(box)[0]],
              'posterior_radius_approx':[format(float(v),'.8g') for v in m.box_center_radius(box)[1]],
              'contingent_next':[]}
    for t1 in (m.TMIN,(m.TMIN+m.TMAX)/2,m.TMAX):
        u1=contingent_u1(box,t0,selected,t1)
        critical['contingent_next'].append({'t1':str(t1),'u1':str(u1),
                    'independent_four_tick_check':verify_next_backup(box,t0,selected,t1)})
    return {'run':'208','evidence':'EXACT_RATIONAL_TWO_STAGE_THRUST_CONTINGENT_BACKUP',
            'initial_four_tick':old_interval,'initial_two_stage':new,
            'initial_independent_checks':sample,'reachable_rollouts':rows,
            'strict_reachable_witness':critical,'gate_A':'blocked',
            'caveats':['The next measurement is not exploited: all legal posterior subsets of the full predicted box are covered',
                       'One-step four-tick backup existence, not two-step bridge or recursive feasibility',
                       'u1 can depend on next visible thrust but not future thrust, disturbance or measurement',
                       'Full box reset can be conservative; no infinite-time terminal guarantee',
                       'The 100-tick trajectories are deterministic admissible examples, not all-histories guarantees']}

if __name__=='__main__':main()
