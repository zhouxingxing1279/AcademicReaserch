import importlib
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]

def _subject():
    return importlib.import_module("check_vertical_visible_fiber_width")


class VerticalVisibleFiberWidthTests(unittest.TestCase):
    def test_exact_primal_dual_certificate_matches(self):
        result = _subject().visible_fiber_width_certificate()
        cert = result["fiber_lp_certificate"]

        self.assertEqual(cert["visible_equality_residual"], F(0))
        self.assertTrue(cert["box_feasible"])
        self.assertEqual(cert["primal_objective"], F(16315003, 75000000))
        self.assertEqual(cert["dual_objective"], cert["primal_objective"])
        self.assertEqual(cert["dual_lambda"], F(29, 15))
        self.assertEqual(cert["fractional_pivot_index"], 3)
        self.assertEqual(cert["fractional_pivot_value"], F(-26445009, 75715726))

    def test_conditioning_reverses_the_old_unconditional_gate(self):
        result = _subject().visible_fiber_width_certificate()
        comparison = result["comparison"]

        self.assertEqual(
            comparison["unconditional_direction_halfwidth"],
            F(3889781459, 3600000000),
        )
        self.assertGreater(comparison["unconditional_direction_halfwidth"], F(1))
        self.assertLess(comparison["worst_visible_fiber_halfwidth"], F(1))
        self.assertEqual(
            comparison["conditioning_reduction"],
            comparison["unconditional_direction_halfwidth"]
            - comparison["worst_visible_fiber_halfwidth"],
        )

    def test_claim_scope_does_not_promote_a_seed_gate_to_closed_loop_proof(self):
        result = _subject().run()

        self.assertEqual(result["status"], "pass")
        self.assertTrue(result["all_visible_fibers_pass_unit_seed_gate"])
        self.assertFalse(result["is_recursive_feasibility_proof"])
        self.assertFalse(result["is_fifteen_tick_safety_proof"])
        self.assertFalse(result["full_six_state_guarantee"])

    def test_checker_writes_hash_bound_reproducible_artifact(self):
        subject_path = ROOT / "verification/check_vertical_visible_fiber_width.py"
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
                (ROOT / "results/theory_vertical_visible_fiber_width_20261012/exact_checks.json").read_text()
            )
            self.assertEqual(artifact, archived)
            for dependency in (
                "verification/check_vertical_visible_fiber_width.py",
                "verification/test_vertical_visible_fiber_width.py",
                "verification/check_vertical_correlated_return_seed.py",
                "configs/planar_baseline.json",
                "docs/learning/100_vertical_visible_fiber_seed_gate.md",
                "docs/literature/READ_PAPERS.md",
                "docs/research/run164_literature_gate.md",
                "docs/research/run164_research_log.md",
            ):
                self.assertEqual(
                    artifact["source_sha256"][dependency],
                    hashlib.sha256((ROOT / dependency).read_bytes()).hexdigest(),
                )


if __name__ == "__main__":
    unittest.main()
