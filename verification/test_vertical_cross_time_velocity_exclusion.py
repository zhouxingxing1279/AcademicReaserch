import importlib
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verification"))


def _subject():
    return importlib.import_module("check_vertical_cross_time_velocity_exclusion")


class VerticalCrossTimeVelocityExclusionTests(unittest.TestCase):
    def test_rational_cosine_and_sqrt_bounds_are_certified(self):
        bounds = _subject().certificate()["elementary_bounds"]
        self.assertTrue(bounds["cos_9_over_20_strictly_above_9_over_10"])
        self.assertTrue(bounds["sqrt_1229_over_100_strictly_below_351_over_100"])

    def test_global_vertical_acceleration_lower_bound(self):
        acceleration = _subject().certificate()["vertical_acceleration"]
        self.assertEqual(acceleration["lower_bound"], F(-28953, 4000))
        self.assertTrue(acceleration["valid_for_every_domain_state_input_and_wind"])

    def test_fifteen_step_induction_excludes_run169_velocity(self):
        reachable = _subject().certificate()["cross_time_projection"]
        self.assertEqual(reachable["vz_lower_after_15_steps"], F(-90859, 40000))
        self.assertGreater(reachable["vz_lower_after_15_steps"], reachable["run169_vz"])
        self.assertTrue(reachable["run169_vz_excluded"])

    def test_scope_does_not_upgrade_projection_to_full_reachability(self):
        result = _subject().run()
        self.assertTrue(result["run169_velocity_witness_excluded_from_15_step_reachable_projection"])
        self.assertFalse(result["full_nonlinear_reachable_set_computed"])
        self.assertFalse(result["all_aerodynamic_threshold_violations_excluded"])
        self.assertFalse(result["is_recursive_feasibility_proof"])


if __name__ == "__main__":
    unittest.main()
