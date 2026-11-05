"""Run independent stages; each successful stage is saved before continuing.

Usage: .venv/Scripts/python.exe -m experiments.oit_mrpi_verify --stage all
Existing stage outputs require --replace-stage, preventing accidental repeats.
"""
import argparse
import csv
import hashlib
import json
import platform
from pathlib import Path
import time
import numpy as np
import scipy
import osqp
from src.oit_mrpi.control import TubeMPC
from experiments.oit_mrpi_theory import run_theory
from experiments.oit_mrpi_benchmarks import static_benchmarks, estimator_benchmarks
from experiments.oit_mrpi_closedloop import (matched_information, feasible_grid, adaptive_runs,
                                           monte_carlo_fast_branch)

OUT=Path('experiments/results/oit_mrpi_20261105')


def clean(x):
    if isinstance(x,np.ndarray): return clean(x.tolist())
    if isinstance(x,(np.integer,)): return int(x)
    if isinstance(x,(np.bool_,)): return bool(x)
    if isinstance(x,(float,np.floating)): return float(x) if np.isfinite(x) else None
    if isinstance(x,dict): return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [clean(v) for v in x]
    return x


def write_csv(path,rows):
    if not rows: return
    fields=list(dict.fromkeys(k for r in rows for k in r))
    with path.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(clean(rows))


def save(path,data):
    path.write_text(json.dumps(clean(data),ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')


def hashes():
    files=list(Path('src/oit_mrpi').glob('*.py'))+list(Path('experiments').glob('oit_mrpi*.py'))
    files += [Path('tests/test_oit_mrpi.py'),Path('docs/research/proposal/OIT_MRPI_VALIDATION_PLAN.md')]
    return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--stage',default='all',
        choices=['all','theory','static','estimator','matched','feasible','closedloop','montecarlo'])
    parser.add_argument('--replace-stage',action='store_true');args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    stages=['theory','static','estimator','matched','feasible','closedloop','montecarlo'] if args.stage=='all' else [args.stage]
    ctrl=None
    for stage in stages:
        target=OUT/(stage+'.json')
        if target.exists() and not args.replace_stage:
            print('SKIP completed stage',stage,flush=True);continue
        if stage in ('matched','feasible','closedloop','montecarlo') and ctrl is None:
            ctrl=TubeMPC()
            save(OUT/'controller.json',dict(K=ctrl.K,L=ctrl.L,F_joint=ctrl.joint.F,D_joint=ctrl.joint.D,
                static_margins=ctrl.static,S=ctrl.joint.S.record(),tail=ctrl.joint.tail,
                terminal_H=ctrl.terminal.H,terminal_h=ctrl.terminal.h,P=ctrl.P,
                terminal_depth=ctrl.terminal_depth,horizon=ctrl.N,window=ctrl.window))
        tic=time.perf_counter();source_before=hashes()
        print('START',stage,flush=True)
        if stage=='theory': result=run_theory(OUT,write_csv)
        elif stage=='static': result=static_benchmarks(OUT,write_csv)
        elif stage=='estimator': result=estimator_benchmarks(OUT,write_csv)
        elif stage=='matched': result=matched_information(ctrl,OUT,write_csv)
        elif stage=='feasible': result={'rows':feasible_grid(ctrl,OUT,write_csv)}
        elif stage=='closedloop': result=adaptive_runs(ctrl,OUT,write_csv)
        else: result=monte_carlo_fast_branch(ctrl,OUT)
        result.update(wall_seconds=time.perf_counter()-tic,source_hashes_at_run=source_before,
            environment=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,
                             osqp=osqp.__version__,platform=platform.platform()),
            arithmetic='float64 LP/QP with residual checks; analytical proofs separate; not outward-rounded formal verification')
        save(target,result);print('DONE',stage,result['wall_seconds'],flush=True)
    save(OUT/'manifest.json',dict(date='2026-11-05',source_hashes=hashes(),
        data_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in OUT.iterdir()
                     if p.is_file() and p.name!='manifest.json'}))


if __name__=='__main__': main()
