#!/usr/bin/env python3
"""Run268: sound observation-conditioned affine (v,phi,omega) strip at tick60.

Frozen Run260 4-state Euler truth; tau=0 on ticks 35..59. This is NOT
an exact posterior, a controller, or a terminal information RCI.
"""
import argparse
import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path

H = F(1, 50)
T = F(981, 100)
R = F(3246383, 1600000)
EP = F(1, 50)
PHI60 = F(1, 125)   # Run260 reliable unconditional |phi_60| <= .008
OMEGA60 = F(1, 100) # Run260 reliable unconditional |omega_60| <= .01

def futures(start):
    if start not in ('SMM', 'MMS'):
        raise ValueError(start)
    for bits in product('SM', repeat=3):
        seq = ''.join(bits)
        if seq == 'MMM' or (start == 'SMM' and seq[0] != 'S'):
            continue
        yield seq

def latest_pair(start, future):
    if future not in futures(start):
        raise ValueError((start, future))
    successes = ([35] if start == 'SMM' else [45]) + [
        k for k, flag in zip((50, 55, 60), future) if flag == 'S'
    ]
    return successes[-2], successes[-1]

def weights(s, t):
    n = t - s
    if n not in (5, 10, 15):
        raise ValueError(n)
    return [(i, F(i - s + 1, n)) for i in range(s, t)] + [
        (i, F(1)) for i in range(t, 60)
    ]

def strip(s, t):
    """|v60 + h*T*A*phi60 - h*h*T*B*omega60 - dy/(n*h)| <= E+Q.

    dy=y_t-y_s; exact Euler p/v identity and phi_i=phi60-(60-i)*h*omega60.
    Q uses |sin(z)-z|<=|z|^3/6, valid for every real z.
    """
    w = weights(s, t)
    a = sum((c for _, c in w), F(0))
    b = sum((c * (60 - i) for i, c in w), F(0))
    n, m = t - s, 60 - t
    e = 2 * EP / (n * H) + H * R * (F(n + 1, 2) + m)
    q = H * T * sum((c * (PHI60 + (60 - i) * H * OMEGA60) ** 3 / 6
                     for i, c in w), F(0))
    return {'s': s, 't': t, 'A': a, 'B': b, 'E': e, 'Q': q,
            'radius': e + q, 'phi_coefficient': H * T * a,
            'omega_coefficient': -(H ** 2) * T * b}

def certificate(root=None):
    if root:
        cfg = json.loads((Path(root) / 'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics'] == 'defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s'])) == H
        assert F(str(cfg['plant']['inertia_kg_m2'])) == H
        assert F(str(cfg['plant']['gravity_m_s2'])) == T
        assert cfg['sensing']['position_period_ticks'] == 5
        assert cfg['sensing']['max_consecutive_missed_packets'] == 2
        assert F(str(cfg['sensing']['observed_noise_halfwidth']['px'])) == EP
    branches = {}
    for start in ('SMM', 'MMS'):
        branches[start] = {}
        for future in futures(start):
            s, t = latest_pair(start, future)
            z = strip(s, t)
            assert s >= 35 and t <= 60 and t > s
            assert z['Q'] < F(1, 100000)
            branches[start][future] = {key: str(val) for key, val in z.items()}
    assert len(branches['SMM']) == 4 and len(branches['MMS']) == 7
    return {'run': 268, 'evidence': 'EXACT_RATIONAL_COEFFICIENTS_AND_ANALYTIC_SINE_REMAINDER',
            'scope': 'Run260 fixed zero-reading history through45, SMM/MMS; tau=0 ticks35..59; all nonempty future measurement fibers, arbitrary bounded position/attitude readings and legal packets',
            'formula': '|v60 + phi_coefficient*phi60 + omega_coefficient*omega60 - (y_t-y_s)/((t-s)*h)| <= radius',
            'current_attitude_observation': '|phi60-y_phi60|<=0.005, |omega60-y_omega60|<=0.01; intersect strips if observed',
            'proof': 'Euler position/velocity telescoping, zero torque angular back-substitution, independent bounded position errors/disturbances, global |sin(z)-z|<=|z|^3/6',
            'branches': branches, 'gate_A': 'blocked',
            'not_certified': ['exact SMF posterior', 'terminal information-state RCI', '15-tick causal return', 'MPC solver', 'infinite recursive feasibility', 'six-state physical safety', '20ms WCET']}

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--root', type=Path)
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    s = json.dumps(certificate(a.root), sort_keys=True, indent=2) + '\n'
    if a.output:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(s)
    else:
        print(s, end='')

if __name__ == '__main__':
    main()
