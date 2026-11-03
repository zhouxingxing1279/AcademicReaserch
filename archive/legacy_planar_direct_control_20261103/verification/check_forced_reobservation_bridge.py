#!/usr/bin/env python3
"""Run253: exact finite bridge and forced-success separation for Run251/252 witnesses.

NOT a terminal invariant set, a full SMF posterior certificate, or a proof of
infinite-horizon recursive feasibility. All calculations use Fraction.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

H = J = F(1, 50)
T = F(981, 100)
R = F(3246383, 1600000)
U = F(2, 25)
NOISE_P = F(1, 50)
D15 = F(42202979, 80000000)  # Run251 verified pair
LIMITS = {'p': F(5), 'v': F(3), 'phi': F(9, 20), 'omega': F(2)}
BRIDGE = (F(1, 25), F(-1, 25), F(-1, 25), F(1, 25), F(0))


def envelope(j: int):
    """Sound abs bound from tick15 for either path, any shared |tau|<=U.

    Initial positions/angles/rates are exactly zero, initial |v|=D15/2.
    |sin(phi)|<=|phi| makes the rational bound conservative but rigorous.
    """
    assert 0 <= j <= 15
    phi = lambda i: H * U * i * (i - 1) / 2
    vel = lambda i: D15 / 2 + i * H * R + H * T * sum(phi(k) for k in range(i))
    return {'p': H * sum(vel(i) for i in range(j)),
            'v': vel(j), 'phi': phi(j), 'omega': j * U}


def gaps():
    """Two Run251 paths: opposite residuals on ticks15..24; then arbitrary.

    Common torques give identical angular states, so -T*sin(phi) cancels in
    pairwise differences exactly, independently of the common torque history.
    """
    dp25 = 10 * H * D15 + 2 * H**2 * R * sum(range(10))
    dv25 = D15 + 2 * 10 * H * R
    dp30_min = dp25 + 5 * H * dv25 - 2 * H**2 * R * sum(range(5))
    dp30_max = dp25 + 5 * H * dv25 + 2 * H**2 * R * sum(range(5))
    return dp25, dv25, dp30_min, dp30_max


def verify(root=None):
    assert all(abs(t) <= U for t in BRIDGE)
    assert any(t != 0 for t in BRIDGE)
    assert sum(BRIDGE) == 0
    for j in range(16):
        assert all(v < LIMITS[k] for k, v in envelope(j).items()), (j, envelope(j))
    assert envelope(10)['v'] == F(113157903, 160000000)
    assert envelope(10)['p'] == F(181187993, 2000000000)
    dp25, dv25, dp30_min, dp30_max = gaps()
    assert dv25 == F(107130639, 80000000)
    assert dp25 == F(35710213, 200000000)
    assert dp30_min == F(236985959, 800000000)
    assert dp30_min > 2 * NOISE_P
    assert dp30_max >= dp30_min
    if root is not None:
        cfg = json.loads((Path(root) / 'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics'] == 'defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s'])) == H
        assert F(str(cfg['plant']['inertia_kg_m2'])) == J
        assert F(str(cfg['plant']['gravity_m_s2'])) == T
        assert F(str(cfg['domain']['input_upper'][1])) == U
        assert cfg['sensing']['position_period_ticks'] == 5
        assert cfg['sensing']['max_consecutive_missed_packets'] == 2
        assert F(str(cfg['sensing']['observed_noise_halfwidth']['px'])) == NOISE_P
        from check_velocity_indistinguishability import lateral_witness
        from check_dropout_velocity_fiber import velocity_gap, envelope as old_envelope
        assert lateral_witness(15)['terminal_velocity_gap'] == D15
        assert velocity_gap(10) == dv25
        assert all(old_envelope(j) == envelope(j) for j in range(11))
    return {
        'run': 253,
        'model': 'Run249 fixed-thrust four-state discrete Euler, exact rational conservative envelope',
        'evidence': 'EXACT_FINITE_CAUSAL_BRIDGE_AND_FORCED_POSITION_OBSERVATION_SEPARATION',
        'history': 'Run251 0-15 zero torque, same noisy outputs; Run252 15-25 opposite extreme lateral residuals, common arbitrary torque; loss word SSSMM',
        'bridge_nonzero_common_torque_Nm': [str(t) for t in BRIDGE],
        'scope': 'both Run251/252 witness paths, every shared admissible torque 15..29, all admissible residuals 25..29; not all SMF-consistent states',
        'safety_all_intermediate_ticks_15_to_30': True,
        'worst_abs_envelope_tick30': {k: str(v) for k, v in envelope(15).items()},
        'pair_position_gap_tick25_m': str(dp25),
        'pair_velocity_gap_tick25_m_s': str(dv25),
        'pair_position_gap_tick30_lower_m': str(dp30_min),
        'pair_position_gap_tick30_upper_m': str(dp30_max),
        'same_success_position_reading_at_tick30_possible': False,
        'measurement_strip_pair_separation_margin_m': str(dp30_min - 2 * NOISE_P),
        'forced_success_tick30': True,
        'after_success_single_posterior_position_diameter_upper_m': str(2 * NOISE_P),
        'caveat': 'successful position packet distinguishes THESE two trajectories; does not identify velocity uniquely or certify full posterior successor/terminal invariance',
        'recursive_feasibility_proved': False,
        'terminal_invariant_set_proved': False,
        'gate_A': 'blocked',
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    payload = json.dumps(verify(args.root), ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload)
    else:
        print(payload, end='')

if __name__ == '__main__':
    main()
