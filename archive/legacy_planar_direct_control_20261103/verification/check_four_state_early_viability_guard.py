#!/usr/bin/env python3
"""Run247: exact two-sided necessary velocity viability guard and early no-return witness.

NOT a sufficient safety filter, SMF posterior test, or recursive MPC certificate.
All comparisons are Fraction arithmetic with alternating Taylor sine enclosures.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

H = J = F(1, 50)
T, R, U = F(981, 100), F(3246383, 1600000), F(2, 25)
P_MAX, V_MAX, PHI_MAX, OMEGA_MAX = F(5), F(3), F(45, 100), F(2)
INITIAL = (F(-1, 50), F(-1, 10), F(-1, 200), F(-1, 100))
TORQUES = (U,) * 12 + (-U,) * 12 + (F(0),) * 6


def sin_bounds(x: F):
    """Rigorous lower/upper bounds for sin on [-0.45, 0.45]."""
    assert abs(x) <= PHI_MAX
    if x < 0:
        low, high = sin_bounds(-x)
        return -high, -low
    low = x - x**3 / 6
    return low, low + x**5 / 120


def reachable_corner():
    """One true Run245 initial corner and r=-R, with enclosed p/v."""
    p = (INITIAL[0], INITIAL[0])
    v = (INITIAL[1], INITIAL[1])
    phi, omega = INITIAL[2:]
    rows = [(p, v, phi, omega)]
    for tau in TORQUES:
        low, high = sin_bounds(phi)
        p_next = (p[0] + H * v[0], p[1] + H * v[1])
        v_next = (v[0] - H * (R + T * high),
                  v[1] - H * (R + T * low))
        phi, omega = phi + H * omega, omega + (H / J) * tau
        p, v = p_next, v_next
        rows.append((p, v, phi, omega))
    return rows


def pitch_envelope(phi: F, omega: F, j: int):
    """Euler phi_{k+j}; torque at k only affects phi_{k+2}."""
    assert j >= 0
    center = phi + H * j * omega
    radius = H * (H / J) * U * F(j * (j - 1), 2)
    return center - radius, center + radius


def necessary_velocity_guard(phi: F, omega: F, horizon: int):
    """Necessary interval [floor,ceiling] for any fully-safe future policy.

    For r=-R, even the most optimistic (maximum) future velocity cannot
    fall below -V_MAX. For r=+R, even the most optimistic (minimum) future
    velocity cannot exceed +V_MAX. Each bound permits arbitrary future
    full-state/noncausal torques and uses safe-angle clipping. Thus it is
    necessary, not sufficient, for robust viability.
    """
    assert horizon >= 1 and abs(phi) <= PHI_MAX and abs(omega) <= OMEGA_MAX
    minus_accum = plus_accum = F(0)
    for j in range(horizon):
        low, high = pitch_envelope(phi, omega, j)
        low, high = max(low, -PHI_MAX), min(high, PHI_MAX)
        if low > high:
            return None  # No trajectory could respect the angle hard limit.
        minus_accum += H * (R + T * sin_bounds(low)[0])
        plus_accum += H * (R - T * sin_bounds(high)[1])
    return -V_MAX + minus_accum, V_MAX - plus_accum


def first_rejection(rows, max_horizon=30):
    """Search only this witness prefix and finite tested horizons.

    A non-rejection does NOT imply viability; no other trajectories are
    classified and no completeness claim is made.
    """
    for k, (_, v, phi, omega) in enumerate(rows):
        for n in range(1, max_horizon + 1):
            guard = necessary_velocity_guard(phi, omega, n)
            if guard is None:
                continue
            floor, ceiling = guard
            if v[1] < floor:
                return k, n, 'negative', floor - v[1]
            if v[0] > ceiling:
                return k, n, 'positive', v[0] - ceiling
    return None


def verify(root=None):
    if root is not None:
        cfg = json.loads((Path(root) / 'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics'] == 'defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s'])) == H
        assert F(str(cfg['plant']['inertia_kg_m2'])) == J
        assert F(str(cfg['plant']['gravity_m_s2'])) == T
        assert F(str(cfg['domain']['input_upper'][1])) == U
        assert F(str(cfg['domain']['state_upper'][2])) == V_MAX
        assert F(str(cfg['domain']['state_upper'][4])) == PHI_MAX
        assert cfg['sensing']['position_period_ticks'] == 5
        assert cfg['sensing']['max_consecutive_missed_packets'] == 2
        assert cfg['sensing']['always_observed_indices'] == [4, 5]
        assert cfg['sensing']['position_indices'] == [0, 1]
        for val, idx in zip(INITIAL, (0, 2, 4, 5)):
            center = F(str(cfg['initial_set']['center'][idx]))
            half = F(str(cfg['initial_set']['halfwidth'][idx]))
            assert val == center - half
        assert R == F(47, 25) + F(243, 16000) * T
        import check_four_state_terminal_nonviability as previous
        assert previous.reachable_corner() == reachable_corner()
    rows = reachable_corner()
    assert len(rows) == 31
    for p, v, phi, omega in rows:
        assert max(abs(p[0]), abs(p[1])) < P_MAX
        assert max(abs(v[0]), abs(v[1])) < V_MAX
        assert abs(phi) < PHI_MAX and abs(omega) < OMEGA_MAX
    assert pitch_envelope(F(0), F(0), 1) == (F(0), F(0))
    first = first_rejection(rows)
    assert first is not None
    k, n, side, margin = first
    assert (k, n, side) == (26, 20, 'negative') and margin > 0
    _, v, phi, omega = rows[k]
    floor, ceiling = necessary_velocity_guard(phi, omega, n)
    assert v[1] < floor and v[0] < ceiling
    assert all(first_rejection(rows[:i + 1]) is None for i in range(k))
    assert necessary_velocity_guard(F(0), F(0), 13)[0] < 0
    return {
        'run': 247,
        'base_run': 246,
        'evidence': 'EXACT_RATIONAL_TWO_SIDED_NECESSARY_VIABILITY_GUARD',
        'model': 'frozen 4-state Euler, fixed T, |tau|<=U, |r|<=R',
        'initial_corner': list(map(str, INITIAL)),
        'prefix_control': 'Run245 +U*12, -U*12, zero*6',
        'adverse_prefix_and_future_disturbance': 'r=-R every tick',
        'earliest_rejected_prefix_tick_within_30_tick_guard_scan': k,
        'future_horizon_ticks': n,
        'unavoidable_violation_by_tick': k + n,
        'tick26_phi_exact': str(phi),
        'tick26_omega_exact': str(omega),
        'tick26_velocity_enclosure': list(map(str, v)),
        'necessary_velocity_floor_at_tick26': str(floor),
        'necessary_velocity_ceiling_at_tick26': str(ceiling),
        'strict_negative_violation_margin_m_s': str(margin),
        'strict_velocity_upper_bound_at_tick46': str(v[1] - (floor + V_MAX)),
        'hover_13tick_necessary_velocity_interval': list(map(str, necessary_velocity_guard(F(0), F(0), 13))),
        'no_rejection_before_tick26_under_this_finite_guard_scan': True,
        'no_rejection_implies_viability': False,
        'guard_is_sufficient_for_viability': False,
        'guard_on_outer_SMF_can_prove_true_posterior_infeasible': False,
        'shared_causal_feedback_synthesized': False,
        'recursive_feasibility_proved': False,
        'gate_A': 'blocked',
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    content = json.dumps(verify(args.root), ensure_ascii=False, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content)
    else:
        print(content, end='')

if __name__ == '__main__':
    main()
