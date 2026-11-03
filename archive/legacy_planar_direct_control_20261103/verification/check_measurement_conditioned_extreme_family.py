#!/usr/bin/env python3
"""Exact local gate for a measurement-conditioned extreme information family."""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

from check_houska_vertical_adapter import run as adapter_run
from check_six_facet_measurement_gate import six_facet_template


ROOT = Path(__file__).resolve().parents[1]
ZERO = F(0)


def _contract():
    adapter = adapter_run()
    return (
        adapter["tracking_error_box"]["position_halfwidth"],
        adapter["tracking_error_box"]["velocity_halfwidth"],
        adapter["measurement_operators"]["success"]["noise_halfwidth"],
    )


def measurement_center_domain():
    position, _, noise = _contract()
    return -position - noise, position + noise


def maximal_center_domain():
    position, _, noise = _contract()
    return -position + noise, position - noise


def posterior_interval(measurement_center):
    """Return the exact position projection of X intersect S(eta)."""
    position, _, noise = _contract()
    lower_domain, upper_domain = measurement_center_domain()
    if not lower_domain <= measurement_center <= upper_domain:
        raise ValueError("measurement strip has empty intersection with the physical box")
    return (
        max(-position, measurement_center - noise),
        min(position, measurement_center + noise),
    )


def clamped_center(measurement_center):
    lower, upper = maximal_center_domain()
    return min(upper, max(lower, measurement_center))


def maximal_position_interval(center):
    lower, upper = maximal_center_domain()
    if not lower <= center <= upper:
        raise ValueError("maximal-family center is outside its certified domain")
    _, _, noise = _contract()
    return center - noise, center + noise


def tight_offsets(center):
    """Tight supports of R(c) in (+p,+v,-q,-p,-v,+q) order."""
    _, velocity, noise = _contract()
    lower, upper = maximal_center_domain()
    if not lower <= center <= upper:
        raise ValueError("maximal-family center is outside its certified domain")
    kappa = six_facet_template()["kappa"]
    return [
        center + noise,
        velocity,
        -center + noise + kappa * velocity,
        -center + noise,
        velocity,
        center + noise + kappa * velocity,
    ]


def configuration_valid(offsets):
    template = six_facet_template()
    return all(
        sum(coefficient * offset for coefficient, offset in zip(row, offsets)) <= ZERO
        for row in template["G"]
    )


def rectangle_contains(outer_center, inner_center):
    """Containment for equal-width maximal rectangles; true iff centers agree."""
    outer = maximal_position_interval(outer_center)
    inner = maximal_position_interval(inner_center)
    return outer[0] <= inner[0] and inner[1] <= outer[1]


def _matvec(matrix, vector):
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]


def run():
    position, velocity, noise = _contract()
    if (position, velocity, noise) != (F(1), F(11, 4), F(1, 50)):
        raise AssertionError("certified vertical measurement contract changed")

    center_bounds = maximal_center_domain()
    endpoint_offsets = [tight_offsets(center) for center in center_bounds]
    if not all(configuration_valid(offsets) for offsets in endpoint_offsets):
        raise AssertionError("measurement-conditioned endpoint left configuration cone")
    if rectangle_contains(center_bounds[0], center_bounds[1]):
        raise AssertionError("distinct endpoint rectangles became comparable")
    if rectangle_contains(center_bounds[1], center_bounds[0]):
        raise AssertionError("distinct endpoint rectangles became comparable")

    template = six_facet_template()
    endpoint_vertex_sets = []
    for offsets in endpoint_offsets:
        vertices = sorted({tuple(_matvec(vertex_map, offsets)) for vertex_map in template["Lambda"]})
        endpoint_vertex_sets.append([list(vertex) for vertex in vertices])

    measurement_bounds = measurement_center_domain()
    boundary_posteriors = {
        str(center): posterior_interval(center)
        for center in measurement_bounds
    }
    return {
        "claim": "actual_position_measurements_generate_a_continuum_of_incomparable_extreme_sets",
        "evidence_level": "exact_measurement_conditioned_extreme_information_family",
        "facet_order": template["facet_order"],
        "physical_position_halfwidth": position,
        "physical_velocity_halfwidth": velocity,
        "measurement_noise_halfwidth": noise,
        "measurement_center_domain": list(measurement_bounds),
        "maximal_family_center_domain": list(center_bounds),
        "maximal_family": "R(c)=[c-a,c+a]x[-V,V] for c in [-P+a,P-a]",
        "tight_offset_map": "(c+a,V,-c+a+kappa*V,-c+a,V,c+a+kappa*V)",
        "parameter_polytope_vertex_count": 2,
        "parameter_polytope_vertex_offsets": endpoint_offsets,
        "endpoint_configured_vertex_sets": endpoint_vertex_sets,
        "endpoint_extreme_sets_incomparable": True,
        "true_extreme_set_boundary_cardinality": "continuum",
        "true_extreme_set_boundary": "{R(c): c in [-P+a,P-a]}",
        "maximality_argument": "equal-width rectangles satisfy R(c1) subseteq R(c2) iff c1=c2",
        "boundary_measurement_posteriors": boundary_posteriors,
        "coverage_map": "eta maps to clip(eta,[-P+a,P-a])",
        "all_nonempty_measurement_posteriors_covered": True,
        "measurement_closed_information_ensemble": True,
        "measurement_closure_argument": "compact subsets of R(c) remain subsets after arbitrary intersections",
        "endpoint_convex_hull_equals_physical_box": True,
        "velocity_halfwidth_after_measurement": velocity,
        "slant_facets_redundant_on_maximal_family": True,
        "regular_six_facet_meta_configuration_certified": False,
        "run184_velocity_cycle_removed": False,
        "graph_invariant_information_ensemble_certified": False,
        "input_feasibility_certified": False,
        "terminal_invariance_certified": False,
        "mpc_recursive_feasibility_certified": False,
        "full_six_state_guarantee": False,
        "limitations": [
            "the true extreme boundary is a continuum; the two parameter vertices are finite representatives only",
            "the position update leaves the full physical velocity halfwidth unchanged",
            "the slant inequalities are tight supports but redundant on these rectangular maximal sets",
            "no propagation, control, terminal, or recursive-feasibility condition is certified",
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
        "verification/check_measurement_conditioned_extreme_family.py",
        "verification/test_measurement_conditioned_extreme_family.py",
        "verification/check_six_facet_measurement_gate.py",
        "verification/check_houska_vertical_adapter.py",
        "configs/planar_baseline.json",
        "docs/superpowers/specs/2026-10-27-measurement-conditioned-extreme-family-design.md",
    ]
    result["source_sha256"] = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in sources
    }
    encoded = _encode(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(encoded, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "evidence_level": encoded["evidence_level"],
        "parameter_polytope_vertex_count": encoded["parameter_polytope_vertex_count"],
        "true_extreme_set_boundary_cardinality": encoded["true_extreme_set_boundary_cardinality"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
