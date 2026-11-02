#!/usr/bin/env python3
"""Run262: exact three-tick lateral acceleration/torque authority obstruction.

Frozen Run261 four-state Euler plant, constant T=mg. This is a necessary
condition for any terminal state family, NOT a terminal RCI or an MPC design.
"""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

H = F(1, 50)
J = F(1, 50)
T = F(981, 100)
U = F(2, 25)
R = F(3246383, 1600000)


def certificate(root=None):
    # phi0=omega0=v0=0, and r0=r1=r2=+R. For any causal
    # |tau_i|<=U, phi1=0, phi2=(H*H/J)*tau0, independent of tau1,2.
    # v3=3*H*R-H*T*sin(phi2), and sin(phi2)<=abs(phi2).
    phi2_abs_cap = H * H * U / J
    first_two_velocity = 2 * H * R
    worst_case_lower_v3 = 3 * H * R - H * T * phi2_abs_cap
    width_floor_3 = 2 * worst_case_lower_v3
    assert phi2_abs_cap == F(1, 625)
    assert worst_case_lower_v3 == F(48570177, 400000000)
    assert worst_case_lower_v3 > F(3, 25)
    assert first_two_velocity == F(3246383, 40000000)
    p3 = 3 * H * H * R
    assert p3 < 5
    assert 3 * H * U / J < 2
    assert 3 * H * H * U / J < F(9, 20)
    if root is not None:
        cfg = json.loads((Path(root) / 'configs/planar_baseline.json').read_text())
        assert F(str(cfg['plant']['dt_s'])) == H
        assert F(str(cfg['plant']['inertia_kg_m2'])) == J
        assert F(str(cfg['plant']['gravity_m_s2'])) == T
        assert F(str(cfg['domain']['input_upper'][1])) == U
        assert F(str(cfg['domain']['input_lower'][1])) == -U
        assert cfg['plant']['truth_semantics'] == 'defined_discrete_euler'
    return {
        'run': 262,
        'scope': 'frozen_four_state_Euler_constant_T_9.81',
        'starting_true_state': ['0', '0', '0', '0'],
        'adversarial_residual_ticks_0_to_2': str(R),
        'torque_quantifier': 'for_all_causal_tau0_tau1_tau2_in_minusU_plusU',
        'phi2_absolute_upper': str(phi2_abs_cap),
        'v2_exact_under_plusR': str(first_two_velocity),
        'v3_universal_lower_under_plusR': str(worst_case_lower_v3),
        'v3_necessary_symmetric_velocity_span': str(width_floor_3),
        'p3_exact_under_plusR': str(p3),
        'implication': 'Any robust controlled invariant state set containing origin with |v|<=0.12 is impossible for this plant; not a statement about |v|<=3 hard constraint',
        'feedback_and_observation': 'bound holds even with perfect state feedback; tau0 affects v only at third successor tick',
        'closed_loop_controller_implemented': False,
        'terminal_information_RCI_certified': False,
        'gate_A': 'blocked',
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    output = json.dumps(certificate(args.root), indent=2, sort_keys=True, ensure_ascii=False) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output)
    else:
        print(output, end='')


if __name__ == '__main__':
    main()
