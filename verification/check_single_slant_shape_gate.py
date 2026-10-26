#!/usr/bin/env python3
"""Exact shape-level gate for one position--velocity coupled normal pair."""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

from check_houska_vertical_adapter import run as adapter_run


ROOT = Path(__file__).resolve().parents[1]
ZERO = F(0)


def shape_recurrence():
    """Return the exact radius recurrence for q = p - kappa*v."""
    adapter = adapter_run()
    h = adapter["A"][0][1]
    kappa = F(5) * h
    mixing = h / kappa
    retained = F(1) - mixing
    disturbance = adapter["discrete_W_velocity_halfwidth"]
    signed_state = [
        [F(1) + mixing, -mixing],
        [mixing, retained],
    ]
    return {
        "coordinate": "q = p - kappa * v",
        "h": h,
        "kappa": kappa,
        "signed_state_matrix": signed_state,
        "signed_input_matrix": [[ZERO], [-kappa * h]],
        "radius_matrix": [[abs(value) for value in row] for row in signed_state],
        "radius_disturbance": [ZERO, kappa * disturbance],
        "velocity_disturbance_halfwidth": disturbance,
        "measurement_position_radius": adapter["measurement_operators"]["success"][
            "noise_halfwidth"
        ],
    }


def _step(radii, recurrence):
    matrix = recurrence["radius_matrix"]
    noise = recurrence["radius_disturbance"]
    return [
        sum(matrix[row][column] * radii[column] for column in range(2)) + noise[row]
        for row in range(2)
    ]


def _matmul(left, right):
    return [[
        sum(left[row][inner] * right[inner][column] for inner in range(len(right)))
        for column in range(len(right[0]))
    ] for row in range(len(left))]


def _matrix_power(matrix, exponent):
    result = [[F(1), ZERO], [ZERO, F(1)]]
    for _ in range(exponent):
        result = _matmul(result, matrix)
    return result


def return_obstruction():
    """Prove the unchanged-q success reset cannot close the 15-step return."""
    recurrence = shape_recurrence()
    power = _matrix_power(recurrence["radius_matrix"], 15)
    q_q_gain = power[1][1]
    return {
        "fifteen_step_radius_matrix": power,
        "fifteen_step_radius_matrix_q_q": q_q_gain,
        "coefficient_excess": q_q_gain - F(1),
        "positive_position_coefficient": power[1][0],
        "positive_measurement_position_radius": recurrence["measurement_position_radius"],
        "no_nonnegative_return_radius": q_q_gain > F(1),
        "reason": (
            "r_q(15)-R has positive coefficient on R, positive coefficient on nu, "
            "and nonnegative disturbance terms"
        ),
    }


def run():
    adapter = adapter_run()
    recurrence = shape_recurrence()
    kappa = recurrence["kappa"]
    nu = recurrence["measurement_position_radius"]
    radius_matrix = recurrence["radius_matrix"]
    success_return_checks = []
    for age in (5, 10, 15):
        power = _matrix_power(radius_matrix, age)
        success_return_checks.append({
            "prediction_age": age,
            "q_q_gain": power[1][1],
            "q_position_gain": power[1][0],
            "nonnegative_fixed_radius_possible": power[1][1] < F(1),
        })

    # Reproduce and reject the candidate archived before independent review.
    wrong_lambda = F(3, 5)
    wrong_return_radius = (
        nu + F(15) * kappa * recurrence["velocity_disturbance_halfwidth"]
        / (F(1) - wrong_lambda**15)
        + kappa * recurrence["velocity_disturbance_halfwidth"] / (F(1) - wrong_lambda)
    )
    wrong_first_target = [
        F(4, 5) * nu + F(1, 5) * wrong_return_radius,
        F(1, 5) * nu + F(4, 5) * wrong_return_radius
        + recurrence["radius_disturbance"][1],
    ]
    correct_radii = [nu, wrong_return_radius]
    rejected_predictions = []
    for age in range(1, 16):
        correct_radii = _step(correct_radii, recurrence)
        rejected_predictions.append({
            "age": age,
            "position_radius": correct_radii[0],
            "slant_radius": correct_radii[1],
            "derived_velocity_radius": sum(correct_radii) / kappa,
        })
    first_failed_success = next(
        age for age in (5, 10, 15)
        if rejected_predictions[age - 1]["slant_radius"] > wrong_return_radius
    )
    velocity_capacity = adapter["tracking_error_box"]["velocity_halfwidth"]
    obstruction = return_obstruction()
    if not obstruction["no_nonnegative_return_radius"]:
        raise AssertionError("expected the corrected 15-step q-radius obstruction")

    return {
        "claim": "fixed_slant_parallelogram_outer_recurrence_is_not_graph_invariant",
        "evidence_level": "exact_fixed_slant_parallelogram_shape_obstruction",
        "recurrence": recurrence,
        "return_obstruction": obstruction,
        "success_return_checks": success_return_checks,
        "periodic_shape_cycle_certified": False,
        "rejected_run185_candidate": {
            "initial_position_radius": nu,
            "initial_slant_radius": wrong_return_radius,
            "first_miss_position_underbound": (
                _step([nu, wrong_return_radius], recurrence)[0] - wrong_first_target[0]
            ),
            "first_failed_success_age": first_failed_success,
            "derived_velocity_radius_at_age_5": rejected_predictions[4][
                "derived_velocity_radius"
            ],
            "all_shape_radius_capacity_checks_pass": all(
                item["derived_velocity_radius"] <= velocity_capacity
                for item in rejected_predictions
            ),
        },
        "full_information_ensemble_certified": False,
        "center_dynamics_certified": False,
        "input_feasibility_certified": False,
        "mpc_recursive_feasibility_certified": False,
        "full_six_state_guarantee": False,
        "limitations": [
            "the obstruction applies to the fixed-orientation p/q parallelogram outer recurrence",
            "it does not reject a six-facet template that retains active velocity facets",
            "it does not reject rotating/mode-dependent facets or constrained zonotopes",
            "centers, controls, meta-ensembles, and terminal MPC remain open",
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
        "verification/check_single_slant_shape_gate.py",
        "verification/test_single_slant_shape_gate.py",
        "verification/check_houska_vertical_adapter.py",
        "configs/planar_baseline.json",
        "docs/superpowers/specs/2026-10-26-single-slant-shape-gate-design.md",
    ]
    result["source_sha256"] = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in sources
    }
    encoded = _encode(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(encoded, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "claim": encoded["claim"],
        "evidence_level": encoded["evidence_level"],
        "fifteen_step_q_q_gain": encoded["return_obstruction"][
            "fifteen_step_radius_matrix_q_q"
        ],
        "periodic_shape_cycle_certified": encoded["periodic_shape_cycle_certified"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
