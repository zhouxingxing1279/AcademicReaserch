"""Run240: exact all-real-observation envelope regressions (5/10/15 modes)."""
import unittest
from fractions import Fraction as F
from pathlib import Path
import check_four_state_all_observations as m


class AllObservationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=m.verify()

    def test_prior_run239_reproduced(self):
        self.assertEqual(m.interval(15,F(0))['radius'],F(353411321,960000000))
        self.assertEqual(m.interval(15,F(0))['upper'],F(353411321,960000000))

    def test_five_tick_zero_observation_no_shrink(self):
        self.assertEqual(m.interval(5,F(0))['radius'],F(19716681,80000000))
        self.assertEqual(m.mode_certificate(5)['relative_radius_reduction'],'0')

    def test_ten_tick_uniform_shrink_exact(self):
        self.assertEqual(F(m.mode_certificate(10)['max_posterior_velocity_interval_radius']),F(229572001,720000000))
        self.assertTrue(m.mode_certificate(10)['uniform_strict_radius_reduction'])

    def test_fifteen_tick_uniform_shrink_exact(self):
        self.assertEqual(F(m.mode_certificate(15)['max_posterior_velocity_interval_radius']),F(353411321,960000000))
        self.assertTrue(m.mode_certificate(15)['uniform_strict_radius_reduction'])

    def test_all_knot_extrema_reproduced(self):
        for n,expected in ((5,F(19716681,80000000)),(10,F(229572001,720000000)),(15,F(353411321,960000000))):
            self.assertEqual(max(m.interval(n,y)['radius'] for y in m.knots(n) if m.interval(n,y)),expected)

    def test_piecewise_convex_envelope_midpoints(self):
        # Between knots, max of affine supports is convex.
        for n in m.MODES:
            ks=m.knots(n)
            for a,b in zip(ks,ks[1:]):
                left,right=m.interval(n,a),m.interval(n,b)
                mid=m.interval(n,(a+b)/2)
                if left and right and mid:
                    self.assertLessEqual(mid['radius'],max(left['radius'],right['radius']))

    def test_primal_dual_all_branches_and_modes(self):
        for n in m.MODES:
            for y in m.knots(n):
                for s in (-1,1):
                    w=m.branch_upper(n,s,y)
                    if w:
                        self.assertLessEqual(abs(w['position']-y),m.NOISE)
                        self.assertTrue(all(-1<=xi<=1 for xi in w['xi']))

    def test_symmetry(self):
        for n in m.MODES:
            for y in m.knots(n):
                a,b=m.interval(n,y),m.interval(n,-y)
                self.assertEqual(bool(a),bool(b))
                if a:
                    self.assertEqual(a['upper'],-b['lower'])
                    self.assertEqual(a['radius'],b['radius'])

    def test_no_uniform_absolute_bound_shrink(self):
        for n in m.MODES:
            p=sum((p for p,v in m.generators(n)),F(0))
            v=sum((v for p,v in m.generators(n)),F(0))
            self.assertEqual(m.interval(n,p)['upper'],v)

    def test_unobservable_last_disturbance(self):
        for n in m.MODES:
            self.assertEqual(m.generators(n)[-1],(F(0),m.H*m.R))
            self.assertGreaterEqual(m.interval(n,F(0))['radius'],m.H*m.R)

    def test_next_15_tick_finite_safety(self):
        for item in self.c['modes']:
            self.assertLess(F(item['unconditional_next_15_zero_torque_position_bound']),m.LIMITS[0])
            self.assertLess(F(item['unconditional_next_15_zero_torque_velocity_bound']),m.LIMITS[1])
        self.assertFalse(self.c['recursive_invariance_certified'])
        self.assertFalse(self.c['smf_mpc_closed_loop_certified'])

    def test_empty_and_invalid(self):
        self.assertIsNone(m.interval(15,F(1)))
        with self.assertRaises(ValueError):m.generators(0)
        with self.assertRaises(ValueError):m.branch_upper(5,0,F(0))

    def test_config_contract(self):
        root=Path(__file__).resolve().parents[1]
        if (root/'configs/planar_baseline.json').exists():
            self.assertEqual(m.verify(root),self.c)
        else:self.skipTest('requires full repository checkout; GitHub Actions must verify')

if __name__=='__main__':unittest.main()
