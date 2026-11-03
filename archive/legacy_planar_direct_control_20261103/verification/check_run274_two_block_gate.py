#!/usr/bin/env python3
"""Run274: exact rational two-block shared safety and third-block entry gate.

Only for the frozen 4-state Euler truth and the Run260 tick-60 outer boxes.
The bound is sufficient, not an exact reachable set or terminal RCI.
"""
import argparse
import itertools
import json
from fractions import Fraction as F
from pathlib import Path

H, T, R = F(1, 50), F(981, 100), F(3246383, 1600000)
A, W = F(1, 125), F(1, 100)
BOX = {
    'SMM': {'p': F(665412229, 1250000000), 'v': F(7841778593, 5000000000)},
    'MMS': {'p': F(2474339699, 10000000000), 'v': F(2187058727, 2000000000)},
}

def bound(q, p0, v0, a=A, w=W):
    """For tau=0: global |sin(phi)|<=|phi|, all bounded r and all initial box states."""
    assert isinstance(q, int) and q >= 0
    return {
        'p': p0 + q*H*v0 + H**2*(R*q*(q-1)/2
             + T*(a*q*(q-1)/2 + H*w*q*(q-1)*(q-2)/6)),
        'v': v0 + H*(q*R + T*(q*a + H*w*q*(q-1)/2)),
        'phi': a + q*H*w,
        'omega': w,
    }

def safe(s):
    return s['p'] <= 5 and s['v'] <= 3 and s['phi'] <= F(9,20) and s['omega'] <= 2

def modes(n):
    return [''.join(t) for t in itertools.product('SM', repeat=n) if 'MMM' not in ''.join(t)]

def certify(root=None):
    if root is not None:
        root = Path(root)
        cfg = json.loads((root/'configs/planar_baseline.json').read_text())
        old = json.loads((root/'results/run273_full_box_bridge_20261102/checks.json').read_text())
        run260 = json.loads((root/'results/run260_conditional_shared_bridge_20261102/checks.json').read_text())
        assert cfg['plant']['truth_semantics'] == 'defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s'])) == H
        assert F(str(cfg['plant']['gravity_m_s2'])) == T
        assert cfg['sensing']['position_period_ticks'] == 5
        assert cfg['sensing']['max_consecutive_missed_packets'] == 2
        assert old['run'] == 273 and run260['certified_last_tick'] == 60
        for name in BOX:
            for axis in ('p','v'):
                assert max(abs(F(x)) for x in run260['branches'][name]['tick60_outer'][axis]) == BOX[name][axis]
            for axis, val in bound(15, **{'p0':BOX[name]['p'], 'v0':BOX[name]['v']}).items():
                assert str(val) == old['branches'][name]['tick75_outer_abs'][axis]
    patterns = modes(6)
    assert len(patterns) == 44 and all('MMM' not in s for s in patterns)
    assert len(modes(3)) == 7
    a90 = A + 30*H*W
    extra_v = bound(15, F(0), F(0), a=a90)['v']
    gate_v = F(3) - extra_v
    assert gate_v == F(187678479, 80000000)
    branches = {}
    for name, init in BOX.items():
        states = [bound(q, init['p'], init['v']) for q in range(46)]
        assert all(safe(s) for s in states[:31])
        certified_max = max(q for q,s in enumerate(states) if safe(s))
        assert all(safe(s) for s in states[:certified_max+1])
        assert not safe(states[certified_max+1])
        assert certified_max == {'SMM':33, 'MMS':44}[name]
        at90 = states[30]
        gated105 = bound(15, at90['p'], gate_v, a=a90)
        assert safe(gated105)
        assert at90['v'] > gate_v
        branches[name] = {
            'tick75': {k:str(v) for k,v in states[15].items()},
            'tick90': {k:str(v) for k,v in at90.items()},
            'tick105_unconditional': {k:str(v) for k,v in states[45].items()},
            'all_ticks_60_to_90_safe': True,
            'largest_q_certified_by_this_envelope': certified_max,
            'first_envelope_failure_q': certified_max+1,
            'first_envelope_failure_not_a_reachable_counterexample': True,
            'tick90_conditional_gate_v': str(gate_v),
            'tick105_bound_if_gate_met': {k:str(v) for k,v in gated105.items()},
            'unconditional_tick90_box_meets_gate': False,
        }
    return {
        'run': 274,
        'base': 'Run260 reliable tick60 SMM/MMS outer boxes, Run273 exact 15-step certificate',
        'model': 'frozen 4-state Euler, fixed T=9.81, shared tau=0',
        'all_legal_65_to_90_packet_sequences_count': len(patterns),
        'all_legal_65_to_90_packet_sequences': patterns,
        'tick90_conditional_15step_velocity_gate': str(gate_v),
        'gate_semantics': 'Sufficient for next 15 steps only when reliable tick90 posterior is inside p90 unconditional bound, velocity +/-gate, phi +/-a90, omega +/-W; not proved for all observations',
        'branches': branches,
        'not_certified': ['all tick90 posterior fibers satisfy gate', 'information terminal RCI', 'MPC optimizer', 'exact SMF/CZ posterior', 'infinite recursive feasibility', 'six-state safety', '20ms WCET'],
        'gate_A': 'blocked',
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--root', type=Path)
    p.add_argument('--output', type=Path)
    args=p.parse_args()
    data=json.dumps(certify(args.root), sort_keys=True, indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(data)
    else:
        print(data, end='')

if __name__=='__main__':
    main()
