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

from check_homothetic_s4_rci_gate import audit


class HomotheticS4RciGateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = audit(ROOT)

    def test_frozen_s4_and_exact_vertex_membership(self):
        self.assertEqual(self.result["template"]["nonredundant_facets"], 102)
        self.assertEqual(
            self.result["witness"]["vertex"],
            [
                "19040871601/4000000000",
                "4786988769/1600000000",
                "13488347/39240000",
                "4169653/3139200",
            ],
        )
        self.assertTrue(self.result["witness"]["inside_s4_exact"])
        self.assertGreaterEqual(self.result["witness"]["active_facets"], 4)
        self.assertEqual(self.result["witness"]["active_normal_rank"], 4)

    def test_low_thrust_torque_gap_is_positive_for_every_positive_scale(self):
        gap = self.result["torque_gap"]
        self.assertEqual(gap["thrust_N"], "981/200")
        self.assertEqual(gap["slope"], "5626543/1569600")
        self.assertEqual(gap["intercept_Nm"], "6254383/174400")
        self.assertGreater(F(gap["slope"]), 0)
        self.assertGreater(F(gap["intercept_Nm"]), 0)
        self.assertEqual(
            F(gap["lower_slope"]) - F(gap["upper_slope"]),
            F(gap["slope"]),
        )
        self.assertEqual(
            F(gap["lower_intercept_Nm"]) - F(gap["upper_intercept_Nm"]),
            F(gap["intercept_Nm"]),
        )
        self.assertFalse(self.result["exists_positive_homothetic_scale"])

    def test_claim_scope_does_not_overreach_candidate_class(self):
        self.assertEqual(self.result["evidence_level"], "COUNTEREXAMPLE")
        self.assertEqual(self.result["gate_A_status"], "blocked")
        self.assertFalse(self.result["proves_general_rci_nonexistence"])
        self.assertFalse(self.result["proves_six_state_safety"])
        self.assertFalse(self.result["proves_recursive_feasibility"])

    def test_direct_dependencies_are_hash_bound(self):
        expected = {
            "configs/planar_baseline.json",
            "verification/check_scheduling_visible_predecessor.py",
            "verification/check_homothetic_s4_rci_gate.py",
            "verification/test_homothetic_s4_rci_gate.py",
        }
        self.assertEqual(set(self.result["dependencies_sha256"]), expected)
        self.assertTrue(all(len(value) == 64 for value in self.result["dependencies_sha256"].values()))

    def test_checker_reproduces_archived_result(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "checks.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(HERE / "check_homothetic_s4_rci_gate.py"),
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
            archived = ROOT / "results/homothetic_s4_rci_gate_20261028/checks.json"
            self.assertEqual(json.loads(output.read_text()), json.loads(archived.read_text()))


if __name__ == "__main__":
    unittest.main()
