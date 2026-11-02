#!/usr/bin/env python3
"""Run255: full Run254 interval-posterior finite shared-input bridge.

Exact Fraction outward enclosure, NOT a true-posterior identity or invariant set.
"""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

H = J = F(1, 50)
T = F(981, 100)
R = F(3246383, 1600000)
U = F(2, 25)
GRID = 10**10
LIMIT = {'p': F(5), 'v': F(3), 'phi': F(9, 20), 'omega': F(2)}
NOISE = {'p': F(1, 50), 'phi': F(1, 200), 'omega': F(1, 100)}
INIT = {'p': (-F(1, 50), F(1, 50)), 'v': (-F(1, 10), F(1, 10)),
        'phi': (-F(1, 200), F(1, 200)), 'omega': (-F(1, 100), F(1, 100))}
SUCCESS = (5, 10, 15, 30)
PULSE = (F(1, 25), -F(1, 25), -F(1, 25), F(1, 25), F(0))


def down(x):
    return F((x.numerator * GRID) // x.denominator, GRID)


def bound(a, b):
    return down(a), -down(-b)


def sin_bounds(x):
    assert abs(x) <= LIMIT['phi']
    if x < 0:
        a, b = sin_bounds(-x)
        return -b, -a
    a = x - x**3 / 6
    return a, a + x**5 / 120


def step(s, tau):
    assert abs(tau) <= U
    p, v, phi, omega = (s[k] for k in ('p', 'v', 'phi', 'omega'))
    slo, shi = sin_bounds(phi[0])[0], sin_bounds(phi[1])[1]
    return {'p': bound(p[0] + H*v[0], p[1] + H*v[1]),
            'v': bound(v[0] - H*(T*shi + R), v[1] + H*(R - T*slo)),
            'phi': bound(phi[0] + H*omega[0], phi[1] + H*omega[1]),
            'omega': bound(omega[0] + H/J*tau, omega[1] + H/J*tau)}


def safe(s):
    return all(-LIMIT[k] <= lo <= hi <= LIMIT[k] for k, (lo, hi) in s.items())


def posterior30():
    s = dict(INIT)
    for k in range(1, 31):
        s = step(s, F(0))
        obs = {'phi': F(0), 'omega': F(0)}
        if k in SUCCESS:
            obs['p'] = F(0)
        for key, y in obs.items():
            lo, hi = s[key]
            s[key] = (max(lo, y-NOISE[key]), min(hi, y+NOISE[key]))
            assert s[key][0] <= s[key][1]
        assert safe(s)
    return s


def bridge(s, horizon=40):
    rows = [dict(s)]
    for i in range(horizon):
        rows.append(step(rows[-1], PULSE[i] if i < len(PULSE) else F(0)))
    return rows


def serial(s):
    return {k: [str(x) for x in v] for k, v in s.items()}


def verify(root=None):
    s = posterior30()
    assert s['p'] == (-F(1, 50), F(1, 50))
    assert s['v'] == (-F(269364701, 200000000), F(269364701, 200000000))
    assert s['phi'] == (-F(1, 200), F(1, 200))
    assert s['omega'] == (-F(1, 100), F(1, 100))
    rows = bridge(s)
    assert all(safe(q) for q in rows[:40])  # ticks 30..69 inclusive
    assert not safe(rows[40])  # interval method fails at 70; NOT physical impossibility
    assert rows[40]['v'][0] < -LIMIT['v'] and rows[40]['v'][1] > LIMIT['v']
    assert rows[39]['v'] == (-F(5994167869, 2000000000), F(374557013, 125000000))
    if root is not None:
        import sys
        sys.path.insert(0, str(Path(root)/'verification'))
        import check_four_state_shielded_smf_mpc as prior
        import check_forced_success_velocity_alias as alias
        assert alias.outer_history()[30] == s
        assert all(prior.step(rows[i], PULSE[i] if i < 5 else F(0)) == rows[i+1]
                   for i in range(40))
        cfg = json.loads((Path(root)/'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics'] == 'defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s'])) == H
        assert F(str(cfg['plant']['inertia_kg_m2'])) == J
        assert F(str(cfg['plant']['gravity_m_s2'])) == T
        assert F(str(cfg['domain']['input_upper'][1])) == U
        assert cfg['sensing']['position_period_ticks'] == 5
        assert cfg['sensing']['max_consecutive_missed_packets'] == 2
    return {
        'run': 255,
        'evidence': 'EXACT_OUTWARD_RATIONAL_FULL_INTERVAL_POSTERIOR_FINITE_SHARED_BRIDGE',
        'history': 'SSSMMS; all successful position/angle/rate readings zero',
        'starting_tick': 30,
        'starting_box': serial(s),
        'shared_nonzero_torque_first_five_Nm': [str(x) for x in PULSE],
        'subsequent_torque_Nm': '0',
        'last_certified_safe_tick': 69,
        'certified_future_steps': 39,
        'tick69_outer_box': serial(rows[39]),
        'tick70_outer_box': serial(rows[40]),
        'tick70_outer_box_violates_speed': True,
        'tick70_actual_unsafety_proved': False,
        'future_measurement_branches': 'all noise-consistent success/miss paths; posterior subset of unconditioned prediction',
        'scope': 'one fixed Run254 observation history, its FULL sound interval posterior and all subsequent disturbance/noise/packet branches; not all histories',
        'infinite_horizon_terminal_invariance': False,
        'recursive_feasibility': False,
        'gate_A': 'blocked',
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    content = json.dumps(verify(args.root), sort_keys=True, indent=2, ensure_ascii=False) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content)
    else:
        print(content, end='')


if __name__ == '__main__':
    main()
