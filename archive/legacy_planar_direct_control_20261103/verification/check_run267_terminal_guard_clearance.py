#!/usr/bin/env python3
"""Run267: exact-rational screening of Run260/264 reliable outer boxes.

PASS means every state in the BOX passes Run266's three-tick NECESSARY
speed guard. It does NOT prove three-tick viability, terminal invariance,
shared causal feedback, or a full measurement-conditioned SMF posterior.
"""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

H = J = F(1, 50)
T, U, R, V = F(981, 100), F(2, 25), F(3246383, 1600000), F(3)
DELTA = H * H * U / J
BOXES = {
    60: {
        'SMM': {'v': ('-7841778593/5000000000', '15679162373/10000000000'),
                'phi': ('-1/125', '1/125'), 'omega': ('-1/100', '1/100')},
        'MMS': {'v': ('-2187058727/2000000000', '5466914349/5000000000'),
                'phi': ('-1/125', '1/125'), 'omega': ('-1/100', '1/100')},
    },
    75: {
        'SMM': {'v': ('-22047163143/10000000000', '2204276833/1000000000'),
                'phi': ('-11/1000', '11/1000'), 'omega': ('-1/100', '1/100')},
        'MMS': {'v': ('-2162362449/1250000000', '3459486931/2000000000'),
                'phi': ('-11/1000', '11/1000'), 'omega': ('-1/100', '1/100')},
    },
}


def sin_bounds(x):
    x = F(x)
    p = x - x**3 / 6 + x**5 / 120 - x**7 / 5040
    e = abs(x)**9 / 362880
    return p - e, p + e


def uniform_guard(box):
    """For all (phi,omega) in box, upper bound on lower necessary guard,
    and lower bound on upper necessary guard. Monotonic sin on (-1,1).
    """
    pl, ph = map(F, box['phi'])
    wl, wh = map(F, box['omega'])
    vl, vh = map(F, box['v'])
    assert all(abs(x + 2*H*y) + DELTA < 1
               for x in (pl, ph) for y in (wl, wh))
    a_hi = (ph, ph + H*wh, ph + 2*H*wh - DELTA)
    a_lo = (pl, pl + H*wl, pl + 2*H*wl + DELTA)
    lower_guard_upper = -V + 3*H*R + H*T*sum(sin_bounds(x)[1] for x in a_hi)
    upper_guard_lower = V - 3*H*R + H*T*sum(sin_bounds(x)[0] for x in a_lo)
    return vl - lower_guard_upper, upper_guard_lower - vh


def certificate(root=None):
    assert DELTA == F(1, 625)
    if root is not None:
        root = Path(root)
        prior = {60: json.loads((root/'results/run260_conditional_shared_bridge_20261102/checks.json').read_text()),
                 75: json.loads((root/'results/run264_epoch_backup_20261102/checks.json').read_text())}
        for tick, src in prior.items():
            for mode, box in BOXES[tick].items():
                actual = src['branches'][mode][f'tick{tick}_outer']
                assert all(tuple(actual[k]) == v for k, v in box.items())
        cfg = json.loads((root/'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics'] == 'defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s'])) == H
        assert F(str(cfg['plant']['inertia_kg_m2'])) == J
        assert F(str(cfg['plant']['gravity_m_s2'])) == T
        assert F(str(cfg['domain']['state_upper'][2])) == V
        assert F(str(cfg['domain']['input_upper'][1])) == U
    result = {}
    for tick, branches in BOXES.items():
        result[str(tick)] = {}
        for mode, box in branches.items():
            margins = uniform_guard(box)
            assert all(m > 0 for m in margins)
            result[str(tick)][mode] = {
                'strict_guard_clearance_lower_m_s': str(margins[0]),
                'strict_guard_clearance_upper_m_s': str(margins[1]),
                'minimum_clearance_m_s_decimal': format(float(min(margins)), '.10f'),
                'every_state_in_outer_box_passes_necessary_guard': True,
            }
    for mode in ('SMM', 'MMS'):
        v60 = tuple(map(F, BOXES[60][mode]['v']))
        v75 = tuple(map(F, BOXES[75][mode]['v']))
        assert v75[0] < v60[0] and v75[1] > v60[1]
    return {
        'run': 267,
        'scope': 'only Run260 SMM/MMS fixed-history reliable unconditioned boxes at ticks 60 and 75',
        'method': 'monotonic sin plus exact rational degree-7 Taylor bounds with rigorous order-9 remainder',
        'branches': result,
        'zero_torque_tick75_outer_velocity_not_subset_tick60_outer': True,
        'meaning': 'necessary-screen PASS for every point in each box; not sufficient for safe control',
        'not_proved': ['exact SMF posterior', 'existence of shared causal 15-tick return policy',
                       'information-state RCI', 'recursive feasibility', 'closed-loop stability',
                       'six-state safety', '20ms WCET'],
        'gate_A': 'blocked',
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    data = json.dumps(certificate(args.root), indent=2, sort_keys=True, ensure_ascii=False) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(data)
    else:
        print(data, end='')


if __name__ == '__main__':
    main()
