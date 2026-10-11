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
        return importlib.import_module("check_vertical_affine_shared_branch")
    except ModuleNotFoundError:
        try:
            return importlib.import_module(
                "verification.check_vertical_affine_shared_branch"
            )
        except ModuleNotFoundError:
            return None


class VerticalAffineSharedBranchTests(unittest.TestCase):
    def test_one_mode_nine_gain_is_shared_by_success_and_miss(self):
        subject = _subject()
        result = getattr(subject, "shared_branch_certificate", lambda: {})()

        self.assertEqual(result.get("source_label"), (9, 15))
        self.assertEqual(result.get("position_gain"), F(0))
        self.assertEqual(result.get("velocity_gain"), F(-114428600, 70527869))
        self.assertEqual(result.get("input_support"), F(572143, 160000))
        self.assertEqual(result.get("branch_policy_count"), 1)
        self.assertEqual(set(result.get("branches", {})), {"miss", "success"})

    def test_both_branches_share_exact_true_error_supports(self):
        subject = _subject()
        result = getattr(subject, "shared_branch_certificate", lambda: {})()
        expected_position = F(85072353058880561, 87379729200000000)
        expected_velocity = F(4751967529055069, 1747594584000000)

        for label in ("miss", "success"):
            row = result.get("branches", {}).get(label, {})
            self.assertEqual(row.get("tracking_position_halfwidth"), expected_position)
            self.assertEqual(row.get("tracking_velocity_halfwidth"), expected_velocity)
            self.assertTrue(row.get("tracking_hard_box_satisfied"))
            self.assertTrue(row.get("estimator_target_contained"))

    def test_claim_stops_before_recurrent_target_inclusion(self):
        subject = _subject()
        result = getattr(subject, "run", lambda: {})()

        self.assertEqual(
            result.get("evidence_level"),
            "exact_one_step_shared_success_miss_safety_witness_after_affine_rescue",
        )
        self.assertTrue(result.get("shared_branch_state_input_safety_certified"))
        self.assertFalse(result.get("recurrent_target_inclusion_certified"))
        self.assertFalse(result.get("is_rci_certificate"))
        self.assertFalse(result.get("recursive_feasibility_certified"))

    def test_checker_writes_hash_bound_exact_artifact(self):
        subject_path = ROOT / "verification/check_vertical_affine_shared_branch.py"
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "exact_checks.json"
            completed = subprocess.run(
                [sys.executable, str(subject_path), "--output", str(output)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            generated = json.loads(output.read_text())
            archived = json.loads((
                ROOT
                / "results/theory_vertical_affine_shared_branch_20261011/exact_checks.json"
            ).read_text())
            self.assertEqual(generated, archived)
            for name, digest in generated["source_sha256"].items():
                self.assertEqual(
                    digest,
                    hashlib.sha256((ROOT / name).read_bytes()).hexdigest(),
                )


if __name__ == "__main__":
    unittest.main()
