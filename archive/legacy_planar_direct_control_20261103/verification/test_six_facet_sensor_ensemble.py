import importlib
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
KAPPA = F(1, 10)
INDEPENDENT_NORMALS = [
    [F(1), F(0)], [F(0), F(1)], [-F(1), KAPPA],
    [-F(1), F(0)], [F(0), -F(1)], [F(1), -KAPPA],
]


def _subject():
    try:
        return importlib.import_module("check_six_facet_sensor_ensemble")
    except ModuleNotFoundError:
        return None


def _independent_vertices(offsets):
    """Enumerate every feasible pairwise facet intersection without template maps."""
    vertices = []
    for first in range(6):
        for second in range(first + 1, 6):
            a, b = INDEPENDENT_NORMALS[first]
            c, d = INDEPENDENT_NORMALS[second]
            determinant = a * d - b * c
            if determinant == 0:
                continue
            candidate = [
                (d * offsets[first] - b * offsets[second]) / determinant,
                (-c * offsets[first] + a * offsets[second]) / determinant,
            ]
            if all(
                normal[0] * candidate[0] + normal[1] * candidate[1] <= bound
                for normal, bound in zip(INDEPENDENT_NORMALS, offsets)
            ):
                vertices.append(candidate)
    return vertices


class SixFacetSensorEnsembleTests(unittest.TestCase):
    def test_measurement_meta_row_uses_position_halfwidth(self):
        """Using diameter or the wrong opposite facet changes the sensor ensemble."""
        subject = _subject()
        self.assertIsNotNone(subject)
        self.assertEqual(
            subject.measurement_meta_row(),
            [F(1, 2), F(0), F(0), F(1, 2), F(0), F(0)],
        )

    def test_configured_asymmetric_offsets_have_exact_position_supports(self):
        """Treating offsets as radii would lose a translated measurement fiber."""
        subject = _subject()
        offsets = [F(4, 3), F(3, 2), F(37, 60), F(2, 3), F(5, 2), F(83, 60)]
        result = subject.compatible_measurement_interval(offsets, F(6, 5))
        self.assertEqual(result["position_max"], F(4, 3))
        self.assertEqual(result["position_min"], F(-2, 3))
        self.assertEqual(result["center_interval"], [F(2, 15), F(8, 15)])
        self.assertTrue(result["compatible"])
        self.assertEqual(result["measurement_meta_coordinate"], F(1))
        self.assertTrue(result["meta_compatible"])

    def test_exact_two_a_boundary_is_a_single_measurement_center(self):
        """Comparing width with a instead of 2a rejects the exact boundary."""
        subject = _subject()
        offsets = [F(4, 3), F(3, 2), F(37, 60), F(2, 3), F(5, 2), F(83, 60)]
        boundary = subject.compatible_measurement_interval(offsets, F(1))
        self.assertEqual(boundary["center_interval"], [F(1, 3), F(1, 3)])
        self.assertTrue(boundary["compatible"])
        too_narrow = subject.compatible_measurement_interval(offsets, F(1, 2))
        self.assertEqual(too_narrow["center_interval"], [F(5, 6), F(-1, 6)])
        self.assertFalse(too_narrow["compatible"])
        self.assertFalse(too_narrow["meta_compatible"])

    def test_general_configured_offsets_match_independent_vertex_enumeration(self):
        """The width row must hold beyond translated centrally symmetric witnesses."""
        subject = _subject()
        configured = 0
        noncentral = 0
        values = [F(1, 2), F(3, 4), F(1), F(5, 4), F(3, 2)]
        for offsets in product(values, repeat=6):
            vertices = _independent_vertices(offsets)
            facet_active = [
                any(normal[0] * vertex[0] + normal[1] * vertex[1] == bound
                    for vertex in vertices)
                for normal, bound in zip(INDEPENDENT_NORMALS, offsets)
            ]
            if len(vertices) != 6 or not all(facet_active):
                continue
            configured += 1
            if len({offsets[index] + offsets[index + 3] for index in range(3)}) > 1:
                noncentral += 1
            position_max = max(vertex[0] for vertex in vertices)
            position_min = min(vertex[0] for vertex in vertices)
            width = position_max - position_min
            for halfwidth in [width / 2 - F(1, 20), width / 2, width / 2 + F(1, 20)]:
                result = subject.compatible_measurement_interval(offsets, halfwidth)
                self.assertEqual(result["position_max"], position_max)
                self.assertEqual(result["position_min"], position_min)
                self.assertEqual(result["compatible"], width <= 2 * halfwidth)
        self.assertEqual(configured, 625)
        self.assertEqual(noncentral, 540)

    def test_invalid_configuration_is_rejected_before_evidence(self):
        """A width identity outside the selected vertex configuration is not admissible."""
        subject = _subject()
        invalid = [F(1, 10), F(11, 4), F(1), F(1, 10), F(11, 4), F(1)]
        with self.assertRaisesRegex(AssertionError, "configuration"):
            subject.compatible_measurement_interval(invalid, F(1, 50))

    def test_run_limits_claim_to_the_measurement_row(self):
        """Eliminating center enumeration must not become a graph or MPC theorem."""
        subject = _subject()
        result = subject.run()
        self.assertEqual(
            result["evidence_level"],
            "exact_six_facet_sensor_ensemble_measurement_row",
        )
        self.assertTrue(result["continuous_measurement_centers_represented"])
        self.assertFalse(result["complete_Z_H_Omega_certified"])
        self.assertFalse(result["graph_invariant_information_ensemble_certified"])
        self.assertFalse(result["input_feasibility_certified"])
        self.assertFalse(result["terminal_invariance_certified"])
        self.assertFalse(result["mpc_recursive_feasibility_certified"])
        self.assertFalse(result["full_six_state_guarantee"])
        self.assertEqual(result["assumptions"], [
            "G*y <= 0 for the Run186 six-facet configuration",
            "P(y) is nonempty",
            "C = [1, 0] and measurement noise is [-a, a]",
        ])

    def test_cli_artifact_is_hash_bound_and_reproducible(self):
        """A stale sensor-ensemble archive must fail after any source contract changes."""
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "exact_checks.json"
            completed = subprocess.run(
                [sys.executable, str(ROOT / "verification/check_six_facet_sensor_ensemble.py"),
                 "--output", str(output)],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            generated = json.loads(output.read_text())
            archived = json.loads((
                ROOT / "results/theory_six_facet_sensor_ensemble_20261027/exact_checks.json"
            ).read_text())
            self.assertEqual(generated, archived)
            for name, digest in generated["source_sha256"].items():
                self.assertEqual(
                    digest,
                    hashlib.sha256((ROOT / name).read_bytes()).hexdigest(),
                )


if __name__ == "__main__":
    unittest.main()
