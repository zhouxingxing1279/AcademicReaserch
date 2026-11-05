"""Calibrate on one flight, evaluate a separate frozen flight; no controller changes."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys
import numpy as np
from scipy.signal import lfilter
from pyulog import ULog
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from audit_cz_interface import sample, ROOT, OUT, REPO
sys.path.insert(0, str(REPO))
from src.outerloop.finite_memory import Contract, FiniteMemoryEstimator, ContractError

DT = .004


def rollout(u, dt, tau, gain=1., bias=0., p0=0., v0=0., a0=0.):
    target = gain*np.asarray(u)+bias
    if tau == 0:
        dv = dt*target
        vp = v0+np.r_[0., np.cumsum(dv)[:-1]]
        dp = vp*dt+.5*dt**2*target
    else:
        e = np.exp(-dt/tau)
        a = lfilter([1-e], [1,-e], target)+a0*e**np.arange(1,len(u)+1)
        ap = np.r_[a0,a[:-1]]
        dv = tau*(1-e)*ap+(dt-tau*(1-e))*target
        vp = v0+np.r_[0.,np.cumsum(dv)[:-1]]
        dp = vp*dt+tau*(dt-tau*(1-e))*ap+(.5*dt**2-tau*(dt-tau*(1-e)))*target
    return np.column_stack([p0+np.r_[0.,np.cumsum(dp)], v0+np.r_[0.,np.cumsum(dv)]])


def load(name):
    folder = ROOT/name
    report = json.loads((folder/'report.json').read_text())
    if not report['completed']:
        raise ValueError(f'{name} did not complete: {report.get("error")}')
    log = ULog(str(folder/'flight.ulg'), ['trajectory_setpoint','vehicle_local_position_groundtruth',
        'hover_thrust_estimate','vehicle_attitude_groundtruth','vehicle_local_position_setpoint'])
    sp = log.get_dataset('trajectory_setpoint').data
    t = sp['timestamp']*1e-6
    commands = np.column_stack([sp[f'acceleration[{i}]'] for i in range(3)])
    active = np.all(np.isfinite(commands),axis=1) & np.all(np.isnan(np.column_stack([sp[f'position[{i}]'] for i in range(3)])),axis=1)
    indices = np.flatnonzero(active & ~np.r_[False,active[:-1]])
    planned = json.loads((folder/'blocks.json').read_text())
    if len(indices) != len(planned):
        raise ValueError(f'Expected {len(planned)} pure acceleration blocks, found {len(indices)}')
    gt = log.get_dataset('vehicle_local_position_groundtruth').data
    hte = log.get_dataset('hover_thrust_estimate').data
    blocks = []
    for i, first in enumerate(indices):
        after = first+np.flatnonzero(~active[first:])[0]
        start, end = t[first], t[after]
        times = start+np.arange(int(np.floor((end-start)/DT))+1)*DT
        p = sample(gt,times,['x','y','z']); v = sample(gt,times,['vx','vy','vz'])
        a0 = np.mean(sample(gt, start+np.array([-.06,-.04,-.02,0.]), ['ax','ay','az']),axis=0)
        blocks.append(dict(index=i, axis=planned[i]['axis'], start=start, end=end,
            times=times, p=p, v=v, a0=a0, cmd_times=t[first:after], commands=commands[first:after],
            hover_thrust=float(sample(hte,[start],['hover_thrust'])[0,0])))
    send = json.loads((folder/'sent.json').read_text())
    accel = [s for s in send if s['kind']=='acceleration']
    gaps = [b['host_before']-a['host_before'] for a,b in zip(accel,accel[1:]) if a['phase']==b['phase']]
    log_gaps = np.concatenate([np.diff(b['cmd_times']) for b in blocks])
    # Log transition time minus latest reference at the corresponding changed send.
    # This includes reference age and is explicitly not a network-delay estimate.
    transition_brackets = []
    for b in blocks:
        sent = [s for s in accel if s['phase']==f'acceleration_{b["index"]}']
        changed_s = [s for j,s in enumerate(sent) if j==0 or s['command'] != sent[j-1]['command']]
        changed_r = [j for j in range(len(b['commands'])) if j==0 or not np.array_equal(b['commands'][j],b['commands'][j-1])]
        if len(changed_s) != len(changed_r):
            raise ValueError('Send/receive transition count differs')
        for s,j in zip(changed_s,changed_r):
            if not np.allclose(s['command'],b['commands'][j],atol=1e-6):
                raise ValueError('Send/receive command mismatch')
            transition_brackets.append(float(b['cmd_times'][j]-s['sim_time']))
    audit = dict(name=name, completed=True, landed=report['landed'], block_count=len(blocks),
        logger_config_restored=report['logger_config_restored'],
        send_interval_wall_max=max(gaps), logged_command_interval_sim_median=float(np.median(log_gaps)),
        logged_command_interval_sim_max=float(max(log_gaps)),
        receive_minus_latest_reference_range=[min(transition_brackets),max(transition_brackets)],
        hover_thrust_at_blocks=[b['hover_thrust'] for b in blocks],
        max_abs_velocity=np.max(abs(np.vstack([b['v'] for b in blocks])),axis=0).tolist())
    return blocks, audit


def input_for(block, axis, delay):
    ti = block['times'][:-1]+DT/2-delay
    indices = np.searchsorted(block['cmd_times'],ti,side='right')-1
    return np.where(indices >= 0, block['commands'][np.maximum(indices,0),axis],0.)


def predict(block, axis, parameters):
    return rollout(input_for(block,axis,parameters['delay']),DT,parameters['tau'],parameters['gain'],
        parameters['bias'],block['p'][0,axis],block['v'][0,axis],block['a0'][axis])


def fit(blocks, axis, taus, delays):
    best = None
    rankings = []
    for tau in taus:
        for delay in delays:
            features, targets = [], []
            for b in blocks:
                u = input_for(b,axis,delay)
                base = rollout(u,DT,tau,0.,0.,v0=b['v'][0,axis],a0=b['a0'][axis])[:,1]
                gu = rollout(u,DT,tau)[:,1]
                bi = rollout(np.ones(len(u)),DT,tau)[:,1]
                features.append(np.column_stack([gu,bi])[::5])
                targets.append((b['v'][:,axis]-base)[::5])
            x,y = np.vstack(features),np.concatenate(targets)
            theta = np.linalg.lstsq(x,y,rcond=None)[0]
            rmse = float(np.sqrt(np.mean((x@theta-y)**2)))
            result = dict(tau=float(tau),delay=float(delay),gain=float(theta[0]),bias=float(theta[1]),calibration_velocity_rmse=rmse)
            rankings.append(result)
            if best is None or rmse < best['calibration_velocity_rmse']:
                best = result
    return best, sorted(rankings,key=lambda r:r['calibration_velocity_rmse'])[:10]


def metrics(errors):
    e = np.vstack(errors)
    return dict(position_rmse=float(np.sqrt(np.mean(e[:,0]**2))),velocity_rmse=float(np.sqrt(np.mean(e[:,1]**2))),
                position_absmax=float(np.max(abs(e[:,0]))),velocity_absmax=float(np.max(abs(e[:,1]))))


def evaluate(blocks, axis, params):
    full, step = [], []
    for b in blocks:
        actual = np.column_stack([b['p'][:,axis],b['v'][:,axis]])
        full.append((predict(b,axis,params)-actual)[::5])
        # Non-overlapping 0.5 s windows; initialized from diagnostic truth.
        for i in range(0,len(b['times'])-125,125):
            u = input_for(b,axis,params['delay'])[i:i+125]
            a0 = (b['v'][i,axis]-b['v'][max(0,i-5),axis])/(DT*min(i,5)) if i else b['a0'][axis]
            pred = rollout(u,DT,params['tau'],params['gain'],params['bias'],b['p'][i,axis],b['v'][i,axis],a0)
            step.append((pred[-1]-actual[i+125])[None,:])
    return dict(full_block=metrics(full), half_second=metrics(step))


def command_moments(block, start, end, axis):
    boundaries = np.r_[start,block['cmd_times'][(block['cmd_times']>start)&(block['cmd_times']<end)],end]
    idx = np.searchsorted(block['cmd_times'],boundaries[:-1]+1e-8,side='right')-1
    if np.any(idx < 0):
        raise ValueError('Command history does not cover replay interval')
    u = block['commands'][idx,axis]
    dv = np.sum(np.diff(boundaries)*u)
    dp = np.sum(.5*((end-boundaries[:-1])**2-(end-boundaries[1:])**2)*u)
    return float(dp),float(dv)


def replay(blocks):
    results = []
    for b in blocks:
        times = b['start']+np.arange(int((b['end']-b['start'])/.5)+1)*.5
        pos = np.column_stack([np.interp(times,b['times'],b['p'][:,i]) for i in range(3)])
        vel = np.column_stack([np.interp(times,b['times'],b['v'][:,i]) for i in range(3)])
        rng = np.random.default_rng(20261104+b['index'])
        noise = rng.uniform(-.005,.005,(len(times),3))
        first = []
        for axis in range(3):
            estimator = FiniteMemoryEstimator(Contract(),np.array([0.,vel[0,axis]]))
            fail, empty, correction = None, None, 0.
            for k,t in enumerate(times):
                transformed_position = pos[k,axis]-pos[0,axis]-correction
                y = transformed_position+noise[k,axis]
                try:
                    post = estimator.observe([(k,y)])
                    if not post.contains([transformed_position,vel[k,axis]]) and fail is None:
                        fail = k
                    post.representative()  # contains(False) alone does not distinguish an empty CZ
                except ContractError:
                    empty = k
                    break
                if k < len(times)-1:
                    # Compensate the known first-moment difference between the
                    # actual switched input and a constant interval-average input.
                    # p' = p - cumulative(dp_actual - h*dv_actual/2), v' = v.
                    dp,dv = command_moments(b,t,t+.5,axis)
                    correction += dp-.25*dv
                    estimator.advance(dv/.5)
            first.append(dict(first_containment_failure=fail,first_empty_posterior=empty))
        results.append(dict(block=b['index'],first_failure_by_axis=first,
            scope='Offline exact known-input moment compensation then original CZ replay; actual switched commands, ideal initial truth and bounded synthetic position noise. Not online controller validation.'))
    return results


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--calibration',required=True); p.add_argument('--validation',required=True)
    args = p.parse_args()
    cal,ca = load(args.calibration); val,va = load(args.validation)
    models,rankings = {},{}
    for axis,label in enumerate(['N','E','D']):
        static,_ = fit(cal,axis,[0.],[0.])
        lag,rank = fit(cal,axis,np.r_[0.,np.arange(.02,.82,.02)],np.arange(0.,.22,.02))
        models[label] = dict(ideal=dict(tau=0.,delay=0.,gain=1.,bias=0.),static=static,lag=lag)
        rankings[label] = rank
        print(label,models[label],flush=True)
    results = {label:{model:dict(parameters=param,calibration=evaluate(cal,axis,param),validation=evaluate(val,axis,param))
        for model,param in models[label].items()} for axis,label in enumerate(['N','E','D'])}
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/'model_comparison.json').write_text(json.dumps(dict(calibration_audit=ca,validation_audit=va,
        models=results,calibration_top_candidates=rankings,validation_estimator_diagnostic=replay(val),
        scope='Empirical identification, groundtruth/difference initialized. Validation never used for fitting. Effective lag/delay not uniquely physical.'),indent=2))
    with (OUT/'predictions.csv').open('w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['split','block','excited_axis','axis','model','sim_time','reference_p','reference_v','prediction_p','prediction_v'])
        for split,blocks in [('calibration',cal),('validation',val)]:
            for b in blocks:
                for axis,label in enumerate(['N','E','D']):
                    for model,param in models[label].items():
                        pred = predict(b,axis,param)
                        for j in range(0,len(b['times']),5):
                            writer.writerow([split,b['index'],b['axis'],label,model,b['times'][j],
                                b['p'][j,axis],b['v'][j,axis],*pred[j]])
    inputs = [Path(__file__),Path(__file__).with_name('audit_cz_interface.py'),
              Path(__file__).with_name('identify_acceleration.py'),REPO/'docs/simulation/INTERFACE_IDENTIFICATION_PLAN.md']
    for name in [args.calibration,args.validation]:
        inputs.extend(ROOT/name/f for f in ['flight.ulg','report.json','blocks.json','sent.json','truth.json','schedule.json'])
    (OUT/'provenance.json').write_text(json.dumps({str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},indent=2))
    fig,axes = plt.subplots(3,2,figsize=(11,9),layout='constrained')
    colors={'ideal':'#999999','static':'#db9b23','lag':'#0072b2'}
    for axis,label in enumerate(['N','E','D']):
        b = next(b for b in val if b['axis']==axis)
        t=b['times']-b['start']
        axes[axis,0].plot(t,b['v'][:,axis],color='black',label='Reference (pose difference)')
        for model,param in models[label].items():
            pred=predict(b,axis,param)
            axes[axis,0].plot(t,pred[:,1],color=colors[model],label=model)
            axes[axis,1].plot(t,pred[:,0]-b['p'][:,axis],color=colors[model],label=model)
        axes[axis,0].set_ylabel(label+' velocity [m/s]')
        axes[axis,1].set_ylabel(label+' position prediction error [m]')
        for ax in axes[axis]:
            ax.set_xlabel('Time in held-out excitation block [s]'); ax.grid(alpha=.2)
    axes[0,0].legend(fontsize=8)
    fig.suptitle('PX4/Gazebo interface identification: independent validation flight')
    fig.savefig(OUT/'validation_predictions.png',dpi=180);fig.savefig(OUT/'validation_predictions.svg')
    plt.close(fig)


if __name__=='__main__':
    main()
