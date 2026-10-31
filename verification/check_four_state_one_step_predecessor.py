#!/usr/bin/env python3
"""Run224: exact rational one-step robust predecessor *witnesses*, not an RCI kernel.

Frozen four-state (px,vx,phi,omega) Euler subsystem, zero attitude process
noise, and Run208/210 independently selectable lateral residual. Controller
selects T,tau before the residual. All sine enclosures are rational and
certified by alternating Taylor bounds for |phi| <= 0.45.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as Q
from pathlib import Path

H=Q(1,50); TMIN=Q(981,200); TMAX=Q(2943,200)
R0=Q(47,25); RT=Q(243,16000); MASS=Q(1); INERTIA=Q(1,50)
PMAX=Q(5); VMAX=Q(3); PHIMAX=Q(9,20); OMAX=Q(2); TAUMAX=Q(2,25)


def sine_bounds(phi):
    """Exact bounds from s7<=sin(r)<=s5, 0<=r<=0.45."""
    if abs(phi)>PHIMAX: raise ValueError('phi outside certified domain')
    r=abs(phi)
    s5=r-r**3/Q(6)+r**5/Q(120)
    s7=s5-r**7/Q(5040)
    return (s7,s5) if phi>=0 else (-s5,-s7)


def residual_radius(thrust):
    assert TMIN<=thrust<=TMAX
    return R0+RT*thrust


def next_bounds(state,thrust,torque):
    """Rational enclosure of F(x,u,r) for ALL |r|<=R(T)."""
    p,v,phi,omega=state
    if not (TMIN<=thrust<=TMAX and -TAUMAX<=torque<=TAUMAX):
        raise ValueError('input outside bounds')
    slo,shi=sine_bounds(phi); rad=residual_radius(thrust)
    return {'p':(p+H*v,p+H*v),
            'v':(v+H*(-thrust*shi+(-rad)),v+H*(-thrust*slo+rad)),
            'phi':(phi+H*omega,phi+H*omega),
            'omega':(omega+H*torque/INERTIA,omega+H*torque/INERTIA)}


def in_domain(state):
    p,v,phi,omega=state
    return -PMAX<=p<=PMAX and -VMAX<=v<=VMAX and -PHIMAX<=phi<=PHIMAX and -OMAX<=omega<=OMAX


def certified_predecessor(state,thrust,torque):
    """Sufficient exact test for exists u forall r F(x,u,r) in X.

    Does not characterize the whole predecessor because the sine enclosure
    is not the exact transcendental sine value.
    """
    if not in_domain(state): return False
    b=next_bounds(state,thrust,torque)
    return all(-lim<=lo<=hi<=lim for key,lim in [('p',PMAX),('v',VMAX),('phi',PHIMAX),('omega',OMAX)] for lo,hi in [b[key]])


def boundary_obstruction(radius):
    """At vx=+3, phi<=radius, r=+R(T) violates vx bound for every T.

    Exact for any radius in [0,.45] with sin_upper(radius)<R0/TMAX+RT.
    Negative-velocity/tilt case follows by symmetry.
    """
    if not Q(0)<=radius<=PHIMAX: raise ValueError('radius outside domain')
    return sine_bounds(radius)[1] < RT+R0/TMAX


def config_contract(root):
    c=json.loads((Path(root)/'configs/planar_baseline.json').read_text(),parse_float=Q)
    assert c['plant']['truth_semantics']=='defined_discrete_euler'
    assert Q(c['plant']['dt_s'])==H
    assert Q(c['plant']['mass_kg'])==MASS
    assert Q(c['plant']['inertia_kg_m2'])==INERTIA
    assert [Q(x) for x in c['domain']['input_lower']]==[TMIN,-TAUMAX]
    assert [Q(x) for x in c['domain']['input_upper']]==[TMAX,TAUMAX]
    assert [Q(c['domain']['state_upper'][i]) for i in (0,2,4,5)]==[PMAX,VMAX,PHIMAX,OMAX]
    assert [Q(c['domain']['state_lower'][i]) for i in (0,2,4,5)]==[-PMAX,-VMAX,-PHIMAX,-OMAX]
    return True


def verify(root=None):
    if root is not None: config_contract(root)
    radius=Q(717,5000)
    assert boundary_obstruction(radius)
    assert not boundary_obstruction(Q(3,20))
    witnesses=[]
    for sign in (+1,-1):
        x=(Q(0),sign*VMAX,sign*Q(3,20),Q(0))
        u=(TMAX,Q(0))
        assert certified_predecessor(x,*u)
        b=next_bounds(x,*u)
        witnesses.append({'state':[str(z) for z in x],
                          'input':[str(z) for z in u],
                          'successor_bounds':{k:[str(z) for z in interval] for k,interval in b.items()},
                          'certified_for_all_residuals':True})
    # Stronger one-step exclusion for ANY thrust and torque, using upper sine.
    assert sine_bounds(radius)[1] < RT+R0/TMAX
    return {'run':'224','base':'Run223 frozen four-state Euler; Run208/210 lateral residual envelope',
            'quantifiers':'exists (T,tau) chosen from current full state; forall r_x in [-R(T),R(T)]',
            'evidence':'EXACT_RATIONAL_SINE_ENCLOSURE_ONE_STEP_PREDECESSOR',
            'boundary_exclusion_radius':str(radius),
            'boundary_exclusion_gap_lower':str(RT+R0/TMAX-sine_bounds(radius)[1]),
            'boundary_witnesses':witnesses,'gate_A':'blocked',
            'limitations':['One-step predecessor of the full state safety box X only; witnesses are NOT an invariant subset or terminal kernel.',
                           'Uses full-state causal feedback and zero angular process disturbance; does not establish SMF output-feedback feasibility.',
                           'The Run208/210 residual is independently adversarial and need not represent persistent physical aerodynamics.',
                           'No recursive feasibility, Lyapunov stability, 20ms timing guarantee, or six-state safety.']}


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path);p.add_argument('--output',type=Path);a=p.parse_args()
    out=json.dumps(verify(a.root),indent=2,sort_keys=True,ensure_ascii=False)+'\n'
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(out)
    else: print(out,end='')
if __name__=='__main__':main()
