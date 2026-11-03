#!/usr/bin/env python3
"""Run233: reproducible full-state feedback seed; numerical evidence, never RCI proof.

Frozen four-state Euler plant, bounded control-dependent horizontal residual.
The policy is saturated state feedback (not MPC or output feedback).
"""
from __future__ import annotations
import argparse
import json
import math
import random
from pathlib import Path

H = 0.02
THRUST = 9.81
TMIN, TMAX = 4.905, 14.715
TAUMAX = 0.08
INERTIA = 0.02
R0, RT = 1.88, 243 / 16000
RADIUS = R0 + RT * THRUST
LIMITS = (5.0, 3.0, 0.45, 2.0)
# Discrete LQR linearization about hover: Q=diag(1,1,10,1), R=1.
# Offline scipy.linalg.solve_discrete_are, SciPy 1.17.0; gains frozen.
K = (-0.58081592, -0.91373144, 4.11224856, 0.74135794)
TICKS = 1000


def policy(x, feedback=True):
    if not feedback:
        return THRUST, 0.0
    torque = max(-TAUMAX, min(TAUMAX, -sum(a * b for a, b in zip(K, x))))
    return THRUST, torque


def step(x, u, residual):
    thrust, torque = u
    if not (TMIN <= thrust <= TMAX and abs(torque) <= TAUMAX + 1e-14):
        raise ValueError('inadmissible control')
    if abs(residual) > R0 + RT * thrust + 1e-12:
        raise ValueError('residual outside bound')
    p, v, phi, omega = x
    return (p + H * v,
            v + H * (-thrust * math.sin(phi) + residual),
            phi + H * omega,
            omega + H * torque / INERTIA)


def disturbance(name, tick, x, rng):
    if name == 'positive':
        return RADIUS
    if name == 'negative':
        return -RADIUS
    if name == 'alternate':
        return RADIUS if tick % 2 == 0 else -RADIUS
    if name == 'square_40':
        return RADIUS if tick % 80 < 40 else -RADIUS
    if name == 'square_80':
        return RADIUS if tick % 160 < 80 else -RADIUS
    if name == 'outward':
        return RADIUS if x[0] >= 0 else -RADIUS
    if name == 'random':
        return rng.uniform(-RADIUS, RADIUS)
    raise ValueError('unknown disturbance')


def episode(name, x0=(0.0, 0.0, 0.0, 0.0), seed=233, feedback=True, ticks=TICKS):
    if ticks < 1:
        raise ValueError('ticks must be positive')
    x = tuple(float(a) for a in x0)
    rng = random.Random(seed)
    maxima = [abs(a) for a in x]
    sum_p2 = x[0] * x[0]
    first_violation = 0 if any(abs(a) > b for a, b in zip(x, LIMITS)) else None
    saturation = 0
    for k in range(ticks):
        u = policy(x, feedback)
        saturation += abs(u[1]) >= TAUMAX - 1e-12
        r = disturbance(name, k, x, rng)
        x = step(x, u, r)
        for i in range(4):
            maxima[i] = max(maxima[i], abs(x[i]))
        sum_p2 += x[0] * x[0]
        if first_violation is None and any(abs(a) > b + 1e-12 for a, b in zip(x, LIMITS)):
            first_violation = k + 1
    return {'first_violation_tick': first_violation,
            'max_abs_state': [round(a, 9) for a in maxima],
            'position_rms_m': round(math.sqrt(sum_p2 / (ticks + 1)), 9),
            'saturated_torque_ticks': saturation,
            'final_state': [round(a, 9) for a in x]}


def verify(root=None):
    if root is not None:
        config = json.loads((Path(root) / 'configs/planar_baseline.json').read_text())
        assert config['plant']['truth_semantics'] == 'defined_discrete_euler'
        assert abs(config['plant']['dt_s'] - H) < 1e-12
        assert abs(config['plant']['inertia_kg_m2'] - INERTIA) < 1e-12
        assert config['domain']['input_lower'] == [TMIN, -TAUMAX]
        assert config['domain']['input_upper'] == [TMAX, TAUMAX]
        assert [config['domain']['state_upper'][i] for i in (0, 2, 4, 5)] == list(LIMITS)
    scenarios = ('positive', 'negative', 'alternate', 'square_40', 'square_80', 'outward', 'random')
    deterministic = {s: episode(s) for s in scenarios}
    uncontrolled = episode('positive', feedback=False)
    rng = random.Random(233001)
    monte_carlo = []
    for i in range(128):
        x0 = (rng.uniform(-0.05, 0.05), rng.uniform(-0.05, 0.05),
              rng.uniform(-0.005, 0.005), rng.uniform(-0.01, 0.01))
        monte_carlo.append(episode('random', x0, seed=233100 + i))
    return {'run': 233, 'base_main': '8cee19a9a937f7037cf4ba1b28f2ede8ed82b98b',
            'model': 'frozen full-state four-dimensional Euler, T fixed 9.81 N',
            'policy': 'clipped full-state discrete-LQR seed, not SMF or MPC',
            'gain': list(K), 'torque_limit': TAUMAX,
            'residual_halfwidth': RADIUS, 'ticks_per_episode': TICKS,
            'deterministic_scenarios': deterministic,
            'uncontrolled_positive': uncontrolled,
            'random_episodes': len(monte_carlo),
            'random_violations': sum(e['first_violation_tick'] is not None for e in monte_carlo),
            'random_max_abs_state': [max(e['max_abs_state'][j] for e in monte_carlo) for j in range(4)],
            'random_mean_position_rms_m': round(sum(e['position_rms_m'] for e in monte_carlo) / len(monte_carlo), 9),
            'gate_A': 'blocked',
            'limitations': [
                'Finite deterministic and Monte Carlo trajectories do not prove robust invariance.',
                'Full-state feedback with known state is not intermittent-measurement SMF or Tube MPC.',
                'Frozen disturbance sequences are not an exhaustive adaptive adversary.',
                'No recursive feasibility, asymptotic stability, six-state safety, or timing bound.']}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    s = json.dumps(verify(args.root), ensure_ascii=False, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(s)
    else:
        print(s, end='')


if __name__ == '__main__':
    main()
