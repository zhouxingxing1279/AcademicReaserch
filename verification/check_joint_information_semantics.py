#!/usr/bin/env python3
"""Exact semantic checks for the vertical joint information-set contract."""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

from check_cycle_lifted_zonotope import (
    age_zonotopes,
    least_mode_zero_box,
    lift_cycle,
    problem_data,
)


ROOT = Path(__file__).resolve().parents[1]
H = F(1, 50)
POSITION_GAIN = F(9, 2)
PRODUCT_THRESHOLD = F(57902137, 162000000)


def miss_path_fiber_certificate():
    """Certify the unavoidable mode-14 fiber from the required initialization."""
    _, A0, G0, A1, G1, _ = problem_data()
    cycles = [lift_cycle(length, A0, G0, A1, G1) for length in (5, 10, 15)]
    mode14 = age_zonotopes(least_mode_zero_box(cycles), A0, G0)[14]
    conditional_q_halfwidth = sum(
        abs(mode14[1][column] + H * mode14[3][column])
        for column in range(len(mode14[0]))
    )
    strict_excess = conditional_q_halfwidth - PRODUCT_THRESHOLD
    assert conditional_q_halfwidth == F(23312147, 48000000)
    assert strict_excess == F(166210873, 1296000000)

    # On a miss edge, d+ = [[1,h],[0,1]] d + [0,h] deltaT.
    # It contains neither hidden eta nor the physical residual primitive.
    same_observation_for_entire_fiber = True
    return {
        "conditional_q_halfwidth": conditional_q_halfwidth,
        "product_threshold": PRODUCT_THRESHOLD,
        "strict_excess": strict_excess,
        "same_observation_for_entire_fiber": same_observation_for_entire_fiber,
        "threshold_is_reachable_on_initial_miss_path": conditional_q_halfwidth <= PRODUCT_THRESHOLD,
    }


def success_velocity_split(
    eta_position,
    eta_velocity,
    d_velocity,
    correction_thrust,
    residual,
    measurement_noise,
):
    """Apply one success update while keeping the shared primitive unsplit."""
    eta_position = F(eta_position)
    eta_velocity = F(eta_velocity)
    d_velocity = F(d_velocity)
    correction_thrust = F(correction_thrust)
    residual = F(residual)
    measurement_noise = F(measurement_noise)
    q = eta_position + H * eta_velocity
    innovation = q + measurement_noise
    eta_velocity_next = eta_velocity + H * residual - POSITION_GAIN * innovation
    d_velocity_next = d_velocity + H * correction_thrust + POSITION_GAIN * innovation
    tracking_velocity_next = eta_velocity_next + d_velocity_next
    assert tracking_velocity_next == (
        eta_velocity + d_velocity + H * (residual + correction_thrust)
    )
    return {
        "q": q,
        "eta_velocity_next": eta_velocity_next,
        "d_velocity_next": d_velocity_next,
        "tracking_velocity_next": tracking_velocity_next,
    }


def joint_target_counterexample():
    """Refute treating the Run142 product threshold as joint necessity.

    The source is an actual member of the mode-14 zonotope attaining the
    positive ``q`` support.  A successful measurement with positive extremal
    noise is propagated through the current Run136 matrix.  Although the
    resulting visible ``d_v`` exceeds every admissible product target, the
    correlated pair ``(eta_v, d_v)`` has an admissible tracking error
    ``e_v = eta_v + d_v``.
    """
    config, A0, G0, A1, G1, _ = problem_data()
    cycles = [lift_cycle(length, A0, G0, A1, G1) for length in (5, 10, 15)]
    mode_zero_box = least_mode_zero_box(cycles)
    mode14 = age_zonotopes(mode_zero_box, A0, G0)[14]
    q_columns = [
        mode14[1][column] + H * mode14[3][column]
        for column in range(len(mode14[0]))
    ]
    coefficients = [
        F(1) if value > 0 else F(-1) if value < 0 else F(0)
        for value in q_columns
    ]
    eta = [
        sum(row[column] * coefficients[column] for column in range(len(row)))
        for row in mode14
    ]
    q = eta[1] + H * eta[3]

    # G1 already contains the configured halfwidths.  Primitive 4 is the
    # next vertical position-noise primitive; all physical residuals are set
    # to zero, which is admissible in their symmetric boxes.
    primitives = [F(0)] * len(G1[0])
    primitives[4] = F(1)
    eta_next = [
        sum(A1[row][column] * eta[column] for column in range(len(A1)))
        + sum(G1[row][column] * primitives[column]
              for column in range(len(primitives)))
        for row in range(len(A1))
    ]

    noise = config["sensing"]["observed_noise_halfwidth"]["pz"]
    d_position_next = q + noise
    d_velocity_next = POSITION_GAIN * (q + noise)
    tracking_position_next = eta_next[1] + d_position_next
    tracking_velocity_next = eta_next[3] + d_velocity_next

    nominal = config["mpc"]["ancillary_rci_contract"]["nominal_state_domain"]
    tracking_position_limit = min(
        config["domain"]["state_upper"][1] - nominal["upper"][1],
        nominal["lower"][1] - config["domain"]["state_lower"][1],
    )
    tracking_velocity_limit = min(
        config["domain"]["state_upper"][3] - nominal["upper"][3],
        nominal["lower"][3] - config["domain"]["state_lower"][3],
    )
    product_d_velocity_limit = tracking_velocity_limit - mode_zero_box[3]

    eta_target_in_mode0_box = all(
        abs(value) <= halfwidth
        for value, halfwidth in zip(eta_next, mode_zero_box)
    )
    tracking_target_in_source_domain = (
        abs(tracking_position_next) <= tracking_position_limit
        and abs(tracking_velocity_next) <= tracking_velocity_limit
    )
    product_threshold_not_joint_necessary = (
        q > PRODUCT_THRESHOLD
        and abs(d_velocity_next) > product_d_velocity_limit
        and eta_target_in_mode0_box
        and tracking_target_in_source_domain
    )
    if not product_threshold_not_joint_necessary:
        raise AssertionError("joint-target counterexample did not close")
    return {
        "q": q,
        "noise": noise,
        "eta_source": eta,
        "eta_target": eta_next,
        "eta_position_next": eta_next[1],
        "eta_velocity_next": eta_next[3],
        "d_position_next": d_position_next,
        "d_velocity_next": d_velocity_next,
        "tracking_position_next": tracking_position_next,
        "tracking_velocity_next": tracking_velocity_next,
        "product_q_threshold": PRODUCT_THRESHOLD,
        "product_d_velocity_limit": product_d_velocity_limit,
        "tracking_position_limit": tracking_position_limit,
        "tracking_velocity_limit": tracking_velocity_limit,
        "q_product_threshold_violated": q > PRODUCT_THRESHOLD,
        "product_d_velocity_limit_violated": (
            abs(d_velocity_next) > product_d_velocity_limit
        ),
        "eta_target_in_mode0_box": eta_target_in_mode0_box,
        "tracking_target_in_source_domain": tracking_target_in_source_domain,
        "product_threshold_not_joint_necessary": (
            product_threshold_not_joint_necessary
        ),
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


def run():
    miss_path = miss_path_fiber_certificate()
    witness = joint_target_counterexample()
    return {
        "status": "pass",
        "claim": "run142_product_threshold_is_not_necessary_for_a_joint_information_target",
        "miss_path_fiber": miss_path,
        "joint_target_counterexample": witness,
        "evidence_level": (
            "exact_counterexample_to_product_threshold_as_joint_necessity"
        ),
        "correct_joint_coordinates": [
            "eta_pz", "eta_vz", "e_pz=eta_pz+d_pz", "e_vz=eta_vz+d_vz"
        ],
        "limitations": [
            "the witness corrects a necessary-condition error; it is not an invariant-set certificate",
            "no four-dimensional joint predecessor or causal RCI is synthesized",
            "horizontal and attitude coordinates are not analyzed beyond mode-zero containment",
            "terminal ingredients and recursive MPC feasibility remain open",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    result = run()
    sources = [
        "verification/check_joint_information_semantics.py",
        "verification/test_joint_information_semantics.py",
        "verification/check_cycle_lifted_zonotope.py",
        "verification/check_vertical_causal_predecessor.py",
        "configs/planar_baseline.json",
        "docs/learning/80_joint_information_coordinate_correction.md",
        "docs/research/run143_literature_gate.md",
        "docs/research/run143_research_log.md",
    ]
    result["source_sha256"] = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in sources
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(_encode(result), ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps({
        "status": result["status"],
        "claim": result["claim"],
        "mode14_q_halfwidth": str(
            result["miss_path_fiber"]["conditional_q_halfwidth"]
        ),
        "product_threshold": str(
            result["miss_path_fiber"]["product_threshold"]
        ),
        "joint_counterexample": result["joint_target_counterexample"][
            "product_threshold_not_joint_necessary"
        ],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
