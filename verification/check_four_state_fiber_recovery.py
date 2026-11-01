#!/usr/bin/env python3
"""Run238: exact finite-horizon shared-information backup from Run236/237 fiber.

This is a 15-tick robust reachable zonotope, not an invariant terminal set,
not an SMF-MPC controller, and not a result for the whole initial prior.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

Z, O = F(0), F(1)
H, T, J = F(1, 50), F(981, 100), F(1, 50)
R = F(47, 25) + F(243, 16000) * T
D = R + T * F(9, 20) ** 3 / 6
GAP = 15
STATE_LIMITS = (F(5), F(3), F(9, 20), F(2))
TAU_MAX = F(2, 25)


def generators(n: int):
    """Exact convex hull of reachable x_n from x±=(0,±hD,0,0).

    Each r_k is independent in [-R,R]; the two initial states are convexified.
    State order (p,v,phi,omega); fixed T=9.81, common tau=0.
    """
    if n < 0:
        raise ValueError('negative tick')
    initial = (n * H * H * D, H * D, Z, Z)
    disturbances = [(H * H * R * (n - 1 - j), H * R, Z, Z)
                    for j in range(n)]
    return [initial] + disturbances


def dot(a, b):
    return sum((x * y for x, y in zip(a, b)), Z)


def support(n: int, direction):
    return sum((abs(dot(direction, g)) for g in generators(n)), Z)


def advance_zero_torque(g):
    p, v, phi, omega = g
    return (p + H * v, v, phi + H * omega, omega)


def verify(root=None):
    if root is not None:
        cfg = json.loads((Path(root) / 'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics'] == 'defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s'])) == H
        assert F(str(cfg['plant']['inertia_kg_m2'])) == J
        assert cfg['sensing']['position_period_ticks'] == 5
        assert cfg['sensing']['max_consecutive_missed_packets'] == 2
        assert cfg['sensing']['position_indices'] == [0, 1]
        assert cfg['sensing']['always_observed_indices'] == [4, 5]
        assert tuple(F(str(cfg['domain']['state_upper'][i])) for i in (0, 2, 4, 5)) == STATE_LIMITS
        assert F(str(cfg['domain']['input_lower'][0])) <= T <= F(str(cfg['domain']['input_upper'][0]))
        assert F(str(cfg['domain']['input_lower'][1])) <= Z <= F(str(cfg['domain']['input_upper'][1]))
        assert F(str(cfg['initial_set']['halfwidth'][2])) >= H * D
        assert all(F(str(cfg['initial_set']['center'][i])) == Z for i in (0, 2, 4, 5))
    assert H / J == O
    assert H * D < F(1, 10)
    # Exact induction: x_{n+1} = A0 x_n + B r_n, all shared torques zero.
    for n in range(GAP):
        assert [advance_zero_torque(g) for g in generators(n)] + [(Z, H * R, Z, Z)] == generators(n + 1)
    state_bounds = []
    for n in range(GAP + 1):
        bounds = tuple(support(n, tuple(O if i == j else Z for i in range(4))) for j in range(4))
        assert all(bound < limit for bound, limit in zip(bounds, STATE_LIMITS))
        state_bounds.append(bounds)
    assert len(generators(GAP)) == GAP + 1
    assert state_bounds[1][0] == H * H * D
    assert state_bounds[1][1] == H * (D + R)
    assert state_bounds[GAP][0] == GAP * H * H * D + H * H * R * GAP * (GAP - 1) / 2
    assert state_bounds[GAP][1] == H * D + GAP * H * R
    # Constructive limitation: with initial +hD and r=+R each tick, zero-torque
    # backup inevitably violates the speed constraint by tick 73.
    first_bad = next(n for n in range(1, 200) if H * D + n * H * R > STATE_LIMITS[1])
    assert first_bad == 73
    assert H * D + (first_bad - 1) * H * R <= STATE_LIMITS[1]
    return {
        'run': 238,
        'evidence': 'EXACT_RATIONAL_FINITE_HORIZON_SHARED_INFORMATION_BACKUP',
        'scope': 'Run236 two-state fiber only, fixed-thrust frozen four-state Euler, 15 ticks',
        'initial_fiber': ['(0,+hD,0,0)', '(0,-hD,0,0)'],
        'common_causal_policy': 'T=981/100 N, tau=0 Nm; ignores all measurements',
        'disturbance': f'r_k in [-{R},+{R}] independently each tick',
        'h': str(H), 'R': str(R), 'D': str(D),
        'zonotope_generators_at_tick_15': len(generators(GAP)),
        'exact_one_step_position_halfwidth': str(state_bounds[1][0]),
        'exact_one_step_velocity_halfwidth': str(state_bounds[1][1]),
        'exact_15_step_position_halfwidth': str(state_bounds[GAP][0]),
        'exact_15_step_velocity_halfwidth': str(state_bounds[GAP][1]),
        'max_observation_gap_ticks': GAP,
        'all_0_to_15_state_and_input_hard_constraints_certified': True,
        'zero_torque_backup_first_speed_violation_tick_under_positive_adversary': first_bad,
        'terminal_invariance_certified': False,
        'full_prior_certified': False,
        'smf_mpc_recursive_feasibility_certified': False,
        'limitations': [
            'Not a robust invariant set or a recursive output-feedback terminal policy',
            'Only the specified Run236 two-point fiber, not the full initial prior or arbitrary posterior',
            'No use of noisy measurements or measurement updates; does not implement MPC',
            '15 ticks of finite safety do not permit indefinite repetition without a new certified recovery step',
            'No six-state dynamics, stability or real-time worst-case timing certification'
        ],
        'gate_A': 'blocked_for_output_feedback_SMF_MPC'
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--root', type=Path)
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    s = json.dumps(verify(a.root), sort_keys=True, ensure_ascii=False, indent=2) + '\n'
    if a.output:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(s)
    else:
        print(s, end='')


if __name__ == '__main__':
    main()
