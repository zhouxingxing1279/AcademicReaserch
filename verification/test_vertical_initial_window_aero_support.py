import importlib
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verification"))


def _subject():
    return importlib.import_module("check_vertical_initial_window_aero_support")


class VerticalInitialWindowAeroSupportTests(unittest.TestCase):
    def test_fifteen_step_pitch_bound_uses_torque_dynamics(self):
        pitch = _subject().certificate()["pitch_projection"]
        self.assertEqual(pitch["absolute_upper_through_step_15"], F(22, 125))
        self.assertTrue(pitch["covers_every_admissible_torque_history"])

    def test_horizontal_velocity_projection_is_below_global_domain_bound(self):
        horizontal = _subject().certificate()["horizontal_velocity_projection"]
        self.assertEqual(horizontal["acceleration_absolute_upper"], F(222281, 50000))
        self.assertEqual(horizontal["velocity_absolute_upper_through_step_15"], F(716843, 500000))
        self.assertLess(horizontal["velocity_absolute_upper_through_step_15"], F(3))

    def test_reachable_vertical_aerodynamic_support_is_below_target(self):
        support = _subject().certificate()["vertical_aerodynamic_support"]
        self.assertEqual(support["upper"], F(15381098824149, 12500000000000))
        self.assertEqual(support["run168_target"] - support["upper"], F(1371915844271969, 10237500000000000))
        self.assertTrue(support["strictly_below_run168_target"])

    def test_scope_is_initial_window_not_recursive_tube(self):
        result = _subject().run()
        self.assertTrue(result["initial_fifteen_step_window_aero_support_certified"])
        self.assertFalse(result["measurement_conditioned_reset_closure_proved"])
        self.assertFalse(result["recursive_tube_invariance_proved"])
        self.assertFalse(result["is_recursive_feasibility_proof"])


if __name__ == "__main__":
    unittest.main()
