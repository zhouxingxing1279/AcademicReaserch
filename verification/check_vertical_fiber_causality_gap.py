#!/usr/bin/env python3
"""Exact causal/full-state predecessor gap on the vertical mode-4 fiber.

This is deliberately a one-step negative control for later RCI synthesis.
It does not construct an invariant set.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

from check_cycle_lifted_zonotope import (
    CYCLE_LENGTHS,
    age_zonotopes,
    least_mode_zero_box,
    lift_cycle,
    problem_data,
)


ROOT = Path(__file__).resolve().parents[1]
H = F(1, 50)
POSITION_GAIN = F(9, 2)
SUCCESS_VELOCITY_TARGET = F(13, 20)
MISS_VELOCITY_TARGET = F(7, 100)


def audit_model_constants(config, success_matrix):
    """Bind the reduced formulas to the current plant and Run136 edge map."""
    assert config["plant"]["dt_s"] == H
    assert config["sensing"]["observed_noise_halfwidth"]["pz"] == F(1, 50)
    assert success_matrix[3][1] == -POSITION_GAIN
    assert success_matrix[3][3] == 1 - POSITION_GAIN * H


def _mode_four_zonotope():
    _, A0, G0, A1, G1, _ = problem_data()
    cycles = [lift_cycle(length, A0, G0, A1, G1) for length in CYCLE_LENGTHS]
    mode_zero_box = least_mode_zero_box(cycles)
    return age_zonotopes(mode_zero_box, A0, G0)[4]


def mode_four_q_support():
    """Return exact support of eta_pz + h eta_vz and an attaining member."""
    mode_four = _mode_four_zonotope()
    direction_columns = [
        mode_four[1][column] + H * mode_four[3][column]
        for column in range(len(mode_four[0]))
    ]
    coefficients = [F(1) if value >= 0 else F(-1) for value in direction_columns]
    witness = [
        sum(row[column] * coefficients[column] for column in range(len(row)))
        for row in mode_four
    ]
    support = sum(abs(value) for value in direction_columns)
    assert witness[1] + H * witness[3] == support
    return support, witness


def run():
    config = json.loads((ROOT / "configs/planar_baseline.json").read_text(), parse_float=F)
    _, _, _, success_matrix, _, _ = problem_data()
    audit_model_constants(config, success_matrix)
    q_support, witness = mode_four_q_support()
    mode_four = _mode_four_zonotope()
    noise_width = config["sensing"]["observed_noise_halfwidth"]["pz"]
    correction_lower = config["mpc"]["ancillary_correction_lower"][0]
    correction_upper = config["mpc"]["ancillary_correction_upper"][0]
    correction_limit = min(-correction_lower, correction_upper)
    nominal_thrust = config["plant"]["gravity_m_s2"]
    actuator_lower = config["domain"]["input_lower"][0]
    actuator_upper = config["domain"]["input_upper"][0]

    hidden_contribution = POSITION_GAIN * q_support
    future_noise_contribution = POSITION_GAIN * noise_width
    causal_required_radius = hidden_contribution + future_noise_contribution
    success_position_target = q_support + noise_width
    required_extreme_correction = (
        causal_required_radius - SUCCESS_VELOCITY_TARGET
    ) / H

    full_success_radius = (
        hidden_contribution
        - H * required_extreme_correction
        + future_noise_contribution
    )
    full_miss_radius = H * required_extreme_correction
    actual_thrusts = [
        nominal_thrust - required_extreme_correction,
        nominal_thrust + required_extreme_correction,
    ]
    edge_vertex_checks = []
    for q_sign in (F(-1), F(1)):
        q = q_sign * q_support
        correction = -(required_extreme_correction / q_support) * q
        actual_thrust = nominal_thrust + correction
        miss_position_image = F(0)
        miss_image = H * correction
        miss_position_ok = miss_position_image == 0
        miss_velocity_ok = abs(miss_image) <= MISS_VELOCITY_TARGET
        edge_vertex_checks.append({
            "edge": "miss_to_5",
            "q": q,
            "noise": None,
            "correction": correction,
            "image_d_pz": miss_position_image,
            "image_d_vz": miss_image,
            "position_target_ok": miss_position_ok,
            "velocity_target_ok": miss_velocity_ok,
            "target_ok": miss_position_ok and miss_velocity_ok,
            "input_ok": actuator_lower <= actual_thrust <= actuator_upper,
        })
        for noise_sign in (F(-1), F(1)):
            noise = noise_sign * noise_width
            success_position_image = q + noise
            success_image = H * correction + POSITION_GAIN * (q + noise)
            success_position_ok = abs(success_position_image) <= success_position_target
            success_velocity_ok = abs(success_image) <= SUCCESS_VELOCITY_TARGET
            edge_vertex_checks.append({
                "edge": "success_to_0",
                "q": q,
                "noise": noise,
                "correction": correction,
                "image_d_pz": success_position_image,
                "image_d_vz": success_image,
                "position_target_ok": success_position_ok,
                "velocity_target_ok": success_velocity_ok,
                "target_ok": success_position_ok and success_velocity_ok,
                "input_ok": actuator_lower <= actual_thrust <= actuator_upper,
            })

    success_lower = required_extreme_correction
    success_upper = -required_extreme_correction
    miss_lower = -MISS_VELOCITY_TARGET / H
    miss_upper = MISS_VELOCITY_TARGET / H
    required_lower = max(success_lower, miss_lower, correction_lower)
    required_upper = min(success_upper, miss_upper, correction_upper)

    state_lower = config["domain"]["state_lower"]
    state_upper = config["domain"]["state_upper"]
    hover = [F(0), F(2), F(0), F(0), F(0), F(0)]
    coordinate_supports = [sum(abs(value) for value in row) for row in mode_four]
    lower_slacks = [
        z - radius - lo
        for lo, z, radius in zip(state_lower, hover, coordinate_supports)
    ]
    upper_slacks = [
        hi - z - radius
        for z, radius, hi in zip(hover, coordinate_supports, state_upper)
    ]
    source_domain_ok = all(value > 0 for value in lower_slacks + upper_slacks)

    full = {
        "policy": "delta_T(q) = -(required_extreme_correction / q_support) * q",
        "required_extreme_correction": required_extreme_correction,
        "correction_authority": correction_limit,
        "correction_authority_ok": required_extreme_correction <= correction_limit,
        "miss_image_velocity_radius": full_miss_radius,
        "miss_target_radius": MISS_VELOCITY_TARGET,
        "miss_target_ok": full_miss_radius <= MISS_VELOCITY_TARGET,
        "success_image_velocity_radius": full_success_radius,
        "success_target_radius": SUCCESS_VELOCITY_TARGET,
        "success_target_ok": full_success_radius <= SUCCESS_VELOCITY_TARGET,
        "actual_thrusts_at_hidden_extremes": actual_thrusts,
        "actuator_box_ok": all(actuator_lower <= value <= actuator_upper
                               for value in actual_thrusts),
    }
    causal = {
        "same_observation": {"mode": 4, "d_pz": F(0), "d_vz": F(0)},
        "positive_hidden_state_requires_delta_T_at_most": success_upper,
        "negative_hidden_state_requires_delta_T_at_least": success_lower,
        "required_lower": required_lower,
        "required_upper": required_upper,
        "common_control_exists": required_lower <= required_upper,
    }

    assert q_support == F(1004143, 7200000)
    assert required_extreme_correction == F(108143, 32000)
    assert source_domain_ok
    assert all(full[key] for key in (
        "correction_authority_ok", "miss_target_ok", "success_target_ok",
        "actuator_box_ok",
    ))
    assert len(edge_vertex_checks) == 6
    assert all(row["target_ok"] and row["input_ok"] for row in edge_vertex_checks)
    assert not causal["common_control_exists"]

    return {
        "status": "pass",
        "claim": "strict_actual_model_observation_fiber_predecessor_gap",
        "mode": 4,
        "unknown_successors": ["miss_to_5", "success_to_0"],
        "q_support": q_support,
        "q_support_witness_eta": witness,
        "position_target_radius_on_success": success_position_target,
        "source_domain_ok": source_domain_ok,
        "source_fiber_domain": {
            "coordinate_supports": coordinate_supports,
            "lower_slacks": lower_slacks,
            "upper_slacks": upper_slacks,
            "entire_fiber_inside": source_domain_ok,
        },
        "edge_vertex_checks": edge_vertex_checks,
        "full_state_fiber_policy": full,
        "causal_observation_fiber": causal,
        "strict_gap": {
            "causal_minimum_success_velocity_radius": causal_required_radius,
            "full_state_minimum_with_input_saturation": max(
                future_noise_contribution,
                causal_required_radius - H * correction_limit,
            ),
            "chosen_success_velocity_radius": SUCCESS_VELOCITY_TARGET,
        },
        "evidence_level": "exact_one_step_counterexample_not_an_rci_certificate",
        "limitations": [
            "does not construct a mode-indexed invariant set",
            "does not prove causal vertical RCI infeasibility",
            "does not cover the horizontal or attitude coordinates",
            "the full-state policy is deliberately noncausal for the real controller",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output)
    if output.exists():
        raise FileExistsError(output)
    result = run()
    sources = [
        "verification/check_vertical_fiber_causality_gap.py",
        "verification/test_vertical_fiber_causality_gap.py",
        "verification/check_cycle_lifted_zonotope.py",
        "configs/planar_baseline.json",
        "docs/research/run141_literature_gate.md",
    ]
    result["source_sha256"] = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in sources
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, default=str) + "\n")
    print(json.dumps({
        "status": result["status"],
        "claim": result["claim"],
        "q_support": str(result["q_support"]),
        "required_full_state_extreme_correction": str(
            result["full_state_fiber_policy"]["required_extreme_correction"]),
        "causal_common_control_exists": result["causal_observation_fiber"][
            "common_control_exists"],
    }, indent=2))


if __name__ == "__main__":
    main()
