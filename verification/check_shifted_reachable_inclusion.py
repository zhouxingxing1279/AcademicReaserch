#!/usr/bin/env python3
"""Exact affine-box checks for shifted reachable-set inclusion.

The checker separates sufficient assumptions from the inclusion result.  It
does not infer disturbance nesting from data and does not compare two newly
optimized control sequences.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
import argparse
import hashlib
import json


ROOT = Path(__file__).resolve().parents[1]


def _vector(values):
    return tuple(Q(value) for value in values)


def _matrix(values):
    return tuple(tuple(Q(value) for value in row) for row in values)


def _matvec(matrix, vector):
    return tuple(sum((a * b for a, b in zip(row, vector)), Q(0)) for row in matrix)


def _add(*vectors):
    return tuple(sum(items, Q(0)) for items in zip(*vectors))


@dataclass(frozen=True)
class AffineBox:
    """Axis-aligned closed box represented by exact center and radius."""

    center: tuple
    radius: tuple

    def __init__(self, center, radius):
        center_q, radius_q = _vector(center), _vector(radius)
        if len(center_q) != len(radius_q) or any(value < 0 for value in radius_q):
            raise ValueError('box requires equal dimensions and nonnegative radii')
        object.__setattr__(self, 'center', center_q)
        object.__setattr__(self, 'radius', radius_q)

    @property
    def lower(self):
        return tuple(c - r for c, r in zip(self.center, self.radius))

    @property
    def upper(self):
        return tuple(c + r for c, r in zip(self.center, self.radius))

    def inclusion_margins(self, other):
        if len(self.center) != len(other.center):
            raise ValueError('dimension mismatch')
        return tuple(
            old_r - abs(new_c - old_c) - new_r
            for old_c, old_r, new_c, new_r in zip(
                self.center, self.radius, other.center, other.radius
            )
        )

    def encloses(self, other):
        return all(value >= 0 for value in self.inclusion_margins(other))

    def intersect(self, other):
        lower = tuple(max(a, b) for a, b in zip(self.lower, other.lower))
        upper = tuple(min(a, b) for a, b in zip(self.upper, other.upper))
        if any(lo > hi for lo, hi in zip(lower, upper)):
            raise ValueError('empty intersection')
        return AffineBox(
            [(lo + hi) / 2 for lo, hi in zip(lower, upper)],
            [(hi - lo) / 2 for lo, hi in zip(lower, upper)],
        )

    def affine_step(self, state_matrix, input_matrix, control, disturbance):
        f, b, u = _matrix(state_matrix), _matrix(input_matrix), _vector(control)
        center = _add(_matvec(f, self.center), _matvec(b, u), disturbance.center)
        radius = _add(
            _matvec(tuple(tuple(abs(value) for value in row) for row in f), self.radius),
            disturbance.radius,
        )
        return AffineBox(center, radius)

    def update_without_measurement(self):
        return self


def reachable_sequence(initial, state_matrix, input_matrix, controls, disturbances):
    if len(controls) != len(disturbances):
        raise ValueError('one disturbance set is required per control')
    sequence = [initial]
    for control, disturbance in zip(controls, disturbances):
        sequence.append(sequence[-1].affine_step(
            state_matrix, input_matrix, control, disturbance
        ))
    return tuple(sequence)


def shifted_inclusion_certificate(old_stage_one, posterior, state_matrix, input_matrix,
                                  old_controls, new_controls,
                                  old_disturbances, new_disturbances):
    """Check sufficient shift assumptions and every resulting stage inclusion."""
    if len(old_controls) != len(new_controls) + 1:
        raise ValueError('old sequence must contain the applied head plus shifted tail')
    if len(old_disturbances) != len(new_disturbances) + 1:
        raise ValueError('old disturbance sequence must be one stage longer')
    old_tail_controls = tuple(_vector(value) for value in old_controls[1:])
    new_controls_q = tuple(_vector(value) for value in new_controls)
    same_controls = new_controls_q == old_tail_controls
    nested_disturbances = all(
        old.encloses(new)
        for old, new in zip(old_disturbances[1:], new_disturbances)
    )
    old_sequence = reachable_sequence(
        old_stage_one, state_matrix, input_matrix,
        old_tail_controls, old_disturbances[1:],
    )
    new_sequence = reachable_sequence(
        posterior, state_matrix, input_matrix,
        new_controls_q, new_disturbances,
    )
    margins = tuple(
        old.inclusion_margins(new) for old, new in zip(old_sequence, new_sequence)
    )
    inclusions = tuple(all(value >= 0 for value in stage) for stage in margins)
    return {
        'assumptions': {
            'posterior_in_old_stage_one': old_stage_one.encloses(posterior),
            'same_shifted_control_tail': same_controls,
            'nested_disturbances': nested_disturbances,
        },
        'stage_margins': margins,
        'stage_inclusions': inclusions,
        'all_stage_inclusions': all(inclusions),
    }


def template_sandwich(certified_support_upper, old_template_upper):
    if len(certified_support_upper) != len(old_template_upper):
        raise ValueError('template dimensions differ')
    return tuple(min(Q(new), Q(old)) for new, old in zip(
        certified_support_upper, old_template_upper
    ))


def _six_state_contract(config):
    dt = Q(config['plant']['dt_s'])
    gravity = Q(config['plant']['gravity_m_s2'])
    inertia = Q(config['plant']['inertia_kg_m2'])
    if config['state_order'] != ['px', 'pz', 'vx', 'vz', 'phi', 'omega']:
        raise ValueError('unexpected state order')
    if config['input_order'] != ['T', 'tau']:
        raise ValueError('unexpected input order')
    if config['sensing']['position_period_ticks'] != 5:
        raise ValueError('unexpected position period')
    if config['sensing']['max_consecutive_missed_packets'] != 2:
        raise ValueError('unexpected dropout bound')

    f = [[Q(int(i == j)) for j in range(6)] for i in range(6)]
    f[0][2] = dt
    f[1][3] = dt
    f[2][4] = -dt * gravity
    f[4][5] = dt
    # The first input is the thrust deviation t=T-g in this affine contract.
    b = [[Q(0), Q(0)] for _ in range(6)]
    b[3][0] = dt
    b[5][1] = dt / inertia

    phi_max = Q(config['domain']['state_upper'][4])
    thrust_deviation = max(
        gravity - Q(config['domain']['input_lower'][0]),
        Q(config['domain']['input_upper'][0]) - gravity,
    )
    thrust_max = Q(config['domain']['input_upper'][0])
    dx = Q('1.880') + thrust_deviation * phi_max + thrust_max * phi_max**3 / 6
    dz = Q('2.086') + thrust_max * phi_max**2 / 2
    disturbance = AffineBox(
        [Q(0)] * 6,
        [Q(0), Q(0), dt * dx, dt * dz, Q(0), Q(0)],
    )
    return f, b, disturbance, dx, dz


def _serialise_certificate(certificate):
    margins = certificate['stage_margins']
    return {
        'assumptions': certificate['assumptions'],
        'checked_stages': len(margins),
        'all_stage_inclusions': certificate['all_stage_inclusions'],
        'stage_inclusions': list(certificate['stage_inclusions']),
        'minimum_coordinate_margin': str(min(value for stage in margins for value in stage)),
        'stage_margins': [[str(value) for value in stage] for stage in margins],
    }


def run():
    config_path = ROOT / 'configs/planar_baseline.json'
    config = json.loads(config_path.read_text(), parse_float=Q)
    f, b, disturbance, dx, dz = _six_state_contract(config)
    horizon = config['mpc']['horizon']
    if horizon != 25:
        raise ValueError('certificate is frozen to horizon 25')

    old_stage_one = AffineBox(
        [Q(0)] * 6,
        [Q('.04'), Q('.04'), Q('.2'), Q('.2'), Q('.01'), Q('.02')],
    )
    posteriors = {
        'position_success': AffineBox(
            [Q('.005'), Q('-.004'), Q(0), Q(0), Q(0), Q(0)],
            [Q('.02'), Q('.02'), Q('.15'), Q('.15'), Q('.005'), Q('.01')],
        ),
        # No position packet: the positional update is exactly the prediction.
        'position_miss': old_stage_one.update_without_measurement(),
    }
    old_controls = [[Q(0), Q(0)] for _ in range(horizon + 1)]
    new_controls = old_controls[1:]
    old_disturbances = [disturbance] * (horizon + 1)
    new_disturbances = old_disturbances[1:]
    cases = []
    for name, posterior in posteriors.items():
        certificate = shifted_inclusion_certificate(
            old_stage_one, posterior, f, b,
            old_controls, new_controls,
            old_disturbances, new_disturbances,
        )
        case = _serialise_certificate(certificate)
        case.update({
            'name': name,
            'position_update': 'intersection' if name == 'position_success' else 'identity',
        })
        cases.append(case)

    zero = AffineBox([Q(0)], [Q(0)])
    unit = AffineBox([Q(0)], [Q(1)])
    changed_control = shifted_inclusion_certificate(
        zero, zero, [[Q(1)]], [[Q(1)]],
        [[Q(0)], [Q(0)]], [[Q(2)]], [zero, zero], [zero],
    )
    larger_disturbance = shifted_inclusion_certificate(
        zero, zero, [[Q(1)]], [[Q(0)]],
        [[Q(0)], [Q(0)]], [[Q(0)]], [unit, unit],
        [AffineBox([Q(0)], [Q(2)])],
    )
    old_centered = AffineBox([Q(0)], [Q(1)])
    shifted = AffineBox([Q(1)], [Q(1, 2)])
    all_cases_pass = all(case['all_stage_inclusions'] for case in cases)
    return {
        'status': 'pass' if all_cases_pass else 'blocked',
        'shifted_reachable_gate': (
            'pass_for_declared_affine_contract' if all_cases_pass else 'blocked'
        ),
        'recursive_feasibility_gate': 'blocked_pending_control_terminal_certificate',
        'model': 'six-state affine outer-inclusion coordinates (px,pz-2,vx,vz,phi,omega)',
        'input_coordinates': '(t,tau) with t=T-g',
        'horizon': horizon,
        'disturbance_bounds': {'Dx': str(dx), 'Dz': str(dz)},
        'measurement_contract': {
            'position_period_ticks': config['sensing']['position_period_ticks'],
            'max_consecutive_missed_packets': config['sensing']['max_consecutive_missed_packets'],
            'no_position_measurement_update': 'identity',
        },
        'cases': cases,
        'counterexamples': {
            'changed_control': _serialise_certificate(changed_control),
            'larger_disturbance': _serialise_certificate(larger_disturbance),
            'radius_only_center_omission': {
                'old_radius': str(old_centered.radius[0]),
                'new_radius': str(shifted.radius[0]),
                'center_displacement': str(abs(shifted.center[0] - old_centered.center[0])),
                'inclusion_margin': str(old_centered.inclusion_margins(shifted)[0]),
                'included': old_centered.encloses(shifted),
            },
        },
        'source_sha256': {
            str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in [Path(__file__), config_path]
        },
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    if arguments.output.exists():
        parser.error('output must not already exist')
    result = run()
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2) + '\n')
    print('shifted reachable:', result['shifted_reachable_gate'])
    print('recursive feasibility:', result['recursive_feasibility_gate'])
    for item in result['cases']:
        print(item['name'], item['checked_stages'], item['minimum_coordinate_margin'])
