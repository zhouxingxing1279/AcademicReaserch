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
        return importlib.import_module(
            "check_vertical_translated_template_obstruction"
        )
    except ModuleNotFoundError:
        try:
            return importlib.import_module(
                "verification.check_vertical_translated_template_obstruction"
            )
        except ModuleNotFoundError:
            return None


class VerticalTranslatedTemplateObstructionTests(unittest.TestCase):
    def test_return_shapes_are_propagated_from_the_exact_run148_convex_components(self):
        subject = _subject()
        certificate = getattr(subject, "translated_template_certificate", lambda: {})()

        self.assertEqual(certificate.get("component_modes"), (4, 9, 14))
        self.assertEqual(
            certificate.get("mode_zero_component_generator_counts"),
            (36, 71, 106),
        )
        expected_success_counts = {
            4: (42, 77, 112),
            9: (47, 82, 117),
            14: (52, 87, 122),
        }
        for mode, counts in expected_success_counts.items():
            self.assertEqual(
                certificate.get("return_edges", {}).get(mode, {}).get(
                    "success_image_component_generator_counts"
                ),
                counts,
            )

    def test_all_three_return_edges_violate_the_translation_invariant_ep_width(self):
        subject = _subject()
        certificate = getattr(subject, "translated_template_certificate", lambda: {})()
        rows = certificate.get("return_edges", {})

        target = F(23312147, 48000000)
        expected = {
            4: (F(51293581, 72000000), F(32650721, 144000000)),
            9: (F(14038717, 14400000), F(70450729, 144000000)),
            14: (F(12222431, 9600000), F(4725001, 6000000)),
        }
        self.assertEqual(tuple(rows), (4, 9, 14))
        for mode, (source, excess) in expected.items():
            row = rows[mode]
            self.assertEqual(row.get("target_ep_halfwidth"), target)
            self.assertEqual(row.get("success_ep_halfwidth"), source)
            self.assertEqual(row.get("strict_ep_halfwidth_excess"), excess)
            self.assertTrue(row.get("strict_width_obstruction"))
            self.assertFalse(row.get("translated_return_containment_possible"))

    def test_correction_and_arbitrary_centers_cannot_repair_ep_width(self):
        subject = _subject()
        certificate = getattr(subject, "translated_template_certificate", lambda: {})()

        self.assertEqual(
            certificate.get("correction_translation_per_unit_thrust"),
            (F(0), F(0), F(0), F(1, 50)),
        )
        self.assertFalse(certificate.get("correction_changes_ep_support"))
        self.assertTrue(certificate.get("set_translation_preserves_directional_width"))
        for row in certificate.get("return_edges", {}).values():
            self.assertTrue(row.get("obstruction_holds_for_all_source_centers"))
            self.assertTrue(row.get("obstruction_holds_for_all_target_centers"))
            self.assertTrue(row.get("obstruction_holds_for_all_current_corrections"))

    def test_unknown_mode4_and_mode9_branches_share_one_input_but_fail_on_success_alone(self):
        subject = _subject()
        certificate = getattr(subject, "translated_template_certificate", lambda: {})()
        rows = certificate.get("return_edges", {})

        for mode in (4, 9):
            row = rows.get(mode, {})
            self.assertEqual(row.get("outgoing_labels"), ("miss", "success"))
            self.assertTrue(row.get("one_current_input_shared_across_success_and_miss"))
            self.assertTrue(row.get("miss_shape_matches_next_mode_by_construction"))
            self.assertTrue(row.get("success_edge_alone_is_infeasible"))
            self.assertFalse(row.get("shared_input_branch_containment_possible"))

    def test_claim_rejects_only_the_translated_fixed_shape_family(self):
        subject = _subject()
        result = getattr(subject, "run", lambda: {})()

        self.assertEqual(result.get("status"), "pass")
        self.assertEqual(
            result.get("evidence_level"),
            "exact_ep_width_obstruction_for_run148_translated_fixed_shape_family",
        )
        self.assertEqual(result.get("earliest_obstruction_mode"), 4)
        self.assertEqual(result.get("obstructed_return_modes"), (4, 9, 14))
        self.assertTrue(result.get("translated_fixed_shape_family_rejected"))
        self.assertFalse(result.get("history_conditioned_information_ensemble_rejected"))
        self.assertFalse(result.get("scheduled_decision_dependent_family_rejected"))
        self.assertFalse(result.get("is_rci_certificate"))
        self.assertFalse(result.get("full_six_state_guarantee"))

    def test_checker_writes_a_hash_bound_exact_artifact(self):
        subject_path = (
            ROOT / "verification/check_vertical_translated_template_obstruction.py"
        )
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
                (
                    ROOT
                    / "results/theory_vertical_translated_template_obstruction_20261003/exact_checks.json"
                ).read_text()
            )
            self.assertEqual(artifact, archived)
            for dependency in (
                "verification/check_vertical_translated_template_obstruction.py",
                "verification/test_vertical_translated_template_obstruction.py",
                "verification/check_vertical_multi_return_template.py",
                "verification/check_vertical_control_translation_split.py",
                "verification/check_vertical_correlated_return_seed.py",
                "verification/check_cycle_lifted_zonotope.py",
                "configs/planar_baseline.json",
                "docs/learning/87_vertical_translated_template_obstruction.md",
                "docs/literature/READ_PAPERS.md",
                "docs/research/run150_literature_gate.md",
                "docs/research/run150_research_log.md",
            ):
                self.assertEqual(
                    artifact["source_sha256"].get(dependency),
                    hashlib.sha256((ROOT / dependency).read_bytes()).hexdigest(),
                )


if __name__ == "__main__":
    unittest.main()
