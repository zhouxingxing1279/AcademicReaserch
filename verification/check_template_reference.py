#!/usr/bin/env python3
"""Offline uncompressed-CZ comparison on the identical affine observation record.

This reference keeps all measurements and does not have the template pilot's
forced skipped LP rollout. It is not an equal-cost algorithm benchmark.
"""
import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
import numpy as np
from check_constrained_zonotope import CZ, eye, zeros, run as contract

ROOT = Path(__file__).resolve().parents[1]


def run(template_path):
    cached = json.loads(template_path.read_text())
    for relative, expected in cached['source_sha256'].items():
        assert hashlib.sha256((ROOT/relative).read_bytes()).hexdigest() == expected
    assert cached['ticks'] == 60 and cached['horizon'] == 25
    frozen = contract()
    cfg = json.loads((ROOT/'configs/planar_baseline.json').read_text(), parse_float=Q)
    f = eye(6)
    f[0, 2] = f[1, 3] = f[4, 5] = Q('.02')
    f[2, 4] = -Q('.02')*Q('9.81')
    w = zeros(6, 2)
    w[2, 0], w[3, 1] = Q('.02')*Q(frozen['dx']), Q('.02')*Q(frozen['dz'])
    cz = CZ([Q(0)]*6, np.diag([Q(v) for v in cfg['initial_set']['halfwidth']]))
    truth = np.array([Q('.005'), Q('-.004'), Q('.03'), Q('-.02'), Q('.001'), Q(0)], dtype=object)
    snapshots = {s['tick']: s for s in cached['snapshots']}
    records = []
    for tick in range(61):
        if tick:
            truth = f @ truth
            cz = cz.predict(f, w)
        indices = [4, 5]+([0, 1] if tick % 15 == 0 else [])
        noise = [Q(cfg['sensing']['observed_noise_halfwidth'][cfg['state_order'][i]]) for i in indices]
        y = [truth[i]+width*Q((-1)**(tick+j), 2) for j, (i, width) in enumerate(zip(indices, noise))]
        cz = cz.observe(indices, y, noise)
        if tick in snapshots:
            for i in (2, 3):
                plus, lp = cz.support_certificate(eye(6)[i])
                minus, lm = cz.support_certificate(-eye(6)[i])
                pb = snapshots[tick]['posterior_bounds']
                records.append({'tick': tick, 'coordinate': cfg['state_order'][i],
                    'reference_upper': str(plus), 'reference_lower': str(-minus),
                    'reference_halfwidth_upper': str((plus+minus)/2),
                    'reference_halfwidth_decimal': float((plus+minus)/2),
                    'template_published_halfwidth': str((Q(pb[i])+Q(pb[i+6]))/2),
                    'reference_positive_dual': [str(v) for v in lp],
                    'reference_negative_dual': [str(v) for v in lm]})
    return {'status': 'offline_affine_record_diagnostic_not_equal_budget_comparison',
            'reference_final_generators': cz.g.shape[1], 'reference_final_equalities': len(cz.b),
            'records': records,
            'template_result_sha256': hashlib.sha256(template_path.read_bytes()).hexdigest(),
            'source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                              for p in [Path(__file__), ROOT/'verification/check_constrained_zonotope.py',
                                        ROOT/'configs/planar_baseline.json']}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--template-result', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('output must not already exist')
    result = run(args.template_result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    for row in result['records']:
        print(row['tick'], row['coordinate'], row['reference_halfwidth_decimal'])
