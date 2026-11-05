"""Read-only audit/replay of retained flights; writes separate diagnostics."""
import json
from pathlib import Path
import sys
import numpy as np
from scipy.optimize import linprog
from pyulog import ULog

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from src.outerloop.finite_memory import Contract, FiniteMemoryEstimator, ContractError
ROOT = REPO/'experiments/results/gazebo_cz'
OUT = REPO/'experiments/results/interface_identification'
TOPICS = ['vehicle_local_position_groundtruth', 'vehicle_attitude_groundtruth',
          'vehicle_angular_velocity_groundtruth', 'hover_thrust_estimate',
          'trajectory_setpoint', 'vehicle_status', 'vehicle_local_position',
          'vehicle_attitude_setpoint', 'offboard_control_mode']


def sample(data, times, keys):
    return np.array([np.interp(times, data['timestamp']*1e-6, data[k]) for k in keys]).T


def minimum_acceleration(rows, axis, initial, actual_dt):
    """Minimum interval-constant disturbance bound compatible with positions.

    Variables are initial p,v, one acceleration disturbance per interval and a.
    This is an offline diagnostic, not a new online estimator/certificate.
    """
    n = len(rows)-1
    dim = 3+n
    state = np.zeros((2, dim)); state[:, :2] = np.eye(2)
    offset = np.zeros(2)
    constraints, rhs = [], []
    for k, row in enumerate(rows):
        if k == 0:
            history = [(state.copy(), offset.copy())]
        else:
            dt = row['sim_time']-rows[k-1]['sim_time'] if actual_dt else .5
            a = np.array([[1., dt], [0., 1.]])
            b = np.array([.5*dt*dt, dt])
            state, offset = a@state, a@offset+b*rows[k-1]['input'][axis]
            state[:, 1+k] += b
            history.append((state.copy(), offset.copy()))
        for stamp, measurement in row['arrivals']:
            s, o = history[stamp]
            for sign in [-1, 1]:
                constraints.append(sign*s[0])
                rhs.append(.005+sign*(measurement[axis]-o[0]))
    for j in range(n):
        for sign in [-1, 1]:
            v = np.zeros(dim); v[2+j] = sign; v[-1] = -1
            constraints.append(v); rhs.append(0.)
    objective = np.zeros(dim); objective[-1] = 1
    bounds = [(initial[0]-.005, initial[0]+.005),
              (initial[1]-.01, initial[1]+.01)]+[(None, None)]*n+[(0., None)]
    result = linprog(objective, A_ub=np.array(constraints), b_ub=rhs, bounds=bounds, method='highs')
    return float(result.fun) if result.success else None


def replay_original(rows):
    result = []
    for axis in range(3):
        estimator = FiniteMemoryEstimator(Contract(), rows[0]['nominal'][axis])
        contained_failure, empty = None, None
        for row in rows:
            try:
                post = estimator.observe([(s,y[axis]) for s,y in row['arrivals']])
                if not post.contains(row['state'][axis]) and contained_failure is None:
                    contained_failure = row['k']
                post.representative()
            except ContractError:
                empty = row['k']
                break
            if 'input' not in row:
                break
            estimator.advance(row['input'][axis])
        result.append(dict(axis=axis,first_containment_failure=contained_failure,first_empty_posterior=empty))
    return result


def audit(name):
    folder = ROOT/name
    rows = json.loads((folder/'algorithm.json').read_text())
    report = json.loads((folder/'report.json').read_text())
    times = np.array([r['sim_time'] for r in rows]); t0 = times[0]
    log = ULog(str(folder/'flight.ulg'), TOPICS)
    data = {d.name: d.data for d in log.data_list if d.multi_id == 0}
    gt = data['vehicle_local_position_groundtruth']
    p = sample(gt, times, ['x', 'y', 'z'])
    v = sample(gt, times, ['vx', 'vy', 'vz'])
    old = np.array([r['state'] for r in rows])
    target = np.array(report['target_ned'])
    residuals = []
    for k in range(len(rows)-1):
        dt = times[k+1]-times[k]
        u = np.array(rows[k]['input'])
        residuals.append(dict(k=k, dt=dt,
            equivalent_velocity=((v[k+1]-v[k])/dt-u).tolist(),
            equivalent_position=(2*(p[k+1]-p[k]-dt*v[k])/dt**2-u).tolist()))
    rates = {name: dict(count=len(d['timestamp']), median_dt=float(np.median(np.diff(d['timestamp']))*1e-6))
             for name, d in data.items()}
    pre = (gt['timestamp']*1e-6 >= t0-2) & (gt['timestamp']*1e-6 <= t0)
    hte = data['hover_thrust_estimate']; ht = hte['timestamp']*1e-6
    hi = int(np.argmin(abs(ht-t0)))
    q = sample(data['vehicle_attitude_groundtruth'], [t0], [f'q[{j}]' for j in range(4)])[0]
    qw, qx, qy, qz = q
    rpy = [np.arctan2(2*(qw*qx+qy*qz), 1-2*(qx*qx+qy*qy)),
           np.arcsin(np.clip(2*(qw*qy-qz*qx), -1, 1)),
           np.arctan2(2*(qw*qz+qx*qy), 1-2*(qy*qy+qz*qz))]
    replay = {}
    initial_old = np.array(rows[0]['nominal'])
    initial_aligned = np.column_stack([p[0]-target, v[0]])
    for label, initial, actual in [('original_fixed_T', initial_old, False),
                                   ('actual_dt', initial_old, True),
                                   ('actual_dt_oracle_initial', initial_aligned, True)]:
        replay[label] = []
        for k in range(1, len(rows)):
            required = [minimum_acceleration(rows[:k+1], ax, initial[ax], actual) for ax in range(3)]
            replay[label].append(dict(k=k, minimum_a=required,
                                     compatible_a_002=[a is not None and a <= .02+1e-7 for a in required]))
    triplets = {}
    packets = {stamp:np.array(y) for row in rows for stamp,y in row['arrivals']}
    if all(k in packets for k in range(3)):
        for label, h0, h1 in [('fixed_T',.5,.5),('actual_dt',times[1]-times[0],times[2]-times[1])]:
            ratio = h1/h0
            residual = packets[2]-(1+ratio)*packets[1]+ratio*packets[0]-.5*h1*(h0*np.array(rows[0]['input'])+h1*np.array(rows[1]['input']))
            bound = .5*h1*(h0+h1)*.02+(2+2*ratio)*.005
            triplets[label] = dict(residual=residual.tolist(),allowed_abs=float(bound),
                                  inconsistent=(abs(residual)>bound+1e-7).tolist())
    result = dict(name=name, t0=t0, rates=rates,
        clock_position_max_difference=np.max(abs(p-target-old[:, :, 0]), axis=0).tolist(),
        finite_difference_velocity_max_difference=np.max(abs(v-old[:, :, 1]), axis=0).tolist(),
        prior_to_first_sample_difference=(old[0]-initial_old).tolist(),
        initial_truth_velocity=v[0].tolist(), initial_rpy_deg=np.rad2deg(rpy).tolist(),
        initial_angular_velocity=sample(data['vehicle_angular_velocity_groundtruth'], [t0], [f'xyz[{j}]' for j in range(3)])[0].tolist(),
        prehandoff_velocity_absmax=[float(np.max(abs(gt[k][pre]))) for k in ['vx','vy','vz']],
        hover_thrust_at_handoff=float(hte['hover_thrust'][hi]), hover_thrust_valid=bool(hte['valid'][hi]),
        residuals_using_logged_truth_velocity=residuals, replay=replay, original_finite_memory_replay=replay_original(rows),
        first_three_position_consistency=triplets,
        scope='Groundtruth interpolated on PX4/Gazebo simulation clock; replay is float64 LP and full-prefix diagnosis, not finite-window proof.')
    return result


if __name__ == '__main__':
    OUT.mkdir(parents=True, exist_ok=True)
    results = [audit(n) for n in ['fresh_nominal_04', 'fresh_force_01', 'fresh_force_02', 'max_gap_force_01']]
    (OUT/'old_log_audit.json').write_text(json.dumps(results, indent=2))
    for r in results:
        print(json.dumps({k:r[k] for k in ['name','initial_truth_velocity','initial_rpy_deg','hover_thrust_at_handoff',
              'finite_difference_velocity_max_difference','clock_position_max_difference']}, indent=2))
        print('first residual', r['residuals_using_logged_truth_velocity'][0])
        print('k2 replay', {k:v[1] for k,v in r['replay'].items()} if len(r['replay']['actual_dt']) > 1 else '')
