import json
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from check_pd_offset_endpoint_counterexample import (
    _assert_frozen_example,
    build_report,
    quadratic_max_on_interval,
)


class PdOffsetEndpointCounterexampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = build_report(ROOT)

    def test_frozen_endpoint_checks_pass_but_global_check_fails(self):
        example = self.result["counterexample"]
        self.assertEqual(example["quadratic"], ["-1/2", "1/2", "1"])
        self.assertEqual(example["endpoint_values"], {"0": "1", "1": "1"})
        self.assertTrue(example["endpoint_only_condition_passes"])
        self.assertEqual(example["global_maximizer"], "1/2")
        self.assertEqual(example["global_maximum"], "9/8")
        self.assertFalse(example["global_condition_passes"])
        self.assertEqual(example["violation"], "1/8")

    def test_concave_quadratic_checks_interior_stationary_point(self):
        result = quadratic_max_on_interval(F(-1, 2), F(1, 2), F(1), F(0), F(1))
        self.assertEqual(result["maximizers"], [F(1, 2)])
        self.assertEqual(result["maximum"], F(9, 8))
        self.assertEqual(result["candidates"], [F(0), F(1, 2), F(1)])

    def test_convex_quadratic_maximum_is_at_endpoint(self):
        result = quadratic_max_on_interval(F(1), F(-1), F(0), F(0), F(2))
        self.assertEqual(result["maximum"], F(2))
        self.assertEqual(result["maximizers"], [F(2)])
        self.assertEqual(result["candidates"], [F(0), F(2)])

    def test_linear_and_constant_degeneracies_remain_exact(self):
        increasing = quadratic_max_on_interval(F(0), F(3, 7), F(-2), F(-1), F(2))
        self.assertEqual(increasing["maximum"], F(-8, 7))
        self.assertEqual(increasing["maximizers"], [F(2)])
        constant = quadratic_max_on_interval(F(0), F(0), F(5, 9), F(-1), F(2))
        self.assertEqual(constant["maximum"], F(5, 9))
        self.assertEqual(constant["maximizers"], [F(-1), F(2)])

    def test_reversed_interval_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "lower endpoint exceeds upper endpoint"):
            quadratic_max_on_interval(F(1), F(2), F(3), F(1), F(0))

    def test_scope_is_limited_to_endpoint_unsoundness(self):
        self.assertEqual(self.result["evidence_level"], "COUNTEREXAMPLE")
        self.assertEqual(self.result["gate_A_status"], "blocked")
        self.assertFalse(self.result["proves_pd_rci_nonexistence"])
        self.assertFalse(self.result["proves_six_state_safety"])
        self.assertFalse(self.result["proves_recursive_feasibility"])

    def test_frozen_example_rejects_algebraic_perturbation(self):
        with self.assertRaises(AssertionError):
            _assert_frozen_example(
                parameter_lower=F(0),
                parameter_upper=F(1),
                radius_intercept=F(1),
                radius_slope=F(2),
                dynamics_intercept=F(1),
                dynamics_slope=F(-1, 2),
            )

    def test_direct_dependencies_are_hash_bound(self):
        expected = {
            "verification/check_pd_offset_endpoint_counterexample.py",
            "verification/test_pd_offset_endpoint_counterexample.py",
            "docs/research/run196_literature_gate.md",
            "docs/superpowers/specs/2026-10-29-pd-offset-endpoint-counterexample-design.md",
        }
        self.assertEqual(set(self.result["dependencies_sha256"]), expected)
        self.assertTrue(all(len(value) == 64 for value in self.result["dependencies_sha256"].values()))

    def test_checker_reproduces_archived_result(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "checks.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(HERE / "check_pd_offset_endpoint_counterexample.py"),
                    "--root",
                    str(ROOT),
                    "--output",
                    str(output),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            archived = ROOT / "results/pd_offset_endpoint_counterexample_20261029/checks.json"
            self.assertEqual(json.loads(output.read_text()), json.loads(archived.read_text()))


if __name__ == "__main__":
    unittest.main()
