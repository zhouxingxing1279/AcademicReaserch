#!/usr/bin/env python3
"""Run277: exact shared-open-loop impossibility for one TRUE Run271 MMS posterior fiber.

This is a velocity-diameter necessary obstruction, NOT a closed-loop impossibility
or a proof of unsafe physical flight. It applies to the frozen four-state Euler
benchmark only. All numerical certificates use fractions.Fraction.
"""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

H = F(1, 50)
R = F(3246383, 1600000)
VMAX = F(3)
PLUS_V60 = F(22724681, 80000000)
MINUS_V60 = -PLUS_V60
DELTA0 = PLUS_V60 - MINUS_V60


def velocity_diameter(n):
    """Two worlds share the same torque and thrust; r+=+R, r-=-R."""
    if not isinstance(n, int) or n < 0:
        raise ValueError('nonnegative integer tick horizon required')
    return DELTA0 + 2 * H * R * n


def first_impossible_horizon():
    # Require diameter > 2*VMAX, strict. Integer division is exact.
    slope = 2 * H * R
    q = (2 * VMAX - DELTA0) / slope
    return q.numerator // q.denominator + 1


def verify(root=None):
    n = first_impossible_horizon()
    assert n == 67
    assert velocity_diameter(n-1) <= 2*VMAX < velocity_diameter(n)
    assert DELTA0 == F(22724681, 40000000)
    if root is not None:
        root = Path(root)
        prior = json.loads((root / 'results/run271_run260_membership_20261102/checks.json').read_text())
        assert prior['run260_membership'].startswith('constructive consistent true trajectories')
        xp = list(map(F, prior['tick60_plus_state']))
        xm = list(map(F, prior['tick60_minus_state']))
        assert xp[1] == PLUS_V60 and xm[1] == MINUS_V60
        assert xp[2:] == xm[2:] == [F(0),F(0)]
        assert prior['packet_history_ticks_5_to_60'] == 'SSSMMSMMSMMS'
        cfg = json.loads((root / 'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics'] == 'defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s'])) == H
        assert F(str(cfg['plant']['gravity_m_s2'])) == F(981,100)
        assert F(str(cfg['domain']['state_upper'][2])) == VMAX
        assert F(str(cfg['domain']['state_lower'][2])) == -VMAX
        assert cfg['sensing']['position_period_ticks'] == 5
        assert cfg['sensing']['max_consecutive_missed_packets'] == 2
    return {
        'run': 277,
        'model': 'frozen discrete four-state Euler, shared thrust and torque, independent |r|<=R',
        'parent': 'Run271 genuine common-observation MMS posterior pair at tick60',
        'parent_packet_history_5_to_60': 'SSSMMSMMSMMS',
        'initial_velocity_plus': str(PLUS_V60),
        'initial_velocity_minus': str(MINUS_V60),
        'initial_velocity_diameter': str(DELTA0),
        'sample_period_s': str(H),
        'disturbance_halfwidth_m_s2': str(R),
        'velocity_hard_limit_abs_m_s': str(VMAX),
        'strict_first_obstruction_horizon_ticks': n,
        'strict_first_obstruction_tick': 60+n,
        'diameter_at_66': str(velocity_diameter(66)),
        'diameter_at_67': str(velocity_diameter(67)),
        'excess_over_hard_box_diameter_at_67': str(velocity_diameter(67)-2*VMAX),
        'duration_s': str(n*H),
        'proof': 'For any common open-loop torque and thrust schedule, equal initial (phi,omega) imply equal future angles; subtracting v+ = v + h*(-T*sin(phi)+r) gives Delta v(n)=Delta v(0)+2*n*h*R for r+=R,r-=-R. Since both speeds cannot lie in [-3,3] if Delta v>6, at least one world violates a hard constraint no later than tick127. If angle/input constraints fail earlier, policy already fails.',
        'legal_future_packet_branch': 'all position opportunities success, with each world using its own legal noise=0 reading; policy ignores these readings',
        'quantifiers': 'forall shared observation-independent torque sequences, exists one of two true initial states and bounded disturbance sequences causing hard-box failure by tick127',
        'does_not_prove': ['failure of causal observation-conditioned feedback','impossibility of robust MPC','exact full posterior','failure at tick126','terminal information RCI','six-state physical safety','20ms WCET'],
        'gate_A': 'blocked'
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root',type=Path)
    ap.add_argument('--output',type=Path)
    args = ap.parse_args()
    s=json.dumps(verify(args.root),sort_keys=True,indent=2,ensure_ascii=False)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(s)
    else:
        print(s,end='')

if __name__=='__main__':
    main()
