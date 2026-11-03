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
        return importlib.import_module("check_vertical_joint_second_sweep")
    except ModuleNotFoundError:
        return None


class VerticalJointSecondSweepTests(unittest.TestCase):
    def test_edge_pullback_has_exact_dynamics_and_shared_innovation_support(self):
        """Wrong-sign dynamics or splitting q and n must fail exact literals."""
        subject = _subject()
        pullback = getattr(subject, "_edge_pullback_facets", None)

        self.assertTrue(callable(pullback))
        self.assertEqual(
            pullback([(F(2), F(3), F(5))], "miss", F(7)),
            [(F(2), F(76, 25), F(5))],
        )
        self.assertEqual(
            pullback([(F(2), F(3), F(5))], "success", F(1, 7)),
            [(F(2), F(76, 25), F(39, 14))],
        )
        self.assertEqual(
            pullback([(F(-9), F(2), F(11))], "success", F(123)),
            [(F(-9), F(91, 50), F(11))],
        )

    def test_second_sweep_retains_fourteen_modes_and_collapses_mode_fourteen(self):
        """Reporting all modes nonempty or accepting a line/point must fail."""
        subject = _subject()
        certify = getattr(subject, "second_sweep_full_fiber_zero_policy", None)

        self.assertTrue(callable(certify))
        result = certify()
        self.assertEqual(set(result["modes"]), set(range(15)))
        self.assertEqual(result["positive_volume_mode_count"], 14)
        self.assertEqual(result["collapsed_modes"], [14])
        for mode in range(14):
            row = result["modes"][mode]
            self.assertFalse(row["second_sweep_observation_projection_empty"])
            self.assertGreater(row["second_sweep_observation_projection_area"], 0)
            self.assertEqual(row["joint_inner_dimension"], 4)
        self.assertTrue(
            result["modes"][14]["second_sweep_observation_projection_empty"]
        )
        self.assertEqual(
            result["modes"][0]["second_sweep_observation_projection_area"],
            F(53862840297880234229399, 9216000000000000000000),
        )
        self.assertEqual(
            result["modes"][9]["second_sweep_observation_projection_area"],
            F(111387579346946906251, 207360000000000000000),
        )

    def test_mode_fourteen_has_an_exact_input_independent_width_obstruction(self):
        """A sampled emptiness result or a shift-only argument must fail."""
        subject = _subject()
        result = getattr(subject, "second_sweep_full_fiber_zero_policy", lambda: {})()
        obstruction = result.get("mode14_width_obstruction", {})

        self.assertEqual(
            obstruction.get("success_innovation_halfwidth"),
            F(24272147, 48000000),
        )
        self.assertEqual(
            obstruction.get("success_velocity_spread"),
            F(72816441, 32000000),
        )
        self.assertEqual(
            obstruction.get("mode_zero_target_velocity_halfwidth"),
            F(94125081847, 57600000000),
        )
        self.assertEqual(
            obstruction.get("strict_halfwidth_excess"),
            F(36944511953, 57600000000),
        )
        self.assertTrue(obstruction.get("strict_width_obstruction"))
        self.assertTrue(obstruction.get("correction_only_translates_interval"))

    def test_unknown_success_miss_branches_share_the_zero_correction(self):
        """Choosing a different current input after the packet outcome must fail."""
        subject = _subject()
        result = getattr(subject, "second_sweep_full_fiber_zero_policy", lambda: {})()

        self.assertEqual(result.get("graph_edge_count"), 17)
        self.assertEqual(result.get("shared_correction_thrust"), F(0))
        self.assertEqual(
            sum(len(row["edges"]) for row in result.get("modes", {}).values()),
            17,
        )
        for mode, targets in ((4, {(5, "miss"), (0, "success")}),
                              (9, {(10, "miss"), (0, "success")})):
            row = result["modes"][mode]
            self.assertEqual(row["policy_values_on_observation_projection"], 1)
            self.assertEqual(
                {(edge["target"], edge["label"]) for edge in row["edges"]},
                targets,
            )

    def test_claim_is_limited_to_the_complete_fiber_candidate_class(self):
        """A mode-14 collapse must not be relabelled as general RCI impossibility."""
        subject = _subject()
        run = getattr(subject, "run", None)

        self.assertTrue(callable(run))
        result = run()
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["descending_sweep_iterations"], 2)
        self.assertEqual(
            result["evidence_level"],
            "exact_mode14_width_obstruction_for_complete_fiber_second_sweep",
        )
        self.assertTrue(result["complete_fiber_candidate_class_rejected"])
        self.assertFalse(result["general_joint_information_rci_rejected"])
        self.assertFalse(result["is_rci_certificate"])
        self.assertFalse(result["full_six_state_guarantee"])

    def test_checker_writes_a_hash_bound_exact_artifact(self):
        """An unarchived result or omitted direct dependency must fail."""
        subject_path = ROOT / "verification/check_vertical_joint_second_sweep.py"
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
                (ROOT / "results/theory_vertical_joint_second_sweep_20261003/exact_checks.json").read_text()
            )
            self.assertEqual(artifact["status"], "pass")
            self.assertEqual(artifact["collapsed_modes"], [14])
            self.assertEqual(archived, artifact)
            for dependency in (
                "verification/check_vertical_joint_second_sweep.py",
                "verification/test_vertical_joint_second_sweep.py",
                "verification/check_vertical_joint_first_sweep.py",
                "verification/check_vertical_joint_predecessor.py",
                "verification/check_vertical_causal_predecessor.py",
                "verification/check_rolling_control_normal_ledger.py",
                "verification/test_rolling_control_normal_ledger.py",
                "verification/check_cycle_lifted_zonotope.py",
                "verification/check_mode_nestedness.py",
                "verification/check_mode_radius.py",
                "verification/check_intermittent_metric.py",
                "configs/planar_baseline.json",
                "docs/learning/83_vertical_joint_second_sweep.md",
                "docs/literature/READ_PAPERS.md",
                "docs/research/run146_literature_gate.md",
                "docs/research/run146_research_log.md",
            ):
                self.assertEqual(
                    artifact["source_sha256"].get(dependency),
                    hashlib.sha256((ROOT / dependency).read_bytes()).hexdigest(),
                )


if __name__ == "__main__":
    unittest.main()
