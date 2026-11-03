#!/usr/bin/env python3
"""Measurement-age directions: exact positive transport, no online support LP.

The predictor covers common open-loop inputs and ignores future observations.
This is an estimator/interface proof checker, not an output-feedback controller.
"""
import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
import numpy as np
from check_constrained_zonotope import eye, zeros, run as frozen_contract
from check_cz_template import Template, outward, GRID

ROOT = Path(__file__).resolve().parents[1]


class Transport:
    def __init__(self):
        self.dt, self.g = Q(1, 50), Q('9.81')
        self.dx = Q('1.880')+Q('4.905')*Q('.45')+Q('14.715')*Q('.45')**3/6
        self.dz = Q('2.086')+Q('14.715')*Q('.45')**2/2
        self.noise = {0: Q('.02'), 1: Q('.02'), 4: Q('.005'), 5: Q('.01')}
        self.f = eye(6)
        self.f[0, 2] = self.f[1, 3] = self.f[4, 5] = self.dt
        self.f[2, 4] = -self.dt*self.g
        self.w = zeros(6, 2)
        self.w[2, 0], self.w[3, 1] = self.dt*self.dx, self.dt*self.dz
        rows = list(eye(6))+list(-eye(6))
        for axis in (0, 1):
            for age in range(1, 16):
                direction = eye(6)[axis]-age*self.dt*eye(6)[axis+2]
                rows.extend((direction, -direction))
        self.h = np.array(rows, dtype=object)
        self.terms, self.q = [], []
        for sign in (1, -1):
            offset = 0 if sign == 1 else 6
            for state in range(6):
                terms = [(offset+state, Q(1))]
                if state in (0, 1, 4):
                    nxt = {0: 2, 1: 3, 4: 5}[state]
                    terms.append((offset+nxt, self.dt))
                if state == 2:
                    terms.append((10 if sign == 1 else 4, self.dt*self.g))
                self.terms.append(terms)
                self.q.append(self.dt*({2: self.dx, 3: self.dz}.get(state, Q(0))))
        for axis in (0, 1):
            for age in range(1, 16):
                for sign in (1, -1):
                    terms = [(self.strip(axis, age-1, sign), Q(1))]
                    if axis == 0:
                        terms.append((4 if sign == 1 else 10, age*self.dt**2*self.g))
                    self.terms.append(terms)
                    self.q.append(age*self.dt**2*[self.dx, self.dz][axis])
        # Two nonnegative combinations for each velocity bound and age.
        self.implications = []
        for axis in (0, 1):
            for age in range(1, 16):
                scale = 1/(age*self.dt)
                self.implications.extend([
                    (axis+2, axis, self.strip(axis, age, -1), scale),
                    (axis+8, axis+6, self.strip(axis, age, 1), scale)])

    def strip(self, axis, age, sign):
        if age == 0:
            return axis+(0 if sign == 1 else 6)
        return 12+axis*30+(age-1)*2+(0 if sign == 1 else 1)

    def initial(self):
        radius = [Q('.02'), Q('.02'), Q('.1'), Q('.1'), Q('.005'), Q('.01')]
        return [sum(abs(x)*r for x, r in zip(row, radius)) for row in self.h]

    def close(self, b):
        result = list(b)
        for target, pos, memory, scale in self.implications:
            result[target] = min(result[target], outward(scale*(b[pos]+b[memory])))
        return result

    def predict(self, b):
        return self.close([outward(sum(weight*b[col] for col, weight in terms)+q)
                           for terms, q in zip(self.terms, self.q)])

    def update(self, b, indices, measurements):
        result = list(b)
        for i, value in zip(indices, measurements):
            if not isinstance(value, Q):
                raise TypeError('measurement endpoints must be exact Fractions')
            # Deliberately no quantization: the rounding theorem uses exact strips.
            result[i] = min(result[i], value+self.noise[i])
            result[i+6] = min(result[i+6], -value+self.noise[i])
        return self.close(result)

    def rollout(self, b, horizon=25):
        chain = [list(b)]
        for _ in range(horizon):
            chain.append(self.predict(chain[-1]))
        return chain


def analytical_bounds(t):
    delta = Q(1, GRID)
    acceleration = [t.dx+t.g*t.noise[4], t.dz]
    cases = []
    for gap in (5, 10, 15):
        for age in range(15):
            velocity, position = [], []
            for a in acceleration:
                reset = 2*t.noise[0]/(gap*t.dt)+t.dt*a*(gap+1)/2
                velocity.append(reset+age*t.dt*a+65*delta)
                position.append(t.noise[0]+age*t.dt*reset+t.dt**2*a*age*(age-1)/2+100*delta)
            cases.append({'gap': gap, 'age': age, 'velocity': [str(x) for x in velocity],
                          'position': [str(x) for x in position]})
    return {'acceleration': [str(v) for v in acceleration], 'cases': cases,
            'max_velocity_halfwidth': [str(max(Q(c['velocity'][i]) for c in cases)) for i in (0, 1)],
            'max_position_halfwidth': [str(max(Q(c['position'][i]) for c in cases)) for i in (0, 1)],
            'initialization': 'prior position strip at tick0 is valid even if its position packet is absent; first success by tick10',
            'rounding_velocity_allowance': str(65*delta), 'rounding_position_allowance': str(100*delta)}


def obstruction(t):
    # Two affine-inclusion trajectories share all data through current tick14.
    # Position opportunities 5 and10 both fail; angles are exactly zero.
    age, horizon = 14, 25
    elapsed = age+horizon
    half_span = elapsed*t.dt*t.dx
    first_exit = int(Q(3)/(t.dt*t.dx))+1
    states = []
    x = np.array([Q(0)]*6, dtype=object)
    for k in range(elapsed+1):
        assert x[0] == t.dt**2*t.dx*k*(k-1)/2
        assert x[2] == k*t.dt*t.dx
        if k in (0, age, first_exit-1, first_exit, elapsed):
            states.append({'tick': k, 'positive_state': [str(v) for v in x],
                           'negative_state': [str(-v) for v in x]})
        x = t.f @ x+t.w[:, 0]
    assert half_span > 3
    return {'status': 'common_open_loop_outer_model_horizon_obstructed',
            'age': age, 'future_horizon': horizon, 'elapsed_ticks': elapsed,
            'terminal_velocity_half_span': str(half_span),
            'terminal_velocity_width': str(2*half_span), 'allowed_width': '6',
            'first_zero_center_velocity_violation_tick': first_exit, 'witnesses': states,
            'scope': 'global independent-box affine inclusion; not physical nonlinear impossibility and not feedback-policy MPC'}


def make_successes(label, ticks):
    if label == 'initial_two_misses':
        return set(range(10, ticks+1, 15))
    gaps = {'every5': [5], 'every15': [15], 'mixed': [5, 15, 10]}[label]
    successes, tick, i = {0}, 0, 0
    while tick <= ticks:
        tick += gaps[i % len(gaps)]
        if tick <= ticks:
            successes.add(tick)
        i += 1
    return successes


def verify_identities(t):
    for row, terms in enumerate(t.terms):
        actual = sum((weight*t.h[col] for col, weight in terms), np.array([Q(0)]*6))
        assert np.array_equal(actual, t.h[row] @ t.f)
        assert t.q[row] == sum(abs(x) for x in t.h[row] @ t.w)
        assert all(weight >= 0 for _, weight in terms)
    for target, a, b, scale in t.implications:
        assert np.array_equal(t.h[target], scale*(t.h[a]+t.h[b]))


def run(ticks=600):
    frozen = frozen_contract()
    t = Transport()
    assert str(t.dx) == frozen['dx'] and str(t.dz) == frozen['dz']
    verify_identities(t)
    bounds = analytical_bounds(t)
    max_v = list(map(Q, bounds['max_velocity_halfwidth']))
    max_p = list(map(Q, bounds['max_position_halfwidth']))
    limit = [Q(5), Q('1.5'), Q(3), Q(3), Q('.45'), Q(2)]
    cases = []
    for label in ('every5', 'every15', 'mixed', 'initial_two_misses'):
        successes = make_successes(label, ticks)
        misses = 0
        for tick in range(0, ticks+1, 5):
            misses = 0 if tick in successes else misses+1
            assert misses <= 2
        x = np.array([Q('.005'), Q('-.004'), Q('.03'), Q('-.02'), Q('.001'), Q(0)], dtype=object)
        b, old, snapshots = t.initial(), None, []
        peak_v, peak_p = [Q(0)]*2, [Q(0)]*2
        shift_rows, memberships = 0, 0
        all_posterior_domain, first_future_failure = True, None
        digest = hashlib.sha256()
        for tick in range(ticks+1):
            if tick:
                x = t.f @ x
                b = old[1]
            indices = [4, 5]+([0, 1] if tick in successes else [])
            y = [x[i]+t.noise[i]*Q((-1)**(tick+j), 2) for j, i in enumerate(indices)]
            previous = b
            b = t.update(b, indices, y)
            assert all(a <= c for a, c in zip(b, previous))
            for i in (0, 1):
                vp, pp = (b[i+2]+b[i+8])/2, (b[i]+b[i+6])/2
                assert vp <= max_v[i] and pp <= max_p[i]
                peak_v[i], peak_p[i] = max(peak_v[i], vp), max(peak_p[i], pp)
            all_posterior_domain &= all(b[i] <= limit[i % 6] for i in range(12))
            chain = t.rollout(b)
            if old is not None:
                for stage in range(25):
                    assert all(a <= c for a, c in zip(chain[stage], old[stage+1]))
                    shift_rows += len(b)
            for stage, future in enumerate(chain):
                if first_future_failure is None and any(future[i] > limit[i % 6] for i in range(12)):
                    first_future_failure = {'tick': tick, 'stage': stage}
            if tick in (0, 15, 30, 60, 150, 300, ticks):
                template = Template(t.h, b)
                cz, latent = template.to_cz(), template.witness(x)
                assert all(abs(v) <= 1 for v in latent)
                assert np.array_equal(cz.c+cz.g @ latent, x)
                assert np.array_equal(cz.a @ latent, cz.b)
                memberships += 1
                snapshots.append({'tick': tick, 'velocity_halfwidth': [str((b[i]+b[i+6])/2) for i in (2, 3)],
                                  'position_halfwidth': [str((b[i]+b[i+6])/2) for i in (0, 1)],
                                  'bounds': [str(v) for v in b]})
            digest.update(('|'.join(str(v) for v in b)+'\n').encode())
            old = chain
        cases.append({'name': label, 'ticks': ticks, 'shift_rows': shift_rows,
                      'checked_cz_memberships': memberships, 'snapshots': snapshots,
                      'peak_velocity_halfwidth': [str(v) for v in peak_v],
                      'peak_position_halfwidth': [str(v) for v in peak_p],
                      'posterior_coordinate_domain_check': bool(all_posterior_domain),
                      'first_future_coordinate_domain_failure': first_future_failure,
                      'posterior_bounds_sha256': digest.hexdigest()})
        print(label, 'peak v', [float(v) for v in peak_v], 'domain', all_posterior_domain,
              'future', first_future_failure, flush=True)
    return {'status': 'bounded_posterior_and_monotone_transport_certified_for_affine_contract',
            'direction_count': len(t.h), 'cz_generators': 66, 'cz_equalities': 60,
            'transport_identities': len(t.terms), 'closure_identities': len(t.implications),
            'online_support_lp_calls': 0, 'grid_denominator': GRID,
            'analytic_all_gap_age_bounds': bounds, 'cases': cases, 'obstruction': obstruction(t),
            'mpc_gate': 'blocked_common_open_loop_predictor; feedback_and_terminal_contract_required',
            'realtime_gate': 'not_certified',
            'source_sha256': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                              for p in [Path(__file__), ROOT/'verification/check_cz_template.py',
                                        ROOT/'verification/check_constrained_zonotope.py',
                                        ROOT/'configs/planar_baseline.json']}}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--ticks', type=int, default=600)
    args = parser.parse_args()
    if args.output.exists() or args.ticks < 30:
        parser.error('output must be new and ticks at least 30')
    result = run(args.ticks)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
