"""Render auditable figures only from saved experiment data."""
import csv
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    p = Path('experiments/results/finite_memory_tube')
    result = json.loads((p/'results.json').read_text())
    with (p/'trajectories.csv').open() as f:
        rows = list(csv.DictReader(f))
    with (p/'matched_information.csv').open() as f:
        matched = list(csv.DictReader(f))
    plt.rcParams.update({'font.size': 10, 'axes.spines.top': False, 'axes.spines.right': False,
                         'svg.fonttype': 'none'})
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 7.7), constrained_layout=True)
    color, other = '#126b81', '#c96a35'
    rr = [r for r in rows if r['case'] == 'max_gap' and r['mode'] == 'cz' and r['axis'] == '0']
    tt = np.array([float(r['k']) for r in rr])*.5
    z = np.array([float(r['p_nominal']) for r in rr])
    axes[0, 0].fill_between(tt, z-.1525, z+.1525, color=color, alpha=.15, label='Analytic tube projection')
    axes[0, 0].plot(tt, [float(r['p']) for r in rr], color=color, label='Actual mathematical plant')
    axes[0, 0].plot(tt, z, '--', color=other, label='Nominal')
    axes[0, 0].set(xlabel='Time (s)', ylabel='Position (m)', title='A  Maximum legal gap, endpoint noise')
    axes[0, 0].legend(fontsize=8)
    cc = [r for r in matched if r['case'] == 'fresh' and r['mode'] == 'cz']
    axes[0, 1].plot([int(r['k']) for r in cc], [int(r['full_generators']) for r in cc], color=other, label='Full-history CZ')
    axes[0, 1].plot([int(r['k']) for r in cc], [int(r['cz_generators']) for r in cc], color=color, label='Finite-memory CZ')
    axes[0, 1].axhline(9, color=color, linestyle=':', alpha=.6, label='Bound 2Q+1 = 9')
    axes[0, 1].set(xlabel='Reception step', ylabel='Generators per axis', title='B  Representation growth')
    axes[0, 1].legend(fontsize=8)
    names, ratios = ['fresh', 'max_gap', 'random', 'reorder'], []
    for name in names:
        cc = [r for r in matched if r['case'] == name and r['mode'] == 'cz']
        ratios.append(np.mean([float(r['cz_v'])/float(r['pair_v']) for r in cc]))
    axes[1, 0].bar(names, ratios, color=[color]*4)
    axes[1, 0].axhline(1, color=other, linestyle='--', linewidth=1)
    for i, ratio in enumerate(ratios):
        axes[1, 0].text(i, ratio+.025, f'{ratio:.3f}', ha='center', fontsize=9)
    axes[1, 0].set(ylim=(0, 1.15), ylabel='Mean velocity width ratio (CZ / pair)',
                   title='C  Matched information; seed 0, first 40 steps')
    grid = np.full((4, 4), np.nan)
    for item in result['delivery_graph_and_budget']:
        if item['status'] == 'nonempty':
            grid[item['M'], item['L']] = item['nominal_input']
    im = axes[1, 1].imshow(grid, vmin=0, vmax=4, cmap='YlGnBu', origin='lower')
    for i in range(4):
        for j in range(4):
            value = grid[i, j]
            axes[1, 1].text(j, i, 'NC' if np.isnan(value) else f'{value:.2f}',
                            ha='center', va='center', fontsize=8,
                            color='white' if value > 2.5 else 'black')
    axes[1, 1].set(xticks=range(4), yticks=range(4), xlabel='Maximum delivery delay L',
                   ylabel='Maximum missed generations M', title='D  Nominal input budget (NC: not certified)')
    fig.colorbar(im, ax=axes[1, 1], shrink=.8, label='Input units')
    fig.suptitle('Finite-memory output-feedback benchmark — mathematical model only', fontsize=14)
    fig.savefig(p/'benchmark.png', dpi=200)
    fig.savefig(p/'benchmark.svg')
    plt.close(fig)


if __name__ == '__main__':
    main()
