#!/usr/bin/env python3
"""Run234: exact-rational infinite-zonotope RCI for a FIXED-THRUST four-state plant.

Proof covers nonlinear sin(phi), all independent bounded residuals, all times,
full-state linear feedback. It does NOT certify SMF, MPC, dropout, or 6D safety.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

ZERO = F(0)
ONE = F(1)
H = F(1, 50)
J = F(1, 50)
T = F(981, 100)
TAU_MAX = F(2, 25)
K = tuple(F(x) for x in ('-0.123', '-0.494', '2.341', '0.933'))
PHI_LIMIT = F(9, 20)
LIMITS = (F(5), F(3), PHI_LIMIT, F(2))
R = F(47, 25) + F(243, 16000) * T
# Taylor remainder |phi-sin(phi)| <= |phi|^3/6 for real phi.
D = R + T * PHI_LIMIT**3 / 6
N = 800
B = (ZERO, H, ZERO, ZERO)
A = ((ONE, H, ZERO, ZERO),
     (ZERO, ONE, -H*T, ZERO),
     (ZERO, ZERO, ONE, H),
     tuple(-x if i < 3 else ONE-x for i, x in enumerate(K)))


def dot(a, b):
    return sum((x*y for x, y in zip(a, b)), ZERO)


def matvec(x):
    return tuple(dot(row, x) for row in A)


def round_up(x, digits=6):
    scale = 10**digits
    if x < 0:
        raise ValueError('round_up is for nonnegative support bounds')
    num = -((-x.numerator*scale)//x.denominator)
    return f'{num//scale}.{num%scale:0{digits}d}'


def certificate(n=N):
    if n < 1:
        raise ValueError('positive block length required')
    # Exact rational A^j B and A^n columns. No floating-point or interval wrapping.
    sums = [ZERO]*4
    torque_sum = ZERO
    sum_max = ZERO
    v = B
    cols = [tuple(ONE if i == j else ZERO for i in range(4)) for j in range(4)]
    for _ in range(n):
        sums = [s+abs(x) for s, x in zip(sums, v)]
        torque_sum += abs(dot(K, v))
        sum_max += max(abs(x) for x in v)
        v = matvec(v)
        cols = [matvec(col) for col in cols]
    power = tuple(tuple(cols[j][i] for j in range(4)) for i in range(4))
    row_norms = tuple(sum(map(abs, row), ZERO) for row in power)
    rho = max(row_norms)
    if rho >= ONE:
        raise AssertionError('A^n infinity norm does not certify contraction')
    # For k=m*n+j (m>=1, 0<=j<n):
    # |e_i A^(m*n) A^j B| <= ||row_i(A^n)||_1 rho^(m-1) ||A^j B||_inf.
    tails = tuple(row_norm*sum_max/(ONE-rho) for row_norm in row_norms)
    state = tuple(D*(s+t) for s, t in zip(sums, tails))
    kpower = tuple(dot(K, tuple(power[i][j] for i in range(4))) for j in range(4))
    torque_tail = sum(map(abs, kpower), ZERO)*sum_max/(ONE-rho)
    torque = D*(torque_sum+torque_tail)
    if not all(s < limit for s, limit in zip(state, LIMITS)):
        raise AssertionError('state constraint not certified')
    if not torque < TAU_MAX:
        raise AssertionError('unsaturated feedback input not certified')
    return {'run': 234,
            'certificate': 'EXACT_RATIONAL_INFINITE_ZONOTOPE_RPI_AND_NONLINEAR_EMBEDDING',
            'block_length': n,
            'gain': [str(k) for k in K],
            'thrust_N': str(T),
            'residual_acceleration_halfwidth': str(R),
            'nonlinear_remainder_acceleration_bound': str(D-R),
            'effective_acceleration_halfwidth': str(D),
            'power_infinity_norm_upper': round_up(rho, 9),
            'state_abs_upper_rounded_outward': [round_up(x) for x in state],
            'torque_abs_upper_rounded_outward': round_up(torque),
            'state_limits': [str(x) for x in LIMITS],
            'torque_limit': str(TAU_MAX),
            'set_definition': 'S=sum_{j>=0} A_cl^j B [-D,D], compact nonempty robust invariant set',
            'quantifiers': 'for all x in S, all r in [-R,R], fixed T=9.81 and tau=-Kx, next state in S',
            'gate_A': 'blocked_for_output_feedback_MPC',
            'limitations': ['Fixed thrust and full-state feedback only; not intermittent-measurement SMF or MPC.',
                            'S is implicitly represented as an infinite zonotope; finite support/tail bounds certify containment, not exact membership.',
                            'No six-state coupled vertical safety, tracking objective, stability to a point, or 20 ms online guarantee.']}


def verify(root=None):
    if root is not None:
        config = json.loads((Path(root)/'configs/planar_baseline.json').read_text())
        assert config['plant']['truth_semantics'] == 'defined_discrete_euler'
        assert F(str(config['plant']['dt_s'])) == H
        assert F(str(config['plant']['inertia_kg_m2'])) == J
        assert tuple(F(str(x)) for x in config['domain']['input_lower']) == (F(4905,1000), -TAU_MAX)
        assert tuple(F(str(x)) for x in config['domain']['input_upper']) == (F(14715,1000), TAU_MAX)
        assert tuple(F(str(config['domain']['state_upper'][i])) for i in (0,2,4,5)) == LIMITS
    return certificate()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    content = json.dumps(verify(args.root), indent=2, ensure_ascii=False, sort_keys=True) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content)
    else:
        print(content, end='')


if __name__ == '__main__':
    main()
