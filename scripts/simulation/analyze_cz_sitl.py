"""Audit retained SITL trials and plot model residuals; run in WSL venv."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import numpy as np
from pyulog import ULog
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parents[2]
ROOT = REPO/'experiments/results/gazebo_cz'


def analyze(name):
    folder = ROOT/name
    report = json.loads((folder/'report.json').read_text())
    rows = json.loads((folder/'algorithm.json').read_text())
    if not rows:
        return dict(name=name, completed=False, error=report.get('error'), algorithm_samples=0)
    computed = [row for row in rows if row['status'] == 'computed']
    times = np.array([row['sim_time'] for row in rows])
    trace = (folder/'px4.log').read_text(errors='replace')
    paths = re.findall(r'\./log/(\d{4}-\d\d-\d\d/[^\s]+\.ulg)', trace)
    received = []
    if paths:
        source = Path.home()/'px4-research/PX4-Autopilot/build/px4_sitl_default/rootfs/log'/paths[-1]
        if not source.exists():
            source = Path.home()/'px4-research/cz-sitl'/name/'log'/paths[-1]
        if source.exists():
            shutil.copy2(source, folder/'flight.ulg')
            log = ULog(str(folder/'flight.ulg'), ['trajectory_setpoint', 'vehicle_status'])
            ds = next(d for d in log.data_list if d.name == 'trajectory_setpoint')
            a = np.column_stack([ds.data[f'acceleration[{j}]'] for j in range(3)])
            p = np.column_stack([ds.data[f'position[{j}]'] for j in range(3)])
            v = np.column_stack([ds.data[f'velocity[{j}]'] for j in range(3)])
            for row in computed:
                matches = np.flatnonzero(np.max(np.abs(a-np.array(row['input'])), axis=1) < 1e-6)
                received.append(dict(k=row['k'], matched=len(matches),
                                     acceleration_only=bool(len(matches) and np.all(np.isnan(p[matches])) and np.all(np.isnan(v[matches]))),
                                     px4_times=(ds.data['timestamp'][matches]/1e6).tolist()))
    actual_dt_residual = []
    for before, after in zip(rows, rows[1:]):
        if before['status'] != 'computed':
            continue
        dt = after['sim_time']-before['sim_time']
        state0, state1, command = np.array(before['state']), np.array(after['state']), np.array(before['input'])
        r_p = state1[:, 0]-state0[:, 0]-dt*state0[:, 1]-.5*dt*dt*command
        r_v = state1[:, 1]-state0[:, 1]-dt*command
        actual_dt_residual.append(dict(k=after['k'], dt=dt, a_position=(2*r_p/dt**2).tolist(),
                                       a_velocity=(r_v/dt).tolist()))
    def first_bad(label):
        return next((r['k'] for r in computed if not all(r[label])), None)
    u = np.array([r['input'] for r in computed])
    states = np.array([r['state'] for r in rows])
    expected_hash = report['source_hashes']
    algorithm_hash_matches = all(hashlib.sha256((REPO/p).read_bytes()).hexdigest() == h
                                 for p, h in expected_hash.items() if p.startswith('src/'))
    result = dict(name=name, requested_force=report['force_newtons'], delivery=report['delivery'],
                  completed=report['completed'], landed=report['landed'], error=report.get('error'),
                  algorithm_samples=len(rows), commands=len(computed), duration_until_last_sample=float(times[-1]-times[0]),
                  sent_commands=sum(row.get('command_sent', False) for row in computed)
                      if all('command_sent' in row for row in computed) else None,
                  commands_matched_in_px4=sum(item['matched'] > 0 for item in received),
                  first_containment_failure=first_bad('contained'), first_tube_failure=first_bad('tube'),
                  first_error_bound_failure=first_bad('error_bound'),
                  max_position_error=np.max(np.abs(states[:, :, 0]), axis=0).tolist(),
                  max_reference_speed=np.max(np.abs(states[:, :, 1]), axis=0).tolist(),
                  max_command=float(np.max(np.abs(u))) if len(u) else None,
                  maximum_compute_ms=max(r['compute_ms'] for r in rows),
                  sample_intervals=np.diff(times).tolist(), actual_dt_residual=actual_dt_residual,
                  command_reception=received, source_algorithm_hashes_match=algorithm_hash_matches)
    (folder/'audit.json').write_text(json.dumps(result, indent=2))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('names', nargs='+')
    args = parser.parse_args()
    summaries = [analyze(name) for name in args.names]
    (ROOT/'summary.json').write_text(json.dumps(summaries, indent=2))
    representative = list({(s['delivery'], s['requested_force']): s for s in summaries}.values())
    fig, axes = plt.subplots(2, len(representative), figsize=(5*len(representative), 6.5), squeeze=False, layout='constrained')
    colors = ['#0072B2', '#D55E00', '#009E73']
    for col, summary in enumerate(representative):
        rows = json.loads((ROOT/summary['name']/'algorithm.json').read_text())
        t = np.array([r['sim_time'] for r in rows]); t -= t[0]
        for axis, (color, label) in enumerate(zip(colors, ['North', 'East', 'Down'])):
            axes[0, col].plot(t, [r['state'][axis][0] for r in rows], 'o-', color=color, label=label)
            residual = summary['actual_dt_residual']
            axes[1, col].plot(t[1:1+len(residual)], [r['a_velocity'][axis] for r in residual],
                              'o-', color=color, label=label)
        axes[0, col].set(title=summary['name'], ylabel='Position relative to target (m)', xlabel='Time since first sample (s)')
        axes[0, col].legend(fontsize=8)
        axes[1, col].axhspan(-.02, .02, color='gray', alpha=.2, label='Design disturbance bound')
        axes[1, col].set(ylabel='Velocity residual / actual dt (m/s²)', xlabel='Time since first sample (s)')
        axes[1, col].legend(fontsize=8)
        for ax in axes[:, col]:
            ax.grid(alpha=.2)
    fig.suptitle('PX4 / Gazebo integration: retained failures, unchanged CZ + Tube MPC', fontsize=13)
    fig.savefig(ROOT/'sitl_residuals.png', dpi=180)
    fig.savefig(ROOT/'sitl_residuals.svg')
    plt.close(fig)
    for s in summaries:
        print(json.dumps(s), flush=True)


if __name__ == '__main__':
    main()
