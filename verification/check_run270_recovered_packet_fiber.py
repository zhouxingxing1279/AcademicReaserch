#!/usr/bin/env python3
"""Run270: exact rational two-trajectory post-success information floor.

Frozen Run260 four-state defined-discrete Euler plant. No MPC/RCI claim.
"""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

H = F(1, 50)
R = F(3246383, 1600000)
T = F(981, 100)
J = F(1, 50)
EPS_P = F(1, 50)
START, END = 45, 60


def trajectory(sign, active_from=53):
    """Tick45 zero state, tau=0, disturbance sign*R on [active_from,60)."""
    if sign not in (-1, 1) or not START <= active_from < END:
        raise ValueError((sign, active_from))
    p = v = phi = omega = F(0)
    states = {START: (p, v, phi, omega)}
    for k in range(START, END):
        r = sign * R if k >= active_from else F(0)
        # phi=0 exactly; sin(phi)=0 exactly for this witness.
        p, v, phi, omega = p + H*v, v + H*r, phi + H*omega, omega
        states[k+1] = (p, v, phi, omega)
    return states


def family(j):
    """Symmetric +/- disturbance for the last j Euler transitions."""
    if not 1 <= j <= END - START:
        raise ValueError(j)
    plus, minus = trajectory(1, END-j), trajectory(-1, END-j)
    return plus, minus


def check_legal(states):
    assert set(states) == set(range(START, END+1))
    for p, v, phi, omega in states.values():
        assert abs(p) <= 5 and abs(v) <= 3
        assert abs(phi) <= F(45, 100) and abs(omega) <= 2
    return True


def certificate(root=None):
    if root is not None:
        cfg = json.loads((Path(root)/'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics'] == 'defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s'])) == H
        assert F(str(cfg['plant']['inertia_kg_m2'])) == J
        assert F(str(cfg['plant']['gravity_m_s2'])) == T
        assert cfg['sensing']['position_period_ticks'] == 5
        assert cfg['sensing']['max_consecutive_missed_packets'] == 2
        assert F(str(cfg['sensing']['observed_noise_halfwidth']['px'])) == EPS_P
        assert cfg['sensing']['always_observed_indices'] == [4, 5]
        assert cfg['sensing']['position_indices'] == [0, 1]
        assert cfg['domain']['state_lower'][0] == -5
        assert cfg['domain']['state_upper'][0] == 5
        assert cfg['domain']['state_lower'][2] == -3
        assert cfg['domain']['state_upper'][2] == 3
    plus, minus = family(7)
    assert check_legal(plus) and check_legal(minus)
    assert plus[START] == minus[START] == (F(0),)*4
    assert all(plus[k][2:] == minus[k][2:] == (F(0),F(0)) for k in plus)
    # Packet history: tick45 success y=0, ticks50 and55 missed, tick60 success y=0.
    # At tick60 each path uses its own legal noise e=-p60.
    assert abs(plus[END][0]) <= EPS_P and abs(minus[END][0]) <= EPS_P
    assert plus[END][0] == -minus[END][0]
    assert plus[END][1] == -minus[END][1]
    assert plus[END][0] == H*H*R*F(7*6,2)
    assert plus[END][1] == 7*H*R
    # An alternative pair with +/-R for all 15 ticks is separated by the forced packet.
    extremal_plus, extremal_minus = family(15)
    assert check_legal(extremal_plus) and check_legal(extremal_minus)
    sep15 = extremal_plus[END][0]-extremal_minus[END][0]
    assert sep15 > 2*EPS_P
    # j=8 is not compatible with a common zero reading in this restricted consecutive-burst family.
    plus8, minus8 = family(8)
    assert abs(plus8[END][0]) > EPS_P
    assert plus8[END][0]-minus8[END][0] > 2*EPS_P
    return {
        'run': 270,
        'scope': 'specific legal tick45..60 zero-torque, zero-angular-reading observation fiber; not all Run260 tick45 posteriors',
        'model': 'Run260 frozen four-state defined-discrete Euler; fixed T=9.81N, tau=0',
        'packets': 'tick45 success y=0; tick50/55 miss; tick60 forced success y=0; angular measurements zero at every tick',
        'last_seven_disturbance_ticks': list(range(53,60)),
        'post_success_plus_state': [str(z) for z in plus[END]],
        'post_success_minus_state': [str(z) for z in minus[END]],
        'post_success_noise_plus': str(-plus[END][0]),
        'post_success_noise_minus': str(-minus[END][0]),
        'post_success_velocity_diameter_floor': str(plus[END][1]-minus[END][1]),
        'post_success_position_diameter': str(plus[END][0]-minus[END][0]),
        'full_extreme_position_separation_tick60': str(sep15),
        'max_common_reading_position_separation': str(2*EPS_P),
        'full_extreme_min_measurement_gap': str(sep15-2*EPS_P),
        'restricted_last_8_burst_position_separation': str(plus8[END][0]-minus8[END][0]),
        'proof': 'Exact Euler recurrence with phi=omega=tau=0. Symmetric +/-R on last j ticks yields p60=+/-h^2*R*j*(j-1)/2 and v60=+/-j*h*R. For j=7, |p60|<=eps_p and both histories yield y60=0 with distinct legal noise. Earlier angular observations coincide and position packets at 50/55 are absent. Thus any guaranteed posterior for this fiber includes both v60 values. For j=15, |delta p60|>2 eps_p so the two extreme histories cannot share a successful position reading.',
        'evidence': 'exact Fraction construction plus per-tick physical-hard-box checks',
        'not_certified': ['membership of both trajectories in actual Run260 tick45 posterior', 'all-fiber lower bound', 'optimal lower bound over all disturbances', 'exact SMF/CZ posterior', '15-tick causal return', 'MPC solver', 'infinite recursive feasibility', 'six-state safety', '20ms WCET'],
        'gate_A': 'blocked',
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--root', type=Path)
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    result = json.dumps(certificate(a.root), indent=2, sort_keys=True) + '\n'
    if a.output:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(result)
    else:
        print(result, end='')

if __name__ == '__main__':
    main()
