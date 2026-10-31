"""Run222 exact-rational obstruction tests."""
import unittest
from fractions import Fraction as Q
from pathlib import Path

import check_four_state_terminal_obstruction as m


class FourStateTerminalObstructionTests(unittest.TestCase):
    def test_exact_positive_drift(self):
        self.assertEqual(m.growth_lower_bound(), Q(3905869, 3200000))
        self.assertGreater(m.growth_lower_bound(), 0)

    def test_strict_crossing_from_zero(self):
        d = m.H * m.growth_lower_bound()
        self.assertEqual(m.first_exceedance(Q(0), d), 123)
        self.assertLessEqual(122*d, m.V_LIMIT)
        self.assertGreater(123*d, m.V_LIMIT)

    def test_uniform_crossing_from_any_bounded_velocity(self):
        d = m.H * m.growth_lower_bound()
        self.assertEqual(m.first_exceedance(-m.V_LIMIT, d), 246)
        for start in (-m.V_LIMIT, -Q(1), Q(0), Q(1), m.V_LIMIT):
            self.assertGreater(start + 246*d, m.V_LIMIT)

    def test_stronger_tilt_or_smaller_disturbance_changes_obstruction(self):
        self.assertLess(m.growth_lower_bound(phi_radius=Q(1, 4)), 0)
        self.assertLess(m.growth_lower_bound(r0=Q(0), rt=Q(0)), 0)
        self.assertGreater(m.R0/m.T_MAX + m.R_T, m.ZF_PHI+m.E_PHI)

    def test_report_is_not_full_system_certificate(self):
        r = m.verify()
        self.assertFalse(r['nonempty_robust_invariant_subset_of_attitude_strip_and_bounded_vx'])
        self.assertEqual(r['gate_A'], 'blocked')
        self.assertEqual(r['steps_to_violate_from_vx_minus_three'], 246)

    def test_real_repository_config(self):
        root = Path(__file__).resolve().parents[1]
        if (root/'configs/planar_baseline.json').exists():
            self.assertTrue(m.config_contract(root))
        else:
            self.skipTest('full checkout required; CI must execute this check')


if __name__ == '__main__':
    unittest.main()
