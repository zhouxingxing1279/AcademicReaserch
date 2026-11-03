#!/usr/bin/env python3
"""Certified time-uniform ellipsoidal error multi-set for the 15-mode observer.

The scalar Bellman map is

    T(r)_b = max_(a,b) c r_a + sqrt(q_ab).

Its contraction factor is c < 1.  Directed square-root intervals give a
componentwise lower iterate and an invariant rational upper vector obtained
from a geometric residual tail.  The result certifies the scalar ellipsoid
family only; it does not claim that this family is useful for MPC tightening.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

from check_intermittent_metric import ETA0
from check_mode_nestedness import run as c2_contract
from check_mode_radius import down, sqrt_interval, up

ROOT = Path(__file__).resolve().parents[1]


def _bellman(radii, edges, contraction, upper):
    c = contraction[1 if upper else 0]
    result = {}
    rounding = up if upper else down
    for a, b, q in edges:
        d = sqrt_interval(q)[1 if upper else 0]
        candidate = rounding(c * radii[a] + d)
        result[b] = max(result.get(b, candidate), candidate)
    return result


def fixed_point_enclosure(edges, mode_count, contraction=None, iterations=2048):
    """Enclose the unique nonnegative Bellman fixed point with rationals."""
    if iterations < 1:
        raise ValueError('iterations must be positive')
    contraction = contraction or sqrt_interval(ETA0)
    c_lo, c_hi = contraction
    if not (F(0) <= c_lo <= c_hi < F(1)):
        raise ValueError('contraction interval must lie in [0, 1)')
    modes = set(range(mode_count))
    if {b for _, b, _ in edges} != modes:
        raise ValueError('every mode must have an incoming edge')
    if any(a not in modes or b not in modes or F(q) < 0 for a, b, q in edges):
        raise ValueError('edge has invalid mode or negative energy')

    lower = {j: F(0) for j in modes}
    upper_iterate = dict(lower)
    for _ in range(iterations):
        lower = _bellman(lower, edges, contraction, upper=False)
        upper_iterate = _bellman(upper_iterate, edges, contraction, upper=True)

    next_upper = _bellman(upper_iterate, edges, contraction, upper=True)
    residual = max(next_upper[j] - upper_iterate[j] for j in modes)
    if residual < 0:
        raise AssertionError('Bellman iteration from zero must be monotone')
    tail = up(residual / (F(1) - c_hi))
    upper = {j: up(upper_iterate[j] + tail) for j in modes}
    # Independent postcondition: the returned upper vector is edge invariant.
    for a, b, q in edges:
        d_hi = sqrt_interval(q)[1]
        if up(c_hi * upper[a] + d_hi) > upper[b]:
            raise AssertionError(f'upper enclosure is not invariant on edge {a}->{b}')
    return {
        'lower': lower,
        'upper': upper,
        'upper_iterate': upper_iterate,
        'residual_upper': residual,
        'tail_upper': tail,
        'iterations': iterations,
        'contraction': contraction,
    }


def run():
    contract = c2_contract()
    edges = [(row['from'], row['to'], row['box_max']) for row in contract['edges']]
    enclosure = fixed_point_enclosure(edges, mode_count=15)
    config = json.loads((ROOT / 'configs/planar_baseline.json').read_text(), parse_float=F)
    limits = [(F(hi) - F(lo)) / 2 for lo, hi in
              zip(config['domain']['state_lower'], config['domain']['state_upper'])]

    modes = []
    for j in range(15):
        velocity_factor = sqrt_interval(ETA0 ** (-j))
        velocity = (
            down(enclosure['lower'][j] * velocity_factor[0]),
            up(enclosure['upper'][j] * velocity_factor[1]),
        )
        angle = (enclosure['lower'][j], enclosure['upper'][j])
        modes.append({
            'mode': j,
            'radius': (enclosure['lower'][j], enclosure['upper'][j]),
            'velocity_support': velocity,
            'angle_support': angle,
            'velocity_limit': limits[2],
            'angle_limit': limits[4],
            'velocity_strictly_infeasible': velocity[0] > limits[2],
            'angle_strictly_infeasible': angle[0] > limits[4],
        })

    assert all(row['velocity_strictly_infeasible'] for row in modes)
    assert all(row['angle_strictly_infeasible'] for row in modes)
    edge_checks = []
    c_hi = enclosure['contraction'][1]
    for a, b, q in edges:
        lhs = up(c_hi * enclosure['upper'][a] + sqrt_interval(q)[1])
        edge_checks.append({'from': a, 'to': b, 'lhs': lhs,
                            'rhs': enclosure['upper'][b], 'pass': lhs <= enclosure['upper'][b]})
    assert all(row['pass'] for row in edge_checks)

    return {
        'status': 'pass',
        'claim': 'frozen_linear_inclusion_has_time_uniform_mode_ellipsoid',
        'control_gate': 'blocked_by_scalar_metric_geometry',
        'mode_count': 15,
        'edge_count': len(edges),
        'iterations': enclosure['iterations'],
        'contraction_interval': enclosure['contraction'],
        'upper_residual': enclosure['residual_upper'],
        'upper_tail': enclosure['tail_upper'],
        'modes': modes,
        'edge_invariance_checks': edge_checks,
        'limitations': [
            'conditional on the Run131--134 frozen linearized actual-input observer contract',
            'certifies a common scalar ellipsoidal outer multi-set, not the minimal set-valued multi-set',
            'large supports reject this certificate class for hard-constraint tightening, not SMF itself',
            'no ancillary RCI, terminal set, recursive-feasibility, or closed-loop claim',
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    output = Path(args.output)
    if output.exists():
        raise FileExistsError(output)
    result = run()
    sources = [
        'verification/check_mode_invariant_radius.py',
        'verification/test_mode_invariant_radius.py',
        'verification/check_mode_radius.py',
        'verification/check_mode_nestedness.py',
        'verification/check_intermittent_metric.py',
        'configs/planar_baseline.json',
        'docs/learning/72_time_uniform_estimator_multiset.md',
    ]
    result['source_sha256'] = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in sources
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str) + '\n')
    print(json.dumps({
        'status': result['status'],
        'claim': result['claim'],
        'control_gate': result['control_gate'],
        'radius_interval_mode_0': result['modes'][0]['radius'],
        'radius_interval_mode_14': result['modes'][-1]['radius'],
        'all_velocity_infeasible': all(row['velocity_strictly_infeasible'] for row in result['modes']),
        'all_angle_infeasible': all(row['angle_strictly_infeasible'] for row in result['modes']),
        'edge_checks': len(result['edge_invariance_checks']),
    }, indent=2, default=str))


if __name__ == '__main__':
    main()
