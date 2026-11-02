#!/usr/bin/env python3
"""Run269: exact indistinguishable disturbance-pair floor before a forced position packet.

Frozen Run260 4-state defined-discrete Euler plant only. No MPC/RCI claim.
"""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

H = F(1, 50)
T = F(981, 100)
J = F(1, 50)
R = F(3246383, 1600000)
TAU_MAX = F(2, 25)
MAX_GAP = 14  # tick45 success; ticks50 and55 missed; tick60 forced success


def difference(q):
    """Exact differences for r_i=+R and r_i=-R, i=0..q-1."""
    if not 0 <= q <= MAX_GAP:
        raise ValueError(q)
    return {'position': H * H * R * q * (q - 1), 'velocity': 2 * H * R * q}


def zero_torque_witness(q, sign):
    """Exact Euler trajectory from x=0, tau=0, r=sign*R."""
    if sign not in (-1, 1):
        raise ValueError(sign)
    p, v, phi, omega = F(0), F(0), F(0), F(0)
    out = [(p, v, phi, omega)]
    for _ in range(q):
        p, v, phi, omega = p + H * v, v + H * sign * R, phi + H * omega, omega
        out.append((p, v, phi, omega))
    return out


def certificate(root=None):
    if root:
        cfg = json.loads((Path(root) / 'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics'] == 'defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s'])) == H
        assert F(str(cfg['plant']['inertia_kg_m2'])) == J
        assert F(str(cfg['plant']['gravity_m_s2'])) == T
        assert cfg['sensing']['position_period_ticks'] == 5
        assert cfg['sensing']['max_consecutive_missed_packets'] == 2
        assert cfg['sensing']['always_observed_indices'] == [4, 5]
        assert cfg['sensing']['position_indices'] == [0, 1]
        assert cfg['domain']['state_lower'][0] == -5
        assert cfg['domain']['state_upper'][0] == 5
        assert cfg['domain']['state_lower'][2] == -3
        assert cfg['domain']['state_upper'][2] == 3
    plus = zero_torque_witness(MAX_GAP, 1)
    minus = zero_torque_witness(MAX_GAP, -1)
    for xp, xm in zip(plus, minus):
        for x in (xp, xm):
            assert abs(x[0]) <= 5 and abs(x[1]) <= 3
            assert abs(x[2]) <= F(45, 100) and abs(x[3]) <= 2
        assert xp[2:] == xm[2:] == (F(0), F(0))
    assert plus[-1][0] - minus[-1][0] == difference(MAX_GAP)['position']
    assert plus[-1][1] - minus[-1][1] == difference(MAX_GAP)['velocity']
    gaps = {str(q): {k: str(v) for k, v in difference(q).items()}
            for q in (1, 4, 5, 9, 10, 14)}
    return {
        'run': 269,
        'model': 'frozen Run260 four-state defined-discrete Euler, T=mg, tau arbitrary shared causal',
        'history': 'tick45 success; ticks50,55 missed; ticks46..59 no position readings; angular outputs every tick',
        'quantifier': 'for any common causal torque policy, two opposite legal lateral-disturbance histories with identical angular observations and no position updates have identical controls; any safe posterior covering both has at least the listed projection diameters',
        'q14_position_difference': str(difference(14)['position']),
        'q14_velocity_difference': str(difference(14)['velocity']),
        'q14_plus_state': [str(z) for z in plus[-1]],
        'q14_minus_state': [str(z) for z in minus[-1]],
        'gaps': gaps,
        'proof': 'Euler p_next=p+h*v, v_next=v+h*(-T*sin(phi)+r), phi_next=phi+h*omega, omega_next=omega+h*tau/J. Same angular observations imply identical tau,phi,omega. Subtract +/-R trajectories: Delta v_q=2qhR, Delta p_q=q(q-1)h^2 R. No position packets at 50,55; angular observations equal.',
        'scope': 'necessary information-width floor for a specific nonempty observation fiber before tick60 success, not a terminal RCI, not a bound after tick60 measurement, not six-state',
        'gate_A': 'blocked',
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--root', type=Path)
    p.add_argument('--output', type=Path)
    a = p.parse_args()
    s = json.dumps(certificate(a.root), sort_keys=True, indent=2) + '\n'
    if a.output:
        a.output.parent.mkdir(parents=True, exist_ok=True)
        a.output.write_text(s)
    else:
        print(s, end='')


if __name__ == '__main__':
    main()
