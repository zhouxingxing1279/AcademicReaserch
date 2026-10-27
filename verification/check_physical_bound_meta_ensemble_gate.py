#!/usr/bin/env python3
"""Exact gate for the physical-containment-only six-offset meta ensemble."""
from __future__ import annotations

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

from check_houska_vertical_adapter import run as adapter_run
from check_six_facet_measurement_gate import six_facet_template


ROOT = Path(__file__).resolve().parents[1]


def _matvec(matrix, vector):
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]


def physical_support_vector():
    """Return exact supports of the certified tracking-error box in template directions."""
    adapter = adapter_run()
    p = adapter["tracking_error_box"]["position_halfwidth"]
    v = adapter["tracking_error_box"]["velocity_halfwidth"]
    kappa = six_facet_template()["kappa"]
    return [p, v, p + kappa * v, p, v, p + kappa * v]


def run():
    template = six_facet_template()
    adapter = adapter_run()
    p = adapter["tracking_error_box"]["position_halfwidth"]
    v = adapter["tracking_error_box"]["velocity_halfwidth"]
    if (p, v) != (F(1), F(11, 4)):
        raise AssertionError("certified physical tracking-error box changed")

    dominating = physical_support_vector()
    if dominating != [F(1), F(11, 4), F(51, 40), F(1), F(11, 4), F(51, 40)]:
        raise AssertionError("physical support vector changed")
    margins = _matvec(template["G"], dominating)
    if max(margins) != 0:
        raise AssertionError("physical box offsets left the six-facet configuration cone")

    mapped_vertices = [tuple(_matvec(vertex_map, dominating)) for vertex_map in template["Lambda"]]
    unique_vertices = sorted({vertex for vertex in mapped_vertices})
    box_vertices = sorted({(-p, -v), (-p, v), (p, -v), (p, v)})
    if unique_vertices != box_vertices:
        raise AssertionError("dominating six-facet polytope is not the physical box")

    # If P(y) is physically admissible, P(y) is a subset of X by definition.
    # Support monotonicity then gives y_i=h_P(Y_i)<=h_X(Y_i)=dominating_i
    # for the tight configured representation. Thus P(dominating)=X contains
    # every admissible P(y), making X the unique extreme set of the ensemble.
    return {
        "claim": "physical_containment_only_collapses_to_one_extreme_information_set",
        "evidence_level": "exact_physical_bound_meta_ensemble_singleton_extreme_set",
        "facet_order": template["facet_order"],
        "physical_position_halfwidth": p,
        "physical_velocity_halfwidth": v,
        "physical_support_offsets": dominating,
        "configuration_max_margin": max(margins),
        "dominating_offsets_in_configuration_cone": True,
        "configured_vertex_set": [list(vertex) for vertex in unique_vertices],
        "physical_box_equals_dominating_polytope": True,
        "domination_argument": "P(y) subseteq X implies h_P(Y_i) <= h_X(Y_i) componentwise",
        "all_admissible_sets_contained_in_extreme_set": True,
        "extreme_set_count": 1,
        "extreme_set_offsets": [dominating],
        "physical_only_meta_domain_useful_for_online_information": False,
        "variable_H_Omega_family_certified": False,
        "graph_invariant_information_ensemble_certified": False,
        "mpc_recursive_feasibility_certified": False,
        "full_six_state_guarantee": False,
        "limitations": [
            "the result concerns only the meta domain defined by physical containment",
            "no additional information-conditioned shape or center constraints are selected",
            "no variable H/Omega family or mode-graph propagation is constructed",
            "the result is a representation stopping certificate, not a controller theorem",
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
        "verification/check_physical_bound_meta_ensemble_gate.py",
        "verification/test_physical_bound_meta_ensemble_gate.py",
        "verification/check_six_facet_measurement_gate.py",
        "verification/check_houska_vertical_adapter.py",
        "configs/planar_baseline.json",
        "docs/superpowers/specs/2026-10-27-physical-bound-meta-ensemble-gate-design.md",
    ]
    result["source_sha256"] = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in sources
    }
    encoded = _encode(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(encoded, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "evidence_level": encoded["evidence_level"],
        "extreme_set_count": encoded["extreme_set_count"],
        "physical_support_offsets": encoded["physical_support_offsets"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
