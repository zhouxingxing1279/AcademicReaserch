import importlib
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction as F


ROOT = Path(__file__).resolve().parents[1]


def _subject():
    try:
        return importlib.import_module("check_vertical_joint_predecessor")
    except ModuleNotFoundError:
        return None


class VerticalJointPredecessorTests(unittest.TestCase):
    def test_joint_candidate_accepts_the_run143_correlated_success_witness(self):
        """Reintroducing the rejected independent d limit must fail this test."""
        subject = _subject()
        contains = getattr(subject, "joint_candidate_contains", None)

        self.assertTrue(callable(contains))
        self.assertTrue(contains(
            0,
            (F(-1, 50), F(-64124993, 288000000)),
            (F(23312147, 48000000), F(9237859, 4500000)),
        ))

    def test_critical_fibers_have_a_positive_volume_inner_box(self):
        """A single d witness or zero-width fiber is not a nonempty joint predecessor."""
        subject = _subject()
        certify = getattr(subject, "critical_mode_predecessors", None)

        self.assertTrue(callable(certify))
        result = certify()
        self.assertEqual(result["observation_halfwidths"], (F(1, 5), F(1, 4)))
        self.assertEqual(result.get("tracking_error_limits"), (F(1), F(11, 4)))
        self.assertEqual(set(result["modes"]), {4, 9, 14})
        for mode in (4, 9, 14):
            row = result["modes"][mode]
            self.assertTrue(row["positive_volume_inner_certificate"])
            self.assertEqual(row.get("joint_inner_dimension"), 4)
            self.assertGreater(row.get("eta_projection_area", F(0)), 0)
            self.assertGreater(row["current_fiber_position_slack"], 0)
            self.assertGreater(row["current_fiber_velocity_slack"], 0)
            self.assertGreater(row["next_tracking_position_slack"], 0)
            self.assertGreater(row["next_tracking_velocity_slack"], 0)

        self.assertEqual(
            result["modes"][14]["next_tracking_position_slack"],
            F(14847853, 48000000),
        )
        self.assertEqual(
            result["modes"][14]["next_tracking_velocity_slack"],
            F(22053067447, 57600000000),
        )

    def test_mode_four_and_nine_unknown_branches_share_one_input(self):
        """Assigning one correction to success and another to miss must fail."""
        subject = _subject()
        result = getattr(subject, "critical_mode_predecessors", lambda: {})()

        for mode, miss_target in ((4, 5), (9, 10)):
            row = result.get("modes", {}).get(mode, {})
            self.assertEqual(row.get("shared_correction_thrust"), F(0))
            self.assertEqual(row.get("policy_values_on_inner_box"), 1)
            self.assertEqual(
                {(edge["target"], edge["label"]) for edge in row.get("edges", [])},
                {(miss_target, "miss"), (0, "success")},
            )
            self.assertTrue(all(edge["eta_target_contained"] for edge in row["edges"]))

    def test_mode_fourteen_forced_success_predecessor_is_nonempty(self):
        """The old product-d obstruction must not empty the corrected joint candidate."""
        subject = _subject()
        result = getattr(subject, "critical_mode_predecessors", lambda: {})()
        row = result.get("modes", {}).get(14, {})

        self.assertEqual(row.get("shared_correction_thrust"), F(0))
        self.assertEqual(
            [(edge["target"], edge["label"]) for edge in row.get("edges", [])],
            [(0, "success")],
        )
        self.assertTrue(row["edges"][0]["eta_target_contained"])
        self.assertTrue(row.get("positive_volume_inner_certificate"))

    def test_residual_bound_is_tied_to_the_same_actual_thrust(self):
        """Using a detached or independently sampled residual width must fail."""
        subject = _subject()
        result = getattr(subject, "critical_mode_predecessors", lambda: {})()

        self.assertEqual(
            result.get("nominal_thrust_interval"),
            (F(1356943, 160000), F(1782257, 160000)),
        )
        self.assertEqual(result.get("shared_correction_thrust"), F(0))
        self.assertEqual(
            result.get("residual_halfwidth_at_actual_thrust_upper"),
            F(411370817, 128000000),
        )
        self.assertLess(
            result["residual_halfwidth_at_actual_thrust_upper"],
            result["run136_certified_residual_halfwidth"],
        )
        self.assertEqual(
            result["modes"][14]["edges"][0].get(
                "minimum_eta_residual_sensitive_facet_slack"
            ),
            F(471323459, 320),
        )

    def test_artifact_limits_claim_to_one_step_nonemptiness(self):
        """The checker must not relabel a local inner certificate as an RCI."""
        subject = _subject()
        run = getattr(subject, "run", None)

        self.assertTrue(callable(run))
        result = run()
        self.assertEqual(result["status"], "pass")
        self.assertEqual(
            result["evidence_level"],
            "exact_positive_volume_inner_certificate_for_three_critical_one_step_predecessors",
        )
        self.assertFalse(result["is_rci_certificate"])
        self.assertFalse(result["fixed_point_iteration_run"])
        self.assertFalse(result["full_six_state_guarantee"])

    def test_checker_writes_hash_bound_exact_artifact(self):
        """An unarchived or source-unbound result cannot support the research claim."""
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "checks.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "verification/check_vertical_joint_predecessor.py"),
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
            self.assertIn(
                "verification/check_vertical_joint_predecessor.py",
                artifact["source_sha256"],
            )
            for dependency in (
                "verification/check_mode_nestedness.py",
                "verification/check_mode_radius.py",
                "verification/check_intermittent_metric.py",
            ):
                self.assertEqual(
                    artifact["source_sha256"].get(dependency),
                    hashlib.sha256((ROOT / dependency).read_bytes()).hexdigest(),
                )
            self.assertEqual(
                artifact["critical_modes"]["14"]["edges"][0]["label"],
                "success",
            )


if __name__ == "__main__":
    unittest.main()
