import hashlib
import importlib
import json
from fractions import Fraction as F
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
VERIFICATION = ROOT / "verification"


def _subject():
    if str(VERIFICATION) not in sys.path:
        sys.path.insert(0, str(VERIFICATION))
    return importlib.import_module("check_vertical_full_cycle_input_authority")


class VerticalFullCycleInputAuthorityTests(unittest.TestCase):
    def test_first_policy_independent_position_failure_is_miss_thirteen(self):
        subject = _subject()
        result = getattr(subject, "full_cycle_authority_certificate", lambda: {})()

        self.assertEqual(result.get("source_seed"), "J14")
        self.assertEqual(result.get("first_infeasible_miss_count"), 13)
        self.assertEqual(
            result.get("steps", {}).get(12, {}).get("position_lower_bound"),
            F(398207933, 400000000),
        )
        self.assertEqual(
            result.get("steps", {}).get(13, {}).get("position_lower_bound"),
            F(934206607, 900000000),
        )
        self.assertEqual(
            result.get("steps", {}).get(13, {}).get("strict_excess"),
            F(34206607, 900000000),
        )

    def test_relaxed_full_state_causal_policy_is_still_infeasible(self):
        subject = _subject()
        result = getattr(subject, "run", lambda: {})()

        self.assertEqual(
            result.get("evidence_level"),
            "exact_policy_independent_full_cycle_position_diameter_obstruction",
        )
        self.assertTrue(result.get("arbitrary_causal_bounded_policy_ruled_out"))
        self.assertTrue(result.get("full_state_feedback_relaxation_ruled_out"))
        self.assertFalse(result.get("different_seed_ruled_out"))
        self.assertFalse(result.get("scheduled_residual_ruled_out"))
        self.assertFalse(result.get("is_rci_certificate"))

    def test_checker_writes_hash_bound_exact_artifact(self):
        subject_path = ROOT / "verification/check_vertical_full_cycle_input_authority.py"
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
                / "results/theory_vertical_full_cycle_input_authority_20261011/exact_checks.json"
            ).read_text())
            self.assertEqual(generated, archived)
            self.assertTrue({
                "verification/check_vertical_correlated_return_seed.py",
                "verification/check_mode_radius.py",
                "verification/check_mode_nestedness.py",
                "verification/check_vertical_joint_predecessor.py",
            }.issubset(generated["source_sha256"]))
            for name, digest in generated["source_sha256"].items():
                self.assertEqual(
                    digest,
                    hashlib.sha256((ROOT / name).read_bytes()).hexdigest(),
                )


if __name__ == "__main__":
    unittest.main()
