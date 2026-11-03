#!/usr/bin/env python3
"""Analytic phase-plane figure; not a trajectory experiment."""
import argparse
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    # Braking facets change at rate increments h*b=.08; draw their knots.
    omega=np.linspace(-2,2,51);n=np.arange(26)
    plt.rcParams['svg.fonttype']='none'
    # Exact finite-facet description evaluated in float64 only for plotting.
    stop=lambda s:np.max(.02*s[:,None]*n-.0008*n*(n-1),axis=1)
    lower=-.45+stop(np.maximum(-omega,0));upper=.45-stop(np.maximum(omega,0))
    fig,(ax,bx)=plt.subplots(1,2,figsize=(10,4),layout='constrained')
    ax.fill_betweenx(omega,lower,upper,color='#99c5bc',alpha=.8,label='Full-state braking kernel')
    ax.add_patch(Rectangle((-.45,-2),.9,4,fill=False,edgecolor='#555555',linestyle='--',label='Original angular domain'))
    ax.scatter([0],[2],color='#b84937',s=35,zorder=4,label='Unrecoverable: (0, 2)')
    ax.add_patch(Rectangle((-.0225,-.12),.045,.24,fill=False,edgecolor='#244b78',lw=2))
    ax.set(xlabel='Angle (rad)',ylabel='Angular rate (rad/s)',title='Braking couples angle and angular rate',xlim=(-.5,.5),ylim=(-2.2,2.2))
    ax.legend(loc='lower left',fontsize=7)
    bx.add_patch(Rectangle((-.0225,-.12),.045,.24,facecolor='#e1eaf3',edgecolor='#244b78',lw=2,label='Outer box of proven invariant set'))
    bx.add_patch(Rectangle((-.005,-.01),.01,.02,facecolor='#244b78',alpha=.8,label='Initial set'))
    bx.set(xlabel='Angle (rad)',ylabel='Angular rate (rad/s)',title='Fixed zero-reference output feedback',xlim=(-.03,.03),ylim=(-.16,.16))
    bx.legend(loc='upper center',fontsize=7)
    for q in (ax,bx):q.grid(alpha=.2);q.axhline(0,color='grey',lw=.5);q.axvline(0,color='grey',lw=.5)
    fig.suptitle('Attitude subsystem only: exact Euler-model analysis',fontsize=13)
    fig.supxlabel('The outer box is a constraint bound; it is not itself an invariant set.',fontsize=9)
    a.output.parent.mkdir(parents=True,exist_ok=True);fig.savefig(a.output)
if __name__=='__main__':main()
