import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction as F

import check_joint_information_semantics as semantics


ROOT = Path(__file__).resolve().parents[1]


class JointInformationSemanticsTests(unittest.TestCase):
    def test_checker_writes_a_passing_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "checks.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "verification/check_joint_information_semantics.py"),
                    "--output",
                    str(output),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            artifact = json.loads(output.read_text())
            self.assertEqual(artifact["status"], "pass")
            self.assertEqual(
                artifact["evidence_level"],
                "exact_counterexample_to_product_threshold_as_joint_necessity",
            )
            self.assertFalse(
                artifact["miss_path_fiber"][
                    "threshold_is_reachable_on_initial_miss_path"
                ]
            )
            self.assertTrue(
                artifact["joint_target_counterexample"][
                    "product_threshold_not_joint_necessary"
                ]
            )
            self.assertIn(
                "verification/check_joint_information_semantics.py",
                artifact["source_sha256"],
            )

    def test_miss_path_preserves_the_full_mode14_q_fiber(self):
        certificate = getattr(semantics, "miss_path_fiber_certificate", lambda: {})()

        self.assertEqual(
            certificate.get("conditional_q_halfwidth"),
            F(23312147, 48000000),
        )
        self.assertEqual(
            certificate.get("product_threshold"),
            F(57902137, 162000000),
        )
        self.assertEqual(
            certificate.get("strict_excess"),
            F(166210873, 1296000000),
        )
        self.assertTrue(certificate.get("same_observation_for_entire_fiber"))
        self.assertFalse(certificate.get("threshold_is_reachable_on_initial_miss_path"))

    def test_success_measurement_spread_cancels_from_tracking_velocity(self):
        split = getattr(semantics, "success_velocity_split", lambda *args: {})(
            F(1, 10), F(1, 5), F(-1, 4), F(3, 2), F(-2), F(1, 50)
        )
        reflected = getattr(semantics, "success_velocity_split", lambda *args: {})(
            F(-1, 10), F(1, 5), F(-1, 4), F(3, 2), F(-2), F(-1, 50)
        )

        self.assertEqual(split.get("q"), F(13, 125))
        self.assertEqual(split.get("eta_velocity_next"), F(-199, 500))
        self.assertEqual(split.get("d_velocity_next"), F(169, 500))
        self.assertEqual(split.get("tracking_velocity_next"), F(-3, 50))
        self.assertNotEqual(
            split.get("eta_velocity_next"), reflected.get("eta_velocity_next")
        )
        self.assertNotEqual(
            split.get("d_velocity_next"), reflected.get("d_velocity_next")
        )
        self.assertEqual(reflected.get("tracking_velocity_next"), F(-3, 50))

    def test_product_threshold_is_not_necessary_for_a_joint_target(self):
        witness = getattr(semantics, "joint_target_counterexample", lambda: {})()

        self.assertEqual(witness.get("q"), F(23312147, 48000000))
        self.assertEqual(witness.get("eta_velocity_next"), F(-64124993, 288000000))
        self.assertEqual(witness.get("d_velocity_next"), F(72816441, 32000000))
        self.assertEqual(witness.get("tracking_velocity_next"), F(9237859, 4500000))
        self.assertEqual(
            witness.get("product_d_velocity_limit"), F(61142137, 36000000)
        )
        self.assertTrue(witness.get("q_product_threshold_violated"))
        self.assertTrue(witness.get("product_d_velocity_limit_violated"))
        self.assertTrue(witness.get("eta_target_in_mode0_box"))
        self.assertTrue(witness.get("tracking_target_in_source_domain"))
        self.assertTrue(witness.get("product_threshold_not_joint_necessary"))


if __name__ == "__main__":
    unittest.main()
