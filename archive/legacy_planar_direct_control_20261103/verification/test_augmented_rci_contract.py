import copy
import json
import unittest
from pathlib import Path

from check_augmented_rci_contract import audit_contract


ROOT = Path(__file__).resolve().parents[1]


def complete_contract_fixture():
    return json.loads((ROOT / "configs/planar_baseline.json").read_text())


class AugmentedRciContractTests(unittest.TestCase):
    def test_current_repository_config_is_ready_for_synthesis_but_is_not_a_certificate(self):
        config = json.loads((ROOT / "configs/planar_baseline.json").read_text())
        report = audit_contract(config, root=ROOT)
        self.assertEqual(report["status"], "ready")
        self.assertEqual(report["missing_obligations"], [])
        self.assertEqual(report["invalid_obligations"], [])
        self.assertTrue(report["solver_admissible"])
        self.assertEqual(
            report["evidence_level"],
            "contract_ready_not_an_invariant_set_certificate",
        )

    def test_complete_causal_contract_is_ready(self):
        report = audit_contract(complete_contract_fixture(), root=ROOT)
        self.assertEqual(report["status"], "ready")
        self.assertEqual(report["missing_obligations"], [])
        self.assertTrue(report["solver_admissible"])

    def test_policy_cannot_observe_hidden_error_or_realized_disturbance(self):
        config = complete_contract_fixture()
        config["mpc"]["ancillary_rci_contract"]["policy"]["observes"] += ["eta", "residual"]
        report = audit_contract(config, root=ROOT)
        self.assertEqual(report["status"], "blocked")
        self.assertIn("causal_partial_information_policy", report["invalid_obligations"])
        self.assertFalse(report["solver_admissible"])

    def test_policy_class_and_one_control_per_observation_fiber_are_fail_closed(self):
        for field, value in (
            ("class", "arbitrary_noncausal_policy"),
            ("same_control_for_entire_observation_fiber", False),
        ):
            with self.subTest(field=field):
                config = complete_contract_fixture()
                config["mpc"]["ancillary_rci_contract"]["policy"][field] = value
                report = audit_contract(config, root=ROOT)
                self.assertEqual(report["status"], "blocked")
                self.assertIn("causal_partial_information_policy", report["invalid_obligations"])

    def test_control_must_be_chosen_before_unknown_successor_edge(self):
        config = complete_contract_fixture()
        contract = config["mpc"]["ancillary_rci_contract"]
        contract["quantifier_order"] = [
            "forall_current_mode_and_observation",
            "forall_successor_edge",
            "exists_causal_control",
            "forall_hidden_estimation_errors_and_primitives",
        ]
        report = audit_contract(config, root=ROOT)
        self.assertEqual(report["status"], "blocked")
        self.assertIn("invariance_semantics_and_quantifier_order", report["invalid_obligations"])

    def test_shared_primitives_must_reach_both_error_coordinates(self):
        config = complete_contract_fixture()
        graph = config["mpc"]["ancillary_rci_contract"]["disturbance_graph"]
        graph["edge_primitive_indices"]["success"]["eta"].remove(1)
        report = audit_contract(config, root=ROOT)
        self.assertEqual(report["status"], "blocked")
        self.assertIn("shared_actual_thrust_disturbance_graph", report["invalid_obligations"])

    def test_shared_vector_and_edge_incidence_are_fail_closed(self):
        mutations = (
            lambda graph: graph["primitive_vector"].update(id="independent_copies"),
            lambda graph: graph["primitive_vector"]["order"].reverse(),
            lambda graph: graph["edge_primitive_indices"]["miss"]["d"].append(0),
            lambda graph: graph["edge_primitive_indices"]["success"]["observer"].remove(2),
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                config = complete_contract_fixture()
                graph = config["mpc"]["ancillary_rci_contract"]["disturbance_graph"]
                mutate(graph)
                report = audit_contract(config, root=ROOT)
                self.assertEqual(report["status"], "blocked")
                self.assertIn("shared_actual_thrust_disturbance_graph", report["invalid_obligations"])

    def test_d_update_must_be_the_shared_difference_not_an_independent_disturbance_copy(self):
        config = complete_contract_fixture()
        graph = config["mpc"]["ancillary_rci_contract"]["disturbance_graph"]
        graph["coupled_update"] = {
            "tracking_error_update": "equation_71_1",
            "estimation_error_update": "run136_edge_map",
            "d_update": "independent_disturbance_copy",
        }
        report = audit_contract(config, root=ROOT)
        self.assertEqual(report["status"], "blocked")
        self.assertIn("shared_actual_thrust_disturbance_graph", report["invalid_obligations"])

    def test_physical_residual_width_must_keep_the_same_actual_thrust(self):
        config = complete_contract_fixture()
        graph = config["mpc"]["ancillary_rci_contract"]["disturbance_graph"]
        graph["physical_residual_halfwidth"]["r_x"] = "global_constant"
        report = audit_contract(config, root=ROOT)
        self.assertEqual(report["status"], "blocked")
        self.assertIn("shared_actual_thrust_disturbance_graph", report["invalid_obligations"])

    def test_initialization_artifact_must_exist(self):
        config = complete_contract_fixture()
        init = config["mpc"]["ancillary_rci_contract"]["initialization"]
        init["eta_set_artifact"] = "results/does-not-exist.json"
        report = audit_contract(config, root=ROOT)
        self.assertEqual(report["status"], "blocked")
        self.assertIn("nonempty_initialization_slice", report["invalid_obligations"])

    def test_candidate_safety_constraints_are_fail_closed(self):
        contract = complete_contract_fixture()["mpc"]["ancillary_rci_contract"]
        mutations = (
            ("true_state_relation", "x = z + eta"),
            ("true_state_must_remain_in_source_domain", False),
            ("actual_input_relation", "actual_input = correction"),
            ("actual_input_must_remain_in_actuator_box", False),
            ("eta_projection_must_lie_in_run136_mode_set", False),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                config = complete_contract_fixture()
                config["mpc"]["ancillary_rci_contract"]["candidate_constraints"][field] = value
                report = audit_contract(config, root=ROOT)
                self.assertEqual(report["status"], "blocked")
                self.assertIn("candidate_source_and_input_constraints", report["invalid_obligations"])

    def test_nominal_plus_correction_allocation_must_fit_actuator_box(self):
        config = complete_contract_fixture()
        config["mpc"]["ancillary_correction_upper"][0] += 1
        report = audit_contract(config, root=ROOT)
        self.assertEqual(report["status"], "blocked")
        self.assertIn("candidate_source_and_input_constraints", report["invalid_obligations"])

    def test_input_allocation_boxes_must_be_finite_and_ordered(self):
        mutations = (
            lambda config: config["mpc"].update(
                nominal_input_lower=[12, 0], nominal_input_upper=[11, 0]
            ),
            lambda config: config["mpc"].update(
                ancillary_correction_lower=[1, -0.08],
                ancillary_correction_upper=[-1, 0.08],
            ),
            lambda config: config["domain"].update(
                input_lower=[4.905, 0.08], input_upper=[14.715, -0.08]
            ),
            lambda config: config["mpc"]["nominal_input_upper"].__setitem__(0, float("inf")),
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                config = complete_contract_fixture()
                mutate(config)
                report = audit_contract(config, root=ROOT)
                self.assertEqual(report["status"], "blocked")
                self.assertIn("candidate_source_and_input_constraints", report["invalid_obligations"])


if __name__ == "__main__":
    unittest.main()
