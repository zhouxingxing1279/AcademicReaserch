import unittest
import numpy as np
from src.oit_mrpi.sets import (ConstrainedZonotope as CZ, box, linear_map,
    minkowski_sum, generalized_intersection, outer_reduce, to_polytope,
    affine_containment, contains, pontryagin_inner,homothetic_cz_rpi)
from src.oit_mrpi.rpi import (finite_reach, invariant_tail, rakovic_scaled,
                             one_step_rpi, rpi_direction_residual)
from src.oit_mrpi.estimation import window_estimate, literal_oit, ConstantBiasLearner
from src.oit_mrpi.control import TubeMPC, double_integrator, lqr


class OitMrpiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ctrl = TubeMPC(window=3)

    def test_generalized_intersection_and_tightening(self):
        Z = box([-1, -1], [1, 1])
        Y = box([.7], [.9])
        C = generalized_intersection(Z, np.array([[1., 1.]]), Y)
        self.assertTrue(C.point_contains([.4, .4]))
        self.assertFalse(C.point_contains([0, 0]))
        self.assertAlmostEqual(C.support(np.array([1., 1.])), .9)
        X = to_polytope(box([-2, -2], [2, 2]))
        T = pontryagin_inner(X, C)
        np.testing.assert_allclose(T.h+C.support_many(X.H), X.h)

    def test_batch_interval_hull_dominates(self):
        F = np.array([[.5, .4], [-.3, .6]])
        D = np.diag([.2, .1]); Z = finite_reach(F, D, 0)
        for N in range(1, 10):
            Z = outer_reduce(minkowski_sum(linear_map(F, Z), CZ(np.zeros(2), D)), 2)
            batch = outer_reduce(finite_reach(F, D, N), 2)
            self.assertEqual(contains(to_polytope(Z), batch)['status'], 'certified_float')

    def test_tail_rpi_on_all_polygon_facets(self):
        sys = double_integrator(); F = sys.A+sys.B@lqr(sys.A, sys.B); D = sys.B*.05
        Z, meta = invariant_tail(F, D, 1e-7)
        P = to_polytope(Z)
        self.assertLessEqual(max(rpi_direction_residual(F, D, Z, P.H)), 1e-8)
        self.assertLess(meta['tail_bound_inf'], 1e-7)

    def test_rakovic_rank_deficient_disturbance(self):
        sys = double_integrator(); F = sys.A+sys.B@lqr(sys.A, sys.B); D = sys.B*.05
        Z, meta = rakovic_scaled(F, D)
        ref, _ = invariant_tail(F, D, 1e-9)
        Q = np.array([[1, 0], [0, 1], [1, 1], [-1, 1]], dtype=float)
        Q /= np.linalg.norm(Q, axis=1)[:, None]
        self.assertGreaterEqual(min(Z.support_many(Q)-ref.support_many(Q)), -1e-8)
        self.assertLess(max(Z.support_many(Q)-ref.support_many(Q)), 1e-3)
        self.assertLess(meta['total_error_inf_bound'], 5e-4)

    def test_one_step_certificate(self):
        sys = double_integrator(); F = sys.A+sys.B@lqr(sys.A, sys.B); D = sys.B*.05
        Z, meta = one_step_rpi(F, D)
        self.assertLess(meta['certificate_residual'], 1e-8)
        P = to_polytope(Z)
        self.assertLess(max(rpi_direction_residual(F, D, Z, P.H)), 1e-8)

    def test_adr_for_noncentrally_symmetric_triangle(self):
        # Conv{(0,0),(1,0),(0,1)} via three barycentric coordinates.
        Z = CZ(np.array([.5, .5]), np.array([[0., .5, 0.], [0., 0., .5]]),
               np.ones((1, 3)), np.array([-1.]))
        successor = minkowski_sum(linear_map(.5*np.eye(2), Z), linear_map(.5*np.eye(2), Z))
        cert = affine_containment(successor, Z)
        self.assertEqual(cert['status'], 'certified_float')
        bad = affine_containment(box([-2, -2], [2, 2]), Z)
        self.assertEqual(bad['status'], 'uncertified')

    def test_joint_dynamics_against_plant_and_observer(self):
        d = self.ctrl; A, B, C = d.sys.A, d.sys.B.ravel(), d.sys.C
        rng = np.random.default_rng(104)
        for _ in range(30):
            x, hat, z = rng.normal(size=(3, 2)); v, w, noise = rng.uniform(-1, 1, 3)
            u = v+(d.K@(hat-z)).item()
            xp = A@x+B*(u+.05*w)
            pred = A@hat+B*u
            hp = pred+d.L.ravel()*((C@xp).item()+.1*noise-(C@pred).item())
            zp = A@z+B*v
            eta = np.r_[x-hat, hat-z]
            expected = d.joint.F@eta+d.joint.D@np.array([w, noise])
            np.testing.assert_allclose(np.r_[xp-hp, hp-zp], expected, atol=1e-12)

    def test_window_shift_and_true_containment(self):
        d = self.ctrl; joint = d.joint
        eta = np.zeros(4); innovations = []; ds = [eta[2:].copy()]
        rng = np.random.default_rng(105)
        Q = rng.normal(size=(18, 4))
        old = joint.compatible_tube(innovations, ds, 3, 4)
        for k in range(5):
            omega = rng.uniform(-1, 1, 2)
            r = (joint.Hinnovation@eta+joint.noise_innovation@omega).item()
            eta = joint.F@eta+joint.D@omega
            innovations.append(r); ds.append(eta[2:].copy())
            new = joint.compatible_tube(innovations, ds, 3, 4)
            self.assertTrue(new[0].point_contains(eta))
            for i in range(4):
                self.assertLessEqual(max(new[i].support_many(Q)-old[i+1].support_many(Q)), 2e-7)
            old = new

    def test_unrestricted_window_is_inside_literal_oit(self):
        s = double_integrator(); x = np.array([2., 2.]); ys=[]; us=[]
        for k in range(5):
            ys.append(x[0]+.1*np.cos(k))
            if k < 4:
                us.append(.03*np.sin(k)); x=s.A@x+s.B.ravel()*(us[-1]+.05*np.sin(3*k))
        Z = window_estimate(s.A, s.B, s.C, ys, us, .05, .1)
        O = literal_oit(s.A, s.B, s.C, ys, us, .05, .1)
        self.assertTrue(Z.point_contains(x))
        self.assertEqual(contains(O, Z)['status'], 'certified_float')

    def test_constant_bias_learning_retains_future_support(self):
        learner = ConstantBiasLearner(-.3, .3, .02)
        old = (-.32, .32)
        for residual in (-.02, .02, 0):
            observation = .12+residual
            new = learner.update(observation-.005, observation+.005)
            self.assertLessEqual(old[0], new[0]); self.assertGreaterEqual(old[1], new[1])
            self.assertLessEqual(new[0], .1); self.assertGreaterEqual(new[1], .14)
            old = new

    def test_homothetic_synthesis_matches_analytic_triangle(self):
        Z=CZ(np.array([.5,.5]),np.array([[0.,.5,0.],[0.,0.,.5]]),np.ones((1,3)),[-1.])
        result,cert=homothetic_cz_rpi(.5*np.eye(2),linear_map(.5*np.eye(2),Z),Z)
        self.assertEqual(cert['status'],'certified_float')
        self.assertAlmostEqual(cert['scale'],1.,places=7)
        self.assertAlmostEqual(result.support(np.array([1.,1.])),1.,places=7)


if __name__ == '__main__':
    unittest.main()
