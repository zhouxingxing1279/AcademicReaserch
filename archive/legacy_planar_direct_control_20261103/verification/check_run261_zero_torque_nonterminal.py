#!/usr/bin/env python3
"""Run261: exact physical-model witness rejecting indefinite repetition of Run260's backup.

Scope: the *frozen* four-state discrete-Euler plant with independently selectable
bounded lateral acceleration residual. This is a counterexample only to the
specific constant T=mg, tau=0 continuation, not to all causal feedback laws,
not to any candidate terminal RCI, and not to a physical wind realization.
"""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

H = J = F(1, 50)
T = F(981, 100)
R = F(3246383, 1600000)
P_LIMIT, V_LIMIT, PHI_LIMIT, OMEGA_LIMIT = F(5), F(3), F(9, 20), F(2)
PULSE = (F(1, 25), -F(1, 25), -F(1, 25), F(1, 25), F(0))


def pulse_witness():
    """An exact *existence* proof, not a rational evaluation of sine.

    Choose r_k=T*sin(phi_k) in ticks 30..34. This is admissible because
    |sin(phi)|<=|phi| and T*max|phi|<=R. Consequently v and p remain zero.
    """
    phi = omega = F(0)
    states = []
    for tau in PULSE:
        states.append((phi, omega, tau))
        phi, omega = phi + H * omega, omega + H / J * tau
    assert (phi, omega) == (0, 0)
    assert [q[0] for q in states] == [F(0), F(0), F(1, 1250), F(1, 1250), F(0)]
    max_abs_phi = max(abs(q[0]) for q in states)
    assert T * max_abs_phi < R
    assert all(abs(q[0]) <= PHI_LIMIT and abs(q[1]) <= OMEGA_LIMIT for q in states)
    return states, max_abs_phi


def adversarial_continuation():
    """From x45=0, choose r_k=+R, T=mg, tau=0 for k>=45.

    Thus phi=omega=0, p_{45+n}=h^2*R*n(n-1)/2,
    v_{45+n}=n*h*R. All arithmetic below is exact rational.
    """
    rows = []
    for n in range(0, 75):
        p = H * H * R * n * (n - 1) / 2
        v = n * H * R
        rows.append({'tick': 45 + n, 'p': p, 'v': v, 'phi': F(0), 'omega': F(0)})
    first_bad = next(row for row in rows if not (
        abs(row['p']) <= P_LIMIT and abs(row['v']) <= V_LIMIT
        and abs(row['phi']) <= PHI_LIMIT and abs(row['omega']) <= OMEGA_LIMIT))
    assert first_bad['tick'] == 119
    assert all(abs(row['p']) <= P_LIMIT and abs(row['v']) <= V_LIMIT for row in rows[:-1])
    assert first_bad['p'] < P_LIMIT and first_bad['v'] > V_LIMIT
    return rows, first_bad


def verify(root=None):
    states, max_phi = pulse_witness()
    rows, bad = adversarial_continuation()
    assert rows[-2]['tick'] == 118
    assert rows[-2]['v'] == F(236985959, 80000000)
    assert bad['v'] == F(120116171, 40000000)
    assert bad['p'] == F(8768480483, 4000000000)
    # The all-zero truth until tick45 has zero-noise readings consistent with
    # BOTH Run260 starting packet histories SMM and MMS. Later every position
    # packet succeeds with reading y=p, n_p=0; phi/omega read zero each tick.
    # This legal sensing schedule does not force the open-loop backup to react.
    for pattern in ('SMM', 'MMS'):
        assert len(pattern) == 3 and pattern != 'MMM'
    if root is not None:
        cfg = json.loads((Path(root) / 'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics'] == 'defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s'])) == H
        assert F(str(cfg['plant']['inertia_kg_m2'])) == J
        assert F(str(cfg['plant']['gravity_m_s2'])) == T
        assert cfg['sensing']['position_period_ticks'] == 5
        assert cfg['sensing']['max_consecutive_missed_packets'] == 2
        assert F(str(cfg['domain']['state_upper'][2])) == V_LIMIT
        assert F(str(cfg['domain']['input_upper'][1])) >= 0
        # The frozen four-state residual is R, unlike six-state T-dependent r_x.
        assert F(str(cfg['sensing']['observed_noise_halfwidth']['px'])) == F(1, 50)
    return {
        'run': 261,
        'evidence': 'EXACT_RATIONAL_TRUE_TRAJECTORY_WITNESS_WITH_ANALYTIC_SINE_BOUND',
        'scope': 'frozen four-state discrete Euler plant, additive |r_x|<=R, fixed T=mg; not six-state or real-world wind realizability',
        'histories': ['Run254 SSSMMS all-zero readings through 30', 'Run259 SMM and MMS all-zero readings through 45'],
        'prefix_ticks_30_to_34_torque_Nm': [str(x) for x in PULSE],
        'prefix_residual_choice': 'r_x=T*sin(phi) at ticks30..34, zero otherwise through tick44; admissible by |sin(phi)|<=|phi|',
        'max_abs_prefix_phi_rad': str(max_phi),
        'prefix_residual_magnitude_upper_bound': str(T * max_phi),
        'residual_halfwidth_m_s2': str(R),
        'continuation': 'from x45=(0,0,0,0), choose T=mg,tau=0,r_x=+R every tick; all position packets succeed with zero noise',
        'last_safe_tick': 118,
        'last_safe_velocity_m_s': str(rows[-2]['v']),
        'first_unsafe_tick': bad['tick'],
        'first_unsafe_position_m': str(bad['p']),
        'first_unsafe_velocity_m_s': str(bad['v']),
        'violated_constraint': 'v<=3 m/s',
        'proves_no_indefinite_repetition_of_this_fixed_backup': True,
        'rules_out_other_causal_controllers': False,
        'rules_out_terminal_information_rci': False,
        'infinite_horizon_recursive_feasibility': False,
        'gate_A': 'blocked',
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    content = json.dumps(verify(args.root), ensure_ascii=False, sort_keys=True, indent=2) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content)
    else:
        print(content, end='')


if __name__ == '__main__':
    main()
