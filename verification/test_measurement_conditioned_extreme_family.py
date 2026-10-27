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


def _subject():
    try:
        return importlib.import_module("check_measurement_conditioned_extreme_family")
    except ModuleNotFoundError:
        return None


class MeasurementConditionedExtremeFamilyTests(unittest.TestCase):
    def test_measurement_domain_and_boundary_posteriors_are_exact(self):
        subject = _subject()
        self.assertIsNotNone(subject)
        self.assertEqual(subject.measurement_center_domain(), (-F(51, 50), F(51, 50)))
        expected = {
            -F(51, 50): (-F(1), -F(1)),
            -F(49, 50): (-F(1), -F(24, 25)),
            F(0): (-F(1, 50), F(1, 50)),
            F(49, 50): (F(24, 25), F(1)),
            F(51, 50): (F(1), F(1)),
        }
        for center, interval in expected.items():
            with self.subTest(center=center):
                self.assertEqual(subject.posterior_interval(center), interval)
        with self.assertRaises(ValueError):
            subject.posterior_interval(F(52, 50))

    def test_every_boundary_posterior_is_covered_by_clamped_maximal_center(self):
        subject = _subject()
        self.assertIsNotNone(subject)
        for center in (-F(51, 50), -F(1), -F(49, 50), F(0), F(49, 50), F(1), F(51, 50)):
            with self.subTest(center=center):
                clipped = subject.clamped_center(center)
                self.assertGreaterEqual(clipped, -F(49, 50))
                self.assertLessEqual(clipped, F(49, 50))
                left, right = subject.posterior_interval(center)
                outer_left, outer_right = subject.maximal_position_interval(clipped)
                self.assertGreaterEqual(left, outer_left)
                self.assertLessEqual(right, outer_right)

    def test_tight_six_direction_offsets_are_affine_and_configured(self):
        subject = _subject()
        self.assertIsNotNone(subject)
        expected = {
            -F(49, 50): [-F(24, 25), F(11, 4), F(51, 40), F(1), F(11, 4), -F(137, 200)],
            F(0): [F(1, 50), F(11, 4), F(59, 200), F(1, 50), F(11, 4), F(59, 200)],
            F(49, 50): [F(1), F(11, 4), -F(137, 200), -F(24, 25), F(11, 4), F(51, 40)],
        }
        for center, offsets in expected.items():
            with self.subTest(center=center):
                self.assertEqual(subject.tight_offsets(center), offsets)
                self.assertTrue(subject.configuration_valid(offsets))

    def test_distinct_maximal_rectangles_are_incomparable(self):
        subject = _subject()
        self.assertIsNotNone(subject)
        centers = (-F(49, 50), -F(1, 3), F(0), F(2, 5), F(49, 50))
        for outer in centers:
            for inner in centers:
                with self.subTest(outer=outer, inner=inner):
                    self.assertEqual(subject.rectangle_contains(outer, inner), outer == inner)

    def test_two_parameter_vertices_do_not_replace_continuum_boundary(self):
        subject = _subject()
        self.assertIsNotNone(subject)
        result = subject.run()
        self.assertEqual(result["parameter_polytope_vertex_count"], 2)
        self.assertEqual(result["true_extreme_set_boundary_cardinality"], "continuum")
        self.assertTrue(result["endpoint_extreme_sets_incomparable"])
        self.assertTrue(result["all_nonempty_measurement_posteriors_covered"])
        self.assertTrue(result["measurement_closed_information_ensemble"])
        self.assertFalse(result["regular_six_facet_meta_configuration_certified"])
        self.assertFalse(result["graph_invariant_information_ensemble_certified"])
        self.assertFalse(result["mpc_recursive_feasibility_certified"])
        self.assertFalse(result["full_six_state_guarantee"])

    def test_cli_artifact_is_hash_bound_and_reproducible(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "exact_checks.json"
            completed = subprocess.run(
                [sys.executable, str(ROOT / "verification/check_measurement_conditioned_extreme_family.py"),
                 "--output", str(output)],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            generated = json.loads(output.read_text())
            archived = json.loads((
                ROOT / "results/theory_measurement_conditioned_extreme_family_20261027/exact_checks.json"
            ).read_text())
            self.assertEqual(generated, archived)
            required = {
                "verification/check_measurement_conditioned_extreme_family.py",
                "verification/test_measurement_conditioned_extreme_family.py",
                "verification/check_six_facet_measurement_gate.py",
                "verification/check_houska_vertical_adapter.py",
                "configs/planar_baseline.json",
                "docs/superpowers/specs/2026-10-27-measurement-conditioned-extreme-family-design.md",
            }
            self.assertEqual(set(generated["source_sha256"]), required)
            for name, digest in generated["source_sha256"].items():
                self.assertEqual(digest, hashlib.sha256((ROOT / name).read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
