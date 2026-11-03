import hashlib
import importlib
import json
from fractions import Fraction as F
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def _subject():
    try:
        return importlib.import_module("check_vertical_multi_return_template")
    except ModuleNotFoundError:
        return None


class VerticalMultiReturnTemplateTests(unittest.TestCase):
    def test_all_initialization_return_paths_reach_the_full_source_fiber(self):
        subject = _subject()
        certificate = getattr(subject, "multi_return_template_certificate", lambda: {})()
        returns = certificate.get("initialization_returns", {})

        self.assertEqual(tuple(returns), (4, 9, 14))
        for mode in (4, 9, 14):
            row = returns[mode]
            self.assertEqual(row.get("miss_edge_count"), mode)
            self.assertTrue(row.get("source_zonotope_reached_exactly"))
            self.assertTrue(row.get("success_return_edge_present"))
            self.assertEqual(row.get("correction_thrust_sequence"), (F(0),) * mode)
            self.assertEqual(row.get("visible_offset_before_success"), (F(0), F(0)))
            self.assertTrue(row.get("visible_offset_derived_by_miss_dynamics"))

    def test_each_return_seed_preserves_path_local_primitives_and_rank(self):
        subject = _subject()
        certificate = getattr(subject, "multi_return_template_certificate", lambda: {})()
        seeds = certificate.get("return_seeds", {})

        self.assertEqual(tuple(seeds), (4, 9, 14))
        self.assertEqual(
            tuple(seeds[mode]["source_generator_count"] for mode in seeds),
            (34, 69, 104),
        )
        self.assertEqual(
            tuple(seeds[mode]["generator_count"] for mode in seeds),
            (36, 71, 106),
        )
        for seed in seeds.values():
            self.assertEqual(seed.get("affine_hull_dimension"), 3)
            self.assertEqual(len(seed.get("independent_generator_indices", ())), 3)
            self.assertTrue(seed.get("shared_residual_primitive"))
            self.assertTrue(seed.get("shared_measurement_primitive"))
            self.assertTrue(seed.get("all_generators_satisfy_dv_equals_L_dp"))

    def test_all_three_complete_images_fit_estimator_and_true_error_constraints(self):
        subject = _subject()
        certificate = getattr(subject, "multi_return_template_certificate", lambda: {})()
        seeds = certificate.get("return_seeds", {})

        expected = {
            4: {
                "eta_support": (F(1, 50), F(37857863, 36000000)),
                "eta_slack": (F(0), F(0)),
                "tracking_error_support": (F(1004143, 7200000), F(101462161, 72000000)),
                "tracking_error_slack": (F(6195857, 7200000), F(96537839, 72000000)),
            },
            9: {
                "eta_support": (F(1, 50), F(204679321, 288000000)),
                "eta_slack": (F(0), F(10909287, 32000000)),
                "tracking_error_support": (F(42435007, 144000000), F(31802149, 18000000)),
                "tracking_error_slack": (F(101564993, 144000000), F(17697851, 18000000)),
            },
            14: {
                "eta_support": (F(1, 50), F(7329131969, 7200000000)),
                "eta_slack": (F(0), F(242440631, 7200000000)),
                "tracking_error_support": (F(23312147, 48000000), F(152955031, 72000000)),
                "tracking_error_slack": (F(24687853, 48000000), F(45044969, 72000000)),
            },
        }
        for mode, values in expected.items():
            for key, value in values.items():
                self.assertEqual(seeds[mode].get(key), value)
            self.assertTrue(seeds[mode].get("eta_projection_in_mode0_vertical_box"))
            self.assertTrue(seeds[mode].get("tracking_error_projection_in_hard_box"))

    def test_minimal_convex_template_is_rank_three_and_constraint_admissible(self):
        subject = _subject()
        certificate = getattr(subject, "multi_return_template_certificate", lambda: {})()
        template = certificate.get("common_mode_zero_template", {})

        self.assertEqual(
            template.get("representation"),
            "exact_perspective_lift_of_convex_hull_of_path_zonotopes",
        )
        self.assertEqual(template.get("component_modes"), (4, 9, 14))
        self.assertEqual(template.get("path_selector_count"), 3)
        self.assertEqual(template.get("local_generator_counts"), (36, 71, 106))
        self.assertEqual(template.get("total_local_generator_count"), 213)
        self.assertEqual(
            template.get("lift_constraints"),
            (
                "lambda_m >= 0",
                "sum_m lambda_m = 1",
                "-lambda_m <= v_m_i <= lambda_m",
                "x = sum_m G_m v_m",
            ),
        )
        self.assertEqual(template.get("affine_hull_dimension"), 3)
        self.assertTrue(template.get("least_convex_container"))
        self.assertTrue(template.get("preserves_path_local_generator_column_coupling"))
        self.assertTrue(template.get("prevents_simultaneous_full_path_activation"))
        self.assertTrue(template.get("permits_fractional_cross_path_mixtures"))
        self.assertEqual(
            template.get("fractional_two_path_selector_witness"),
            (F(1, 2), F(1, 2), F(0)),
        )
        self.assertFalse(template.get("two_unit_scale_selectors_feasible"))
        self.assertTrue(template.get("all_points_satisfy_dv_equals_L_dp"))
        self.assertEqual(
            template.get("eta_support"),
            (F(1, 50), F(37857863, 36000000)),
        )
        self.assertEqual(template.get("eta_slack"), (F(0), F(0)))
        self.assertEqual(
            template.get("tracking_error_support"),
            (F(23312147, 48000000), F(152955031, 72000000)),
        )
        self.assertEqual(
            template.get("tracking_error_slack"),
            (F(24687853, 48000000), F(45044969, 72000000)),
        )
        self.assertTrue(template.get("eta_projection_in_mode0_vertical_box"))
        self.assertTrue(template.get("tracking_error_projection_in_hard_box"))
        self.assertFalse(template.get("has_strict_estimator_margin"))

    def test_naive_generator_concatenation_is_rejected_without_rejecting_convex_hull(self):
        subject = _subject()
        certificate = getattr(subject, "multi_return_template_certificate", lambda: {})()
        naive = certificate.get("naive_concatenation_negative_control", {})

        self.assertEqual(naive.get("eta_support"),
                         (F(3, 50), F(10008843797, 3600000000)))
        self.assertEqual(naive.get("tracking_error_support"),
                         (F(11037859, 12000000), F(31802149, 6000000)))
        self.assertFalse(naive.get("eta_projection_in_mode0_vertical_box"))
        self.assertFalse(naive.get("tracking_error_projection_in_hard_box"))
        self.assertTrue(naive.get("failure_is_representation_specific"))

    def test_claim_stops_before_controlled_invariance(self):
        subject = _subject()
        result = getattr(subject, "run", lambda: {})()

        self.assertEqual(result.get("status"), "pass")
        self.assertEqual(
            result.get("evidence_level"),
            "exact_rank_three_minimal_convex_template_for_three_fixed_zero_correction_returns",
        )
        self.assertEqual(
            result.get("certificate_scope"),
            "fixed_zero_correction_initialization_baseline",
        )
        self.assertTrue(result.get("all_fixed_zero_correction_return_seeds_certified"))
        self.assertTrue(result.get("common_mode_zero_template_certified"))
        self.assertFalse(result.get("is_policy_independent_necessity"))
        self.assertFalse(result.get("strict_estimator_margin"))
        self.assertFalse(result.get("is_rci_certificate"))
        self.assertFalse(result.get("full_six_state_guarantee"))

    def test_checker_writes_a_hash_bound_exact_artifact(self):
        subject_path = ROOT / "verification/check_vertical_multi_return_template.py"
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "checks.json"
            completed = subprocess.run(
                [sys.executable, str(subject_path), "--output", str(output)],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(completed.returncode, 0, completed.stderr)
            artifact = json.loads(output.read_text())
            archived = json.loads(
                (ROOT / "results/theory_vertical_multi_return_template_20261003/exact_checks.json").read_text()
            )
            self.assertEqual(artifact, archived)
            for dependency in (
                "verification/check_vertical_multi_return_template.py",
                "verification/test_vertical_multi_return_template.py",
                "verification/check_vertical_correlated_return_seed.py",
                "verification/check_vertical_joint_first_sweep.py",
                "verification/check_vertical_joint_predecessor.py",
                "verification/check_cycle_lifted_zonotope.py",
                "verification/check_mode_nestedness.py",
                "verification/check_mode_radius.py",
                "configs/planar_baseline.json",
                "docs/learning/85_vertical_multi_return_template.md",
                "docs/literature/READ_PAPERS.md",
                "docs/research/run148_literature_gate.md",
                "docs/research/run148_research_log.md",
            ):
                self.assertEqual(
                    artifact["source_sha256"].get(dependency),
                    hashlib.sha256((ROOT / dependency).read_bytes()).hexdigest(),
                )


if __name__ == "__main__":
    unittest.main()
