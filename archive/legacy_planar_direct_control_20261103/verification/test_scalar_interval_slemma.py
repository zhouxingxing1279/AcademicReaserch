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

from check_scalar_interval_slemma import build_report, verify_slemma_certificate


class ScalarIntervalSlemmaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = build_report(ROOT)

    def test_one_minus_square_has_zero_gram_boundary_certificate(self):
        check = verify_slemma_certificate(
            F(-1), F(0), F(1), F(1), ((F(0), F(0)), (F(0), F(0)))
        )
        self.assertTrue(check["valid"])
        self.assertEqual(check["determinant"], F(0))

    def test_one_plus_s_has_rank_one_boundary_certificate(self):
        check = verify_slemma_certificate(
            F(0),
            F(1),
            F(1),
            F(1, 2),
            ((F(1, 2), F(1, 2)), (F(1, 2), F(1, 2))),
        )
        self.assertTrue(check["valid"])
        self.assertEqual(check["determinant"], F(0))

    def test_normalized_run196_residual_has_no_nonnegative_diagonal_at_any_nonnegative_multiplier(self):
        # f(s)=1-g(s)=(s^2-1)/8 is negative at s=0.  Since q00=c-lambda,
        # every lambda>=0 makes q00<0.
        check = verify_slemma_certificate(
            F(1, 8), F(0), F(-1, 8), F(0),
            ((F(-1, 8), F(0)), (F(0), F(1, 8))),
        )
        self.assertFalse(check["valid"])
        self.assertFalse(check["gram_psd"])

    def test_negative_multiplier_is_rejected_even_with_psd_gram(self):
        check = verify_slemma_certificate(
            F(1), F(0), F(1), F(-1), ((F(2), F(0)), (F(0), F(0)))
        )
        self.assertFalse(check["valid"])
        self.assertTrue(check["gram_psd"])
        self.assertFalse(check["multiplier_nonnegative"])

    def test_coefficient_mismatch_is_rejected(self):
        check = verify_slemma_certificate(
            F(-1), F(0), F(1), F(1), ((F(1), F(0)), (F(0), F(0)))
        )
        self.assertFalse(check["valid"])
        self.assertFalse(check["coefficient_identity"])

    def test_asymmetric_gram_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "symmetric"):
            verify_slemma_certificate(
                F(1), F(0), F(1), F(0), ((F(1), F(1)), (F(0), F(1)))
            )

    def test_report_freezes_evidence_boundary_and_constraint_counts(self):
        self.assertEqual(self.result["evidence_level"], "DERIVED")
        self.assertEqual(self.result["full_19pair_status"], "OPEN")
        self.assertEqual(self.result["gate_A_status"], "blocked")
        synthesis = self.result["synthesis_contract"]
        self.assertEqual(synthesis["facets"], 38)
        self.assertEqual(synthesis["vertices"], 160)
        self.assertEqual(synthesis["quadratic_interval_lmis"], 6080)
        self.assertTrue(synthesis["contains_parameter_independent_subclass"])
        self.assertFalse(self.result["proves_six_state_safety"])
        self.assertFalse(self.result["proves_recursive_feasibility"])

    def test_direct_dependencies_are_hash_bound(self):
        expected = {
            "verification/check_scalar_interval_slemma.py",
            "verification/test_scalar_interval_slemma.py",
            "docs/research/run197_literature_gate.md",
            "docs/superpowers/specs/2026-10-29-scalar-interval-exact-sdp-design.md",
        }
        self.assertEqual(set(self.result["dependencies_sha256"]), expected)
        self.assertTrue(all(len(value) == 64 for value in self.result["dependencies_sha256"].values()))

    def test_checker_reproduces_archived_result(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "checks.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(HERE / "check_scalar_interval_slemma.py"),
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
            archived = ROOT / "results/scalar_interval_slemma_20261029/checks.json"
            self.assertEqual(json.loads(output.read_text()), json.loads(archived.read_text()))


if __name__ == "__main__":
    unittest.main()
