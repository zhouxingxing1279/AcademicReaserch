import json
import tempfile
import unittest
from fractions import Fraction as F
from pathlib import Path

import check_affine_offset_socp_gate as gate


ROOT = Path(__file__).resolve().parents[1]


class SocpIdentityTests(unittest.TestCase):
    def test_soc_identity_is_exact(self):
        check = gate.verify_psd_soc_identity(F(3, 2), F(-2, 3), F(5, 4))
        self.assertTrue(check["identity"])
        self.assertEqual(check["lhs_minus_rhs"], 4 * check["determinant"])

    def test_soc_and_principal_minor_tests_agree(self):
        for matrix in ((F(1), F(0), F(2)), (F(1), F(2), F(1)), (F(-1), F(0), F(-1))):
            check = gate.verify_psd_soc_identity(*matrix)
            self.assertEqual(check["psd_by_minors"], check["psd_by_soc_squared"])


class FrozenSizeTests(unittest.TestCase):
    def test_raw_and_effective_dimensions(self):
        size = gate.problem_size(facets=38, vertices=160, state_dimension=4)
        self.assertEqual(size["soc_constraints"], 6080)
        self.assertEqual(size["raw_scalar_variables"], 6514)
        self.assertEqual(size["effective_scalar_variables_after_pair_equalities"], 6476)
        self.assertEqual(size["configuration_endpoint_inequalities"], 12160)
        self.assertEqual(size["hard_state_endpoint_inequalities"], 2560)
        self.assertEqual(size["torque_endpoint_inequalities"], 640)
        self.assertEqual(size["common_core_endpoint_inequalities"], 76)

    def test_report_is_archivable(self):
        report = gate.build_report(ROOT)
        self.assertEqual(report["evidence_level"], "DERIVED")
        self.assertEqual(report["numerical_feasibility"], "OPEN")
        self.assertTrue(report["solver_inventory"]["usable_conic_solver"])
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "report.json"
            target.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
            self.assertEqual(json.loads(target.read_text())["problem_size"]["soc_constraints"], 6080)


class ArchivedResultTests(unittest.TestCase):
    def test_archived_result_matches_current_checker(self):
        archived = json.loads(
            (ROOT / "results/affine_offset_socp_gate_20261029/checks.json").read_text()
        )
        self.assertEqual(archived, gate.build_report(ROOT, inventory=archived["solver_inventory"]))


if __name__ == "__main__":
    unittest.main()
