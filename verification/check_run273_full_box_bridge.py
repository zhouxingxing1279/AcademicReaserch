#!/usr/bin/env python3
"""Run273: exact-rational 15-step full Run260 outer-box safety under tau=0.

A sufficient *finite* safety certificate, not a terminal invariant-set proof.
"""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

H, J, T = F(1, 50), F(1, 50), F(981, 100)
R = F(3246383, 1600000)
A, W = F(1, 125), F(1, 100)  # |phi60|, |omega60|
BOX = {
    'SMM': {'p': F(665412229, 1250000000), 'v': F(7841778593, 5000000000)},
    'MMS': {'p': F(2474339699, 10000000000), 'v': F(2187058727, 2000000000)},
}


def outer_abs(pattern, q):
    """Analytic bounds from |sin(phi)|<=|phi| for q Euler steps, tau=0."""
    assert pattern in BOX and 0 <= q <= 15
    p0, v0 = BOX[pattern]['p'], BOX[pattern]['v']
    phi = A + q*H*W
    v = v0 + H*(q*R + T*(q*A + H*W*q*(q-1)/2))
    p = p0 + q*H*v0 + H*H*(R*q*(q-1)/2
        + T*(A*q*(q-1)/2 + H*W*q*(q-1)*(q-2)/6))
    return {'p': p, 'v': v, 'phi': phi, 'omega': W}


def packet_patterns():
    out = []
    for a in 'SM':
        for b in 'SM':
            for c in 'SM':
                seq = a+b+c
                if 'MMM' not in seq:
                    out.append(seq)
    return out


def certify(root=None):
    if root is not None:
        root = Path(root)
        cfg = json.loads((root/'configs/planar_baseline.json').read_text())
        old = json.loads((root/'results/run260_conditional_shared_bridge_20261102/checks.json').read_text())
        assert cfg['plant']['truth_semantics'] == 'defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s'])) == H
        assert F(str(cfg['plant']['inertia_kg_m2'])) == J
        assert F(str(cfg['plant']['gravity_m_s2'])) == T
        assert F(str(cfg['sensing']['observed_noise_halfwidth']['px'])) == F(1, 50)
        assert cfg['sensing']['position_period_ticks'] == 5
        assert cfg['sensing']['max_consecutive_missed_packets'] == 2
        assert old['certified_last_tick'] == 60
        for name in BOX:
            b = old['branches'][name]['tick60_outer']
            for axis in ('p', 'v'):
                assert max(abs(F(x)) for x in b[axis]) == BOX[name][axis]
            assert max(abs(F(x)) for x in b['phi']) == A
            assert max(abs(F(x)) for x in b['omega']) == W
    patterns = packet_patterns()
    assert len(patterns) == 7 and 'MMS' in patterns and 'MMM' not in patterns
    branches = {}
    for name in BOX:
        states = [outer_abs(name, q) for q in range(16)]
        for state in states:
            assert state['p'] < 5 and state['v'] < 3
            assert state['phi'] < F(9, 20) and state['omega'] < 2
        branches[name] = {
            'tick60_outer_abs': {k: str(v) for k, v in outer_abs(name, 0).items()},
            'tick75_outer_abs': {k: str(v) for k, v in states[-1].items()},
            'all_16_ticks_hard_safe': True,
            'tick75_outer_v_not_subset_of_tick60_outer': states[-1]['v'] > BOX[name]['v'],
        }
    # Actual admissible zero state at tick60: Run271 history with cancellation
    # r=T*sin(phi) in ticks30..44 and r=0 in ticks45..59, same zero observations.
    # With tau=0 and r=+R thereafter, phi=omega=0, v_q=q*h*R,
    # p_q=h^2*R*q*(q-1)/2; first speed violation occurs at q=74.
    def witness(q):
        return H*H*R*q*(q-1)/2, q*H*R
    assert witness(73)[1] < 3 < witness(74)[1]
    assert witness(74)[0] < 5
    return {
        'run': 273,
        'base': 'Run260 tick60 SMM/MMS unconditional reliable outer boxes',
        'model': 'frozen four-state Euler, fixed T, tau=0',
        'future_packet_patterns_65_70_75': patterns,
        'branches': branches,
        'zero_state_tick60_member': 'constructive Run271 MMS->MMS zero-history continuation',
        'zero_torque_counterexample': {
            'disturbance': '+R for ticks60..133',
            'first_speed_violation_q': 74,
            'tick133_speed': str(witness(73)[1]),
            'tick134_speed': str(witness(74)[1]),
            'tick134_position': str(witness(74)[0]),
        },
        'quantifiers': 'all states in either reliable Run260 tick60 outer box, all bounded r, all future success/miss/noise histories: tau=0 safe through tick75; zero torque not infinitely safe from a reachable tick60 true state',
        'not_certified': ['terminal information RCI', '15-step return to a common terminal information family', 'MPC optimizer', 'full CZ posterior', 'six-state physical safety', 'infinite recursive feasibility', '20ms WCET'],
        'gate_A': 'blocked',
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    data = json.dumps(certify(args.root), sort_keys=True, indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(data)
    else:
        print(data, end='')


if __name__ == '__main__':
    main()
