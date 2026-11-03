"""Regression tests for the vertical nominal-thrust reserve certificate."""
import unittest
from fractions import Fraction as F


class NominalThrustReserveChecks(unittest.TestCase):
    def _subject(self):
        try:
            from check_nominal_thrust_reserve import run
        except ImportError as exc:
            self.fail(f"nominal-thrust reserve implementation is missing: {exc}")
        return run

    def test_full_nominal_thrust_domain_is_rejected_exactly(self):
        result = self._subject()()

        self.assertEqual(result['status'], 'pass')
        self.assertEqual(result['necessary_nominal_thrust_interval'],
                         [F(1198021, 160000), F(1782257, 160000)])
        self.assertFalse(result['full_range_nominal_candidate_admissible'])
        self.assertTrue(result['separate_nominal_thrust_bounds_configured'])
        self.assertTrue(result['hover_nominal_thrust_admissible'])
        self.assertTrue(all(witness['strict_outward_drift']
                            for witness in result['endpoint_obstruction_witnesses']))

    def test_boundary_reserves_match_actual_thrust_residuals(self):
        result = self._subject()()
        lower, upper = result['necessary_nominal_thrust_interval']
        negative, positive = result['boundary_correction_reserves']

        self.assertEqual(negative, lower - F(981, 200))
        self.assertEqual(negative, F(413221, 160000))
        self.assertEqual(positive, F(2943, 200) - upper)
        self.assertEqual(positive, F(572143, 160000))


if __name__ == '__main__':
    unittest.main()
