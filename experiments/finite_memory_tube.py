"""Local reproducible benchmark; run from repository root with .venv Python."""
import csv
import hashlib
import json
import platform
import time
from dataclasses import replace, asdict
from pathlib import Path
import numpy as np
import scipy
import osqp
from src.outerloop.finite_memory import (Contract, FiniteMemoryEstimator,
                                        pair_window, full_history, arrival_graph)
from src.outerloop.tube_mpc import TubeDesign, NominalMPC

OUT = Path('experiments/results/finite_memory_tube')


def schedule(c, steps, name, rng):
    events, gap = [], 0
    for k in range(steps):
        if name == 'fresh':
            event = 0
        elif name == 'max_gap':
            event = -1 if gap < c.missing else c.delay
        elif name == 'reorder':
            event = c.delay if k % 2 == 0 else 0
        else:
            event = -1 if gap < c.missing and rng.random() < .4 else int(rng.integers(c.delay+1))
        gap = gap+1 if event == -1 else 0
        events.append(event)
    return events


def run_case(name, seed, mode, c, steps=80):
    rng = np.random.default_rng(seed)
    events = schedule(c, steps, name, rng)
    # Pre-generate common exogenous disturbances independently of controller.
    w = rng.uniform(-c.acceleration, c.acceleration, (steps, 3))
    noise = rng.uniform(-c.noise, c.noise, (steps, 3))
    if name == 'max_gap':
        w[:] = c.acceleration*np.array([1, -1, 1])
        noise[:] = c.noise*np.array([1, -1, 1])
    elif name == 'reorder':
        w = c.acceleration*((-1.)**np.arange(steps))[:, None]*np.array([[1, -1, 1]])
        noise = c.noise*((-1.)**np.arange(steps))[:, None]*np.array([[1, 1, -1]])
    d = TubeDesign(c)
    z = np.array([[1.5, 0.], [-1., 0.], [.6, 0.]])
    initial = z.copy()
    x = z+rng.uniform(-1, 1, (3, 2))*[c.initial_p, c.initial_v]
    filters = [FiniteMemoryEstimator(c, v, constrained=mode == 'cz') for v in z]
    optimizers = [NominalMPC(d) for _ in range(3)]
    pending, rows, comparisons = {}, [], []
    all_packets, all_commands = [{}, {}, {}], [{}, {}, {}]
    counts = dict(containment=0, error_bound=0, tube=0, state=0, input=0, shift=0, descent=0)
    for k in range(steps):
        if events[k] >= 0:
            pending.setdefault(k+events[k], []).append((k, x[:, 0]+noise[k]))
        arrivals = list(reversed(pending.pop(k, [])))
        for axis in range(3):
            tic = time.perf_counter()
            known = [(stamp, value[axis]) for stamp, value in arrivals]
            posterior = filters[axis].observe(known)
            hat = posterior.representative()
            estimate_ms = (time.perf_counter()-tic)*1000
            low, high = posterior.bounds()
            contains = posterior.contains(x[axis])
            tic = time.perf_counter()
            seq = optimizers[axis].solve(z[axis])
            qp_ms = (time.perf_counter()-tic)*1000
            actual_u = seq[0]+d.K@(hat-z[axis])
            next_z = d.A@z[axis]+d.B*seq[0]
            next_x = d.A@x[axis]+d.B*(actual_u+w[k, axis])
            shift = optimizers[axis].shifted(z[axis], seq)
            shift_violation = optimizers[axis].violation(next_z, shift)
            drop = (optimizers[axis].cost(next_z, shift)-optimizers[axis].cost(z[axis], seq)
                    +z[axis]@d.Q@z[axis]+d.R*seq[0]**2)
            counts['containment'] += int(not contains)
            counts['error_bound'] += int(np.any(np.abs(x[axis]-hat) > d.E+1e-7))
            counts['tube'] += int(not d.in_tube(next_x-next_z, 2e-6))
            counts['state'] += int(np.any(np.abs(next_x) > np.array(d.state_limits)+1e-6))
            counts['input'] += int(abs(actual_u) > d.input_limit+1e-6)
            counts['shift'] += int(shift_violation > 2e-6)
            counts['descent'] += int(drop > 2e-6)
            rows.append(dict(case=name, seed=seed, mode=mode, axis=axis, k=k,
                             p=x[axis, 0], velocity=x[axis, 1], p_hat=hat[0], v_hat=hat[1],
                             p_nominal=z[axis, 0], v_nominal=z[axis, 1], command=actual_u,
                             nominal_command=seq[0], p_width=high[0]-low[0], v_width=high[1]-low[1],
                             generators=posterior.generators.shape[1], equalities=len(posterior.rhs),
                             estimate_ms=estimate_ms, qp_ms=qp_ms, shift_violation=shift_violation,
                             sample_contained=int(contains)))
            all_packets[axis].update(known)
            if axis == 0 and seed == 0 and k < 40 and len(filters[axis].packets) >= 2:
                # Both representations see exactly the SAME history and commands.
                cz = pair_window(c, k, filters[axis].packets, filters[axis].commands, True)
                pair = pair_window(c, k, filters[axis].packets, filters[axis].commands, False)
                full = full_history(c, k, all_packets[axis], all_commands[axis], initial[axis])
                cl, ch = cz.bounds()
                pl, ph = pair.bounds()
                fl, fh = full.bounds()
                assert np.all(cl <= fl+2e-7) and np.all(fh <= ch+2e-7)
                assert np.all(pl <= cl+2e-7) and np.all(ch <= ph+2e-7)
                comparisons.append(dict(case=name, mode=mode, k=k, cz_p=ch[0]-cl[0],
                                        cz_v=ch[1]-cl[1], pair_p=ph[0]-pl[0], pair_v=ph[1]-pl[1],
                                        full_p=fh[0]-fl[0], full_v=fh[1]-fl[1],
                                        cz_generators=cz.generators.shape[1],
                                        full_generators=full.generators.shape[1]))
            filters[axis].advance(actual_u)
            all_commands[axis][k] = actual_u
            x[axis], z[axis] = next_x, next_z
    summary = dict(case=name, seed=seed, mode=mode, M=c.missing, L=c.delay,
                   steps=steps, axis_steps=len(rows), failures=counts,
                   max_generators=max(r['generators'] for r in rows),
                   max_equalities=max(r['equalities'] for r in rows),
                   position_rmse=float(np.sqrt(np.mean([r['p']**2 for r in rows]))),
                   estimation_rmse=float(np.sqrt(np.mean([(r['p']-r['p_hat'])**2 for r in rows]))),
                   max_command=max(abs(r['command']) for r in rows),
                   estimate_ms_p95=float(np.quantile([r['estimate_ms'] for r in rows], .95)),
                   estimate_ms_max=max(r['estimate_ms'] for r in rows),
                   qp_ms_p95=float(np.quantile([r['qp_ms'] for r in rows], .95)),
                   qp_ms_max=max(r['qp_ms'] for r in rows))
    assert summary['max_generators'] <= 2*c.span+1
    assert summary['max_equalities'] <= c.span-1
    return summary, rows, comparisons


def write_csv(path, rows):
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    start = time.perf_counter()
    summaries, rows, comparisons, grid = [], [], [], []
    c = Contract()
    for M in range(4):
        for L in range(4):
            cc = replace(c, missing=M, delay=L)
            record = dict(M=M, L=L, **arrival_graph(M, L))
            try:
                d = TubeDesign(cc)
                record.update(status='nonempty', input_margin=d.input_margin,
                              nominal_input=d.v_limit, E=d.E.tolist())
            except ValueError as e:
                record.update(status='not_certified', reason=str(e))
            grid.append(record)
    cases = [('fresh', 0, c), ('max_gap', 0, c), ('reorder', 0, replace(c, delay=2))]
    cases += [('random', seed, c) for seed in range(10)]
    for name, seed, cc in cases:
        for mode in ['cz', 'pair']:
            summary, rr, comp = run_case(name, seed, mode, cc)
            summaries.append(summary)
            rows.extend(rr)
            comparisons.extend(comp)
            print(json.dumps(summary), flush=True)
    write_csv(OUT/'trajectories.csv', rows)
    write_csv(OUT/'matched_information.csv', comparisons)
    hashes = {str(p): hashlib.sha256(p.read_bytes().replace(b'\r\n', b'\n')).hexdigest()
              for p in [Path('experiments/finite_memory_tube.py'), Path('src/outerloop/finite_memory.py'),
                        Path('src/outerloop/tube_mpc.py'), Path('requirements-research.txt')]}
    results = dict(contract=asdict(c), seed_count=10, summaries=summaries,
                   delivery_graph_and_budget=grid, wall_seconds=time.perf_counter()-start,
                   total_axis_steps=len(rows), source_hashes=hashes,
                   environment=dict(python=platform.python_version(), platform=platform.platform(),
                                    numpy=np.__version__, scipy=scipy.__version__, osqp=osqp.__version__),
                   evidence='float64 finite simulations, not formal arithmetic or physical flight')
    (OUT/'results.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
    assert all(not any(s['failures'].values()) for s in summaries), 'Retained failure data: inspect results.json'


if __name__ == '__main__':
    main()
