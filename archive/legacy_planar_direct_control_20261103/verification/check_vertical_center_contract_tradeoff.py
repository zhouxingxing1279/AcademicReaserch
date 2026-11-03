#!/usr/bin/env python3
"""Exact three-factor contract needed to remove the Run165 center obstruction."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

from check_cycle_lifted_zonotope import problem_data
from check_vertical_correlated_return_seed import correlated_return_seed


H = F(1, 50)
MISS_COUNT = 14
POSITION_LIMIT = F(1)
ROOT = Path(__file__).resolve().parents[1]


def center_contract_certificate():
    config, _, miss_generators, _, _, _ = problem_data()
    rows = correlated_return_seed()["return_seed"]["generators_by_row"]
    visible = [rows[2][i] - rows[0][i] for i in range(len(rows[0]))]
    endpoint = [
        rows[2][i] + MISS_COUNT * H * rows[3][i]
        for i in range(len(rows[0]))
    ]

    slope = F(29, 15)
    visible_radius = sum((abs(value) for value in visible), F(0))
    affine_intercept = sum(
        (abs(value - slope * observation)
         for value, observation in zip(endpoint, visible)),
        F(0),
    )
    fixed_subgradient = sum(
        (observation * (F(1) if value - slope * observation > 0 else F(-1))
         for value, observation in zip(endpoint, visible)
         if value - slope * observation != 0),
        F(0),
    )
    free_subgradient_radius = sum(
        (abs(observation)
         for value, observation in zip(endpoint, visible)
         if value - slope * observation == 0),
        F(0),
    )
    affine_branch_max = fixed_subgradient + free_subgradient_radius

    residual_halfwidth = miss_generators[3][1]
    correction_limit = F(str(config["mpc"]["ancillary_correction_upper"][0]))
    triangular = F(MISS_COUNT * (MISS_COUNT - 1), 2)
    residual_budget = triangular * H * residual_halfwidth
    correction_budget = triangular * H * H * correction_limit
    current_endpoint = sum((abs(value) for value in endpoint), F(0))

    visible_radius_max = (POSITION_LIMIT - affine_intercept) / slope
    residual_scale_max = (
        POSITION_LIMIT - current_endpoint + correction_budget
    ) / residual_budget
    authority_scale_min = (
        current_endpoint + residual_budget - POSITION_LIMIT
    ) / correction_budget

    visible_only = affine_intercept + slope * visible_radius_max
    residual_only = current_endpoint + residual_scale_max * residual_budget - correction_budget
    authority_only = current_endpoint + residual_budget - authority_scale_min * correction_budget

    if not (
        affine_intercept == F(16315003, 75000000)
        and visible_radius == F(24272147, 48000000)
        and affine_branch_max == F(20432147, 48000000)
        and visible_radius_max <= affine_branch_max
        and residual_budget == correction_budget == F(52065013, 400000000)
        and current_endpoint == F(3889781459, 3600000000)
        and visible_radius_max == F(58684997, 145000000)
        and residual_scale_max == F(16254878, 42598647)
        and authority_scale_min == F(68942416, 42598647)
        and visible_only == residual_only == authority_only == POSITION_LIMIT
    ):
        raise AssertionError("vertical center-contract certificate changed")

    return {
        "conditional_initial_support": {
            "visible_coordinate": "d_p=e_p-eta_p",
            "endpoint_direction": "e_p+14h*e_v",
            "formula": "b + lambda*r",
            "visible_slope": slope,
            "affine_intercept": affine_intercept,
            "affine_branch_range": [F(0), affine_branch_max],
            "primal_attainment_on_affine_branch": True,
            "dual_upper_bound_on_affine_branch": True,
        },
        "three_factor_contract": {
            "condition": "b + lambda*r + beta*D - gamma*C <= 1",
            "visible_radius": "r",
            "future_residual_scale": "beta",
            "correction_authority_scale": "gamma",
            "residual_budget": residual_budget,
            "correction_budget": correction_budget,
        },
        "single_factor_thresholds": {
            "visible_radius_max": visible_radius_max,
            "future_residual_scale_max": residual_scale_max,
            "correction_authority_scale_min": authority_scale_min,
        },
        "boundary_checks": {
            "current_contract_endpoint": current_endpoint,
            "visible_only_endpoint": visible_only,
            "residual_only_endpoint": residual_only,
            "authority_only_endpoint": authority_only,
        },
    }


def run():
    return {
        "status": "pass",
        "claim": "exact_visible_center_residual_authority_tradeoff",
        **center_contract_certificate(),
        "is_necessary_for_current_four_state_path": True,
        "is_recursive_feasibility_proof": False,
        "is_full_six_state_guarantee": False,
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
        "verification/check_vertical_center_contract_tradeoff.py",
        "verification/test_vertical_center_contract_tradeoff.py",
        "verification/check_vertical_extreme_visible_fiber_obstruction.py",
        "verification/check_vertical_correlated_return_seed.py",
        "verification/check_cycle_lifted_zonotope.py",
        "configs/planar_baseline.json",
        "docs/learning/102_vertical_center_contract_tradeoff.md",
        "docs/literature/READ_PAPERS.md",
        "docs/research/run166_literature_gate.md",
        "docs/research/run166_research_log.md",
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
