#!/usr/bin/env python3
"""Exact worst conditional J14 width after observing the visible offset."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

from check_vertical_correlated_return_seed import correlated_return_seed


H = F(1, 50)
MISS_COUNT = 14
ROOT = Path(__file__).resolve().parents[1]


def _sign(value):
    return F(1) if value > 0 else F(-1) if value < 0 else F(0)


def _one_equality_box_support(direction, equality):
    """Certify max direction*z subject to equality*z=0 and |z|<=1."""
    weighted_ratios = sorted(
        (direction[i] / equality[i], abs(equality[i]), i)
        for i in range(len(direction))
        if equality[i]
    )
    total_weight = sum((weight for _, weight, _ in weighted_ratios), F(0))
    cumulative = F(0)
    for dual_lambda, weight, pivot in weighted_ratios:
        cumulative += weight
        if 2 * cumulative >= total_weight:
            break

    witness = [
        _sign(coefficient - dual_lambda * constraint)
        for coefficient, constraint in zip(direction, equality)
    ]
    nonpivot_residual = sum(
        (constraint * witness[i] for i, constraint in enumerate(equality) if i != pivot),
        F(0),
    )
    witness[pivot] = -nonpivot_residual / equality[pivot]
    primal = sum((coefficient * value for coefficient, value in zip(direction, witness)), F(0))
    dual = sum(
        (abs(coefficient - dual_lambda * constraint)
         for coefficient, constraint in zip(direction, equality)),
        F(0),
    )
    residual = sum(
        (constraint * value for constraint, value in zip(equality, witness)), F(0)
    )
    return {
        "primal_witness": witness,
        "visible_equality_residual": residual,
        "box_feasible": all(abs(value) <= 1 for value in witness),
        "primal_objective": primal,
        "dual_lambda": dual_lambda,
        "dual_objective": dual,
        "fractional_pivot_index": pivot,
        "fractional_pivot_value": witness[pivot],
    }


def visible_fiber_width_certificate():
    rows = correlated_return_seed()["return_seed"]["generators_by_row"]
    visible = [
        rows[2][column] - rows[0][column]
        for column in range(len(rows[0]))
    ]
    direction = [
        rows[2][column] + MISS_COUNT * H * rows[3][column]
        for column in range(len(rows[0]))
    ]
    certificate = _one_equality_box_support(direction, visible)
    unconditional = sum((abs(value) for value in direction), F(0))
    conditional = certificate["primal_objective"]
    if not (
        certificate["box_feasible"]
        and certificate["visible_equality_residual"] == 0
        and certificate["primal_objective"] == certificate["dual_objective"]
        and conditional < 1 < unconditional
    ):
        raise AssertionError("visible-fiber certificate changed")
    return {
        "coordinates": ("eta_p", "eta_v", "e_p", "e_v"),
        "visible_coordinate": "d_p=e_p-eta_p",
        "dependent_visible_coordinate": "d_v=(103/100)d_p",
        "tested_direction": "e_p+14h*e_v",
        "fiber_lp_certificate": certificate,
        "comparison": {
            "unconditional_direction_halfwidth": unconditional,
            "worst_visible_fiber_halfwidth": conditional,
            "conditioning_reduction": unconditional - conditional,
        },
    }


def run():
    result = visible_fiber_width_certificate()
    return {
        "status": "pass",
        "claim": "exact_worst_visible_fiber_directional_halfwidth",
        **result,
        "all_visible_fibers_pass_unit_seed_gate": True,
        "old_unconditional_gate_is_necessary_for_conditioned_policy": False,
        "is_recursive_feasibility_proof": False,
        "is_fifteen_tick_safety_proof": False,
        "full_six_state_guarantee": False,
    }


def _encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _encode(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_encode(item) for item in value]
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    result = run()
    sources = [
        "verification/check_vertical_visible_fiber_width.py",
        "verification/test_vertical_visible_fiber_width.py",
        "verification/check_vertical_correlated_return_seed.py",
        "configs/planar_baseline.json",
        "docs/learning/100_vertical_visible_fiber_seed_gate.md",
        "docs/literature/READ_PAPERS.md",
        "docs/research/run164_literature_gate.md",
        "docs/research/run164_research_log.md",
    ]
    result["source_sha256"] = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in sources
    }
    encoded = _encode(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(encoded, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": encoded["status"], "claim": encoded["claim"]}, indent=2))


if __name__ == "__main__":
    main()
