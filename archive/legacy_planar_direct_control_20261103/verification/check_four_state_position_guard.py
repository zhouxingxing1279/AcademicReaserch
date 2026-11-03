#!/usr/bin/env python3
"""Run230: exact 25-step necessary position guard for the frozen four-state plant.

Full-state causal control is allowed; the adversary selects r=+R(T) (or -R(T))
after each thrust command. This is a universal finite-horizon exclusion, not
an RCI construction, a proof of global kernel emptiness, or an SMF controller.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as Q
from pathlib import Path
import check_four_state_bridge_graph as prior

HORIZON = 25
BASE_MAIN = 'd3f221144d73142dc2da2b9f31e21c2c30fb46e4'


def tilt_upper(step: int) -> Q:
    """phi_k <= h^2*(tau_max/I)*k(k-1)/2, for phi0=omega0=0."""
    if step < 0: raise ValueError('negative step')
    return prior.H**2 * prior.TAUMAX / prior.INERTIA * step * (step-1) / 2


def adversarial_acceleration_lower(step: int):
    """Exact lower bound on -T*sin(phi_k)+R(T) for all legal T,tau histories.

    The Taylor s5 upper bound and monotonicity of sin on [-0.45,0.45]
    imply sin(phi_k)<=s5(tilt_upper(k)). The affine thrust minimum is
    attained at an endpoint, chosen separately for each step.
    """
    phi=tilt_upper(step)
    if phi > prior.PHIMAX:
        raise ValueError('tilt envelope exceeds certified sine domain')
    s5=prior.sine_bounds(phi)[1]
    slope=prior.RT-s5
    t=prior.TMIN if slope>=0 else prior.TMAX
    return prior.R0+t*slope,t


def position_guard(horizon=HORIZON):
    if horizon<1: raise ValueError('empty horizon')
    p=Q(0);v=Q(0);rows=[]
    for k in range(horizon):
        a,t=adversarial_acceleration_lower(k)
        p+=prior.H*v
        v+=prior.H*a
        rows.append({'step':k+1,'phi_upper':str(tilt_upper(k)),
                     'worst_thrust_for_lower_bound':str(t),
                     'acceleration_lower':str(a),
                     'position_displacement_lower':str(p),
                     'velocity_lower':str(v)})
    return {'horizon':horizon,'minimum_outward_displacement':p,
            'positive_position_threshold':prior.PMAX-p,'rows':rows}


def verify(root=None):
    if root is not None: prior.config_contract(root)
    d=position_guard()
    assert tilt_upper(24)==Q(276,625) # 0.4416 rad, within 0.45
    assert tilt_upper(24)<prior.PHIMAX
    assert d['minimum_outward_displacement']>Q(1,8)
    assert Q(49,10)>d['positive_position_threshold']
    assert d['rows'][0]['worst_thrust_for_lower_bound']==str(prior.TMIN)
    assert d['rows'][-1]['worst_thrust_for_lower_bound']==str(prior.TMAX)
    return {'run':'230','base_main':BASE_MAIN,
            'model':'Frozen Run224 Euler four-state, full-state causal inputs, independent Run208/210 residual',
            'adversary':'r_k=+R(T_k) for positive-boundary witness; sign mirror for negative boundary',
            'claim':'All causal admissible controls from (p0,0,0,0) with p0>threshold must violate |p|<=5 by or before step 25 under a legal disturbance sequence; symmetric for p0<-threshold.',
            'horizon':HORIZON,'outward_displacement_lower':str(d['minimum_outward_displacement']),
            'positive_position_threshold':str(d['positive_position_threshold']),
            'strict_positive_witness_p0':'49/10',
            'strict_positive_witness_p25_lower':str(Q(49,10)+d['minimum_outward_displacement']),
            'negative_witness_is_sign_mirror':True,
            'rows':d['rows'],'gate_A':'blocked',
            'limitations':['A necessary exclusion on the zero-velocity/zero-attitude/zero-rate slice only, not an RCI emptiness theorem.',
                           'Relies on independently adversarial Run208/210 residual at every sample; not a physical wind persistence model.',
                           'Does not construct a closed terminal graph, SMF output feedback MPC, or recursive feasibility.',
                           'No worst-case solver time or six-state safety result.']}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path);ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    s=json.dumps(verify(args.root),indent=2,ensure_ascii=False,sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(s)
    else: print(s,end='')

if __name__=='__main__': main()
