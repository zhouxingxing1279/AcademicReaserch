#!/usr/bin/env python3
"""Exact six-facet configuration and position-measurement support gate."""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

from check_houska_vertical_adapter import run as adapter_run


ZERO = F(0)
ONE = F(1)
KAPPA = F(1, 10)
ROOT = Path(__file__).resolve().parents[1]


def _vertex_map(Y, first, second):
    a, b = Y[first]
    c, d = Y[second]
    determinant = a * d - b * c
    if determinant == 0:
        raise ValueError("adjacent facet normals must be independent")
    inverse = [[d / determinant, -b / determinant],
               [-c / determinant, a / determinant]]
    result = [[ZERO for _ in range(len(Y))] for _ in range(2)]
    for row in range(2):
        result[row][first] = inverse[row][0]
        result[row][second] = inverse[row][1]
    return result


def _matmul(left, right):
    return [[
        sum(left[row][inner] * right[inner][column]
            for inner in range(len(right)))
        for column in range(len(right[0]))
    ] for row in range(len(left))]


def six_facet_template():
    """Return the cyclic Y/G/Lambda triple for q=p-kappa*v."""
    Y = [
        [ONE, ZERO],
        [ZERO, ONE],
        [-ONE, KAPPA],
        [-ONE, ZERO],
        [ZERO, -ONE],
        [ONE, -KAPPA],
    ]
    adjacent_pairs = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0)]
    vertex_maps = [_vertex_map(Y, first, second) for first, second in adjacent_pairs]
    identity = [[F(row == column) for column in range(6)] for row in range(6)]
    configuration_rows = []
    for vertex_map in vertex_maps:
        product = _matmul(Y, vertex_map)
        for row in range(6):
            residual = [
                product[row][column] - identity[row][column]
                for column in range(6)
            ]
            if any(residual):
                configuration_rows.append(residual)
    return {
        "coordinate": "q = p - kappa * v",
        "kappa": KAPPA,
        "facet_order": ["+p", "+v", "-q", "-p", "-v", "+q"],
        "Y": Y,
        "adjacent_pairs": adjacent_pairs,
        "Lambda": vertex_maps,
        "G": configuration_rows,
    }


def _configuration_valid(position, velocity, slant):
    template = six_facet_template()
    offsets = [position, velocity, slant, position, velocity, slant]
    return all(
        sum(coefficient * offset for coefficient, offset in zip(row, offsets)) <= 0
        for row in template["G"]
    )


def canonical_measurement_support(position_cap, velocity_radius, slant_radius):
    """Return tight symmetric supports after intersecting with |p|<=position_cap."""
    if min(position_cap, velocity_radius, slant_radius) < 0:
        raise ValueError("support radii must be nonnegative")
    tight = {
        "position": min(position_cap, slant_radius + KAPPA * velocity_radius),
        "velocity": min(velocity_radius, (position_cap + slant_radius) / KAPPA),
        "slant": min(slant_radius, position_cap + KAPPA * velocity_radius),
    }
    return {
        "raw_offsets": {
            "position": position_cap,
            "velocity": velocity_radius,
            "slant": slant_radius,
        },
        "tight_supports": tight,
        "raw_configuration_valid": _configuration_valid(
            position_cap, velocity_radius, slant_radius
        ),
        "tight_configuration_valid": _configuration_valid(
            tight["position"], tight["velocity"], tight["slant"]
        ),
    }


def run():
    adapter = adapter_run()
    if F(5) * adapter["A"][0][1] != KAPPA:
        raise AssertionError("six-facet slope no longer matches the five-sample transport scale")
    position_before = adapter["tracking_error_box"]["position_halfwidth"]
    velocity = adapter["tracking_error_box"]["velocity_halfwidth"]
    slant_before = ONE
    measurement_cap = adapter["measurement_operators"]["success"]["noise_halfwidth"]
    posterior = canonical_measurement_support(measurement_cap, velocity, slant_before)
    tight = posterior["tight_supports"]
    pre_measurement_valid = _configuration_valid(
        position_before, velocity, slant_before
    )
    if not pre_measurement_valid:
        raise AssertionError("pre-measurement witness is outside the six-facet configuration cone")
    if not posterior["tight_configuration_valid"]:
        raise AssertionError("canonical posterior is outside the six-facet configuration cone")
    strict_reduction = slant_before - tight["slant"]
    if strict_reduction <= 0:
        raise AssertionError("expected active velocity facets to tighten the slant support")
    return {
        "claim": "active_velocity_facets_can_remove_the_unchanged_slant_measurement_obstruction",
        "evidence_level": "exact_six_facet_measurement_support_map",
        "template": six_facet_template(),
        "support_identity": {
            "position": "min(a, r_q + kappa*r_v)",
            "velocity": "min(r_v, (a + r_q)/kappa)",
            "slant": "min(r_q, a + kappa*r_v)",
        },
        "strict_measurement_witness": {
            "position_radius_before": position_before,
            "velocity_radius": velocity,
            "slant_support_before": slant_before,
            "measurement_position_cap": measurement_cap,
            "pre_measurement_configuration_valid": pre_measurement_valid,
            "raw_post_measurement_configuration_valid": posterior[
                "raw_configuration_valid"
            ],
            "canonical_post_measurement_configuration_valid": posterior[
                "tight_configuration_valid"
            ],
            "slant_support_after": tight["slant"],
            "strict_slant_reduction": strict_reduction,
        },
        "active_velocity_facets_can_tighten_slant_support": True,
        "graph_invariant_information_ensemble_certified": False,
        "center_reparameterization_certified": False,
        "input_feasibility_certified": False,
        "terminal_invariance_certified": False,
        "mpc_recursive_feasibility_certified": False,
        "full_six_state_guarantee": False,
        "limitations": [
            "the support identity is for one centrally symmetric six-facet set and a centered position strip",
            "measurement-dependent centers and the Z/H/Omega ensemble remain unconstructed",
            "the 15-mode/17-edge graph LP and shared current controls remain untested",
            "a local strict support reduction is not a closed-loop conservatism comparison",
        ],
    }


def _encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, list):
        return [_encode(item) for item in value]
    if isinstance(value, tuple):
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
        "verification/check_six_facet_measurement_gate.py",
        "verification/test_six_facet_measurement_gate.py",
        "verification/check_houska_vertical_adapter.py",
        "configs/planar_baseline.json",
        "docs/superpowers/specs/2026-10-27-six-facet-measurement-gate-design.md",
    ]
    result["source_sha256"] = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in sources
    }
    encoded = _encode(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(encoded, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "claim": encoded["claim"],
        "evidence_level": encoded["evidence_level"],
        "strict_slant_reduction": encoded["strict_measurement_witness"][
            "strict_slant_reduction"
        ],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
