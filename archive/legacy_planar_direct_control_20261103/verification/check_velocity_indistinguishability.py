#!/usr/bin/env python3
"""Run251: exact indistinguishable-disturbance velocity-width certificate.

Scope: Run249 frozen four-state Euler model, fixed T=9.81, lateral residual
|r_k|<=R, noisy position every 5 ticks, always observed angle/rate.
This is a *necessary* posterior width for one feasible output history, not
an invariant terminal set or an MPC feasibility/safety certificate.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

H = F(1, 50)
R = F(3246383, 1600000)
POSITION_NOISE = F(1, 50)
POSITION_LIMIT = F(5)
VELOCITY_LIMIT = F(3)


def optimum_deltas(n: int):
    """Exact primal/dual optimum for max sum(d_w), sum(w*d_w)=0, |d_w|<=1.

    Index w=0 is the last residual (no contribution to measured p_n).
    A weighted-median dual lambda=1/pivot supplies a sharp upper bound.
    """
    assert n >= 3
    weights = range(n)
    for pivot in range(1, n):
        heavier = sum(w for w in weights if w > pivot)
        lighter = sum(w for w in weights if w < pivot)
        if abs(heavier - lighter) <= pivot:
            break
    else:
        raise AssertionError('weighted median pivot absent')
    d = {w: (F(1) if w < pivot else F(-1) if w > pivot
             else F(heavier - lighter, pivot)) for w in weights}
    assert all(-1 <= x <= 1 for x in d.values())
    assert sum(w * d[w] for w in weights) == 0
    primal = sum(d.values())
    dual = sum(abs(1 - F(w, pivot)) for w in weights)
    assert primal == dual
    return pivot, d, primal, dual


def lateral_witness(n: int):
    pivot, d, primal, dual = optimum_deltas(n)
    p_plus = p_minus = v_plus = v_minus = F(0)
    records = [(0, p_plus, p_minus, v_plus, v_minus)]
    for i in range(n):
        residual = R * d[n - 1 - i]
        p_plus, p_minus, v_plus, v_minus = (
            p_plus + H * v_plus, p_minus + H * v_minus,
            v_plus + H * residual, v_minus - H * residual)
        records.append((i + 1, p_plus, p_minus, v_plus, v_minus))
        assert abs(p_plus) <= POSITION_LIMIT and abs(p_minus) <= POSITION_LIMIT
        assert abs(v_plus) <= VELOCITY_LIMIT and abs(v_minus) <= VELOCITY_LIMIT
        assert p_plus == -p_minus and v_plus == -v_minus
    assert p_plus == p_minus == 0  # exact identical terminal position
    assert v_plus - v_minus == 2 * H * R * primal
    observed = {k: abs(records[k][1]) for k in range(5, n + 1, 5)}
    assert all(e <= POSITION_NOISE for e in observed.values())
    # The common position observation can be the midpoint of the two paths;
    # common angle/rate measurements are 0 under zero torque and phi0=omega0=0.
    # Even if packets at all 5-tick opportunities succeed, both paths agree.
    return {'n': n, 'pivot': pivot, 'd_by_weight': d, 'primal': primal,
            'dual': dual, 'records': records, 'observed_half_separation': observed,
            'terminal_velocity_gap': v_plus - v_minus,
            'necessary_posterior_halfwidth': (v_plus - v_minus) / 2}


def verify():
    data = [lateral_witness(n) for n in (5, 10, 15)]
    long = data[-1]
    assert long['pivot'] == 10
    assert long['primal'] == F(13, 2)
    assert long['terminal_velocity_gap'] == F(42202979, 80000000)
    assert long['necessary_posterior_halfwidth'] == F(42202979, 160000000)
    return {
        'run': 251,
        'model': 'Run249 frozen four-state Euler, fixed thrust, independent bounded lateral residual',
        'evidence': 'EXACT_RATIONAL_TWO_INDISTINGUISHABLE_TRAJECTORIES_AND_SHARP_RESTRICTED_LP_DUAL',
        'initial_true_state': ['0', '0', '0', '0'],
        'shared_control': 'tau=0; same angular observations; all position packets can succeed',
        'position_noise_halfwidth_m': str(POSITION_NOISE),
        'residual_bound_m_s2': str(R),
        'h_s': str(H),
        'certificates': [{
            'ticks': a['n'], 'dual_pivot_weight': a['pivot'],
            'residual_multipliers_by_weight_0_to_n_minus_1': [str(a['d_by_weight'][w]) for w in range(a['n'])],
            'primal_sum': str(a['primal']), 'dual_upper': str(a['dual']),
            'observed_position_half_separation_m': {str(k): str(v) for k, v in a['observed_half_separation'].items()},
            'terminal_velocity_gap_m_s': str(a['terminal_velocity_gap']),
            'necessary_velocity_posterior_halfwidth_m_s': str(a['necessary_posterior_halfwidth']),
            'all_intermediate_true_states_safe_for_zero_torque': True,
            'same_position_observation_at_all_5_tick_opportunities': True,
        } for a in data],
        'claim_scope': 'one physically admissible common noisy output history, not a universal lower bound for every posterior',
        'restricted_lp_optimality': 'exact terminal position equality, antisymmetric bounded residual pairs, fixed common initial state',
        'terminal_invariant_set_proved': False,
        'recursive_feasibility_proved': False,
        'six_state_guarantee': False,
        'gate_A': 'blocked',
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    payload = json.dumps(verify(), ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload)
    else:
        print(payload, end='')


if __name__ == '__main__':
    main()
