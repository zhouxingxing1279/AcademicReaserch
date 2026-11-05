"""Independent saved-result audit; does not rerun the experiment suite."""
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import numpy as np
from experiments.oit_mrpi_verify import clean,save,OUT
from experiments.oit_mrpi_closedloop import reconstruct_mc_sets
from src.oit_mrpi.control import TubeMPC


def exact_reduction_witness(record):
    F=np.array([[Q(v) for v in row] for row in record['rational_F']],dtype=object)
    D=np.array([[Q(v) for v in row] for row in record['rational_D']],dtype=object)
    I=np.array([[Q(1),Q(0)],[Q(0),Q(1)]],dtype=object)
    P=np.array([[Q(1),Q(1)],[Q(1),Q(-1)]],dtype=object)
    def rad(G): return np.array([sum(abs(x) for x in row) for row in G],dtype=object)
    def reduce(G):
        use_axis=rad(G)[0]<=Q(7,10)
        base,inverse=(I,I) if use_axis else (P,P/Q(2))
        return base@np.diag(rad(inverse@G))
    seq=np.zeros((2,1),dtype=object);term=D.copy();terms=[]
    for k in range(record['N']):
        seq=reduce(np.column_stack([F@seq,D]))
        terms.append(term);term=F@term
    batch=reduce(np.column_stack(terms))
    q=np.array([Q(1,2),Q(1,2)],dtype=object)
    gap=sum(abs(x) for x in q@batch)-sum(abs(x) for x in q@seq)
    assert gap==Q(247,2500)
    # F^2=(14/25)I, hence exact Schur stability without a numeric eigensolver.
    assert np.all(F@F==Q(14,25)*I)
    return dict(exact_gap=str(gap),exact_schur_witness='F^2=(14/25)I',
                batch_generators=[[str(x) for x in row] for row in batch],
                sequential_generators=[[str(x) for x in row] for row in seq],
                direction=['1/2','1/2'],exact_arithmetic=True)


def main():
    load=lambda name:json.loads((OUT/(name+'.json')).read_text(encoding='utf-8'))
    theory,static,est,matched,feasible,closed,mc=[load(n) for n in
        ('theory','static','estimator','matched','feasible','closedloop','montecarlo')]
    numerical_files={str(p) for p in Path('src/oit_mrpi').glob('*.py')}
    numerical_files|={str(Path('experiments')/f) for f in
        ('oit_mrpi_theory.py','oit_mrpi_benchmarks.py','oit_mrpi_closedloop.py','oit_mrpi_verify.py')}
    source_checks=[]
    for name,d in zip(('theory','static','estimator','matched','feasible','closedloop','montecarlo'),
                      (theory,static,est,matched,feasible,closed,mc)):
        mismatch=[p for p,h in d['source_hashes_at_run'].items()
                  if p in numerical_files and hashlib.sha256(Path(p).read_bytes()).hexdigest()!=h]
        source_checks.append(dict(stage=name,mismatches=mismatch))
    assert all(not r['mismatches'] for r in source_checks),source_checks
    exact=exact_reduction_witness(theory['A']['nonmonotone_counterexample'])
    assert not closed['failures']
    assert mc['constraint_failures']==0 and mc['trajectories']==10000
    assert all(r['sample_contained'] for r in closed['rows'])
    assert max(r['descent'] for r in closed['rows'])<2e-6
    certified=[r for r in static['rows'] if r.get('certified_RPI')]
    assert all(r['sampled_RPI_violation']<2e-7 for r in certified)

    # Inspect actual Monte Carlo arrays independently of loop summary fields.
    a=np.load(OUT/'monte_carlo_10000.npz')
    direct_violation=max(np.max(abs(a['x_true'])-np.array([5.,3.])),np.max(abs(a['u'])-1))
    assert direct_violation<=2e-7
    assert np.max(abs(a['disturbances_and_sensor_noise_unit']))<=1
    ctrl=TubeMPC()
    reconstruction=[]
    for trajectory in (0,1,37,128,9999):
        for k in (0,1,15,30):
            X,tube=reconstruct_mc_sets(OUT/'monte_carlo_10000.npz',trajectory,k,ctrl)
            ok=X.point_contains(a['x_true'][trajectory,k])
            assert ok
            reconstruction.append(dict(trajectory=trajectory,k=k,true_state_contained=ok))
    costs={}
    for comparison in ('fixed','known_d_only'):
        delta=[]
        for seed in range(12):
            ref=next(r for r in closed['summaries'] if r['seed']==seed and r['method']==comparison)
            act=next(r for r in closed['summaries'] if r['seed']==seed and r['method']=='adaptive')
            delta.append(1-act['cost']/ref['cost'])
        costs[comparison]=dict(paired_reductions=delta,median=float(np.median(delta)),
                               minimum=float(min(delta)),maximum=float(max(delta)))
    timings={}
    for m in ('fixed_RPI','known_d_only','OIT_CZ_compatible'):
        rr=[r for r in closed['rows'] if r['method']==m]
        timings[m]=dict(median_ms=float(np.median([r['runtime_total']*1000 for r in rr])),
                        p95_ms=float(np.quantile([r['runtime_total']*1000 for r in rr],.95)),
                        max_ms=float(max(r['runtime_total']*1000 for r in rr)),
                        fraction_le20ms=float(np.mean([r['runtime_total']<=.020 for r in rr])),
                        fraction_le50ms=float(np.mean([r['runtime_total']<=.050 for r in rr])),
                        QP_solves=sum(r['solver']=='solved' for r in rr),steps=len(rr))
    counts={m:sum(r['feasible'] for r in feasible['rows'] if r['method']==m)
            for m in {r['method'] for r in feasible['rows']}}
    supports={}
    full_width_supports={}
    for label in ('position','velocity','input'):
        filt=lambda method:[r for r in matched['rows'] if r['method']==method and r['window']==3
                            and r['horizon']==1 and r['direction']==label]
        cz=filt('OIT_CZ')
        supports[label]={m:float(np.median([1-x['halfwidth']/y['halfwidth'] for x,y in zip(cz,filt(m))]))
                         for m in ('fixed_RPI','known_d_slice','ordinary_zonotope')}
        qi={'position':0,'velocity':1,'input':4}[label]
        common_noise=float(np.abs(ctrl.Qdir[qi]@ctrl.joint.D).sum())
        full_width_supports[label]={m:float(np.median([
            1-(x['halfwidth']+common_noise)/(y['halfwidth']+common_noise)
            for x,y in zip(cz,filt(m))]))
            for m in ('fixed_RPI','known_d_slice','ordinary_zonotope')}
    system_audit=[]
    for system in static['systems']:
        A,B,C,K=[np.array(system[k]) for k in ('A','B','C','K')]
        O=np.vstack([C@np.linalg.matrix_power(A,k) for k in range(len(A))])
        system_audit.append(dict(system_id=system['system_id'],
            closedloop_radius=float(max(abs(np.linalg.eigvals(A+B@K)))),
            observability_rank=int(np.linalg.matrix_rank(O)),n=len(A),
            observability_min_singular_value=float(min(np.linalg.svd(O,compute_uv=False)))))
    learning=theory['C']
    paper={m:sum(r['status']=='ok' and r['contained'] is False for r in est['rows'] if r['method']==m)
           for m in {r['method'] for r in est['rows']}}
    result=dict(source_checks=source_checks,exact_reduction_counterexample=exact,
        direct_MC_max_constraint_violation=float(direct_violation),MC_reconstructed_sets=reconstruction,
        cost_comparisons=costs,closedloop_timings=timings,feasible_grid_counts=counts,
        feasible_grid_points_per_method=31*25,support_width_improvements=supports,
        full_one_step_width_improvements=full_width_supports,generated_system_checks=system_audit,
        static_certified_cases=len(certified),
        static_tight_2d4d=[r for r in static['rows'] if r['n'] in (2,4) and
                          r['method'] in ('rakovic_scaled','CZ_batch_plus_certified_tail')],
        paper_noncontainment_counts=paper,
        execution_notes=['Initial Monte Carlo shortcut implementation stopped on 140 fixed-envelope-ineligible initial plans.',
                         'It was corrected to evaluate the actual adaptive branch without altering any initial state or noise seed.',
                         'All 140 actual adaptive checks still admitted the unconstrained optimum; no MC QP solves occurred.',
                         'Final suite rerun once after adding known-d control and homothetic CZ synthesis to lock numerical source hashes.',
                         'No numerical data were filtered by performance; all coarse accuracy failures retained.'])
    save(OUT/'audit.json',result)
    print(json.dumps(clean({k:result[k] for k in ('feasible_grid_counts','cost_comparisons','closedloop_timings',
                                                  'support_width_improvements','static_certified_cases')}),indent=2))
    save(OUT/'manifest.json',dict(date='2026-11-05',
         source_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in
                       list(Path('src/oit_mrpi').glob('*.py'))+list(Path('experiments').glob('oit_mrpi*.py'))+
                       [Path('tests/test_oit_mrpi.py')]},
         data_hashes={str(p.relative_to(OUT)):hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in OUT.rglob('*') if p.is_file() and p.name!='manifest.json'}))


if __name__=='__main__':main()
