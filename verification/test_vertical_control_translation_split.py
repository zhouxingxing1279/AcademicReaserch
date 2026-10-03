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
        return importlib.import_module("check_vertical_control_translation_split")
    except ModuleNotFoundError:
        try:
            return importlib.import_module(
                "verification.check_vertical_control_translation_split"
            )
        except ModuleNotFoundError:
            return None


class VerticalControlTranslationSplitTests(unittest.TestCase):
    def test_miss_and_success_maps_match_hand_derived_shared_primitive_values(self):
        subject = _subject()
        update = getattr(subject, "vertical_edge_update", lambda *args, **kwargs: {})
        arguments = {
            "eta": (F(1, 10), F(-1, 5)),
            "visible_offset": (F(3, 10), F(2, 5)),
            "correction_thrust": F(1, 2),
            "physical_residual": F(24383, 24000),
            "measurement_noise": F(1, 100),
        }

        miss = update("miss", **arguments)
        success = update("success", **arguments)

        self.assertEqual(miss.get("eta_next"), (F(12, 125), F(-215617, 1200000)))
        self.assertEqual(miss.get("visible_offset_next"), (F(77, 250), F(41, 100)))
        self.assertEqual(miss.get("tracking_error_next"), (F(101, 250), F(276383, 1200000)))
        self.assertEqual(success.get("eta_next"), (F(-1, 100), F(-788017, 1200000)))
        self.assertEqual(success.get("visible_offset_next"), (F(207, 500), F(887, 1000)))
        self.assertEqual(success.get("tracking_error_next"), (F(101, 250), F(276383, 1200000)))
        self.assertTrue(miss.get("split_identity_holds"))
        self.assertTrue(success.get("split_identity_holds"))

    def test_fixed_absolute_residual_makes_control_effect_a_center_translation(self):
        subject = _subject()
        compare = getattr(subject, "compare_corrections_with_fixed_residual", lambda *args, **kwargs: {})

        for label in ("miss", "success"):
            result = compare(
                label,
                eta=(F(1, 10), F(-1, 5)),
                visible_offset=(F(3, 10), F(2, 5)),
                first_correction=F(-1),
                second_correction=F(2),
                physical_residual=F(7, 5),
                measurement_noise=F(1, 100),
            )
            self.assertEqual(result.get("eta_translation"), (F(0), F(0)))
            self.assertEqual(result.get("tracking_error_translation"), (F(0), F(3, 50)))
            self.assertEqual(result.get("visible_offset_translation"), (F(0), F(3, 50)))
            self.assertTrue(result.get("shape_unchanged_for_fixed_residual_set"))

    def test_scheduled_residual_changes_joint_shape_but_cancels_from_visible_offset(self):
        subject = _subject()
        column = getattr(subject, "scheduled_residual_generator", lambda *args, **kwargs: ())

        low = column(F(981, 200))
        high = column(F(2943, 200))
        self.assertEqual(low, (F(0), F(413221, 8000000), F(0), F(413221, 8000000)))
        self.assertEqual(high, (F(0), F(572143, 8000000), F(0), F(572143, 8000000)))
        self.assertEqual(
            tuple(high[index] - low[index] for index in range(4)),
            (F(0), F(79461, 4000000), F(0), F(79461, 4000000)),
        )
        self.assertEqual((low[2] - low[0], low[3] - low[1]), (F(0), F(0)))
        self.assertEqual((high[2] - high[0], high[3] - high[1]), (F(0), F(0)))

    def test_run136_global_column_dominates_scheduled_range_exactly(self):
        subject = _subject()
        certificate = getattr(subject, "control_translation_certificate", lambda: {})()
        residual = certificate.get("residual_envelopes", {})

        self.assertEqual(residual.get("actual_thrust_interval"), (F(981, 200), F(2943, 200)))
        self.assertEqual(residual.get("scheduled_width_at_lower"), F(413221, 160000))
        self.assertEqual(residual.get("scheduled_width_at_upper"), F(572143, 160000))
        self.assertEqual(residual.get("run136_vertical_step_generator"), F(572143, 8000000))
        self.assertEqual(residual.get("scheduled_step_generator_increase"), F(79461, 4000000))
        self.assertTrue(residual.get("global_envelope_contains_all_scheduled_widths"))
        self.assertTrue(residual.get("run136_column_matches_global_upper_envelope"))

    def test_claim_separates_fixed_envelope_from_decision_dependent_branch(self):
        subject = _subject()
        result = getattr(subject, "run", lambda: {})()

        self.assertEqual(result.get("status"), "pass")
        self.assertEqual(
            result.get("evidence_level"),
            "exact_vertical_control_translation_and_residual_shape_split",
        )
        self.assertEqual(result.get("fixed_envelope_control_effect"), "translation_only")
        self.assertEqual(result.get("scheduled_residual_control_effect"), "translation_and_shape")
        self.assertTrue(result.get("fixed_W_intrinsic_shape_interface_available"))
        self.assertFalse(result.get("scheduled_W_fixed_disturbance_theorem_directly_applicable"))
        self.assertFalse(result.get("zero_center_target_is_policy_independent"))
        self.assertTrue(result.get("run148_shape_valid_under_global_envelope_up_to_translation"))
        self.assertFalse(result.get("is_rci_certificate"))
        self.assertFalse(result.get("full_six_state_guarantee"))

    def test_checker_writes_a_hash_bound_exact_artifact(self):
        subject_path = ROOT / "verification/check_vertical_control_translation_split.py"
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
                (ROOT / "results/theory_vertical_control_translation_split_20261003/exact_checks.json").read_text()
            )
            self.assertEqual(artifact, archived)
            for dependency in (
                "verification/check_vertical_control_translation_split.py",
                "verification/test_vertical_control_translation_split.py",
                "verification/check_vertical_multi_return_template.py",
                "verification/check_hover_partial_information_contract.py",
                "verification/check_cycle_lifted_zonotope.py",
                "configs/planar_baseline.json",
                "docs/learning/86_vertical_control_translation_split.md",
                "docs/literature/READ_PAPERS.md",
                "docs/research/run149_literature_gate.md",
                "docs/research/run149_research_log.md",
            ):
                self.assertEqual(
                    artifact["source_sha256"].get(dependency),
                    hashlib.sha256((ROOT / dependency).read_bytes()).hexdigest(),
                )


if __name__ == "__main__":
    unittest.main()
