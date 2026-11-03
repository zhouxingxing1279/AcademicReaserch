#!/usr/bin/env python3
"""Bounded CZ pilot: floating LP proposals, exact rational dual certificates.

Coordinates are (px,pz-2,vx,vz,phi,omega). No reduction or controller.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
from scipy.optimize import linprog

ROOT = Path(__file__).resolve().parents[1]


def zeros(n, m):
    return np.full((n, m), Q(0), dtype=object)


def eye(n):
    a = zeros(n, n)
    for i in range(n):
        a[i, i] = Q(1)
    return a


class CZ:
    def __init__(self, c, g, a=None, b=None):
        self.c = np.array(c, dtype=object)
        self.g = np.array(g, dtype=object)
        self.a = zeros(0, self.g.shape[1]) if a is None else a
        self.b = np.array([], dtype=object) if b is None else b

    def predict(self, f, w):
        return CZ(f @ self.c, np.hstack((f @ self.g, w)),
                  np.hstack((self.a, zeros(len(self.b), w.shape[1]))), self.b.copy())

    def observe(self, indices, y, noise):
        # y = H x + R nu; preserve the *same* latent coefficients.
        r = len(indices)
        a = np.vstack((np.hstack((self.a, zeros(len(self.b), r))),
                       np.hstack((self.g[indices], np.diag(noise)))))
        return CZ(self.c.copy(), np.hstack((self.g, zeros(len(self.c), r))),
                  a, np.concatenate((self.b, np.array(y, dtype=object)-self.c[indices])))

    def recenter(self, center):
        return CZ(self.c-np.array(center, dtype=object), self.g.copy(), self.a.copy(), self.b.copy())

    def dual_upper(self, direction, lam):
        d = np.array(direction, dtype=object)
        lam = np.array(lam, dtype=object)
        return d @ self.c + self.b @ lam + sum(abs(v) for v in d @ self.g-lam @ self.a)

    def support_certificate(self, direction):
        d = np.array(direction, dtype=object)
        f = d @ self.g
        if not len(self.b):
            return self.dual_upper(d, []), []
        proposal = linprog(-np.array(f, dtype=float), A_eq=np.array(self.a, dtype=float),
                           b_eq=np.array(self.b, dtype=float), bounds=(-1, 1), method='highs')
        if not proposal.success:
            # A numerical infeasibility claim is never a certified empty set.
            lam = [Q(0)] * len(self.b)
        else:
            lam = [Q(float(-v)).limit_denominator(10**9) for v in proposal.eqlin.marginals]
        return self.dual_upper(d, lam), lam


def box_supports(g):
    return [sum(abs(v) for v in row) for row in g]


def outer_strip(g, indices, noise):
    # Fixed rational gains; valid outer inclusion for any K, no optimality claim.
    k = zeros(6, len(indices))
    h = zeros(len(indices), 6)
    for j, i in enumerate(indices):
        h[j, i] = k[i, j] = Q(1)
        if i in (0, 1):
            k[i+2, j] = [Q(5), Q(9, 2)][i]
    return np.hstack(((eye(6)-k @ h) @ g, k @ np.diag(noise)))


def run():
    cfg = json.loads((ROOT/'configs/planar_baseline.json').read_text(), parse_float=Q)
    dt = Q(cfg['plant']['dt_s'])
    gravity = Q(cfg['plant']['gravity_m_s2'])
    assert dt == Q(1, 50) and gravity == Q(981, 100)
    assert cfg['plant']['mass_kg'] == 1
    assert cfg['plant']['truth_semantics'] == 'defined_discrete_euler'
    assert cfg['plant']['external_process_halfwidth'] == [0]*6
    assert cfg['plant']['wind_bounds_m_s'] == [[Q('-0.5'), Q('0.5')]]*2
    assert cfg['state_order'] == ['px', 'pz', 'vx', 'vz', 'phi', 'omega']
    assert cfg['initial_set']['center'] == [0, 2, 0, 0, 0, 0]
    assert cfg['domain']['state_lower'] == [-5, Q('.5'), -3, -3, Q('-.45'), -2]
    assert cfg['domain']['state_upper'] == [5, Q('3.5'), 3, 3, Q('.45'), 2]
    assert cfg['domain']['input_lower'] == [Q('4.905'), Q('-.08')]
    assert cfg['domain']['input_upper'] == [Q('14.715'), Q('.08')]
    assert cfg['sensing']['position_period_ticks'] == 5
    assert cfg['sensing']['max_consecutive_missed_packets'] == 2
    assert cfg['sensing']['delay_ticks'] == 0
    assert cfg['sensing']['always_observed_indices'] == [4, 5]
    assert cfg['sensing']['position_indices'] == [0, 1]
    # Original global-on-domain nonlinear residual contract (theory 06 / C2).
    dx = Q('1.880')+Q('4.905')*Q('.45')+Q('14.715')*Q('.45')**3/6
    dz = Q('2.086')+Q('14.715')*Q('.45')**2/2
    f = eye(6)
    f[0, 2] = f[1, 3] = f[4, 5] = dt
    f[2, 4] = -dt*gravity
    w = zeros(6, 2)
    w[2, 0], w[3, 1] = dt*dx, dt*dz
    initial = [Q(v) for v in cfg['initial_set']['halfwidth']]
    center = [Q(v) for v in cfg['initial_set']['center']]
    domain = [min(center[i]-Q(cfg['domain']['state_lower'][i]),
                  Q(cfg['domain']['state_upper'][i])-center[i]) for i in range(6)]
    names = cfg['state_order']
    noise_map = cfg['sensing']['observed_noise_halfwidth']
    assert all(initial[i] <= Q(noise_map[names[i]]) for i in (0, 1, 4, 5))
    cases = []
    for label, successes in [('every_5', {0, 5, 10, 15, 20, 25}),
                              ('two_misses', {0, 15, 25})]:
        cz = CZ([Q(0)]*6, np.diag(initial))
        z = np.diag(initial)
        records = []
        domain_ok = True
        max_outer = [Q(0)]*6
        for tick in range(26):
            if tick:
                cz = cz.predict(f, w)
                z = np.hstack((f @ z, w))
            domain_ok &= all(v <= bound for v, bound in zip(box_supports(z), domain))
            indices = [4, 5]+([0, 1] if tick in successes else [])
            noise = [Q(noise_map[names[i]]) for i in indices]
            cz = cz.observe(indices, [Q(0)]*len(indices), noise)
            if tick:  # tick-zero strips are redundant with the benchmark prior
                z = outer_strip(z, indices, noise)
            # Exact feasible witness for this symmetric, zero-observation pilot.
            assert all(v == 0 for v in cz.b) and all(v == 0 for v in cz.c)
            bounds = box_supports(z)
            domain_ok &= all(v <= bound for v, bound in zip(bounds, domain))
            max_outer = [max(a, b) for a, b in zip(max_outer, bounds)]
            if tick in (5, 15, 25):
                for i, name in enumerate(names):
                    d = list(eye(6)[i])
                    upper, lam = cz.support_certificate(d)
                    # Reflection symmetry proves h(-d)=h(d); no extra LP needed.
                    assert upper >= 0
                    records.append(dict(tick=tick, coordinate=name, upper=str(upper),
                                        upper_decimal=float(upper), outer=str(bounds[i]),
                                        outer_decimal=float(bounds[i]),
                                        strict_improvement=upper < bounds[i],
                                        dual=[str(v) for v in lam]))
        cases.append(dict(name=label, successes=sorted(successes), records=records,
                          all_source_and_posterior_domains_certified=bool(domain_ok),
                          outer_peak=[str(v) for v in max_outer],
                          final_generators=cz.g.shape[1], final_equalities=len(cz.b)))
    return dict(status='bounded_symmetric_observation_pilot_not_controller',
                physical_domain_gate=('pass_for_declared_records_only' if all(
                    c['all_source_and_posterior_domains_certified'] for c in cases) else 'blocked'),
                arithmetic='rational dual upper bounds; scipy only proposes multipliers',
                model='six-state affine physical outer inclusion; hover input T=g, tau=0',
                dx=str(dx), dz=str(dz), cases=cases,
                source_sha256={str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in [Path(__file__), ROOT/'configs/planar_baseline.json']})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('output must not already exist')
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    for case in result['cases']:
        print(case['name'], 'domain:', case['all_source_and_posterior_domains_certified'],
              'size:', case['final_generators'], case['final_equalities'])
        for row in case['records']:
            if row['tick'] == 25:
                print(row['coordinate'], row['upper_decimal'], row['outer_decimal'])
