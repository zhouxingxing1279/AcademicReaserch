"""Independent geometry checks and complete-compression-outage safety test."""
import unittest
from unittest.mock import patch
import numpy as np
from scipy.optimize import linprog

import experiments.cong_mpc_validate as experiment


class ValidationChecks(unittest.TestCase):
    def test_polygon_support_matches_independent_lp(self):
        model = experiment.Model("fast")
        S, _, _, plan, _ = experiment.boundary_case(model, 45, 90)
        S = S.predict(model, plan[0])
        y = float(model.C @ np.mean(S.v, axis=0))
        S = S.observe(model, y)
        for method in experiment.METHODS:
            P, count = experiment.compress(S, model, method, 8, np.r_[plan[1:], 0.])
            self.assertLessEqual(len(P.v), 8)
            self.assertTrue(all(P.contains(v) for v in S.v))
            if method == "control":
                self.assertEqual(count, 8)
            for q in model.pool[::4]:
                result = linprog(-q, A_ub=P.H, b_ub=P.b, bounds=[(None, None)]*2, method="highs")
                self.assertTrue(result.success)
                self.assertAlmostEqual(float(P.support(q)), -result.fun, places=7)

    def test_complete_compression_outage_uses_plan_then_terminal(self):
        model = experiment.Model("slow")
        initial = experiment.boundary_case(model, 0, 0)
        oversized = experiment.box(np.full(2, -10.), np.full(2, 10.))
        # Every candidate update is unusable; the original plan must still
        # finish, and the zero-input invariant terminal set must take over.
        with patch.object(experiment, "compress", return_value=(oversized, 0)), patch.object(experiment, "STEPS", model.N + 4):
            rows, case = experiment.run_case(model, 0, 0, 0, "control", 6, 0, initial, [])
        self.assertEqual(case["fallback_steps"], model.N + 3)
        self.assertEqual(case["completed_steps"], model.N + 4)
        self.assertLessEqual(max(r["state_violation"] for r in rows), experiment.TOL)
        self.assertLessEqual(max(r["input_violation"] for r in rows), experiment.TOL)
        self.assertLessEqual(case["max_stored_faces"], 6)

    def test_conditioning_does_not_commute_with_outer_approximation(self):
        diamond = experiment.Polygon(np.array([[1., 0], [0, 1.], [-1., 0], [0, -1.]]))
        square = experiment.box(np.full(2, -1.), np.full(2, 1.))
        q = np.array([1., 1.])
        # A narrow strip avoids a degenerate polygon while preserving the
        # analytic gap: diamond support <= .5005, box support = 1.
        d = diamond.clip(q, .001).clip(-q, .001)
        b = square.clip(q, .001).clip(-q, .001)
        self.assertAlmostEqual(float(d.support([1., 0.])), .5005, places=8)
        self.assertAlmostEqual(float(b.support([1., 0.])), 1., places=8)


if __name__ == "__main__":
    unittest.main()
