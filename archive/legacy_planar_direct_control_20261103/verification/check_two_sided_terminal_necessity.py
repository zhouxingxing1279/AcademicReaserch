#!/usr/bin/env python3
"""Run223: exact necessary tilt-span obstruction for frozen lateral Euler model.

This is NOT a construction of a robust controlled invariant (RCI) set.
The lateral residual is an independently adversarial Run208/210 envelope.
"""
from __future__ import annotations

import argparse
import json
from fractions import Fraction as Q
from pathlib import Path

H = Q(1, 50)
T_MIN, T_MAX = Q(981, 200), Q(2943, 200)
R0, RT = Q(47, 25), Q(243, 16000)
PHI_LIMIT, OMEGA_LIMIT, V_LIMIT = Q(9, 20), Q(2), Q(3)
RADII = (Q(3, 50), Q(7, 50), Q(717, 5000), Q(3, 20))


def sin_upper(radius):
    """sin(r) <= r-r^3/6+r^5/120 for 0<=r<=0.45 (Taylor alternating)."""
    if not Q(0) <= radius <= PHI_LIMIT:
        raise ValueError('radius outside certified angular domain')
    return radius - radius**3/Q(6) + radius**5/Q(120)


def drift_acceleration_lower(radius):
    """For phi<=radius, r_x=+R(T), all admissible T.

    Symmetrically, phi>=-radius, r_x=-R(T) forces -vx drift.
    """
    s = sin_upper(radius)
    return min(R0 + (RT-s)*t for t in (T_MIN, T_MAX))


def first_strict_crossing_from_minus_limit(delta):
    """Positive drift per tick; first n with -V_LIMIT+n*delta > V_LIMIT."""
    if delta <= 0:
        raise ValueError('no strictly positive certified drift')
    ratio = 2*V_LIMIT/delta
    return ratio.numerator//ratio.denominator + 1


def minimum_tilt_reversal_ticks(radius):
    """Only a kinematic bound, NOT a requirement that a reversal occurs."""
    ratio = 2*radius/(H*OMEGA_LIMIT)
    return (ratio.numerator + ratio.denominator - 1)//ratio.denominator


def config_contract(root):
    c = json.loads((Path(root)/'configs/planar_baseline.json').read_text(), parse_float=Q)
    assert c['plant']['truth_semantics'] == 'defined_discrete_euler'
    assert Q(c['plant']['dt_s']) == H
    assert Q(c['domain']['input_lower'][0]) == T_MIN
    assert Q(c['domain']['input_upper'][0]) == T_MAX
    assert Q(c['domain']['state_lower'][2]) == -V_LIMIT
    assert Q(c['domain']['state_upper'][2]) == V_LIMIT
    assert Q(c['domain']['state_lower'][4]) == -PHI_LIMIT
    assert Q(c['domain']['state_upper'][4]) == PHI_LIMIT
    assert Q(c['domain']['state_upper'][5]) == OMEGA_LIMIT
    return True


def verify(root=None):
    if root is not None:
        config_contract(root)
    rows=[]
    for radius in RADII:
        accel=drift_acceleration_lower(radius)
        row={'radius':str(radius), 'sin_upper':str(sin_upper(radius)),
             'adversarial_acceleration_lower':str(accel),
             'positive_drift_obstruction':accel>0}
        if accel>0:
            step=H*accel
            n=first_strict_crossing_from_minus_limit(step)
            assert (n-1)*step<=2*V_LIMIT<n*step
            row.update(velocity_step_lower=str(step),
                       uniform_crossing_ticks=n,
                       uniform_crossing_seconds=str(n*H))
        rows.append(row)
    assert all(r['positive_drift_obstruction'] for r in rows[:3])
    assert not rows[3]['positive_drift_obstruction']
    return {
        'run':'223', 'base':'Run222 frozen lateral Euler and Run208/210 residual envelope',
        'evidence':'EXACT_RATIONAL_TAYLOR_UPPER_AND_ADVERSARIAL_DRIFT',
        'rows':rows,
        'necessary_projection':'Any nonempty robust controlled invariant C must have sup_C(phi)>717/5000 and inf_C(phi)<-717/5000.',
        'minimum_reversal_ticks_if_opposite_thresholds_are_visited':minimum_tilt_reversal_ticks(Q(717,5000)),
        'gate_A':'blocked',
        'limitations':[
            'Necessary condition only; does not prove existence or nonexistence of a wider four-state terminal kernel.',
            'Uses independently selectable lateral residual +/-[47/25+(243/16000)T] every tick, not verified persistent physical aerodynamics.',
            'Reversal ticks are a kinematic lower bound only, not a guaranteed or required transition.',
            'No four-state SMF-MPC rollout, recursive feasibility, stability, or six-state guarantee.'
        ]
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--root',type=Path)
    p.add_argument('--output',type=Path)
    a=p.parse_args()
    data=json.dumps(verify(a.root),indent=2,sort_keys=True,ensure_ascii=False)+'\n'
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(data)
    else:
        print(data,end='')

if __name__=='__main__':main()
