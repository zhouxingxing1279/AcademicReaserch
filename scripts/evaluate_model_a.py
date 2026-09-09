#!/usr/bin/env python3
"""Causal model-A replay; retained baseline logs use exactly the same sources."""
import argparse,csv,gzip,hashlib,io,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
import numpy as np
from smf_mpc import plant
from smf_mpc.neural_model import ResidualMLP
from smf_mpc.learned_filter import LearnedZonotopeSMF
from smf_mpc.zonotope_filter import contains,NumericalFailure
from smf_mpc.filter import OutOfDomain
from smf_mpc.sets import EmptySet
from smf_mpc.sensing import PacketSchedule
from run_zonotope import source_data
from run_g1 import drop_for,save_json


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('training',type=Path);parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    if args.output.exists() and any(args.output.iterdir()):parser.error('use an empty output directory')
    args.output.mkdir(parents=True,exist_ok=True)
    model=ResidualMLP.from_dict(json.loads((args.training/'model.json').read_text()));cert=json.loads((args.training/'envelope.json').read_text())
    config=json.loads((ROOT/'configs/planar_baseline.json').read_text());baseline=json.loads((ROOT/'results/nonlinear_zonotope_20260909/summary.json').read_text())['runs']
    prior_hash={(r['seed'],r['scenario']):r['source_trajectory_sha256'] for r in baseline}
    rows=[];summaries=[]
    for seed in (70001,70002,70003):
        prior,truth,inputs,potential,digest=source_data(config,seed)
        for scenario in ('S0','S1','S2'):
            if prior_hash[seed,scenario]!=digest:raise RuntimeError('baseline source hash mismatch')
            schedule=PacketSchedule();idx=schedule.step(0)
            f=LearnedZonotopeSMF(prior,plant.observe(truth[0],0,idx,potential[0],config),config,model,cert,60)
            status='COMPLETED';detail=None;stop=1000;failures=0;latencies=[];max_neural=np.zeros(2);max_radius=np.zeros(6)
            for k in range(1001):
                if k:
                    idx=schedule.step(k,drop_for(k,5,scenario));obs=plant.observe(truth[k],k,idx,potential[k],config)
                    start=time.perf_counter_ns()
                    try:f.advance(inputs[k-1],obs)
                    except (OutOfDomain,EmptySet,NumericalFailure) as exc:
                        status=type(exc).__name__;detail=str(exc);stop=k;latencies.append((time.perf_counter_ns()-start)/1e6)
                        rows.append({'seed':seed,'scenario':scenario,'tick':k,'time_s':k*.02,'status':status,'lp_member':'','vx_radius':'','vz_radius':''});break
                    latencies.append((time.perf_counter_ns()-start)/1e6)
                    max_neural=np.maximum(max_neural,f.diagnostics['neural_remainder_radius'])
                try:member=contains(f.zonotope,truth[k])
                except NumericalFailure as exc:status='NumericalFailure';detail=str(exc);member=None
                max_radius=np.maximum(max_radius,f.box.radius)
                rows.append({'seed':seed,'scenario':scenario,'tick':k,'time_s':k*.02,'status':status if member is None else 'VALID_NUMERICAL_SET',
                             'lp_member':'' if member is None else int(member),'vx_radius':f.box.radius[2],'vz_radius':f.box.radius[3]})
                if member is None:stop=k;break
                if not member:status='MEMBERSHIP_FAILURE';failures+=1;stop=k;break
            summaries.append({'seed':seed,'scenario':scenario,'budget':60,'status':status,'stop_tick':stop,'stop_time_s':stop*.02,
                              'failure_detail':detail,'lp_membership_failures':failures,'source_trajectory_sha256':digest,'matches_baseline_source':True,
                              'max_posterior_radius_on_valid_prefix':max_radius.tolist(),'max_neural_discrete_remainder_on_valid_prefix':max_neural.tolist(),
                              'filter_timing_ms':dict(zip(('p50','p95','p99','max'),np.percentile(latencies,[50,95,99,100]).tolist())),
                              'over_20ms':sum(t>20 for t in latencies),'baseline_completed_20s':True})
            print(json.dumps({k:summaries[-1][k] for k in ('seed','scenario','status','stop_time_s')}),flush=True)
    buffer=io.StringIO(newline='');writer=csv.DictWriter(buffer,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (args.output/'steps.csv.gz').write_bytes(gzip.compress(buffer.getvalue().encode(),mtime=0))
    save_json(args.output/'summary.json',{'scope':'single-model A pilot, no C/D conclusion, no real-time guarantee','model_sha256':model.digest(),'runs':summaries})
    sources=[*sorted((ROOT/'src').rglob('*.py')),Path(__file__).resolve(),ROOT/'scripts/run_zonotope.py',ROOT/'scripts/run_g1.py']
    save_json(args.output/'manifest.json',{'source_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},
        'artifact_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(args.output.iterdir()) if p.is_file()},
        'model_file_sha256':hashlib.sha256((args.training/'model.json').read_bytes()).hexdigest(),
        'envelope_file_sha256':hashlib.sha256((args.training/'envelope.json').read_bytes()).hexdigest()})
    if any(r['lp_membership_failures'] or r['status'] in ('NumericalFailure','EmptySet') for r in summaries):raise SystemExit(1)


if __name__=='__main__':main()
