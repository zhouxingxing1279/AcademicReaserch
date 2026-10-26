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
        return importlib.import_module("check_lifted_cell_composability")
    except ModuleNotFoundError:
        return None


class LiftedCellComposabilityTests(unittest.TestCase):
    def test_miss_edges_leave_the_equal_centered_position_cell(self):
        """Ignoring d_p^+=d_p+h*d_v would falsely chain the local cells."""
        subject = _subject()
        certify = getattr(subject, "composability_certificate", None)

        self.assertTrue(callable(certify))
        rows = {
            (row["source_mode"], row["target_mode"], row["edge_label"]): row
            for row in certify()["edges"]
        }
        for key in ((0, 1, "miss"), (4, 5, "miss")):
            self.assertEqual(rows[key]["d_position_support"], F(41, 200))
            self.assertEqual(rows[key]["d_velocity_support"], F(1, 4))
            self.assertEqual(rows[key]["position_excess_over_target_cell"], F(1, 200))
            self.assertFalse(rows[key]["contained_in_equal_centered_target_d_cell"])

    def test_mode_four_success_requires_much_larger_visible_target_widths(self):
        """Dropping the innovation columns would understate the success image."""
        subject = _subject()
        result = getattr(subject, "composability_certificate", lambda: {})()
        success_rows = [
            row for row in result.get("edges", []) if row["edge_label"] == "success"
        ]

        self.assertEqual(len(success_rows), 1)
        success = success_rows[0]
        self.assertEqual(success["d_position_support"], F(2624143, 7200000))
        self.assertEqual(success["d_velocity_support"], F(1548143, 1600000))
        self.assertEqual(
            success["position_excess_over_target_cell"], F(1184143, 7200000)
        )
        self.assertEqual(
            success["velocity_excess_over_target_cell"], F(1148143, 1600000)
        )
        self.assertFalse(success["contained_in_equal_centered_target_d_cell"])

    def test_local_normal_closure_is_not_relabelled_as_cell_graph_closure(self):
        subject = _subject()
        run = getattr(subject, "run", None)

        self.assertTrue(callable(run))
        result = run()
        self.assertTrue(result["run180_local_target_normals_closed"])
        self.assertTrue(result["run181_local_target_normals_closed"])
        self.assertFalse(result["existing_cells_form_a_composable_graph"])
        self.assertEqual(
            result["evidence_level"],
            "exact_visible_successor_support_noncontainment_certificate",
        )
        self.assertFalse(result["finite_cell_cover_impossible"])
        self.assertFalse(result["terminal_family_closed"])
        self.assertFalse(result["recursive_feasibility_certified"])

    def test_checker_writes_reproducible_hash_bound_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "exact_checks.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "verification/check_lifted_cell_composability.py"),
                    "--output",
                    str(output),
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            generated = json.loads(output.read_text())
            archived = json.loads((
                ROOT
                / "results/theory_lifted_cell_composability_20261026/exact_checks.json"
            ).read_text())
            self.assertEqual(generated, archived)
            for name, digest in generated["source_sha256"].items():
                self.assertEqual(
                    digest,
                    hashlib.sha256((ROOT / name).read_bytes()).hexdigest(),
                )


if __name__ == "__main__":
    unittest.main()
