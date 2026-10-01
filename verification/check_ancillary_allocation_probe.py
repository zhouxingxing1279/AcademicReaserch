#!/usr/bin/env python3
"""Exact audit of the explicit nominal/correction input-budget probe.

The split is deliberately the most favorable first existence probe for an
ancillary RCI.  The correction torque receives the complete actuator range,
so nominal torque is fixed at zero.  The correction-thrust radius equals the
largest vertical residual over the actual thrust interval.  The remaining
thrust interval is the widest interval symmetric about hover whose Minkowski
sum with that correction interval remains inside the actual actuator box.

This checks an input-budget contract only.  It does not construct a causal
feedback, an RCI set, a terminal set, or a recursively feasible MPC.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run():
    config = json.loads((ROOT / 'configs/planar_baseline.json').read_text(),
                        parse_float=F)
    actual_lower = list(map(F, config['domain']['input_lower']))
    actual_upper = list(map(F, config['domain']['input_upper']))
    nominal_lower = list(map(F, config['mpc']['nominal_input_lower']))
    nominal_upper = list(map(F, config['mpc']['nominal_input_upper']))
    correction_lower = list(map(F, config['mpc']['ancillary_correction_lower']))
    correction_upper = list(map(F, config['mpc']['ancillary_correction_upper']))

    gravity = F(config['plant']['gravity_m_s2'])
    phi_max = F(config['domain']['state_upper'][4])
    residual_offset = F(2086, 1000)
    residual_slope = phi_max ** 2 / 2

    def residual(thrust):
        return residual_offset + residual_slope * thrust

    minkowski_lower = [a + b for a, b in zip(nominal_lower, correction_lower)]
    minkowski_upper = [a + b for a, b in zip(nominal_upper, correction_upper)]
    sum_within = all(lo <= value for lo, value in zip(actual_lower, minkowski_lower))
    sum_within &= all(value <= hi for value, hi in zip(minkowski_upper, actual_upper))

    actual_thrust_radius = (actual_upper[0] - actual_lower[0]) / 2
    correction_thrust_radius = correction_upper[0]
    nominal_thrust_radius = (nominal_upper[0] - nominal_lower[0]) / 2
    widest_symmetric = (
        nominal_lower[0] + nominal_upper[0] == 2 * gravity
        and correction_lower[0] == -correction_thrust_radius
        and correction_thrust_radius == residual(actual_upper[0])
        and nominal_thrust_radius == actual_thrust_radius - correction_thrust_radius
    )

    # At the maximum e_vz boundary, solve delta_T + d_z(bar_T+delta_T)=0.
    lower_bar = nominal_lower[0]
    required_negative = -(residual_offset + residual_slope * lower_bar) / (1 + residual_slope)
    lower_actual = lower_bar + required_negative
    positive_boundary_balance = {
        'nominal_thrust': lower_bar,
        'correction_thrust': required_negative,
        'actual_thrust': lower_actual,
        'residual': residual(lower_actual),
        'net_vz_increment_divided_by_h': required_negative + residual(lower_actual),
    }

    # At the minimum e_vz boundary, solve delta_T - d_z(bar_T+delta_T)=0.
    upper_bar = nominal_upper[0]
    required_positive = (residual_offset + residual_slope * upper_bar) / (1 - residual_slope)
    upper_actual = upper_bar + required_positive
    negative_boundary_balance = {
        'nominal_thrust': upper_bar,
        'correction_thrust': required_positive,
        'actual_thrust': upper_actual,
        'residual': -residual(upper_actual),
        'net_vz_increment_divided_by_h': required_positive - residual(upper_actual),
    }

    assert correction_lower[0] <= required_negative <= correction_upper[0]
    assert correction_lower[0] <= required_positive <= correction_upper[0]
    assert actual_lower[0] <= lower_actual <= actual_upper[0]
    assert actual_lower[0] <= upper_actual <= actual_upper[0]
    authority_margin = min(
        required_negative - correction_lower[0],
        correction_upper[0] - required_positive,
    )
    torque_nominal = nominal_lower[1:2] + nominal_upper[1:2]
    nominal_torque_has_interior = nominal_lower[1] < nominal_upper[1]

    assert sum_within
    assert widest_symmetric
    assert positive_boundary_balance['net_vz_increment_divided_by_h'] == 0
    assert negative_boundary_balance['net_vz_increment_divided_by_h'] == 0
    assert authority_margin == 0

    return {
        'status': 'pass',
        'claim': 'explicit_boundary_tight_input_allocation_probe_is_algebraically_consistent',
        'actual_input_lower': actual_lower,
        'actual_input_upper': actual_upper,
        'nominal_input_lower': nominal_lower,
        'nominal_input_upper': nominal_upper,
        'correction_input_lower': correction_lower,
        'correction_input_upper': correction_upper,
        'minkowski_sum_lower': minkowski_lower,
        'minkowski_sum_upper': minkowski_upper,
        'minkowski_sum_within_actual_input_box': sum_within,
        'thrust': {
            'widest_symmetric_hover_probe': widest_symmetric,
            'nominal_radius': nominal_thrust_radius,
            'correction_radius': correction_thrust_radius,
            'positive_boundary_balance': positive_boundary_balance,
            'negative_boundary_balance': negative_boundary_balance,
            'robust_authority_margin': authority_margin,
        },
        'torque': {
            'nominal_interval': torque_nominal,
            'correction_interval': [correction_lower[1], correction_upper[1]],
            'nominal_has_nonempty_interior': nominal_torque_has_interior,
        },
        'usable_as_final_nominal_input_domain': (
            nominal_torque_has_interior and authority_margin > 0
        ),
        'evidence_level': 'exact_input_budget_contract_not_an_rci_certificate',
        'limitations': [
            'boundary balance is an amplitude witness, not a causal disturbance-cancellation policy',
            'zero thrust-authority margin makes the probe unsuitable as a final robust MPC allocation',
            'singleton nominal torque cannot represent maneuvering nominal dynamics',
            'no augmented error RCI, state-domain closure, terminal set, or recursive feasibility is proved',
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
        'verification/check_ancillary_allocation_probe.py',
        'verification/test_ancillary_allocation_probe.py',
        'configs/planar_baseline.json',
        'docs/learning/75_ancillary_input_allocation_probe.md',
    ]
    result['source_sha256'] = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in sources
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str) + '\n')
    print(json.dumps({
        'status': result['status'],
        'nominal_input_lower': list(map(float, result['nominal_input_lower'])),
        'nominal_input_upper': list(map(float, result['nominal_input_upper'])),
        'correction_input_lower': list(map(float, result['correction_input_lower'])),
        'correction_input_upper': list(map(float, result['correction_input_upper'])),
        'robust_authority_margin': float(result['thrust']['robust_authority_margin']),
        'usable_as_final_nominal_input_domain': result['usable_as_final_nominal_input_domain'],
    }, indent=2))


if __name__ == '__main__':
    main()
