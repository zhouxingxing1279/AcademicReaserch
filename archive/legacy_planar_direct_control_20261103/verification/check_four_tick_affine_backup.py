#!/usr/bin/env python3
"""Run205: exact four-tick open-loop backup admissibility for shifted SMF boxes.

For an initial *outer* box, known T0 and arbitrary future T1..T3, compute
all first torques tau0 such that tau1=tau2=tau3=0 guarantees the original
four-state hard constraints for ticks 1..4. No terminal/recursive guarantee.
All computations use fractions.Fraction; no floating point is used.
"""
from __future__ import annotations
import argparse
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
Z=Q(0)

def radius(t):return Q(47,25)+Q(243,16000)*t

def load_contract(root=ROOT):
    d=json.loads((Path(root)/'configs/planar_baseline.json').read_text(),parse_float=Q)
    assert d['state_order']==['px','pz','vx','vz','phi','omega']
    assert d['plant']['truth_semantics']=='defined_discrete_euler'
    assert d['sensing']['always_observed_indices']==[4,5]
    assert d['sensing']['position_period_ticks']==5
    assert d['sensing']['max_consecutive_missed_packets']==2
    assert d['mpc']['ancillary_rci_contract']['mode_graph']['control_precedes_successor_edge'] is True
    assert d['mpc']['ancillary_rci_contract']['disturbance_graph']['physical_residual_halfwidth']['r_x']=='47/25 + (243/16000) * actual_thrust'
    c={'h':d['plant']['dt_s'],'J':d['plant']['inertia_kg_m2'],
       'tmin':d['domain']['input_lower'][0],'tmax':d['domain']['input_upper'][0],
       'umax':d['domain']['input_upper'][1],
       'limits':tuple(d['domain']['state_upper'][i] for i in (0,2,4,5)),
       'sigma_p':d['sensing']['observed_noise_halfwidth']['px'],
       'sigma_phi':d['sensing']['observed_noise_halfwidth']['phi'],
       'sigma_omega':d['sensing']['observed_noise_halfwidth']['omega']}
    assert c['h']==c['J']==Q(1,50)
    assert c['limits']==(Q(5),Q(3),Q(9,20),Q(2))
    assert (c['sigma_p'],c['sigma_phi'],c['sigma_omega'])==(Q(1,50),Q(1,200),Q(1,100))
    return c

def read_rows(root=ROOT):
    d=json.loads((Path(root)/'results/four_state_conditional_smf_20261030/checks.json').read_text())
    assert d['status']=='PASS' and len(d['rows'])==6
    return {(int(x['gap_ticks']),x['thrust']):x for x in d['rows']}

def radii_from_run202(row,packet,c):
    if packet=='success':
        return (c['sigma_p'],
                min(Q(row['certified_post_return_velocity_outer_halfwidth']),
                    Q(row['certified_box_velocity_outer_halfwidth'])),c['sigma_phi'],c['sigma_omega'])
    if packet=='miss':
        return (Q(row['certified_box_position_outer_halfwidth']),
                Q(row['certified_box_velocity_outer_halfwidth']),c['sigma_phi'],c['sigma_omega'])
    raise ValueError(packet)

def step(x,t,u,c):
    p,v,phi,om=x;h=c['h'];j=c['J']
    return (p+h*v,v-h*t*phi,phi+h*om,om+h*u/j)

def initial(center,rad):
    assert len(center)==len(rad)==4 and all(a>=0 for a in rad)
    return tuple(center),tuple(tuple(rad[i] if i==j else Z for i in range(4)) for j in range(4))

def propagate_affine(state,t,k,c):
    """State is (constant center, coefficient of tau0, independent generators)."""
    center,coef,gens=state
    new_center=step(center,t,Z,c)
    new_coef=step(coef,t,Q(1) if k==0 else Z,c)
    new_gens=tuple(step(g,t,Z,c) for g in gens)+((Z,c['h']*radius(t),Z,Z),)
    return new_center,new_coef,new_gens

def constrain(interval,a,b,limit):
    """Intersect [lo,hi] with |a+b*tau|<=limit, exact rational."""
    lo,hi=interval
    if limit<0:return (Q(1),Q(0))
    if b==0:
        return interval if abs(a)<=limit else (Q(1),Q(0))
    x=(-limit-a)/b;y=(limit-a)/b
    return (max(lo,min(x,y)),min(hi,max(x,y)))

def audit(center,rad,t0,c,horizon=4,limits=None):
    assert horizon>=1 and c['tmin']<=t0<=c['tmax']
    limits=c['limits'] if limits is None else limits
    assert all(abs(a)+r<=lim for a,r,lim in zip(center,rad,limits)), 'initial box outside hard constraints'
    initial_center,initial_gens=initial(center,rad)
    initial_state=(initial_center,(Z,)*4,initial_gens)
    allowed=(-c['umax'],c['umax'])
    # each coordinate center and generator is multi-affine in independent future T.
    # At fixed tau, the signed coordinate extrema over the T hyperrectangle
    # are attained at vertices; the exact interval is intersection of all
    # corresponding vertex inequalities, for all ticks.
    inequalities=0
    tight=[]
    for future in itertools.product((c['tmin'],c['tmax']),repeat=horizon-1):
        state=initial_state
        for k,t in enumerate((t0,)+future):
            state=propagate_affine(state,t,k,c)
            x,b,gens=state
            for i in range(4):
                spread=sum(abs(g[i]) for g in gens)
                old=allowed
                allowed=constrain(allowed,x[i],b[i],limits[i]-spread)
                inequalities+=1
                if allowed!=old:
                    tight.append((k+1,i,tuple(str(y) for y in future),str(x[i]),str(b[i]),str(spread)))
    return {'feasible':allowed[0]<=allowed[1],
            'lower':str(allowed[0]),'upper':str(allowed[1]),
            'inequalities':inequalities,'future_vertices':2**(horizon-1),
            'active_updates':tight[-10:], 'horizon':horizon}

def filter_torque(proposed,certificate):
    if not certificate['feasible']:
        return None
    lo,hi=Q(certificate['lower']),Q(certificate['upper'])
    return max(lo,min(hi,proposed))

def run(root=ROOT):
    c=load_contract(root);row=read_rows(root)[(10,'high')];t=c['tmax']
    cases=[]
    for label,center in [('origin',(Z,Z,Z,Z)),
                         ('shifted_velocity',(Z,Q(47,20),Z,Z)),
                         ('shifted_attitude',(Z,Z,Q(19,50),Q(4,5)))]:
        for packet in ('success','miss'):
            rad=radii_from_run202(row,packet,c)
            a=audit(center,rad,t,c)
            proposed=Q(1,25)
            selected=filter_torque(proposed,a)
            cases.append({'case':label,'packet':packet,'center':list(map(str,center)),
                          'radii':list(map(str,rad)),'proposed_torque':str(proposed),
                          'filtered_torque':None if selected is None else str(selected),**a})
    return {'status':'PASS','evidence':'EXACT_RATIONAL_FOUR_TICK_OPEN_LOOP_BACKUP_ADMISSION',
            'main_contract':'frozen four-state Euler proxy; current thrust known; future T independent in full interval; residual independent each tick',
            'policy':'one causal tau0, future tau1..tau3 identically zero; packet results ignored after decision',
            'rows':cases,'gate_A':'blocked',
            'caveats':['Synthetic shifted posterior centers are physically admissible but their reachability from the frozen initial set is not established',
                       'Run202 reliable interval outer boxes discard CZ correlations',
                       'All four ticks share one open-loop policy, but no terminal/recursive feasibility or all-time safety follows',
                       'No state/measurement feedback used within four-tick backup; this is a safety admission building block, not MPC']}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=ROOT);ap.add_argument('--output',type=Path)
    a=ap.parse_args();s=json.dumps(run(a.root),indent=2,ensure_ascii=False)+'\n'
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    else:print(s,end='')
if __name__=='__main__':main()
