import unittest
from fractions import Fraction as F


class VerticalCausalPredecessorTests(unittest.TestCase):
    def test_exact_polygon_reduction_removes_corner_touching_redundancy(self):
        """A redundant diagonal must not survive as a fake polygon facet."""
        from check_vertical_causal_predecessor import ExactPolygon

        polygon = ExactPolygon.from_inequalities([
            (F(1), F(0), F(1)),
            (F(-1), F(0), F(1)),
            (F(0), F(1), F(1)),
            (F(0), F(-1), F(1)),
            (F(1), F(1), F(2)),
        ])

        self.assertFalse(polygon.is_empty)
        self.assertEqual(len(polygon.facets), 4)
        self.assertEqual(
            set(polygon.vertices),
            {(F(-1), F(-1)), (F(-1), F(1)), (F(1), F(-1)), (F(1), F(1))},
        )

    def test_branch_predecessor_eliminates_one_shared_input_not_one_per_edge(self):
        """Splitting the input by successor edge would incorrectly retain the source box."""
        from check_vertical_causal_predecessor import ExactPolygon, robust_predecessor

        source = ExactPolygon.box(F(1), F(1))
        lower_target = ExactPolygon.from_inequalities([
            (F(1), F(0), F(1)),
            (F(-1), F(0), F(1)),
            (F(0), F(1), F(1)),
            (F(0), F(-1), F(-1, 2)),
        ])
        upper_target = ExactPolygon.from_inequalities([
            (F(1), F(0), F(1)),
            (F(-1), F(0), F(1)),
            (F(0), F(1), F(-1, 2)),
            (F(0), F(-1), F(1)),
        ])
        zero = ((F(0), F(0)), (F(0), F(0)))
        input_map = (F(0), F(1))
        lower_edge = {
            "A": zero,
            "B": input_map,
            "target": lower_target,
            "disturbance_direction": (F(0), F(0)),
            "disturbance_halfwidth": F(0),
        }
        upper_edge = {**lower_edge, "target": upper_target}

        self.assertFalse(
            robust_predecessor(source, [lower_edge], (F(-1), F(1))).is_empty
        )
        self.assertFalse(
            robust_predecessor(source, [upper_edge], (F(-1), F(1))).is_empty
        )
        self.assertTrue(
            robust_predecessor(source, [lower_edge, upper_edge], (F(-1), F(1))).is_empty
        )

    def test_mode_four_hidden_support_is_bound_from_run136_zonotope(self):
        """Replacing the estimator fiber by a hand-entered box must be detectable."""
        from check_vertical_causal_predecessor import vertical_problem_data

        problem = vertical_problem_data()
        self.assertEqual(len(problem["q_halfwidths"]), 15)
        self.assertEqual(problem["q_halfwidths"][4], F(1004143, 7200000))
        self.assertEqual(problem["input_bounds"], (F(-572143, 160000), F(572143, 160000)))

    def test_run141_negative_control_is_rejected_by_causal_robustification(self):
        """A solver that lets the correction depend on hidden q would retain d=0."""
        from check_vertical_causal_predecessor import run141_negative_control

        result = run141_negative_control()
        self.assertTrue(result["full_state_hidden_policy_feasible"])
        self.assertFalse(result["causal_product_fiber_contains_origin"])
        self.assertEqual(result["required_hidden_policy_extreme"], F(108143, 32000))

    def test_first_mode_iteration_groups_unknown_successors_before_projection(self):
        """Mode 4/9 must have two edge constraints in one predecessor call."""
        from check_vertical_causal_predecessor import iterate_vertical_product_fiber

        result = iterate_vertical_product_fiber(max_iterations=1)
        self.assertEqual(result["iterations"], 1)
        self.assertEqual(len(result["sets"]), 15)
        self.assertEqual(result["outgoing_edge_counts"][4], 2)
        self.assertEqual(result["outgoing_edge_counts"][9], 2)
        self.assertEqual(result["outgoing_edge_counts"][14], 1)
        self.assertTrue(all(not result["sets"][mode].is_empty for mode in range(14)))
        self.assertTrue(result["sets"][14].is_empty)
        self.assertTrue(result["sets"][0].contains((F(0), F(0))))

    def test_finite_predecessor_prefix_is_not_mislabeled_as_rci(self):
        """A one-step descending outer sequence is not an invariance certificate."""
        from check_vertical_causal_predecessor import iterate_vertical_product_fiber

        result = iterate_vertical_product_fiber(max_iterations=1)
        self.assertFalse(result["fixed_point"])
        self.assertFalse(result["is_rci_certificate"])
        self.assertEqual(
            result["evidence_level"],
            "finite_outer_predecessor_prefix_not_an_rci_certificate",
        )

    def test_mode14_success_has_an_exact_product_fiber_width_obstruction(self):
        """No shared input can shrink hidden-fiber spread into mode-zero velocity room."""
        from check_vertical_causal_predecessor import mode14_product_fiber_obstruction

        obstruction = mode14_product_fiber_obstruction()
        self.assertEqual(obstruction["success_velocity_spread"], F(72816441, 32000000))
        self.assertEqual(obstruction["largest_mode_zero_velocity_halfwidth"], F(61142137, 36000000))
        self.assertEqual(obstruction["strict_excess"], F(166210873, 288000000))
        self.assertGreater(obstruction["strict_excess"], 0)
        self.assertTrue(obstruction["mode14_predecessor_is_empty"])
        self.assertTrue(obstruction["required_initialization_is_impossible"])

    def test_final_claim_is_limited_to_the_product_fiber_candidate_class(self):
        """The mode-14 obstruction must not be promoted to general RCI nonexistence."""
        from check_vertical_causal_predecessor import run

        result = run()
        self.assertEqual(result["status"], "pass")
        self.assertEqual(
            result["claim"],
            "no_nonempty_required_product_fiber_rci_multiset",
        )
        self.assertEqual(
            result["evidence_level"],
            "exact_nonexistence_for_product_fiber_candidate_class",
        )
        self.assertFalse(result["general_output_feedback_rci_nonexistence_proved"])
        self.assertIn("joint_eta_d_information_set_remains_open", result["limitations"])


if __name__ == "__main__":
    unittest.main()
