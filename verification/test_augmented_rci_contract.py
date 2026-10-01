import copy
import json
import unittest
from pathlib import Path

from check_augmented_rci_contract import audit_contract


ROOT = Path(__file__).resolve().parents[1]


def complete_contract_fixture():
    config = json.loads((ROOT / "configs/planar_baseline.json").read_text())
    config["mpc"]["ancillary_rci_contract"] = {
        "semantics": "partial_information_controlled_rci",
        "quantifier_order": [
            "forall_current_mode_and_observation",
            "exists_causal_control",
            "forall_hidden_estimation_errors_successor_edges_and_primitives",
        ],
        "policy": {
            "class": "mode_indexed_observation_vertex_policy",
            "observes": ["d", "mode", "z", "nominal_input"],
        },
        "nominal_state_domain": {
            "lower": [-1, 1.5, -1, -1, -0.1, -0.5],
            "upper": [1, 2.5, 1, 1, 0.1, 0.5],
        },
        "mode_graph": {
            "mode_count": 15,
            "edges": [[j, j + 1, "miss"] for j in range(14)]
            + [[4, 0, "success"], [9, 0, "success"], [14, 0, "success"]],
            "control_precedes_successor_edge": True,
        },
        "disturbance_graph": {
            "actual_thrust_depends_on_correction": True,
            "residual_bound_depends_on_actual_thrust": True,
            "eta_primitive_ids": ["rx", "rz", "n_px", "n_pz", "n_phi", "n_omega"],
            "d_primitive_ids": ["rx", "rz", "n_px", "n_pz", "n_phi", "n_omega"],
        },
        "initialization": {
            "required_mode": 0,
            "eta_set_artifact": "results/theory_cycle_lifted_zonotope_20260929/exact_checks.json",
            "d_is_zero": True,
        },
    }
    return config


class AugmentedRciContractTests(unittest.TestCase):
    def test_current_repository_config_is_blocked_by_six_missing_obligations(self):
        config = json.loads((ROOT / "configs/planar_baseline.json").read_text())
        report = audit_contract(config, root=ROOT)
        self.assertEqual(report["status"], "blocked")
        self.assertEqual(
            report["missing_obligations"],
            [
                "invariance_semantics_and_quantifier_order",
                "causal_partial_information_policy",
                "nominal_state_domain",
                "dropout_mode_graph_and_input_timing",
                "shared_actual_thrust_disturbance_graph",
                "nonempty_initialization_slice",
            ],
        )
        self.assertFalse(report["solver_admissible"])

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
        graph["d_primitive_ids"].remove("rz")
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


if __name__ == "__main__":
    unittest.main()
