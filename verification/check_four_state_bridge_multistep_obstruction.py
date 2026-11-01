#!/usr/bin/env python3
"""Run232: exact all-control finite-horizon obstruction for a narrow central bridge.

Frozen four-state Euler model. From the origin, a causal controller cannot
instantaneously rotate the plant. An adversary selects r_k=+/-R(T_k) after
thrust. The resulting rational velocity envelope excludes the three-mode
Run228 bridge candidate for 14-step safety, even with full-state feedback.

This is NOT an empty-RCI proof for the physical safe set, nor an SMF result.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as Q
from pathlib import Path
import check_four_state_bridge_graph as plant

BASE_MAIN = '0f05bf4273be2f00b5731e3a371a1500f7177236'
HORIZON = 14
MODE_TILT_FLOOR = Q(3,20)  # Run228 positive/negative modes begin at |phi|=0.15


def tilt_envelope(step):
    """All-control |phi_step| bound from phi0=omega0=0, |tau|<=tau_max."""
    if not isinstance(step,int) or step<0:
        raise ValueError('step must be a nonnegative integer')
    return (plant.H**2 * plant.TAUMAX / plant.INERTIA
            * step * (step-1) / 2)


def adversarial_velocity_envelope(steps=HORIZON):
    """Uniform v_k lower bound for r=+R(T); mirror upper bound for -R(T).

    The controller may observe the full state and choose arbitrary legal
    thrust/torque at every tick. For all k<=steps, |phi_k|<=alpha_k.
    Since sin is increasing on [-0.45,0.45], sin(phi_k)<=s5(alpha_k).
    Thus dv>=h*(R0+min_T T*(RT-s5(alpha_k))), with affine min at
    TMIN or TMAX. Every operation and the Taylor enclosure are rational.
    """
    if not isinstance(steps,int) or not 1<=steps<=HORIZON:
        raise ValueError('steps must be an integer in [1,14]')
    velocity=Q(0)
    position=Q(0)
    rows=[]
    for k in range(steps):
        alpha=tilt_envelope(k)
        if alpha>plant.PHIMAX:
            raise ValueError('tilt envelope outside sine domain')
        sine_upper=plant.sine_bounds(alpha)[1]
        acceleration,thrust=min(
            ((plant.R0+t*(plant.RT-sine_upper),t)
             for t in (plant.TMIN,plant.TMAX)),key=lambda pair:pair[0])
        position+=plant.H*velocity
        velocity+=plant.H*acceleration
        rows.append({'tick':k+1,'tilt_before_step_upper':str(alpha),
                     'thrust_endpoint_minimizer':str(thrust),
                     'acceleration_lower':str(acceleration),
                     'velocity_lower':str(velocity),
                     'position_lower':str(position)})
    alpha_final=tilt_envelope(steps)
    if alpha_final>=MODE_TILT_FLOOR:
        raise ValueError('final tilt may reach an outer mode')
    return {'steps':steps,'velocity_lower':velocity,'position_lower':position,
            'tilt_absolute_upper_at_final':alpha_final,'rows':rows}


def bridge_obstruction(width,steps=HORIZON):
    """If the origin belongs to a bridge |v|<=width and every other mode
    excludes |phi|<0.15, then v_steps>width proves union non-invariance.

    A failed test means only that THIS adversarial certificate is inconclusive.
    """
    width=Q(width)
    if width<=0 or width>plant.VMAX:
        raise ValueError('bridge velocity halfwidth outside physical domain')
    d=adversarial_velocity_envelope(steps)
    first=next((row['tick'] for row in d['rows']
                if Q(row['velocity_lower'])>width),None)
    return {'bridge_velocity_halfwidth':str(width),
            'strict_noninvariance':first is not None,
            'first_forced_velocity_exit_tick':first,
            'velocity_lower_at_horizon':str(d['velocity_lower']),
            'tilt_upper_at_horizon':str(d['tilt_absolute_upper_at_final']),
            'positive_adversary':'r_k=+R(T_k) chosen after causal control',
            'negative_mirror':'r_k=-R(T_k) yields v_k<=-v_lower_k',
            'scope':'origin-containing three-mode bridge with no other cell at |phi|<0.15'}


def verify(root=None):
    if root is not None:
        plant.config_contract(root)
    assert tilt_envelope(HORIZON)==Q(91,625)
    assert tilt_envelope(HORIZON)<MODE_TILT_FLOOR
    d=adversarial_velocity_envelope()
    assert all(Q(row['acceleration_lower'])>0 for row in d['rows'])
    assert d['velocity_lower']>Q(2,5)  # >0.4 m/s even under all legal controls
    assert d['velocity_lower']<Q(41,100)
    cases={name:bridge_obstruction(width) for name,width in
           [('run228_narrow',Q(3,100)),('run228_expanded',Q(1,20)),
            ('width_0p40',Q(2,5)),('width_0p41',Q(41,100))]}
    assert cases['run228_narrow']['first_forced_velocity_exit_tick']==1
    assert cases['run228_expanded']['first_forced_velocity_exit_tick']==2
    assert cases['width_0p40']['first_forced_velocity_exit_tick']==13
    assert not cases['width_0p41']['strict_noninvariance']
    return {'run':'232','base_main':BASE_MAIN,'model':'frozen four-state Euler with independent |r|<=R(T)',
            'quantifiers':'forall full-state causal controls, exists legal adversarial residual policy',
            'horizon':HORIZON,'outer_mode_tilt_floor':str(MODE_TILT_FLOOR),
            'terminal_tilt_absolute_upper':str(d['tilt_absolute_upper_at_final']),
            'necessary_bridge_velocity_halfwidth':str(d['velocity_lower']),
            'rows':d['rows'],'cases':cases,'gate_A':'blocked',
            'limitations':['Excludes only origin-containing three-mode candidates with no alternative small-tilt cells.',
                           'No proof of global RCI emptiness, nonempty terminal RCI, output-feedback MPC safety or stability.',
                           'The independent per-tick worst-case residual is a model contract, not a measured aerodynamic trajectory.',
                           'An inconclusive width (e.g. 0.41) is not a positive invariance certificate.']}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    s=json.dumps(verify(args.root),ensure_ascii=False,indent=2,sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(s)
    else:print(s,end='')

if __name__=='__main__':main()
