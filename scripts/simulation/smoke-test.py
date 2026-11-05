#!/usr/bin/env python3
"""Start local SITL, verify telemetry and optionally test X500 takeoff/landing.

Run with ~/px4-research/.venv/bin/python. This only starts a local simulator;
there is no serial/remote endpoint option and no forced arming.
"""
import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import time

from pymavlink import mavutil

parser = argparse.ArgumentParser()
parser.add_argument('--model', choices=['x500', 'rc_cessna', 'standard_vtol'], default='x500')
parser.add_argument('--flight', action='store_true')
parser.add_argument('--gui', action='store_true')
args = parser.parse_args()
if args.flight and args.model != 'x500':
    parser.error('The takeoff/landing check is only defined for X500.')
if subprocess.run(['pgrep', '-x', 'px4'], capture_output=True).returncode == 0:
    raise SystemExit('Close the existing PX4 instance before testing.')

root = Path(os.environ.get('PX4_RESEARCH_ROOT', str(Path.home() / 'px4-research')))
stamp = time.strftime('%Y%m%d-%H%M%S')
prefix = root / 'logs' / f'smoke-{args.model}-{stamp}'
report = {'model': args.model, 'flight_requested': args.flight, 'gui_requested': args.gui,
          'passed': False, 'log': str(prefix.with_suffix('.log'))}
env = dict(os.environ, GZ_PARTITION=f'px4_smoke_{os.getpid()}')
link = mavutil.mavlink_connection('udpin:127.0.0.1:14540', source_system=255)
last_heartbeat = 0
max_alt = 0.0
process = None


def receive(duration, predicate=None):
    global last_heartbeat, max_alt
    deadline = time.monotonic() + duration
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f'SITL exited with code {process.returncode}')
        now = time.monotonic()
        if now - last_heartbeat >= 1:
            link.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_GCS,
                                    mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
            last_heartbeat = now
        msg = link.recv_match(blocking=True, timeout=0.2)
        if msg is None or msg.get_srcSystem() != 1:
            continue
        if msg.get_type() == 'GLOBAL_POSITION_INT':
            max_alt = max(max_alt, msg.relative_alt / 1000.0)
        if msg.get_type() == 'STATUSTEXT':
            print(msg.text, flush=True)
        if predicate and predicate(msg):
            return msg
    if predicate:
        raise TimeoutError(f'Expected telemetry not received within {duration}s')


def command(command_id, *values):
    params = list(values) + [0] * (7 - len(values))
    link.mav.command_long_send(1, 1, command_id, 0, *params)
    ack = receive(10, lambda m: m.get_type() == 'COMMAND_ACK' and m.command == command_id)
    if ack.result not in (mavutil.mavlink.MAV_RESULT_ACCEPTED,
                          mavutil.mavlink.MAV_RESULT_IN_PROGRESS):
        raise RuntimeError(f'Command {command_id} rejected: MAV_RESULT={ack.result}')
    return ack


try:
    with prefix.with_suffix('.log').open('w') as output:
        process = subprocess.Popen(
            [str(root / 'bin' / 'launch-px4.sh'), args.model, 'gui' if args.gui else 'headless'],
            stdin=subprocess.PIPE, stdout=output, stderr=subprocess.STDOUT,
            env=env, start_new_session=True, text=True)
        heartbeat = receive(120, lambda m: m.get_type() == 'HEARTBEAT'
                            and m.autopilot == mavutil.mavlink.MAV_AUTOPILOT_PX4)
        report['heartbeat'] = True
        report['vehicle_type'] = heartbeat.type
        receive(25)
        position = receive(30, lambda m: m.get_type() == 'LOCAL_POSITION_NED')
        report['local_position_ned'] = [position.x, position.y, position.z]
        if args.flight:
            command(mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 1)
            command(mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, float('nan'),
                    float('nan'), float('nan'), 5)
            receive(75, lambda m: m.get_type() == 'GLOBAL_POSITION_INT'
                    and m.relative_alt >= 4000)
            receive(5)
            command(mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 0, 0, float('nan'),
                    float('nan'), float('nan'), 0)
            receive(90, lambda m: m.get_type() == 'HEARTBEAT'
                    and not (m.base_mode & mavutil.mavlink.MAV_MODE_FLAG_SAFETY_ARMED))
            report['landed_and_disarmed'] = True
        report['passed'] = True
except Exception as exc:
    report['error'] = str(exc)
finally:
    report['max_relative_altitude_m'] = max_alt
    if process is not None:
        if process.poll() is None:
            try:
                process.stdin.write('shutdown\n')
                process.stdin.flush()
                process.wait(timeout=8)
            except (BrokenPipeError, subprocess.TimeoutExpired):
                pass
        try:
            os.killpg(process.pid, signal.SIGINT)
        except ProcessLookupError:
            pass
        try:
            process.wait(timeout=8)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()
    link.close()
    prefix.with_suffix('.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2), flush=True)
raise SystemExit(0 if report['passed'] else 1)
