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
        return importlib.import_module("check_vertical_joint_first_sweep")
    except ModuleNotFoundError:
        return None


class VerticalJointFirstSweepTests(unittest.TestCase):
    def test_all_fifteen_modes_retain_positive_volume_full_fiber_inner_sets(self):
        """Dropping any mode or accepting a point/line certificate must fail."""
        subject = _subject()
        certify = getattr(subject, "first_sweep_inner_certificates", None)

        self.assertTrue(callable(certify))
        result = certify()
        self.assertEqual(set(result["modes"]), set(range(15)))
        self.assertEqual(result["nonempty_mode_count"], 15)
        for mode in range(15):
            row = result["modes"][mode]
            self.assertTrue(row["positive_volume_inner_certificate"])
            self.assertEqual(row["joint_inner_dimension"], 4)
            self.assertGreater(row["eta_projection_area"], 0)
            self.assertGreater(row["observation_projection_area"], 0)

    def test_mode_fourteen_projection_has_the_hand_checked_exact_area(self):
        """A sampled or floating projection must not replace exact rational geometry."""
        subject = _subject()
        result = getattr(subject, "first_sweep_inner_certificates", lambda: {})()
        row = result.get("modes", {}).get(14, {})

        self.assertEqual(
            row.get("observation_projection_area"),
            F(899947970530621291, 691200000000000000),
        )
        self.assertEqual(row.get("observation_projection_facet_count"), 4)
        self.assertEqual(row.get("shared_correction_thrust"), F(0))

    def test_one_policy_per_mode_covers_all_seventeen_graph_edges(self):
        """Selecting inputs after observing a packet outcome must fail this test."""
        subject = _subject()
        result = getattr(subject, "first_sweep_inner_certificates", lambda: {})()

        self.assertEqual(result.get("graph_edge_count"), 17)
        self.assertEqual(
            sum(len(row["edges"]) for row in result.get("modes", {}).values()),
            17,
        )
        for mode, row in result["modes"].items():
            self.assertEqual(row["policy_values_on_observation_projection"], 1)
            self.assertTrue(all(edge["eta_target_contained"] for edge in row["edges"]))
            if mode in (4, 9):
                self.assertEqual(len(row["edges"]), 2)

    def test_zero_policy_projection_contains_the_run144_common_box(self):
        """A claimed extension that loses the previously certified common box must fail."""
        subject = _subject()
        result = getattr(subject, "first_sweep_inner_certificates", lambda: {})()

        self.assertEqual(result.get("common_observation_box_halfwidths"), (F(1, 5), F(1, 4)))
        for row in result["modes"].values():
            self.assertTrue(row["contains_run144_common_observation_box"])

    def test_result_is_only_a_conservative_first_sweep_inner_certificate(self):
        """One descending predecessor layer must never be relabelled as an RCI."""
        subject = _subject()
        run = getattr(subject, "run", None)

        self.assertTrue(callable(run))
        result = run()
        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["descending_sweep_iterations"], 1)
        self.assertEqual(
            result["evidence_level"],
            "exact_positive_volume_inner_certificates_for_all_fifteen_first_sweep_modes",
        )
        self.assertFalse(result["is_maximal_observation_projection"])
        self.assertFalse(result["is_rci_certificate"])
        self.assertFalse(result["fixed_point_iteration_run"])
        self.assertFalse(result["full_six_state_guarantee"])

    def test_checker_writes_a_hash_bound_exact_artifact(self):
        """An unarchived result or omitted direct dependency must fail."""
        subject_path = ROOT / "verification/check_vertical_joint_first_sweep.py"
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
            self.assertEqual(artifact["status"], "pass")
            self.assertEqual(len(artifact["modes"]), 15)
            for dependency in (
                "verification/check_vertical_joint_first_sweep.py",
                "verification/test_vertical_joint_first_sweep.py",
                "verification/check_vertical_joint_predecessor.py",
                "verification/check_vertical_causal_predecessor.py",
                "verification/check_cycle_lifted_zonotope.py",
                "configs/planar_baseline.json",
                "docs/learning/82_vertical_joint_first_sweep.md",
                "docs/literature/READ_PAPERS.md",
                "docs/research/run145_literature_gate.md",
                "docs/research/run145_research_log.md",
            ):
                self.assertEqual(
                    artifact["source_sha256"].get(dependency),
                    hashlib.sha256((ROOT / dependency).read_bytes()).hexdigest(),
                )


if __name__ == "__main__":
    unittest.main()
