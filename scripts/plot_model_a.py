#!/usr/bin/env python3
"""Plot actual model-A pilot artifacts; fixed first pilot seed and S2."""
import argparse,csv,gzip,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]


def main():
    p=argparse.ArgumentParser();p.add_argument('training',type=Path);p.add_argument('replay',type=Path);args=p.parse_args()
    h=json.loads((args.training/'history.json').read_text());s=json.loads((args.training/'training_summary.json').read_text())
    with gzip.open(args.replay/'steps.csv.gz','rt') as f:rows=list(csv.DictReader(f))
    with gzip.open(ROOT/'results/nonlinear_zonotope_20260909/steps.csv.gz','rt') as f:old=list(csv.DictReader(f))
    plt.rcParams.update({'svg.hashsalt':'model-a-20260909','font.size':9})
    fig,ax=plt.subplots(1,3,figsize=(12,4),layout='constrained')
    for key,label in [('train_sum_squared_error_mean','Train'),('validation_sum_squared_error_mean','Validation')]:
        ax[0].plot([x['iteration'] for x in h],[x[key] for x in h],label=label)
    ax[0].axvline(s['selected_iteration'],color='gray',linestyle='--');ax[0].set(xlabel='L-BFGS iteration',ylabel='Mean squared vector error',title='Point-loss training',yscale='log')
    ax[1].bar([-.17,.83],[1.879898044,2.085497555],width=.34,label='Physics-only bound')
    ax[1].bar([.17,1.17],s['global_partition_halfwidth'],width=.34,label='Model A partition bound')
    ax[1].set(xticks=[0,1],xticklabels=['Horizontal','Vertical'],ylabel='Acceleration bound (m/s²)',title='Whole-domain residual envelope')
    for source,label in [(old,'Physics-only zonotope'),(rows,'Model A zonotope')]:
        r=[x for x in source if x['seed']=='70001' and x['scenario']=='S2' and x['vz_radius'] and float(x['time_s'])<=1 and ('budget' not in x or x['budget']=='60')]
        ax[2].plot([float(x['time_s']) for x in r],[float(x['vz_radius']) for x in r],label=label)
    ax[2].axvline(.26,color='firebrick',linestyle='--');ax[2].set(xlabel='Time (s)',ylabel='Vertical velocity half-width (m/s)',title='Same pilot input and measurements')
    for a in ax:a.grid(axis='y',alpha=.2);a.legend(fontsize=7)
    fig.suptitle('Single-seed model A: lower prediction error does not ensure usable sets')
    fig.savefig(args.training/'findings.svg',metadata={'Date':None});plt.close(fig)


if __name__=='__main__':main()
