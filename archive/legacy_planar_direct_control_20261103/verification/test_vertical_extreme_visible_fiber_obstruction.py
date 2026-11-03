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
    return importlib.import_module("check_vertical_extreme_visible_fiber_obstruction")


class VerticalExtremeVisibleFiberObstructionTests(unittest.TestCase):
    def test_positive_extreme_observation_is_reachable_and_fixes_nonzero_primitives(self):
        certificate = _subject().extreme_visible_fiber_certificate()
        fiber = certificate["extreme_fiber"]

        self.assertEqual(fiber["visible_dp"], F(24272147, 48000000))
        self.assertTrue(fiber["witness_in_generator_box"])
        self.assertEqual(fiber["visible_equality_residual"], F(0))
        self.assertTrue(fiber["all_nonzero_visible_primitives_fixed_at_support_sign"])

    def test_entire_extreme_fiber_starts_beyond_the_unit_endpoint_direction(self):
        certificate = _subject().extreme_visible_fiber_certificate()
        interval = certificate["initial_endpoint_direction_interval"]

        self.assertEqual(interval["lower"], F(3745601423, 3600000000))
        self.assertEqual(interval["upper"], F(3889781459, 3600000000))
        self.assertGreater(interval["lower"], F(1))

    def test_worst_future_residual_cancels_maximum_negative_control_authority(self):
        certificate = _subject().extreme_visible_fiber_certificate()
        balance = certificate["fourteen_miss_balance"]

        self.assertEqual(balance["positive_residual_shift"], F(52065013, 400000000))
        self.assertEqual(balance["maximum_negative_control_shift"], -balance["positive_residual_shift"])
        self.assertEqual(balance["certified_endpoint_lower_bound"], F(3889781459, 3600000000))
        self.assertEqual(balance["strict_position_violation"], F(289781459, 3600000000))

    def test_claim_scope_is_strategy_independent_but_contract_specific(self):
        result = _subject().run()

        self.assertEqual(result["status"], "pass")
        self.assertTrue(result["allows_optimistic_full_state_causal_feedback"])
        self.assertTrue(result["rules_out_current_fifteen_tick_contract"])
        self.assertFalse(result["rules_out_other_seed_or_residual_contracts"])
        self.assertFalse(result["is_recursive_feasibility_proof"])
        self.assertFalse(result["full_six_state_guarantee"])

    def test_checker_writes_hash_bound_reproducible_artifact(self):
        subject_path = ROOT / "verification/check_vertical_extreme_visible_fiber_obstruction.py"
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
                (ROOT / "results/theory_vertical_extreme_visible_fiber_obstruction_20261012/exact_checks.json").read_text()
            )
            self.assertEqual(artifact, archived)
            for dependency in (
                "verification/check_vertical_extreme_visible_fiber_obstruction.py",
                "verification/test_vertical_extreme_visible_fiber_obstruction.py",
                "verification/check_vertical_visible_fiber_width.py",
                "verification/check_vertical_correlated_return_seed.py",
                "verification/check_cycle_lifted_zonotope.py",
                "configs/planar_baseline.json",
                "docs/learning/101_vertical_extreme_visible_fiber_obstruction.md",
                "docs/literature/READ_PAPERS.md",
                "docs/research/run165_literature_gate.md",
                "docs/research/run165_research_log.md",
            ):
                self.assertEqual(
                    artifact["source_sha256"][dependency],
                    hashlib.sha256((ROOT / dependency).read_bytes()).hexdigest(),
                )


if __name__ == "__main__":
    unittest.main()
