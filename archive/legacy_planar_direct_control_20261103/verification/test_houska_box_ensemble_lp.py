import importlib
from fractions import Fraction as F
import hashlib
import json
import numpy as np
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def _subject():
    try:
        return importlib.import_module("check_houska_box_ensemble_lp")
    except ModuleNotFoundError:
        return None


def _matvec(matrix, vector):
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]


class HouskaBoxTemplateTests(unittest.TestCase):
    def test_box_vertex_maps_reconstruct_all_four_corners(self):
        """A sign or column-order error in Lambda must change a physical corner."""
        subject = _subject()
        build = getattr(subject, "box_template", None)
        self.assertTrue(callable(build))
        template = build()
        y = [F(3), F(5), F(1), F(2)]
        vertices = [_matvec(vertex_map, y) for vertex_map in template["Lambda"]]
        self.assertEqual(vertices, [
            [F(3), F(5)],
            [F(3), F(-2)],
            [F(-1), F(5)],
            [F(-1), F(-2)],
        ])
        for vertex in vertices:
            self.assertTrue(all(lhs <= rhs for lhs, rhs in zip(
                _matvec(template["Y"], vertex), y
            )))

    def test_configuration_cone_accepts_nonempty_and_rejects_crossed_boxes(self):
        """Dropping either nonemptiness row would admit a crossed interval."""
        subject = _subject()
        build = getattr(subject, "box_template", None)
        self.assertTrue(callable(build))
        G = build()["G"]
        self.assertTrue(all(value <= 0 for value in _matvec(G, [F(3), F(5), F(1), F(2)])))
        self.assertGreater(_matvec(G, [F(-2), F(5), F(1), F(2)])[0], 0)
        self.assertGreater(_matvec(G, [F(3), F(-3), F(1), F(2)])[1], 0)

    def test_meta_vertex_maps_have_sixteen_vertices_and_four_extreme_sets(self):
        """Treating zero-radius meta vertices as extreme information sets changes the policy budget."""
        subject = _subject()
        build = getattr(subject, "meta_template", None)
        self.assertTrue(callable(build))
        template = build()
        z = [F(2), F(4), F(1), F(6), F(2), F(3)]
        vertices = [_matvec(vertex_map, z) for vertex_map in template["Omega"]]
        self.assertEqual(len(vertices), 16)
        extreme = [vertices[index] for index in template["extreme_indices"]]
        self.assertEqual(extreme, [
            [F(6), F(9), F(-2), F(-3)],
            [F(6), F(1), F(-2), F(5)],
            [F(1), F(9), F(3), F(-3)],
            [F(1), F(1), F(3), F(5)],
        ])
        radii = [[(y[0] + y[2]) / 2, (y[1] + y[3]) / 2] for y in extreme]
        self.assertEqual(radii, [[F(2), F(3)]] * 4)

    def test_first_meta_row_is_position_radius_measurement_coordinate(self):
        """Using position diameter instead of radius would double the measurement cap."""
        subject = _subject()
        build = getattr(subject, "meta_template", None)
        self.assertTrue(callable(build))
        template = build()
        self.assertEqual(template["Z"][0], [F(1, 2), F(0), F(1, 2), F(0)])
        y = [F(6), F(9), F(-2), F(-3)]
        meta_coordinate = _matvec(template["Z"], y)
        self.assertEqual(meta_coordinate, [F(2), F(4), F(-4), F(6), F(-6), F(3)])
        self.assertTrue(all(lhs <= rhs for lhs, rhs in zip(
            meta_coordinate, [F(2), F(4), F(1), F(6), F(2), F(3)]
        )))
        self.assertTrue(all(value <= 0 for value in _matvec(
            template["H"], [F(2), F(4), F(1), F(6), F(2), F(3)]
        )))


class HouskaGraphLPTests(unittest.TestCase):
    def test_success_update_preserves_predicted_position_endpoints(self):
        """Shrinking radius without shifting centers can discard a legal boundary measurement."""
        subject = _subject()
        model = subject.build_graph_lp()
        success_edge_index = next(
            index for index, edge in enumerate(model["edge_constraints"])
            if edge["source"] == 4 and edge["target"] == 0 and edge["label"] == "success"
        )
        predicted = model["predicted_ensembles"][4]
        posterior = model["success_posterior_ensembles"][success_edge_index]
        values = {index: F(0) for index in predicted + posterior}
        values[predicted[0]] = F(1)
        values[predicted[5]] = F(1)
        values[posterior[0]] = F(1, 50)
        values[posterior[5]] = F(1)
        success_rows = [
            row for row in model["_lp"].rows
            if row["name"].startswith("success_") and "[4->0" in row["name"]
            and not row["name"].startswith("success_to_target")
        ]
        violations = [
            sum(coefficient * values.get(variable, F(0))
                for variable, coefficient in row["coefficients"].items()) - row["rhs"]
            for row in success_rows
        ]
        self.assertEqual(max(violations), F(49, 50))

        values[posterior[1]] = F(49, 50)
        values[posterior[2]] = F(49, 50)
        repaired = [
            sum(coefficient * values.get(variable, F(0))
                for variable, coefficient in row["coefficients"].items()) - row["rhs"]
            for row in success_rows
        ]
        self.assertLessEqual(max(repaired), F(0))

    def test_graph_lp_owns_controls_by_source_not_by_edge(self):
        """Allocating edge-specific controls would make modes 4 and 9 noncausal."""
        subject = _subject()
        build = getattr(subject, "build_graph_lp", None)
        self.assertTrue(callable(build))
        model = build()
        self.assertEqual(len(model["source_controls"]), 15)
        self.assertTrue(all(len(block) == 4 for block in model["source_controls"].values()))
        self.assertEqual(len(model["predicted_ensembles"]), 15)
        self.assertNotIn("edge_controls", model)
        by_source = {}
        for edge in model["edge_constraints"]:
            by_source.setdefault(edge["source"], []).append(edge)
            self.assertEqual(edge["measurement_stage"], "after_transition")
        for mode in (4, 9):
            self.assertEqual(len(by_source[mode]), 2)
            self.assertEqual(
                {tuple(edge["control_block"]) for edge in by_source[mode]},
                {tuple(model["source_controls"][mode])},
            )

    def test_graph_lp_has_all_fifteen_sources_and_seventeen_labeled_edges(self):
        """Dropping a miss edge or moving success before transition weakens invariance."""
        subject = _subject()
        build = getattr(subject, "build_graph_lp", None)
        self.assertTrue(callable(build))
        model = build()
        self.assertEqual(model["mode_count"], 15)
        self.assertEqual(len(model["edge_constraints"]), 17)
        self.assertEqual(
            [edge["label"] for edge in model["edge_constraints"]].count("miss"), 14
        )
        self.assertEqual(
            [edge["label"] for edge in model["edge_constraints"]].count("success"), 3
        )
        self.assertEqual(len(model["success_posterior_ensembles"]), 3)
        self.assertGreater(model["constraint_count"], 0)

    def test_solver_infeasibility_has_an_exact_farkas_cycle_certificate(self):
        """A numerical infeasible status alone must not reject the box template."""
        subject = _subject()
        solve = getattr(subject, "solve_graph_lp", None)
        self.assertTrue(callable(solve))
        result = solve()
        self.assertEqual(result["solver_status"], "infeasible")
        self.assertFalse(result["exact_primal_feasible"])
        certificate = result["exact_farkas_certificate"]
        self.assertEqual(certificate["cycle"], [0, 1, 2, 3, 4, 0])
        self.assertEqual(certificate["per_edge_velocity_radius_growth"], F(572143, 8000000))
        self.assertEqual(certificate["aggregate_coefficients"], {})
        self.assertEqual(certificate["aggregate_rhs"], F(-572143, 800000))
        self.assertTrue(certificate["contradiction"])
        names = [entry["row"] for entry in certificate["row_multipliers"]]
        self.assertEqual(len(names), 21)
        self.assertEqual(len(names), len(set(names)))
        self.assertTrue(all(entry["multiplier"] >= 0 for entry in certificate["row_multipliers"]))
        model = subject.build_graph_lp()
        actual_rows = {row["name"]: row for row in model["_lp"].rows}
        self.assertTrue(set(names).issubset(actual_rows))
        aggregate = {}
        rhs = F(0)
        for entry in certificate["row_multipliers"]:
            row = actual_rows[entry["row"]]
            multiplier = entry["multiplier"]
            rhs += multiplier * row["rhs"]
            for variable, coefficient in row["coefficients"].items():
                aggregate[variable] = aggregate.get(variable, F(0)) + multiplier * coefficient
        self.assertFalse({variable: value for variable, value in aggregate.items() if value})
        self.assertEqual(rhs, F(-572143, 800000))
        self.assertEqual(
            result["evidence_level"],
            "exact_axis_aligned_box_information_ensemble_infeasibility_certificate",
        )
        self.assertFalse(result["invariant_information_ensemble_certified"])
        self.assertFalse(result["exact_optimality_certified"])
        self.assertFalse(result["mpc_recursive_feasibility_certified"])

    def test_cli_artifact_is_hash_bound_and_reproducible(self):
        """An edited checker or stale archived candidate must be detected on replay."""
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "exact_checks.json"
            completed = subprocess.run(
                [sys.executable, str(ROOT / "verification/check_houska_box_ensemble_lp.py"),
                 "--output", str(output)],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertTrue(output.exists(), "checker did not create the requested artifact")
            generated = json.loads(output.read_text())
            self.assertEqual(
                generated["claim"],
                "causal_axis_aligned_box_graph_lp_is_exactly_infeasible",
            )
            self.assertFalse(generated["exact_primal_feasible"])
            archived = json.loads((
                ROOT / "results/theory_houska_box_ensemble_lp_20261026/exact_checks.json"
            ).read_text())
            self.assertEqual(generated, archived)
            for name, digest in generated["source_sha256"].items():
                self.assertEqual(digest, hashlib.sha256((ROOT / name).read_bytes()).hexdigest())

    def test_numerical_dual_diagnostics_use_scipy_marginal_sign(self):
        """Using c+A.T@marginal reports a false residual on a known optimal LP."""
        subject = _subject()
        diagnostics = getattr(subject, "numerical_dual_diagnostics", None)
        self.assertTrue(callable(diagnostics))
        result = diagnostics(
            np.array([1.0]),
            np.array([[-1.0]]),
            np.array([-1.0]),
            np.array([1.0]),
            np.array([-1.0]),
        )
        self.assertEqual(result["stationarity_residual"], 0.0)
        self.assertEqual(result["duality_gap"], 0.0)
        self.assertEqual(result["dual_sign_violation"], 0.0)


if __name__ == "__main__":
    unittest.main()
