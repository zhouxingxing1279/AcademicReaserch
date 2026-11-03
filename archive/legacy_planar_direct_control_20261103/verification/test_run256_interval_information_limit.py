import unittest
from fractions import Fraction as F
from check_run256_interval_information_limit import (
    verify, width, width_floor, observe,
)
from check_run255_posterior_bridge import posterior30, bridge, NOISE, R, H, LIMIT

class TestIntervalInformationLimit(unittest.TestCase):
    def setUp(self):
        self.s30 = posterior30()
        self.p35 = bridge(self.s30, 5)[5]
    def test_success_miss_nonempty(self):
        self.assertIsNotNone(observe(self.p35, {'phi': F(0), 'omega': F(0)}))
        self.assertIsNotNone(observe(self.p35, {'phi': F(0), 'omega': F(0), 'p': F(0)}))
    def test_success_cannot_reduce_velocity(self):
        for y in (F(0), self.p35['p'][0]-NOISE['p'], self.p35['p'][1]+NOISE['p']):
            self.assertEqual(observe(self.p35, {'phi': F(0), 'omega': F(0), 'p': y})['v'], self.p35['v'])
    def test_success_reduces_position(self):
        self.assertLess(width(observe(self.p35, {'p': F(0)}), 'p'), width(self.p35, 'p'))
    def test_velocity_width_increases(self):
        self.assertGreater(width(self.p35, 'v'), width(self.s30, 'v'))
    def test_disturbance_floor(self):
        self.assertEqual(2*H*R, F(3246383, 40000000))
    def test_tick70_not_forced_by_width_floor(self):
        self.assertLessEqual(width_floor(40), 2*LIMIT['v'])
    def test_tick71_width_exceeds_speed_box(self):
        self.assertGreater(width_floor(41), 2*LIMIT['v'])
    def test_scope(self):
        self.assertFalse(verify()['physical_unsafety_proved'])
        self.assertFalse(verify()['terminal_information_invariance_proved'])
    def test_certificate(self):
        self.assertEqual(verify()['first_tick_width_floor_exceeds_hard_box'], 71)

if __name__ == '__main__': unittest.main()
