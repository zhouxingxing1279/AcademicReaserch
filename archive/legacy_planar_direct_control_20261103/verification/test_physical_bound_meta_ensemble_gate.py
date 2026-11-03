import importlib
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
NORMALS = [
    [F(1), F(0)], [F(0), F(1)], [-F(1), F(1, 10)],
    [-F(1), F(0)], [F(0), -F(1)], [F(1), -F(1, 10)],
]
BOX_VERTICES = [
    [F(p), F(v) * F(11, 4)] for p in (-1, 1) for v in (-1, 1)
]


def _subject():
    try:
        return importlib.import_module("check_physical_bound_meta_ensemble_gate")
    except ModuleNotFoundError:
        return None


class PhysicalBoundMetaEnsembleGateTests(unittest.TestCase):
    def test_physical_box_support_vector_is_exact(self):
        subject = _subject()
        self.assertIsNotNone(subject)
        expected = [F(1), F(11, 4), F(51, 40), F(1), F(11, 4), F(51, 40)]
        self.assertEqual(subject.physical_support_vector(), expected)
        independent = [
            max(n[0] * x[0] + n[1] * x[1] for x in BOX_VERTICES)
            for n in NORMALS
        ]
        self.assertEqual(independent, expected)

    def test_support_vector_represents_exactly_the_physical_box(self):
        result = _subject().run()
        self.assertTrue(result["physical_box_equals_dominating_polytope"])
        self.assertTrue(result["dominating_offsets_in_configuration_cone"])
        self.assertEqual(result["configured_vertex_set"], BOX_VERTICES)

    def test_physical_containment_has_single_extreme_set(self):
        result = _subject().run()
        self.assertEqual(result["extreme_set_count"], 1)
        self.assertEqual(result["extreme_set_offsets"], [result["physical_support_offsets"]])
        self.assertTrue(result["all_admissible_sets_contained_in_extreme_set"])

    def test_result_stops_before_variable_meta_family_or_control_claims(self):
        result = _subject().run()
        self.assertEqual(
            result["evidence_level"],
            "exact_physical_bound_meta_ensemble_singleton_extreme_set",
        )
        self.assertFalse(result["variable_H_Omega_family_certified"])
        self.assertFalse(result["graph_invariant_information_ensemble_certified"])
        self.assertFalse(result["mpc_recursive_feasibility_certified"])
        self.assertFalse(result["full_six_state_guarantee"])

    def test_cli_artifact_is_hash_bound_and_reproducible(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "exact_checks.json"
            completed = subprocess.run(
                [sys.executable, str(ROOT / "verification/check_physical_bound_meta_ensemble_gate.py"),
                 "--output", str(output)],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            generated = json.loads(output.read_text())
            archived = json.loads((
                ROOT / "results/theory_physical_bound_meta_ensemble_gate_20261027/exact_checks.json"
            ).read_text())
            self.assertEqual(generated, archived)
            required = {
                "verification/check_physical_bound_meta_ensemble_gate.py",
                "verification/test_physical_bound_meta_ensemble_gate.py",
                "verification/check_six_facet_measurement_gate.py",
                "verification/check_houska_vertical_adapter.py",
                "configs/planar_baseline.json",
                "docs/superpowers/specs/2026-10-27-physical-bound-meta-ensemble-gate-design.md",
            }
            self.assertEqual(set(generated["source_sha256"]), required)
            for name, digest in generated["source_sha256"].items():
                self.assertEqual(digest, hashlib.sha256((ROOT / name).read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
