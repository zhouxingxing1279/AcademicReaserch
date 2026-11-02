import unittest
from fractions import Fraction as F
from check_run257_correlated_position_velocity import (
    acceleration_bounds, success_velocity, uniform_width,
    zero_success_witness, verify,
)
from check_run255_posterior_bridge import posterior30, bridge, NOISE

class TestRun257CorrelatedVelocity(unittest.TestCase):
    def setUp(self):
        self.rows = bridge(posterior30(), 5)

    def test_five_acceleration_intervals(self):
        self.assertEqual(len(acceleration_bounds(self.rows)), 5)
        self.assertTrue(all(a<=b for a,b in acceleration_bounds(self.rows)))

    def test_box_matches_run256(self):
        self.assertEqual(self.rows[-1]['v'],
                         (-F(3110667463,2000000000), F(1554705901,1000000000)))

    def test_zero_success_shrinks_velocity(self):
        lo,hi = success_velocity(F(0),self.rows)
        self.assertLess(hi-lo,F(11,10))
        self.assertGreater(hi-lo,F(1))

    def test_all_nonempty_success_uniform_width(self):
        for y in (self.rows[-1]['p'][0]-NOISE['p'],F(0),
                  self.rows[-1]['p'][1]+NOISE['p']):
            lo,hi=success_velocity(y,self.rows)
            self.assertLessEqual(hi-lo,uniform_width(self.rows))

    def test_zero_success_nonempty_witness(self):
        lo,hi=zero_success_witness()
        self.assertTrue(-NOISE['p']<=lo<=hi<=NOISE['p'])

    def test_miss_still_box(self):
        cert=verify()
        self.assertEqual(cert['tick35_miss_velocity_width_unimproved'],
                         cert['tick35_independent_box_velocity_width'])

    def test_scope_not_invariance(self):
        cert=verify()
        self.assertFalse(cert['terminal_information_invariance_proved'])
        self.assertFalse(cert['recursive_feasibility_proved'])

    def test_run_id(self):
        self.assertEqual(verify()['run'],257)

if __name__=='__main__':
    unittest.main()
