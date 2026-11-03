#!/usr/bin/env python3
"""Run259: bounded-memory rolling position anchor under at most two packet misses.

A sound p-v outer projection for one Run254 observation history, not a full
H-rep/CZ posterior, a general output-feedback controller, or terminal RCI.
"""
import argparse
import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path

from check_run255_posterior_bridge import (
    H, J, T, R, NOISE, PULSE, posterior30, step, sin_bounds, safe,
)
from check_run256_interval_information_limit import observe
from check_run258_delayed_anchor import (
    velocity_from_position_anchor, uniform_anchor_width, meet,
)


def acceleration(s):
    lo, hi = s['phi']
    return -T * sin_bounds(hi)[1] - R, -T * sin_bounds(lo)[0] + R


def reset_width_cap(n):
    """Universal post-success bound when phi is observed every intervening tick.

    Assumes fixed T, |r|<=R, |phi|<=NOISE['phi'] after each attitude update,
    position strip halfwidth NOISE['p'], and a previous successful anchor.
    Does NOT apply to the unobserved-angle Run254 ticks31--34.
    """
    assert n in (5, 10, 15)
    return (4 * NOISE['p'] / (n * H)
            + H * (n + 1) * (R + T * NOISE['phi']))


def roll(pattern, readings=None):
    """Seven legal 35/40/45 packet patterns (MMM prohibited).

    The anchor is replaced after a successful packet; old strips are safely
    forgotten, which can lose tightness but never discard true states.
    """
    if len(pattern) != 3 or any(c not in 'SM' for c in pattern) or pattern == 'MMM':
        raise ValueError('illegal 35/40/45 packet pattern')
    readings = {} if readings is None else readings
    s = posterior30()
    anchor = s['p']
    anchor_tick = 30
    accelerations = []
    records = {}
    max_memory = 0
    for k in range(30, 45):
        accelerations.append(acceleration(s))
        max_memory = max(max_memory, len(accelerations))
        s = step(s, PULSE[k-30] if k < 35 else F(0))
        tick = k + 1
        if tick >= 35:
            s = observe(s, {'phi': F(0), 'omega': F(0)})
            assert s is not None
        if tick in (35, 40, 45):
            success = pattern[(tick-35)//5] == 'S'
            if success:
                y = readings.get(tick, F(0))
                s = observe(s, {'p': y})
                assert s is not None, (pattern, tick, y)
                projected = velocity_from_position_anchor(y, anchor, accelerations)
                s = dict(s)
                s['v'] = meet(s['v'], projected)
                assert s['v'][0] <= s['v'][1]
                cap = uniform_anchor_width(anchor, accelerations)
                assert s['v'][1] - s['v'][0] <= cap
                records[str(tick)] = {
                    'packet': 'S', 'previous_anchor_tick': anchor_tick,
                    'anchor_age_steps': len(accelerations),
                    'velocity': [str(q) for q in s['v']],
                    'velocity_width': str(s['v'][1]-s['v'][0]),
                    'strip_width_cap': str(cap),
                }
                anchor = s['p']
                anchor_tick = tick
                accelerations = []
            else:
                records[str(tick)] = {
                    'packet': 'M', 'previous_anchor_tick': anchor_tick,
                    'anchor_age_steps': len(accelerations),
                    'velocity': [str(q) for q in s['v']],
                    'velocity_width': str(s['v'][1]-s['v'][0]),
                }
        assert safe(s), (pattern, tick, s)
    assert max_memory <= 15
    return records, max_memory


def physical_zero_witness():
    """A real r=0 trajectory enclosed by rational sine bounds at ticks35/40/45."""
    p0 = p1 = v0 = v1 = phi = omega = F(0)
    result = {}
    for k in range(30, 45):
        slo, shi = sin_bounds(phi)
        p0, p1, v0, v1, phi, omega = (
            p0 + H*v0, p1 + H*v1,
            v0 - H*T*shi, v1 - H*T*slo,
            phi + H*omega,
            omega + H/J*(PULSE[k-30] if k < 35 else F(0)),
        )
        if k+1 in (35, 40, 45):
            assert phi == omega == 0
            assert -NOISE['p'] <= p0 <= p1 <= NOISE['p']
            result[str(k+1)] = {'position_outer': [str(p0), str(p1)], 'velocity_outer': [str(v0), str(v1)]}
    return result


def verify(root=None):
    patterns = [''.join(p) for p in product('SM', repeat=3) if ''.join(p) != 'MMM']
    branches = {}
    max_memory = 0
    for pattern in patterns:
        rec, memory = roll(pattern)
        max_memory = max(max_memory, memory)
        branches[pattern] = rec
    assert max_memory == 15
    assert branches['MMS']['45']['anchor_age_steps'] == 15
    assert branches['SMS']['45']['anchor_age_steps'] == 10
    assert branches['SSS']['45']['anchor_age_steps'] == 5
    assert F(branches['MMS']['45']['velocity_width']) < F(1)
    assert F(branches['SMS']['45']['velocity_width']) < F(9, 10)
    assert F(branches['SSS']['40']['velocity_width']) > F(1)
    # Releasing p30 at the successful tick35 is sound but less tight than
    # Run258's retained p30->p40 strip on the SS branch.
    from check_run258_delayed_anchor import branch_at_40
    retained40, _ = branch_at_40(True, True)
    assert F(branches['SSS']['40']['velocity_width']) > retained40['v'][1]-retained40['v'][0]
    caps = {str(n): str(reset_width_cap(n)) for n in (5, 10, 15)}
    assert reset_width_cap(5) > reset_width_cap(15) > reset_width_cap(10)
    # After the first post-pulse success, each subsequent anchor gap has
    # per-tick attitude measurements, so its strip respects this uniform cap.
    for pat, rec in branches.items():
        for item in rec.values():
            if item['packet'] == 'S' and item['previous_anchor_tick'] >= 35:
                assert F(item['velocity_width']) <= reset_width_cap(item['anchor_age_steps'])
    witness = physical_zero_witness()
    for rec in branches.values():
        for tick, item in rec.items():
            lo, hi = (F(q) for q in item['velocity'])
            wlo, whi = (F(q) for q in witness[tick]['velocity_outer'])
            assert lo <= wlo <= whi <= hi
    # Nonzero, noise-consistent position readings remain valid for the witness.
    for pattern in patterns:
        for y in (-F(1, 100), F(1, 100)):
            roll(pattern, {35: y, 40: y, 45: y})
    if root is not None:
        cfg = json.loads((Path(root)/'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics'] == 'defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s'])) == H
        assert F(str(cfg['plant']['inertia_kg_m2'])) == J
        assert F(str(cfg['plant']['gravity_m_s2'])) == T
        assert cfg['sensing']['position_period_ticks'] == 5
        assert cfg['sensing']['max_consecutive_missed_packets'] == 2
        assert F(str(cfg['sensing']['observed_noise_halfwidth']['px'])) == NOISE['p']
        assert F(str(cfg['sensing']['observed_noise_halfwidth']['phi'])) == NOISE['phi']
    return {
        'run': 259,
        'evidence': 'EXACT_RATIONAL_ROLLING_ANCHOR_15_STEP_FORCED_SUCCESS_OUTER_PROJECTION',
        'history': 'Run254 SSSMMS through tick30; Run255 pulse 30..34; zero torque 35..44',
        'position_packet_patterns': patterns,
        'branches': {pat: {
            'tick40_width': rec['40']['velocity_width'],
            'tick45_packet': rec['45']['packet'],
            'tick45_width': rec['45']['velocity_width'],
            'tick45_anchor_age_steps': rec['45']['anchor_age_steps'],
        } for pat, rec in branches.items()},
        'max_stored_acceleration_intervals': max_memory,
        'uniform_post_pulse_success_width_caps_m_s': caps,
        'zero_reading_physical_witness_checked_at_ticks': [35, 40, 45],
        'scope': 'bounded-memory sound p-v projection for one zero-angle-readings tree; old anchors may lose tightness; general caps require phi observed each tick and fixed T',
        'complete_cz_or_hrep_filter': False,
        'terminal_information_invariance_proved': False,
        'recursive_feasibility_proved': False,
        'gate_A': 'blocked',
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    content = json.dumps(verify(args.root), indent=2, sort_keys=True, ensure_ascii=False)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content)
    else:
        print(content, end='')


if __name__ == '__main__':
    main()
