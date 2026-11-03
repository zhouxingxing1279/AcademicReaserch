#!/usr/bin/env python3
"""C2-R: rigorous radius intervals and finite-horizon directional diagnostic.

No floating point is used for acceptance decisions. Fractions on a 10^-12
grid enclose square roots and every rounded radius transition. Generator
propagation is exact for the declared independent-box linear inclusion,
which is only an outer model of the physical observer.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from math import isqrt
from pathlib import Path

from check_mode_nestedness import run as c2_contract
from check_intermittent_metric import ETA0, ETA_ROBUST, H

ROOT = Path(__file__).resolve().parents[1]
SCALE = 10 ** 12


def down(x):
    return F((x * SCALE).numerator // (x * SCALE).denominator, SCALE)


def up(x):
    scaled = x * SCALE
    return F(-((-scaled.numerator) // scaled.denominator), SCALE)


def sqrt_interval(x):
    x = F(x)
    if x < 0:
        raise ValueError('square-root input must be nonnegative')
    n = isqrt((x.numerator * SCALE * SCALE) // x.denominator)
    lo = F(n, SCALE)
    hi = lo if lo * lo == x else F(n + 1, SCALE)
    assert lo * lo <= x <= hi * hi
    return lo, hi


def radius_step(radii, edges, contraction=None):
    c_lo, c_hi = contraction or sqrt_interval(ETA0)
    result = {}
    for a, b, q in edges:
        if a not in radii:
            continue
        d_lo, d_hi = sqrt_interval(q)
        lo = down(c_lo * radii[a][0] + d_lo)
        hi = up(c_hi * radii[a][1] + d_hi)
        if b in result:
            lo, hi = max(lo, result[b][0]), max(hi, result[b][1])
        result[b] = (lo, hi)
    return result


def radius_history(start, seed, edges, horizon):
    result = [{start: seed}]
    for _ in range(horizon):
        result.append(radius_step(result[-1], edges))
    return result


def support_interval(radii, direction):
    values = []
    for j, (lo, hi) in radii.items():
        factor = sqrt_interval(ETA0 ** (-j)) if direction == 'velocity' else (F(1), F(1))
        values.append((down(lo * factor[0]), up(hi * factor[1])))
    return max(v[0] for v in values), max(v[1] for v in values)


def first_violation(history, direction, limit):
    for step, radii in enumerate(history):
        lo, hi = support_interval(radii, direction)
        if lo > limit:
            return {'step': step, 'lower': lo, 'upper': hi,
                    'display_lower': float(lo), 'display_upper': float(hi)}
        if hi > limit:
            raise AssertionError('ambiguous threshold: increase directed-rounding precision')
    return None


def propagate_generators(A, Z, G):
    return [[sum(A[i][k] * Z[k][j] for k in range(len(A)))
             for j in range(len(Z[0]))] + list(G[i]) for i in range(len(A))]


def row_supports(Z):
    return [sum(abs(v) for v in row) for row in Z]


def backward_support(path, coordinate, widths, edge_matrices):
    """Independent dual-direction calculation; does not multiply generators."""
    c = [F(int(i == coordinate)) for i in range(len(widths))]
    total = F(0)
    for edge in reversed(path):
        A, G = edge_matrices[edge]
        total += sum(abs(sum(c[i] * G[i][j] for i in range(len(c)))) for j in range(len(G[0])))
        c = [sum(c[i] * A[i][j] for i in range(len(c))) for j in range(len(c))]
    return total + sum(abs(c[i]) * widths[i] for i in range(len(c)))


def geometry_history(start, widths, edges, horizon):
    seed = [[widths[i] if i == j else F(0) for j in range(6)] for i in range(6)]
    states = [(start, (), seed)]
    matrices = {(r['from'], r['to']): (r['A'], r['G_normalized']) for r in edges}
    records = []
    peaks = list(widths)
    witnesses = [{'step': 0, 'path': []} for _ in range(6)]
    for step in range(horizon + 1):
        supports = [row_supports(Z) for _, _, Z in states]
        maxima = [max(w[i] for w in supports) for i in range(6)]
        for i in range(6):
            winner = next(k for k, w in enumerate(supports) if w[i] == maxima[i])
            path = states[winner][1]
            # Every coordinate extremum is independently checked in dual form.
            assert backward_support(path, i, widths, matrices) == maxima[i]
            if maxima[i] > peaks[i]:
                peaks[i] = maxima[i]
                witnesses[i] = {'step': step, 'path': path}
        records.append({'step': step, 'path_count': len(states), 'halfwidths': maxima})
        if step == horizon:
            break
        next_states = []
        for mode, path, Z in states:
            for edge in edges:
                if edge['from'] == mode:
                    a, b = edge['from'], edge['to']
                    next_states.append((b, path + ((a, b),),
                                        propagate_generators(edge['A'], Z, edge['G_normalized'])))
        states = next_states
    return {'start_mode': start, 'records': records, 'peak_halfwidths': peaks,
            'peak_witnesses': witnesses, 'dual_support_checks': 6 * len(records)}


def run():
    # Recompute C2 from its source, do not trust a hand-edited result JSON.
    contract = c2_contract()
    config = json.loads((ROOT / 'configs/planar_baseline.json').read_text(), parse_float=F)
    horizon = config['mpc']['horizon']
    assert horizon == 25
    limits = [(F(hi) - F(lo)) / 2 for lo, hi in zip(config['domain']['state_lower'],
                                                    config['domain']['state_upper'])]
    velocity_limit = min(limits[2:4])
    angle_limit = limits[4]
    edges = [(r['from'], r['to'], r['box_max']) for r in contract['edges']]
    widths = [F(1, 50), F(1, 50), F(1, 10), F(1, 10), F(1, 200), F(1, 100)]
    assert config['initial_set']['halfwidth'] == widths
    noise = config['sensing']['observed_noise_halfwidth']
    assert widths[0] == noise['px'] and widths[1] == noise['pz']
    assert widths[4] == noise['phi'] and widths[5] == noise['omega']
    scalar_cases, geometry_cases = [], []
    for start in (0, 5):
        initial_energy = (ETA0 ** start * (F(180) * (widths[0] + start * H * widths[2]) ** 2
                                          + 2 * widths[2] ** 2) + widths[4] ** 2 + widths[5] ** 2)
        for seed_name, energy in [('zero_best_case', F(0)), ('same_initial_box', initial_energy)]:
            history = radius_history(start, sqrt_interval(energy), edges, horizon)
            old_e = energy
            # Numerically enclose the theoretical dominance also at this precision.
            for radii in history[1:]:
                old_e = ETA_ROBUST * old_e + contract['c_box']
                assert max(hi ** 2 for _, hi in radii.values()) <= old_e
            scalar_cases.append({'start_mode': start, 'seed': seed_name, 'initial_energy': energy,
                                 'first_velocity_violation': first_violation(history, 'velocity', velocity_limit),
                                 'first_angle_violation': first_violation(history, 'angle', angle_limit),
                                 'horizon_velocity_support': support_interval(history[-1], 'velocity'),
                                 'history': [{'step': i, 'radii': {str(j): value for j, value in r.items()}}
                                             for i, r in enumerate(history)]})
        geometry_cases.append(geometry_history(start, widths, contract['edges'], horizon))
    zero_cases = [r for r in scalar_cases if r['seed'] == 'zero_best_case']
    assert [r['first_velocity_violation']['step'] for r in zero_cases] == [17, 17]
    assert [r['first_angle_violation']['step'] for r in zero_cases] == [4, 3]
    # The same rounded transition gives a compositional online upper certificate.
    # Each actual successor seed is capped by the old predicted value for that mode.
    shift_checks = 0
    for a, b, _ in edges:
        old = radius_history(a, (F(1), F(1)), edges, horizon + 1)
        cap = old[1][b][1]
        new = radius_history(b, (cap, cap), edges, horizon)
        for i, radii in enumerate(new):
            assert set(radii) <= set(old[i + 1])
            assert all(hi <= old[i + 1][j][1] for j, (_, hi) in radii.items())
            shift_checks += 1
    # These are widths around a free center. Passing does not control the center.
    peaks = [max(c['peak_halfwidths'][i] for c in geometry_cases) for i in range(6)]
    assert all(v < limit for v, limit in zip(peaks, limits))
    return {'status': 'pass', 'radius_control_gate': 'blocked',
            'geometry_coordinate_width_gate': 'pass_finite_horizon_only',
            'closed_loop_gate': 'not_proved', 'horizon': horizon, 'rounding_denominator': SCALE,
            'contraction_interval': sqrt_interval(ETA0), 'initial_error_box_halfwidth': widths,
            'edge_noise_energy': [{'from': a, 'to': b, 'q': q} for a, b, q in edges],
            'radius_cases': scalar_cases, 'geometry_cases': geometry_cases,
            'geometry_peak_halfwidths': peaks, 'state_interval_halfwidths': limits,
            'remaining_halfwidth_for_center_and_control_tube': [a - b for a, b in zip(limits, peaks)],
            'rounded_radius_shift_checks': shift_checks,
            'dual_support_checks': sum(c['dual_support_checks'] for c in geometry_cases),
            'limitations': ['physical-domain and actual-input conditional',
                           'generator support exact only for the stated independent-box affine inclusion',
                           'finite initialization horizon, not all rolling windows or infinite time',
                           'no input, terminal, controller, learning-advantage, or realtime certificate']}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    output = Path(args.output)
    if output.exists():
        raise FileExistsError(output)
    result = run()
    sources = ['verification/check_mode_radius.py', 'verification/test_mode_radius.py',
               'verification/check_mode_nestedness.py', 'verification/check_intermittent_metric.py',
               'configs/planar_baseline.json', 'docs/learning/07_mode_radius_and_geometry.md']
    result['source_sha256'] = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in sources}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str) + '\n')
    print(json.dumps({'status': result['status'], 'radius_gate': result['radius_control_gate'],
                      'radius_cases': [{k: c[k] for k in ('start_mode', 'seed', 'first_velocity_violation',
                                                        'first_angle_violation')} for c in result['radius_cases']],
                      'geometry_peak_halfwidths': list(map(float, result['geometry_peak_halfwidths'])),
                      'shift_checks': result['rounded_radius_shift_checks'],
                      'dual_support_checks': result['dual_support_checks']}, default=str, indent=2))


if __name__ == '__main__':
    main()
