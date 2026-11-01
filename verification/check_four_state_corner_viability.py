#!/usr/bin/env python3
"""Run248: exact early full-information nonviability witness for Run245 prefix.

The certificate applies to one real initial-box corner and r=-R. It is a
necessary viability obstruction, not an SMF posterior or MPC controller.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

import check_four_state_early_viability_guard as prior

H, T, R, U = prior.H, prior.T, prior.R, prior.U
PHI_MAX, V_MAX = prior.PHI_MAX, prior.V_MAX
INITIAL = (F(-1, 50), F(-1, 10), F(1, 200), F(1, 100))
PREFIX = prior.TORQUES
HORIZON = 30


def reachable_corner():
    """Sound rational enclosures for a single physical corner and fixed r=-R."""
    p = (INITIAL[0], INITIAL[0])
    v = (INITIAL[1], INITIAL[1])
    phi, omega = INITIAL[2:]
    rows = [(p, v, phi, omega)]
    for tau in PREFIX:
        low, high = prior.sin_bounds(phi)
        p_new = (p[0] + H*v[0], p[1] + H*v[1])
        v_new = (v[0] - H*(R + T*high), v[1] - H*(R + T*low))
        phi, omega = phi + H*omega, omega + (H/prior.J)*tau
        p, v = p_new, v_new
        rows.append((p, v, phi, omega))
    return rows


def extremal_pitch(phi, omega, j):
    """Lower pitch bound for arbitrary |tau|<=U, exact Euler timing."""
    return phi + H*j*omega - H*(H/prior.J)*U*F(j*(j-1), 2)


def full_information_negative_witness(rows, k, n):
    """Upper bound on v_(k+n) under r=-R, all admissible future torques.

    Any future trajectory violating angle limits is already unsafe. Otherwise
    sin is monotone on [-0.45,0.45] and phi_(k+j)>=extremal_pitch.
    """
    p, v, phi, omega = rows[k]
    angles = [extremal_pitch(phi, omega, j) for j in range(n)]
    assert all(-PHI_MAX <= a <= PHI_MAX for a in angles)
    upper = v[1] - H*sum((R + T*prior.sin_bounds(a)[0] for a in angles), F(0))
    return upper, min(angles), max(angles)


def first_rejection(rows, max_horizon=HORIZON):
    """Finite guard scan only, NOT earliest physical loss of viability."""
    for k, (_, v, phi, omega) in enumerate(rows):
        for n in range(1, max_horizon+1):
            guard = prior.necessary_velocity_guard(phi, omega, n)
            if guard is not None and v[1] < guard[0]:
                return k, n, guard[0] - v[1]
    return None


def verify(root=None):
    if root is not None:
        cfg = json.loads((Path(root)/'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics'] == 'defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s'])) == H
        assert F(str(cfg['plant']['inertia_kg_m2'])) == prior.J
        assert F(str(cfg['plant']['gravity_m_s2'])) == T
        assert F(str(cfg['domain']['input_upper'][1])) == U
        assert F(str(cfg['domain']['state_upper'][2])) == V_MAX
        assert F(str(cfg['domain']['state_upper'][4])) == PHI_MAX
        assert cfg['sensing']['position_period_ticks'] == 5
        assert cfg['sensing']['max_consecutive_missed_packets'] == 2
        for val, idx in zip(INITIAL, (0, 2, 4, 5)):
            center = F(str(cfg['initial_set']['center'][idx]))
            half = F(str(cfg['initial_set']['halfwidth'][idx]))
            assert val in (center-half, center+half)
    rows = reachable_corner()
    assert len(rows) == 31
    for p, v, phi, omega in rows:
        assert max(map(abs, p)) < prior.P_MAX
        assert max(map(abs, v)) < V_MAX
        assert abs(phi) < PHI_MAX and abs(omega) < prior.OMEGA_MAX
    rejection = first_rejection(rows)
    assert rejection is not None
    k, n, guard_margin = rejection
    assert (k, n) == (14, 30)
    upper, min_phi, max_phi = full_information_negative_witness(rows, k, n)
    assert upper < -V_MAX
    assert guard_margin > 0
    assert all(first_rejection(rows[:j+1]) is None for j in range(k))
    _, v, phi, omega = rows[k]
    floor, ceiling = prior.necessary_velocity_guard(phi, omega, n)
    assert v[1] < floor and upper == v[1] - (floor + V_MAX)
    return {
        'run': 248,
        'base_run': 247,
        'evidence': 'EXACT_RATIONAL_FULL_INFORMATION_EARLY_NONVIABILITY_WITNESS',
        'model': 'frozen four-state explicit Euler, fixed T=9.81, |tau|<=0.08, |r|<=R',
        'initial_true_corner': list(map(str, INITIAL)),
        'adverse_disturbance': 'r=-R every tick',
        'prefix_control': 'Run245 +U*12,-U*12,0*6',
        'first_rejection_within_prefix_and_horizon_le_30': k,
        'future_horizon_ticks': n,
        'unavoidable_velocity_violation_by_tick': k+n,
        'tick14_velocity_enclosure': list(map(str, v)),
        'tick14_phi_exact': str(phi),
        'tick14_omega_exact': str(omega),
        'future_extremal_pitch_min': str(min_phi),
        'future_extremal_pitch_max': str(max_phi),
        'tick14_necessary_velocity_floor': str(floor),
        'tick14_necessary_velocity_ceiling': str(ceiling),
        'strict_negative_violation_margin_m_s': str(-V_MAX-upper),
        'rigorous_upper_velocity_at_tick44': str(upper),
        'packet_observations_cannot_rescue_after_tick14_even_with_full_state': True,
        'earliest_true_nonviability_time_proved': False,
        'smf_posterior_tested': False,
        'shared_causal_feedback_synthesized': False,
        'mpc_optimization_implemented': False,
        'recursive_feasibility_proved': False,
        'gate_A': 'blocked',
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = json.dumps(verify(args.root), indent=2, ensure_ascii=False, sort_keys=True)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result)
    else:
        print(result, end='')

if __name__ == '__main__':
    main()
