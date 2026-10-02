#!/usr/bin/env python3
"""Exact inner certificates for one vertical joint predecessor sweep.

For every packet-loss mode, this checker constructs an exact rational
observation polygon on which the single causal policy ``deltaT=0`` keeps the
entire hidden estimation-error fiber inside the vertical joint candidate.
It verifies all outgoing estimator edges.  The polygons are conservative
inner projections of the first descending predecessor layer, not maximal
projections and not invariant sets.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

from check_vertical_joint_predecessor import (
    H,
    OBSERVATION_HALFWIDTHS,
    SHARED_CORRECTION_THRUST,
    _eta_edge_certificate,
    _polygon_area,
    _residual_halfwidth,
    _tracking_limits,
    _vertical_problem,
    _zonotope_polygon,
)
from check_vertical_causal_predecessor import ExactPolygon


ROOT = Path(__file__).resolve().parents[1]


def _vertical_support(zonotope, normal):
    return sum(
        abs(normal[0] * zonotope[1][column] + normal[1] * zonotope[3][column])
        for column in range(len(zonotope[0]))
    )


def _full_fiber_zero_policy_projection(zonotope, position_limit, velocity_limit,
                                       residual_halfwidth):
    """Return d values whose complete eta fiber is safe now and after one step."""
    eta_position = _vertical_support(zonotope, (F(1), F(0)))
    eta_velocity = _vertical_support(zonotope, (F(0), F(1)))
    eta_next_position = _vertical_support(zonotope, (F(1), H))
    return ExactPolygon.from_inequalities([
        (F(1), F(0), position_limit - eta_position),
        (F(-1), F(0), position_limit - eta_position),
        (F(0), F(1), velocity_limit - eta_velocity - H * residual_halfwidth),
        (F(0), F(-1), velocity_limit - eta_velocity - H * residual_halfwidth),
        (F(1), H, position_limit - eta_next_position),
        (F(-1), -H, position_limit - eta_next_position),
    ])


def _contains_box(polygon, halfwidths):
    px, py = halfwidths
    return all(
        polygon.contains((sx * px, sy * py))
        for sx in (F(-1), F(1))
        for sy in (F(-1), F(1))
    )


def first_sweep_inner_certificates():
    """Certify positive-volume inner subsets of all 15 first-sweep modes."""
    config, zonotopes = _vertical_problem()
    position_limit, velocity_limit = _tracking_limits(config)
    nominal_interval = tuple(
        config["mpc"][key][0]
        for key in ("nominal_input_lower", "nominal_input_upper")
    )
    correction_interval = tuple(
        config["mpc"][key][0]
        for key in ("ancillary_correction_lower", "ancillary_correction_upper")
    )
    if not correction_interval[0] <= SHARED_CORRECTION_THRUST <= correction_interval[1]:
        raise AssertionError("zero correction is outside the frozen allocation")
    actual_interval = tuple(value + SHARED_CORRECTION_THRUST for value in nominal_interval)
    residual_halfwidth = _residual_halfwidth(actual_interval[1])
    noise = config["sensing"]["observed_noise_halfwidth"]["pz"]

    graph = config["mpc"]["ancillary_rci_contract"]["mode_graph"]["edges"]
    outgoing = {mode: [] for mode in range(15)}
    for source, target, label in graph:
        outgoing[source].append((target, label))

    rows = {}
    for mode, zonotope in enumerate(zonotopes):
        eta_polygon = _zonotope_polygon(zonotope)
        observation_polygon = _full_fiber_zero_policy_projection(
            zonotope, position_limit, velocity_limit, residual_halfwidth
        )
        eta_area = _polygon_area(eta_polygon)
        observation_area = _polygon_area(observation_polygon)
        edges = [
            _eta_edge_certificate(
                mode, target, label, zonotopes, residual_halfwidth, noise
            )
            for target, label in outgoing[mode]
        ]
        contains_common_box = _contains_box(
            observation_polygon, OBSERVATION_HALFWIDTHS
        )
        positive = (
            not observation_polygon.is_empty
            and eta_area > 0
            and observation_area > 0
            and contains_common_box
            and all(edge["eta_target_contained"] for edge in edges)
        )
        if not positive:
            raise AssertionError(f"mode {mode} lacks a positive-volume first-sweep inner set")
        rows[mode] = {
            "shared_correction_thrust": SHARED_CORRECTION_THRUST,
            "policy_values_on_observation_projection": 1,
            "eta_projection_area": eta_area,
            "observation_projection_area": observation_area,
            "observation_projection_facet_count": len(observation_polygon.facets),
            "observation_projection_facets": observation_polygon.facets,
            "observation_projection_vertices": observation_polygon.vertices,
            "contains_run144_common_observation_box": contains_common_box,
            "joint_inner_dimension": 4,
            "edges": edges,
            "positive_volume_inner_certificate": positive,
        }

    return {
        "candidate": "S_j = E_eta_vertical_j x {|e_pz|<=1, |e_vz|<=11/4}",
        "inner_projection_class": "complete_eta_fiber_with_shared_zero_correction",
        "common_observation_box_halfwidths": OBSERVATION_HALFWIDTHS,
        "shared_correction_thrust": SHARED_CORRECTION_THRUST,
        "nominal_thrust_interval": nominal_interval,
        "actual_thrust_interval": actual_interval,
        "residual_halfwidth_at_actual_thrust_upper": residual_halfwidth,
        "graph_edge_count": len(graph),
        "nonempty_mode_count": len(rows),
        "modes": rows,
    }


def run():
    certificate = first_sweep_inner_certificates()
    return {
        "status": "pass",
        "claim": "all_fifteen_vertical_joint_first_sweep_modes_have_positive_volume_inner_certificates",
        **certificate,
        "descending_sweep_iterations": 1,
        "evidence_level": (
            "exact_positive_volume_inner_certificates_for_all_fifteen_first_sweep_modes"
        ),
        "is_maximal_observation_projection": False,
        "is_rci_certificate": False,
        "fixed_point_iteration_run": False,
        "full_six_state_guarantee": False,
        "limitations": [
            "each observation polygon is a zero-policy complete-fiber inner projection, not the maximal first-sweep projection",
            "one descending predecessor layer is not a controlled invariant set",
            "no fixed-point iteration or finite-termination test is run",
            "horizontal, attitude, torque, terminal, shift, and recursive MPC feasibility remain open",
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
        "verification/check_vertical_joint_first_sweep.py",
        "verification/test_vertical_joint_first_sweep.py",
        "verification/check_vertical_joint_predecessor.py",
        "verification/check_vertical_causal_predecessor.py",
        "verification/check_cycle_lifted_zonotope.py",
        "verification/check_mode_nestedness.py",
        "verification/check_mode_radius.py",
        "verification/check_intermittent_metric.py",
        "configs/planar_baseline.json",
        "docs/learning/82_vertical_joint_first_sweep.md",
        "docs/literature/READ_PAPERS.md",
        "docs/research/run145_literature_gate.md",
        "docs/research/run145_research_log.md",
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
        "nonempty_mode_count": encoded["nonempty_mode_count"],
        "graph_edge_count": encoded["graph_edge_count"],
        "evidence_level": encoded["evidence_level"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
