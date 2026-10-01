#!/usr/bin/env python3
"""Exact necessary nominal-thrust reserve for a compact vertical tube.

The frozen tracking-error contract is

    e_vz+ = e_vz + h (delta_T + r_z),
    |r_z| <= d_z(T),  d_z(T) = c + alpha*T,
    T = bar_T + delta_T in [T_min, T_max].

At the maximum/minimum of a nonempty compact invariant set, constant
positive/negative residuals require both correction signs.  Saturating the
actual thrust at the corresponding endpoint gives the necessary nominal
range [T_min + d_z(T_min), T_max - d_z(T_max)].
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run():
    config_path = ROOT / 'configs/planar_baseline.json'
    config = json.loads(config_path.read_text(), parse_float=F)
    thrust_min, thrust_max = map(F, (
        config['domain']['input_lower'][0],
        config['domain']['input_upper'][0],
    ))
    gravity = F(config['plant']['gravity_m_s2'])
    phi_max = F(config['domain']['state_upper'][4])
    c = F(2086, 1000)
    alpha = phi_max ** 2 / 2

    def residual(thrust):
        return c + alpha * thrust

    negative_reserve = residual(thrust_min)
    positive_reserve = residual(thrust_max)
    nominal_lower = thrust_min + negative_reserve
    nominal_upper = thrust_max - positive_reserve
    assert nominal_lower < nominal_upper

    endpoint_witnesses = [
        {
            'nominal_thrust': thrust_min,
            'tracking_boundary': 'maximum_e_vz',
            'residual': residual(thrust_min),
            'allowed_correction_sign': 'delta_T_nonnegative',
            'least_outward_increment_divided_by_h': residual(thrust_min),
            'strict_outward_drift': residual(thrust_min) > 0,
        },
        {
            'nominal_thrust': thrust_max,
            'tracking_boundary': 'minimum_e_vz',
            'residual': -residual(thrust_max),
            'allowed_correction_sign': 'delta_T_nonpositive',
            'greatest_outward_increment_divided_by_h': -residual(thrust_max),
            'strict_outward_drift': -residual(thrust_max) < 0,
        },
    ]

    full_range_candidate = [thrust_min, thrust_max]
    necessary = [nominal_lower, nominal_upper]
    separate_nominal_bounds = (
        'nominal_input_lower' in config['mpc'] and
        'nominal_input_upper' in config['mpc']
    )
    return {
        'status': 'pass',
        'claim': 'full_nominal_thrust_domain_precludes_any_nonempty_compact_vertical_ancillary_rci',
        'vertical_residual': {'c': c, 'alpha': alpha},
        'actual_thrust_interval': full_range_candidate,
        'full_range_nominal_candidate': full_range_candidate,
        'necessary_nominal_thrust_interval': necessary,
        'boundary_correction_reserves': [negative_reserve, positive_reserve],
        'full_range_nominal_candidate_admissible': (
            full_range_candidate[0] >= necessary[0] and
            full_range_candidate[1] <= necessary[1]
        ),
        'separate_nominal_thrust_bounds_configured': separate_nominal_bounds,
        'hover_nominal_thrust_admissible': nominal_lower <= gravity <= nominal_upper,
        'endpoint_obstruction_witnesses': endpoint_witnesses,
        'evidence_level': 'exact_necessary_condition_and_endpoint_nonexistence_proof',
        'limitations': [
            'the necessary interval is not an ancillary-RCI existence certificate',
            'the proof uses only the frozen vertical outer-residual contract',
            'estimator geometry, horizontal coupling, torque, terminal ingredients, and recursive feasibility remain open',
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
        'verification/check_nominal_thrust_reserve.py',
        'verification/test_nominal_thrust_reserve.py',
        'configs/planar_baseline.json',
        'docs/learning/74_nominal_thrust_reserve_gate.md',
    ]
    result['source_sha256'] = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in sources
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str) + '\n')
    print(json.dumps({
        'status': result['status'],
        'necessary_nominal_thrust_interval': list(map(float, result['necessary_nominal_thrust_interval'])),
        'full_range_nominal_candidate_admissible': result['full_range_nominal_candidate_admissible'],
        'hover_nominal_thrust_admissible': result['hover_nominal_thrust_admissible'],
    }, indent=2))


if __name__ == '__main__':
    main()
