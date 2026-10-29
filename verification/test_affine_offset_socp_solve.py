import json
import hashlib
import unittest
from pathlib import Path

import numpy as np

import check_affine_offset_socp_solve as subject


ROOT = Path(__file__).resolve().parents[1]


class AffineOffsetSocpSolveTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.problem = subject.build_problem()

    def test_locked_layout_and_cone_counts(self):
        layout = self.problem["layout"]
        self.assertEqual(layout.variables, 6514)
        self.assertEqual(sum(type(cone).__name__ == "SecondOrderConeT" for cone in self.problem["cones"]), 6080)
        self.assertEqual(self.problem["A"].shape[1], 6514)

    def test_exact_vertex_maps_reproduce_float_maps(self):
        for float_map, exact_map in zip(self.problem["maps"], self.problem["maps_exact"]):
            rebuilt = np.array([[float(value) for value in row] for row in exact_map])
            np.testing.assert_allclose(float_map, rebuilt, atol=0.0, rtol=0.0)

    def test_archived_report_replays(self):
        archived = json.loads((ROOT / "results/affine_offset_socp_solve_20261029/checks.json").read_text())
        current = subject.build_report(ROOT)
        self.assertEqual(archived["problem"], current["problem"])
        self.assertEqual(archived["solver"]["status"], current["solver"]["status"])
        self.assertEqual(archived["solver"]["iterations"], current["solver"]["iterations"])
        self.assertTrue(archived["dual_infeasibility_ray_audit"]["passes_tolerance_1e_7"])
        self.assertEqual(archived["robustness_solve_no_equilibration"]["status"], "PrimalInfeasible")
        self.assertTrue(archived["robustness_solve_no_equilibration"]["dual_ray_audit"]["passes_tolerance_1e_7"])

    def test_archived_dual_ray_is_an_independent_numerical_certificate(self):
        report = json.loads((ROOT / "results/affine_offset_socp_solve_20261029/checks.json").read_text())
        ray_path = ROOT / report["dual_ray_artifact"]["path"]
        self.assertEqual(hashlib.sha256(ray_path.read_bytes()).hexdigest(), report["dual_ray_artifact"]["sha256"])
        ray = np.load(ray_path, allow_pickle=False)
        audit = subject.audit_dual_ray(self.problem, ray)
        self.assertTrue(audit["passes_tolerance_1e_7"])
        self.assertLess(audit["b_dot_z"], -0.99)
        self.assertLessEqual(audit["stationarity_inf_norm"], 1e-7)


if __name__ == "__main__":
    unittest.main()
