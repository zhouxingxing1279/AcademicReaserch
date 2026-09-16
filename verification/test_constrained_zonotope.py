"""Analytic regressions for support certificates and representation contracts."""
import unittest
from fractions import Fraction as Q
import numpy as np
from check_constrained_zonotope import CZ, eye


class Contracts(unittest.TestCase):
    def test_nonzero_strip_and_recenter(self):
        z = CZ([Q(0)], eye(1)).observe([0], [Q(1, 2)], [Q(1, 4)])
        # [1/4,3/4], nonzero b; exact duals for both endpoints.
        self.assertEqual(z.dual_upper([Q(1)], [Q(1)]), Q(3, 4))
        self.assertEqual(z.dual_upper([Q(-1)], [Q(-1)]), Q(-1, 4))
        self.assertEqual(z.recenter([Q(1, 2)]).dual_upper([Q(1)], [Q(1)]), Q(1, 4))
        self.assertLessEqual(z.support_certificate([Q(1)])[0], Q(3, 4))

    def test_correlated_line_and_constraint_deletion(self):
        z = CZ([Q(0)]*2, eye(2), np.array([[Q(1), Q(-1)]], dtype=object),
               np.array([Q(0)], dtype=object))
        self.assertEqual(z.dual_upper([Q(1), Q(-1)], [Q(1)]), 0)
        relaxed = CZ(z.c, z.g)
        self.assertEqual(relaxed.dual_upper([Q(1), Q(-1)], []), 2)
        # Thus an outer relaxation can violate the previous prediction cap.

    def test_arbitrary_dual_is_safe(self):
        z = CZ([Q(0)], eye(1)).observe([0], [Q(1, 2)], [Q(1, 4)])
        for lam in [Q(-10), Q(0), Q(1, 3), Q(1), Q(20)]:
            self.assertGreaterEqual(z.dual_upper([Q(1)], [lam]), Q(3, 4))


if __name__ == '__main__':
    unittest.main()
