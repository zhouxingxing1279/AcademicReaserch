import unittest
from fractions import Fraction as F
from check_run266_tilt_aware_velocity_guard import (H,J,T,U,R,V,DELTA,
    sin_bounds,necessary_interval,certify_counterexample,certificate)

class TestRun266(unittest.TestCase):
    def test_exact_delta(self):
        self.assertEqual(DELTA,F(1,625))
    def test_sin_interval_zero(self):
        self.assertEqual(sin_bounds(0),(F(0),F(0)))
    def test_sin_interval_symmetry(self):
        for x in (F(1,10),F(53,100),F(1,625)):
            a,b=sin_bounds(x); c,d=sin_bounds(-x)
            self.assertEqual((c,d),(-b,-a))
    def test_zero_guard_refines_old(self):
        lo,hi=necessary_interval(0,0)
        self.assertLessEqual(hi,F(1151429823,400000000))
        self.assertEqual(lo,-hi)
    def test_negative_tilt_tightens_upper(self):
        self.assertLess(necessary_interval(-F(1,10),0)[1],necessary_interval(0,0)[1])
    def test_positive_tilt_relaxes_upper(self):
        self.assertGreater(necessary_interval(F(1,10),0)[1],necessary_interval(0,0)[1])
    def test_omega_shift_changes_guard(self):
        self.assertLess(necessary_interval(0,-F(1))[1],necessary_interval(0,0)[1])
    def test_legal_full_domain(self):
        for phi in (-F(9,20),0,F(9,20)):
            for omega in (-F(2),0,F(2)):
                lo,hi=necessary_interval(phi,omega)
                self.assertLess(lo,hi)
    def test_witness_v3(self):
        self.assertGreater(F(certify_counterexample()['v3_guaranteed_lower']),V)
    def test_witness_first_two_safe(self):
        w=certify_counterexample()
        self.assertLess(F(w['v1_bounds'][1]),V)
        self.assertLess(F(w['v2_bounds'][1]),V)
    def test_witness_position_safe(self):
        self.assertLess(F(certify_counterexample()['p3_upper']),5)
    def test_no_unsupported_claim(self):
        c=certificate()
        self.assertEqual(c['gate_A'],'blocked')
        self.assertIn('terminal information RCI exists or does not exist',c['does_not_assert'])

if __name__=='__main__':
    unittest.main()
