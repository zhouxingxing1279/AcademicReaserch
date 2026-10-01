"""Regression tests for the cycle-lifted zonotopic error multi-set."""
import unittest
from fractions import Fraction as F


class CycleLiftedZonotopeChecks(unittest.TestCase):
    def _subject(self):
        try:
            from check_cycle_lifted_zonotope import run
        except ImportError as exc:
            self.fail(f"cycle-lifted zonotope implementation is missing: {exc}")
        return run

    def test_cycle_lift_preserves_reset_cancellation_and_closes_domain(self):
        result = self._subject()()

        self.assertEqual(result['status'], 'pass')
        self.assertEqual(result['cycle_lengths'], [5, 10, 15])
        self.assertEqual(result['mode_zero_box'][:2], [F(1, 50), F(1, 50)])
        self.assertEqual(result['mode_zero_box'][4:], [F(1, 200), F(1, 100)])
        self.assertTrue(all(row['pass'] for row in result['cycle_invariance_checks']))
        self.assertTrue(all(row['pass'] for row in result['edge_invariance_checks']))
        self.assertTrue(all(row['fits_state_domain_halfwidth'] for row in result['modes']))

        oldest = result['modes'][14]['coordinate_support']
        self.assertGreater(oldest[2], F(27, 10))
        self.assertLess(oldest[2], F(3))
        self.assertGreater(oldest[3], F(2))
        self.assertLess(oldest[3], F(21, 10))

    def test_per_tick_interval_boxing_destroys_signed_cycle_cancellation(self):
        result = self._subject()()
        witness = result['negative_control']

        self.assertEqual(witness['cycle_length'], 15)
        self.assertEqual(witness['signed_x_velocity_gain'], F(1, 2))
        self.assertEqual(witness['boxed_x_velocity_gain'], F(23, 10))
        self.assertGreater(witness['boxed_x_velocity_gain'], 1)


if __name__ == '__main__':
    unittest.main()
