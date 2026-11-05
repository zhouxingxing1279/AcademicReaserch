"""Post-run audit and decision plots; preserves the frozen screen and its outputs.

Run after cong_mpc_screen: python -m experiments.cong_mpc_audit
No experiment parameters are changed and no simulation is rerun here.
"""
from pathlib import Path
import csv
import hashlib
import json
import numpy as np
from scipy.optimize import linprog
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT = Path('experiments/results/cong_mpc_screen')


def read(name):
    with (OUT / name).open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def main():
    summary = json.loads((OUT / 'summary.json').read_text(encoding='utf-8'))
    assert hashlib.sha256(Path('experiments/cong_mpc_screen.py').read_bytes()).hexdigest() == summary['script_sha256']
    for name, digest in summary['csv_sha256'].items():
        assert hashlib.sha256((OUT / name).read_bytes()).hexdigest() == digest, name
    steps, cases, dual = (read(n) for n in ('c_closed_loop_steps.csv', 'c_closed_loop_cases.csv', 'c_dual.csv'))
    audit = {'input_hashes_verified': len(summary['csv_sha256']), 'closed_loop': {}, 'paired_cost': {}, 'dual': {}}
    for method in ('horizon', 'uniform', 'box'):
        rows = [r for r in steps if r['method'] == method]
        runs = [r for r in cases if r['method'] == method]
        audit['closed_loop'][method] = {
            'completed': sum(int(r['steps']) == 30 and not r['failure'] for r in runs),
            'total': len(runs),
            'mean_cost': float(np.mean([float(r['cost']) for r in runs])),
            'max_residuals': {key: max(float(r[key]) for r in rows) for key in ('state_violation', 'input_violation', 'shift_violation')},
            'update_plus_solve_ms_median_p95_max': np.quantile([float(r['estimate_ms']) + float(r['solve_ms']) for r in rows], [.5, .95, 1]).tolist(),
        }
    for method in ('uniform', 'box'):
        paired = []
        for h in cases:
            if h['method'] != 'horizon':
                continue
            b = next(r for r in cases if r['method'] == method and r['period'] == h['period'] and r['seed'] == h['seed'])
            paired.append({'seed': int(h['seed']), 'period': int(h['period']), 'relative_cost_change': float(h['cost']) / float(b['cost']) - 1})
        gains = [r['relative_cost_change'] for r in paired]
        audit['paired_cost'][method] = {'cases': paired, 'min_median_max': np.quantile(gains, [0, .5, 1]).tolist(), 'strictly_lower_count': sum(g < 0 for g in gains)}
    active = {(r['degree'], r['direction']) for r in dual if int(r['budget']) == 0 and float(r['gap']) > 2e-6}
    audit['dual']['positive_initial_gap_cases'] = len(active)
    audit['dual']['total_queries'] = sum(int(r['budget']) == 0 for r in dual)
    for budget in (0, 1, 3, 10, 30):
        rows = [r for r in dual if int(r['budget']) == budget]
        audit['dual'][str(budget)] = {
            'mean_gap': float(np.mean([float(r['gap']) for r in rows])),
            'max_gap': max(float(r['gap']) for r in rows),
            'active_median_gap': float(np.median([float(r['gap']) for r in rows if (r['degree'], r['direction']) in active])),
        }
    # Conditioning counterexample: diamond and its axis box have equal supports
    # in +/- coordinate directions, but conditioning x1+x2=0 loses tightness.
    diamond = np.array([[1, 1], [1, -1], [-1, 1], [-1, -1]])
    box = np.array([[1, 0], [-1, 0], [0, 1], [0, -1]])
    vals = {}
    for name, H in (('diamond', diamond), ('box', box)):
        r = linprog([-1, 0], A_ub=H, b_ub=np.ones(4), A_eq=[[1, 1]], b_eq=[0], bounds=[(None, None)]*2, method='highs')
        assert r.success
        vals[name] = -r.fun
    assert abs(vals['diamond']-.5) < 1e-10 and abs(vals['box']-1) < 1e-10
    audit['conditioning_counterexample_h_e1'] = vals
    audit['scope'] = 'Postprocessing frozen data; conditioning LP is a separate analytic counterexample, not a new closed-loop trial.'
    audit['audit_script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (OUT / 'audit.json').write_text(json.dumps(audit, indent=2), encoding='utf-8')

    fig, axes = plt.subplots(1, 3, figsize=(15, 4.6), layout='constrained')
    names = ['exact', 'horizon', 'uniform', 'box']
    counts = [summary['C']['feasible'][n] for n in names]
    bars = axes[0].bar(names, counts, color=['#404040', '#237a91', '#b58d4c', '#b86d6d'])
    axes[0].bar_label(bars, padding=3)
    axes[0].set(title='Feasible samples (2,700 per method)', ylabel='Count', ylim=(0, 1450))
    axes[0].text(.5, .93, 'horizon / uniform: 42 normals each', transform=axes[0].transAxes, ha='center', fontsize=9)
    for j, method in enumerate(('uniform', 'box')):
        vals = 100*np.array([r['relative_cost_change'] for r in audit['paired_cost'][method]['cases']])
        axes[1].scatter(j + np.linspace(-.1, .1, len(vals)), vals, s=25, alpha=.8, label=method)
        axes[1].plot([j-.2, j+.2], [np.median(vals)]*2, color='black')
    axes[1].axhline(0, color='gray', linestyle='--', linewidth=1)
    axes[1].set(xticks=[0, 1], xticklabels=['vs uniform', 'vs box'], title='Paired closed-loop cost changes', ylabel='100 * (J_horizon / J_baseline - 1) (%)')
    budgets = [0, 1, 3, 10, 30]
    axes[2].semilogy(budgets, [max(1e-16, audit['dual'][str(b)]['max_gap']) for b in budgets], '-o')
    axes[2].set(title='Dual support bound: worst gap', xlabel='Iteration budget', ylabel='Absolute gap (floor 1e-16)')
    axes[2].text(.98, .95, '246 / 504 initially nontrivial\nScalar dual only', transform=axes[2].transAxes, ha='right', va='top', fontsize=9)
    fig.suptitle('Mechanism evidence: modest gains against equal-size baseline', fontsize=13)
    fig.savefig(OUT / 'decision_evidence.png', dpi=180)
    fig.savefig(OUT / 'decision_evidence.pdf')
    print(json.dumps({k: v for k, v in audit.items() if k != 'paired_cost'}, indent=2))


if __name__ == '__main__':
    main()
