#!/usr/bin/env python3
"""Run252: exact necessary velocity-fiber growth during two legal missed position packets.

This is NOT a terminal invariant set, closed-loop MPC controller, or proof of
recursive feasibility. Reuses Run251's one admissible common output history.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as F
from pathlib import Path
from check_velocity_indistinguishability import H, R, lateral_witness

T = F(981, 100)
J = H
U = F(2, 25)
P_MAX, V_MAX, PHI_MAX, OMEGA_MAX = F(5), F(3), F(9, 20), F(2)


def envelope(j: int):
    """Sound absolute bounds for either true path and ANY shared |tau|<=U."""
    assert 0 <= j <= 10
    a = lateral_witness(15)['necessary_posterior_halfwidth']
    phi = lambda i: H * U * i * (i - 1) / 2
    vel = lambda i: a + i * H * R + H * T * sum(phi(k) for k in range(i))
    return {'p': H * sum(vel(i) for i in range(j)),
            'v': vel(j), 'phi': phi(j), 'omega': j * U}


def velocity_gap(j: int):
    """Difference independent of every shared torque; opposite future residuals."""
    assert 0 <= j <= 10
    return lateral_witness(15)['terminal_velocity_gap'] + 2 * j * H * R


def verify():
    witness = lateral_witness(15)
    assert witness['records'][-1][1:3] == (F(0), F(0))
    assert all(e <= F(1, 50) for e in witness['observed_half_separation'].values())
    assert all(envelope(j)['p'] < P_MAX and envelope(j)['v'] < V_MAX
               and envelope(j)['phi'] < PHI_MAX and envelope(j)['omega'] < OMEGA_MAX
               for j in range(11))
    assert velocity_gap(5) == F(74666809, 80000000)
    assert velocity_gap(10) == F(107130639, 80000000)
    return {
        'run': 252,
        'basis': 'Run251 same initial state and common successful position observations at ticks 5/10/15',
        'dropout_word_at_position_opportunities': 'SSSMM',
        'evidence': 'EXACT_RATIONAL_CAUSAL_TWO_MISS_VELOCITY_DIAMETER_NECESSARY_BOUND',
        'quantifiers': 'after the specific Run251 zero-torque prefix, for every causal admissible torque continuation choose two legal residual sequences and identical available noisy observations',
        'witness': 'two physical paths; common angular measurements at every tick; no position measurement at 20/25',
        'assumptions': 'frozen fixed-thrust four-state Euler, independent lateral residual, no extra velocity/IMU measurement',
        'bounds': [{
            'tick': 15 + j,
            'necessary_velocity_diameter_m_s': str(velocity_gap(j)),
            'necessary_velocity_halfwidth_m_s': str(velocity_gap(j) / 2),
            'universal_true_state_abs_envelope': {k: str(v) for k, v in envelope(j).items()},
        } for j in (0, 5, 10)],
        'safety_scope': 'both adversarial paths remain within all state bounds through tick25 for any shared admissible torque continuation after tick15',
        'limitation': 'one admissible observation history and loss word, not a uniform lower bound for all SMF posteriors; does not disprove existence of safe feedback',
        'terminal_invariant_set_proved': False,
        'recursive_feasibility_proved': False,
        'gate_A': 'blocked',
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    result = json.dumps(verify(), ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result)
    else:
        print(result, end='')


if __name__ == '__main__':
    main()
