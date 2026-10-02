#!/usr/bin/env python3
"""Exact one-step inner certificates for the vertical joint information set.

The joint coordinates are ``(eta_pz, eta_vz, e_pz, e_vz)`` and the
controller observes ``d=e-eta``.  This checker only proves that the three
critical mode predecessors contain a positive-volume observation-fiber
region.  It does not iterate a fixed point or certify an RCI.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

from check_cycle_lifted_zonotope import (
    age_zonotopes,
    least_mode_zero_box,
    lift_cycle,
    problem_data,
)
from check_vertical_causal_predecessor import ExactPolygon


ROOT = Path(__file__).resolve().parents[1]
H = F(1, 50)
POSITION_GAIN = F(9, 2)
OBSERVATION_HALFWIDTHS = (F(1, 5), F(1, 4))
SHARED_CORRECTION_THRUST = F(0)


def _vertical_problem():
    config, A0, G0, A1, G1, _ = problem_data()
    cycles = [lift_cycle(length, A0, G0, A1, G1) for length in (5, 10, 15)]
    mode_zero_box = least_mode_zero_box(cycles)
    zonotopes = age_zonotopes(mode_zero_box, A0, G0)
    return config, zonotopes


def _tracking_limits(config):
    nominal = config["mpc"]["ancillary_rci_contract"]["nominal_state_domain"]
    position = min(
        config["domain"]["state_upper"][1] - nominal["upper"][1],
        nominal["lower"][1] - config["domain"]["state_lower"][1],
    )
    velocity = min(
        config["domain"]["state_upper"][3] - nominal["upper"][3],
        nominal["lower"][3] - config["domain"]["state_lower"][3],
    )
    return position, velocity


def _vertical_generators(zonotope):
    return [
        (zonotope[1][column], zonotope[3][column])
        for column in range(len(zonotope[0]))
        if zonotope[1][column] or zonotope[3][column]
    ]


def _zonotope_polygon(zonotope):
    generators = _vertical_generators(zonotope)
    inequalities = []
    for x, y in generators:
        for sign in (F(1), F(-1)):
            a, b = sign * y, -sign * x
            support = sum(abs(a * gx + b * gy) for gx, gy in generators)
            inequalities.append((a, b, support))
    return ExactPolygon.from_inequalities(inequalities)


def _polygon_area(polygon):
    terms = (
        first[0] * second[1] - first[1] * second[0]
        for first, second in zip(
            polygon.vertices, polygon.vertices[1:] + polygon.vertices[:1]
        )
    )
    return abs(sum(terms, F(0))) / 2


def _support(generators, normal, matrix):
    a, b = normal
    return sum(
        abs(
            a * (matrix[0][0] * x + matrix[0][1] * y)
            + b * (matrix[1][0] * x + matrix[1][1] * y)
        )
        for x, y in generators
    )


def _residual_halfwidth(actual_thrust):
    return F(1043, 500) + F(81, 800) * F(actual_thrust)


def _eta_edge_certificate(source, target, label, zonotopes, residual_halfwidth, noise):
    success = label == "success"
    matrix = (
        ((F(0), F(0)), (-POSITION_GAIN, F(1) - POSITION_GAIN * H))
        if success
        else ((F(1), H), (F(0), F(1)))
    )
    residual_direction = (F(0), H)
    noise_direction = (F(-1), -POSITION_GAIN)
    generators = _vertical_generators(zonotopes[source])
    target_polygon = _zonotope_polygon(zonotopes[target])
    slacks = []
    residual_sensitive_slacks = []
    for a, b, bound in target_polygon.facets:
        support = _support(generators, (a, b), matrix)
        residual_coefficient = abs(
            a * residual_direction[0] + b * residual_direction[1]
        )
        support += residual_coefficient * residual_halfwidth
        if success:
            support += abs(a * noise_direction[0] + b * noise_direction[1]) * noise
        slack = bound - support
        slacks.append(slack)
        if residual_coefficient:
            residual_sensitive_slacks.append(slack)
    return {
        "target": target,
        "label": label,
        "eta_target_contained": all(slack >= 0 for slack in slacks),
        "minimum_eta_facet_slack": min(slacks),
        "minimum_eta_residual_sensitive_facet_slack": min(
            residual_sensitive_slacks
        ),
        "target_facet_count": len(target_polygon.facets),
    }


def joint_candidate_contains(mode, eta, tracking_error):
    """Membership in S_j = E_j x B_e; no independent d limit is imposed."""
    if mode not in range(15):
        return False
    eta = tuple(map(F, eta))
    tracking_error = tuple(map(F, tracking_error))
    if len(eta) != 2 or len(tracking_error) != 2:
        return False
    config, zonotopes = _vertical_problem()
    position_limit, velocity_limit = _tracking_limits(config)
    return (
        _zonotope_polygon(zonotopes[mode]).contains(eta)
        and abs(tracking_error[0]) <= position_limit
        and abs(tracking_error[1]) <= velocity_limit
    )


def critical_mode_predecessors():
    """Certify one shared zero-input policy on a positive-volume d-box."""
    config, zonotopes = _vertical_problem()
    tracking_position_limit, tracking_velocity_limit = _tracking_limits(config)
    nominal_interval = tuple(config["mpc"][key][0] for key in (
        "nominal_input_lower", "nominal_input_upper"
    ))
    correction_interval = tuple(config["mpc"][key][0] for key in (
        "ancillary_correction_lower", "ancillary_correction_upper"
    ))
    if not correction_interval[0] <= SHARED_CORRECTION_THRUST <= correction_interval[1]:
        raise AssertionError("zero correction is outside the frozen allocation")
    actual_thrust_interval = tuple(
        thrust + SHARED_CORRECTION_THRUST for thrust in nominal_interval
    )
    residual_halfwidth = _residual_halfwidth(actual_thrust_interval[1])
    run136_halfwidth = _residual_halfwidth(config["domain"]["input_upper"][0])
    noise = config["sensing"]["observed_noise_halfwidth"]["pz"]
    edges = config["mpc"]["ancillary_rci_contract"]["mode_graph"]["edges"]
    outgoing = {mode: [] for mode in range(15)}
    for source, target, label in edges:
        outgoing[source].append((target, label))

    d_position, d_velocity = OBSERVATION_HALFWIDTHS
    modes = {}
    for mode in (4, 9, 14):
        zonotope = zonotopes[mode]
        eta_polygon = _zonotope_polygon(zonotope)
        eta_area = _polygon_area(eta_polygon)
        eta_position = sum(abs(value) for value in zonotope[1])
        eta_velocity = sum(abs(value) for value in zonotope[3])
        q_support = sum(
            abs(zonotope[1][column] + H * zonotope[3][column])
            for column in range(len(zonotope[0]))
        )
        current_position_slack = tracking_position_limit - eta_position - d_position
        current_velocity_slack = tracking_velocity_limit - eta_velocity - d_velocity
        next_position_slack = (
            tracking_position_limit - q_support - d_position - H * d_velocity
        )
        next_velocity_slack = (
            tracking_velocity_limit
            - eta_velocity
            - d_velocity
            - H * residual_halfwidth
        )
        edge_certificates = [
            _eta_edge_certificate(
                mode, target, label, zonotopes, residual_halfwidth, noise
            )
            for target, label in outgoing[mode]
        ]
        positive = (
            d_position > 0
            and d_velocity > 0
            and eta_area > 0
            and current_position_slack > 0
            and current_velocity_slack > 0
            and next_position_slack > 0
            and next_velocity_slack > 0
            and all(edge["eta_target_contained"] for edge in edge_certificates)
        )
        if not positive:
            raise AssertionError(f"critical mode {mode} has no certified inner predecessor")
        modes[mode] = {
            "shared_correction_thrust": SHARED_CORRECTION_THRUST,
            "policy_values_on_inner_box": 1,
            "eta_projection_area": eta_area,
            "joint_inner_dimension": 4,
            "current_fiber_position_slack": current_position_slack,
            "current_fiber_velocity_slack": current_velocity_slack,
            "next_tracking_position_slack": next_position_slack,
            "next_tracking_velocity_slack": next_velocity_slack,
            "edges": edge_certificates,
            "positive_volume_inner_certificate": positive,
        }

    return {
        "candidate": "S_j = E_eta_vertical_j x {|e_pz|<=1, |e_vz|<=11/4}",
        "observation": "d = e - eta",
        "observation_halfwidths": OBSERVATION_HALFWIDTHS,
        "tracking_error_limits": (tracking_position_limit, tracking_velocity_limit),
        "shared_correction_thrust": SHARED_CORRECTION_THRUST,
        "nominal_thrust_interval": nominal_interval,
        "actual_thrust_interval": actual_thrust_interval,
        "residual_halfwidth_at_actual_thrust_upper": residual_halfwidth,
        "run136_certified_residual_halfwidth": run136_halfwidth,
        "modes": modes,
    }


def run():
    certificate = critical_mode_predecessors()
    return {
        "status": "pass",
        "claim": "three_critical_vertical_joint_one_step_predecessors_have_positive_volume_inner_certificates",
        "candidate": certificate["candidate"],
        "predecessor_semantics": (
            "one correction per fixed d fiber, shared across hidden eta and all outgoing edges"
        ),
        "observation_halfwidths": certificate["observation_halfwidths"],
        "nominal_thrust_interval": certificate["nominal_thrust_interval"],
        "actual_thrust_interval": certificate["actual_thrust_interval"],
        "residual_halfwidth_at_actual_thrust_upper": certificate[
            "residual_halfwidth_at_actual_thrust_upper"
        ],
        "run136_certified_residual_halfwidth": certificate[
            "run136_certified_residual_halfwidth"
        ],
        "critical_modes": certificate["modes"],
        "evidence_level": (
            "exact_positive_volume_inner_certificate_for_three_critical_one_step_predecessors"
        ),
        "is_rci_certificate": False,
        "fixed_point_iteration_run": False,
        "full_six_state_guarantee": False,
        "limitations": [
            "the certificate is an inner subset of only three one-step predecessors",
            "it does not prove that the full candidate is controlled invariant",
            "the remaining modes and any descending fixed-point iteration are not checked",
            "horizontal, attitude, terminal, shift, and recursive MPC feasibility remain open",
            "the frozen input allocation remains an existence probe without maneuvering interior",
        ],
    }


def _encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, tuple):
        return [_encode(item) for item in value]
    if isinstance(value, list):
        return [_encode(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _encode(item) for key, item in value.items()}
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    result = run()
    sources = [
        "verification/check_vertical_joint_predecessor.py",
        "verification/test_vertical_joint_predecessor.py",
        "verification/check_cycle_lifted_zonotope.py",
        "verification/check_vertical_causal_predecessor.py",
        "verification/check_mode_nestedness.py",
        "verification/check_mode_radius.py",
        "verification/check_intermittent_metric.py",
        "configs/planar_baseline.json",
        "docs/learning/81_vertical_joint_one_step_predecessor.md",
        "docs/literature/READ_PAPERS.md",
        "docs/research/run144_literature_gate.md",
        "docs/research/run144_research_log.md",
    ]
    result["source_sha256"] = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in sources
    }
    encoded = _encode(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(encoded, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "status": encoded["status"],
        "claim": encoded["claim"],
        "critical_modes": sorted(encoded["critical_modes"]),
        "evidence_level": encoded["evidence_level"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
