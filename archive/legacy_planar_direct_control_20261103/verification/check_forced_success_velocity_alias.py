#!/usr/bin/env python3
"""Run254: exact hidden-velocity alias after a forced successful position packet.

Constructive necessary posterior diameter for ONE legitimate observation history
plus a sound Run249 interval-SMF outer box. NOT an exact posterior or terminal RCI.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as F
from pathlib import Path
from check_four_state_shielded_smf_mpc import (
    H, J, T, R, U, INIT, NOISE, KEYS, P_MAX, V_MAX, PHI_MAX, OMEGA_MAX,
    step, strip, safe)

LIMITS = {'p': P_MAX, 'v': V_MAX, 'phi': PHI_MAX, 'omega': OMEGA_MAX}
SUCCESS = (5, 10, 15, 30)
MISSED = (20, 25)
PATTERN = (F(-3, 4),) * 5 + (F(1),) * 10


def truth_path(sign):
    """Exact Euler trajectory, zero torque, zero initial state."""
    assert sign in (-1, 1)
    p = v = phi = omega = F(0)
    out = [{'p': p, 'v': v, 'phi': phi, 'omega': omega}]
    for k in range(30):
        r = F(0) if k < 15 else sign * PATTERN[k-15] * R
        assert abs(r) <= R
        p, v, phi, omega = (p + H*v, v + H*r,
                             phi + H*omega, omega + H/J*F(0))
        out.append({'p': p, 'v': v, 'phi': phi, 'omega': omega})
    return out


def outer_history():
    """Run249 sound interval SMF for zero-valued available measurements."""
    s = dict(INIT)
    rows = [dict(s)]
    for k in range(1, 31):
        obs = {'phi': F(0), 'omega': F(0)}
        if k in SUCCESS:
            obs['p'] = F(0)
        s = strip(step(s, F(0)), obs)
        assert s is not None
        assert safe(s), (k, s)
        rows.append(s)
    return rows


def verify(root=None):
    plus, minus = truth_path(1), truth_path(-1)
    rows = outer_history()
    assert len(plus) == len(minus) == len(rows) == 31
    assert sum(F(14-i)*PATTERN[i] for i in range(15)) == 0
    assert sum(PATTERN) == F(25, 4)
    assert plus[30]['p'] == minus[30]['p'] == 0
    assert plus[30]['v'] == R/8 and minus[30]['v'] == -R/8
    assert plus[30]['v'] - minus[30]['v'] == R/4
    for k in range(31):
        for path in (plus[k], minus[k]):
            assert all(abs(path[key]) <= LIMITS[key] for key in KEYS)
            assert all(rows[k][key][0] <= path[key] <= rows[k][key][1]
                       for key in KEYS), (k, path, rows[k])
            if k in SUCCESS:
                assert abs(path['p']) <= NOISE['p']
            assert path['phi'] == path['omega'] == 0
    assert rows[30]['p'] == (-NOISE['p'], NOISE['p'])
    assert rows[30]['v'] == (-F(269364701, 200000000),
                              F(269364701, 200000000))
    assert all(plus[k]['p'] == minus[k]['p'] == 0 for k in SUCCESS)
    if root is not None:
        cfg = json.loads((Path(root)/'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics'] == 'defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s'])) == H
        assert F(str(cfg['plant']['inertia_kg_m2'])) == J
        assert F(str(cfg['plant']['gravity_m_s2'])) == T
        assert F(str(cfg['domain']['input_upper'][1])) == U
        assert cfg['sensing']['position_period_ticks'] == 5
        assert cfg['sensing']['max_consecutive_missed_packets'] == 2
        assert F(str(cfg['sensing']['observed_noise_halfwidth']['px'])) == NOISE['p']
    return {
        'run': 254,
        'evidence': 'EXACT_RATIONAL_CONSTRUCTIVE_VELOCITY_ALIAS_AT_FORCED_SUCCESS',
        'model': 'Run249 fixed-thrust four-state defined discrete Euler; zero common torque',
        'position_packet_word_ticks_5_to_30': 'SSSMMS',
        'successful_position_readings': {str(k): '0' for k in SUCCESS},
        'angular_and_rate_readings': 'zero at every tick, with zero measurement noise',
        'lateral_residual_plus_ticks_15_to_19': '-3R/4',
        'lateral_residual_plus_ticks_20_to_29': '+R',
        'lateral_residual_minus': 'negative of plus path',
        'r_bound_m_s2': str(R),
        'terminal_position_both_m': '0',
        'terminal_velocity_plus_m_s': str(plus[30]['v']),
        'terminal_velocity_minus_m_s': str(minus[30]['v']),
        'necessary_true_posterior_velocity_diameter_m_s': str(R/4),
        'run249_interval_smf_outer_velocity_diameter_m_s': str(rows[30]['v'][1]-rows[30]['v'][0]),
        'run249_interval_smf_outer_position_diameter_m': str(rows[30]['p'][1]-rows[30]['p'][0]),
        'max_abs_truth_position_m': str(max(abs(s['p']) for path in (plus,minus) for s in path)),
        'max_abs_truth_velocity_m_s': str(max(abs(s['v']) for path in (plus,minus) for s in path)),
        'all_truth_ticks_safe': True,
        'all_truth_ticks_contained_in_run249_smf': True,
        'scope': 'one legal zero-valued measurement history; necessary lower and interval outer upper bounds, NOT exact true posterior diameter',
        'terminal_invariant_set_proved': False,
        'recursive_feasibility_proved': False,
        'gate_A': 'blocked',
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    result = json.dumps(verify(args.root), sort_keys=True, indent=2, ensure_ascii=False) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result)
    else:
        print(result, end='')


if __name__ == '__main__':
    main()
