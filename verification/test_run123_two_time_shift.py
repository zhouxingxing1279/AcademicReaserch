import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


from verification.check_run123_two_time_shift import verify_two_time_shift


class TwoTimeShiftTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = verify_two_time_shift()

    def test_causal_posterior_adds_one_disturbance_and_one_measurement(self):
        posterior = self.result["causal_posterior"]
        self.assertEqual(posterior["old_latent_dimension"], 601)
        self.assertEqual(posterior["new_latent_dimension"], 602)
        self.assertEqual(posterior["impulse_prefix_max_power"], 601)
        self.assertTrue(posterior["is_complete_impulse_prefix"])
        self.assertTrue(posterior["prediction_generators_match"])
        self.assertTrue(posterior["inherited_measurement_rows_match"])
        self.assertTrue(posterior["new_measurement_row_matches_prediction"])
        self.assertEqual(posterior["measurement_row_rank"], 3)
        self.assertTrue(posterior["nonempty"])
        self.assertAlmostEqual(
            posterior["absolute_position_measurement"],
            posterior["nominal_successor_position"]
            + posterior["position_measurement_residual"],
            places=15,
        )

    def test_measurement_intersection_is_aligned_with_old_nominal_successor(self):
        transfer = self.result["set_transfer"]
        self.assertLessEqual(transfer["maximum_support_excess"], 1e-9)
        self.assertEqual(transfer["checked_direction_count"], 300)
        self.assertEqual(transfer["alignment"], "old_nominal_successor")

    def test_shifted_candidate_preserves_all_robust_constraints(self):
        shifted = self.result["shifted_candidate"]
        self.assertTrue(self.result["old_candidate"]["solver_success"])
        self.assertLess(self.result["old_candidate"]["terminal_inf_norm"], 1e-12)
        self.assertAlmostEqual(shifted["appended_nominal_input"], 0.0, places=15)
        self.assertLess(shifted["terminal_inf_norm"], 1e-12)
        self.assertGreaterEqual(shifted["minimum_robust_slack"], -1e-9)
        self.assertTrue(shifted["terminal_append_covered_by_run121_rpi"])

    def test_scope_does_not_overclaim_recursive_feasibility(self):
        self.assertEqual(self.result["evidence_level"], "one_step_numerical_baseline")
        self.assertIn("not", self.result["scope_warning"].lower())

    def test_script_is_directly_executable_from_repository_root(self):
        root = Path(__file__).resolve().parents[1]
        environment = os.environ.copy()
        environment["ACADEMIC_RESEARCH_NO_WRITE"] = "1"
        with tempfile.TemporaryDirectory() as temporary_directory:
            completed = subprocess.run(
                [sys.executable, str(root / "verification/check_run123_two_time_shift.py")],
                cwd=temporary_directory,
                env=environment,
                capture_output=True,
                text=True,
                timeout=30,
            )
        self.assertEqual(completed.returncode, 0, completed.stderr)


if __name__ == "__main__":
    unittest.main()
