import importlib
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def _subject():
    try:
        return importlib.import_module("check_mode4_unknown_branch_lifted_cell")
    except ModuleNotFoundError:
        return None


class ModeFourUnknownBranchLiftedCellTests(unittest.TestCase):
    def test_one_visible_policy_is_shared_before_the_unknown_label(self):
        """Separate miss/success policies would violate the information timing."""
        subject = _subject()
        certify = getattr(subject, "mode4_unknown_branch_certificate", None)

        self.assertTrue(callable(certify))
        result = certify()
        self.assertFalse(result["policy_uses_hidden_eta"])
        self.assertFalse(result["policy_uses_future_edge_label"])
        self.assertEqual(result["affine_fibre_policy"]["offset"], F(0))
        self.assertEqual(result["policy_values_before_label"], 1)
        self.assertEqual(
            {(row["target_mode"], row["edge_label"]) for row in result["branches"]},
            {(5, "miss"), (0, "success")},
        )

    def test_every_estimator_and_tracking_target_normal_closes(self):
        """Dropping either branch or checking only coordinate boxes must fail."""
        subject = _subject()
        result = getattr(subject, "mode4_unknown_branch_certificate", lambda: {})()

        branches = {row["edge_label"]: row for row in result.get("branches", [])}
        self.assertEqual(set(branches), {"miss", "success"})
        self.assertEqual(branches["miss"]["target_normal_count"], 18)
        self.assertEqual(branches["success"]["target_normal_count"], 8)
        for branch in branches.values():
            rows = branch["eta_target_normal_rows"] + branch["tracking_target_normal_rows"]
            self.assertTrue(all(row["slack"] >= 0 for row in rows))
            self.assertTrue(branch["branch_closed"])
        self.assertTrue(result["both_unknown_branches_closed"])

    def test_success_noise_and_physical_residual_have_correct_shared_roles(self):
        """Measurement innovation must cancel from e, while one residual drives eta and e."""
        subject = _subject()
        result = getattr(subject, "mode4_unknown_branch_certificate", lambda: {})()

        self.assertEqual(result.get("measurement_noise_halfwidth"), F(1, 50))
        self.assertTrue(result.get("shared_actual_thrust_residual_law"))
        self.assertEqual(
            result.get("residual_halfwidth_at_actual_thrust_upper"),
            F(411370817, 128000000),
        )
        success = next(row for row in result["branches"] if row["edge_label"] == "success")
        miss = next(row for row in result["branches"] if row["edge_label"] == "miss")
        for branch in (miss, success):
            self.assertIn("joint_primitive_columns", branch)
            columns = {row["label"]: row["vector"] for row in branch["joint_primitive_columns"]}
            residual = columns["rho_z"]
            self.assertEqual(residual[:2], (F(0), F(411370817, 6400000000)))
            self.assertEqual(residual[2:], residual[:2])
            self.assertTrue(branch["shared_residual_identity_verified"])
        self.assertTrue(success["success_measurement_noise_propagated"])
        success_columns = {
            row["label"]: row["vector"] for row in success["joint_primitive_columns"]
        }
        self.assertEqual(
            success_columns["n_pz"],
            (F(-1, 50), F(-9, 100), F(0), F(0)),
        )
        self.assertTrue(any(row["noise_support"] > 0 for row in success["eta_target_normal_rows"]))
        self.assertTrue(all(row["noise_support"] == 0 for row in success["tracking_target_normal_rows"]))
        self.assertTrue(success["measurement_innovation_cancels_from_tracking_error"])
        self.assertTrue(success["measurement_cancellation_identity_verified"])

    def test_source_positive_volume_includes_exact_estimator_area(self):
        """Positive d widths alone must not certify a four-dimensional source cell."""
        subject = _subject()
        result = getattr(subject, "mode4_unknown_branch_certificate", lambda: {})()

        self.assertEqual(
            result.get("eta_projection_area"),
            F(41105550110953, 240000000000000),
        )
        self.assertTrue(result.get("positive_volume_source_cell"))
        self.assertTrue(result.get("both_unknown_branches_closed"))

    def test_scope_stays_at_a_two_edge_one_step_certificate(self):
        subject = _subject()
        run = getattr(subject, "run", None)

        self.assertTrue(callable(run))
        result = run()
        self.assertEqual(
            result["evidence_level"],
            "exact_two_edge_unknown_label_target_normal_support_certificate",
        )
        self.assertFalse(result["is_rci_certificate"])
        self.assertFalse(result["terminal_family_closed"])
        self.assertFalse(result["recursive_feasibility_certified"])
        self.assertFalse(result["full_six_state_guarantee"])

    def test_checker_writes_hash_bound_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "exact_checks.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "verification/check_mode4_unknown_branch_lifted_cell.py"),
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
            archived = json.loads((
                ROOT
                / "results/theory_mode4_unknown_branch_lifted_cell_20261026/exact_checks.json"
            ).read_text())
            self.assertEqual(artifact, archived)
            self.assertIn(
                "verification/check_mode4_unknown_branch_lifted_cell.py",
                artifact["source_sha256"],
            )
            for name, digest in artifact["source_sha256"].items():
                self.assertEqual(
                    digest,
                    hashlib.sha256((ROOT / name).read_bytes()).hexdigest(),
                )


if __name__ == "__main__":
    unittest.main()
