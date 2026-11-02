#!/usr/bin/env python3
"""Run265: exact necessary three-step speed guard for frozen four-state Euler plant.

Only a necessary robust viability filter, not an RCI, MPC, or SMF controller.
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
V = F(3)


def certificate(root=None):
    # phi0=omega0=0; r_i=+R or -R for i=0,1,2.
    # For any admissible causal tau sequence, phi1=0, phi2=H^2*tau0/J.
    # sin(phi2) <= H^2*U/J, sin(phi2) >= -H^2*U/J.
    min_outward_increment = 3*H*R - H*T*(H*H*U/J)
    safe_positive_start_cap = V-min_outward_increment
    safe_negative_start_floor = -V+min_outward_increment
    unsafe_positive_start = F(29, 10)  # 2.9 m/s
    unsafe_negative_start = -unsafe_positive_start
    assert min_outward_increment == F(48570177, 400000000)
    assert safe_positive_start_cap == F(1151429823, 400000000)
    assert unsafe_positive_start > safe_positive_start_cap
    assert unsafe_negative_start < safe_negative_start_floor
    # Under +R the first two velocity steps are independent of torque.
    v1 = unsafe_positive_start + H*R
    v2 = unsafe_positive_start + 2*H*R
    v3_lower = unsafe_positive_start + min_outward_increment
    assert v1 < V and v2 < V and v3_lower > V
    # p3 does not depend on tau because the first two accelerations do not.
    p3 = 3*H*unsafe_positive_start + 3*H*H*R
    assert p3 < F(5)
    assert 3*H*U/J < F(2)
    assert 3*H*H*U/J < F(9,20)
    if root is not None:
        cfg = json.loads((Path(root)/'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics'] == 'defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s'])) == H
        assert F(str(cfg['plant']['inertia_kg_m2'])) == J
        assert F(str(cfg['plant']['gravity_m_s2'])) == T
        assert F(str(cfg['domain']['input_upper'][1])) == U
        assert F(str(cfg['domain']['input_lower'][1])) == -U
    return {
        'run': 265,
        'scope': 'frozen_4state_Euler_T9.81_phi0_omega0_zero_only',
        'hard_speed_limit_m_s': str(V),
        'three_tick_outward_speed_increment_lower_m_s': str(min_outward_increment),
        'necessary_v0_interval_at_zero_attitude_m_s': [str(safe_negative_start_floor), str(safe_positive_start_cap)],
        'positive_adversarial_initial_v0_m_s': str(unsafe_positive_start),
        'positive_adversarial_v1_m_s': str(v1),
        'positive_adversarial_v2_m_s': str(v2),
        'positive_adversarial_v3_strict_lower_m_s': str(v3_lower),
        'positive_adversarial_p3_m': str(p3),
        'negative_case': 'sign_symmetric_r=-R_v0=-2.9; all causal torques fail |v3|<=3',
        'quantifiers': 'forall causal admissible tau0,tau1,tau2; exists legal r0=r1=r2=sign(v0)*R',
        'information_fiber_implication': 'any posterior containing (p=0,v=+/-2.9,phi=0,omega=0) is not 3-step robust viable; small velocity width alone is insufficient',
        'does_not_assert': ['these states occur in Run260 tick60 posterior', 'all Run264 tick75 posteriors are unsafe', 'terminal information RCI nonexistent', 'MPC/SMF closed loop implemented'],
        'gate_A': 'blocked',
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    content = json.dumps(certificate(args.root), sort_keys=True, indent=2, ensure_ascii=False)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content)
    else:
        print(content, end='')


if __name__ == '__main__':
    main()
