import unittest
import json
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path


class VerticalFiberCausalityGapTests(unittest.TestCase):
    def test_vertical_constants_must_match_config_and_run136_success_map(self):
        import check_vertical_fiber_causality_gap as checker
        from check_cycle_lifted_zonotope import problem_data

        self.assertTrue(hasattr(checker, "audit_model_constants"))
        config = json.loads(
            (Path(__file__).resolve().parents[1] / "configs/planar_baseline.json").read_text(),
            parse_float=F,
        )
        _, _, _, success_matrix, _, _ = problem_data()
        checker.audit_model_constants(config, success_matrix)
        drifted = deepcopy(config)
        drifted["plant"]["dt_s"] = F(3, 100)
        with self.assertRaises(AssertionError):
            checker.audit_model_constants(drifted, success_matrix)

    def test_mode_four_support_is_derived_from_current_run136_geometry(self):
        try:
            from check_vertical_fiber_causality_gap import mode_four_q_support
        except ImportError as exc:
            self.fail(f"vertical causality-gap checker is missing: {exc}")

        support, witness = mode_four_q_support()
        self.assertEqual(support, F(1004143, 7200000))
        self.assertEqual(witness[1] + F(1, 50) * witness[3], support)

    def test_full_state_fiber_policy_fits_both_unknown_successors(self):
        from check_vertical_fiber_causality_gap import run

        result = run()
        full = result["full_state_fiber_policy"]
        self.assertTrue(full["correction_authority_ok"])
        self.assertTrue(full["miss_target_ok"])
        self.assertTrue(full["success_target_ok"])
        self.assertEqual(full["required_extreme_correction"], F(108143, 32000))

    def test_entire_mode_four_fiber_is_inside_hover_source_domain(self):
        from check_vertical_fiber_causality_gap import run

        result = run()
        self.assertIn("source_fiber_domain", result)
        source = result["source_fiber_domain"]
        self.assertTrue(source["entire_fiber_inside"])
        self.assertEqual(
            source["coordinate_supports"],
            [
                F(612587961, 4000000000),
                F(202879313, 1800000000),
                F(301172253, 160000000),
                F(48156437, 36000000),
                F(1, 200),
                F(1, 100),
            ],
        )
        self.assertTrue(all(value > 0 for value in source["lower_slacks"]))
        self.assertTrue(all(value > 0 for value in source["upper_slacks"]))

    def test_one_causal_control_has_empty_observation_fiber_intersection(self):
        from check_vertical_fiber_causality_gap import run

        result = run()
        causal = result["causal_observation_fiber"]
        self.assertEqual(causal["required_lower"], F(108143, 32000))
        self.assertEqual(causal["required_upper"], F(-108143, 32000))
        self.assertGreater(causal["required_lower"], causal["required_upper"])
        self.assertFalse(causal["common_control_exists"])

    def test_full_state_policy_is_checked_on_all_edge_vertices(self):
        from check_vertical_fiber_causality_gap import run

        result = run()
        self.assertIn("edge_vertex_checks", result)
        checks = result["edge_vertex_checks"]
        self.assertEqual(len(checks), 6)
        self.assertEqual(
            sum(row["edge"] == "success_to_0" for row in checks),
            4,
        )
        self.assertEqual(
            sum(row["edge"] == "miss_to_5" for row in checks),
            2,
        )
        self.assertTrue(all("position_target_ok" in row for row in checks))
        self.assertTrue(all("velocity_target_ok" in row for row in checks))
        self.assertTrue(all(row["position_target_ok"] for row in checks))
        self.assertTrue(all(row["velocity_target_ok"] for row in checks))
        self.assertTrue(all(row["target_ok"] for row in checks))
        self.assertTrue(all(row["input_ok"] for row in checks))

    def test_claim_is_strict_one_step_gap_not_an_rci_certificate(self):
        from check_vertical_fiber_causality_gap import run

        result = run()
        self.assertEqual(result["status"], "pass")
        self.assertEqual(
            result["claim"],
            "strict_actual_model_observation_fiber_predecessor_gap",
        )
        self.assertEqual(
            result["evidence_level"],
            "exact_one_step_counterexample_not_an_rci_certificate",
        )


if __name__ == "__main__":
    unittest.main()
