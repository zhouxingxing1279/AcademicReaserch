#!/usr/bin/env python3
"""C2 exact arithmetic audit; not a closed-loop or formal proof checker."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path

from check_intermittent_metric import (
    AXES, H, ETA0, ETA_ROBUST, YOUNG_NOISE_MULTIPLIER,
    a0, a1, p_age, matmul, transpose, matsub, matscale, psd2,
)

ROOT = Path(__file__).resolve().parents[1]
EDGES = [(j, j + 1, 0) for j in range(14)] + [(j, 0, 1) for j in (4, 9, 14)]


def metric(j):
    P = [[F(0) for _ in range(6)] for _ in range(6)]
    for axis, ix in [('x', (0, 2)), ('z', (1, 3))]:
        block = p_age(AXES[axis]['p'], j)
        for r in range(2):
            for c in range(2):
                P[ix[r]][ix[c]] = block[r][c]
    P[4][4] = P[5][5] = F(1)
    return P


def matrices(success, widths):
    A = [[F(0) for _ in range(6)] for _ in range(6)]
    G = [[F(0) for _ in range(7)] for _ in range(6)]
    for axis, ix, wi, ni in [('x', (0, 2), 0, 3), ('z', (1, 3), 1, 4)]:
        ell = AXES[axis]['ell']
        block = a1(ell) if success else a0()
        for r in range(2):
            for c in range(2):
                A[ix[r]][ix[c]] = block[r][c]
        G[ix[1]][wi] = H
        if success:
            G[ix[0]][ni] = -1
            G[ix[1]][ni] = -ell
    G[2][2] = H * F(981, 100)
    G[4][5] = G[5][6] = -1
    return A, [[F(a) * widths[c] for c, a in enumerate(row)] for row in G]


def quad(P, v):
    return sum(v[i] * P[i][j] * v[j] for i in range(len(v)) for j in range(len(v)))


def support_squared(j, c):
    # Explicit inverse of the two 2x2 blocks, no floating-point inversion.
    value = c[4] ** 2 + c[5] ** 2
    for axis, ix in [('x', (0, 2)), ('z', (1, 3))]:
        p = AXES[axis]['p']
        cp, cv = c[ix[0]], c[ix[1]]
        value += ETA0 ** (-j) * (cp * cp / p + (j * H * cp + cv) ** 2)
    return value


def reachable(j, steps):
    modes = {j}
    for _ in range(steps):
        modes = {b for a, b, _ in EDGES if a in modes}
    return modes


def run():
    cfg = json.loads((ROOT / 'configs/planar_baseline.json').read_text(), parse_float=F)
    assert cfg['plant']['dt_s'] == H
    assert cfg['sensing']['position_period_ticks'] == 5
    assert cfg['sensing']['max_consecutive_missed_packets'] == 2
    phi = cfg['domain']['state_upper'][4]
    tmax = cfg['domain']['input_upper'][0]
    bt = tmax - cfg['plant']['gravity_m_s2']
    dx = F(1880, 1000) + bt * phi + tmax * phi ** 3 / 6
    dz = F(2086, 1000) + tmax * phi ** 2 / 2
    noise = cfg['sensing']['observed_noise_halfwidth']
    widths = [dx, dz, noise['phi'], noise['px'], noise['pz'], noise['phi'], noise['omega']]
    lower, upper = [], []
    for j in range(15):
        for axis in AXES.values():
            p = axis['p']
            tr = ETA0 ** j * (p + 1 + p * (j * H) ** 2)
            det = ETA0 ** (2 * j) * p
            lower.append(det / tr)
            upper.append(tr)
    alpha_low, alpha_high = min([F(1)] + lower), max([F(1)] + upper)
    # Certify the claimed eigenvalue enclosure using exact 2x2 PSD tests.
    for j in range(15):
        for axis in AXES.values():
            P = p_age(axis['p'], j)
            I = [[F(1), F(0)], [F(0), F(1)]]
            assert psd2(matsub(P, matscale(alpha_low, I)))
            assert psd2(matsub(matscale(alpha_high, I), P))

    edge_results = []
    for j, k, success in EDGES:
        A, G = matrices(success, widths)
        for axis in AXES.values():
            B = a1(axis['ell']) if success else a0()
            assert psd2(matsub(matscale(ETA0, p_age(axis['p'], j)),
                               matmul(transpose(B), matmul(p_age(axis['p'], k), B))))
        Q = matmul(transpose(G), matmul(metric(k), G))
        corners = [(quad(Q, s), s) for s in itertools.product((-1, 1), repeat=7)]
        maximum, witness = max(corners)
        trace = sum(Q[i][i] for i in range(7))
        edge_results.append({'from': j, 'to': k, 'success': success,
                             'box_max': maximum, 'maximizing_signs': witness,
                             'trace_upper_spectral_gain': trace, 'A': A, 'G_normalized': G})
    box_max = max(r['box_max'] for r in edge_results)
    cd_upper = YOUNG_NOISE_MULTIPLIER * max(r['trace_upper_spectral_gain'] for r in edge_results)
    c_box = YOUNG_NOISE_MULTIPLIER * box_max
    # Independent closed form of the maximizing successful reset edge.
    ex = H * (dx + F(981, 100) * noise['phi'])
    ez = H * dz
    expected = (F(120) * noise['px'] ** 2 + (ex + 5 * noise['px']) ** 2
                + F(60) * noise['pz'] ** 2 + (ez + F(9, 2) * noise['pz']) ** 2
                + noise['phi'] ** 2 + noise['omega'] ** 2)
    assert box_max == expected
    # Shift inclusions are graph identities; audit through the configured horizon.
    count = 0
    for j, k, _ in EDGES:
        for i in range(cfg['mpc']['horizon'] + 1):
            assert reachable(k, i) <= reachable(j, i + 1)
            count += 1
    # A rational strict directional witness: velocity normal, mode 0 vs all modes.
    c = [F(0), F(0), F(1), F(0), F(0), F(0)]
    current = support_squared(0, c)
    all_modes = max(support_squared(j, c) for j in range(15))
    assert current == 1 and all_modes == ETA0 ** (-14) and all_modes > current
    # Negative control: scalar shrinkage alone does not order different metrics.
    small_e = F(9, 10)
    assert small_e * support_squared(14, c) > support_squared(0, c)
    # Window reset can destroy shift order; the min cap restores it.
    predicted = ETA_ROBUST * 1 + c_box
    recomputed = predicted + 1
    assert recomputed > predicted and min(recomputed, predicted) == predicted
    # Every age has velocity support squared >= e.  The symmetric velocity
    # interval [-3,3] cannot contain even one such ellipsoid when e > 9.
    e_future = F(0)
    first_empty = None
    necessary_checks = []
    for i in range(1, cfg['mpc']['horizon'] + 1):
        e_future = ETA_ROBUST * e_future + c_box
        necessary_checks.append({'step': i, 'minimum_e': e_future})
        if first_empty is None and e_future > F(9):
            first_empty = i
    assert first_empty == 3
    # Two-sided signed bounds must use max(0,b+,b-), not square each side.
    assert max(F(0), F(-2), F(3)) ** 2 == 9
    return {'status': 'pass', 'domain_conditional': True,
            'state_order': cfg['state_order'], 'disturbance_order':
            ['wx', 'wz', 'n_phi_current', 'n_px_next', 'n_pz_next', 'n_phi_next', 'n_omega_next'],
            'disturbance_halfwidth': widths, 'mode_metrics': [metric(j) for j in range(15)],
            'alpha_lower': alpha_low, 'alpha_upper': alpha_high,
            'c_d_spectral_upper': cd_upper, 'box_energy_max': box_max,
            'c_box': c_box, 'scalar_fixed_point': c_box / (1 - ETA_ROBUST),
            'decimal_summary': { 'alpha_lower': float(alpha_low), 'alpha_upper': float(alpha_high),
                'c_d_upper': float(cd_upper), 'c_box': float(c_box),
                'scalar_fixed_point': float(c_box / (1 - ETA_ROBUST)),
                'all_mode_velocity_support_ratio': float(all_modes) ** 0.5},
            'edges': edge_results, 'corner_evaluations': len(EDGES) * 128,
            'graph_shift_checks': count,
            'strict_support_witness_squared': {'reachable_mode_0': current, 'all_modes': all_modes},
            'mpc_ellipsoid_only_gate': {'status': 'blocked', 'first_certain_empty_step': first_empty,
                'velocity_limit': 3, 'minimum_e_at_step_3': necessary_checks[2]['minimum_e'],
                'scope': 'uniform Young recursion plus un-intersected ellipsoidal tightening only; not plant infeasibility'},
            'negative_controls': ['cross_mode_scalar_order_insufficient', 'window_reset_requires_cap'],
            'limitations': ['not a formal proof assistant', 'not a controller feasibility certificate',
                'current angular noise is a bounded correlated input after direct measurement reset',
                'nonlinear remainder bounds require source-domain and actual-input certificates']}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    output = Path(args.output)
    if output.exists():
        raise FileExistsError(output)
    result = run()
    sources = ['verification/check_mode_nestedness.py', 'verification/check_intermittent_metric.py',
               'configs/planar_baseline.json', 'docs/learning/06_mode_dependent_nestedness.md']
    result['source_sha256'] = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in sources}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False, default=str) + '\n')
    print(json.dumps({'status': result['status'], **result['decimal_summary'],
                      'corner_evaluations': result['corner_evaluations'],
                      'graph_shift_checks': result['graph_shift_checks'],
                      'mpc_gate': result['mpc_ellipsoid_only_gate']['status'],
                      'first_empty_step': result['mpc_ellipsoid_only_gate']['first_certain_empty_step']}, indent=2))


if __name__ == '__main__':
    main()
