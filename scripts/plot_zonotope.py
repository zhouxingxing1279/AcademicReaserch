#!/usr/bin/env python3
"""Plot recorded numerical pilots; fixed seed 70001, S2, no trajectory selection."""
import argparse,csv,gzip,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('results',type=Path);args=p.parse_args()
    with gzip.open(args.results/'steps.csv.gz','rt',newline='') as f:rows=list(csv.DictReader(f))
    with (ROOT/'results/g1_20260909/planar_steps.csv').open() as f:old=list(csv.DictReader(f))
    plt.rcParams.update({'svg.hashsalt':'nonlinear-zono-20260909','font.size':10})
    fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained')
    for budget in (30,60,120):
        a=[r for r in rows if r['seed']=='70001' and r['scenario']=='S2' and r['budget']==str(budget) and r['vz_radius']]
        axes[0].plot([float(r['time_s']) for r in a],[float(r['vz_radius']) for r in a],label=f'Zonotope p={budget}',alpha=.85)
    a=[r for r in old if r['seed']=='70001' and r['scenario']=='S2' and r['lower_3']]
    axes[0].plot([float(r['time_s']) for r in a],[(float(r['upper_3'])-float(r['lower_3']))/2 for r in a],label='G1 box (stops at 1.36 s)',color='black',linestyle='--')
    axes[0].set(xlabel='Time (s)',ylabel='Vertical velocity half-width (m/s)',title='Same source trajectory and observations')
    s=json.loads((args.results/'summary.json').read_text())['runs']
    budgets=sorted({r['budget'] for r in s})
    axes[1].bar([str(b) for b in budgets],[max(r['max_reduction_mixed_width_increase'] for r in s if r['budget']==b) for b in budgets],color='#4878a8')
    axes[1].set(xlabel='Generator budget',ylabel='Max normalized directional width increase',title='Immediate reduction loss: 30 mixed directions')
    axes[0].legend(fontsize=8)
    for ax in axes:ax.grid(axis='y',alpha=.2)
    fig.suptitle('Nonlinear zonotope numerical pilots — no neural model or MPC')
    fig.savefig(args.results/'findings.svg',metadata={'Date':None})
    plt.close(fig)


if __name__=='__main__':main()
