import sys
import unittest
from fractions import Fraction as Q
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_generic_cz_support_certificate import (
    certified_query,
    dual_upper,
    reconstruct_member,
    run,
)


class GenericCZSupportCertificateTests(unittest.TestCase):
    def test_multi_equality_member_reconstruction_is_exact(self):
        a = np.array([
            [Q(1), Q(1), Q(0), Q(1)],
            [Q(0), Q(1), Q(1), -Q(1)],
        ], dtype=object)
        member = np.array([Q(1, 5), -Q(1, 10), Q(3, 10), Q(2, 5)], dtype=object)
        b = a @ member
        proposal = np.array([float(v) for v in member])
        rebuilt = reconstruct_member(a, b, proposal)
        self.assertIsNotNone(rebuilt)
        self.assertTrue(all(a @ rebuilt == b))
        self.assertTrue(all(abs(v) <= 1 for v in rebuilt))

    def test_dual_bound_does_not_require_optimal_multiplier(self):
        c = np.array([Q(0), Q(0)], dtype=object)
        g = np.array([[Q(1), Q(0), Q(1, 2)],
                      [Q(0), Q(1), -Q(1, 2)]], dtype=object)
        a = np.array([[Q(1), Q(1), Q(0)]], dtype=object)
        b = np.array([Q(0)], dtype=object)
        p = np.array([Q(1), Q(2)], dtype=object)
        upper = dual_upper(c, g, a, b, p, np.array([Q(0)], dtype=object))
        lower, queried_upper, _, _ = certified_query(c, g, a, b, p)
        self.assertLessEqual(lower, queried_upper)
        self.assertGreaterEqual(upper, queried_upper)

    def test_seeded_stress_reconstructs_all_reference_cases(self):
        result = run(seed=20260923, cases=64)
        self.assertEqual(result["reconstructed_members"], 64)
        self.assertEqual(result["numerically_audited_brackets"], 64)


if __name__ == "__main__":
    unittest.main()
