#!/usr/bin/env python3
"""Run244: exact adverse-residual authority obstruction for Run243 pulse family.

The statement is a robust *counterexample* to repeating a fixed, attitude-
resetting 15-tick pulse with 5/10/15 free ticks. It is NOT a no-go theorem
for general output-feedback control or SMF-MPC. All proof comparisons use
fractions; the only transcendental fact used is |sin(x)| <= |x|.
"""
from __future__ import annotations
import argparse
import json
import math
from fractions import Fraction as F
from pathlib import Path

H = J = F(1, 50)
T = F(981, 100)
R = F(47, 25) + F(243, 16000) * T
TAU_MAX = F(2, 25)
V_MAX = F(3)
PACKET_PERIOD = 5
MAX_MISSES = 2
SHAPE = (1,) * 3 + (-1,) * 6 + (1,) * 3 + (0,) * 3
FREE_TICKS = (5, 10, 15)


def attitude_response():
    """Unit-amplitude pulse attitude angles at the beginning of each tick."""
    phi = omega = F(0)
    angles = []
    for s in SHAPE:
        angles.append(phi)
        phi, omega = phi + H * omega, omega + H / J * s
    assert phi == omega == 0
    return tuple(angles)


def per_pulse_correction_bound():
    """Bound |sum_j h*T*sin(u*phi_unit[j])| for |u|<=TAU_MAX."""
    return H * T * TAU_MAX * sum(map(abs, attitude_response()), F(0))


def per_cycle_lower_bound(free_ticks):
    """Lower bound on velocity growth under r_j=+R at every tick."""
    if free_ticks not in FREE_TICKS:
        raise ValueError('unsupported free-tick mode')
    return (len(SHAPE) + free_ticks) * H * R - per_pulse_correction_bound()


def first_certified_violation_cycles(free_ticks):
    d = per_cycle_lower_bound(free_ticks)
    assert d > 0
    return V_MAX // d + 1


def numerical_witness(free_ticks):
    """Sanity-only Euler trajectory with saturated fixed pulse u=+0.08."""
    cycles = first_certified_violation_cycles(free_ticks)
    p = v = phi = omega = 0.0
    first_velocity_violation = None
    tick = 0
    for _ in range(cycles):
        for s in SHAPE + (0,) * free_ticks:
            tick += 1
            p, v, phi, omega = (p + float(H) * v,
                                v + float(H) * (float(R) - float(T) * math.sin(phi)),
                                phi + float(H) * omega,
                                omega + float(TAU_MAX) * s)
            if first_velocity_violation is None and abs(v) > float(V_MAX):
                first_velocity_violation = tick
    assert abs(phi) < 1e-12 and abs(omega) < 1e-12
    return {'ticks': tick, 'first_velocity_violation_tick': first_velocity_violation,
            'final_p_m': p, 'final_v_m_s': v}


def verify(root=None):
    if root is not None:
        cfg = json.loads((Path(root) / 'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics'] == 'defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s'])) == H
        assert F(str(cfg['plant']['inertia_kg_m2'])) == J
        assert F(str(cfg['plant']['gravity_m_s2'])) == T
        assert cfg['sensing']['position_period_ticks'] == PACKET_PERIOD
        assert cfg['sensing']['max_consecutive_missed_packets'] == MAX_MISSES
        assert F(str(cfg['domain']['state_upper'][2])) == V_MAX
        assert F(str(cfg['domain']['state_lower'][2])) == -V_MAX
        assert F(str(cfg['domain']['input_upper'][1])) == TAU_MAX
        assert F(str(cfg['domain']['input_lower'][1])) == -TAU_MAX
    angles = attitude_response()
    assert all(a >= 0 for a in angles)
    assert max(angles) == F(9, 50)
    assert sum(angles) == F(27, 25)
    assert per_pulse_correction_bound() == F(26487, 1562500)
    assert R == F(3246383, 1600000)
    modes = []
    for n in FREE_TICKS:
        N = len(SHAPE) + n
        assert N % PACKET_PERIOD == 0
        d = per_cycle_lower_bound(n)
        cycles = first_certified_violation_cycles(n)
        assert (cycles - 1) * d <= V_MAX < cycles * d
        modes.append({
            'free_ticks': n,
            'selected_packet_gap_ticks': N,
            'cycles_until_guaranteed_velocity_violation_at_latest': cycles,
            'ticks_until_violation_at_latest': N * cycles,
            'per_cycle_velocity_growth_lower_m_s': str(d),
            'velocity_lower_at_end_m_s': str(cycles * d),
            'velocity_constraint_margin_m_s': str(cycles * d - V_MAX),
            'all_packet_opportunities_success': True,
            'selected_packets_are_successful': True,
            'numerical_sanity_only': numerical_witness(n),
        })
    assert [x['cycles_until_guaranteed_velocity_violation_at_latest'] for x in modes] == [4, 4, 3]
    return {
        'run': 244,
        'base_run': 243,
        'evidence': 'EXACT_RATIONAL_ADVERSARIAL_VELOCITY_OBSTRUCTION',
        'scope': 'Fixed T, frozen four-state Euler; repeating 15-tick Run243 pulse shape followed by 5/10/15 zero-torque ticks; |pulse amplitude|<=0.08; known zero initial attitude',
        'initial_state': ['0', '0', '0', '0'],
        'disturbance_witness': 'r_x=+R at every tick; other noises zero; every 5-tick position packet succeeds (controller may ignore intermediate successes)',
        'quantifier': 'forall bounded pulse amplitudes (even full-state or clairvoyant), exists one legal constant positive residual and legal all-success packet history producing |v|>3 by stated tick',
        'proof_inequality': 'v_{k+N} >= v_k + N*H*R - H*T*TAU_MAX*sum(abs(phi_unit_j)); |sin(u*phi_unit_j)|<=|u*phi_unit_j|',
        'pulse_shape': list(SHAPE),
        'unit_pulse_attitude_angles': [str(x) for x in angles],
        'pulse_ticks': len(SHAPE),
        'unit_angle_sum': str(sum(angles)),
        'max_unit_angle': str(max(angles)),
        'max_attitude_abs_rad': str(max(angles) * TAU_MAX),
        'residual_halfwidth_m_s2': str(R),
        'per_pulse_max_velocity_correction_m_s': str(per_pulse_correction_bound()),
        'velocity_limit_m_s': str(V_MAX),
        'modes': modes,
        'all_legal_packet_patterns_robust_safety_for_this_pulse_family': False,
        'general_output_feedback_infeasible': False,
        'smf_mpc_recursive_feasibility_proved': False,
        'gate_A': 'blocked',
        'limitations': [
            'Only the specific attitude-resetting pulse shape with zero-torque free intervals is ruled out, not arbitrary bounded torque sequences',
            'The counterexample is one admissible all-success packet pattern; it suffices to disprove a guarantee quantified over all patterns',
            'The state may violate other constraints earlier; the contradiction assumes safe evolution until the stated velocity bound and proves that assumption false',
            'No general noisy-attitude SMF, MPC optimization, terminal invariant information set, or six-state guarantee is supplied',
        ],
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--root', type=Path)
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    content = json.dumps(verify(a.root), indent=2, ensure_ascii=False, sort_keys=True) + '\n'
    if a.output:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(content)
    else:
        print(content, end='')

if __name__ == '__main__':
    main()
