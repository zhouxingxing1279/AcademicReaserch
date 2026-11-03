#!/usr/bin/env python3
"""Exact coordinate-freedom gate for the configured six-facet family."""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
from itertools import combinations
import json
from pathlib import Path

from check_houska_vertical_adapter import run as adapter_run
from check_six_facet_measurement_gate import six_facet_template


ZERO = F(0)
HALF = F(1, 2)
ROOT = Path(__file__).resolve().parents[1]
PAIRED_ORDER = ["c_p", "c_v", "c_q", "r_p", "r_v", "r_q"]


def paired_coordinates(offsets):
    """Map (+p,+v,-q,-p,-v,+q) offsets to three centers and radii."""
    if len(offsets) != 6:
        raise ValueError("six facet offsets are required")
    return {
        "c_p": (offsets[0] - offsets[3]) * HALF,
        "c_v": (offsets[1] - offsets[4]) * HALF,
        "c_q": (offsets[5] - offsets[2]) * HALF,
        "r_p": (offsets[0] + offsets[3]) * HALF,
        "r_v": (offsets[1] + offsets[4]) * HALF,
        "r_q": (offsets[2] + offsets[5]) * HALF,
    }


def vector_to_paired(vector):
    if len(vector) != 6:
        raise ValueError("six paired coordinates are required")
    return dict(zip(PAIRED_ORDER, vector))


def offsets_from_paired(coordinates):
    """Invert paired_coordinates without imposing translation consistency."""
    return [
        coordinates["c_p"] + coordinates["r_p"],
        coordinates["c_v"] + coordinates["r_v"],
        -coordinates["c_q"] + coordinates["r_q"],
        -coordinates["c_p"] + coordinates["r_p"],
        -coordinates["c_v"] + coordinates["r_v"],
        coordinates["c_q"] + coordinates["r_q"],
    ]


def skew(coordinates):
    """Return the missing coordinate in a five-parameter translated-symmetric model."""
    kappa = six_facet_template()["kappa"]
    return coordinates["c_q"] - coordinates["c_p"] + kappa * coordinates["c_v"]


def _tight_offsets(normals, offsets, target_normals):
    vertices = []
    for first, second in combinations(range(len(normals)), 2):
        a, b = normals[first]
        c, d = normals[second]
        determinant = a * d - b * c
        if determinant == 0:
            continue
        vertex = [
            (d * offsets[first] - b * offsets[second]) / determinant,
            (-c * offsets[first] + a * offsets[second]) / determinant,
        ]
        if all(
            normal[0] * vertex[0] + normal[1] * vertex[1] <= bound
            for normal, bound in zip(normals, offsets)
        ) and vertex not in vertices:
            vertices.append(vertex)
    if not vertices:
        raise ValueError("measurement intersection is empty")
    return [
        max(normal[0] * vertex[0] + normal[1] * vertex[1] for vertex in vertices)
        for normal in target_normals
    ]


def measurement_intersection_offsets(offsets, center, halfwidth):
    """Return tight six-direction supports after a position measurement strip."""
    if halfwidth < 0:
        raise ValueError("measurement halfwidth must be nonnegative")
    template = six_facet_template()
    normals = template["Y"] + [[F(1), F(0)], [-F(1), F(0)]]
    bounds = list(offsets) + [center + halfwidth, -center + halfwidth]
    return _tight_offsets(normals, bounds, template["Y"])


def transform_parameter_vertices(vertices):
    """Apply the invertible paired-coordinate map to parameter vertices."""
    return [[paired_coordinates(vertex)[name] for name in PAIRED_ORDER] for vertex in vertices]


def _matvec(matrix, vector):
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]


def run():
    template = six_facet_template()
    adapter = adapter_run()
    halfwidth = adapter["measurement_operators"]["success"]["noise_halfwidth"]
    if halfwidth != F(1, 50):
        raise AssertionError("actual measurement halfwidth changed")
    source = [F(3, 200)] * 6
    measurement_center = F(-23, 4000)
    posterior = measurement_intersection_offsets(source, measurement_center, halfwidth)
    expected = [F(57, 4000)] + [F(3, 200)] * 5
    if posterior != expected:
        raise AssertionError("one-sided measurement posterior changed")
    source_paired = paired_coordinates(source)
    posterior_paired = paired_coordinates(posterior)
    if skew(source_paired) != 0 or skew(posterior_paired) != F(3, 8000):
        raise AssertionError("five-coordinate nonclosure witness changed")
    margins = _matvec(template["G"], posterior)
    if max(margins) != F(-3, 4000):
        raise AssertionError("posterior is not strictly inside the selected configuration")

    base = source
    parameter_vertices = [base] + [
        [value + (F(1, 10000) if index == axis else ZERO)
         for index, value in enumerate(base)]
        for axis in range(6)
    ]
    transformed = transform_parameter_vertices(parameter_vertices)
    recovered = [offsets_from_paired(vector_to_paired(vertex)) for vertex in transformed]
    if recovered != parameter_vertices or len({tuple(vertex) for vertex in transformed}) != 7:
        raise AssertionError("invertible coordinate map changed the extreme-candidate count")

    return {
        "claim": "five_center_radius_coordinates_are_not_measurement_closed",
        "evidence_level": "exact_six_facet_meta_coordinate_nonclosure_certificate",
        "facet_order": template["facet_order"],
        "paired_coordinate_order": PAIRED_ORDER,
        "skew_definition": "delta = c_q - c_p + kappa*c_v",
        "source_offsets": source,
        "source_skew": skew(source_paired),
        "measurement_center": measurement_center,
        "measurement_halfwidth": halfwidth,
        "measurement_interval": [measurement_center - halfwidth, measurement_center + halfwidth],
        "posterior_offsets": posterior,
        "posterior_skew": skew(posterior_paired),
        "posterior_configuration_max_margin": max(margins),
        "five_coordinate_family_rejected": True,
        "six_coordinate_map_invertible": True,
        "same_polytope_extreme_count_before": len(parameter_vertices),
        "same_polytope_extreme_count_after": len(transformed),
        "same_polytope_extreme_count_preserved": True,
        "bounded_meta_polytope_selected": False,
        "complete_H_Omega_certified": False,
        "graph_invariant_information_ensemble_certified": False,
        "mpc_recursive_feasibility_certified": False,
        "full_six_state_guarantee": False,
        "limitations": [
            "the witness is a representation-closure counterexample, not a controller result",
            "budget neutrality concerns the same polytope under an invertible coordinate map",
            "no bounded direct-offset meta polytope or H/Omega configuration is selected",
            "the 15-mode/17-edge graph LP, input constraints, and terminal conditions are untested",
        ],
    }


def _encode(value):
    if isinstance(value, F):
        return str(value)
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
        "verification/check_six_facet_meta_coordinate_gate.py",
        "verification/test_six_facet_meta_coordinate_gate.py",
        "verification/check_six_facet_measurement_gate.py",
        "verification/check_houska_vertical_adapter.py",
        "configs/planar_baseline.json",
        "docs/superpowers/specs/2026-10-27-six-facet-meta-coordinate-gate-design.md",
    ]
    result["source_sha256"] = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in sources
    }
    encoded = _encode(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(encoded, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "evidence_level": encoded["evidence_level"],
        "posterior_skew": encoded["posterior_skew"],
        "extreme_count": encoded["same_polytope_extreme_count_after"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
