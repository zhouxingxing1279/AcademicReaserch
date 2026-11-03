"""Regression tests for the time-uniform mode-radius certificate."""
import unittest
from fractions import Fraction as F


class InvariantRadiusChecks(unittest.TestCase):
    def _subject(self):
        try:
            from check_mode_invariant_radius import fixed_point_enclosure
        except ImportError as exc:  # A missing research artifact is a test failure, not a collection error.
            self.fail(f"mode-invariant radius implementation is missing: {exc}")
        return fixed_point_enclosure

    def test_tail_bound_closes_exact_self_loop_fixed_point(self):
        fixed_point_enclosure = self._subject()
        result = fixed_point_enclosure(
            [(0, 0, F(1))], mode_count=1,
            contraction=(F(1, 2), F(1, 2)), iterations=4,
        )
        self.assertEqual(result['lower'][0], F(15, 8))
        self.assertEqual(result['upper'][0], F(2))
        self.assertLessEqual(F(1, 2) * result['upper'][0] + 1,
                             result['upper'][0])

    def test_two_mode_upper_bound_satisfies_every_edge(self):
        fixed_point_enclosure = self._subject()
        edges = [(0, 1, F(1)), (1, 0, F(4))]
        result = fixed_point_enclosure(
            edges, mode_count=2,
            contraction=(F(1, 2), F(1, 2)), iterations=24,
        )
        lower, upper = result['lower'], result['upper']
        self.assertLess(lower[0], F(10, 3))
        self.assertLess(lower[1], F(8, 3))
        self.assertGreaterEqual(upper[0], F(10, 3))
        self.assertGreaterEqual(upper[1], F(8, 3))
        self.assertLessEqual(F(1, 2) * upper[0] + 1, upper[1])
        self.assertLessEqual(F(1, 2) * upper[1] + 2, upper[0])

    def test_rejects_a_mode_without_incoming_edge(self):
        fixed_point_enclosure = self._subject()
        with self.assertRaisesRegex(ValueError, 'incoming edge'):
            fixed_point_enclosure(
                [(0, 0, F(1))], mode_count=2,
                contraction=(F(1, 2), F(1, 2)), iterations=4,
            )


if __name__ == '__main__':
    unittest.main()
