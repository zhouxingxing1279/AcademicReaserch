#!/usr/bin/env python3
"""Run260: 15-tick measurement-independent shared zero-torque safety bridge.

The two starting sets are SOUND OUTER BOXES of ONE fixed zero-reading
Run254/259 history, not exact posteriors. No future measurements are used
during this bridge: every future noise-consistent posterior is a subset
of the unconditioned predicted box. This is NOT a terminal invariant set.
"""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

from check_run255_posterior_bridge import (
    H, J, T, R, NOISE, LIMIT, PULSE, posterior30, step, safe,
)
from check_run256_interval_information_limit import observe
from check_run258_delayed_anchor import meet, velocity_from_position_anchor
from check_run259_rolling_anchor import acceleration, roll


def posterior_at_45(pattern):
    """Replay the frozen zero-reading history, preserving Run259's reset rule."""
    if pattern not in ('SMM', 'MMS'):
        raise ValueError("Only the two specified Run259 worst-case packet modes")
    s = posterior30()
    anchor = s['p']
    accelerations = []
    for k in range(30, 45):
        accelerations.append(acceleration(s))
        s = step(s, PULSE[k - 30] if k < 35 else F(0))
        tick = k + 1
        if tick >= 35:
            s = observe(s, {'phi': F(0), 'omega': F(0)})
            assert s is not None
        if tick in (35, 40, 45) and pattern[(tick - 35)//5] == 'S':
            s = observe(s, {'p': F(0)})
            assert s is not None
            s = dict(s)
            s['v'] = meet(s['v'], velocity_from_position_anchor(
                F(0), anchor, accelerations))
            assert s['v'][0] <= s['v'][1]
            anchor = s['p']
            accelerations = []
        assert safe(s)
    previous, memory = roll(pattern)
    assert s['v'] == tuple(F(x) for x in previous['45']['velocity'])
    assert memory <= 15
    return s


def unconditional_bridge(s, horizon=15):
    """Common u=(T=9.81 N, tau=0) for all states, disturbances and packets."""
    if horizon != 15:
        raise ValueError("Frozen finite 15-tick certificate only")
    rows = [dict(s)]
    for _ in range(horizon):
        rows.append(step(rows[-1], F(0)))
    return rows


def serial(s):
    return {key: [str(x) for x in s[key]] for key in ('p', 'v', 'phi', 'omega')}


def verify(root=None):
    branches = {}
    for pattern in ('SMM', 'MMS'):
        s45 = posterior_at_45(pattern)
        rows = unconditional_bridge(s45)
        assert len(rows) == 16
        assert all(safe(s) for s in rows)
        margins = {key: min(LIMIT[key] - max(abs(s[key][0]), abs(s[key][1]))
                            for s in rows) for key in LIMIT}
        assert all(x > 0 for x in margins.values())
        branches[pattern] = {
            'tick45_outer': serial(rows[0]),
            'tick60_outer': serial(rows[-1]),
            'min_hard_constraint_margins': {k: str(margins[k]) for k in
                                            ('p', 'v', 'phi', 'omega')},
            'all_16_boxes_safe': True,
        }
    assert branches['SMM']['tick60_outer']['v'] == [
        '-7841778593/5000000000', '15679162373/10000000000']
    assert branches['MMS']['tick60_outer']['v'] == [
        '-2187058727/2000000000', '5466914349/5000000000']
    if root is not None:
        cfg = json.loads((Path(root) / 'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics'] == 'defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s'])) == H
        assert F(str(cfg['plant']['inertia_kg_m2'])) == J
        assert F(str(cfg['plant']['gravity_m_s2'])) == T
        assert cfg['sensing']['position_period_ticks'] == 5
        assert cfg['sensing']['max_consecutive_missed_packets'] == 2
        assert F(str(cfg['sensing']['observed_noise_halfwidth']['px'])) == NOISE['p']
        assert cfg['domain']['input_lower'][1] <= 0 <= cfg['domain']['input_upper'][1]
    return {
        'run': 260,
        'evidence': 'EXACT_RATIONAL_FINITE_OPEN_LOOP_SHARED_SAFETY_BRIDGE',
        'start': 'Run254 SSSMMS all-zero history through 30, Run259 zero phi/omega and conditional packet history through 45',
        'starting_packet_patterns': ['SMM', 'MMS'],
        'future_measurement_handling': 'no updates applied; all noise-consistent future success/miss posterior branches are subsets of the unconditioned prediction',
        'shared_control_ticks_45_to_59': {'actual_thrust_N': str(T), 'torque_Nm': '0'},
        'certified_last_tick': 60,
        'future_safe_steps': 15,
        'branches': branches,
        'complete_information_state_terminal_rcis': False,
        'infinite_horizon_recursive_feasibility': False,
        'general_arbitrary_history_safety': False,
        'gate_A': 'blocked',
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = json.dumps(verify(args.root), sort_keys=True, indent=2,
                        ensure_ascii=False) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result)
    else:
        print(result, end='')


if __name__ == '__main__':
    main()
