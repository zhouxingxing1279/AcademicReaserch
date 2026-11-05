"""Generate eight standalone scientific figures from saved raw results."""
import csv
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

OUT=Path('experiments/results/oit_mrpi_20261105')
FIG=OUT/'figures'
COLORS={'fixed_RPI':'#666666','known_d_slice':'#a9843d','ordinary_zonotope':'#0072b2',
        'OIT_CZ':'#d55e00','OIT_CZ_compatible':'#d55e00','known_d_only':'#a9843d'}


def data(name): return json.loads((OUT/(name+'.json')).read_text(encoding='utf-8'))


def save(fig,name):
    fig.tight_layout();fig.savefig(FIG/(name+'.png'),dpi=180,bbox_inches='tight')
    fig.savefig(FIG/(name+'.svg'),bbox_inches='tight');plt.close(fig)


def main():
    FIG.mkdir(exist_ok=True)
    plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False,
                         'axes.grid':True,'grid.alpha':.2,'figure.facecolor':'white'})
    st=data('static');ma=data('matched');est=data('estimator');fg=data('feasible')
    polygons=np.load(OUT/'set_polygons.npz')
    fig,axs=plt.subplots(1,2,figsize=(11,4))
    for ax,sid,title in zip(axs,['double_integrator_lqr','double_integrator_weak'],['LQR feedback','Weak feedback (rho=0.95)']):
        for method in ['polytope_truncated_reference','rakovic_scaled','zonotope_iterative_RPI',
                       'zonotope_one_step_RPI','CZ_batch_plus_certified_tail']:
            key=sid+'__'+method
            if key in polygons:
                v=polygons[key];v=np.vstack([v,v[0]])
                ax.plot(v[:,0],v[:,1],label=method.replace('_',' '),lw=1.3)
        ax.set_title(title);ax.set_xlabel('Position error');ax.set_ylabel('Velocity error')
    axs[1].legend(fontsize=7,loc='upper left',bbox_to_anchor=(1,1))
    save(fig,'01_mrpi_sets')

    fig,axs=plt.subplots(1,2,figsize=(10,4))
    for ax,label in zip(axs,['position','input']):
        for method in COLORS:
            r=[r for r in ma['rows'] if r['method']==method and r['window']==3 and r['horizon']==1 and r['direction']==label]
            if r: ax.plot([v['k'] for v in r],[v['halfwidth'] for v in r],label=method,color=COLORS[method])
        ax.set_title('One-step '+label+' uncertainty');ax.set_xlabel('Observation step');ax.set_ylabel('Half-width (initial-set contribution)')
    axs[1].legend(fontsize=8)
    save(fig,'02_oit_vs_static')

    fig,ax=plt.subplots(figsize=(7,4))
    for method in sorted({r['method'] for r in st['rows']}):
        r=[r for r in st['rows'] if r['method']==method and r['n']==2 and r.get('status')=='ok']
        if r: ax.scatter([max(v['runtime_set'],1e-6)*1000 for v in r],
                         [max(v['hausdorff_error'],1e-10) for v in r],label=method,s=40)
    ax.set_xscale('log');ax.set_yscale('log');ax.set_xlabel('Set construction time (ms)')
    ax.set_ylabel('2D polygon Hausdorff distance to finite reference')
    ax.legend(fontsize=7,loc='upper left',bbox_to_anchor=(1,1))
    save(fig,'03_error_runtime')

    fig,ax=plt.subplots(figsize=(7,4))
    for method in ['true_prior_full_history','recursive_interval_reduction','OIT_CZ_window_2','OIT_CZ_window_4','OIT_CZ_window_8']:
        r=[r for r in est['rows'] if r['method']==method and r['status']=='ok']
        ax.plot([v['k'] for v in r],[v['g'] for v in r],label=method)
    ax.set_xlabel('Time step');ax.set_ylabel('Generator coefficients');ax.legend(fontsize=8)
    save(fig,'04_generators_time')

    fig,ax=plt.subplots(figsize=(7,4))
    for method in sorted({r['method'] for r in st['rows']}):
        r=[r for r in st['rows'] if r['method']==method and r['n']>=4 and r.get('status')=='ok']
        dims=sorted({v['n'] for v in r})
        ax.plot(dims,[1000*np.median([v['runtime_set'] for v in r if v['n']==n]) for n in dims],'-o',label=method)
    ax.set_yscale('log');ax.set_xlabel('State dimension');ax.set_ylabel('Median set runtime over two rho cases (ms)')
    ax.set_xticks([4,8,16,32]);ax.legend(fontsize=7,loc='upper left',bbox_to_anchor=(1,1))
    save(fig,'05_dimension_runtime')

    fig,axs=plt.subplots(1,2,figsize=(10,4))
    r=est['window_sweep'];axs[0].plot([v['window'] for v in r],[v['outer_support_polygon_area'] for v in r],'-o')
    axs[0].set_xlabel('Window transitions');axs[0].set_ylabel('128-direction outer polygon area')
    axs[0].set_title('Same realized measurement record')
    r=est['poor_observability'];axs[1].loglog([v['gramian_min_eigenvalue'] for v in r],[v['box_area'] for v in r],'-o')
    axs[1].set_xlabel('Minimum observation Gramian eigenvalue');axs[1].set_ylabel('Estimate interval-hull area')
    save(fig,'06_window_volume_observability')

    fig,ax=plt.subplots(figsize=(7,4));r=st['rho_sweep']
    ax.plot([v['rho'] for v in r],[v['horizon'] for v in r],'-o')
    ax.set_xlabel('Closed-loop spectral radius');ax.set_ylabel('Truncation horizon for tail inf-bound <= 1e-5')
    save(fig,'07_rho_horizon')

    fig,axs=plt.subplots(1,2,figsize=(10,4));r=fg['rows']
    methods=['fixed_RPI','known_d_only','ordinary_zonotope','OIT_CZ_compatible']
    counts=[sum(v['feasible'] for v in r if v['method']==m) for m in methods]
    # Point grid quadrature is explicitly not exact feasible-region volume.
    axs[0].bar(range(4),counts,color=[COLORS[m] for m in methods])
    axs[0].set_xticks(range(4),['Fixed','Known d','Zonotope','OIT-CZ'])
    axs[0].set_ylabel('Feasible points in 31 x 25 grid')
    lookup={(v['p'],v['v'],v['method']):v['feasible'] for v in r}
    points=sorted({(v['p'],v['v']) for v in r})
    for category,color in [('both','#666666'),('adaptive_only','#d55e00')]:
        selected=[(p,v) for p,v in points if lookup[(p,v,'OIT_CZ_compatible')] and
                  (lookup[(p,v,'fixed_RPI')] if category=='both' else not lookup[(p,v,'fixed_RPI')])]
        if selected:
            a=np.array(selected);axs[1].scatter(a[:,0],a[:,1],s=13,c=color,label=category)
    axs[1].set_xlabel('Nominal position');axs[1].set_ylabel('Nominal velocity');axs[1].legend(fontsize=8)
    save(fig,'08_feasible_region')
    print('Saved 8 PNG and 8 SVG figures',flush=True)


if __name__=='__main__':main()
