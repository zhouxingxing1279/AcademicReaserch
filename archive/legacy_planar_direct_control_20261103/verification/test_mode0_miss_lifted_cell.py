import importlib
import json
from fractions import Fraction as F
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ModeZeroMissLiftedCellTests(unittest.TestCase):
    def subject(self):
        return importlib.import_module("check_mode0_miss_lifted_cell")

    def test_contract_edge_policy_and_shared_residual_are_explicit(self):
        result = self.subject().mode0_miss_certificate()
        self.assertEqual((result["source_mode"], result["target_mode"], result["edge_label"]), (0, 1, "miss"))
        self.assertTrue(result["edge_present_in_contract"])
        self.assertFalse(result["policy_uses_hidden_eta"])
        self.assertEqual(result["affine_fibre_policy"]["offset"], F(0))
        self.assertTrue(result["shared_residual_realization"])
        self.assertEqual(result["residual_halfwidth_at_actual_thrust_upper"], F(411370817, 128000000))

    def test_all_fixed_target_normals_close(self):
        result = self.subject().mode0_miss_certificate()
        rows = result["eta_target_normal_rows"] + result["tracking_target_normal_rows"]
        self.assertEqual(result["target_normal_count"], 10)
        self.assertTrue(all(row["slack"] >= 0 for row in rows))
        self.assertEqual(result["minimum_target_normal_slack"], F(0))
        self.assertTrue(result["one_edge_closed"])

    def test_scope_is_not_upgraded_to_terminal_or_rci(self):
        result = self.subject().run()
        self.assertEqual(result["evidence_level"], "exact_one_edge_target_normal_support_certificate")
        self.assertFalse(result["is_rci_certificate"])
        self.assertFalse(result["terminal_family_closed"])
        self.assertFalse(result["recursive_feasibility_certified"])
        self.assertFalse(result["full_six_state_guarantee"])

    def test_checker_writes_hash_bound_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "exact_checks.json"
            completed = subprocess.run(
                [sys.executable, str(ROOT / "verification/check_mode0_miss_lifted_cell.py"), "--output", str(output)],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            artifact = json.loads(output.read_text())
            self.assertEqual(artifact["status"], "pass")
            self.assertIn("verification/check_mode0_miss_lifted_cell.py", artifact["source_sha256"])


if __name__ == "__main__":
    unittest.main()
