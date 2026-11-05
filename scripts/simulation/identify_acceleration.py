"""Small-axis excitation of local PX4/Gazebo, isolated from the MPC algorithm."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import time
import numpy as np
from cz_sitl import Trial, GazeboReference, mavutil, REPO


def schedule(split):
    rng = np.random.default_rng(20261104+(split == 'validation'))
    blocks = [(axis, sign) for axis in range(3) for sign in ([1, -1] if split == 'calibration' else [-1])]
    rng.shuffle(blocks)
    amplitude = .4 if split == 'calibration' else .3
    durations = [.4, .8, 1.6, .8, .4] if split == 'calibration' else [.4, .6, 1.2, .6, .8]
    return [dict(axis=int(axis), sign=int(sign), phases=[dict(duration=dt,
        u=(np.eye(3)[axis]*sign*amplitude*value).tolist())
        for dt, value in zip(durations, [0, 1, -1, 1, 0])]) for axis, sign in blocks]


class TimedReference(GazeboReference):
    def __init__(self):
        super().__init__()
        self.previous_q = None

    def update_scene(self, message):
        super().update_scene(message)
        for pose in message.pose:
            if pose.name == 'x500_0':
                q = np.array([pose.orientation.w, pose.orientation.x, pose.orientation.y, pose.orientation.z])
                with self.lock:
                    if self.rows:
                        row = self.rows[-1]
                        row['arrival_monotonic'] = time.monotonic()
                        row['tilt'] = float(np.arccos(np.clip(1-2*(q[1]**2+q[2]**2), -1, 1)))
                        row['rotation_rate'] = (float(2*np.arccos(np.clip(abs(q@self.previous_q), -1, 1))/row['dt'])
                                                if self.previous_q is not None else 0.)
                    self.previous_q = q
                break


class IdentificationTrial(Trial):
    def __init__(self, args):
        super().__init__(args)
        self.reference = TimedReference()
        self.sent, self.blocks, self.gates = [], [], []
        self.phase, self.anchor = 'startup', None
        self.report.update(scope='Open-loop acceleration-interface identification; not MPC validation', split=args.split)
        self.plan = schedule(args.split)
        (self.out/'schedule.json').write_text(json.dumps(self.plan, indent=2))
        self.log_config = self.px4/'build/px4_sitl_default/etc/logging/logger_topics.txt'
        self.log_config_installed = False

    def launch(self):
        if subprocess.run(['pgrep', '-x', 'px4'], capture_output=True).returncode == 0:
            raise RuntimeError('Existing PX4; refusing to change its logger or take it over')
        self.old_config = self.log_config.read_bytes() if self.log_config.exists() else None
        topics = ['trajectory_setpoint','offboard_control_mode','vehicle_local_position',
                  'vehicle_local_position_groundtruth','vehicle_attitude','vehicle_attitude_groundtruth',
                  'vehicle_angular_velocity_groundtruth','vehicle_attitude_setpoint',
                  'vehicle_rates_setpoint','vehicle_thrust_setpoint','vehicle_acceleration',
                  'vehicle_status','hover_thrust_estimate','actuator_motors','vehicle_command',
                  'vehicle_command_ack','vehicle_control_mode','vehicle_land_detected',
                  'vehicle_local_position_setpoint']
        self.log_config.parent.mkdir(parents=True, exist_ok=True)
        self.log_config.write_text(''.join(t+' 0 0\n' for t in topics))
        self.log_config_installed = True
        (self.out/'logger_topics.txt').write_bytes(self.log_config.read_bytes())
        super().launch()

    def setpoint(self):
        if self.position_sp is None and self.acceleration_sp is None:
            return
        ref = self.reference.get()
        start = time.monotonic()
        super().setpoint()
        self.sent.append(dict(host_before=start, host_after=time.monotonic(),
            sim_time=ref[0] if ref else None, boot_ms=self.latest_boot_ms, phase=self.phase,
            kind='acceleration' if self.acceleration_sp is not None else 'position',
            command=np.asarray(self.acceleration_sp if self.acceleration_sp is not None else self.position_sp).tolist()))

    def safety(self):
        ref = self.reference.get()
        if self.anchor is not None:
            if np.any(abs(ref[1]-self.anchor) > [1.5,1.5,.8]) or np.any(abs(ref[2]) > 1.):
                raise RuntimeError('Identification supervisory position/velocity limit')
            if (self.custom_mode >> 16) & 255 != 6:
                raise RuntimeError('Left Offboard during identification')

    def hover_gate(self):
        self.phase = 'position_reset'
        self.acceleration_sp, self.position_sp = None, self.hold.copy()
        self.setpoint()
        start = self.reference.get()[0]
        last_good = None
        deadline = time.monotonic()+60
        while time.monotonic() < deadline:
            self.pump(.03)
            self.safety()
            with self.reference.lock:
                rows = [r for r in self.reference.rows if r['t'] >= self.reference.latest[0]-1.5]
            if not rows or rows[-1]['t']-start < 6 or rows[-1]['t']-rows[0]['t'] < 1.45:
                continue
            good = all(np.all(abs(np.array(r['v_difference'])) < .04)
                and np.all(abs(np.array(r['p'])-self.anchor) < .15)
                and r.get('tilt', 1) < .04 and r.get('rotation_rate', 1) < .06 for r in rows)
            if good:
                last_good = dict(sim_time=rows[-1]['t'], waited=rows[-1]['t']-start,
                    velocity_absmax=np.max(abs(np.array([r['v_difference'] for r in rows])),axis=0).tolist(),
                    max_tilt=max(r['tilt'] for r in rows), max_rotation_rate=max(r['rotation_rate'] for r in rows))
                self.gates.append(last_good)
                print('hover_gate '+json.dumps(last_good), flush=True)
                return
        raise TimeoutError('Stable hover gate not satisfied within 60 wall seconds')

    def run(self):
        self.launch()
        self.command(mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, [1.])
        self.command(mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, [0.,0.,0.,float('nan'),float('nan'),float('nan'),3.])
        self.pump(60, lambda: self.local is not None and self.local[2] < -2.6)
        self.pump(8)
        self.hold = self.local.copy()
        self.position_sp = self.hold.copy()
        self.pump(2)
        self.command(mavutil.mavlink.MAV_CMD_DO_SET_MODE, [1.,6.])
        self.pump(3)
        if (self.custom_mode >> 16) & 255 != 6:
            raise RuntimeError('Offboard not confirmed')
        self.anchor = self.reference.get()[1].copy()
        self.report['anchor_ned'] = self.anchor.tolist()
        for i, block in enumerate(self.plan):
            self.hover_gate()
            record = dict(index=i, axis=block['axis'], sign=block['sign'], phases=[], completed=False)
            self.blocks.append(record)
            self.phase = f'acceleration_{i}'
            record['start'] = self.reference.get()[0]
            self.position_sp = None
            planned = record['start']
            for j, part in enumerate(block['phases']):
                self.acceleration_sp = np.array(part['u'])
                self.setpoint()
                record['phases'].append(dict(index=j, planned=planned,
                    start=self.reference.get()[0], command=part['u']))
                planned += part['duration']
                def arrived():
                    self.safety()
                    return self.reference.get()[0] >= planned
                self.pump(15, arrived)
            record['end'] = self.reference.get()[0]
            record['completed'] = True
            print('block '+json.dumps(record), flush=True)
        self.hover_gate()
        self.report['completed'] = True

    def finish(self):
        self.phase = 'landing'
        try:
            super().finish()
        finally:
            if self.log_config_installed:
                if self.old_config is None:
                    self.log_config.unlink()
                else:
                    self.log_config.write_bytes(self.old_config)
            for name, value in [('sent', self.sent), ('blocks', self.blocks), ('hover_gates', self.gates)]:
                (self.out/(name+'.json')).write_text(json.dumps(value, indent=2))
            self.report['identification_source_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
            self.report['completed_blocks'] = sum(b['completed'] for b in self.blocks)
            self.report['logger_config_restored'] = (not self.log_config.exists() if self.old_config is None
                else self.log_config.read_bytes() == self.old_config) if self.log_config_installed else True
            paths = re.findall(r'\./log/(\d{4}-\d\d-\d\d/[^\s]+\.ulg)', (self.out/'px4.log').read_text(errors='replace')) if (self.out/'px4.log').exists() else []
            if paths:
                source = self.px4/'build/px4_sitl_default/rootfs/log'/paths[-1]
                if source.exists():
                    shutil.copy2(source, self.out/'flight.ulg')
            (self.out/'report.json').write_text(json.dumps(self.report, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--split', choices=['calibration','validation'], required=True)
    args = parser.parse_args()
    args.delivery, args.force, args.instrumented = 'fresh', 0., False
    trial = IdentificationTrial(args)
    try:
        trial.run()
    except Exception as exc:
        trial.report['error'] = str(exc)
        print(str(exc), flush=True)
    finally:
        trial.finish()
    raise SystemExit(0 if trial.report['completed'] else 1)
