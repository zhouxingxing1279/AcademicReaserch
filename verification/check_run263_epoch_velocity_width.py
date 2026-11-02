#!/usr/bin/env python3
"""Run263: all-reading measurement-epoch velocity-width outer certificate.

A width-only, packet-automaton invariant for the frozen 4-state Euler plant.
It does NOT construct an exact SMF posterior, a controller, or terminal RCI.
"""
import argparse
import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path

H = F(1, 50)
T = F(981, 100)
R = F(3246383, 1600000)
E_P = F(1, 50)       # position measurement halfwidth, m
E_PHI = F(1, 200)    # angle measurement halfwidth, rad


def acceleration_width_per_tick():
    # Width(sin(phi)) <= width(phi) <= 2 E_PHI by global 1-Lipschitz.
    return 2 * H * (R + T * E_PHI)


def success_cap(n):
    """Sound velocity projection width after a successful position packet.

    Requires a previous successful position strip n steps earlier, and a
    successful bounded-error angle observation at every intervening step.
    """
    if n not in (5, 10, 15):
        raise ValueError('at most two consecutive missed position packets')
    return 4 * E_P / (n * H) + H * (n + 1) * (R + T * E_PHI)


def legal_futures(start):
    if start not in ('SMM', 'MMS'):
        raise ValueError('Run260 only certifies these two histories')
    for bits in product('SM', repeat=3):
        future = ''.join(bits)
        if future == 'MMM':
            continue
        if start == 'SMM' and future[0] != 'S':
            continue  # two preceding misses force success at tick50
        yield future


def final_width(start, future):
    if future not in set(legal_futures(start)):
        raise ValueError('illegal packet future')
    anchor_tick = 35 if start == 'SMM' else 45
    width = None  # deliberately no assumed width at tick45
    records = []
    for tick, packet in zip((50, 55, 60), future):
        propagated = None if width is None else width + 5 * acceleration_width_per_tick()
        if packet == 'S':
            gap = tick - anchor_tick
            projected = success_cap(gap)
            width = projected if propagated is None else min(propagated, projected)
            anchor_tick = tick
        else:
            width = propagated
        records.append({'tick': tick, 'packet': packet,
                        'width_cap': None if width is None else str(width),
                        'anchor_tick': anchor_tick})
    assert width is not None  # forced success by tick60 in both modes
    return width, records


def certificate(root=None):
    caps = {str(n): success_cap(n) for n in (5, 10, 15)}
    delta = acceleration_width_per_tick()
    global_cap = caps['5'] + 10 * delta
    assert caps['5'] > caps['15'] > caps['10']
    assert delta == F(3324863, 40000000)
    assert global_cap == F(75223219, 40000000)
    assert global_cap < 2
    branches = {}
    mode_max = {}
    for start in ('SMM', 'MMS'):
        entries = {}
        for future in legal_futures(start):
            w, rows = final_width(start, future)
            assert w <= global_cap
            entries[future] = {'tick60_velocity_width_cap': str(w)}
        mode_max[start] = max(F(item['tick60_velocity_width_cap']) for item in entries.values())
        branches[start] = entries
    assert len(branches['SMM']) == 4
    assert len(branches['MMS']) == 7
    assert mode_max['SMM'] == caps['15'] + 10 * delta
    assert mode_max['MMS'] == global_cap
    if root is not None:
        cfg = json.loads((Path(root) / 'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics'] == 'defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s'])) == H
        assert F(str(cfg['plant']['gravity_m_s2'])) == T
        assert cfg['sensing']['position_period_ticks'] == 5
        assert cfg['sensing']['max_consecutive_missed_packets'] == 2
        noise = cfg['sensing']['observed_noise_halfwidth']
        assert F(str(noise['px'])) == E_P
        assert F(str(noise['phi'])) == E_PHI
    return {
        'run': 263,
        'evidence': 'EXACT_RATIONAL_ALL_READINGS_POSITION_EPOCH_VELOCITY_WIDTH_CAP',
        'scope': 'Run260 SMM/MMS packet histories at tick45; fixed thrust four-state Euler; every-tick successful bounded-noise attitude readings from anchor; arbitrary nonempty position readings and legal future packets',
        'position_opportunities': [50, 55, 60],
        'angle_observation_required_each_tick': True,
        'future_packet_patterns': {k: sorted(v) for k, v in ((start, list(legal_futures(start))) for start in ('SMM','MMS'))},
        'acceleration_width_increment_per_tick': str(delta),
        'success_velocity_width_caps': {k: str(v) for k, v in caps.items()},
        'tick60_mode_max_velocity_width_caps': {k: str(v) for k, v in mode_max.items()},
        'tick60_uniform_velocity_width_cap': str(global_cap),
        'branches': branches,
        'proof_kind': 'symbolic width-only outer bound via exact discrete position-velocity identity, 1-Lipschitz sin, packet automaton and induction; no enumeration of continuous measurement values',
        'not_certified': ['absolute state safety beyond Run260 finite bridge', 'full H-rep/CZ posterior', 'MPC controller', 'terminal information-state RCI', 'recursive feasibility', 'closed-loop stability', '20ms WCET'],
        'gate_A': 'blocked',
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--root', type=Path)
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    s = json.dumps(certificate(a.root), sort_keys=True, indent=2, ensure_ascii=False) + '\n'
    if a.output:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(s)
    else:
        print(s, end='')

if __name__ == '__main__':
    main()
