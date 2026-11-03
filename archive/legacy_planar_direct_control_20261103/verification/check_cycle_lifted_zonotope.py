#!/usr/bin/env python3
"""Exact cycle-lifted zonotopic invariant multi-set certificate.

The packet-success graph has return cycles of 5, 10, and 15 ticks.  This
checker keeps the signed dynamics over an entire return cycle, finds the
least axis-aligned mode-0 box that contains every lifted successor, and
propagates that box through miss edges without intermediate boxing.  Thus
the age-mode members are zonotopes and reset cancellation is retained.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

from check_mode_nestedness import EDGES, ROOT, matrices
from check_mode_radius import propagate_generators, row_supports

CYCLE_LENGTHS = (5, 10, 15)


def identity(n):
    return [[F(int(i == j)) for j in range(n)] for i in range(n)]


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B)))
             for j in range(len(B[0]))] for i in range(len(A))]


def diagonal(values):
    return [[value if i == j else F(0) for j, value in enumerate(values)]
            for i in range(len(values))]


def problem_data():
    config = json.loads((ROOT / 'configs/planar_baseline.json').read_text(), parse_float=F)
    phi = config['domain']['state_upper'][4]
    thrust_max = config['domain']['input_upper'][0]
    thrust_margin = thrust_max - config['plant']['gravity_m_s2']
    dx = F(1880, 1000) + thrust_margin * phi + thrust_max * phi ** 3 / 6
    dz = F(2086, 1000) + thrust_max * phi ** 2 / 2
    noise = config['sensing']['observed_noise_halfwidth']
    widths = [dx, dz, noise['phi'], noise['px'], noise['pz'],
              noise['phi'], noise['omega']]
    A0, G0 = matrices(0, widths)
    A1, G1 = matrices(1, widths)
    limits = [(F(hi) - F(lo)) / 2 for lo, hi in
              zip(config['domain']['state_lower'], config['domain']['state_upper'])]
    return config, A0, G0, A1, G1, limits


def lift_cycle(length, A0, G0, A1, G1):
    M = identity(len(A0))
    Z = [[] for _ in A0]
    for step in range(length):
        A, G = (A1, G1) if step == length - 1 else (A0, G0)
        Z = propagate_generators(A, Z, G)
        M = matmul(A, M)
    return {'length': length, 'M': M, 'Z': Z,
            'disturbance_support': row_supports(Z)}


def least_mode_zero_box(cycles):
    """Solve the special reset-cycle box inequalities exactly."""
    result = [max(c['disturbance_support'][i] for c in cycles) for i in range(6)]
    for velocity, position in ((2, 0), (3, 1)):
        candidates = []
        for cycle in cycles:
            row = cycle['M'][velocity]
            assert all(value == 0 for i, value in enumerate(row)
                       if i not in (position, velocity))
            gain = abs(row[velocity])
            assert gain < 1
            offset = abs(row[position]) * result[position]
            offset += cycle['disturbance_support'][velocity]
            candidates.append(offset / (1 - gain))
        result[velocity] = max(candidates)
    return result


def age_zonotopes(mode_zero_box, A0, G0):
    result = []
    Z = diagonal(mode_zero_box)
    for mode in range(15):
        result.append(Z)
        Z = propagate_generators(A0, Z, G0)
    return result


def run():
    config, A0, G0, A1, G1, limits = problem_data()
    cycles = [lift_cycle(length, A0, G0, A1, G1) for length in CYCLE_LENGTHS]
    box = least_mode_zero_box(cycles)
    seed = diagonal(box)

    cycle_checks = []
    for cycle in cycles:
        image = propagate_generators(cycle['M'], seed, cycle['Z'])
        support = row_supports(image)
        cycle_checks.append({
            'cycle_length': cycle['length'],
            'image_support': support,
            'box_support': box,
            'pass': all(a <= b for a, b in zip(support, box)),
        })
    assert all(row['pass'] for row in cycle_checks)

    zonotopes = age_zonotopes(box, A0, G0)
    modes = []
    for mode, Z in enumerate(zonotopes):
        support = row_supports(Z)
        modes.append({
            'mode': mode,
            'generator_count': len(Z[0]),
            'coordinate_support': support,
            'domain_halfwidth': limits,
            'fits_state_domain_halfwidth': all(a <= b for a, b in zip(support, limits)),
            'remaining_halfwidth': [b - a for a, b in zip(support, limits)],
        })
    assert all(row['fits_state_domain_halfwidth'] for row in modes)

    edge_checks = []
    for source, target, success in EDGES:
        image = propagate_generators(A1 if success else A0, zonotopes[source],
                                     G1 if success else G0)
        if success:
            support = row_supports(image)
            passed = all(a <= b for a, b in zip(support, box))
            relation = 'success_image_subset_mode_zero_box'
        else:
            support = row_supports(image)
            passed = image == zonotopes[target]
            relation = 'miss_image_equals_next_age_zonotope'
        edge_checks.append({'from': source, 'to': target, 'success': bool(success),
                            'relation': relation, 'image_support': support, 'pass': passed})
    assert len(edge_checks) == 17 and all(row['pass'] for row in edge_checks)

    boxed = identity(6)
    signed = identity(6)
    for step in range(15):
        A = A1 if step == 14 else A0
        boxed = matmul([[abs(value) for value in row] for row in A], boxed)
        signed = matmul(A, signed)
    negative_control = {
        'cycle_length': 15,
        'signed_x_velocity_gain': abs(signed[2][2]),
        'boxed_x_velocity_gain': boxed[2][2],
        'conclusion': 'per_tick_interval_boxing_is_not_a_valid_finiteness_test',
    }
    assert negative_control['signed_x_velocity_gain'] == F(1, 2)
    assert negative_control['boxed_x_velocity_gain'] == F(23, 10)

    return {
        'status': 'pass',
        'claim': 'cycle_lifted_zonotopic_outer_invariant_multiset_has_nonempty_state_domain_tightening',
        'cycle_lengths': list(CYCLE_LENGTHS),
        'mode_zero_box': box,
        'cycles': cycles,
        'cycle_invariance_checks': cycle_checks,
        'modes': modes,
        'edge_invariance_checks': edge_checks,
        'negative_control': negative_control,
        'scope': 'frozen six-state actual-input observer-error inclusion',
        'limitations': [
            'the mode-zero member is an axis-aligned outer box; later members retain signed miss-edge generator geometry',
            'truth containment remains conditional on the nonlinear residual bound and its source domain',
            'domain closure leaves center and ancillary-tube margins but does not prove their joint feasibility',
            'no input tightening, terminal set, recursive feasibility, or closed-loop performance claim',
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
        'verification/check_cycle_lifted_zonotope.py',
        'verification/test_cycle_lifted_zonotope.py',
        'verification/check_mode_nestedness.py',
        'verification/check_mode_radius.py',
        'configs/planar_baseline.json',
        'docs/learning/73_cycle_lifted_zonotope_multiset.md',
    ]
    result['source_sha256'] = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in sources
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str) + '\n')
    print(json.dumps({
        'status': result['status'],
        'claim': result['claim'],
        'mode_zero_box': list(map(float, result['mode_zero_box'])),
        'mode_14_support': list(map(float, result['modes'][14]['coordinate_support'])),
        'cycle_checks': len(result['cycle_invariance_checks']),
        'edge_checks': len(result['edge_invariance_checks']),
        'all_modes_fit_state_domain_halfwidth': all(
            row['fits_state_domain_halfwidth'] for row in result['modes']),
    }, indent=2))


if __name__ == '__main__':
    main()
