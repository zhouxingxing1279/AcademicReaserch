"""Replay saved stimuli and trajectories without rerunning MPC optimization."""
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
import numpy as np
from src.outerloop.finite_memory import Contract, ContractError, FiniteMemoryEstimator
from src.outerloop.tube_mpc import TubeDesign
from experiments.robustness import OUT, TOL


def check():
    result = json.loads((OUT/'results.json').read_text(encoding='utf-8'))
    for name, expected in result['source_hashes'].items():
        assert hashlib.sha256(Path(name).read_bytes().replace(b'\r\n', b'\n')).hexdigest() == expected, name
    assert hashlib.sha256((OUT/'stimuli.json').read_bytes()).hexdigest() == result['stimulus_sha256']
    stimuli = json.loads((OUT/'stimuli.json').read_text(encoding='utf-8'))
    grouped = defaultdict(list)
    with (OUT/'trajectories.csv').open(encoding='utf-8', newline='') as file:
        for row in csv.DictReader(file):
            grouped[row['case_id'], row['mode']].append(row)
    assert len(result['summaries']) == 226
    assert len({(s['case_id'], s['mode']) for s in result['summaries']}) == 226
    c, d = Contract(), TubeDesign(Contract())
    maximum, steps, verified_stops = 0., 0, 0
    for index, summary in enumerate(result['summaries']):
        key = summary['case_id'], summary['mode']
        rows = grouped[key]
        stim = stimuli[key[0]]
        assert len(rows) == summary['axis_steps'] and len(rows) % 3 == 0
        x, z = np.array(stim['initial']), np.array(stim['nominal_initial'])
        filters = [FiniteMemoryEstimator(c, zz, constrained=key[1] == 'cz') for zz in z]
        pending = {}
        for k in range(len(rows)//3):
            event = stim['events'][k]
            if event >= 0:
                pending.setdefault(k+event, []).append((k, x[:, 0]+stim['noise'][k]))
            arrivals = list(reversed(pending.pop(k, [])))
            for axis in range(3):
                row = rows[3*k+axis]
                assert int(row['k']) == k and int(row['axis']) == axis
                posterior = filters[axis].observe([(s, y[axis]) for s, y in arrivals])
                hat = posterior.representative()
                saved_hat = np.array([float(row['p_hat']), float(row['v_hat'])])
                u, nominal_u = float(row['u']), float(row['nominal_u'])
                actual_u = nominal_u+d.K@(hat-z[axis])
                nx = d.A@x[axis]+d.B*(u+stim['disturbance'][k][axis])
                nz = d.A@z[axis]+d.B*nominal_u
                for observed, expected in [
                    (np.array([float(row['p']), float(row['v'])]), x[axis]),
                    (np.array([float(row['z_p']), float(row['z_v'])]), z[axis]),
                    (saved_hat, hat), (u, actual_u),
                    (np.array([float(row['next_p']), float(row['next_v'])]), nx),
                    (float(row['w']), stim['disturbance'][k][axis]),
                    (float(row['p_margin']), 3-abs(nx[0])),
                    (float(row['v_margin']), 2-abs(nx[1])),
                    (float(row['input_margin']), 4-abs(u))]:
                    residual = float(np.max(np.abs(np.asarray(observed)-expected)))
                    maximum = max(maximum, residual)
                    assert residual < 2e-7, (key, k, axis, residual)
                flags = dict(containment=not posterior.contains(x[axis]),
                             error_bound=bool(np.any(np.abs(x[axis]-hat) > d.E+TOL)),
                             tube=not d.in_tube(nx-nz, TOL),
                             state=bool(np.any(np.abs(nx) > np.array(d.state_limits)+TOL)),
                             input=abs(u) > d.input_limit+TOL)
                for label, flag in flags.items():
                    assert int(row['fail_'+label]) == int(flag), (key, k, label)
                filters[axis].advance(u)
                x[axis], z[axis] = nx, nz
                steps += 1
        for label, count in summary['counts'].items():
            assert sum(int(r['fail_'+label]) for r in rows) == count, (key, label)
        for metric, coordinate, limit in [('min_p_margin', 0, 3), ('min_v_margin', 1, 2)]:
            column = 'p_margin' if coordinate == 0 else 'v_margin'
            expected = min([limit-abs(xx[coordinate]) for xx in stim['initial']]
                           +[float(row[column]) for row in rows])
            assert abs(summary[metric]-expected) < 1e-12
        if summary['status'] == 'estimator_contract_error':
            k = len(rows)//3
            assert k == summary['failure_step']
            event = stim['events'][k]
            if event >= 0:
                pending.setdefault(k+event, []).append((k, x[:, 0]+stim['noise'][k]))
            arrivals = list(reversed(pending.pop(k, [])))
            try:
                for axis in range(3):
                    filters[axis].observe([(s, y[axis]) for s, y in arrivals]).representative()
            except ContractError:
                verified_stops += 1
            else:
                raise AssertionError(('Claimed estimator failure did not replay', key))
        if index % 40 == 0:
            print(f'Replayed {index+1}/226 trajectories', flush=True)
    audit = dict(cases=226, axis_steps=steps, maximum_replay_residual=maximum,
                 estimator_failure_stops_reproduced=verified_stops, all_checks='passed',
                 scope='Same-library numerical replay of estimates, dynamics, controls and flags; '
                       'not independent theorem review; MPC optimum and shifted sequence not recomputed')
    (OUT/'replay_audit.json').write_text(json.dumps(audit, indent=2), encoding='utf-8')
    print(json.dumps(audit), flush=True)


if __name__ == '__main__':
    check()
