#!/usr/bin/env python3
"""Run204 experimental four-state causal SMF+torque feedback loop.

Float interval SMF: sound outer propagation in exact mathematics, floating
arithmetic is a NUMERIC CHECK only. Non-MPC, no recursive feasibility claim.
"""
from __future__ import annotations
import argparse,json,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(root=ROOT):
    c=json.loads((Path(root)/'configs/planar_baseline.json').read_text())
    g=c['mpc']['ancillary_rci_contract']['mode_graph']
    assert g['mode_count']==15 and c['sensing']['position_period_ticks']==5
    return dict(h=c['plant']['dt_s'],j=c['plant']['inertia_kg_m2'],
                tmin=c['domain']['input_lower'][0],tmax=c['domain']['input_upper'][0],
                taumax=c['domain']['input_upper'][1],limits=tuple(c['domain']['state_upper'][i] for i in (0,2,4,5)),
                sigma=(c['sensing']['observed_noise_halfwidth']['px'],0.,c['sensing']['observed_noise_halfwidth']['phi'],c['sensing']['observed_noise_halfwidth']['omega']))

def rad(t):return 1.88+243*t/16000

def add(a,b):return (a[0]+b[0],a[1]+b[1])
def scale(a,k):return (min(a[0]*k,a[1]*k),max(a[0]*k,a[1]*k))
def intersect(a,b):
    lo=max(a[0],b[0]);hi=min(a[1],b[1]);
    if lo>hi+1e-11:raise ValueError(f'empty posterior {a} {b}')
    return (lo,hi if hi>=lo else lo)
def middle(a):return (a[0]+a[1])/2

def plant_step(x,t,u,r,c):
    p,v,phi,omega=x;h=c['h']
    return (p+h*v,v-h*t*phi+h*r,phi+h*omega,omega+h*u/c['j'])

def initial(c):
    return ((-0.02,0.02),(-0.1,0.1),(-0.005,0.005),(-0.01,0.01))

def predict(box,t,u,c):
    p,v,phi,omega=box;h=c['h'];d=rad(t)
    acceleration=add(scale(phi,-t),(-d,d))
    return (add(p,scale(v,h)),add(v,scale(acceleration,h)),add(phi,scale(omega,h)),add(omega,(h*u/c['j'],h*u/c['j']))),acceleration

def observe(box,real,packet,c,noise=(0.,0.,0.,0.)):
    y=list(box)
    for i in (2,3)+((0,) if packet else ()):
        val=real[i]+noise[i];r=c['sigma'][i]
        y[i]=intersect(y[i],(val-r,val+r))
    return tuple(y)

def v_from_two_packets(prev_p,cur_p,accelerations,h):
    n=len(accelerations)
    assert n>0
    out=scale(add(cur_p,scale(prev_p,-1)),1/(n*h))
    for i,a in enumerate(accelerations):out=add(out,scale(a,h*(i+1)/n))
    return out

def feedback(box,c):
    p,v,phi,omega=(middle(a) for a in box)
    return max(-c['taumax'],min(c['taumax'],.8*p+1.08*v-2.95*phi-.4*omega))

def simulate(c,controller,scenario,steps=150):
    x=(0.,)*4;box=initial(c);prev_p=box[0];accels=[]
    count_packets=0;maxwidth=[0.]*4;maxstate=[0.]*4;violations=[];max_torque=0.;nonzero=0;covered=0
    # Position packets every 5 ticks; force two misses then one success.
    for tick in range(steps):
        u=(feedback(box,c) if controller=='feedback' else (feedback(tuple((z,z) for z in x),c) if controller=='fullstate' else 0.))
        max_torque=max(max_torque,abs(u));nonzero+=abs(u)>1e-12
        t=c['tmax'] if scenario in ('positive_high','alternating_high') else (c['tmax'] if tick%20<10 else c['tmin'])
        d=rad(t)
        r=d if scenario in ('positive_high','switch_positive') else (d if tick%30<15 else -d)
        oldbox=box
        x=plant_step(x,t,u,r,c)
        box,a=predict(box,t,u,c);accels.append(a)
        packet=(tick+1)%15==0
        box=observe(box,x,packet,c)
        if packet:
            box=list(box)
            box[1]=intersect(box[1],v_from_two_packets(prev_p,box[0],accels,c['h']))
            box=tuple(box);prev_p=box[0];accels=[];count_packets+=1
        if all(lo-1e-8<=z<=hi+1e-8 for z,(lo,hi) in zip(x,box)):covered+=1
        else:raise AssertionError(('containment failed',tick,x,box,oldbox))
        for i,(z,lim) in enumerate(zip(x,c['limits'])):
            maxstate[i]=max(maxstate[i],abs(z));maxwidth[i]=max(maxwidth[i],(box[i][1]-box[i][0])/2)
            if abs(z)>lim+1e-10:violations.append((tick+1,i,abs(z)))
    return dict(controller=controller,scenario=scenario,steps=steps,position_packets=count_packets,
                misses=(steps//5-count_packets),smf_coverage=covered,
                max_abs_state=maxstate,max_smf_halfwidth=maxwidth,
                first_violation=violations[0] if violations else None,
                violations=len(violations),max_abs_torque=max_torque,nonzero_torque_ticks=nonzero,
                final_state=list(x))

def run(root=ROOT):
    c=load(root);rows=[]
    for scenario in ('positive_high','alternating_high','switch_positive'):
        for ctl in ('zero','feedback','fullstate'):
            rows.append(simulate(c,ctl,scenario))
    return dict(status='PASS',evidence='NUMERIC_DETERMINISTIC_CAUSAL_FEEDBACK_PROBE',
                contract='four-state Euler proxy; 15-tick position packet success with misses at 5,10; phi/omega every tick; zero measurement noise (within bounds); known thrust',
                feedback='saturated u=0.8*p_hat+1.08*v_hat-2.95*phi_hat-0.4*omega_hat; midpoint of interval SMF; heuristic, not MPC',
                scenarios=rows,gate_A='blocked',
                caveats=['Numerical interval calculations are not outward-rounded, so coverage is a scenario check not a proof',
                         'Three deterministic disturbance/thrust patterns, not universal robustness',
                         'No terminal invariant set, recursive feasibility or six-state guarantee',
                         'Gain chosen from approximate nominal LQR, not an optimized robust policy'])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=ROOT);ap.add_argument('--output',type=Path)
    a=ap.parse_args();s=json.dumps(run(a.root),indent=2)+'\n'
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    else:print(s,end='')
if __name__=='__main__':main()
