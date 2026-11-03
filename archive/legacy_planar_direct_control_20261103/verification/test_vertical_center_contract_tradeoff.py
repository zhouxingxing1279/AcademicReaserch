import importlib
import sys
import unittest
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "verification"))


def _subject():
    return importlib.import_module("check_vertical_center_contract_tradeoff")


class VerticalCenterContractTradeoffTest(unittest.TestCase):
    def test_support_lp_has_exact_affine_branch_covering_required_threshold(self):
        result = _subject().center_contract_certificate()
        support = result["conditional_initial_support"]
        self.assertEqual(support["visible_slope"], F(29, 15))
        self.assertEqual(support["affine_intercept"], F(16315003, 75000000))
        self.assertEqual(support["affine_branch_range"], [F(0), F(20432147, 48000000)])

    def test_exact_support_formula_has_matching_primal_and_dual_certificates(self):
        result = _subject().center_contract_certificate()
        support = result["conditional_initial_support"]
        self.assertEqual(support["formula"], "b + lambda*r")
        self.assertTrue(support["primal_attainment_on_affine_branch"])
        self.assertTrue(support["dual_upper_bound_on_affine_branch"])

    def test_three_factor_condition_and_single_factor_thresholds_are_exact(self):
        result = _subject().center_contract_certificate()
        tradeoff = result["three_factor_contract"]
        thresholds = result["single_factor_thresholds"]
        self.assertEqual(
            tradeoff["condition"],
            "b + lambda*r + beta*D - gamma*C <= 1",
        )
        self.assertEqual(thresholds["visible_radius_max"], F(58684997, 145000000))
        self.assertEqual(thresholds["future_residual_scale_max"], F(16254878, 42598647))
        self.assertEqual(thresholds["correction_authority_scale_min"], F(68942416, 42598647))

    def test_current_contract_fails_and_each_boundary_contract_is_tight(self):
        result = _subject().center_contract_certificate()
        checks = result["boundary_checks"]
        self.assertEqual(checks["current_contract_endpoint"], F(3889781459, 3600000000))
        self.assertGreater(checks["current_contract_endpoint"], 1)
        self.assertEqual(checks["visible_only_endpoint"], 1)
        self.assertEqual(checks["residual_only_endpoint"], 1)
        self.assertEqual(checks["authority_only_endpoint"], 1)


if __name__ == "__main__":
    unittest.main()
