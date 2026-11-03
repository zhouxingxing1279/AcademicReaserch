#!/usr/bin/env python3
"""Run271: constructive Run260 MMS posterior membership for Run270's pair.

Exact Fraction kinematics; pre-45 r=T*sin(phi) cancels lateral acceleration.
Its legality is certified by |sin(phi)|<=|phi|, without floating point.
"""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

H = J = F(1, 50)
T = F(981, 100)
R = F(3246383, 1600000)
EPS = F(1, 50)
PULSE = (F(1, 25), -F(1, 25), -F(1, 25), F(1, 25), F(0))
SUCCESS = (5, 10, 15, 30, 45, 60)
MISSED = (20, 25, 35, 40, 50, 55)


def packet_automaton():
    count = 0
    for k in range(5, 61, 5):
        assert (k in SUCCESS) != (k in MISSED)
        count = 0 if k in SUCCESS else count + 1
        assert count <= 2
    return ''.join('S' if k in SUCCESS else 'M' for k in range(5, 61, 5))


def shared_prefix():
    # Tick0..30: zero truth, zero control and disturbance, zero readings.
    states = {k: (F(0),)*4 for k in range(31)}
    p = v = phi = omega = F(0)
    attitude = {}
    for k in range(30, 45):
        tau = PULSE[k-30] if k < 35 else F(0)
        # Real disturbance r=T*sin(phi) cancels -T*sin(phi) exactly.
        assert T*abs(phi) <= R  # |sin(phi)|<=|phi|
        attitude[k] = (phi, omega, tau)
        p, v, phi, omega = p + H*v, v, phi + H*omega, omega + H*tau/J
        assert p == v == 0
        assert abs(phi) <= F(9,20) and abs(omega) <= 2
        states[k+1] = (p, v, phi, omega)
    assert states[45] == (F(0),)*4
    assert [attitude[k][0] for k in range(30, 35)] == [
        F(0), F(0), F(1,1250), F(1,1250), F(0)]
    assert [attitude[k][1] for k in range(30, 35)] == [
        F(0), F(1,25), F(0), -F(1,25), F(0)]
    assert all(states[k][2:] == (F(0),F(0)) for k in range(35,46))
    return states, attitude


def continuation(sign):
    assert sign in (-1,1)
    states, _ = shared_prefix()
    p, v, phi, omega = states[45]
    for k in range(45,60):
        r = sign*R if k >= 53 else F(0)
        p, v, phi, omega = p + H*v, v + H*r, phi + H*omega, omega
        states[k+1] = (p, v, phi, omega)
    return states


def check_state_box(states):
    for p,v,phi,omega in states.values():
        assert abs(p) <= 5 and abs(v) <= 3
        assert abs(phi) <= F(9,20) and abs(omega) <= 2


def verify(root=None):
    packet = packet_automaton()
    assert packet == 'SSSMMSMMSMMS'
    _, attitude = shared_prefix()
    plus, minus = continuation(1), continuation(-1)
    check_state_box(plus); check_state_box(minus)
    assert all(plus[k] == minus[k] for k in range(46))
    assert all(plus[k][2:] == minus[k][2:] for k in range(61))
    assert plus[60] == (
        F(68174043,4000000000), F(22724681,80000000),F(0),F(0))
    assert minus[60] == tuple(-z for z in plus[60])
    for k in SUCCESS:
        assert abs(plus[k][0]) <= EPS and abs(minus[k][0]) <= EPS
    assert all(plus[k][2:] == (F(0),F(0))
               for k in list(range(31))+list(range(35,61)))
    if root is not None:
        cfg = json.loads((Path(root)/'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics'] == 'defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s'])) == H
        assert F(str(cfg['plant']['inertia_kg_m2'])) == J
        assert F(str(cfg['plant']['gravity_m_s2'])) == T
        assert F(str(cfg['sensing']['observed_noise_halfwidth']['px'])) == EPS
        assert cfg['sensing']['position_period_ticks'] == 5
        assert cfg['sensing']['max_consecutive_missed_packets'] == 2
        cert = json.loads((Path(root)/
            'results/run260_conditional_shared_bridge_20261102/checks.json').read_text())
        for pattern in ('SMM','MMS'):
            box = cert['branches'][pattern]['tick45_outer']
            assert all(F(bounds[0]) <= 0 <= F(bounds[1])
                       for bounds in box.values())
    return {
        'run':271,
        'packet_history_ticks_5_to_60':packet,
        'compatible_run260_tick45_pattern':
            'MMS only (35 miss,40 miss,45 success)',
        'pre45_nonzero_torque_ticks':[30,31,32,33],
        'pre45_phi_at_ticks_30_to_34':
            [str(attitude[k][0]) for k in range(30,35)],
        'pre45_omega_at_ticks_30_to_34':
            [str(attitude[k][1]) for k in range(30,35)],
        'pre45_disturbance_semantics':
            'r_k=T*sin(phi_k) on 30..44, r=0 before; |r|<=T*max|phi|<=R via |sin x|<=|x|',
        'pre45_disturbance_abs_upper_bound':
            str(T*max(abs(v[0]) for v in attitude.values())),
        'pre45_disturbance_limit':str(R),
        'tick45_true_state':[str(x) for x in plus[45]],
        'tick60_plus_state':[str(x) for x in plus[60]],
        'tick60_minus_state':[str(x) for x in minus[60]],
        'tick60_noise_plus':str(-plus[60][0]),
        'tick60_noise_minus':str(-minus[60][0]),
        'tick60_velocity_diameter_lower_bound':
            str(plus[60][1]-minus[60][1]),
        'all_true_states_in_hard_box':True,
        'all_success_position_readings_zero':True,
        'all_required_attitude_readings_zero':True,
        'run260_membership':
            'constructive consistent true trajectories for MMS zero-reading history; guaranteed included by any sound posterior',
        'not_certified':[
            'exact posterior',
            'other Run260 SMM future 50/55 miss branch (illegal)',
            'all observation fibers','all causal controls',
            '15-tick feedback return','terminal information RCI',
            'MPC solver','infinite recursive feasibility',
            'six-state safety','20ms WCET'],
        'gate_A':'blocked',
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',type=Path)
    ap.add_argument('--output',type=Path)
    a=ap.parse_args()
    s=json.dumps(verify(a.root),indent=2,sort_keys=True,ensure_ascii=False)+'\n'
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(s)
    else:
        print(s,end='')


if __name__=='__main__':
    main()
