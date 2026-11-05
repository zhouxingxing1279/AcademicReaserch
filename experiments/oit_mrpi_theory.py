"""Analytic witnesses and numerical audits for propositions A-D."""
from fractions import Fraction
import numpy as np
from src.oit_mrpi.sets import (ConstrainedZonotope as CZ, box, linear_map,
    minkowski_sum, outer_reduce, affine_containment, to_polytope,homothetic_cz_rpi)
from src.oit_mrpi.rpi import finite_reach, invariant_tail
from src.oit_mrpi.estimation import ConstantBiasLearner


def search_reduction_counterexample(seed=20261105, max_trials=5000):
    rng = np.random.default_rng(seed)
    P = np.array([[1., 1.], [1., -1.]])
    def reduction(Z):
        basis = np.eye(2) if Z.support(np.array([1., 0.])) <= .7 else P
        return outer_reduce(Z, 2, basis), basis
    for trial in range(max_trials):
        F = rng.integers(-8, 9, (2, 2))/10
        if max(abs(np.linalg.eigvals(F))) >= .98:
            continue
        D = rng.integers(-4, 5, (2, 2))/10
        if abs(np.linalg.det(D)) < .005:
            continue
        Z = finite_reach(F, D, 0)
        for N in range(1, 9):
            Z, basis = reduction(minkowski_sum(linear_map(F, Z), CZ(np.zeros(2), D)))
            batch, _ = reduction(finite_reach(F, D, N))
            Q = np.vstack([np.linalg.inv(basis), -np.linalg.inv(basis)])
            gap = batch.support_many(Q)-Z.support_many(Q)
            if max(gap) > 1e-6:
                q = Q[np.argmax(gap)]
                witness = batch.G@np.sign(q@batch.G)
                frac = lambda a: [[str(Fraction(float(v)).limit_denominator(10**9)) for v in row]
                                  for row in np.atleast_2d(a)]
                qb = [Fraction(float(v)).limit_denominator() for v in q]
                gb = [[Fraction(float(v)).limit_denominator(10**9) for v in row] for row in batch.G]
                gs = [[Fraction(float(v)).limit_denominator(10**9) for v in row] for row in Z.G]
                def h(G):
                    return sum(abs(sum(qb[i]*G[i][j] for i in range(2))) for j in range(len(G[0])))
                return {'found': True, 'trial': trial, 'N': N, 'F': F, 'D': D,
                        'rho_F': float(max(abs(np.linalg.eigvals(F)))),
                        'batch_G': batch.G, 'sequential_G': Z.G, 'direction': q,
                        'witness': witness, 'support_gap': float(max(gap)),
                        'rational_gap_for_saved_generators': str(h(gb)-h(gs)),
                        'rational_F': frac(F), 'rational_D': frac(D),
                        'operator': 'axis box if h_Z(e1)<=0.7; otherwise box in basis [[1,1],[1,-1]]',
                        'scope': 'outer but nonmonotone reduction; rationalized saved witness'}
    return {'found': False, 'trials': max_trials}


def run_theory(out, csv):
    counter = search_reduction_counterexample()
    rng = np.random.default_rng(20261105)
    rows = []
    for i in range(200):
        F = rng.normal(size=(2, 2)); F *= .8/max(abs(np.linalg.eigvals(F)))
        D = rng.normal(size=(2, 2))*.1
        seq = finite_reach(F, D, 0)
        for N in range(1, 9):
            seq = outer_reduce(minkowski_sum(linear_map(F, seq), CZ(np.zeros(2), D)), 2)
            batch = outer_reduce(finite_reach(F, D, N), 2)
            gap = max(batch.support_many(np.eye(2))-seq.support_many(np.eye(2)))
            rows.append(dict(trial=i, N=N, max_batch_minus_sequential=gap,
                             batch_size=float(np.prod(2*np.diag(batch.G))),
                             sequential_size=float(np.prod(2*np.diag(seq.G)))))
    csv(out/'reduction.csv', rows)

    # Non-symmetric CZ: barycentric triangle, invariant by convexity.
    Z = CZ(np.array([.5, .5]), np.array([[0., .5, 0.], [0., 0., .5]]),
           np.ones((1, 3)), np.array([-1.]))
    Znext = minkowski_sum(linear_map(.5*np.eye(2), Z), linear_map(.5*np.eye(2), Z))
    adr = affine_containment(Znext, Z)
    bary = rng.dirichlet(np.ones(3), (5000, 2))
    xi = 2*bary[:, 0]-1; eta = 2*bary[:, 1]-1
    src = np.c_[xi, eta]
    zeta = src@adr['M'].T+adr['t']
    adr['sample_count'] = len(src)
    adr['sample_box_violation'] = float(np.max(abs(zeta)-1))
    adr['sample_equality_residual'] = float(np.max(abs(zeta@Z.Aeq.T-Z.beq)))
    adr['scope'] = 'fixed-CZ feasibility certificate; joint optimization over G,Aeq is not an LP'
    # Equal generator counts: CZ triangle vs its coefficient-constraint deletion.
    adr['triangle_area'] = .5
    adr['same_generator_unconstrained_area'] = 1.
    adr['area_comparison_scope'] = 'representation witness, not optimized-synthesis superiority'
    synthesized,synthesis_cert=homothetic_cz_rpi(.5*np.eye(2),linear_map(.5*np.eye(2),Z),Z)
    unconstrained=CZ(Z.c,Z.G)
    zono,zono_cert=homothetic_cz_rpi(.5*np.eye(2),linear_map(.5*np.eye(2),Z),unconstrained)
    adr['homothetic_CZ_synthesis']=synthesis_cert
    adr['homothetic_unconstrained_synthesis']=zono_cert
    adr['CZ_synthesized_area']=.5*synthesis_cert['scale']**2
    adr['unconstrained_synthesized_area']=zono_cert['scale']**2

    learner = ConstantBiasLearner(-.3, .3, .02)
    learned = []
    for k in range(30):
        q = .12+rng.uniform(-.02, .02)
        measured = q+rng.uniform(-.005, .005)
        low, high = learner.update(measured-.005, measured+.005)
        # Scalar F=.7, mRPI is [low/.3,high/.3], not assumed zero-centered.
        learned.append(dict(k=k, true_bias=.12, q=q, observation=measured,
                            disturbance_low=low, disturbance_high=high,
                            rpi_low=low/.3, rpi_high=high/.3))
    csv(out/'constant_bias_learning.csv', learned)
    return {'A': {'monotone_outer_proof': True, 'checked_cases': len(rows),
                  'max_monotone_violation': max(r['max_batch_minus_sequential'] for r in rows),
                  'nonmonotone_counterexample': counter},
            'B': {'scalar_cut_counterexample': {'F': .5, 'W': [-1, 1], 'mRPI': [-2, 2],
                      'posterior': [-.5, .5], 'next_prediction': [-1.25, 1.25]},
                  'output_feedback_counterexample': {'A': 1., 'B': 1., 'K': -1.,
                      'x': 0., 'z': 0., 'hat_x': 1., 'w': 0., 'claimed_next_error': 0.,
                      'actual_next_error': -1.},
                  'union_envelope': 'Contains old prediction and therefore cannot provide tighter support than it'},
            'C': {'nested_mRPI_proof': True,
                  'invalid_unrelated_learning_witness': {'W': [-1, 1], 'past_w': 0., 'next_w': 1.,
                      'learned_from_past': [0., 0.], 'future_inclusion': False},
                  'valid_learning_model': 'fixed bias b=.12 plus independently bounded residual .02; observed q error .005'},
            'D': adr,
            'additional_corrections': {
                'exact_outer_reduction_fixed_point_is_RPI': True,
                'RPI_is_postfixed_not_necessarily_fixed': True,
                'Rakovic_contraction_already_implies_RPI': True,
                'ordinary_CZ_cannot_represent_unbounded_measurement_strip': True,
                'finite_direction_support_test_is_not_general_inclusion_proof': True}}
