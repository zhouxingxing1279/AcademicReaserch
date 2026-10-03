#!/usr/bin/env python3
"""Exact vertical split between control translations and residual shape.

For a fixed absolute physical residual set, correction thrust enters the
vertical ``(eta, e)`` information dynamics only through a translation of the
true tracking-error coordinates.  The repository's tighter residual model,
however, scales one shared normalized primitive by the actual thrust.  That
scaling changes the joint ``(eta, e)`` generator and is therefore a
decision-dependent uncertainty effect, not a pure translation.

This checker certifies the interface distinction.  It does not synthesize an
invariant set or controller.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path
import sys


VERIFICATION_DIR = Path(__file__).resolve().parent
if str(VERIFICATION_DIR) not in sys.path:
    sys.path.insert(0, str(VERIFICATION_DIR))

from check_cycle_lifted_zonotope import problem_data
from check_vertical_joint_predecessor import H, POSITION_GAIN


ROOT = Path(__file__).resolve().parents[1]


def scheduled_residual_width(actual_thrust):
    return F(1043, 500) + F(81, 800) * F(actual_thrust)


def scheduled_residual_generator(actual_thrust):
    """Shared ``rho_z`` column in ``(eta_p, eta_v, e_p, e_v)``."""
    step = H * scheduled_residual_width(actual_thrust)
    return F(0), step, F(0), step


def vertical_edge_update(label, eta, visible_offset, correction_thrust,
                         physical_residual, measurement_noise=F(0)):
    """One exact vertical edge with one shared physical residual realization."""
    if label not in {"miss", "success"}:
        raise ValueError(f"unknown edge label: {label}")
    eta_p, eta_v = map(F, eta)
    d_p, d_v = map(F, visible_offset)
    correction = F(correction_thrust)
    residual = F(physical_residual)
    noise = F(measurement_noise)
    e_p, e_v = eta_p + d_p, eta_v + d_v

    e_next = (
        e_p + H * e_v,
        e_v + H * (correction + residual),
    )
    if label == "miss":
        eta_next = (
            eta_p + H * eta_v,
            eta_v + H * residual,
        )
        d_next = (
            d_p + H * d_v,
            d_v + H * correction,
        )
    else:
        innovation = eta_p + H * eta_v + noise
        eta_next = (
            -noise,
            eta_v + H * residual - POSITION_GAIN * innovation,
        )
        d_next = (
            e_p + H * e_v + noise,
            d_v + H * correction + POSITION_GAIN * innovation,
        )

    split_identity = all(
        eta_value + d_value == e_value
        for eta_value, d_value, e_value in zip(eta_next, d_next, e_next)
    )
    return {
        "label": label,
        "eta_next": eta_next,
        "visible_offset_next": d_next,
        "tracking_error_next": e_next,
        "split_identity_holds": split_identity,
    }


def _difference(second, first):
    return tuple(b - a for a, b in zip(first, second))


def compare_corrections_with_fixed_residual(
        label, eta, visible_offset, first_correction, second_correction,
        physical_residual, measurement_noise=F(0)):
    first = vertical_edge_update(
        label, eta, visible_offset, first_correction,
        physical_residual, measurement_noise,
    )
    second = vertical_edge_update(
        label, eta, visible_offset, second_correction,
        physical_residual, measurement_noise,
    )
    eta_translation = _difference(second["eta_next"], first["eta_next"])
    d_translation = _difference(
        second["visible_offset_next"], first["visible_offset_next"]
    )
    e_translation = _difference(
        second["tracking_error_next"], first["tracking_error_next"]
    )
    correction_difference = F(second_correction) - F(first_correction)
    expected = (F(0), H * correction_difference)
    return {
        "label": label,
        "correction_difference": correction_difference,
        "eta_translation": eta_translation,
        "visible_offset_translation": d_translation,
        "tracking_error_translation": e_translation,
        "expected_control_translation": expected,
        "shape_unchanged_for_fixed_residual_set": (
            eta_translation == (F(0), F(0))
            and d_translation == expected
            and e_translation == expected
        ),
    }


def control_translation_certificate():
    config, _, _, _, success_generators, _ = problem_data()
    nominal_lower = F(config["mpc"]["nominal_input_lower"][0])
    nominal_upper = F(config["mpc"]["nominal_input_upper"][0])
    correction_lower = F(config["mpc"]["ancillary_correction_lower"][0])
    correction_upper = F(config["mpc"]["ancillary_correction_upper"][0])
    actual_lower = nominal_lower + correction_lower
    actual_upper = nominal_upper + correction_upper
    actuator_lower = F(config["domain"]["input_lower"][0])
    actuator_upper = F(config["domain"]["input_upper"][0])
    lower_width = scheduled_residual_width(actual_lower)
    upper_width = scheduled_residual_width(actual_upper)
    lower_column = scheduled_residual_generator(actual_lower)
    upper_column = scheduled_residual_generator(actual_upper)
    column_increase = tuple(
        high - low for low, high in zip(lower_column, upper_column)
    )
    run136_step_column = success_generators[3][1]

    fixed_residual = upper_width
    translation_checks = {
        label: compare_corrections_with_fixed_residual(
            label,
            eta=(F(1, 10), F(-1, 5)),
            visible_offset=(F(3, 10), F(2, 5)),
            first_correction=correction_lower,
            second_correction=correction_upper,
            physical_residual=fixed_residual,
            measurement_noise=F(1, 100),
        )
        for label in ("miss", "success")
    }
    global_contains = (
        F(81, 800) > 0
        and actual_lower == actuator_lower
        and actual_upper == actuator_upper
        and lower_width <= upper_width
    )
    run136_matches = run136_step_column == H * upper_width
    scheduled_shape_changes = any(value != 0 for value in column_increase)
    residual_cancels_from_d = (
        lower_column[2] - lower_column[0],
        lower_column[3] - lower_column[1],
    ) == (F(0), F(0)) and (
        upper_column[2] - upper_column[0],
        upper_column[3] - upper_column[1],
    ) == (F(0), F(0))
    if not (
        all(row["shape_unchanged_for_fixed_residual_set"]
            for row in translation_checks.values())
        and global_contains
        and run136_matches
        and scheduled_shape_changes
        and residual_cancels_from_d
    ):
        raise AssertionError("vertical control/residual split certificate changed")

    return {
        "coordinates": ("eta_p", "eta_v", "e_p", "e_v"),
        "fixed_absolute_residual_translation_checks": translation_checks,
        "residual_envelopes": {
            "actual_thrust_interval": (actual_lower, actual_upper),
            "scheduled_width_at_lower": lower_width,
            "scheduled_width_at_upper": upper_width,
            "scheduled_generator_at_lower": lower_column,
            "scheduled_generator_at_upper": upper_column,
            "scheduled_generator_increase": column_increase,
            "scheduled_step_generator_increase": column_increase[1],
            "run136_vertical_step_generator": run136_step_column,
            "global_envelope_contains_all_scheduled_widths": global_contains,
            "run136_column_matches_global_upper_envelope": run136_matches,
            "physical_residual_cancels_from_visible_offset_shape": residual_cancels_from_d,
        },
        "scheduled_joint_shape_changes_with_actual_thrust": scheduled_shape_changes,
    }


def run():
    certificate = control_translation_certificate()
    return {
        "status": "pass",
        "claim": "vertical_control_translation_is_separable_only_after_freezing_a_global_residual_envelope",
        **certificate,
        "evidence_level": "exact_vertical_control_translation_and_residual_shape_split",
        "fixed_envelope_control_effect": "translation_only",
        "scheduled_residual_control_effect": "translation_and_shape",
        "fixed_W_intrinsic_shape_interface_available": True,
        "scheduled_W_fixed_disturbance_theorem_directly_applicable": False,
        "zero_center_target_is_policy_independent": False,
        "run148_shape_valid_under_global_envelope_up_to_translation": True,
        "is_rci_certificate": False,
        "full_six_state_guarantee": False,
        "limitations": [
            "the certificate covers only one-step vertical miss and success equations",
            "the fixed-envelope route is sound but discards actual-thrust residual tightening",
            "the scheduled route remains a decision-dependent robust containment problem",
            "no invariant information ensemble, terminal set, shift, or MPC recursive feasibility is certified",
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
        "verification/check_vertical_control_translation_split.py",
        "verification/test_vertical_control_translation_split.py",
        "verification/check_vertical_multi_return_template.py",
        "verification/check_hover_partial_information_contract.py",
        "verification/check_cycle_lifted_zonotope.py",
        "configs/planar_baseline.json",
        "docs/learning/86_vertical_control_translation_split.md",
        "docs/literature/READ_PAPERS.md",
        "docs/research/run149_literature_gate.md",
        "docs/research/run149_research_log.md",
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
        "fixed_envelope_control_effect": encoded["fixed_envelope_control_effect"],
        "scheduled_residual_control_effect": encoded["scheduled_residual_control_effect"],
        "evidence_level": encoded["evidence_level"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
