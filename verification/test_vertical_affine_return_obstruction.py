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
        return importlib.import_module("check_vertical_affine_return_obstruction")
    except ModuleNotFoundError:
        try:
            return importlib.import_module(
                "verification.check_vertical_affine_return_obstruction"
            )
        except ModuleNotFoundError:
            return None


class VerticalAffineReturnObstructionTests(unittest.TestCase):
    def test_two_bounded_affine_corrections_cannot_save_mode_eleven_position(self):
        subject = _subject()
        result = getattr(subject, "return_obstruction_certificate", lambda: {})()

        self.assertEqual(result.get("source_label"), (8, 15))
        self.assertEqual(result.get("checked_target_mode"), 11)
        self.assertEqual(
            result.get("zero_correction_position_halfwidth"),
            F(3714127151, 3600000000),
        )
        self.assertEqual(
            result.get("best_case_position_lower_bound"),
            F(369867929, 360000000),
        )
        self.assertEqual(
            result.get("strict_position_excess"),
            F(9867929, 360000000),
        )
        self.assertTrue(result.get("fixed_age_eight_source_affine_policy_class_infeasible"))

    def test_claim_stops_at_the_frozen_path_and_policy_class(self):
        subject = _subject()
        result = getattr(subject, "run", lambda: {})()

        self.assertEqual(
            result.get("evidence_level"),
            "exact_three_miss_position_support_lower_bound",
        )
        self.assertFalse(result.get("general_output_feedback_infeasibility"))
        self.assertFalse(result.get("is_rci_certificate"))
        self.assertFalse(result.get("recursive_feasibility_certified"))
        self.assertTrue(result.get("age_eight_source_fixed_after_zero_prior_corrections"))
        self.assertTrue(result.get("fixed_global_residual_assumed"))
        self.assertTrue(result.get("centered_affine_policy_only"))
        self.assertFalse(result.get("earlier_feedback_ruled_out"))

    def test_checker_writes_hash_bound_exact_artifact(self):
        subject_path = ROOT / "verification/check_vertical_affine_return_obstruction.py"
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
                / "results/theory_vertical_affine_return_obstruction_20261011/exact_checks.json"
            ).read_text())
            self.assertEqual(generated, archived)
            for name, digest in generated["source_sha256"].items():
                self.assertEqual(
                    digest,
                    hashlib.sha256((ROOT / name).read_bytes()).hexdigest(),
                )
            self.assertTrue({
                "verification/check_cycle_lifted_zonotope.py",
                "verification/check_vertical_affine_rescue.py",
                "verification/check_vertical_translated_template_obstruction.py",
            }.issubset(generated["source_sha256"]))

if __name__ == "__main__":
    unittest.main()
