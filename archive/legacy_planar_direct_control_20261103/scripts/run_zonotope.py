#!/usr/bin/env python3
"""Paired nonlinear-zonotope pilot against the exact G1 source trajectories."""
import argparse,csv,gzip,hashlib,io,json,os,platform,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import numpy as np
import scipy
from smf_mpc import plant
from smf_mpc.data import rng_for
from smf_mpc.sets import Box,EmptySet
from smf_mpc.filter import OutOfDomain
from smf_mpc.sensing import PacketSchedule
from smf_mpc.zonotope_filter import ZonotopeSMF,NumericalFailure,contains
from run_g1 import drop_for,save_json,csv_write


def source_data(config,seed):
    p=config['plant'];h=p['dt_s'];steps=round(config['evaluation']['episode_seconds']/h)
    prior=Box.from_center(config['initial_set']['center'],config['initial_set']['halfwidth'])
    x=rng_for(seed,'initial').uniform(prior.lower,prior.upper);x[2:4]*=.4;x[4:6]=0
    truth=[x.copy()];inputs=[]
    process=rng_for(seed,'process').uniform(-1,1,(steps,6))*p['external_process_halfwidth']
    for k in range(steps):
        u=np.array([p['mass_kg']*p['gravity_m_s2']*(1+.01*np.cos(k*h)),0.])
        x=plant.step(x,u,[0,0],config,process[k]);inputs.append(u);truth.append(x.copy())
    truth,inputs=np.array(truth),np.array(inputs)
    potential=rng_for(seed,'measurement').uniform(-1,1,(steps+1,6))
    digest=hashlib.sha256(truth.astype('<f8').tobytes()+inputs.astype('<f8').tobytes()+potential.astype('<f8').tobytes()).hexdigest()
    return prior,truth,inputs,potential,digest


def replay(config,seed,scenario,budget,expected_hash):
    prior,truth,inputs,potential,digest=source_data(config,seed)
    if digest!=expected_hash:raise RuntimeError('G1 source trajectory hash mismatch')
    schedule=PacketSchedule();indices=schedule.step(0)
    f=ZonotopeSMF(prior,plant.observe(truth[0],0,indices,potential[0],config),config,budget)
    h=config['plant']['dt_s'];steps=len(inputs);rows=[];latencies=[];member_failures=0
    exact_hull_failures=0;status='COMPLETED';stop=steps;failure_detail=None
    maxima={k:np.zeros(6) for k in ('model_radius','remainder_radius','linear_radius','measurement_radius')}
    width_max=np.zeros(6)
    reduction_max=0.0
    for k in range(steps+1):
        if k:
            indices=schedule.step(k,drop_for(k,5,scenario))
            obs=plant.observe(truth[k],k,indices,potential[k],config)
            start=time.perf_counter_ns()
            try:f.advance(inputs[k-1],obs)
            except (OutOfDomain,EmptySet,NumericalFailure) as exc:
                status=type(exc).__name__;stop=k;failure_detail=str(exc)
                latencies.append((time.perf_counter_ns()-start)/1e6)
                rows.append({'seed':seed,'scenario':scenario,'budget':budget,'tick':k,'time_s':k*h,
                    'status':status,'lp_member':'','vx_radius':'','vz_radius':'','px_radius':'','pz_radius':''})
                break
            latencies.append((time.perf_counter_ns()-start)/1e6)
            reduction_max=max(reduction_max,f.diagnostics['reduction_mixed_width_increase'])
            for key in maxima:maxima[key]=np.maximum(maxima[key],f.diagnostics[key])
        try:member=contains(f.zonotope,truth[k])
        except NumericalFailure as exc:
            member=None;status='NumericalFailure';stop=k;failure_detail=str(exc)
        exact_hull_failures+=not f.box.contains(truth[k])
        member_failures+=member is False
        width_max=np.maximum(width_max,f.box.radius)
        rows.append({'seed':seed,'scenario':scenario,'budget':budget,'tick':k,'time_s':k*h,
                     'status':('NumericalFailure' if member is None else 'VALID_NUMERICAL_ZONOTOPE'),'lp_member':('' if member is None else int(member)),
                     'vx_radius':float(f.box.radius[2]),'vz_radius':float(f.box.radius[3]),
                     'px_radius':float(f.box.radius[0]),'pz_radius':float(f.box.radius[1])})
        if member is None:break
        if not member:status='MEMBERSHIP_FAILURE';stop=k;break
    summary={'seed':seed,'scenario':scenario,'budget':budget,'status':status,'stop_tick':stop,'stop_time_s':stop*h,
             'source_trajectory_sha256':digest,'matches_g1_source':True,'failure_detail':failure_detail,
             'lp_membership_failures':member_failures,'exact_hull_membership_failures':int(exact_hull_failures),
             'max_reduction_mixed_width_increase':reduction_max,'max_posterior_radius':width_max.tolist(),'final_valid_radius':f.box.radius.tolist(),
             'component_maxima':{k:v.tolist() for k,v in maxima.items()},
             'filter_timing_ms':dict(zip(('p50','p95','p99','max'),np.percentile(latencies,[50,95,99,100]).tolist())),
             'filter_calls':len(latencies),'over_20ms':sum(t>20 for t in latencies),
             'timing_scope':'filter advance incl strip consistency LP; excludes truth, membership evaluation, logging and MPC; no warmup excluded'}
    return rows,summary


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--budgets',type=int,nargs='+',default=[30,60,120]);args=p.parse_args()
    if any(b<6 for b in args.budgets):p.error('generator budget must be >=6')
    if args.output.exists() and any(args.output.iterdir()):p.error('use an empty output directory')
    args.output.mkdir(parents=True,exist_ok=True)
    config=json.loads((ROOT/'configs/planar_baseline.json').read_text())
    old=json.loads((ROOT/'results/g1_20260909/summary.json').read_text())
    hashes={(r['seed'],r['scenario']):r['source_trajectory_sha256'] for r in old['planar']}
    rows=[];summaries=[]
    for budget in args.budgets:
        for seed in (70001,70002,70003):
            for scenario in ('S0','S1','S2'):
                a,b=replay(config,seed,scenario,budget,hashes[seed,scenario]);rows+=a;summaries.append(b)
                print(json.dumps({k:b[k] for k in ('seed','scenario','budget','status','stop_time_s')}),flush=True)
    buffer=io.StringIO(newline='')
    writer=csv.DictWriter(buffer,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (args.output/'steps.csv.gz').write_bytes(gzip.compress(buffer.getvalue().encode('utf-8'),mtime=0))
    save_json(args.output/'summary.json',{'kind':'nonlinear_zonotope_pilot_no_learning_or_mpc',
        'arithmetic':'FLOAT64_ENGINEERING_MARGIN_NOT_CERTIFIED','runs':summaries})
    sources=[*sorted((ROOT/'src').rglob('*.py')),Path(__file__).resolve(),ROOT/'scripts/run_g1.py']
    save_json(args.output/'manifest.json',{'base_commit':'53b442108038270d95de6158016b3c4458716f5c',
        'config_sha256':hashlib.sha256((ROOT/'configs/planar_baseline.json').read_bytes()).hexdigest(),
        'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
        'machine':platform.machine(),'cpu_count':os.cpu_count(),
        'thread_environment':{k:os.environ.get(k) for k in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS')},
        'source_sha256':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sources},
        'artifact_sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(args.output.iterdir()) if f.is_file()}})
    if any(r['lp_membership_failures'] or r['status'] in ('EmptySet','NumericalFailure') for r in summaries):raise SystemExit(1)


if __name__=='__main__':main()
