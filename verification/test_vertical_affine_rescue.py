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
        return importlib.import_module("check_vertical_affine_rescue")
    except ModuleNotFoundError:
        try:
            return importlib.import_module("verification.check_vertical_affine_rescue")
        except ModuleNotFoundError:
            return None


class VerticalAffineRescueTests(unittest.TestCase):
    def test_exact_velocity_only_gains_fit_input_and_true_velocity_boxes(self):
        subject = _subject()
        result = getattr(subject, "affine_rescue_certificate", lambda: {})()

        expected = {
            9: {
                "predecessor_age": 13,
                "visible_velocity_halfwidth": F(45315007, 32000000),
                "velocity_gain": F(-114428600, 45315007),
                "successor_velocity_halfwidth": F(8857197898290289, 3262680504000000),
                "velocity_margin": F(115173487709711, 3262680504000000),
            },
            14: {
                "predecessor_age": 8,
                "visible_velocity_halfwidth": F(72816441, 32000000),
                "velocity_gain": F(-114428600, 72816441),
                "successor_velocity_halfwidth": F(4732194266975069, 1747594584000000),
                "velocity_margin": F(73690839024931, 1747594584000000),
            },
        }
        for seed, values in expected.items():
            row = result.get("critical_predecessors", {}).get(seed, {})
            for key, value in values.items():
                self.assertEqual(row.get(key), value)
            self.assertEqual(row.get("position_gain"), F(0))
            self.assertEqual(row.get("input_support"), F(572143, 160000))
            self.assertTrue(row.get("robust_input_box_satisfied"))
            self.assertTrue(row.get("successor_true_velocity_box_satisfied"))

    def test_rescue_is_applied_before_the_reported_failing_miss(self):
        subject = _subject()
        result = getattr(subject, "run", lambda: {})()

        self.assertEqual(result.get("failure_miss_counts"), {9: 14, 14: 9})
        self.assertEqual(result.get("rescue_source_ages"), {9: 13, 14: 8})
        self.assertTrue(result.get("rescue_edges_are_deterministic_miss_edges"))
        self.assertFalse(result.get("same_step_success_miss_branching_required"))

    def test_claim_is_only_a_one_step_feasibility_witness(self):
        subject = _subject()
        result = getattr(subject, "run", lambda: {})()

        self.assertEqual(
            result.get("evidence_level"),
            "exact_one_step_affine_in_visible_velocity_rescue_witness",
        )
        self.assertTrue(result.get("critical_zero_policy_excess_eliminated"))
        self.assertFalse(result.get("gain_optimality_claimed"))
        self.assertFalse(result.get("target_inclusion_certified"))
        self.assertFalse(result.get("shared_branch_successor_certified"))
        self.assertFalse(result.get("is_rci_certificate"))
        self.assertFalse(result.get("recursive_feasibility_certified"))

    def test_checker_writes_hash_bound_exact_artifact(self):
        subject_path = ROOT / "verification/check_vertical_affine_rescue.py"
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
                / "results/theory_vertical_affine_rescue_20261011/exact_checks.json"
            ).read_text())
            self.assertEqual(generated, archived)
            for name, digest in generated["source_sha256"].items():
                self.assertEqual(
                    digest,
                    hashlib.sha256((ROOT / name).read_bytes()).hexdigest(),
                )


if __name__ == "__main__":
    unittest.main()
