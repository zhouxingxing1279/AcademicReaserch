#!/usr/bin/env python3
"""Recreate the figure from saved CSV data. Optional matplotlib dependency."""
import argparse
import csv
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('results',type=Path)
    args=p.parse_args()
    with (args.results/'planar_steps.csv').open() as f:planar=list(csv.DictReader(f))
    with (args.results/'linear_steps.csv').open() as f:linear=list(csv.DictReader(f))
    plt.rcParams.update({'svg.hashsalt':'g1-20260909','font.size':10})
    fig,axes=plt.subplots(1,2,figsize=(11,4),layout='constrained')
    # Predeclared first pilot seed, S2; not selected for visual performance.
    rows=[r for r in planar if r['seed']=='70001' and r['scenario']=='S2' and r['lower_3']]
    t=[float(r['time_s']) for r in rows]
    axes[0].fill_between(t,[float(r['lower_3']) for r in rows],[float(r['upper_3']) for r in rows],alpha=.25,label='Box envelope')
    axes[0].plot(t,[float(r['truth_3']) for r in rows],color='black',label='Truth')
    axes[0].axvline(1.36,color='firebrick',linestyle='--',label='Domain stop at 1.36 s')
    axes[0].set(xlabel='Time (s)',ylabel='Vertical velocity (m/s)',title='Planar pilot: envelope growth')
    rows=[r for r in linear if r['scenario']=='S2']
    t=[float(r['time_s']) for r in rows]
    axes[1].plot(t,[float(r['box_velocity_radius']) for r in rows],label='Box')
    axes[1].plot(t,[float(r['zonotope_velocity_hull_radius']) for r in rows],label='Zonotope hull')
    axes[1].set(xlabel='Time (s)',ylabel='Velocity half-width (m/s)',title='Linear diagnostic: same bounded disturbances')
    for ax in axes:ax.grid(alpha=.2);ax.legend(loc='upper left')
    fig.suptitle('G1 numerical pilots only — no neural training or MPC')
    fig.savefig(args.results/'g1_findings.svg',metadata={'Date':None})
    plt.close(fig)


if __name__=='__main__':main()
