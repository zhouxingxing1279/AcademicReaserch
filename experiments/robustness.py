"""Disturbance-first validation. No changes to the estimator or controller.

Run: .venv/Scripts/python.exe -m experiments.robustness
Plan: docs/research/proposal/ROBUSTNESS_PLAN.md
"""
import csv
import hashlib
import json
import platform
import time
from dataclasses import asdict, replace
from fractions import Fraction as F
from itertools import product
from pathlib import Path

import numpy as np
import scipy
import osqp
from scipy.optimize import linprog
from src.outerloop.finite_memory import Contract, ContractError, FiniteMemoryEstimator
from src.outerloop.tube_mpc import TubeDesign, NominalMPC
from experiments.finite_memory_tube import schedule

OUT = Path('experiments/results/robustness')
TOL = 2e-6
ONSET, END_PULSE, STEPS = 20, 30, 60


def radius_lines(M, L):
    """Independent rational intercept/slope expansion of the declared E bound."""
    T, n, Q = F(1, 2), F(1, 200), 2*M+L+1
    p, v = [], []
    for h in range(M+L+1):
        for d in range(1, Q-h+1):
            p.append((2*n+4*h*n/d, h*d*T*T+h*h*T*T))
            v.append((4*n/(d*T), d*T+2*h*T))
    for k in range(Q):
        p.append((F(1, 200)+k*T/100, (k*T)**2/2))
        v.append((F(1, 100), k*T))
    return p, v


def exact_budget(M, L):
    p, v = radius_lines(M, L)
    limits = []
    # Input margin = 3a+16Ep+12Ev; state margins = (delta/4,delta).
    for (p0, p1), (v0, v1) in product(p, v):
        for label, bound, c0, c1 in [
            ('input', F(4), 16*p0+12*v0, 3+16*p1+12*v1),
            ('position', F(12), 4*p0+3*v0, 1+4*p1+3*v1),
            ('velocity', F(2), 4*p0+3*v0, 1+4*p1+3*v1)]:
            limits.append(((bound-c0)/c1, label))
    upper, active = min(limits)
    # Initial box fits iff delta >= .03; delta is nondecreasing in a.
    delta0 = 4*max(x[0] for x in p)+3*max(x[0] for x in v)
    return dict(M=M, L=L, strict_upper_fraction=str(upper),
                strict_upper=float(upper), active_constraint=active,
                positive_interval=bool(upper > 0), initial_box_admitted_at_zero=delta0 >= F(3, 100))


def budget_scan():
    records, grids = [], []
    for M, L in product(range(4), repeat=2):
        record = exact_budget(M, L)
        record['samples'] = []
        for a in [0., .01, .02, .03, .04, .06, .08]:
            sample = dict(a=a)
            try:
                d = TubeDesign(replace(Contract(), missing=M, delay=L, acceleration=a))
                sample.update(budget='positive', nominal_input=d.v_limit)
                try:
                    NominalMPC(d).solve(np.array([1.5, 0.]))
                    sample['initial_qp'] = 'solved'
                except RuntimeError as e:
                    sample['initial_qp'] = str(e)
            except ValueError as e:
                sample.update(budget='not_certified', reason=str(e))
            record['samples'].append(sample)
        records.append(record)
    for a in [.01, .02, .03, .04]:
        item = dict(a=a, total=21*17)
        try:
            d = TubeDesign(replace(Contract(), acceleration=a))
        except ValueError as e:
            item.update(status='not_certified', reason=str(e))
            grids.append(item)
            continue
        opt = NominalMPC(d)
        feasible = infeasible = unresolved = 0
        for p, v in product(np.linspace(-3, 3, 21), np.linspace(-2, 2, 17)):
            z = np.array([p, v])
            if np.any(np.abs(z) > d.z_limit+1e-9):
                infeasible += 1
                continue
            low, high = opt.bounds(z)
            finite = np.isfinite(low)
            result = linprog(np.zeros(opt.N),
                             A_ub=np.vstack([opt.constraint, -opt.constraint[finite]]),
                             b_ub=np.r_[high, -low[finite]],
                             bounds=[(None, None)]*opt.N, method='highs')
            if result.success and opt.violation(z, result.x) <= TOL:
                feasible += 1
            elif result.status == 2:
                infeasible += 1
            else:
                unresolved += 1
        item.update(status='evaluated', feasible=feasible, infeasible=infeasible, unresolved=unresolved)
        grids.append(item)
    return records, grids


def stimulus(seed, delivery, profile, factor, steps=STEPS):
    c = Contract()
    rng = np.random.default_rng(seed)
    events = schedule(c, steps, delivery, rng)
    initial = np.array([[1.5, 0.], [-1., 0.], [.6, 0.]])
    x0 = initial+rng.uniform(-1, 1, (3, 2))*[c.initial_p, c.initial_v]
    noise = rng.uniform(-c.noise, c.noise, (steps, 3))
    w = np.zeros((steps, 3))
    if profile == 'random':
        w[ONSET:] = rng.uniform(-1, 1, (steps-ONSET, 3))
    else:
        noise[:] = c.noise*np.array([1, -1, 1])
        end = END_PULSE if profile == 'pulse' else steps
        w[ONSET:end] = np.array([1, -1, 1])
        if profile == 'alternating':
            w *= ((-1.)**np.arange(steps))[:, None]
    w *= factor*c.acceleration
    return dict(seed=seed, delivery=delivery, profile=profile, factor=factor,
                initial=x0.tolist(), nominal_initial=initial.tolist(),
                events=events, noise=noise.tolist(), disturbance=w.tolist())


def recovery(rows, complete):
    if not complete:
        return None
    by_time = {}
    for r in rows:
        by_time.setdefault(r['k']+1, []).append(abs(r['next_p']) <= .05 and abs(r['next_v']) <= .1)
    for t in range(END_PULSE, STEPS-4):
        if all(len(by_time.get(j, [])) == 3 and all(by_time[j]) for j in range(t, STEPS+1)):
            return (t-END_PULSE)*.5
    return None


def run_case(case_id, mode, stim):
    c, d = Contract(), TubeDesign(Contract())
    x, z = np.array(stim['initial']), np.array(stim['nominal_initial'])
    filters = [FiniteMemoryEstimator(c, zz, constrained=mode == 'cz') for zz in z]
    opts = [NominalMPC(d) for _ in range(3)]
    pending, rows, first, counts = {}, [], {}, dict.fromkeys(
        ['containment', 'error_bound', 'tube', 'state', 'input', 'shift', 'descent'], 0)
    status, reason, failure_step = 'completed', '', None
    for k, event in enumerate(stim['events']):
        if event >= 0:
            pending.setdefault(k+event, []).append((k, x[:, 0]+stim['noise'][k]))
        arrivals = list(reversed(pending.pop(k, [])))
        # Prepare all three commands before applying any axis transition.
        prepared = []
        try:
            for axis in range(3):
                posterior = filters[axis].observe([(s, y[axis]) for s, y in arrivals])
                hat = posterior.representative()
                contained = posterior.contains(x[axis])
                seq = opts[axis].solve(z[axis])
                u = float(seq[0]+d.K@(hat-z[axis]))
                nz = d.A@z[axis]+d.B*seq[0]
                nx = d.A@x[axis]+d.B*(u+stim['disturbance'][k][axis])
                shifted = opts[axis].shifted(z[axis], seq)
                shift = opts[axis].violation(nz, shifted)
                drop = (opts[axis].cost(nz, shifted)-opts[axis].cost(z[axis], seq)
                        +z[axis]@d.Q@z[axis]+d.R*seq[0]**2)
                prepared.append((hat, contained, u, nx, nz, shift, drop, seq[0]))
        except ContractError as e:
            status, reason, failure_step = 'estimator_contract_error', str(e), k
            break
        except RuntimeError as e:
            reason, failure_step = str(e), k
            status = ('qp_infeasible' if 'primal infeasible' in reason else
                      'nominal_state_infeasible' if 'tightened constraints' in reason else
                      'numerical_residual_failure' if 'residual' in reason else 'solver_unresolved')
            break
        for axis, (hat, contained, u, nx, nz, shift, drop, nominal_u) in enumerate(prepared):
            flags = dict(containment=not contained,
                         error_bound=bool(np.any(np.abs(x[axis]-hat) > d.E+TOL)),
                         tube=not d.in_tube(nx-nz, TOL),
                         state=bool(np.any(np.abs(nx) > np.array(d.state_limits)+TOL)),
                         input=abs(u) > d.input_limit+TOL, shift=shift > TOL, descent=drop > TOL)
            for name, flag in flags.items():
                counts[name] += int(flag)
                if flag:
                    first.setdefault(name, k)
            rows.append(dict(case_id=case_id, mode=mode, k=k, axis=axis,
                             p=float(x[axis, 0]), v=float(x[axis, 1]),
                             p_hat=float(hat[0]), v_hat=float(hat[1]),
                             z_p=float(z[axis, 0]), z_v=float(z[axis, 1]),
                             u=u, nominal_u=float(nominal_u), w=stim['disturbance'][k][axis],
                             next_p=float(nx[0]), next_v=float(nx[1]),
                             p_margin=3-abs(float(nx[0])), v_margin=2-abs(float(nx[1])),
                             input_margin=4-abs(u), **{f'fail_{key}': int(val) for key, val in flags.items()}))
            filters[axis].advance(u)
            x[axis], z[axis] = nx, nz
        if counts['state'] or counts['input']:
            status, reason, failure_step = 'hard_constraint_violation', 'No certified fallback; stopped', k
            break
    post = [r for r in rows if r['k'] >= ONSET]
    summary = dict(case_id=case_id, mode=mode, profile=stim['profile'], delivery=stim['delivery'],
                   seed=stim['seed'], factor=stim['factor'], in_contract=stim['factor'] <= 1,
                   status=status, reason=reason, failure_step=failure_step, axis_steps=len(rows),
                   counts=counts, first_failure=first,
                   observed_safe_complete=status == 'completed' and not counts['state'] and not counts['input'],
                   all_checks_pass=status == 'completed' and not any(counts.values()),
                   min_p_margin=min([3-abs(xx[0]) for xx in stim['initial']]+[r['p_margin'] for r in rows]),
                   min_v_margin=min([2-abs(xx[1]) for xx in stim['initial']]+[r['v_margin'] for r in rows]),
                   min_input_margin=min((r['input_margin'] for r in rows), default=None),
                   peak_p_after_onset=max((abs(r['next_p']) for r in post), default=None),
                   peak_v_after_onset=max((abs(r['next_v']) for r in post), default=None),
                   peak_u_after_onset=max((abs(r['u']) for r in post), default=None),
                   recovery_seconds=recovery(rows, status == 'completed') if stim['profile'] == 'pulse' else None)
    return summary, rows


def paired_statistics(summaries):
    output = {}
    pairs = {mode: {s['seed']: s for s in summaries if s['profile'] == 'random' and s['mode'] == mode}
             for mode in ['cz', 'pair']}
    good = [s for s in sorted(pairs['cz']) if all(pairs[m][s]['status'] == 'completed' for m in pairs)]
    rng = np.random.default_rng(20261104)
    for metric in ['peak_p_after_onset', 'peak_v_after_onset', 'peak_u_after_onset']:
        diff = np.array([pairs['cz'][s][metric]-pairs['pair'][s][metric] for s in good])
        if len(diff):
            boot = diff[rng.integers(len(diff), size=(5000, len(diff)))].mean(axis=1)
            output[metric] = dict(n_pairs=len(diff), mean_cz_minus_pair=float(diff.mean()),
                                  interval95=np.quantile(boot, [.025, .975]).tolist(),
                                  cz_mean=float(np.mean([pairs['cz'][s][metric] for s in good])),
                                  pair_mean=float(np.mean([pairs['pair'][s][metric] for s in good])))
    return output


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    budgets, grids = budget_scan()
    stimuli = {}
    for factor, delivery, profile in product([.5, 1, 2, 4, 8, 16, 32],
                                              ['fresh', 'max_gap', 'random'],
                                              ['bias', 'pulse', 'alternating']):
        key = f'stress_{factor:g}_{delivery}_{profile}'
        stimuli[key] = stimulus(20261104, delivery, profile, factor)
    for seed in range(50):
        stimuli[f'random_{seed}'] = stimulus(seed, 'random', 'random', 1)
    (OUT/'stimuli.json').write_text(json.dumps(stimuli, indent=2), encoding='utf-8')
    summaries = []
    with (OUT/'trajectories.csv').open('w', newline='', encoding='utf-8') as file:
        writer = None
        for i, (key, stim) in enumerate(stimuli.items()):
            for mode in ['cz', 'pair']:
                summary, rows = run_case(key, mode, stim)
                summaries.append(summary)
                if writer is None:
                    writer = csv.DictWriter(file, fieldnames=list(rows[0]))
                    writer.writeheader()
                writer.writerows(rows)
            if i % 10 == 0:
                print(f'{len(summaries)}/{2*len(stimuli)} trajectories; {time.perf_counter()-started:.1f}s', flush=True)
    sources = ['experiments/robustness.py', 'experiments/finite_memory_tube.py',
               'src/outerloop/finite_memory.py', 'src/outerloop/tube_mpc.py',
               'docs/research/proposal/ROBUSTNESS_PLAN.md', 'requirements-research.txt']
    hashes = {s: hashlib.sha256(Path(s).read_bytes().replace(b'\r\n', b'\n')).hexdigest() for s in sources}
    result = dict(contract=asdict(Contract()), tolerance=TOL, onset=ONSET, end_pulse=END_PULSE,
                  horizon_steps=STEPS, budgets=budgets, feasible_grid=grids, summaries=summaries,
                  paired_statistics=paired_statistics(summaries), source_hashes=hashes,
                  stimulus_sha256=hashlib.sha256((OUT/'stimuli.json').read_bytes()).hexdigest(),
                  environment=dict(python=platform.python_version(), numpy=np.__version__,
                                   scipy=scipy.__version__, osqp=osqp.__version__),
                  wall_seconds=time.perf_counter()-started,
                  scope='Exact budget algebra plus finite float simulations; no physical or WCET claim')
    (OUT/'results.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(dict(cases=len(summaries), axis_steps=sum(s['axis_steps'] for s in summaries),
                         in_contract_failures=[s['case_id'] for s in summaries if s['in_contract'] and not s['all_checks_pass']],
                         seconds=result['wall_seconds'])), flush=True)


if __name__ == '__main__':
    main()
