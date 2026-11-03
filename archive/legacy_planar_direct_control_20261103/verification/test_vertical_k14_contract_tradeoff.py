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
VERIFICATION = ROOT / "verification"


def _subject():
    if str(VERIFICATION) not in sys.path:
        sys.path.insert(0, str(VERIFICATION))
    return importlib.import_module("check_vertical_k14_contract_tradeoff")


class VerticalK14ContractTradeoffTests(unittest.TestCase):
    def test_exact_k14_tradeoff_and_single_factor_thresholds(self):
        result = _subject().k14_tradeoff_certificate()

        self.assertEqual(result["seed_direction_support"], F(3889781459, 3600000000))
        self.assertEqual(result["residual_budget"], F(52065013, 400000000))
        self.assertEqual(result["input_budget"], result["residual_budget"])
        self.assertTrue(result["residual_equals_h_times_input_authority"])
        self.assertEqual(result["residual_and_input_budget"], F(52065013, 400000000))
        self.assertEqual(result["maximum_seed_scale"], F(3600000000, 3889781459))
        self.assertEqual(result["maximum_residual_scale"], F(16254878, 42598647))
        self.assertEqual(result["minimum_input_scale"], F(68942416, 42598647))

    def test_thresholds_saturate_the_same_necessary_halfspace(self):
        subject = _subject()
        result = subject.k14_tradeoff_certificate()

        self.assertEqual(subject.lower_bound(result["maximum_seed_scale"], F(1), F(1)), F(1))
        self.assertEqual(subject.lower_bound(F(1), result["maximum_residual_scale"], F(1)), F(1))
        self.assertEqual(subject.lower_bound(F(1), F(1), result["minimum_input_scale"]), F(1))

    def test_information_objects_are_not_conflated(self):
        result = _subject().run()

        self.assertEqual(
            result["online_smf_directly_changes"],
            "realized_state_seed_directional_half_diameter",
        )
        self.assertFalse(result["online_smf_directly_changes_future_residual_set"])
        self.assertFalse(result["online_smf_changes_physical_input_authority"])
        self.assertFalse(result["necessary_condition_is_sufficient"])
        self.assertFalse(result["recursive_feasibility_certified"])

    def test_asymmetric_posterior_uses_directional_half_diameter(self):
        subject = _subject()

        self.assertEqual(subject.directional_half_diameter(F(5), F(-5)), F(0))
        self.assertEqual(subject.directional_half_diameter(F(7), F(1)), F(4))

    def test_checker_writes_hash_bound_exact_artifact(self):
        checker = ROOT / "verification/check_vertical_k14_contract_tradeoff.py"
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "exact_checks.json"
            completed = subprocess.run(
                [sys.executable, str(checker), "--output", str(output)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            generated = json.loads(output.read_text())
            archived = json.loads((
                ROOT
                / "results/theory_vertical_k14_contract_tradeoff_20261011/exact_checks.json"
            ).read_text())
            self.assertEqual(generated, archived)
            self.assertIn(
                "verification/check_intermittent_metric.py",
                generated["source_sha256"],
            )
            for name, digest in generated["source_sha256"].items():
                self.assertEqual(digest, hashlib.sha256((ROOT / name).read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
