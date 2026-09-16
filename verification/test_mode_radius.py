"""Regression checks for directed rounding and mode-path merge semantics."""
import unittest
from fractions import Fraction as F
from check_mode_radius import sqrt_interval, radius_step, propagate_generators, row_supports


class RadiusChecks(unittest.TestCase):
    def test_root_encloses_irrational_and_exact_square(self):
        lo, hi = sqrt_interval(F(2))
        self.assertLess(lo * lo, F(2))
        self.assertGreater(hi * hi, F(2))
        self.assertEqual(sqrt_interval(F(9, 4)), (F(3, 2), F(3, 2)))
        with self.assertRaises(ValueError):
            sqrt_interval(F(-1))

    def test_merge_keeps_worst_reachable_path(self):
        # Two paths return to mode 0: 0->1->0 gives 7/2; 0->2->0 gives 2.
        edges = [(0, 1, F(1)), (0, 2, F(4)), (1, 0, F(9)), (2, 0, F(1))]
        one = radius_step({0: (F(0), F(0))}, edges, (F(1, 2), F(1, 2)))
        self.assertEqual(one, {1: (F(1), F(1)), 2: (F(2), F(2))})
        two = radius_step(one, edges, (F(1, 2), F(1, 2)))
        self.assertEqual(two, {0: (F(7, 2), F(7, 2))})

    def test_shared_generator_cancellation_survives(self):
        # Correlated p=v: the innovation v-p cancels, independent boxes would not.
        Z = [[F(1)], [F(1)]]
        A = [[F(0), F(0)], [F(-1), F(1)]]
        G = [[F(0)], [F(1, 5)]]
        self.assertEqual(row_supports(propagate_generators(A, Z, G)), [F(0), F(1, 5)])


if __name__ == '__main__':
    unittest.main()
