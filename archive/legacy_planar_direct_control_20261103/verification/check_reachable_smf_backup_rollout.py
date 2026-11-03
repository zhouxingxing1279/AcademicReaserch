#!/usr/bin/env python3
"""Run206: exact-rational reachable intermittent-SMF/4-tick backup rollout.

Each control is selected after the current measurement and thrust are known,
but before the next residual/packet outcome.  A successful four-tick backup
certificate is only a conditional finite-horizon result, NOT a recursive
feasibility/terminal certificate. Refuse to apply an uncertified command.
"""
from __future__ import annotations
import argparse
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
Z=Q(0)
H=J=Q(1,50)
TMIN=Q(981,200)
TMAX=Q(2943,200)
UMAX=Q(2,25)
LIMITS=(Q(5),Q(3),Q(9,20),Q(2))
SIGMA=(Q(1,50),None,Q(1,200),Q(1,100))
INITIAL_RAD=(Q(1,50),Q(1,10),Q(1,200),Q(1,100))


def verify_contract(root=ROOT):
    path=Path(root)/'configs/planar_baseline.json'
    d=json.loads(path.read_text(),parse_float=Q)
    assert d['state_order']==['px','pz','vx','vz','phi','omega']
    assert d['plant']['truth_semantics']=='defined_discrete_euler'
    assert (d['plant']['dt_s'],d['plant']['inertia_kg_m2'])==(H,J)
    assert (d['domain']['input_lower'][0],d['domain']['input_upper'][0])==(TMIN,TMAX)
    assert d['domain']['input_upper'][1]==UMAX
    assert tuple(d['domain']['state_upper'][i] for i in (0,2,4,5))==LIMITS
    assert tuple(d['sensing']['observed_noise_halfwidth'][k] for k in ('px','phi','omega'))==(SIGMA[0],SIGMA[2],SIGMA[3])
    assert d['sensing']['position_period_ticks']==5 and d['sensing']['max_consecutive_missed_packets']==2
    graph=d['mpc']['ancillary_rci_contract']['mode_graph']
    assert graph['mode_count']==15 and graph['control_precedes_successor_edge'] is True
    assert {(int(a),int(b),kind) for a,b,kind in graph['edges']}==({(i,i+1,'miss') for i in range(14)} | {(4,0,'success'),(9,0,'success'),(14,0,'success')})
    assert d['mpc']['ancillary_rci_contract']['disturbance_graph']['physical_residual_halfwidth']['r_x']=='47/25 + (243/16000) * actual_thrust'
    return True


def rad(t):return Q(47,25)+Q(243,16000)*t

def add(a,b):return (a[0]+b[0],a[1]+b[1])
def scale(a,k):return (min(a[0]*k,a[1]*k),max(a[0]*k,a[1]*k))
def intersect(a,b):
    lo=max(a[0],b[0]);hi=min(a[1],b[1])
    if lo>hi:raise ValueError('inconsistent measurement')
    return lo,hi

def mid(a):return (a[0]+a[1])/2

def box_center_radius(box):return tuple(mid(a) for a in box),tuple((a[1]-a[0])/2 for a in box)

def initial_box():return tuple((-r,r) for r in INITIAL_RAD)

def step(x,t,u,r=Z):
    p,v,phi,om=x
    return p+H*v, v-H*t*phi+H*r, phi+H*om, om+H*u/J

def predict(box,t,u):
    p,v,phi,om=box
    return (add(p,scale(v,H)),add(add(v,scale(phi,-H*t)),(-H*rad(t),H*rad(t))),
            add(phi,scale(om,H)),add(om,(H*u/J,H*u/J)))

def observe(box,truth,success,noise=(Z,Z,Z,Z)):
    out=list(box)
    for i in ((0,2,3) if success else (2,3)):
        s=SIGMA[i];assert s is not None and abs(noise[i])<=s
        y=truth[i]+noise[i]
        out[i]=intersect(out[i],(y-s,y+s))
    return tuple(out)

def support_abs(center,gens):
    return tuple(abs(center[i])+sum(abs(g[i]) for g in gens) for i in range(4))

def constrain(interval,a,b,remaining):
    lo,hi=interval
    if remaining<0:return Q(1),Q(0)
    if b==0:return interval if abs(a)<=remaining else (Q(1),Q(0))
    x=(-remaining-a)/b;y=(remaining-a)/b
    return max(lo,min(x,y)),min(hi,max(x,y))

def backup_audit(box,t0,horizon=4):
    """Exact first-torque interval, with future torque fixed zero.

    Future thrust endpoints suffice because for each fixed independent noise
    primitive every coordinate is separately affine in each future thrust;
    all signed coordinate extrema are bounded by vertex interpolation.
    """
    assert horizon==4 and TMIN<=t0<=TMAX
    center,radii=box_center_radius(box)
    if any(abs(a)+b>lim for a,b,lim in zip(center,radii,LIMITS)):
        return {'feasible':False,'reason':'current_outer_box_outside_hard_limits','inequalities':0}
    allowed=(-UMAX,UMAX);count=0
    for future in itertools.product((TMIN,TMAX),repeat=horizon-1):
        x=center;coef=(Z,)*4
        gens=tuple(tuple(radii[i] if i==j else Z for i in range(4)) for j in range(4))
        for k,t in enumerate((t0,)+future):
            x=step(x,t,Z)
            coef=step(coef,t,Q(1) if k==0 else Z)
            gens=tuple(step(g,t,Z) for g in gens)+((Z,H*rad(t),Z,Z),)
            for i in range(4):
                spread=sum(abs(g[i]) for g in gens)
                allowed=constrain(allowed,x[i],coef[i],LIMITS[i]-spread)
                count+=1
    return {'feasible':allowed[0]<=allowed[1],'reason':'admitted' if allowed[0]<=allowed[1] else 'empty_four_tick_backup_interval',
            'lower':str(allowed[0]),'upper':str(allowed[1]),'inequalities':count}

def proposed(box):
    p,v,phi,om=(mid(a) for a in box)
    raw=Q(4,5)*p+Q(27,25)*v-Q(59,20)*phi-Q(2,5)*om
    return max(-UMAX,min(UMAX,raw))

def filter_torque(box,t):
    a=backup_audit(box,t)
    if not a['feasible']:return None,a
    u=proposed(box)
    return max(Q(a['lower']),min(Q(a['upper']),u)),a

def thrust(scenario,k):
    return TMAX if scenario in ('positive_high','alternating_high') or k%20<10 else TMIN

def residual(scenario,k,t):
    if scenario in ('positive_high','switch_positive'):return rad(t)
    return rad(t) if k%30<15 else -rad(t)

def measurement_noise(scenario,k):
    if scenario=='alternating_high':
        sign=Q(1) if k%2 else Q(-1)
        return (sign*SIGMA[0],Z,sign*SIGMA[2],-sign*SIGMA[3])
    return (Z,Z,Z,Z)

def velocity_from_packets(prev_p,cur_p,accels):
    n=len(accels)
    assert n>0
    out=scale(add(cur_p,scale(prev_p,-1)),Q(1)/(n*H))
    for i,a in enumerate(accels):out=add(out,scale(a,H*Q(i+1,n)))
    return out

def display(q):
    """Rounded for JSON display only; all decisions use exact Fractions."""
    return format(float(q),'.10g')

def rollout(scenario,steps=100,estimator='interval'):
    assert scenario in ('positive_high','alternating_high','switch_positive')
    assert estimator in ('interval','packet_velocity')
    x=(Z,)*4;box=initial_box();maxwidth=[Z]*4
    prev_p=box[0];accels=[];packet_refinements=0
    accepted=successes=misses=filtered=0
    scheduled_misses=0
    first_refusal=None
    maxstate=[Z]*4
    records=[]
    for k in range(steps):
        assert all(lo<=val<=hi for (lo,hi),val in zip(box,x))
        t=thrust(scenario,k)
        u,a=filter_torque(box,t)
        if u is None:
            first_refusal={'tick':k+1,'reason':a['reason'],'center_approx':list(map(display,box_center_radius(box)[0])),
                           'radii_approx':list(map(display,box_center_radius(box)[1])),
                           'true_state_approx':list(map(display,x))}
            break
        filtered+=u!=proposed(box)
        old_phi=box[2]
        accel=add(scale(old_phi,-t),(-rad(t),rad(t)))
        accels.append(accel)
        x=step(x,t,u,residual(scenario,k,t))
        box=predict(box,t,u)
        packet=(k+1)%15==0
        box=observe(box,x,packet,measurement_noise(scenario,k))
        if packet:
            if estimator=='packet_velocity':
                newv=intersect(box[1],velocity_from_packets(prev_p,box[0],accels))
                box=(box[0],newv,box[2],box[3]);packet_refinements+=1
            prev_p=box[0];accels=[]
        assert all(lo<=val<=hi for (lo,hi),val in zip(box,x)),('containment',k,x,box)
        assert all(abs(val)<=lim for val,lim in zip(x,LIMITS)),('hard violation',k,x)
        assert all(abs(val)<=lim for val,lim in zip((x[0],x[1],x[2],x[3]),LIMITS))
        accepted+=1;successes+=packet;misses+=not packet
        scheduled_misses+=((k+1)%5==0 and not packet)
        for i,(val,interval) in enumerate(zip(x,box)):
            maxstate[i]=max(maxstate[i],abs(val))
            maxwidth[i]=max(maxwidth[i],(interval[1]-interval[0])/2)
        if (k+1)%5==0 or k==0:
            records.append({'tick':k+1,'state_approx':list(map(display,x)),
                            'halfwidths_approx':list(map(display,box_center_radius(box)[1])),'last_torque_approx':display(u)})
    return {'scenario':scenario,'estimator':estimator,'requested_steps':steps,'accepted_ticks':accepted,'success_packets':successes,'packet_refinements':packet_refinements,
            'position_not_observed_ticks':misses,'scheduled_position_misses':scheduled_misses,'filtered_torque_ticks':filtered,
            'max_abs_state_approx':list(map(display,maxstate)),'max_posterior_halfwidth_approx':list(map(display,maxwidth)),
            'first_refusal':first_refusal,'last_state_approx':list(map(display,x)),
            'last_posterior_approx':[[display(lo),display(hi)] for lo,hi in box],
            'trace_every_5_ticks':records}

def run(root=ROOT,steps=100):
    verify_contract(root)
    rows=[rollout(s,steps,est) for est in ('interval','packet_velocity') for s in ('positive_high','alternating_high','switch_positive')]
    return {'status':'AUDIT_COMPLETED_WITH_POSSIBLE_REFUSALS','evidence':'EXACT_RATIONAL_FINITE_REACHABLE_SMF_ROLLOUT_WITH_LOCAL_BACKUP_AUDITS',
            'scope':'four-state Euler proxy; deterministic actual reachable histories; no universal terminal/recursive certificate',
            'display':'Rounded decimal strings for human inspection; all dynamics, filters, certificates and assertions use exact Fraction arithmetic',
            'initial_truth':['0']*4,'initial_outer_halfwidth':list(map(str,INITIAL_RAD)),
            'packet_contract':'position attempted every five ticks, first two missed, third success; phi/omega always observed',
            'policy':'posterior midpoint saturated feedback, projected into exact four-tick backup interval; refuse when empty',
            'backup':'first torque selected now; future three torques fixed zero; all future thrust sequences and residuals',
            'rows':rows,'gate_A':'blocked',
            'caveats':['All arithmetic uses Fraction, including measurements; sampled actual histories are not all possible observations',
                       'Four-tick backup admission does not ensure a feasible next-step backup or all-time hard safety',
                       'Interval SMF and packet-to-packet velocity refinement both discard general CZ correlations; no CZ gain is claimed',
                       'A refusal is a fail-closed controller result, not a safe recovery controller',
                       'Not MPC optimization and no terminal controlled invariant set']}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=ROOT)
    ap.add_argument('--steps',type=int,default=100);ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    s=json.dumps(run(args.root,args.steps),indent=2,ensure_ascii=False)+'\n'
    if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(s)
    else:print(s,end='')
if __name__=='__main__':main()
