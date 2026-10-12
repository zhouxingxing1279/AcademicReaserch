import importlib
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verification"))


def _subject():
    return importlib.import_module("check_vertical_measurement_reset_obstruction")


class VerticalMeasurementResetObstructionTests(unittest.TestCase):
    def test_five_step_trajectory_is_exact_and_uses_admissible_primitives(self):
        witness = _subject().certificate()["five_step_physical_witness"]
        self.assertEqual(witness["vertical_velocity_after_success"], F(981, 2000))
        self.assertEqual(witness["vertical_position_after_success"], F(100981, 50000))
        self.assertTrue(witness["all_inputs_winds_and_states_admissible"])

    def test_successful_position_measurement_does_not_reset_true_velocity(self):
        reset = _subject().certificate()["reset_comparison"]
        self.assertEqual(reset["configured_initial_velocity_halfwidth"], F(1, 10))
        self.assertEqual(reset["strict_excess"], F(781, 2000))
        self.assertTrue(reset["same_absolute_initial_window_contract_rejected"])

    def test_measurement_is_exactly_consistent_with_witness(self):
        measurement = _subject().certificate()["successful_measurement"]
        self.assertEqual(measurement["position_noise"], F(0))
        self.assertTrue(measurement["truth_remains_in_posterior"])
        self.assertFalse(measurement["measurement_changes_physical_state"])

    def test_scope_requires_a_periodic_invariant_family(self):
        result = _subject().run()
        self.assertFalse(result["same_initial_window_reset_closure_proved"])
        self.assertTrue(result["measurement_only_reset_implication_rejected"])
        self.assertFalse(result["controlled_return_to_initial_box_impossible"])
        self.assertTrue(result["control_exists_quantifier_not_tested"])
        self.assertFalse(result["recursive_tube_invariance_proved"])
        self.assertEqual(
            result["next_required_object"],
            "causal_controlled_return_predecessor_over_observation_fibers",
        )


if __name__ == "__main__":
    unittest.main()
