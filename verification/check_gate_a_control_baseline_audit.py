#!/usr/bin/env python3
"""Audit the repository evidence for the Gate-A ancillary/RCI baseline.

This script is deliberately not a controller synthesizer.  It verifies the
scope of archived certificates and attaches a SHA-256 digest of the checker
that generated each claim, so a negative result cannot silently be promoted
to a broader plant-level impossibility statement.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def _load(root: Path, relative: str) -> dict:
    return json.loads((root / relative).read_text())


def _sha256(root: Path, relative: str) -> str:
    return hashlib.sha256((root / relative).read_bytes()).hexdigest()


def _evidence(root: Path, *, item_id: str, level: str, source: str,
              result: str, establishes: str, excludes: str) -> dict:
    return {
        "id": item_id,
        "level": level,
        "source": source,
        "source_sha256": _sha256(root, source),
        "result": result,
        "establishes": establishes,
        "excludes": excludes,
    }


def audit(root: Path) -> dict:
    cq = _load(root, "results/lpv_common_quadratic_20260924/checks.json")
    torque = _load(root, "results/lpv_torque_rpi_obstruction_20260924/checks.json")
    search = _load(root, "results/vertex_consistent_ancillary_20260924/checks.json")
    authority = _load(root, "results/actuator_authority_scheduled_residual_20260924/checks.json")
    box = _load(root, "results/axis_aligned_rci_obstruction_20260924/checks.json")
    scheduling = _load(root, "results/thrust_scheduling_contract_20260924/checks.json")
    endpoint = _load(root, "results/endpoint_predecessor_reduction_20260924/checks.json")
    farkas = _load(root, "results/cc_19pair_exact_farkas_20260924/checks.json")

    # Fail closed if any archived result no longer says what this audit cites.
    assert cq["min_eig_P"] > 0
    assert min(x["min_eig_P_minus_MtPM"] for x in cq["endpoint_checks"]) > 0
    assert torque["cases"]["semantic_full_residual"]["vertices"]["14.715"][
        "first_term_count_exceeding_tau_limit"
    ] == 50
    assert search["latin_hypercube_search"]["samples"] == 30000
    assert search["latin_hypercube_search"]["counts"]["combined_finite_pass"] == 0
    assert authority["comparison"]["scheduled_first_horizon_ticks"] == 160
    assert authority["comparison"]["global_first_horizon_ticks"] == 381
    assert box["status"] == "EXACT_AXIS_ALIGNED_RCI_OBSTRUCTION_PASSED"
    assert scheduling["smallest_universal_rho_N_per_tick"] == "9.810"
    assert scheduling["nontrivial_rate_bound_rho_lt_span_is_certified"] is False
    assert endpoint["status"] == "PASS"
    assert endpoint["affine_disturbance_radius_midpoint_identity"] is True
    assert endpoint["affine_pullback_midpoint_identity"] is True
    assert farkas["weighted_rhs"] == "-3069803/88290"
    assert farkas["torque_bound_rows_used"] == 0

    evidence = [
        _evidence(
            root,
            item_id="common_quadratic_static_K",
            level="DERIVED",
            source="verification/check_lpv_common_quadratic_certificate.py",
            result="results/lpv_common_quadratic_20260924/checks.json",
            establishes="One fixed K is strictly common-quadratically stable for the disturbance-free LPV family.",
            excludes="No RCI, disturbance containment, state constraint, torque constraint, or terminal claim.",
        ),
        _evidence(
            root,
            item_id="specific_K_torque_obstruction",
            level="COUNTEREXAMPLE",
            source="verification/check_lpv_torque_rpi_obstruction.py",
            result="results/lpv_torque_rpi_obstruction_20260924/checks.json",
            establishes="The certified nominal K cannot have an origin-containing RPI satisfying the torque limit under the cited disturbance path.",
            excludes="No conclusion about another K, a nonlinear policy, a vertex policy, or plant feasibility.",
        ),
        _evidence(
            root,
            item_id="static_K_search",
            level="NUMERIC_CHECK",
            source="verification/check_vertex_consistent_ancillary_search.py",
            result="results/vertex_consistent_ancillary_20260924/checks.json",
            establishes="No sampled gain passed every finite necessary state and torque check in the frozen search box.",
            excludes="Sampling failure is not an existence or infeasibility certificate.",
        ),
        _evidence(
            root,
            item_id="actuator_authority_trajectory",
            level="NUMERIC_CHECK",
            source="verification/check_actuator_authority_and_scheduled_residual.py",
            result="results/actuator_authority_scheduled_residual_20260924/checks.json",
            establishes="A wider open-loop policy class has feasible low-thrust trajectories numerically; conditioning W on known T materially changes authority.",
            excludes="Not causal feedback, not RCI, and not a recursive-feasibility certificate.",
        ),
        _evidence(
            root,
            item_id="axis_aligned_box_obstruction",
            level="COUNTEREXAMPLE",
            source="verification/check_axis_aligned_rci_obstruction.py",
            result="results/axis_aligned_rci_obstruction_20260924/checks.json",
            establishes="No nonempty origin-centred axis-aligned Cartesian RCI box exists for the stated subsystem contract.",
            excludes="Correlated polytopes, ellipsoids, CZs, parameter-dependent sets, and nonlinear policies remain open.",
        ),
        _evidence(
            root,
            item_id="one_configuration_cone_farkas",
            level="COUNTEREXAMPLE",
            source="verification/check_19pair_cc_exact_farkas.py",
            result="results/cc_19pair_exact_farkas_20260924/checks.json",
            establishes="One audited 19-pair configuration cone is exactly infeasible under its endpoint-robust and hard-state inequalities.",
            excludes="Other cones in the orientation family and other RCI parameterisations remain open.",
        ),
    ]

    direct_dependencies = [
        "verification/check_gate_a_control_baseline_audit.py",
        "verification/test_gate_a_control_baseline_audit.py",
        "configs/planar_baseline.json",
        "results/lpv_common_quadratic_20260924/checks.json",
        "results/lpv_torque_rpi_obstruction_20260924/checks.json",
        "results/vertex_consistent_ancillary_20260924/checks.json",
        "results/actuator_authority_scheduled_residual_20260924/checks.json",
        "results/axis_aligned_rci_obstruction_20260924/checks.json",
        "results/thrust_scheduling_contract_20260924/checks.json",
        "results/endpoint_predecessor_reduction_20260924/checks.json",
        "results/cc_19pair_exact_farkas_20260924/checks.json",
    ]

    return {
        "gate": "A",
        "gate_status": "blocked",
        "scope": "four-state lateral-attitude local benchmark only; not the six-state planar quadrotor guarantee",
        "contract": {
            "current_thrust_measured": True,
            "future_thrust": "arbitrary_jump_in_interval",
            "thrust_interval_N": [scheduling["T_min_N"], scheduling["T_max_N"]],
            "smallest_universal_rate_bound_N_per_tick": scheduling[
                "smallest_universal_rho_N_per_tick"
            ],
            "endpoint_reduction_exact_for_current_affine_contract": bool(
                endpoint["affine_disturbance_radius_midpoint_identity"]
                and endpoint["affine_pullback_midpoint_identity"]
            ),
            "residual_halfwidth": "1.880 + T*0.45^3/6",
        },
        "audit_dependencies_sha256": {
            relative: _sha256(root, relative) for relative in direct_dependencies
        },
        "evidence": evidence,
        "sufficient_ancillary_rci_certificate_present": False,
        "why_blocked": (
            "The repository contains nominal stability and several class-specific or candidate-specific "
            "obstructions, but no sufficient invariant-set/controller certificate covering every allowed "
            "thrust endpoint, disturbance, hard state constraint, and torque constraint."
        ),
        "stopped_branch": (
            "Do not continue local configuration-cone adjacency enumeration until a controller-level "
            "synthesis formulation can return either a sufficient certificate or a class-wide dual certificate."
        ),
        "next_problem": (
            "Construct one sufficient correlated controller/RCI certificate under W(T), arbitrary future "
            "thrust jumps, all state limits, and the torque limit; attack it with independent support checks."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error("output must not already exist")
    out = audit(args.root.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
