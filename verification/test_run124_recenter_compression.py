import importlib
import unittest

import numpy as np


class Run124RecenterCompressionTest(unittest.TestCase):
    def test_stage_admission_does_not_hide_terminal_obstruction(self):
        try:
            module = importlib.import_module(
                "verification.check_run124_recenter_compression"
            )
        except ModuleNotFoundError:
            self.fail("Run124 recenter/compression verifier is not implemented")

        result = module.verify_recenter_compression()

        self.assertEqual(result["compression"]["template_row_count"], 300)
        self.assertIn(
            "maximum_certified_cap_minus_numerical_primal",
            result["compression"],
        )
        self.assertLessEqual(
            max(
                abs(
                    result["compression"][
                        "minimum_certified_cap_minus_numerical_primal"
                    ]
                ),
                abs(
                    result["compression"][
                        "maximum_certified_cap_minus_numerical_primal"
                    ]
                ),
            ),
            1e-7,
        )
        self.assertEqual(
            result["compression"]["outer_inclusion_certificate"],
            "exact-rational weak-duality residual and recenter translation, "
            "rounded outward",
        )
        self.assertIn(
            "minimum_translated_cap_outward_gap", result["compression"]
        )
        self.assertGreaterEqual(
            result["compression"]["minimum_translated_cap_outward_gap"], 0.0
        )
        self.assertGreater(result["recenter"]["scale"], 0.1)
        self.assertGreater(result["recenter"]["initial_shift_inf_norm"], 1e-3)
        self.assertIn("strip_center_residual", result["recenter"])
        self.assertLessEqual(result["recenter"]["posterior_member_violation"], 0.0)
        self.assertLessEqual(
            result["compression"]["maximum_template_minus_numerical_primal"],
            1e-8,
        )
        self.assertLessEqual(
            result["stage_admission"]["maximum_constraint_excess"], 1e-8
        )
        self.assertLessEqual(
            result["stage_admission"]["terminal_nominal_correction_inf_norm"],
            1e-8,
        )
        self.assertEqual(result["stage_admission"]["checked_margin_count"], 300)
        self.assertIn(
            "direct_maximum_constraint_excess", result["stage_admission"]
        )
        self.assertLessEqual(
            result["stage_admission"]["direct_maximum_constraint_excess"],
            1e-8,
        )
        self.assertLessEqual(
            result["stage_admission"]["nominal_dynamics_residual_inf_norm"],
            1e-8,
        )
        self.assertTrue(result["stage_admission"]["admitted"])
        self.assertNotEqual(result["terminal_gate"]["closed_loop_determinant"], 0.0)
        self.assertEqual(
            result["terminal_gate"]["only_consistent_zero_terminal_scale"], 0.0
        )
        self.assertFalse(result["overall_admission"]["admitted"])
        self.assertEqual(
            result["overall_admission"]["blocker"],
            "terminal_mrpi_containment_after_nonzero_recenter",
        )

    def test_dual_residual_cap_is_an_upper_bound_on_known_support(self):
        module = importlib.import_module(
            "verification.check_run124_recenter_compression"
        )

        class OneDimensionalPosterior:
            generators = np.array([[1.0]])

            @staticmethod
            def _inequalities():
                return np.array([[1.0], [-1.0]]), np.array([0.25, 1.0])

        numerical, certified, _exact = module._certified_support_upper(
            OneDimensionalPosterior(), np.array([1.0])
        )
        self.assertAlmostEqual(numerical, 0.25, places=12)
        self.assertGreaterEqual(certified, 0.25)


if __name__ == "__main__":
    unittest.main()
