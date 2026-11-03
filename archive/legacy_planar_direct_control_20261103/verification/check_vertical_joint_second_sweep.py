#!/usr/bin/env python3
"""Exact second sweep for the complete-fiber vertical joint candidate.

The source and target sets are the Run 145 sets
``C_j^1 = E_j x D_j^0`` in ``(eta, d=e-eta)`` coordinates.  This checker
pulls every target ``D_k^0`` facet back through the visible-error dynamics
with the shared zero correction.  It rejects only this complete-fiber
candidate class; it does not reject correlated conditional fibers.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

from check_vertical_causal_predecessor import ExactPolygon
from check_vertical_joint_first_sweep import (
    _polygon_area,
    first_sweep_inner_certificates,
)
from check_vertical_joint_predecessor import (
    H,
    POSITION_GAIN,
    SHARED_CORRECTION_THRUST,
    _vertical_problem,
)


ROOT = Path(__file__).resolve().parents[1]


def _q_halfwidth(zonotope):
    return sum(
        abs(zonotope[1][column] + H * zonotope[3][column])
        for column in range(len(zonotope[0]))
    )


def _edge_pullback_facets(target_facets, label, innovation_halfwidth):
    """Pull target d-facets back through one miss or success edge."""
    pulled = []
    for a, b, bound in target_facets:
        innovation_support = (
            abs(a + POSITION_GAIN * b) * innovation_halfwidth
            if label == "success"
            else F(0)
        )
        pulled.append((a, a * H + b, bound - innovation_support))
    return pulled


def second_sweep_full_fiber_zero_policy():
    """Compute ``C^1 intersect Pre(C^1)`` in the frozen inner class."""
    first = first_sweep_inner_certificates()
    config, zonotopes = _vertical_problem()
    noise = config["sensing"]["observed_noise_halfwidth"]["pz"]
    graph = config["mpc"]["ancillary_rci_contract"]["mode_graph"]["edges"]
    outgoing = {mode: [] for mode in range(15)}
    for source, target, label in graph:
        outgoing[source].append((target, label))

    rows = {}
    collapsed = []
    for mode, zonotope in enumerate(zonotopes):
        source_facets = first["modes"][mode]["observation_projection_facets"]
        inequalities = list(source_facets)
        q_halfwidth = _q_halfwidth(zonotope)
        edges = []
        for target, label in outgoing[mode]:
            innovation_halfwidth = q_halfwidth + noise if label == "success" else F(0)
            pulled = _edge_pullback_facets(
                first["modes"][target]["observation_projection_facets"],
                label,
                innovation_halfwidth,
            )
            inequalities.extend(pulled)
            edges.append({
                "target": target,
                "label": label,
                "shared_correction_thrust": SHARED_CORRECTION_THRUST,
                "innovation_halfwidth": innovation_halfwidth,
                "pulled_target_facet_count": len(pulled),
            })

        polygon = ExactPolygon.from_inequalities(inequalities)
        empty = polygon.is_empty
        area = F(0) if empty else _polygon_area(polygon)
        if empty:
            collapsed.append(mode)
        rows[mode] = {
            "shared_correction_thrust": SHARED_CORRECTION_THRUST,
            "policy_values_on_observation_projection": 1,
            "source_first_sweep_observation_area": first["modes"][mode][
                "observation_projection_area"
            ],
            "second_sweep_observation_projection_empty": empty,
            "second_sweep_observation_projection_area": area,
            "second_sweep_observation_projection_facet_count": len(polygon.facets),
            "second_sweep_observation_projection_facets": polygon.facets,
            "second_sweep_observation_projection_vertices": polygon.vertices,
            "joint_inner_dimension": 0 if empty else 4,
            "edges": edges,
        }

    target_velocity_halfwidth = max(
        abs(vertex[1])
        for vertex in first["modes"][0]["observation_projection_vertices"]
    )
    mode14_q_halfwidth = _q_halfwidth(zonotopes[14])
    innovation_halfwidth = mode14_q_halfwidth + noise
    success_velocity_spread = POSITION_GAIN * innovation_halfwidth
    strict_excess = success_velocity_spread - target_velocity_halfwidth
    obstruction = {
        "forced_edge": (14, 0, "success"),
        "mode14_q_halfwidth": mode14_q_halfwidth,
        "measurement_noise_halfwidth": noise,
        "success_innovation_halfwidth": innovation_halfwidth,
        "success_velocity_spread": success_velocity_spread,
        "mode_zero_target_velocity_halfwidth": target_velocity_halfwidth,
        "strict_halfwidth_excess": strict_excess,
        "strict_width_obstruction": strict_excess > 0,
        "correction_only_translates_interval": True,
    }
    if collapsed != [14] or not obstruction["strict_width_obstruction"]:
        raise AssertionError("second-sweep collapse certificate changed")

    return {
        "candidate": "C_j^1 = E_eta_vertical_j x D_j^0 in (eta,d) coordinates",
        "candidate_class": "complete_eta_fiber_with_shared_zero_correction",
        "shared_correction_thrust": SHARED_CORRECTION_THRUST,
        "graph_edge_count": len(graph),
        "positive_volume_mode_count": 15 - len(collapsed),
        "collapsed_modes": collapsed,
        "modes": rows,
        "mode14_width_obstruction": obstruction,
    }


def run():
    certificate = second_sweep_full_fiber_zero_policy()
    return {
        "status": "pass",
        "claim": "mode14_complete_fiber_second_sweep_is_empty_by_exact_width_obstruction",
        **certificate,
        "descending_sweep_iterations": 2,
        "evidence_level": (
            "exact_mode14_width_obstruction_for_complete_fiber_second_sweep"
        ),
        "complete_fiber_candidate_class_rejected": True,
        "general_joint_information_rci_rejected": False,
        "is_rci_certificate": False,
        "full_six_state_guarantee": False,
        "limitations": [
            "the obstruction rejects C^1 with every d paired with the complete Run136 eta fiber",
            "it does not reject conditional eta-given-d fibers or general information ensembles",
            "the fourteen surviving mode projections do not form an invariant family",
            "horizontal, attitude, torque, terminal, shift, and recursive MPC feasibility remain open",
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
        "verification/check_vertical_joint_second_sweep.py",
        "verification/test_vertical_joint_second_sweep.py",
        "verification/check_vertical_joint_first_sweep.py",
        "verification/check_vertical_joint_predecessor.py",
        "verification/check_vertical_causal_predecessor.py",
        "verification/check_rolling_control_normal_ledger.py",
        "verification/test_rolling_control_normal_ledger.py",
        "verification/check_cycle_lifted_zonotope.py",
        "verification/check_mode_nestedness.py",
        "verification/check_mode_radius.py",
        "verification/check_intermittent_metric.py",
        "configs/planar_baseline.json",
        "docs/learning/83_vertical_joint_second_sweep.md",
        "docs/literature/READ_PAPERS.md",
        "docs/research/run146_literature_gate.md",
        "docs/research/run146_research_log.md",
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
        "positive_volume_mode_count": encoded["positive_volume_mode_count"],
        "collapsed_modes": encoded["collapsed_modes"],
        "evidence_level": encoded["evidence_level"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
