import importlib
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


KAPPA = F(1, 10)
ROOT = Path(__file__).resolve().parents[1]
Y_LITERAL = [
    [F(1), F(0)],
    [F(0), F(1)],
    [F(-1), KAPPA],
    [F(-1), F(0)],
    [F(0), F(-1)],
    [F(1), -KAPPA],
]


def _subject():
    try:
        return importlib.import_module("check_six_facet_measurement_gate")
    except ModuleNotFoundError:
        return None


def _matmul(left, right):
    return [[
        sum(left[row][inner] * right[inner][column]
            for inner in range(len(right)))
        for column in range(len(right[0]))
    ] for row in range(len(left))]


def _pair_vertex(first, second, bounds):
    a, b = Y_LITERAL[first]
    c, d = Y_LITERAL[second]
    determinant = a * d - b * c
    return [
        (d * bounds[first] - b * bounds[second]) / determinant,
        (-c * bounds[first] + a * bounds[second]) / determinant,
    ]


def _enumerate_vertices(bounds):
    vertices = []
    for first in range(6):
        for second in range(first + 1, 6):
            a, b = Y_LITERAL[first]
            c, d = Y_LITERAL[second]
            if a * d - b * c == 0:
                continue
            candidate = _pair_vertex(first, second, bounds)
            if all(
                normal[0] * candidate[0] + normal[1] * candidate[1] <= bound
                for normal, bound in zip(Y_LITERAL, bounds)
            ):
                vertices.append(candidate)
    return vertices


class SixFacetMeasurementGateTests(unittest.TestCase):
    def test_template_has_cyclic_normals_and_all_configuration_rows(self):
        """Changing normal order or dropping a containment row must break the template."""
        subject = _subject()
        self.assertIsNotNone(subject)
        template = subject.six_facet_template()
        self.assertEqual(template["facet_order"], ["+p", "+v", "-q", "-p", "-v", "+q"])
        self.assertEqual(template["Y"], Y_LITERAL)
        identity = [[F(row == column) for column in range(6)] for row in range(6)]
        expected_rows = []
        for vertex_map in template["Lambda"]:
            product = _matmul(Y_LITERAL, vertex_map)
            expected_rows.extend([
                [product[row][column] - identity[row][column] for column in range(6)]
                for row in range(6)
                if any(product[row][column] - identity[row][column] for column in range(6))
            ])
        self.assertEqual(len(expected_rows), 24)
        self.assertEqual(template["G"], expected_rows)

    def test_reference_hexagon_vertices_are_exact_and_inside_all_facets(self):
        """Wrong adjacent-pair inverses must fail against hand-derived vertices."""
        subject = _subject()
        template = subject.six_facet_template()
        offsets = [F(1)] * 6
        vertices = [
            [sum(row[column] * offsets[column] for column in range(6)) for row in vertex_map]
            for vertex_map in template["Lambda"]
        ]
        self.assertEqual(vertices, [
            [F(1), F(1)], [F(-9, 10), F(1)], [F(-1), F(0)],
            [F(-1), F(-1)], [F(9, 10), F(-1)], [F(1), F(0)],
        ])
        for vertex in vertices:
            self.assertTrue(all(
                normal[0] * vertex[0] + normal[1] * vertex[1] <= F(1)
                for normal in Y_LITERAL
            ))

    def test_canonical_measurement_support_matches_independent_vertex_enumeration(self):
        """Using raw slant support must fail when velocity facets make it redundant."""
        subject = _subject()
        cap, velocity, slant = F(1, 50), F(11, 4), F(1)
        actual = subject.canonical_measurement_support(cap, velocity, slant)
        vertices = _enumerate_vertices([cap, velocity, slant, cap, velocity, slant])
        expected = {
            "position": max(vertex[0] for vertex in vertices),
            "velocity": max(vertex[1] for vertex in vertices),
            "slant": max(vertex[0] - KAPPA * vertex[1] for vertex in vertices),
        }
        self.assertEqual(expected, {
            "position": F(1, 50),
            "velocity": F(11, 4),
            "slant": F(59, 200),
        })
        self.assertEqual(actual["tight_supports"], expected)

    def test_strict_witness_is_admissible_before_measurement_and_canonical_after(self):
        """A strict reduction witness outside the prior configuration cone is invalid."""
        subject = _subject()
        result = subject.run()
        witness = result["strict_measurement_witness"]
        self.assertTrue(witness["pre_measurement_configuration_valid"])
        self.assertFalse(witness["raw_post_measurement_configuration_valid"])
        self.assertTrue(witness["canonical_post_measurement_configuration_valid"])
        self.assertEqual(witness["slant_support_before"], F(1))
        self.assertEqual(witness["slant_support_after"], F(59, 200))
        self.assertEqual(witness["strict_slant_reduction"], F(141, 200))

    def test_run_rejects_a_prior_shape_outside_the_configuration_cone(self):
        """Recording an invalid prior is insufficient; the positive gate must not emit."""
        subject = _subject()
        adapter = importlib.import_module("check_houska_vertical_adapter").run()
        adapter["tracking_error_box"]["position_halfwidth"] = F(1, 10)
        with patch.object(subject, "adapter_run", return_value=adapter):
            with self.assertRaisesRegex(AssertionError, "pre-measurement"):
                subject.run()

    def test_evidence_flags_stop_local_support_map_becoming_controller_claim(self):
        """A local exact support identity is not an invariant ensemble or MPC theorem."""
        subject = _subject()
        result = subject.run()
        self.assertEqual(result["evidence_level"], "exact_six_facet_measurement_support_map")
        self.assertTrue(result["active_velocity_facets_can_tighten_slant_support"])
        self.assertFalse(result["graph_invariant_information_ensemble_certified"])
        self.assertFalse(result["input_feasibility_certified"])
        self.assertFalse(result["mpc_recursive_feasibility_certified"])
        self.assertFalse(result["full_six_state_guarantee"])

    def test_cli_artifact_is_hash_bound_and_reproducible(self):
        """A stale archive must fail after checker, test, adapter, config, or design changes."""
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "exact_checks.json"
            completed = subprocess.run(
                [sys.executable, str(ROOT / "verification/check_six_facet_measurement_gate.py"),
                 "--output", str(output)],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            generated = json.loads(output.read_text())
            archived = json.loads((
                ROOT / "results/theory_six_facet_measurement_gate_20261027/exact_checks.json"
            ).read_text())
            self.assertEqual(generated, archived)
            for name, digest in generated["source_sha256"].items():
                self.assertEqual(
                    digest,
                    hashlib.sha256((ROOT / name).read_bytes()).hexdigest(),
                )


if __name__ == "__main__":
    unittest.main()
