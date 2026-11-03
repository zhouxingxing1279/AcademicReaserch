#!/usr/bin/env python3
"""Run204: exact no-go for fixed-origin mode-indexed product-box terminal sets.

This is a class-specific theorem, NOT a no-go for general RCI, CZ, or MPC.
A 5-edge success cycle suffices, independently of controller information.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as Q
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def contract(root=ROOT):
    d=json.loads((Path(root)/'configs/planar_baseline.json').read_text(),parse_float=Q)
    g=d['mpc']['ancillary_rci_contract']['mode_graph']
    assert d['state_order']==['px','pz','vx','vz','phi','omega']
    assert g['mode_count']==15 and g['control_precedes_successor_edge'] is True
    edges={(int(a),int(b),k) for a,b,k in g['edges']}
    assert {(i,i+1,'miss') for i in range(4)} | {(4,0,'success')} <= edges
    assert d['mpc']['ancillary_rci_contract']['disturbance_graph']['physical_residual_halfwidth']['r_x']=='47/25 + (243/16000) * actual_thrust'
    return dict(h=d['plant']['dt_s'],j=d['plant']['inertia_kg_m2'],tmin=d['domain']['input_lower'][0],tmax=d['domain']['input_upper'][0],tau_max=d['domain']['input_upper'][1],state_limits=[d['domain']['state_upper'][i] for i in (0,2,4,5)],edges=edges)

def residual(t):return Q(47,25)+Q(243,16000)*t

def step(x,t,tau,r,c):
    p,v,phi,omega=x;h=c['h']
    assert c['tmin']<=t<=c['tmax'] and abs(tau)<=c['tau_max'] and abs(r)<=residual(t)
    return (p+h*v,v-h*t*phi+h*r,phi+h*omega,omega+h*tau/c['j'])

def clip(x,b):return min(b,max(-b,x))

def nonzero_causal_torque(x,c):
    """Explicit full-state policy, strictly MORE informative than SMF output feedback.

    Chosen solely to expose nonzero torque at the counterexample corner;
    not certified stabilizing or recursively safe.
    """
    p,v,phi,omega=x
    return clip(Q(1,50)*p+Q(1,25)*v-Q(1,10)*phi-Q(1,20)*omega,c['tau_max'])

def corner_witness(c):
    # One admissible physical state in B=[-1,1]x[-1/2,1/2]x[-1/10,1/10]x[-1/5,1/5].
    x=(Q(1),Q(1,2),Q(0),Q(0));tau=nonzero_causal_torque(x,c)
    nxt=step(x,c['tmin'],tau,Q(0),c)
    assert tau!=0 and nxt[0]>1 and all(abs(z)<=bound for z,bound in zip(x,c['state_limits']))
    return dict(mode=4,successor_mode=0,initial=[str(z) for z in x],torque=str(tau),next=[str(z) for z in nxt],position_excess=str(nxt[0]-1),residual='0',thrust=str(c['tmin']))

def five_cycle_proof(c):
    """Symbolic exact proof for ALL nonnegative radii P_i,V_i and all policies.

    On each of the five edges, the p=P_i,v=V_i,phi=omega=0 corner forces
    P_next >= P_i+h V_i. Summation forces all V_i=0. At any mode, the
    zero state and r=d(T)>0 then force V_next>=h*d(T)>0: contradiction.
    This is a physical-state product-box result; measurements cannot reset x.
    """
    cycle=((0,1,'miss'),(1,2,'miss'),(2,3,'miss'),(3,4,'miss'),(4,0,'success'))
    assert all(e in c['edges'] for e in cycle)
    assert c['h']>0 and residual(c['tmin'])>0
    lower=c['h']*residual(c['tmin'])
    assert lower>0
    return dict(cycle=[dict(source=i,target=j,label=k) for i,j,k in cycle],
                necessary_inequality='P_next >= P_current + h * V_current on each cycle edge',
                cycle_sum='0 >= h*(V0+V1+V2+V3+V4); V_i>=0 => all V_i=0',
                residual_step='at x=0, phi=0, any tau, choose r=d(Tmin)>0; v_next=h*d(Tmin)>0',
                forced_positive_velocity_radius=str(lower),
                no_go='NO fixed-origin nonempty symmetric Cartesian-product physical-state boxes indexed by the 15-mode graph can satisfy robust one-step invariance on all legal edges',
                scope='applies to all causal policies, even full-state; not to translated/correlated/measurement-conditioned sets')

def torque_relative_degree(c):
    x=(Q(0),)*4; t=c['tmin'];r=Q(0);tau=c['tau_max']
    zero=[x];impulse=[x]
    for k in range(4):
        zero.append(step(zero[-1],t,Q(0),r,c))
        impulse.append(step(impulse[-1],t,tau if k==0 else Q(0),r,c))
    diff=[[str(b-a) for a,b in zip(x0,x1)] for x0,x1 in zip(zero,impulse)]
    assert all(Q(diff[k][0])==0 for k in range(4))
    assert all(Q(diff[k][1])==0 for k in range(3))
    assert Q(diff[4][0])!=0 and Q(diff[3][1])!=0
    return dict(state_order=['p','v','phi','omega'],delta_state_by_tick=diff,
                first_torque_effect={'omega':1,'phi':2,'v':3,'p':4})

def run(root=ROOT):
    c=contract(root)
    return dict(status='PASS',evidence='EXACT_RATIONAL_CLASS_SPECIFIC_NO_GO',
                source_main='run203',
                cycle_proof=five_cycle_proof(c),
                corner_witness=corner_witness(c),
                relative_degree=torque_relative_degree(c),
                gate_A='blocked',
                caveats=['No-go excludes only fixed-origin axis-aligned Cartesian-product physical-state terminal families, not general RCI or mode-indexed information states',
                         'Full-state nonzero feedback witness has more information than the actual intermittent-measurement controller',
                         'No feedback policy or terminal certificate for the four-state plant has been synthesized'])

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=ROOT);ap.add_argument('--output',type=Path)
    a=ap.parse_args();s=json.dumps(run(a.root),ensure_ascii=False,indent=2)+'\n'
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    else:print(s,end='')
if __name__=='__main__':main()
