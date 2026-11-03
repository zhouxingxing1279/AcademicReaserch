#!/usr/bin/env python3
"""Run231: exact 25-step exclusion of positive-volume four-state terminal cells.

A legal disturbance r_k=+R(T_k) is selected after every causal control.
The certificate excludes whole initial boxes, not merely Run230's zero-state
slice. It is a necessary safety test, NOT an RCI construction or SMF result.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as Q
from pathlib import Path
import check_four_state_bridge_graph as plant

HORIZON = 25
BASE_MAIN = 'b6ab233a2188a138f9ef64d76418827a52fb37f4'


def mirror_box(box):
    """Reflect (p,v,phi,omega) to exploit the exact sign symmetry."""
    return tuple((-hi, -lo) for lo, hi in box)


def positive_position_guard(box, horizon=HORIZON):
    """Lower bound p_h for every causal controller and all x0 in box.

    Adversary r=+R(T), selected after each input. The proof applies if
    the trajectory stays in the physical safe domain until horizon; if it
    leaves earlier, safety is already violated. Thus a lower bound >5
    proves finite-horizon unsafety for the *entire* initial box.
    """
    if not plant.within_domain(box):
        raise ValueError('initial cell outside physical constraints')
    if not 1 <= horizon <= HORIZON:
        raise ValueError('unsupported horizon')
    p_lower, v_lower = box[0][0], box[1][0]
    phi_upper, omega_upper = box[2][1], box[3][1]
    rows = []
    for k in range(horizon):
        tilt_upper = (phi_upper + k*plant.H*omega_upper
                      + plant.H**2*plant.TAUMAX/plant.INERTIA*k*(k-1)/2)
        if not -plant.PHIMAX <= tilt_upper <= plant.PHIMAX:
            raise ValueError('tilt upper envelope outside certified sine domain')
        sine_upper = plant.sine_bounds(tilt_upper)[1]
        a_lower, minimizing_t = min(
            ((plant.R0+t*(plant.RT-sine_upper), t)
             for t in (plant.TMIN, plant.TMAX)), key=lambda z: z[0])
        p_lower += plant.H*v_lower
        v_lower += plant.H*a_lower
        rows.append({'step': k+1, 'tilt_upper': str(tilt_upper),
                     'minimizing_thrust': str(minimizing_t),
                     'position_lower': str(p_lower),
                     'velocity_lower': str(v_lower)})
    return {'horizon': horizon, 'position_lower': p_lower,
            'velocity_lower': v_lower, 'strict_exclusion': p_lower > plant.PMAX,
            'rows': rows}


def witness_box():
    e = Q(1, 200)
    return plant.make_box((Q(49,10), Q(491,100)), (-e,e), (-e,e), (-e,e))


def box_json(box):
    return [[str(lo), str(hi)] for lo,hi in box]


def verify(root=None):
    if root is not None:
        plant.config_contract(root)
    positive = witness_box()
    negative = mirror_box(positive)
    d = positive_position_guard(positive)
    m = positive_position_guard(mirror_box(negative))
    assert plant.within_domain(positive) and plant.within_domain(negative)
    assert d['strict_exclusion'] and m['strict_exclusion']
    assert d['position_lower'] == Q(5) + Q(461731712952866342887537,25000000000000000000000000)
    assert d['position_lower'] == m['position_lower']
    zero_slice = plant.make_box((Q(49,10),Q(49,10)), (0,0),(0,0),(0,0))
    assert positive_position_guard(zero_slice)['position_lower'] == Q(49,10) + Q(98296135986106564467,762939453125000000000)
    center = plant.make_box((0,0),(0,0),(0,0),(0,0))
    assert not positive_position_guard(center)['strict_exclusion']
    return {'run':'231', 'base_main':BASE_MAIN,
            'model':'frozen four-state Euler; full-state causal control; independent |r|<=R(T)',
            'positive_cell':box_json(positive), 'negative_cell':box_json(negative),
            'adversary':'r_k=sign(boundary)*R(T_k), after the causal thrust choice',
            'horizon':HORIZON, 'positive_cell_p25_lower':str(d['position_lower']),
            'strict_margin_above_pmax':str(d['position_lower']-plant.PMAX),
            'both_full_cells_excluded':True,
            'run230_zero_slice_reproduced':True,
            'gate_A':'blocked',
            'limitations':['Only these finite-horizon terminal-cell exclusions; no global RCI emptiness result.',
                           'Relies on independently adversarial residual at each sample.',
                           'No nonempty closed terminal graph, four-state SMF/MPC recursive feasibility, or six-state safety.',
                           'No 20ms worst-case timing guarantee or full historical regression.']}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',type=Path)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    s=json.dumps(verify(args.root),ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(s)
    else:
        print(s,end='')

if __name__=='__main__':main()
