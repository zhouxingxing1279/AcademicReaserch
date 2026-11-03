import importlib
from fractions import Fraction as F
import hashlib
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
KAPPA = F(1, 10)
NORMALS = [
    [F(1), F(0)], [F(0), F(1)], [-F(1), KAPPA],
    [-F(1), F(0)], [F(0), -F(1)], [F(1), -KAPPA],
]


def _subject():
    try:
        return importlib.import_module("check_six_facet_meta_coordinate_gate")
    except ModuleNotFoundError:
        return None


def _vertices(normals, offsets):
    vertices = []
    for first, second in combinations(range(len(normals)), 2):
        a, b = normals[first]
        c, d = normals[second]
        determinant = a * d - b * c
        if determinant == 0:
            continue
        candidate = [
            (d * offsets[first] - b * offsets[second]) / determinant,
            (-c * offsets[first] + a * offsets[second]) / determinant,
        ]
        if all(
            normal[0] * candidate[0] + normal[1] * candidate[1] <= bound
            for normal, bound in zip(normals, offsets)
        ) and candidate not in vertices:
            vertices.append(candidate)
    return vertices


class SixFacetMetaCoordinateGateTests(unittest.TestCase):
    def test_paired_coordinate_map_is_bijective_for_general_offsets(self):
        """Dropping the independent slant center must not appear invertible."""
        subject = _subject()
        self.assertIsNotNone(subject)
        offsets = [F(4, 3), F(3, 2), F(37, 60), F(2, 3), F(5, 2), F(83, 60)]
        coordinates = subject.paired_coordinates(offsets)
        self.assertEqual(coordinates, {
            "c_p": F(1, 3), "c_v": F(-1, 2), "c_q": F(23, 60),
            "r_p": F(1), "r_v": F(2), "r_q": F(1),
        })
        self.assertEqual(subject.offsets_from_paired(coordinates), offsets)
        self.assertEqual(subject.skew(coordinates), F(0))

    def test_actual_measurement_creates_nonzero_skew_inside_configuration(self):
        """A five-coordinate symmetric family must fail on a legal one-sided measurement cut."""
        subject = _subject()
        source = [F(3, 200)] * 6
        center, halfwidth = F(-23, 4000), F(1, 50)
        posterior = subject.measurement_intersection_offsets(source, center, halfwidth)
        expected = [F(57, 4000)] + [F(3, 200)] * 5
        self.assertEqual(posterior, expected)
        self.assertEqual(subject.skew(subject.paired_coordinates(source)), F(0))
        self.assertEqual(subject.skew(subject.paired_coordinates(posterior)), F(3, 8000))

        augmented_normals = NORMALS + [[F(1), F(0)], [-F(1), F(0)]]
        augmented_offsets = source + [center + halfwidth, -center + halfwidth]
        vertices = _vertices(augmented_normals, augmented_offsets)
        independent_supports = [
            max(normal[0] * vertex[0] + normal[1] * vertex[1] for vertex in vertices)
            for normal in NORMALS
        ]
        self.assertEqual(independent_supports, expected)
        self.assertTrue(all(
            any(normal[0] * vertex[0] + normal[1] * vertex[1] == bound
                for vertex in vertices)
            for normal, bound in zip(NORMALS, expected)
        ))

        template = importlib.import_module("check_six_facet_measurement_gate").six_facet_template()
        margins = [sum(a * b for a, b in zip(row, posterior)) for row in template["G"]]
        self.assertLess(max(margins), F(0))
        self.assertEqual(max(margins), F(-3, 4000))

    def test_invertible_reparameterization_preserves_extreme_candidate_count(self):
        """A coordinate rename alone must not claim fewer H/Omega vertices."""
        subject = _subject()
        base = [F(3, 200)] * 6
        vertices = [base] + [
            [value + (F(1, 10000) if index == axis else F(0))
             for index, value in enumerate(base)]
            for axis in range(6)
        ]
        mapped = subject.transform_parameter_vertices(vertices)
        self.assertEqual(len(mapped), 7)
        self.assertEqual(len({tuple(vertex) for vertex in mapped}), 7)
        self.assertEqual(
            [subject.offsets_from_paired(subject.vector_to_paired(vertex)) for vertex in mapped],
            vertices,
        )

    def test_run_stops_before_meta_polytope_or_control_claims(self):
        """The representation gate is not an H/Omega or controller theorem."""
        result = _subject().run()
        self.assertEqual(
            result["evidence_level"],
            "exact_six_facet_meta_coordinate_nonclosure_certificate",
        )
        self.assertTrue(result["five_coordinate_family_rejected"])
        self.assertTrue(result["six_coordinate_map_invertible"])
        self.assertTrue(result["same_polytope_extreme_count_preserved"])
        self.assertFalse(result["bounded_meta_polytope_selected"])
        self.assertFalse(result["complete_H_Omega_certified"])
        self.assertFalse(result["graph_invariant_information_ensemble_certified"])
        self.assertFalse(result["mpc_recursive_feasibility_certified"])
        self.assertFalse(result["full_six_state_guarantee"])

    def test_cli_artifact_is_hash_bound_and_reproducible(self):
        """The archived gate must change whenever its proof sources change."""
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "exact_checks.json"
            completed = subprocess.run(
                [sys.executable, str(ROOT / "verification/check_six_facet_meta_coordinate_gate.py"),
                 "--output", str(output)],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            generated = json.loads(output.read_text())
            archived = json.loads((
                ROOT / "results/theory_six_facet_meta_coordinate_gate_20261027/exact_checks.json"
            ).read_text())
            self.assertEqual(generated, archived)
            for name, digest in generated["source_sha256"].items():
                self.assertEqual(
                    digest,
                    hashlib.sha256((ROOT / name).read_bytes()).hexdigest(),
                )


if __name__ == "__main__":
    unittest.main()
