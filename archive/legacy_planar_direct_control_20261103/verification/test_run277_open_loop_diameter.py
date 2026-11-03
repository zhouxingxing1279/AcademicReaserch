"""Independent exact-rational regression for Run277; no optimizer required."""
import unittest
from fractions import Fraction as F
from check_run277_open_loop_diameter import (H,R,VMAX,DELTA0,PLUS_V60,MINUS_V60,
    velocity_diameter,first_impossible_horizon,verify)

class TestRun277(unittest.TestCase):
    def test_true_prior_pair_diameter(self):
        self.assertEqual(PLUS_V60-MINUS_V60,F(22724681,40000000))
    def test_zero_horizon(self):
        self.assertEqual(velocity_diameter(0),DELTA0)
    def test_one_tick(self):
        self.assertEqual(velocity_diameter(1)-DELTA0,2*H*R)
    def test_independence_from_common_acceleration(self):
        # The common -T*sin(phi) term cancels for ANY common attitude trajectory.
        vp,vm=PLUS_V60,MINUS_V60
        for c in [F(0),F(2,7),-F(31,8),F(11,9)]:
            vp,vm=vp+H*(c+R),vm+H*(c-R)
        self.assertEqual(vp-vm,velocity_diameter(4))
    def test_horizon_exact(self):
        self.assertEqual(first_impossible_horizon(),67)
    def test_boundary_66(self):
        self.assertEqual(velocity_diameter(66),F(236985959,40000000))
        self.assertLessEqual(velocity_diameter(66),2*VMAX)
    def test_boundary_67(self):
        self.assertEqual(velocity_diameter(67),F(120116171,20000000))
        self.assertGreater(velocity_diameter(67),2*VMAX)
    def test_conclusion_scope(self):
        z=verify()
        self.assertEqual(z['strict_first_obstruction_tick'],127)
        self.assertIn('failure of causal observation-conditioned feedback',z['does_not_prove'])
        self.assertEqual(z['gate_A'],'blocked')
    def test_invalid_horizon(self):
        for n in [-1,F(1,2)]:
            with self.assertRaises(ValueError):velocity_diameter(n)

if __name__=='__main__': unittest.main()
