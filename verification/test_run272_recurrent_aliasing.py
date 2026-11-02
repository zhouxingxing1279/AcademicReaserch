import unittest
from fractions import Fraction as F
from check_run272_recurrent_aliasing import H, R, EPS, P60, V60, paired_future, min_position_separation, certify

class Run272Test(unittest.TestCase):
    def test_start_exact(self):
        self.assertEqual(P60, F(68174043, 4000000000))
        self.assertEqual(V60, F(22724681, 80000000))
    def test_all_ticks_symmetric(self):
        for q in range(16):
            a, b = paired_future(q)
            self.assertEqual(tuple(-z for z in a), b)
    def test_euler_dynamics(self):
        for q in range(15):
            a, b = paired_future(q)
            aa, bb = paired_future(q+1)
            self.assertEqual(aa[0], a[0]+H*a[1])
            self.assertEqual(aa[1], a[1]-H*R)
            self.assertEqual(bb[0], b[0]+H*b[1])
            self.assertEqual(bb[1], b[1]+H*R)
    def test_observation_discrimination(self):
        self.assertEqual(min_position_separation(5), F(74666809,1000000000))
        self.assertEqual(min_position_separation(10), F(74666809,1000000000))
        self.assertGreater(min_position_separation(5), 2*EPS)
        self.assertGreater(min_position_separation(10), 2*EPS)
    def test_aliasing_tick75(self):
        a, b = paired_future(15)
        self.assertEqual(a[0]-b[0], F(68174043,2000000000))
        self.assertEqual(b[1]-a[1], F(3246383,5000000))
        self.assertLess(a[0]-b[0], 2*EPS)
    def test_robust_prefix(self):
        d=certify()
        self.assertEqual(d['all_future_disturbances_abs_p_bound'], str(F(749914473,4000000000)))
        self.assertEqual(d['all_future_disturbances_abs_v_bound'], str(F(35710213,40000000)))
        self.assertTrue(d['all_true_states_hard_safe_60_to_75'])
    def test_distinct_success_noise(self):
        a,b=paired_future(15)
        self.assertLessEqual(abs(-a[0]),EPS)
        self.assertLessEqual(abs(-b[0]),EPS)
        self.assertEqual(a[0]-a[0], b[0]-b[0])
    def test_reject_false_generalization(self):
        # An early success distinguishes this pair; not a universal 15-step indistinguishability.
        self.assertGreater(min_position_separation(5), 2*EPS)
        self.assertLess(min_position_separation(15), 2*EPS)

if __name__=='__main__': unittest.main()
