#!/usr/bin/env python3
"""Exact width obstruction for the Run 148 translated fixed-shape family.

The centered mode-zero shape is the exact convex hull
``C0 = conv(J4 union J9 union J14)``.  Under the fixed Run 136 global
residual envelope, correction thrust changes only the center.  This checker
propagates the three convex-hull components through the miss dynamics and
tests the return images at modes 4, 9, and 14.

Directional width is invariant under arbitrary source/target translations.
The correction translation has no ``e_p`` component.  A strict excess in the
``e_p`` halfwidth therefore rejects the translated fixed-shape family without
rejecting history-conditioned information ensembles or decision-dependent
uncertainty models.
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
from check_vertical_multi_return_template import (
    RETURN_MODES,
    multi_return_template_certificate,
)


ROOT = Path(__file__).resolve().parents[1]
EP_DIRECTION = (F(0), F(0), F(1), F(0))


def _linear_image(matrix, generators):
    return [
        [
            sum(
                matrix[row][inner] * generators[inner][column]
                for inner in range(4)
            )
            for column in range(len(generators[0]))
        ]
        for row in range(4)
    ]


def _append_generator(generators, column):
    return [row + [column[index]] for index, row in enumerate(generators)]


def _miss_image(generators, residual_column):
    matrix = (
        (F(1), H, F(0), F(0)),
        (F(0), F(1), F(0), F(0)),
        (F(0), F(0), F(1), H),
        (F(0), F(0), F(0), F(1)),
    )
    return _append_generator(
        _linear_image(matrix, generators),
        (F(0), residual_column, F(0), residual_column),
    )


def _success_image(generators, residual_column, noise_column):
    matrix = (
        (F(0), F(0), F(0), F(0)),
        (-POSITION_GAIN, F(1) - POSITION_GAIN * H, F(0), F(0)),
        (F(0), F(0), F(1), H),
        (F(0), F(0), F(0), F(1)),
    )
    image = _append_generator(
        _linear_image(matrix, generators),
        (F(0), residual_column, F(0), residual_column),
    )
    return _append_generator(
        image,
        (noise_column[0], noise_column[1], F(0), F(0)),
    )


def _zonotope_support(generators, direction):
    return sum(
        (
            abs(
                sum(
                    direction[row] * generators[row][column]
                    for row in range(4)
                )
            )
            for column in range(len(generators[0]))
        ),
        F(0),
    )


def _convex_hull_support(components, direction):
    return max(
        _zonotope_support(generators, direction)
        for generators in components.values()
    )


def translated_template_certificate():
    template = multi_return_template_certificate()
    config, _, _, _, success_generators, _ = problem_data()
    residual_column = success_generators[3][1]
    noise_column = (success_generators[1][4], success_generators[3][4])
    graph = [tuple(edge) for edge in config["mpc"]["ancillary_rci_contract"]
             ["mode_graph"]["edges"]]

    base_components = {
        mode: template["return_seeds"][mode]["generators_by_row"]
        for mode in RETURN_MODES
    }
    mode_shapes = {0: base_components}
    for mode in range(14):
        mode_shapes[mode + 1] = {
            component: _miss_image(generators, residual_column)
            for component, generators in mode_shapes[mode].items()
        }

    target_ep_halfwidth = _convex_hull_support(
        base_components, EP_DIRECTION
    )
    return_edges = {}
    for mode in RETURN_MODES:
        source_components = mode_shapes[mode]
        success_components = {
            component: _success_image(
                generators, residual_column, noise_column
            )
            for component, generators in source_components.items()
        }
        success_ep_halfwidth = _convex_hull_support(
            success_components, EP_DIRECTION
        )
        excess = success_ep_halfwidth - target_ep_halfwidth
        outgoing_labels = tuple(
            label for source, _, label in graph if source == mode
        )
        has_miss = "miss" in outgoing_labels
        miss_matches = (
            {
                component: _miss_image(generators, residual_column)
                for component, generators in source_components.items()
            }
            == mode_shapes.get(mode + 1)
            if has_miss
            else None
        )
        strict_obstruction = excess > 0
        return_edges[mode] = {
            "edge": (mode, 0, "success"),
            "outgoing_labels": outgoing_labels,
            "source_shape_component_generator_counts": tuple(
                len(source_components[component][0])
                for component in RETURN_MODES
            ),
            "success_image_component_generator_counts": tuple(
                len(success_components[component][0])
                for component in RETURN_MODES
            ),
            "target_ep_halfwidth": target_ep_halfwidth,
            "success_ep_halfwidth": success_ep_halfwidth,
            "strict_ep_halfwidth_excess": excess,
            "strict_width_obstruction": strict_obstruction,
            "translated_return_containment_possible": not strict_obstruction,
            "obstruction_holds_for_all_source_centers": strict_obstruction,
            "obstruction_holds_for_all_target_centers": strict_obstruction,
            "obstruction_holds_for_all_current_corrections": strict_obstruction,
            "one_current_input_shared_across_success_and_miss": has_miss,
            "miss_shape_matches_next_mode_by_construction": miss_matches,
            "success_edge_alone_is_infeasible": strict_obstruction,
            "shared_input_branch_containment_possible": (
                not strict_obstruction if has_miss else None
            ),
        }

    obstructed = tuple(
        mode for mode, row in return_edges.items()
        if row["strict_width_obstruction"]
    )
    if not (
        obstructed == RETURN_MODES
        and target_ep_halfwidth == F(23312147, 48000000)
        and all(
            return_edges[mode]["miss_shape_matches_next_mode_by_construction"]
            for mode in (4, 9)
        )
    ):
        raise AssertionError("translated fixed-shape obstruction changed")

    return {
        "coordinates": ("eta_p", "eta_v", "e_p", "e_v"),
        "component_modes": RETURN_MODES,
        "mode_zero_shape": "conv(J_4 union J_9 union J_14)",
        "mode_zero_component_generator_counts": tuple(
            len(base_components[component][0]) for component in RETURN_MODES
        ),
        "fixed_global_residual_step_generator": residual_column,
        "correction_translation_per_unit_thrust": (F(0), F(0), F(0), H),
        "correction_changes_ep_support": False,
        "set_translation_preserves_directional_width": True,
        "return_edges": return_edges,
        "obstructed_return_modes": obstructed,
        "earliest_obstruction_mode": min(obstructed),
    }


def run():
    certificate = translated_template_certificate()
    return {
        "status": "pass",
        "claim": (
            "all_three_run148_translated_fixed_shape_returns_fail_an_exact_ep_width_necessity"
        ),
        **certificate,
        "evidence_level": (
            "exact_ep_width_obstruction_for_run148_translated_fixed_shape_family"
        ),
        "translated_fixed_shape_family_rejected": True,
        "history_conditioned_information_ensemble_rejected": False,
        "scheduled_decision_dependent_family_rejected": False,
        "is_rci_certificate": False,
        "full_six_state_guarantee": False,
        "limitations": [
            "the obstruction covers only the vertical Run148 convex shape propagated with the fixed Run136 envelope",
            "it rejects arbitrary translations and corrections because they cannot change e_p width",
            "it does not reject mode- or history-conditioned intrinsic shapes",
            "it does not reject decision-dependent residual graphs or general output-feedback information ensembles",
            "horizontal, attitude, torque, terminal, shift, and recursive MPC feasibility remain open",
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
        "verification/check_vertical_translated_template_obstruction.py",
        "verification/test_vertical_translated_template_obstruction.py",
        "verification/check_vertical_multi_return_template.py",
        "verification/check_vertical_control_translation_split.py",
        "verification/check_vertical_correlated_return_seed.py",
        "verification/check_cycle_lifted_zonotope.py",
        "configs/planar_baseline.json",
        "docs/learning/87_vertical_translated_template_obstruction.md",
        "docs/literature/READ_PAPERS.md",
        "docs/research/run150_literature_gate.md",
        "docs/research/run150_research_log.md",
    ]
    result["source_sha256"] = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in sources
    }
    encoded = _encode(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(encoded, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps({
        "status": encoded["status"],
        "claim": encoded["claim"],
        "earliest_obstruction_mode": encoded["earliest_obstruction_mode"],
        "obstructed_return_modes": encoded["obstructed_return_modes"],
        "evidence_level": encoded["evidence_level"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
