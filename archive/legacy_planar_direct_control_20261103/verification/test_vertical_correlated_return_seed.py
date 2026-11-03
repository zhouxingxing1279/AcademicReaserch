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
        return importlib.import_module("check_vertical_correlated_return_seed")
    except ModuleNotFoundError:
        return None


class VerticalCorrelatedReturnSeedTests(unittest.TestCase):
    def test_initialization_miss_chain_reaches_the_full_mode_fourteen_fiber(self):
        """Shrinking q|d on the required all-miss history must fail."""
        subject = _subject()
        certificate = getattr(subject, "correlated_return_seed", lambda: {})()
        reach = certificate.get("initialization_reachability", {})

        self.assertEqual(reach.get("initial_mode"), 0)
        self.assertEqual(reach.get("initial_visible_offset"), F(0))
        self.assertEqual(reach.get("miss_edge_count"), 14)
        self.assertTrue(reach.get("mode14_zonotope_reached_exactly"))
        self.assertTrue(reach.get("visible_offset_independent_of_hidden_eta"))
        self.assertEqual(
            reach.get("mode14_q_halfwidth"), F(23312147, 48000000)
        )

    def test_return_seed_keeps_shared_primitives_and_has_exact_rank_three(self):
        """Independent boxing or a false four-dimensional claim must fail."""
        subject = _subject()
        certificate = getattr(subject, "correlated_return_seed", lambda: {})()
        seed = certificate.get("return_seed", {})

        self.assertEqual(seed.get("coordinates"), ("eta_p", "eta_v", "e_p", "e_v"))
        self.assertEqual(seed.get("source_generator_count"), 104)
        self.assertEqual(seed.get("generator_count"), 106)
        self.assertEqual(seed.get("affine_hull_dimension"), 3)
        self.assertEqual(len(seed.get("independent_generator_indices", ())), 3)
        self.assertTrue(seed.get("shared_residual_primitive"))
        self.assertTrue(seed.get("shared_measurement_primitive"))
        self.assertTrue(seed.get("all_generators_satisfy_dv_equals_L_dp"))

    def test_full_return_image_fits_vertical_estimator_and_true_error_constraints(self):
        """A single feasible witness must not stand in for the full image."""
        subject = _subject()
        certificate = getattr(subject, "correlated_return_seed", lambda: {})()
        seed = certificate.get("return_seed", {})

        self.assertEqual(seed.get("eta_support"), (F(1, 50), F(7329131969, 7200000000)))
        self.assertEqual(seed.get("eta_mode0_slack"), (F(0), F(242440631, 7200000000)))
        self.assertEqual(seed.get("tracking_error_support"),
                         (F(23312147, 48000000), F(152955031, 72000000)))
        self.assertEqual(seed.get("tracking_error_slack"),
                         (F(24687853, 48000000), F(45044969, 72000000)))
        self.assertTrue(seed.get("eta_projection_in_mode0_vertical_box"))
        self.assertTrue(seed.get("tracking_error_projection_in_hard_box"))

    def test_correlated_seed_exceeds_product_d_target_without_breaking_true_constraints(self):
        """Reintroducing the rejected independent d bound must fail."""
        subject = _subject()
        certificate = getattr(subject, "correlated_return_seed", lambda: {})()
        comparison = certificate.get("product_target_comparison", {})

        self.assertEqual(comparison.get("return_d_support"),
                         (F(24272147, 48000000), F(72816441, 32000000)))
        self.assertEqual(comparison.get("run146_product_d0_velocity_halfwidth"),
                         F(94125081847, 57600000000))
        self.assertEqual(comparison.get("strict_velocity_excess"),
                         F(36944511953, 57600000000))
        self.assertTrue(comparison.get("violates_run146_product_d0_velocity_bound"))
        self.assertTrue(comparison.get("accepted_by_correlated_true_error_target"))

    def test_claim_is_limited_to_a_required_reachable_seed(self):
        subject = _subject()
        result = getattr(subject, "run", lambda: {})()

        self.assertEqual(result.get("status"), "pass")
        self.assertEqual(
            result.get("evidence_level"),
            "exact_rank_three_correlated_return_seed_for_required_initialization_path",
        )
        self.assertTrue(result.get("run146_next_problem_rejected_as_duplicate"))
        self.assertTrue(result.get("required_return_seed_certified"))
        self.assertFalse(result.get("is_rci_certificate"))
        self.assertFalse(result.get("full_six_state_guarantee"))

    def test_checker_writes_a_hash_bound_exact_artifact(self):
        subject_path = ROOT / "verification/check_vertical_correlated_return_seed.py"
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
                (ROOT / "results/theory_vertical_correlated_return_seed_20261003/exact_checks.json").read_text()
            )
            self.assertEqual(artifact, archived)
            self.assertEqual(artifact["status"], "pass")
            for dependency in (
                "verification/check_vertical_correlated_return_seed.py",
                "verification/test_vertical_correlated_return_seed.py",
                "verification/check_vertical_joint_second_sweep.py",
                "verification/check_vertical_joint_first_sweep.py",
                "verification/check_vertical_joint_predecessor.py",
                "verification/check_cycle_lifted_zonotope.py",
                "verification/check_mode_nestedness.py",
                "verification/check_mode_radius.py",
                "configs/planar_baseline.json",
                "docs/learning/84_vertical_correlated_return_seed.md",
                "docs/literature/READ_PAPERS.md",
                "docs/research/run147_literature_gate.md",
                "docs/research/run147_research_log.md",
            ):
                self.assertEqual(
                    artifact["source_sha256"].get(dependency),
                    hashlib.sha256((ROOT / dependency).read_bytes()).hexdigest(),
                )


if __name__ == "__main__":
    unittest.main()
