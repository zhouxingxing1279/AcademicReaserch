#!/usr/bin/env python3
"""Admission gate for the augmented ancillary invariant-set problem.

This checker does not solve an invariant-set problem.  It prevents a solver
from being run until the partial-information quantifiers, policy interface,
nominal domain, dropout graph, coupled disturbance graph, and nonempty
initialization slice are all explicit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OBLIGATIONS = [
    "invariance_semantics_and_quantifier_order",
    "causal_partial_information_policy",
    "nominal_state_domain",
    "dropout_mode_graph_and_input_timing",
    "shared_actual_thrust_disturbance_graph",
    "nonempty_initialization_slice",
]
EXPECTED_QUANTIFIERS = [
    "forall_current_mode_and_observation",
    "exists_causal_control",
    "forall_hidden_estimation_errors_successor_edges_and_primitives",
]
EXPECTED_EDGES = (
    [[j, j + 1, "miss"] for j in range(14)]
    + [[4, 0, "success"], [9, 0, "success"], [14, 0, "success"]]
)
REQUIRED_OBSERVATIONS = {"d", "mode", "z", "nominal_input"}
HIDDEN_OR_FUTURE_INFORMATION = {
    "eta", "true_state", "residual", "primitive", "successor_edge",
    "future_measurement",
}


def _bounded_nominal_domain(domain, plant_domain):
    if not isinstance(domain, dict):
        return False
    lower, upper = domain.get("lower"), domain.get("upper")
    if not isinstance(lower, list) or not isinstance(upper, list):
        return False
    if len(lower) != 6 or len(upper) != 6:
        return False
    if not all(lo < hi for lo, hi in zip(lower, upper)):
        return False
    plant_lower = plant_domain.get("state_lower", [])
    plant_upper = plant_domain.get("state_upper", [])
    return (
        len(plant_lower) == len(plant_upper) == 6
        and all(plo <= lo < hi <= phi for plo, lo, hi, phi in
                zip(plant_lower, lower, upper, plant_upper))
    )


def _valid_estimator_artifact(initialization, root):
    if not isinstance(initialization, dict):
        return False
    if initialization.get("required_mode") != 0 or initialization.get("d_is_zero") is not True:
        return False
    relative = initialization.get("eta_set_artifact")
    if not isinstance(relative, str):
        return False
    path = root / relative
    if not path.is_file():
        return False
    try:
        artifact = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return False
    return (
        artifact.get("status") == "pass"
        and len(artifact.get("modes", [])) == 15
        and len(artifact.get("edge_invariance_checks", [])) == 17
        and all(row.get("pass") is True for row in artifact["edge_invariance_checks"])
    )


def audit_contract(config, root=None):
    root = Path(root) if root is not None else ROOT
    contract = config.get("mpc", {}).get("ancillary_rci_contract")
    if not isinstance(contract, dict):
        return {
            "status": "blocked",
            "missing_obligations": OBLIGATIONS.copy(),
            "invalid_obligations": [],
            "solver_admissible": False,
            "evidence_level": "problem_not_instantiated",
        }

    missing = []
    invalid = []

    if "semantics" not in contract or "quantifier_order" not in contract:
        missing.append(OBLIGATIONS[0])
    elif not (
        contract["semantics"] == "partial_information_controlled_rci"
        and contract["quantifier_order"] == EXPECTED_QUANTIFIERS
    ):
        invalid.append(OBLIGATIONS[0])

    policy = contract.get("policy")
    if not isinstance(policy, dict):
        missing.append(OBLIGATIONS[1])
    else:
        observes = policy.get("observes")
        policy_class = policy.get("class")
        observes_set = set(observes) if isinstance(observes, list) else set()
        if not (
            isinstance(policy_class, str) and policy_class
            and observes_set == REQUIRED_OBSERVATIONS
            and observes_set.isdisjoint(HIDDEN_OR_FUTURE_INFORMATION)
        ):
            invalid.append(OBLIGATIONS[1])

    if "nominal_state_domain" not in contract:
        missing.append(OBLIGATIONS[2])
    elif not _bounded_nominal_domain(contract["nominal_state_domain"], config.get("domain", {})):
        invalid.append(OBLIGATIONS[2])

    mode_graph = contract.get("mode_graph")
    if not isinstance(mode_graph, dict):
        missing.append(OBLIGATIONS[3])
    elif not (
        mode_graph.get("mode_count") == 15
        and mode_graph.get("edges") == EXPECTED_EDGES
        and mode_graph.get("control_precedes_successor_edge") is True
    ):
        invalid.append(OBLIGATIONS[3])

    disturbance = contract.get("disturbance_graph")
    if not isinstance(disturbance, dict):
        missing.append(OBLIGATIONS[4])
    else:
        eta_ids = disturbance.get("eta_primitive_ids")
        d_ids = disturbance.get("d_primitive_ids")
        eta_set = set(eta_ids) if isinstance(eta_ids, list) else set()
        d_set = set(d_ids) if isinstance(d_ids, list) else set()
        if not (
            disturbance.get("actual_thrust_depends_on_correction") is True
            and disturbance.get("residual_bound_depends_on_actual_thrust") is True
            and eta_set == d_set
            and {"rx", "rz"}.issubset(eta_set)
        ):
            invalid.append(OBLIGATIONS[4])

    if "initialization" not in contract:
        missing.append(OBLIGATIONS[5])
    elif not _valid_estimator_artifact(contract["initialization"], root):
        invalid.append(OBLIGATIONS[5])

    ready = not missing and not invalid
    return {
        "status": "ready" if ready else "blocked",
        "missing_obligations": missing,
        "invalid_obligations": invalid,
        "solver_admissible": ready,
        "evidence_level": (
            "contract_ready_not_an_invariant_set_certificate"
            if ready else "problem_not_instantiated"
        ),
        "semantics": contract.get("semantics"),
        "control_information": sorted(
            contract.get("policy", {}).get("observes", [])
            if isinstance(contract.get("policy"), dict) else []
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "configs/planar_baseline.json")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    config = json.loads(args.config.read_text())
    result = audit_contract(config, root=ROOT)
    sources = [
        "verification/check_augmented_rci_contract.py",
        "verification/test_augmented_rci_contract.py",
        "configs/planar_baseline.json",
        "docs/research/run139_literature_gate.md",
    ]
    result["source_sha256"] = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in sources
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
