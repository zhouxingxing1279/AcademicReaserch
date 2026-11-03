#!/usr/bin/env python3
"""Fixed-dimension template/CZ contracts. Not a controller or timing certificate.

All acceptance arithmetic is rational. Published templates, rather than an
uncompressed historic CZ, are the reference for the next rolling update.
"""
import argparse
import hashlib
import json
from fractions import Fraction as Q
from numbers import Integral
from pathlib import Path
import numpy as np
from check_constrained_zonotope import CZ, eye, zeros, run as original_contract

ROOT = Path(__file__).resolve().parents[1]
GRID = 10**10


def require_rational(values):
    if any(not isinstance(v, (Q, Integral)) for v in np.asarray(values, dtype=object).flat):
        raise TypeError('certificate inputs must be integers or Fractions, not floats')


def outward(value):
    scaled = Q(value)*GRID
    return Q(-((-scaled.numerator)//scaled.denominator), GRID)


class Template:
    """H begins with +I,-I; later rows are additional fixed directions."""
    def __init__(self, h, b):
        require_rational(h)
        require_rational(b)
        self.h = np.array(h, dtype=object)
        self.b = np.array([Q(v) for v in b], dtype=object)
        if self.h.ndim != 2:
            raise ValueError('H must be a matrix')
        self.n = self.h.shape[1]
        if self.h.shape[0] != len(self.b) or len(self.b) < 2*self.n:
            raise ValueError('invalid template dimensions')
        if not np.array_equal(self.h[:2*self.n], np.vstack((eye(self.n), -eye(self.n)))):
            raise ValueError('coordinate directions must come first')

    def parameters(self):
        upper, lower = self.b[:self.n], -self.b[self.n:2*self.n]
        if any(lower > upper):
            raise ValueError('certified empty coordinate box')
        center, radius = (upper+lower)/2, (upper-lower)/2
        extra = self.h[2*self.n:]
        low = np.array([a @ center-sum(abs(v) for v in a*radius) for a in extra], dtype=object)
        slack = (self.b[2*self.n:]-low)/2
        if any(slack < 0):
            raise ValueError('certified empty halfspace/box intersection')
        return center, radius, low, slack

    def to_cz(self):
        c, radius, low, slack = self.parameters()
        extra = self.h[2*self.n:]
        r = len(extra)
        g = np.hstack((np.diag(radius), zeros(self.n, r)))
        a = np.hstack((extra @ np.diag(radius), np.diag(slack)))
        b = (self.b[2*self.n:]+low)/2-extra @ c
        return CZ(c, g, a, b)

    def contains(self, point):
        return all(self.h @ np.array(point, dtype=object) <= self.b)

    def witness(self, point):
        """Exact latent witness for a supplied point, including degenerate widths."""
        point = np.array([Q(v) for v in point], dtype=object)
        if not self.contains(point):
            raise ValueError('point outside template')
        c, radius, low, slack = self.parameters()
        xi = [Q(0) if width == 0 else (v-center)/width
              for v, center, width in zip(point, c, radius)]
        for a, bound, s in zip(self.h[2*self.n:], self.b[2*self.n:], slack):
            xi.append(Q(0) if s == 0 else (bound-a @ point)/s-1)
        return np.array(xi, dtype=object)

    def recenter(self, center):
        return Template(self.h, self.b-self.h @ np.array(center, dtype=object))


def compress(cz, h, cap=None, skip_lp=False):
    """PRECONDITION: cap, if supplied, independently contains the target CZ.

    This routine cannot establish that precondition; rollout obtains it from
    the previously certified predictive chain, posterior update from set
    intersection. An unrelated old cap is never safe merely because min works.
    """
    for values in (cz.c, cz.g, cz.a, cz.b, h):
        require_rational(values)
    if cap is not None and not np.array_equal(h, cap.h):
        raise ValueError('cap uses a different template')
    bounds, records = [], []
    for j, direction in enumerate(h):
        if skip_lp:
            lam = [Q(0)]*len(cz.b)
            exact = cz.dual_upper(direction, lam)
        else:
            exact, lam = cz.support_certificate(direction)
        assert exact == cz.dual_upper(direction, lam)
        upper = outward(exact)
        assert upper >= exact
        bound = upper if cap is None else min(upper, cap.b[j])
        bounds.append(bound)
        records.append({'exact': str(exact), 'rounded': str(upper),
                        'published': str(bound), 'cap_active': bool(bound < upper)})
    return Template(h, bounds), records


def rollout(posterior, f, w, horizon, old=None, skip_lp=False):
    """Constant affine map, zero affine offset; all future measurements ignored.

    old must be a certified chain for this SAME f,w. No arbitrary reoptimized
    input or enlarged disturbance is permitted. Last appended stage has no cap.
    """
    require_rational(f)
    require_rational(w)
    if old is not None:
        if len(old) != horizon+1 or not np.array_equal(posterior.h, old[1].h):
            raise ValueError('incompatible old chain')
        if not all(posterior.b <= old[1].b):
            raise ValueError('posterior not certified inside old first stage')
    chain = [posterior]
    stats = {'shift_rows': 0, 'support_rows': 0, 'cap_active_rows': 0}
    for i in range(1, horizon+1):
        image = chain[-1].to_cz().predict(f, w)
        cap = old[i+1] if old is not None and i < horizon else None
        nxt, records = compress(image, posterior.h, cap, skip_lp)
        stats['support_rows'] += len(records)
        stats['cap_active_rows'] += sum(r['cap_active'] for r in records)
        if cap is not None:
            assert all(nxt.b <= cap.b)
            stats['shift_rows'] += len(nxt.b)
        chain.append(nxt)
    return chain, stats


def run():
    # Reuse all frozen physical-configuration checks from the original CZ pilot.
    prior = original_contract()
    cfg = json.loads((ROOT/'configs/planar_baseline.json').read_text(), parse_float=Q)
    dt = Q(cfg['plant']['dt_s'])
    f = eye(6)
    f[0, 2] = f[1, 3] = f[4, 5] = dt
    f[2, 4] = -dt*Q(cfg['plant']['gravity_m_s2'])
    w = zeros(6, 2)
    w[2, 0], w[3, 1] = dt*Q(prior['dx']), dt*Q(prior['dz'])
    extra = zeros(6, 6)
    for j, (p, v, tau) in enumerate([(0, 2, Q('0.2')), (1, 3, Q('0.2')), (4, 5, dt)]):
        extra[2*j, p], extra[2*j, v] = Q(1), -tau
        extra[2*j+1] = -extra[2*j]
    h = np.vstack((eye(6), -eye(6), extra))
    initial = CZ([Q(0)]*6, np.diag([Q(v) for v in cfg['initial_set']['halfwidth']]))
    p, _ = compress(initial, h)
    truth = np.array([Q('.005'), Q('-.004'), Q('.03'), Q('-.02'), Q('.001'), Q(0)], dtype=object)
    names = cfg['state_order']
    noise_map = cfg['sensing']['observed_noise_halfwidth']
    limit = [Q(5), Q('1.5'), Q(3), Q(3), Q('.45'), Q(2)]
    old = None
    snapshots = []
    counts = {'support_rows': 0, 'shift_rows': 0, 'cap_active_rows': 0,
              'latent_witnesses': 0, 'forced_fallback_rollouts': 0}
    all_posterior_domain = True
    first_prediction_domain_failure = None
    digest = hashlib.sha256()
    max_size = [0, 0]
    max_measurement_size = [0, 0]
    horizon, ticks = cfg['mpc']['horizon'], 60
    for tick in range(ticks+1):
        if tick:
            truth = f @ truth  # admissible affine-model witness, not nonlinear truth simulation
            p = old[1]
        indices = [4, 5]+([0, 1] if tick % 15 == 0 else [])
        noise = [Q(noise_map[names[i]]) for i in indices]
        # Nonzero observations, deterministic admissible signed sensor errors.
        y = [truth[i]+width*Q((-1)**(tick+j), 2) for j, (i, width) in enumerate(zip(indices, noise))]
        updated = p.to_cz().observe(indices, y, noise)
        max_measurement_size = [max(max_measurement_size[0], updated.g.shape[1]),
                                max(max_measurement_size[1], len(updated.b))]
        p, records = compress(updated, h, p)
        counts['support_rows'] += len(records)
        counts['cap_active_rows'] += sum(r['cap_active'] for r in records)
        if old is not None:
            assert all(p.b <= old[1].b)
            counts['shift_rows'] += len(h)
        # Deliberately skip LPs on one rolling update to exercise safe loose bounds.
        forced = tick == 30
        counts['forced_fallback_rollouts'] += int(forced)
        chain, stats = rollout(p, f, w, horizon, old=old, skip_lp=forced)
        for key, value in stats.items():
            counts[key] += value
        predicted_truth = truth.copy()
        for stage, item in enumerate(chain):
            cz = item.to_cz()
            latent = item.witness(predicted_truth)
            assert all(abs(v) <= 1 for v in latent)
            assert np.array_equal(cz.c+cz.g @ latent, predicted_truth)
            assert np.array_equal(cz.a @ latent, cz.b)
            counts['latent_witnesses'] += 1
            max_size = [max(max_size[0], cz.g.shape[1]), max(max_size[1], len(cz.b))]
            domain_ok = all(item.b[j] <= limit[j % 6] for j in range(12))
            if stage == 0:
                all_posterior_domain &= domain_ok
            elif not domain_ok and first_prediction_domain_failure is None:
                first_prediction_domain_failure = {'tick': tick, 'stage': stage,
                    'failed_rows': [{'row': j, 'published_upper': str(item.b[j]),
                                     'domain_upper': str(limit[j % 6])}
                                    for j in range(12) if item.b[j] > limit[j % 6]]}
            digest.update(('|'.join(str(v) for v in item.b)+'\n').encode())
            predicted_truth = f @ predicted_truth
        if tick in (0, 15, 30, 45, 60):
            snapshots.append({'tick': tick, 'posterior_bounds': [str(v) for v in p.b],
                              'velocity_coordinate_halfwidths': [float((p.b[j]+p.b[j+6])/2) for j in (2, 3)],
                              'last_prediction_bounds': [str(v) for v in chain[-1].b]})
            print('tick', tick, 'size', max_size, flush=True)
        old = chain
    return {'status': 'pass_affine_representation_and_shift_contract_only',
            'ticks': ticks, 'horizon': horizon, 'directions': len(h),
            'template': [[str(v) for v in row] for row in h],
            'max_published_cz_generators': max_size[0], 'max_published_cz_equalities': max_size[1],
            'max_temporary_measurement_cz_generators': max_measurement_size[0],
            'max_temporary_measurement_cz_equalities': max_measurement_size[1],
            'temporary_prediction_cz_generators': max_size[0]+w.shape[1],
            'temporary_prediction_cz_equalities': max_size[1],
            'counts': counts, 'grid_denominator': GRID,
            'rolling_bounds_sha256': digest.hexdigest(), 'snapshots': snapshots,
            'posterior_coordinate_domain_checks': bool(all_posterior_domain),
            'first_prediction_box_domain_failure': first_prediction_domain_failure,
            'physical_prediction_gate': 'not_certified_without_all_source_domain_checks',
            'mpc_gate': 'blocked_control_and_terminal_contract_missing',
            'realtime_gate': 'not_evaluated',
            'scope': 'one nonzero affine-model record; position success every 15 ticks; hover input; no future measurement credit',
            'source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                              for p in [Path(__file__), ROOT/'verification/check_constrained_zonotope.py',
                                        ROOT/'configs/planar_baseline.json']}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('output must not already exist')
    result = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(result['counts'], result['first_prediction_box_domain_failure'])
