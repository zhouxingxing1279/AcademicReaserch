"""Replay saved measurements and audit logged transitions without solving MPC.

This is an independent data path, not an independent external review.
"""
import csv
import hashlib
import json
from dataclasses import replace
from pathlib import Path
import numpy as np
from experiments.finite_memory_tube import schedule
from src.outerloop.finite_memory import Contract, FiniteMemoryEstimator
from src.outerloop.tube_mpc import TubeDesign


def main():
    p = Path('experiments/results/finite_memory_tube')
    result = json.loads((p/'results.json').read_text())
    for name, expected in result['source_hashes'].items():
        source = Path(name.replace('\\', '/'))
        actual = hashlib.sha256(source.read_bytes().replace(b'\r\n', b'\n')).hexdigest()
        assert actual == expected, f'Source changed since run: {source}'
    with (p/'trajectories.csv').open() as f:
        raw = list(csv.DictReader(f))
    grouped = {}
    for row in raw:
        key = row['case'], int(row['seed']), row['mode']
        grouped.setdefault(key, {})[(int(row['k']), int(row['axis']))] = row
    assert len(grouped) == 26 and len(raw) == 6240
    tolerance, worst_transition, worst_estimate, checked = 2e-7, 0., 0., 0
    stimuli = {}
    for summary in result['summaries']:
        name, seed, mode = summary['case'], summary['seed'], summary['mode']
        c = replace(Contract(), missing=summary['M'], delay=summary['L'])
        d = TubeDesign(c)
        N = summary['steps']
        rows = grouped[name, seed, mode]
        assert len(rows) == 3*N
        rng = np.random.default_rng(seed)
        events = schedule(c, N, name, rng)
        w = rng.uniform(-c.acceleration, c.acceleration, (N, 3))
        noise = rng.uniform(-c.noise, c.noise, (N, 3))
        if name == 'max_gap':
            w[:] = c.acceleration*np.array([1, -1, 1])
            noise[:] = c.noise*np.array([1, -1, 1])
        elif name == 'reorder':
            w = c.acceleration*((-1.)**np.arange(N))[:, None]*np.array([[1, -1, 1]])
            noise = c.noise*((-1.)**np.arange(N))[:, None]*np.array([[1, 1, -1]])
        initial = np.array([[1.5, 0.], [-1., 0.], [.6, 0.]])
        x0 = initial+rng.uniform(-1, 1, (3, 2))*[c.initial_p, c.initial_v]
        stim = dict(events=events, acceleration=w.tolist(), measurement_noise=noise.tolist(),
                    initial_true_state=x0.tolist(), M=c.missing, L=c.delay)
        key = name+':'+str(seed)
        if key in stimuli:
            assert stimuli[key] == stim
        stimuli[key] = stim
        filters = [FiniteMemoryEstimator(c, state, mode == 'cz') for state in initial]
        arrivals = {}
        for k, event in enumerate(events):
            if event >= 0:
                arrivals.setdefault(k+event, []).append(k)
        for k in range(N):
            for axis in range(3):
                row = rows[k, axis]
                x = np.array([float(row['p']), float(row['velocity'])])
                hat = np.array([float(row['p_hat']), float(row['v_hat'])])
                z = np.array([float(row['p_nominal']), float(row['v_nominal'])])
                u, nominal = float(row['command']), float(row['nominal_command'])
                if k == 0:
                    np.testing.assert_allclose(x, x0[axis], atol=1e-12, rtol=0)
                received = [(s, float(rows[s, axis]['p'])+noise[s, axis])
                            for s in reversed(arrivals.get(k, []))]
                cz = filters[axis].observe(received)
                estimate_residual = float(np.max(np.abs(cz.representative()-hat)))
                worst_estimate = max(worst_estimate, estimate_residual)
                assert estimate_residual <= tolerance and cz.contains(x)
                assert np.all(np.abs(x-hat) <= d.E+tolerance)
                assert abs(u-nominal-d.K@(hat-z)) <= tolerance
                next_x, next_z = d.A@x+d.B*(u+w[k, axis]), d.A@z+d.B*nominal
                assert d.in_tube(x-z) and d.in_tube(next_x-next_z)
                assert np.all(np.abs(next_x) <= d.state_limits+np.array([tolerance]*2))
                assert abs(u) <= d.input_limit+tolerance
                if k+1 < N:
                    nextrow = rows[k+1, axis]
                    recorded_x = [float(nextrow['p']), float(nextrow['velocity'])]
                    recorded_z = [float(nextrow['p_nominal']), float(nextrow['v_nominal'])]
                    residual = max(float(np.max(np.abs(next_x-recorded_x))),
                                   float(np.max(np.abs(next_z-recorded_z))))
                    worst_transition = max(worst_transition, residual)
                    assert residual <= tolerance
                filters[axis].advance(u)
                assert cz.generators.shape[1] <= 2*c.span+1
                assert len(filters[axis].commands) <= c.span
                checked += 1
    audit = dict(axis_steps_replayed=checked, cases=len(grouped), stimuli=len(stimuli),
                 maximum_transition_residual=worst_transition,
                 maximum_estimate_replay_residual=worst_estimate, tolerance=tolerance,
                 source_hash_check='passed', all_checks='passed',
                 scope='Numerical replay, not directed-rounding certification or independent peer review')
    (p/'stimuli.json').write_text(json.dumps(stimuli, indent=2), encoding='utf-8')
    (p/'replay_audit.json').write_text(json.dumps(audit, indent=2), encoding='utf-8')
    print(json.dumps(audit))


if __name__ == '__main__':
    main()
