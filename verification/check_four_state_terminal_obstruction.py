#!/usr/bin/env python3
"""Run222: exact obstruction to a four-state terminal set inside Run221 attitude tube.

Only the frozen four-state Euler uncertainty-envelope model is addressed.
The adversarial residual is admissible in that model; it need not be a
physically realizable persistent aerodynamic disturbance.
"""
from __future__ import annotations

import argparse
import json
from fractions import Fraction as Q
from pathlib import Path

H = Q(1, 50)
T_MIN, T_MAX = Q(981, 200), Q(2943, 200)
V_LIMIT = Q(3)
ZF_PHI, E_PHI = Q(1, 20), Q(1, 100)
R0, R_T = Q(47, 25), Q(243, 16000)


def growth_lower_bound(phi_radius=ZF_PHI + E_PHI, r0=R0, rt=R_T):
    """For r_x=+(r0+rt*T), sin(phi)<=|phi|, and T in [T_MIN,T_MAX]."""
    assert phi_radius >= 0 and r0 >= 0 and rt >= 0
    slope = rt - phi_radius
    return r0 + slope * (T_MAX if slope < 0 else T_MIN)


def first_exceedance(start_velocity, step_growth, limit=V_LIMIT):
    assert -limit <= start_velocity <= limit and step_growth > 0
    # Strict exceedance: integer n > (limit-start_velocity)/step_growth.
    ratio = (limit - start_velocity) / step_growth
    return ratio.numerator // ratio.denominator + 1


def config_contract(root):
    cfg = json.loads((Path(root) / 'configs/planar_baseline.json').read_text(), parse_float=Q)
    assert cfg['plant']['truth_semantics'] == 'defined_discrete_euler'
    assert Q(cfg['plant']['dt_s']) == H
    assert Q(cfg['plant']['mass_kg']) == 1
    assert Q(cfg['domain']['input_lower'][0]) == T_MIN
    assert Q(cfg['domain']['input_upper'][0]) == T_MAX
    assert Q(cfg['domain']['state_lower'][2]) == -V_LIMIT
    assert Q(cfg['domain']['state_upper'][2]) == V_LIMIT
    # The following uncertainty envelope is from the frozen Run208/210
    # verification contract, not from the config's zero external_process noise.
    return True


def verify(root=None):
    if root is not None:
        config_contract(root)
    radius = ZF_PHI + E_PHI
    delta = growth_lower_bound(radius)
    step = H * delta
    assert radius == Q(3, 50)
    assert delta == Q(3905869, 3200000) > 0
    assert step == Q(3905869, 160000000)
    n_zero = first_exceedance(Q(0), step)
    n_worst = first_exceedance(-V_LIMIT, step)
    assert n_zero == 123 and n_worst == 246
    assert (n_zero-1)*step <= V_LIMIT < n_zero*step
    assert -V_LIMIT+(n_worst-1)*step <= V_LIMIT < -V_LIMIT+n_worst*step
    # For a persistent admissible positive residual, every controller that
    # keeps |phi|<=radius has v_x(k+1)>=v_x(k)+step. Thus no nonempty robust
    # controlled invariant set can lie entirely in this strip AND |vx|<=3.
    # This does not rule out terminal sets that allow larger tilt, nor prove
    # impossibility for a correlated/physically restricted residual model.
    required_tilt_lower_bound = R0/T_MAX + R_T
    assert required_tilt_lower_bound > radius
    return {
        'run': '222',
        'scope': 'frozen four-state Euler lateral uncertainty envelope, all admissible thrust and torque policies',
        'evidence': 'EXACT_RATIONAL_ADVERSARIAL_DRIFT_OBSTRUCTION',
        'attitude_phi_radius': str(radius),
        'thrust_interval': [str(T_MIN), str(T_MAX)],
        'lateral_residual_positive_branch': '47/25 + (243/16000)*T',
        'worst_case_acceleration_lower_bound': str(delta),
        'velocity_growth_per_tick_lower_bound': str(step),
        'steps_to_violate_from_vx_zero': n_zero,
        'velocity_lower_bound_at_zero_witness_step': str(n_zero*step),
        'steps_to_violate_from_vx_minus_three': n_worst,
        'velocity_lower_bound_at_worst_witness_step': str(-V_LIMIT+n_worst*step),
        'necessary_positive_tilt_lower_bound_for_nonpositive_acceleration': str(required_tilt_lower_bound),
        'nonempty_robust_invariant_subset_of_attitude_strip_and_bounded_vx': False,
        'gate_A': 'blocked',
        'limitations': [
            'Applies to the Run208/210 independent adversarial lateral residual envelope, not necessarily realizable physical aerodynamics.',
            'Does not exclude a four-state terminal set permitting |phi|>3/50, a reduced disturbance set, or a different terminal strategy.',
            'No four-state SMF/MPC closed loop or terminal Lyapunov stability is established.',
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    data = json.dumps(verify(args.root), indent=2, ensure_ascii=False, sort_keys=True) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(data)
    else:
        print(data, end='')


if __name__ == '__main__':
    main()
