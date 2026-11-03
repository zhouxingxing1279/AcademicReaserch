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

from check_scheduling_visible_predecessor import audit, project_scalar_input


class SchedulingVisiblePredecessorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = audit(ROOT, max_depth=4)

    def test_endpoint_conditioned_projection_never_cross_pairs_torque_rows(self):
        zero = (F(0),) * 4
        rows = {
            "low": [(zero, F(-1), F(-1, 2))],   # tau >= +1/2
            "high": [(zero, F(1), F(-1, 2))],   # tau <= -1/2
        }
        visible = project_scalar_input(rows, F(1), endpoint_conditioned=True)
        common = project_scalar_input(rows, F(1), endpoint_conditioned=False)
        self.assertTrue(all(rhs >= 0 for _, rhs in visible))
        self.assertTrue(any(all(value == 0 for value in row) and rhs < 0 for row, rhs in common))

    def test_frozen_contract_matches_current_information_timing(self):
        contract = self.result["contract"]
        self.assertTrue(contract["current_thrust_measured_before_torque"])
        self.assertEqual(contract["future_thrust"], "arbitrary_jump_in_interval")
        self.assertEqual(contract["thrust_endpoints_N"], ["981/200", "2943/200"])
        self.assertEqual(contract["torque_limit_Nm"], "2/25")
        self.assertEqual(contract["residual_halfwidth"], "47/25 + T*(9/20)^3/6")

    def test_first_four_visible_layers_match_common_set_layers_only_numerically(self):
        common = self.result["common_torque_layers"]
        visible = self.result["scheduling_visible_layers"]
        self.assertEqual([item["unique_candidates"] for item in common], [17, 31, 99, 903])
        self.assertEqual([item["unique_candidates"] for item in visible], [17, 31, 85, 489])
        self.assertEqual([item["nonredundant_facets"] for item in common], [16, 28, 52, 102])
        self.assertEqual([item["nonredundant_facets"] for item in visible], [16, 28, 52, 102])
        self.assertTrue(all(item["same_polytope_numerical"] for item in self.result["layer_comparison"]))
        self.assertTrue(any(
            left["unique_candidates"] != right["unique_candidates"]
            for left, right in zip(common, visible)
        ))

    def test_legacy_fraction_leak_is_detected_and_corrected(self):
        audit_result = self.result["legacy_checker_audit"]
        self.assertTrue(audit_result["fraction_leak_detected"])
        self.assertEqual(
            audit_result["canonicalized_unit_coefficient_type"],
            "float",
        )
        self.assertEqual(audit_result["archived_nonredundant_facet_counts"], [16, 28, 52, 102])
        self.assertEqual(audit_result["corrected_nonredundant_facet_counts"], [16, 28, 52, 102])
        self.assertTrue(audit_result["legacy_nonredundant_facet_counts_still_match_corrected_counts"])
        self.assertTrue(self.result["corrected_fraction_construction"])

    def test_result_refuses_infinite_horizon_and_six_state_overclaim(self):
        self.assertEqual(self.result["evidence_level"], "NUMERIC_CHECK")
        self.assertFalse(self.result["is_rci_certificate"])
        self.assertFalse(self.result["proves_all_depths_equal"])
        self.assertFalse(self.result["proves_six_state_safety"])
        serialized = json.dumps(self.result).lower()
        self.assertNotIn("recursive feasibility is certified", serialized)
        self.assertNotIn("gate a passed", serialized)

    def test_checker_reproduces_archived_result(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "checks.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(HERE / "check_scheduling_visible_predecessor.py"),
                    "--root",
                    str(ROOT),
                    "--max-depth",
                    "4",
                    "--output",
                    str(output),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            archived = ROOT / "results/scheduling_visible_predecessor_20261028/checks.json"
            self.assertEqual(json.loads(output.read_text()), json.loads(archived.read_text()))


if __name__ == "__main__":
    unittest.main()
