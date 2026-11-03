import unittest

import numpy as np

from verification.check_run122_run119_reproduction import reproduce_run119


class Run119ReproductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = reproduce_run119()

    def test_corrected_posterior_supports_match_run114(self):
        expected = np.array(
            [
                2.092531912055255,
                0.320608345499132,
                0.0546690859661024,
                1.902878313682531,
                0.315873912962150,
                0.0547332765315748,
            ]
        )
        np.testing.assert_allclose(
            self.result["posterior_supports"], expected, rtol=0.0, atol=2e-12
        )
        self.assertEqual(self.result["measurement_row_rank"], 2)

    def test_baseline_plan_is_numerically_feasible(self):
        baseline = self.result["baseline"]
        self.assertTrue(baseline["solver_success"])
        self.assertLess(baseline["terminal_inf_norm"], 1e-12)
        self.assertGreaterEqual(baseline["minimum_robust_slack"], -1e-10)
        self.assertGreater(baseline["minimum_state_robust_slack"], 0.095)
        self.assertLess(baseline["minimum_state_robust_slack"], 0.096)
        self.assertAlmostEqual(baseline["minimum_nominal_input"], -0.0149462441, places=8)
        self.assertAlmostEqual(baseline["maximum_nominal_input"], 0.0125663611, places=8)

    def test_measurement_row_deletions_have_opposite_admission_results(self):
        older = self.result["delete_older_packet"]
        newer = self.result["delete_newer_packet"]

        self.assertFalse(older["admitted"])
        self.assertEqual(older["violation_count"], 3)
        self.assertEqual(
            [(v["stage"], v["facet"]) for v in older["violations"]],
            [(0, "upper_input"), (1, "upper_input"), (29, "lower_input")],
        )
        np.testing.assert_allclose(
            [v["excess"] for v in older["violations"]],
            [1.0187340848119564e-4, 1.0605673475865864e-4, 9.036372863556463e-7],
            rtol=0.0,
            atol=2e-12,
        )
        self.assertTrue(newer["admitted"])
        self.assertEqual(newer["violation_count"], 0)
        self.assertLessEqual(newer["maximum_excess"], 1e-8)

    def test_support_solver_tolerances_are_stricter_than_admission_threshold(self):
        settings = self.result["solver_settings"]
        admission_tolerance = self.result["delete_newer_packet"]["violation_tolerance"]
        self.assertEqual(settings["highs_method"], "highs-ds")
        self.assertLess(settings["primal_feasibility_tolerance"], admission_tolerance)
        self.assertLess(settings["dual_feasibility_tolerance"], admission_tolerance)


if __name__ == "__main__":
    unittest.main()
