"""Exact regressions for the shifted reachable-set inclusion contract."""
import unittest
from fractions import Fraction as Q

from check_shifted_reachable_inclusion import (
    AffineBox,
    reachable_sequence,
    shifted_inclusion_certificate,
    template_sandwich,
    run,
)


class ShiftedReachableContracts(unittest.TestCase):
    def test_absolute_posterior_intersection_contracts(self):
        prior = AffineBox([Q(1)], [Q(2)])
        posterior = prior.intersect(AffineBox([Q(2)], [Q(1, 2)]))
        self.assertTrue(prior.encloses(posterior))
        self.assertEqual(posterior.center, (Q(2),))
        self.assertEqual(posterior.radius, (Q(1, 2),))

    def test_center_shift_cannot_be_ignored(self):
        old = AffineBox([Q(0)], [Q(1)])
        smaller_radius_but_shifted = AffineBox([Q(1)], [Q(1, 2)])
        self.assertFalse(old.encloses(smaller_radius_but_shifted))
        self.assertEqual(old.inclusion_margins(smaller_radius_but_shifted), (Q(-1, 2),))

    def test_same_shifted_control_and_nested_disturbance_preserve_inclusion(self):
        old = AffineBox([Q(0)], [Q(2)])
        new = AffineBox([Q(1, 4)], [Q(1)])
        f, b = [[Q(1)]], [[Q(1)]]
        old_w = AffineBox([Q(0)], [Q(1, 2)])
        new_w = AffineBox([Q(0)], [Q(1, 4)])
        cert = shifted_inclusion_certificate(
            old, new, f, b,
            old_controls=[[Q(1)], [Q(-1)], [Q(0)]],
            new_controls=[[Q(-1)], [Q(0)]],
            old_disturbances=[old_w, old_w, old_w],
            new_disturbances=[new_w, new_w],
        )
        self.assertTrue(cert['assumptions']['posterior_in_old_stage_one'])
        self.assertTrue(cert['assumptions']['same_shifted_control_tail'])
        self.assertTrue(cert['assumptions']['nested_disturbances'])
        self.assertTrue(cert['all_stage_inclusions'])

    def test_changed_control_breaks_the_reference_inclusion(self):
        initial = AffineBox([Q(0)], [Q(0)])
        zero_w = AffineBox([Q(0)], [Q(0)])
        cert = shifted_inclusion_certificate(
            initial, initial, [[Q(1)]], [[Q(1)]],
            old_controls=[[Q(0)], [Q(0)]],
            new_controls=[[Q(2)]],
            old_disturbances=[zero_w, zero_w],
            new_disturbances=[zero_w],
        )
        self.assertFalse(cert['assumptions']['same_shifted_control_tail'])
        self.assertFalse(cert['all_stage_inclusions'])

    def test_larger_disturbance_breaks_inclusion(self):
        initial = AffineBox([Q(0)], [Q(0)])
        old_w = AffineBox([Q(0)], [Q(1)])
        new_w = AffineBox([Q(0)], [Q(2)])
        cert = shifted_inclusion_certificate(
            initial, initial, [[Q(1)]], [[Q(0)]],
            old_controls=[[Q(0)], [Q(0)]],
            new_controls=[[Q(0)]],
            old_disturbances=[old_w, old_w],
            new_disturbances=[new_w],
        )
        self.assertFalse(cert['assumptions']['nested_disturbances'])
        self.assertFalse(cert['all_stage_inclusions'])

    def test_no_measurement_is_identity_not_artificial_contraction(self):
        prediction = AffineBox([Q(3, 2)], [Q(7, 5)])
        self.assertIs(prediction.update_without_measurement(), prediction)

    def test_template_sandwich_requires_both_valid_caps(self):
        beta = [Q(3), Q(7)]
        old = [Q(5), Q(6)]
        self.assertEqual(template_sandwich(beta, old), (Q(3), Q(6)))

    def test_reachable_sequence_has_declared_length(self):
        sequence = reachable_sequence(
            AffineBox([Q(0)], [Q(1)]), [[Q(1)]], [[Q(0)]],
            [[Q(0)], [Q(0)]], [AffineBox([Q(0)], [Q(1)])] * 2,
        )
        self.assertEqual(len(sequence), 3)

    def test_six_state_declared_contract_passes_but_control_gate_stays_blocked(self):
        result = run()
        self.assertEqual(result['status'], 'pass')
        self.assertEqual(
            result['shifted_reachable_gate'],
            'pass_for_declared_affine_contract',
        )
        self.assertEqual(
            result['recursive_feasibility_gate'],
            'blocked_pending_control_terminal_certificate',
        )
        self.assertEqual({case['name'] for case in result['cases']},
                         {'position_success', 'position_miss'})
        self.assertTrue(all(case['all_stage_inclusions'] for case in result['cases']))
        self.assertTrue(all(case['checked_stages'] == 26 for case in result['cases']))
        self.assertFalse(result['counterexamples']['changed_control']['all_stage_inclusions'])
        self.assertFalse(result['counterexamples']['larger_disturbance']['all_stage_inclusions'])
        self.assertFalse(result['counterexamples']['radius_only_center_omission']['included'])


if __name__ == '__main__':
    unittest.main()
