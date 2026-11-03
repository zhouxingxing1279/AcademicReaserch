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

from check_scheduling_visible_19pair_farkas import _assert_frozen_contract, build_report


class SchedulingVisible19PairFarkasTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = build_report(ROOT)

    def test_corrected_lp_has_endpoint_specific_vertex_torques(self):
        model = self.result["corrected_lp"]
        self.assertEqual(model["offset_variables"], 38)
        self.assertEqual(model["state_vertices"], 160)
        self.assertEqual(model["torque_variables"], 320)
        self.assertEqual(model["variables"], 358)
        self.assertEqual(model["configuration_inequalities"], 6080)
        self.assertEqual(model["configuration_plus_invariance_inequalities"], 18240)
        self.assertEqual(model["total_inequalities_with_hard_state"], 19520)
        self.assertEqual(model["pair_offset_equalities"], 19)

    def test_corrected_full_lp_is_numerically_infeasible_even_without_torque_bounds(self):
        model = self.result["corrected_lp"]
        self.assertFalse(model["bounded_torque_0p08_feasible"])
        self.assertFalse(model["unbounded_endpoint_torque_feasible"])
        self.assertEqual(model["evidence_level"], "NUMERIC_CHECK")

    def test_sparse_exact_circuit_proves_infeasibility_in_expanded_space(self):
        certificate = self.result["exact_certificate"]
        self.assertEqual(certificate["support_rows"], 24)
        self.assertEqual(certificate["coefficient_rank"], 23)
        self.assertTrue(certificate["all_multipliers_strictly_positive"])
        self.assertTrue(certificate["weighted_lhs_zero_exact"])
        self.assertEqual(certificate["weighted_rhs"], "-3069803/88290")
        self.assertLess(F(certificate["weighted_rhs"]), 0)
        self.assertEqual(certificate["nonzero_weighted_lhs_coefficients"], 0)
        self.assertEqual(certificate["torque_bound_rows_used"], 0)
        self.assertEqual(certificate["pair_offset_equality_rows_used"], 0)
        self.assertEqual(certificate["q_nonnegativity_rows_used"], 0)

    def test_certificate_cancels_each_endpoint_torque_column_separately(self):
        certificate = self.result["exact_certificate"]
        self.assertEqual(certificate["endpoint_torque_coefficients_checked"], 320)
        self.assertEqual(certificate["nonzero_low_endpoint_torque_residuals"], 0)
        self.assertEqual(certificate["nonzero_high_endpoint_torque_residuals"], 0)

    def test_claim_scope_stays_with_fixed_candidate(self):
        self.assertEqual(self.result["evidence_level"], "COUNTEREXAMPLE")
        self.assertEqual(self.result["gate_A_status"], "blocked")
        self.assertFalse(self.result["proves_general_rci_nonexistence"])
        self.assertFalse(self.result["proves_six_state_safety"])
        self.assertFalse(self.result["proves_recursive_feasibility"])

    def test_direct_dependencies_are_hash_bound(self):
        expected = {
            "configs/planar_baseline.json",
            "verification/check_s3_minimal_normal_cover.py",
            "verification/check_19pair_cc_seed_cone.py",
            "verification/check_scheduling_visible_19pair_farkas.py",
            "verification/test_scheduling_visible_19pair_farkas.py",
            "docs/research/run195_literature_gate.md",
            "docs/superpowers/specs/2026-10-28-scheduling-visible-19pair-farkas-design.md",
        }
        self.assertEqual(set(self.result["dependencies_sha256"]), expected)
        self.assertTrue(
            all(len(value) == 64 for value in self.result["dependencies_sha256"].values())
        )

    def test_lower_hard_bounds_are_part_of_the_frozen_contract(self):
        config = json.loads((ROOT / "configs/planar_baseline.json").read_text())
        config["domain"]["input_lower"][1] = -0.081
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "configs").mkdir()
            (root / "configs/planar_baseline.json").write_text(json.dumps(config))
            with self.assertRaises(AssertionError):
                _assert_frozen_contract(root)

    def test_checker_reproduces_archived_result(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "checks.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(HERE / "check_scheduling_visible_19pair_farkas.py"),
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
            archived = (
                ROOT
                / "results/scheduling_visible_19pair_farkas_20261028/checks.json"
            )
            self.assertEqual(json.loads(output.read_text()), json.loads(archived.read_text()))


if __name__ == "__main__":
    unittest.main()
