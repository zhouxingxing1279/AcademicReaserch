#!/usr/bin/env python3
"""Run unchanged finite-memory CZ/Tube MPC against local PX4+Gazebo only."""
import argparse
from collections import deque
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import threading
import time
import xml.etree.ElementTree as ET

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
sys.path.append('/usr/lib/python3/dist-packages')
import numpy as np
from pymavlink import mavutil
from gz.transport13 import Node
from gz.msgs10.odometry_pb2 import Odometry
from gz.msgs10.pose_v_pb2 import Pose_V
from gz.msgs10.entity_wrench_pb2 import EntityWrench
from gz.msgs10.entity_pb2 import Entity
from src.outerloop.finite_memory import Contract, FiniteMemoryEstimator, ContractError
from src.outerloop.tube_mpc import TubeDesign, NominalMPC


class GazeboReference:
    def __init__(self):
        self.lock = threading.Lock()
        self.latest = None
        self.previous = None
        self.rows = []

    def update_scene(self, message):
        for pose in message.pose:
            if pose.name == 'x500_0':
                odometry = Odometry()
                odometry.header.CopyFrom(message.header)
                odometry.pose.CopyFrom(pose)
                self.update(odometry)
                break

    def update(self, message):
        t = message.header.stamp.sec+message.header.stamp.nsec*1e-9
        p = message.pose.position
        # ENU -> NED. No PX4 estimated velocity is fed to the outer filter.
        position = np.array([p.y, p.x, -p.z])
        with self.lock:
            if self.previous is not None and t > self.previous[0]:
                dt = t-self.previous[0]
                velocity = (position-self.previous[1])/dt
                self.latest = (t, position, velocity, dt)
                self.rows.append(dict(t=t, p=position.tolist(), v_difference=velocity.tolist(), dt=dt))
            self.previous = t, position

    def get(self):
        with self.lock:
            return self.latest


def assets(px4, folder):
    model = ET.parse(px4/'Tools/simulation/gz/models/x500/model.sdf')
    plugin = ET.SubElement(model.getroot().find('model'), 'plugin',
                           filename='gz-sim-odometry-publisher-system', name='gz::sim::systems::OdometryPublisher')
    for name, value in [('dimensions', '3'), ('odom_publish_frequency', '100'),
                        ('odom_topic', '/cz/odometry'), ('odom_frame', 'world')]:
        ET.SubElement(plugin, name).text = value
    model_path = folder/'x500_instrumented.sdf'
    model.write(model_path, encoding='utf-8', xml_declaration=True)
    world = ET.parse(px4/'Tools/simulation/gz/worlds/default.sdf')
    include = ET.SubElement(world.getroot().find('world'), 'include')
    ET.SubElement(include, 'uri').text = 'file://'+str(model_path)
    ET.SubElement(include, 'name').text = 'x500_0'
    ET.SubElement(include, 'pose').text = '0 0 0.3 0 0 0'
    world_path = folder/'world.sdf'
    world.write(world_path, encoding='utf-8', xml_declaration=True)
    return world_path


class Trial:
    def __init__(self, args):
        self.args = args
        self.root = Path.home()/'px4-research'
        self.px4 = self.root/'PX4-Autopilot'
        self.out = REPO/'experiments/results/gazebo_cz'/args.name
        self.out.mkdir(parents=True, exist_ok=False)
        self.runtime = self.root/'cz-sitl'/args.name
        self.runtime.mkdir(parents=True, exist_ok=False)
        self.reference = GazeboReference()
        self.processes, self.handles = [], []
        self.telemetry, self.algorithm, self.events = [], [], []
        self.last_hb, self.last_sp = 0., 0.
        self.position_sp, self.acceleration_sp = None, None
        self.armed, self.custom_mode = False, None
        self.local = None
        self.latest_boot_ms = 0
        self.report = dict(name=args.name, delivery=args.delivery, force_newtons=args.force,
                           contract=asdict(Contract()), completed=False, landed=False,
                           scope='Empirical SITL; ideal initial prior and synthetic outer position channel')
        self.report['instrumented_model'] = args.instrumented

    def launch(self):
        if subprocess.run(['pgrep', '-x', 'px4'], capture_output=True).returncode == 0:
            raise RuntimeError('An existing PX4 instance is active; not taking it over')
        os.environ['GZ_PARTITION'] = f'cz_sitl_{os.getpid()}'
        env = dict(os.environ)
        env.update(GZ_SIM_RESOURCE_PATH=str(self.px4/'Tools/simulation/gz/models'),
                   GZ_SIM_SYSTEM_PLUGIN_PATH=str(self.px4/'build/px4_sitl_default/src/modules/simulation/gz_plugins'),
                   GZ_SIM_SERVER_CONFIG_PATH=str(self.px4/'src/modules/simulation/gz_bridge/server.config'),
                   HEADLESS='1', PX4_SYS_AUTOSTART='4001', PX4_SIM_MODEL='gz_x500',
                   PX4_GZ_STANDALONE='1', PX4_GZ_WORLD='default', PX4_GZ_MODEL_NAME='x500_0')
        world = assets(self.px4, self.runtime)
        self.node = Node()
        if self.args.instrumented:
            assert self.node.subscribe(Odometry, '/cz/odometry', self.reference.update)
        else:
            assert self.node.subscribe(Pose_V, '/world/default/dynamic_pose/info', self.reference.update_scene)
        self.force_pub = self.node.advertise('/world/default/wrench/persistent', EntityWrench)
        self.clear_pub = self.node.advertise('/world/default/wrench/clear', Entity)
        self.link = mavutil.mavlink_connection('udpin:127.0.0.1:14540', source_system=255)
        commands = [('gazebo', ['gz', 'sim', '-r', '-s', str(world)]),
                           ('px4', [str(self.px4/'build/px4_sitl_default/bin/px4'),
                                    str(self.px4/'build/px4_sitl_default/etc'),
                                    '-s', 'etc/init.d-posix/rcS'])]
        if not self.args.instrumented:
            env = dict(os.environ)
            commands = [('px4', [str(self.root/'bin/launch-px4.sh'), 'x500', 'headless'])]
        for label, cmd in commands:
            handle = (self.out/(label+'.log')).open('w')
            self.handles.append(handle)
            process = subprocess.Popen(cmd, cwd=self.runtime, env=env, stdin=subprocess.PIPE,
                                       stdout=handle, stderr=subprocess.STDOUT, start_new_session=True, text=True)
            self.processes.append(process)
        self.pump(120, lambda: self.local is not None and self.reference.get() is not None)
        self.pump(12)

    def setpoint(self):
        if self.position_sp is None and self.acceleration_sp is None:
            return
        if self.acceleration_sp is not None:
            mask = 7+56+2048  # ignore p, v, yaw rate; acceleration and yaw active
            p, a = [0., 0., 0.], self.acceleration_sp
        else:
            mask = 56+448+2048
            p, a = self.position_sp, [0., 0., 0.]
        self.link.mav.set_position_target_local_ned_send(self.latest_boot_ms, 1, 1,
            mavutil.mavlink.MAV_FRAME_LOCAL_NED, mask, *p, 0., 0., 0., *a, 0., 0.)

    def pump(self, seconds, predicate=None):
        deadline = time.monotonic()+seconds
        while time.monotonic() < deadline:
            if any(p.poll() is not None for p in self.processes):
                raise RuntimeError('Simulator/PX4 process exited')
            now = time.monotonic()
            if now-self.last_hb >= 1:
                self.link.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_GCS,
                    mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
                self.last_hb = now
            if now-self.last_sp >= .05:
                self.setpoint()
                self.last_sp = now
            m = self.link.recv_match(blocking=True, timeout=.01)
            if m is not None and m.get_srcSystem() == 1:
                kind = m.get_type()
                if kind == 'HEARTBEAT':
                    self.armed = bool(m.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED)
                    self.custom_mode = m.custom_mode
                elif kind == 'LOCAL_POSITION_NED':
                    self.latest_boot_ms = m.time_boot_ms
                    self.local = np.array([m.x, m.y, m.z])
                    self.telemetry.append(m.to_dict())
                elif kind in ['COMMAND_ACK', 'STATUSTEXT']:
                    self.events.append(m.to_dict())
                    if kind == 'STATUSTEXT':
                        print(m.text, flush=True)
                if kind == 'COMMAND_ACK':
                    self.ack = m
            if predicate and predicate():
                return
        if predicate:
            raise TimeoutError('Expected simulator event not observed')

    def command(self, command, values):
        self.ack = None
        self.link.mav.command_long_send(1, 1, command, 0, *(values+[0.]*(7-len(values))))
        self.pump(10, lambda: self.ack is not None and self.ack.command == command)
        if self.ack.result not in [0, 5]:
            raise RuntimeError(f'Command {command} rejected: {self.ack.result}')

    def clear_force(self):
        msg = Entity(name='x500_0', type=Entity.MODEL)
        self.clear_pub.publish(msg)

    def run(self):
        self.launch()
        self.command(mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, [1.])
        self.command(mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, [0., 0., 0., float('nan'), float('nan'), float('nan'), 3.])
        self.pump(60, lambda: self.local is not None and self.local[2] < -2.6)
        self.pump(8)
        self.position_sp = self.local.copy()
        self.pump(2)
        self.command(mavutil.mavlink.MAV_CMD_DO_SET_MODE, [1., 6.])
        self.pump(3)
        self.report['offboard_entered'] = (self.custom_mode >> 16) & 255 == 6
        if not self.report['offboard_entered']:
            raise RuntimeError('Offboard mode not confirmed')
        c, d = Contract(), TubeDesign(Contract())
        ref = self.reference.get()
        target = ref[1]+np.array([.2, 0., 0.])
        x = np.column_stack([ref[1]-target, ref[2]])
        z = x.copy()  # explicitly idealized initial prior, no subsequent velocity feedback
        filters = [FiniteMemoryEstimator(c, zz) for zz in z]
        opts = [NominalMPC(d) for _ in range(3)]
        rng, pending = np.random.default_rng(20261104), {}
        start, previous, force_cleared = ref[0], None, False
        self.report['target_ned'] = target.tolist()
        if self.args.force:
            self.report['force_subscriber_connected'] = bool(self.force_pub.has_connections())
            if not self.report['force_subscriber_connected']:
                raise RuntimeError('No Gazebo wrench subscriber; force trial not started')
            msg = EntityWrench()
            msg.entity.name, msg.entity.type = 'x500_0', Entity.MODEL
            msg.wrench.force.x = self.args.force  # world ENU east
            self.report['force_publish_accepted'] = bool(self.force_pub.publish(msg))
            if not self.report['force_publish_accepted']:
                raise RuntimeError('Gazebo wrench publication failed')
        for k in range(self.args.steps):
            if k:
                self.pump(10, lambda: self.reference.get()[0] >= start+k*c.T)
            ref = self.reference.get()
            x = np.column_stack([ref[1]-target, ref[2]])
            row = dict(k=k, sim_time=ref[0], sample_lateness=ref[0]-(start+k*c.T),
                       reference_velocity_dt=ref[3], state=x.tolist(), nominal=z.tolist(), command_sent=False)
            if previous is not None:
                residual = x-(previous['state']@d.A.T+np.outer(previous['u'], d.B))
                row.update(residual=residual.tolist(), equivalent_a_position=(2*residual[:, 0]/c.T**2).tolist(),
                           equivalent_a_velocity=(residual[:, 1]/c.T).tolist())
            if ref[0]-start >= 4 and not force_cleared:
                self.clear_force()
                force_cleared = True
            if (self.custom_mode >> 16) & 255 != 6:
                raise RuntimeError('PX4 left Offboard during algorithm')
            if self.args.delivery == 'fresh' or k % 2 == 1:
                delay = 0 if self.args.delivery == 'fresh' else 1
                pending.setdefault(k+delay, []).append((k, x[:, 0]+rng.uniform(-c.noise, c.noise, 3)))
            arrivals = pending.pop(k, [])
            row['arrivals'] = [(s, y.tolist()) for s, y in arrivals]
            tic = time.perf_counter()
            try:
                hats, controls, nominal_u, contained = [], [], [], []
                for axis in range(3):
                    post = filters[axis].observe([(s, y[axis]) for s, y in arrivals])
                    hat = post.representative()
                    seq = opts[axis].solve(z[axis])
                    hats.append(hat)
                    nominal_u.append(seq[0])
                    controls.append(float(seq[0]+d.K@(hat-z[axis])))
                    contained.append(bool(post.contains(x[axis])))
            except (ContractError, RuntimeError) as exc:
                row.update(status='estimator_or_qp_failure', error=str(exc), compute_ms=(time.perf_counter()-tic)*1000)
                self.algorithm.append(row)
                raise RuntimeError(f'Algorithm stopped at k={k}: {exc}') from exc
            u, hats = np.array(controls), np.array(hats)
            row.update(status='computed', estimate=hats.tolist(), input=u.tolist(), nominal_input=list(map(float, nominal_u)),
                       contained=contained, error_bound=(np.abs(x-hats) <= d.E+2e-6).all(axis=1).tolist(),
                       tube=[d.in_tube(xx-zz) for xx, zz in zip(x, z)],
                       compute_ms=(time.perf_counter()-tic)*1000)
            self.algorithm.append(row)
            if np.any(np.abs(x) > [3., 2.]) or np.any(np.abs(u) > 4.):
                raise RuntimeError(f'Original state/input constraint exceeded at k={k}')
            if row['sample_lateness'] > .1 or row['compute_ms'] > 250:
                raise RuntimeError('Timing budget exceeded; no unverified stale command fallback')
            self.position_sp, self.acceleration_sp = None, u
            self.setpoint()
            row['command_sent'] = True
            previous = dict(state=x.copy(), u=u.copy())
            for axis in range(3):
                filters[axis].advance(u[axis])
                z[axis] = d.A@z[axis]+d.B*nominal_u[axis]
            print(json.dumps(dict(k=k, t=ref[0]-start, p=x[:, 0].tolist(), u=u.tolist(), contained=contained)), flush=True)
        self.pump(.5)
        self.report['completed'] = True

    def finish(self):
        if hasattr(self, 'clear_pub'):
            self.clear_force()
        if hasattr(self, 'link') and self.armed:
            try:
                self.acceleration_sp, self.position_sp = None, None
                self.command(mavutil.mavlink.MAV_CMD_NAV_LAND,
                             [0., 0., 0., float('nan'), float('nan'), float('nan'), 0.])
                self.pump(75, lambda: not self.armed)
                self.report['landed'] = True
            except Exception as exc:
                self.report['landing_error'] = str(exc)
        for p in reversed(self.processes):
            if p.poll() is None:
                try:
                    os.killpg(p.pid, signal.SIGINT)
                    p.wait(timeout=8)
                except subprocess.TimeoutExpired:
                    os.killpg(p.pid, signal.SIGKILL)
                    p.wait()
        if hasattr(self, 'link'):
            self.link.close()
        for h in self.handles:
            h.close()
        for name, value in [('algorithm', self.algorithm), ('truth', self.reference.rows),
                            ('telemetry', self.telemetry), ('events', self.events)]:
            (self.out/(name+'.json')).write_text(json.dumps(value, indent=2), encoding='utf-8')
        self.report['computed_steps'] = sum(r['status'] == 'computed' for r in self.algorithm)
        self.report['source_hashes'] = {str(p.relative_to(REPO)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in [Path(__file__), REPO/'src/outerloop/finite_memory.py', REPO/'src/outerloop/tube_mpc.py']}
        self.report['px4_commit'] = subprocess.check_output(['git', '-C', str(self.px4), 'rev-parse', 'HEAD'], text=True).strip()
        (self.out/'report.json').write_text(json.dumps(self.report, indent=2), encoding='utf-8')
        print(json.dumps(self.report, indent=2), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--delivery', choices=['fresh', 'max_gap'], default='fresh')
    parser.add_argument('--force', type=float, default=0.)
    parser.add_argument('--steps', type=int, default=40)
    parser.add_argument('--instrumented', action='store_true', help='Reproduce the separate instrumented-model launcher')
    args = parser.parse_args()
    trial = Trial(args)
    try:
        trial.run()
    except Exception as exc:
        trial.report['error'] = str(exc)
        print(str(exc), flush=True)
    finally:
        trial.finish()
    return 0 if trial.report['completed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
