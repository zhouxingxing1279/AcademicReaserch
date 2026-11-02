#!/usr/bin/env python3
"""Run272: exact conditional recurrent hidden-velocity aliasing, not terminal RCI."""
from fractions import Fraction as F
import argparse
import json
from pathlib import Path

H = F(1, 50)
R = F(3246383, 1600000)
EPS = F(1, 50)
P60 = H*H*R*21
V60 = 7*H*R


def paired_future(q, opposite=True):
    """Symmetric pair after q ticks, zero torque and angle, ±R or ∓R."""
    assert 0 <= q <= 15
    sign = -1 if opposite else 1
    p = P60 + q*H*V60 + sign*H*H*R*q*(q-1)/2
    v = V60 + sign*q*H*R
    return (p, v, F(0), F(0)), (-p, -v, F(0), F(0))


def min_position_separation(q):
    """Minimum delta p for all independent disturbances under common torque."""
    assert 0 <= q <= 15
    return 2*P60 + q*H*(2*V60) - H*H*R*q*(q-1)


def certify(root=None):
    if root:
        cfg = json.loads((Path(root)/'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics'] == 'defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s'])) == H
        assert F(str(cfg['plant']['gravity_m_s2'])) == F(981, 100)
        assert F(str(cfg['plant']['inertia_kg_m2'])) == H
        assert F(str(cfg['sensing']['observed_noise_halfwidth']['px'])) == EPS
        assert cfg['sensing']['position_period_ticks'] == 5
        assert cfg['sensing']['max_consecutive_missed_packets'] == 2
        old = json.loads((Path(root)/'results/run271_run260_membership_20261102/checks.json').read_text())
        assert old['tick60_plus_state'] == [str(P60), str(V60), '0', '0']
        assert old['tick60_minus_state'] == [str(-P60), str(-V60), '0', '0']
    # All 16 true states along the opposite-extreme continuation are hard-safe.
    for q in range(16):
        a, b = paired_future(q)
        for p, v, phi, omega in (a, b):
            assert abs(p) <= 5 and abs(v) <= 3
            assert abs(phi) <= F(9, 20) and abs(omega) <= 2
    # Every disturbance continuation from either tick60 witness under tau=0
    # is safe over 15 ticks, using monotone absolute-value outer bounds.
    worst_p = P60 + 15*H*V60 + H*H*R*105
    worst_v = V60 + 15*H*R
    assert worst_p < 5 and worst_v < 3
    # If tick65 or tick70 position succeeds, any two trajectories with the
    # same prior angular readings and common torque are separated by >2eps.
    assert min_position_separation(5) > 2*EPS
    assert min_position_separation(10) > 2*EPS
    # But if 65/70 miss, the forced tick75 success can alias both again.
    assert min_position_separation(15) == 2*P60 < 2*EPS
    a75, b75 = paired_future(15)
    assert a75[0] == P60 and b75[0] == -P60
    assert a75[1] == -8*H*R and b75[1] == 8*H*R
    assert abs(a75[0]) <= EPS and abs(b75[0]) <= EPS
    return {
        'run': 272,
        'base_history': 'Run271 actual Run260 MMS->MMS tick60 zero reading pair',
        'tick60_plus': [str(x) for x in paired_future(0)[0]],
        'tick60_minus': [str(x) for x in paired_future(0)[1]],
        'future_packets': {'65': 'miss', '70': 'miss', '75': 'success y=0'},
        'future_control': 'tau=0, fixed T=9.81N; identical angular observations',
        'future_disturbances': 'plus=-R, minus=+R at ticks60..74',
        'tick75_plus': [str(x) for x in a75],
        'tick75_minus': [str(x) for x in b75],
        'tick75_noise_plus': str(-a75[0]),
        'tick75_noise_minus': str(-b75[0]),
        'velocity_diameter_tick60': str(2*V60),
        'velocity_diameter_tick75': str(b75[1]-a75[1]),
        'position_separation_lower_bound_if_success_65': str(min_position_separation(5)),
        'position_separation_lower_bound_if_success_70': str(min_position_separation(10)),
        'position_separation_tick75_witness': str(a75[0]-b75[0]),
        'common_success_max_position_separation': str(2*EPS),
        'all_true_states_hard_safe_60_to_75': True,
        'all_future_disturbances_safe_for_two_initial_states_tau_zero': True,
        'all_future_disturbances_abs_p_bound': str(worst_p),
        'all_future_disturbances_abs_v_bound': str(worst_v),
        'quantifier': 'specific true tick60 pair and common tau=0; all future disturbances hard-safe, one future opposite-extreme disturbance pair aliases at tick75; not all Run260 posterior fibers or causal policies',
        'not_certified': ['complete Run260 tick60 posterior', '15-tick return to terminal information set', 'invariant information state', 'MPC optimization', 'infinite recursive feasibility', 'six-state safety', '20ms WCET'],
        'gate_A': 'blocked',
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--root', type=Path)
    p.add_argument('--output', type=Path)
    args = p.parse_args()
    out = json.dumps(certify(args.root), indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(out)
    else:
        print(out, end='')


if __name__ == '__main__':
    main()
