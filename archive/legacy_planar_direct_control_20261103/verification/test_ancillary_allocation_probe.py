"""Regression tests for the explicit ancillary input-allocation probe."""
import unittest
from fractions import Fraction as F


class AncillaryAllocationProbeChecks(unittest.TestCase):
    def _subject(self):
        try:
            from check_ancillary_allocation_probe import run
        except ImportError as exc:
            self.fail(f"ancillary allocation probe is missing: {exc}")
        return run

    def test_explicit_split_respects_actual_actuator_box_exactly(self):
        result = self._subject()()

        self.assertEqual(result['status'], 'pass')
        self.assertEqual(result['nominal_input_lower'],
                         [F(1356943, 160000), F(0)])
        self.assertEqual(result['nominal_input_upper'],
                         [F(1782257, 160000), F(0)])
        self.assertEqual(result['correction_input_lower'],
                         [F(-572143, 160000), F(-2, 25)])
        self.assertEqual(result['correction_input_upper'],
                         [F(572143, 160000), F(2, 25)])
        self.assertTrue(result['minkowski_sum_within_actual_input_box'])
        self.assertEqual(result['minkowski_sum_lower'],
                         [F(981, 200), F(-2, 25)])
        self.assertEqual(result['minkowski_sum_upper'],
                         [F(2943, 200), F(2, 25)])

    def test_thrust_probe_has_exact_boundary_authority_but_no_margin(self):
        result = self._subject()()

        self.assertTrue(result['thrust']['widest_symmetric_hover_probe'])
        self.assertEqual(result['thrust']['positive_boundary_balance']['net_vz_increment_divided_by_h'], F(0))
        self.assertEqual(result['thrust']['negative_boundary_balance']['net_vz_increment_divided_by_h'], F(0))
        self.assertEqual(result['thrust']['robust_authority_margin'], F(0))
        self.assertFalse(result['usable_as_final_nominal_input_domain'])

    def test_torque_singleton_is_labelled_as_existence_probe_only(self):
        result = self._subject()()

        self.assertEqual(result['torque']['nominal_interval'], [F(0), F(0)])
        self.assertEqual(result['torque']['correction_interval'], [F(-2, 25), F(2, 25)])
        self.assertFalse(result['torque']['nominal_has_nonempty_interior'])
        self.assertEqual(result['evidence_level'],
                         'exact_input_budget_contract_not_an_rci_certificate')


if __name__ == '__main__':
    unittest.main()
