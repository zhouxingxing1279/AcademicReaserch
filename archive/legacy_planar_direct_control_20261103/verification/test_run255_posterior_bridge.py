import unittest
from fractions import Fraction as F
from check_run255_posterior_bridge import (posterior30, bridge, safe, PULSE, verify, LIMIT)

class TestPosteriorBridge(unittest.TestCase):
    def test_posterior(self):
        self.assertEqual(posterior30()['v'][1], F(269364701,200000000))
    def test_shared_pulse_nonzero(self):
        self.assertEqual(sum(PULSE), 0)
        self.assertTrue(any(PULSE))
    def test_full_box_39(self):
        self.assertTrue(all(safe(x) for x in bridge(posterior30())[:40]))
    def test_outer_failure_40(self):
        self.assertFalse(safe(bridge(posterior30())[40]))
    def test_speed_margin_39(self):
        self.assertLess(bridge(posterior30())[39]['v'][1], LIMIT['v'])
    def test_speed_outer_40(self):
        self.assertGreater(bridge(posterior30())[40]['v'][1], LIMIT['v'])
    def test_certificate_scope(self):
        self.assertFalse(verify()['infinite_horizon_terminal_invariance'])
    def test_verify(self):
        self.assertEqual(verify()['certified_future_steps'], 39)

if __name__ == '__main__': unittest.main()
