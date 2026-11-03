#!/usr/bin/env python3
"""Run G1 validation pilots only; never consumes frozen formal test seeds."""
import argparse
import csv
import hashlib
import json
import platform
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
import numpy as np
import scipy
from scipy.optimize import linprog
from smf_mpc import plant
from smf_mpc.data import rng_for, split_for, windows
from smf_mpc.filter import BoxSMF, OutOfDomain, residual_halfwidth
from smf_mpc.sensing import PacketSchedule
from smf_mpc.sets import Box, Zonotope, EmptySet


def save_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False)+'\n', encoding='utf-8')


def csv_write(path, rows):
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)


def drop_for(tick, period, scenario):
    opportunity = tick//period
    if tick % period or tick == 0:
        return False
    return opportunity % {'S0':1,'S1':2,'S2':3}[scenario] != 0


def planar_replay(config, seed, scenario):
    p, sense = config['plant'], config['sensing']
    h = p['dt_s']; steps = round(config['evaluation']['episode_seconds']/h)
    prior = Box.from_center(config['initial_set']['center'], config['initial_set']['halfwidth'])
    x = rng_for(seed, 'initial').uniform(prior.lower, prior.upper)
    # Deliberately simple fixed-input replay: no hidden state-feedback controller.
    x[2:4] *= .4
    x[4:6] = 0
    all_truth, inputs = [x.copy()], []
    process = rng_for(seed, 'process').uniform(-1,1,(steps,6))*p['external_process_halfwidth']
    for k in range(steps):
        u = np.array([p['mass_kg']*p['gravity_m_s2']*(1+.01*np.cos(k*h)), 0.0])
        x = plant.step(x,u,[0,0],config,process[k])
        inputs.append(u); all_truth.append(x.copy())
    truth, inputs = np.array(all_truth), np.array(inputs)
    potential = rng_for(seed, 'measurement').uniform(-1,1,(steps+1,6))
    schedule = PacketSchedule(sense['position_period_ticks'],sense['max_consecutive_missed_packets'])
    indices = schedule.step(0)
    filt = BoxSMF(prior, plant.observe(truth[0],0,indices,potential[0],config), config)
    rows, members, exact_members = [], [], []
    status, stop_tick = 'COMPLETED', steps
    for k in range(steps+1):
        if k:
            indices = schedule.step(k, drop_for(k,sense['position_period_ticks'],scenario))
            obs = plant.observe(truth[k],k,indices,potential[k],config)
            try:
                filt.advance(inputs[k-1], obs)
            except (OutOfDomain, EmptySet) as exc:
                status = 'OUT_OF_DOMAIN' if isinstance(exc,OutOfDomain) else 'EMPTY_SET'
                stop_tick = k
                rows.append({'seed':seed,'scenario':scenario,'tick':k,'time_s':k*h,
                    'position_arrived':int(0 in indices),'status':status,
                    'contained_exact':'','contained_tol':'',
                    **{f'truth_{j}':float(truth[k,j]) for j in range(6)},
                    **{f'lower_{j}':'' for j in range(6)}, **{f'upper_{j}':'' for j in range(6)}})
                break
        b = filt.box
        exact, member = b.contains(truth[k]), b.contains(truth[k], 1e-10)
        members.append(member); exact_members.append(exact)
        rows.append({'seed':seed,'scenario':scenario,'tick':k,'time_s':k*h,
            'position_arrived':int(0 in indices),'status':'VALID_NUMERICAL_BOX',
            'contained_exact':int(exact),'contained_tol':int(member),
            **{f'truth_{j}':float(truth[k,j]) for j in range(6)},
            **{f'lower_{j}':float(b.lower[j]) for j in range(6)},
            **{f'upper_{j}':float(b.upper[j]) for j in range(6)}})
        if not member:
            status, stop_tick = 'MEMBERSHIP_FAILURE', k
            break
    digest = hashlib.sha256(truth.astype('<f8').tobytes()+inputs.astype('<f8').tobytes()+potential.astype('<f8').tobytes()).hexdigest()
    summary = {'seed':seed,'split':split_for(seed),'scenario':scenario,'status':status,
        'stop_tick':stop_tick,'stop_time_s':stop_tick*h,'valid_steps_including_initial':len(members),
        'membership_failures_on_valid_steps':sum(not m for m in members),
        'exact_membership_failures_on_valid_steps':sum(not m for m in exact_members),
        'final_valid_velocity_halfwidth':filt.box.radius[2:4].tolist(),
        'full_truth_remains_in_domain':all(filt.domain.contains(x) for x in truth),
        'source_trajectory_sha256':digest,'planned_ticks':steps}
    metadata = windows(f'{seed}-{scenario}',seed,steps+1,config['training']['window_ticks'],stride=25)
    return rows, summary, metadata


def linear_comparison(config):
    """Two-state constant-velocity system; comparison does not certify planar filter."""
    h = config['plant']['dt_s']; steps = 1000
    A = np.array([[1,h],[0,1.]])
    C = np.array([[1.,0.]])
    w = np.array([1e-5,.002]); v = np.array([.02])
    rows, summaries = [], []
    for scenario in ('S0','S1','S2'):
        box = Box.from_center([0,0],[.02,.1])
        z = Zonotope(box.center,np.diag(box.radius))
        truth = np.array([0.,.05])
        rng = rng_for(70001, 'linear_noise')
        noise_by_tick = rng.uniform(-1,1,steps+1)
        schedule = PacketSchedule()
        failures = 0
        lp_failures = 0
        for k in range(steps+1):
            if k:
                disturbance = w*np.array([np.sin(k*.07),np.cos(k*.03)])
                truth = A@truth+disturbance
                box = Box.from_center(A@box.center, np.abs(A)@box.radius+w)
                z = z.affine(A,np.diag(w)).reduce(20)
            indices = schedule.step(k,drop_for(k,5,scenario))
            arrives = 0 in indices
            if arrives:
                y = C@truth+v*noise_by_tick[k]
                obsbox = Box([y[0]-v[0],box.lower[1]],[y[0]+v[0],box.upper[1]])
                box = box.intersect(obsbox)
                z = z.strip(C,y,v).reduce(20)
            # Numerical LP witness checks the actual zonotope, in addition to hulls.
            lp = linprog(np.zeros(z.generators.shape[1]), A_eq=z.generators,
                         b_eq=truth-z.center, bounds=[(-1,1)]*z.generators.shape[1], method='highs')
            lp_member = bool(lp.success and np.max(np.abs(z.generators@lp.x-(truth-z.center))) <= 1e-8
                             and np.max(np.abs(lp.x)) <= 1+1e-8)
            lp_failures += not lp_member
            member = box.contains(truth,1e-10) and z.box.contains(truth,1e-10)
            failures += not member
            rows.append({'scenario':scenario,'tick':k,'time_s':k*h,'position_arrived':int(arrives),
                         'box_velocity_radius':box.radius[1],'zonotope_velocity_hull_radius':z.box.radius[1],
                         'truth_position':truth[0],'truth_velocity':truth[1],
                         'both_hulls_contain_truth':int(member), 'zonotope_lp_member':int(lp_member)})
        summaries.append({'scenario':scenario,'ticks':steps,'hull_membership_failures':failures,'zonotope_lp_membership_failures':lp_failures,
            'box_final_velocity_radius':box.radius[1], 'zonotope_final_velocity_hull_radius':z.box.radius[1]})
    return rows, summaries


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',type=Path,default=ROOT/'configs/planar_baseline.json')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists() and any(args.output.iterdir()):
        parser.error('output must be empty: use a new run directory')
    args.output.mkdir(parents=True,exist_ok=True)
    config=json.loads(args.config.read_text())
    # This pilot is deliberately bound to a narrow, reviewed contract.
    if config['sensing']['delay_ticks'] != 0 or config['plant']['truth_semantics'] != 'defined_discrete_euler':
        parser.error('unsupported delay or truth semantics')
    if config['sensing']['position_period_ticks'] != 5 or config['sensing']['max_consecutive_missed_packets'] != 2:
        parser.error('linear comparison requires period=5, max_missing=2')
    rows, summary, index = [], [], []
    for seed in (70001,70002,70003):
        for scenario in ('S0','S1','S2'):
            a,b,c=planar_replay(config,seed,scenario);rows+=a;summary.append(b);index+=c
    linear_rows, linear_summary=linear_comparison(config)
    csv_write(args.output/'planar_steps.csv',rows)
    csv_write(args.output/'linear_steps.csv',linear_rows)
    save_json(args.output/'window_index.json',index)
    save_json(args.output/'summary.json',{'kind':'G1_pilot_not_learning_or_control_evaluation',
        'arithmetic':'FLOAT64_ENGINEERING_MARGIN_NOT_CERTIFIED','discrete_residual_halfwidth':residual_halfwidth(config).tolist(),
        'planar':summary,'linear':linear_summary,
        'limitations':['No neural model or MPC','No formal test seeds consumed',
                       'Global residual envelope assumes the fixed analytic benchmark',
                       'Zonotope membership uses numerical LP witnesses with 1e-8 tolerance',
                       'No rigorous floating point error certificate']})
    sources=[*sorted((ROOT/'src').rglob('*.py')),Path(__file__).resolve()]
    source_hashes={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sources}
    artifacts={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(args.output.iterdir()) if f.is_file()}
    save_json(args.output/'manifest.json',{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,
        'config_sha256':hashlib.sha256(args.config.read_bytes()).hexdigest(),'source_sha256':source_hashes,
        'artifact_sha256':artifacts,'seeds':[70001,70002,70003],'split':'g1_pilot',
        'prior_plan_commit':'1323ab4e1315f112018561d1e502c987e48386bb'})
    print(json.dumps({'planar_statuses':[r['status'] for r in summary],'linear':linear_summary}))
    if any(r['membership_failures_on_valid_steps'] or r['status']=='EMPTY_SET' for r in summary):
        raise SystemExit(1)
    if any(r['hull_membership_failures'] or r['zonotope_lp_membership_failures'] for r in linear_summary):
        raise SystemExit(1)


if __name__=='__main__':
    main()
