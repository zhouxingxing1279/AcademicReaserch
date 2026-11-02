#!/usr/bin/env python3
"""Run266: certified necessary three-step speed guard for tilted 4-state Euler plant.

This is NOT a terminal RCI, a state estimator, or an MPC controller.
Uses rational Taylor remainders to make every numerical rejection sound.
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
P_MAX = F(5)
PHI_MAX = F(9, 20)
OMEGA_MAX = F(2)
DELTA = H*H*U/J


def sin_bounds(x):
    """Rigorous sin(x) bounds: degree-7 Maclaurin + |x|^9/9! remainder."""
    x = F(x)
    p = x - x**3/F(6) + x**5/F(120) - x**7/F(5040)
    err = abs(x)**9/F(362880)
    return p-err, p+err


def necessary_interval(phi, omega):
    """Any three-step robust viable true state must have v in [lo, hi].

    Quantifiers: forall admissible causal torque policy, adversary may choose
    r0=r1=r2=+R or -R. Phi2 depends only on tau0, not later torques.
    """
    phi, omega = F(phi), F(omega)
    assert abs(phi) <= PHI_MAX and abs(omega) <= OMEGA_MAX
    a0, a1, a2 = phi, phi+H*omega, phi+2*H*omega
    # All reachable phi2 are in (-1,1), where sin is increasing.
    assert max(abs(a0), abs(a1), abs(a2)+DELTA) < 1
    upper_sum = sin_bounds(a0)[1] + sin_bounds(a1)[1] + sin_bounds(a2+DELTA)[1]
    lower_sum = sin_bounds(a0)[0] + sin_bounds(a1)[0] + sin_bounds(a2-DELTA)[0]
    lo = -V + 3*H*R + H*T*lower_sum
    hi = V - 3*H*R + H*T*upper_sum
    return lo, hi


def certify_counterexample():
    # A nonzero tilt state that is NOT covered by Run265's zero-tilt slice.
    phi, omega, v0, p0 = -F(1,10), F(0), F(57,20), F(0)
    lo, hi = necessary_interval(phi, omega)
    assert v0 > hi, 'all causal torque choices must violate v3<=3 under r=+R'
    # For first two steps, torque has no effect on phi0/phi1.
    sin_phi_lo, sin_phi_hi = sin_bounds(phi)
    v1_lo = v0 + H*(R-T*sin_phi_hi)
    v1_hi = v0 + H*(R-T*sin_phi_lo)
    v2_lo = v0 + 2*H*(R-T*sin_phi_hi)
    v2_hi = v0 + 2*H*(R-T*sin_phi_lo)
    assert -V < v1_lo <= v1_hi < V
    assert -V < v2_lo <= v2_hi < V
    # p3 = p0 + h(v0+v1+v2), independent of torque through tick 3.
    p3_hi = p0 + H*(v0+v1_hi+v2_hi)
    assert p3_hi < P_MAX
    # Phi3 = phi0 + 3h omega0 + (h^2/J)(2 tau0 + tau1),
    # omega3 = omega0 + (h/J)(tau0+tau1+tau2).
    assert abs(phi)+3*DELTA < PHI_MAX
    assert 3*H*U/J < OMEGA_MAX
    # A guaranteed lower bound on v3 under +R and any admissible tau0.
    v3_lo = v0 + 3*H*R - H*T*(sin_bounds(phi)[1] + sin_bounds(phi+H*omega)[1] + sin_bounds(phi+2*H*omega+DELTA)[1])
    assert v3_lo > V
    return dict(phi=str(phi), omega=str(omega), p0=str(p0), v0=str(v0),
                v1_bounds=[str(v1_lo),str(v1_hi)],
                v2_bounds=[str(v2_lo),str(v2_hi)],
                v3_guaranteed_lower=str(v3_lo),
                p3_upper=str(p3_hi),
                necessary_v0_interval=[str(lo),str(hi)])


def certificate(root=None):
    assert DELTA == F(1,625)
    zero = necessary_interval(F(0), F(0))
    tilted = necessary_interval(-F(1,10), F(0))
    assert tilted[1] < zero[1]
    assert zero[1] <= F(1151429823, 400000000)
    witness = certify_counterexample()
    if root is not None:
        cfg=json.loads((Path(root)/'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics']=='defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s']))==H
        assert F(str(cfg['plant']['inertia_kg_m2']))==J
        assert F(str(cfg['plant']['gravity_m_s2']))==T
        assert F(str(cfg['domain']['state_upper'][2]))==V
        assert F(str(cfg['domain']['state_upper'][4]))==PHI_MAX
        assert F(str(cfg['domain']['state_upper'][5]))==OMEGA_MAX
        assert F(str(cfg['domain']['input_upper'][1]))==U
        assert F(str(cfg['domain']['input_lower'][1]))==-U
    return {
        'run':266,
        'scope':'frozen_4state_defined_discrete_euler_fixed_T9.81_only',
        'parameters':{'h':str(H),'J':str(J),'T':str(T),'U':str(U),'R':str(R),'delta_phi2':str(DELTA)},
        'guard':'v0 >= -V+3hR+hT[sin(phi)+sin(phi+h*omega)+sin(phi+2h*omega-delta)] and v0 <= V-3hR+hT[sin(phi)+sin(phi+h*omega)+sin(phi+2h*omega+delta)]; rational Taylor lower/upper widen these necessary bounds',
        'zero_attitude_necessary_interval':[str(x) for x in zero],
        'negative_tilt_necessary_interval':[str(x) for x in tilted],
        'witness':witness,
        'proof':'phi1=phi0+h*omega0; phi2=phi0+2h*omega0+(h^2/J)*tau0; sin monotone for |phi2|<1; choose r0=r1=r2=+R or -R; bound tau0 via +/-U; bound sin by degree7 Taylor +/- |x|^9/9!',
        'quantifiers':'for every legal torque policy and all measurement/feedback histories, one admissible three-tick disturbance sign causes failure for a state outside the necessary interval',
        'does_not_assert':['Run260 tick60 posterior contains witness','terminal information RCI exists or does not exist','six-state or variable-thrust guarantee','MPC or SMF implemented','20ms worst-case execution'],
        'gate_A':'blocked',
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    s=json.dumps(certificate(args.root),sort_keys=True,indent=2,ensure_ascii=False)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(s)
    else:
        print(s,end='')


if __name__=='__main__':
    main()
