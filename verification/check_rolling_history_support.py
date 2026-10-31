"""Run214: causal rolling affine history support and tick-193 refusal audit.

An exact-rational OUTER bound on velocity is obtained by eliminating initial
position/velocity using any three successful position packets. A bounded
packet memory (default six packets) and exact breakpoint enumeration avoid
numerical optimization. Intersections preserve inclusion but are NOT an
exact constrained-zonotope posterior. Finite backup failure is NOT a plant
nonviability proof. Run with PYTHONPATH=verification.
"""
from __future__ import annotations
import argparse
import itertools
import json
import time
from fractions import Fraction as Q
from pathlib import Path
import check_reachable_smf_backup_rollout as m
import check_nominal_short_mpc as base

Z=Q(0)


def coefficients(a,b,c,q):
    """sum c_i=0 and H*sum (t_i-a)c_i=1, with q=c_2."""
    assert 0<=a<b<c
    cb=(Q(1)/m.H-(c-a)*q)/(b-a)
    return -cb-q,cb,q


def weight(i,a,b,c,q):
    """Coefficient of acceleration at tick i in v_k identity (a<=i<k)."""
    _,cb,cc=coefficients(a,b,c,q)
    pb=m.H*m.H*(b-1-i) if i<b else Z
    pc=m.H*m.H*(c-1-i) if i<c else Z
    return m.H-cb*pb-cc*pc


def breakpoints(a,b,c):
    """Exact candidates for maximizing/minimizing concave/convex support.

    Endpoints of a piecewise-affine support occur when a position coefficient
    or an acceleration weight changes sign. No finite grid approximation.
    """
    db,dc=b-a,c-a
    candidates={Z,Q(1)/(dc*m.H),Q(1)/((dc-db)*m.H)}
    for i in range(a,c):
        pb=m.H*m.H*(b-1-i) if i<b else Z
        pc=m.H*m.H*(c-1-i)
        intercept=m.H-pb/(db*m.H)
        slope=Q(dc,db)*pb-pc
        if slope:candidates.add(-intercept/slope)
    return tuple(sorted(candidates))


def three_packet_support(packets,attitudes,thrusts,end_tick):
    """Reliable interval for v_end_tick using only available observations.

    packets = ((tick, measured_position),)*3; attitudes and thrusts are dicts
    indexed by physical transition tick. Disturbance/measurement noise are
    independently relaxed; this is an outer bound even with coupled dynamics.
    """
    (a,pa),(b,pb),(c,pc)=packets
    assert a<b<c<=end_tick
    assert all(i in attitudes and i in thrusts for i in range(a,end_tick))
    samples=[]
    for q in breakpoints(a,b,c):
        co=coefficients(a,b,c,q)
        center=sum((u*p for u,p in zip(co,(pa,pb,pc))),Z)
        radius=m.SIGMA[0]*sum(map(abs,co),Z)
        for i in range(a,end_tick):
            wi=weight(i,a,b,c,q)
            t=thrusts[i]
            center-=wi*t*attitudes[i]
            radius+=abs(wi)*(t*m.SIGMA[2]+m.rad(t))
        samples.append((q,center-radius,center+radius))
    best_lo=max(samples,key=lambda v:v[1]);best_hi=min(samples,key=lambda v:v[2])
    return (best_lo[1],best_hi[2]),{'packets':(a,b,c),
        'lower_q':str(best_lo[0]),'upper_q':str(best_hi[0]),
        'breakpoints':len(samples)}


def rolling_support(positions,attitudes,thrusts,end_tick,max_packets=6):
    """Intersect exact historical outer supports over bounded packet memory."""
    assert max_packets>=3
    indices=sorted(t for t in positions if t<=end_tick)[-max_packets:]
    if len(indices)<3:return None,{'triples':0}
    lo=None;hi=None;best_lower=None;best_upper=None;count=0
    for triple in itertools.combinations(indices,3):
        bound,meta=three_packet_support(tuple((t,positions[t]) for t in triple),
                                        attitudes,thrusts,end_tick)
        count+=1
        if lo is None or bound[0]>lo:lo=bound[0];best_lower=meta
        if hi is None or bound[1]<hi:hi=bound[1];best_upper=meta
    assert lo<=hi, 'measurement history inconsistent under assumed bounds'
    return (lo,hi),{'triples':count,'best_lower':best_lower,
        'best_upper':best_upper,'oldest_packet':indices[0],
        'newest_packet':indices[-1]}


def replay_to_193(return_controls=False):
    """Run210's exact deterministic positive_high history; refine at tick192.

    The returned state is immediately before control at tick193. No future
    observation is used for control or refinement.
    """
    x=(Z,)*4;box=m.initial_box();prev_p=box[0];accels=[]
    positions={};attitudes={};thrusts={};torques={}
    for k in range(192):
        t=m.thrust('positive_high',k)
        if k==191:
            # Exactly Run213's fixed three-packet q=5 historical refinement.
            triple=((150,positions[150]),(165,positions[165]),(180,positions[180]))
            q=Q(5);co=coefficients(150,165,180,q)
            center=sum((u*p for u,(_,p) in zip(co,triple)),Z)
            radius=m.SIGMA[0]*sum(map(abs,co),Z)
            for i in range(150,191):
                wi=weight(i,150,165,180,q);ti=thrusts[i]
                center-=wi*ti*attitudes[i]
                radius+=abs(wi)*(ti*m.SIGMA[2]+m.rad(ti))
            box=(box[0],m.intersect(box[1],(center-radius,center+radius)),box[2],box[3])
        allowed,reason=base.interval(box,t)
        assert allowed is not None,(k+1,reason)
        u=max(allowed[0],min(allowed[1],m.proposed(box)-Q(1,5)*m.mid(box[3])))
        torques[k]=u
        old_phi=box[2]
        accels.append(m.add(m.scale(old_phi,-t),(-m.rad(t),m.rad(t))))
        attitudes[k]=x[2]+m.measurement_noise('positive_high',k)[2]
        thrusts[k]=t
        x=m.step(x,t,u,m.residual('positive_high',k,t))
        box=m.predict(box,t,u)
        packet=(k+1)%15==0
        box=m.observe(box,x,packet,m.measurement_noise('positive_high',k))
        if packet:
            positions[k+1]=x[0]+m.measurement_noise('positive_high',k)[0]
            box=(box[0],m.intersect(box[1],m.velocity_from_packets(prev_p,box[0],accels)),box[2],box[3])
            prev_p=box[0];accels=[]
        assert all(lo<=val<=hi for (lo,hi),val in zip(box,x))
        assert all(abs(val)<=lim for val,lim in zip(x,m.LIMITS))
    if return_controls:return box,x,positions,attitudes,thrusts,torques
    return box,x,positions,attitudes,thrusts


def five_step_box_corner(box):
    """Adverse fixed thrust/residual, maximum negative torque braking.

    This is a certificate obstruction for a BOX corner, not a proof that
    this joint corner is consistent with the historical measurements.
    """
    s=(box[0][0],box[1][0],box[2][1],box[3][1])
    velocities=[]
    for _ in range(5):
        s=m.step(s,m.TMAX,-m.UMAX,-m.rad(m.TMAX))
        velocities.append(s[1])
    return velocities


def run():
    box,truth,positions,attitudes,thrusts=replay_to_193()
    start=time.perf_counter()
    last3,meta3=rolling_support(positions,attitudes,thrusts,192,3)
    last6,meta6=rolling_support(positions,attitudes,thrusts,192,6)
    seconds=time.perf_counter()-start
    refined=(box[0],m.intersect(box[1],last6),box[2],box[3])
    old_a,old_reason=base.interval(box,m.TMAX)
    new_a,new_reason=base.interval(refined,m.TMAX)
    witness=five_step_box_corner(refined)
    assert last6[0]>box[1][0]
    assert all(a<=z<=b for (a,b),z in zip(refined,truth))
    assert old_a is None and new_a is None
    assert witness[-1]<-m.LIMITS[1]
    return {'run':214,'scenario':'positive_high','tick':193,
        'original_velocity':list(map(str,box[1])),
        'last3_history_support':list(map(str,last3)),
        'last6_history_support':list(map(str,last6)),
        'refined_velocity':list(map(str,refined[1])),
        'lower_improvement':str(refined[1][0]-box[1][0]),
        'actual_velocity':str(truth[1]),
        'old_refusal':old_reason,'refined_refusal':new_reason,
        'refined_five_step_corner_velocity':list(map(str,witness)),
        'velocity_limit':str(m.LIMITS[1]),
        'last3_metadata':meta3,'last6_metadata':meta6,
        'support_wall_seconds':round(seconds,6),
        'truth_contained':True,'hard_violations':0,
        'gate_A':'blocked',
        'evidence':'exact rational historical outer support; deterministic reachable replay; finite box-corner obstruction',
        'limitations':['not a joint CZ posterior or exact historical feasible set',
            'independent attitude/residual relaxation can preserve spurious joint corners',
            'no recovery of tick193 two-stage backup; no recursive feasibility',
            'one deterministic trajectory; timing is machine-dependent']}


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path)
    args=p.parse_args();s=json.dumps(run(),ensure_ascii=False,indent=2)+'\n'
    if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(s)
    else:print(s,end='')
if __name__=='__main__':main()
