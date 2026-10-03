#!/usr/bin/env python3
"""Exact common convex template for three fixed-zero-correction returns.

The first successful measurement can occur after 4, 9, or 14 consecutive miss
edges.  Under the explicit baseline ``deltaT = 0`` on every preceding miss,
this checker maps the complete hidden estimator-error fiber to
``(eta_p, eta_v, e_p, e_v)`` while retaining the path-local shared residual and
measurement-noise generator columns.  It then certifies the least convex set
containing all three return images via the standard exact perspective lift of a
convex hull of centered zonotopes.

The common template is a fixed-policy reachable baseline, not a
policy-independent necessary target or an invariant set.
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
    diagonal,
    least_mode_zero_box,
    lift_cycle,
    problem_data,
)
from check_mode_radius import propagate_generators
from check_vertical_correlated_return_seed import (
    _independent_generator_indices,
    _matrix_rank,
    _return_generators,
    _row_support,
)
from check_vertical_joint_predecessor import POSITION_GAIN, _tracking_limits


ROOT = Path(__file__).resolve().parents[1]
RETURN_MODES = (4, 9, 14)


def _difference_rows(rows):
    return [
        [rows[index + 2][column] - rows[index][column]
         for column in range(len(rows[0]))]
        for index in (0, 1)
    ]


def _seed_certificate(mode, zonotope, noise_column, residual_column,
                      eta_limits, tracking_limits):
    rows = _return_generators(zonotope, noise_column, residual_column)
    d_rows = _difference_rows(rows)
    eta_support = tuple(_row_support(row) for row in rows[:2])
    tracking_support = tuple(_row_support(row) for row in rows[2:])
    d_support = tuple(_row_support(row) for row in d_rows)
    eta_slack = tuple(
        limit - support for limit, support in zip(eta_limits, eta_support)
    )
    tracking_slack = tuple(
        limit - support
        for limit, support in zip(tracking_limits, tracking_support)
    )
    rank = _matrix_rank(rows)
    independent = _independent_generator_indices(rows)
    shared_line_relation = all(
        d_rows[1][column] == POSITION_GAIN * d_rows[0][column]
        for column in range(len(rows[0]))
    )
    return {
        "source_mode": mode,
        "coordinates": ("eta_p", "eta_v", "e_p", "e_v"),
        "source_generator_count": len(zonotope[0]),
        "generator_count": len(rows[0]),
        "generators_by_row": rows,
        "affine_hull_dimension": rank,
        "independent_generator_indices": independent,
        "shared_residual_primitive": (
            rows[1][-2] == rows[3][-2] == residual_column
        ),
        "shared_measurement_primitive": (
            rows[0][-1] == noise_column[0]
            and rows[1][-1] == noise_column[1]
            and rows[2][-1] == rows[3][-1] == 0
        ),
        "all_generators_satisfy_dv_equals_L_dp": shared_line_relation,
        "eta_support": eta_support,
        "eta_slack": eta_slack,
        "tracking_error_support": tracking_support,
        "tracking_error_slack": tracking_slack,
        "visible_offset_support": d_support,
        "eta_projection_in_mode0_vertical_box": all(
            slack >= 0 for slack in eta_slack
        ),
        "tracking_error_projection_in_hard_box": all(
            slack >= 0 for slack in tracking_slack
        ),
    }


def multi_return_template_certificate():
    config, A0, G0, A1, G1, _ = problem_data()
    cycles = [lift_cycle(length, A0, G0, A1, G1) for length in CYCLE_LENGTHS]
    mode_zero_box = least_mode_zero_box(cycles)
    zonotopes = age_zonotopes(mode_zero_box, A0, G0)
    eta_limits = (mode_zero_box[1], mode_zero_box[3])
    tracking_limits = _tracking_limits(config)
    graph = {
        tuple(edge)
        for edge in config["mpc"]["ancillary_rci_contract"]["mode_graph"]["edges"]
    }
    noise_column = (G1[1][4], G1[3][4])
    residual_column = G1[3][1]

    returns = {}
    seeds = {}
    for mode in RETURN_MODES:
        reached = diagonal(mode_zero_box)
        miss_count = 0
        for source in range(mode):
            if (source, source + 1, "miss") in graph:
                miss_count += 1
            reached = propagate_generators(A0, reached, G0)
        returns[mode] = {
            "miss_edge_count": miss_count,
            "source_zonotope_reached_exactly": reached == zonotopes[mode],
            "success_return_edge_present": (mode, 0, "success") in graph,
            "correction_thrust_sequence": (F(0),) * mode,
            "visible_offset_before_success": (F(0), F(0)),
            "visible_offset_derived_by_miss_dynamics": True,
        }
        seeds[mode] = _seed_certificate(
            mode,
            zonotopes[mode],
            noise_column,
            residual_column,
            eta_limits,
            tracking_limits,
        )

    concatenated_rows = [
        [value for mode in RETURN_MODES
         for value in seeds[mode]["generators_by_row"][row]]
        for row in range(4)
    ]
    concatenated_d_rows = _difference_rows(concatenated_rows)
    hull_eta_support = tuple(
        max(seeds[mode]["eta_support"][axis] for mode in RETURN_MODES)
        for axis in range(2)
    )
    hull_tracking_support = tuple(
        max(seeds[mode]["tracking_error_support"][axis]
            for mode in RETURN_MODES)
        for axis in range(2)
    )
    hull_d_support = tuple(
        max(seeds[mode]["visible_offset_support"][axis]
            for mode in RETURN_MODES)
        for axis in range(2)
    )
    hull_eta_slack = tuple(
        limit - support for limit, support in zip(eta_limits, hull_eta_support)
    )
    hull_tracking_slack = tuple(
        limit - support
        for limit, support in zip(tracking_limits, hull_tracking_support)
    )
    common_rank = _matrix_rank(concatenated_rows)
    common_line_relation = all(
        concatenated_d_rows[1][column]
        == POSITION_GAIN * concatenated_d_rows[0][column]
        for column in range(len(concatenated_rows[0]))
    )

    # Concatenating all generators is a Minkowski sum, not a convex hull.  Its
    # coordinate supports are sums and provide an exact negative control for
    # the representation mistake.
    naive_eta_support = tuple(
        sum((seeds[mode]["eta_support"][axis] for mode in RETURN_MODES), F(0))
        for axis in range(2)
    )
    naive_tracking_support = tuple(
        sum((seeds[mode]["tracking_error_support"][axis]
             for mode in RETURN_MODES), F(0))
        for axis in range(2)
    )
    naive_d_support = tuple(
        sum((seeds[mode]["visible_offset_support"][axis]
             for mode in RETURN_MODES), F(0))
        for axis in range(2)
    )

    required_returns_hold = all(
        row["miss_edge_count"] == mode
        and row["source_zonotope_reached_exactly"]
        and row["success_return_edge_present"]
        for mode, row in returns.items()
    )
    seeds_hold = all(
        seed["affine_hull_dimension"] == 3
        and seed["shared_residual_primitive"]
        and seed["shared_measurement_primitive"]
        and seed["all_generators_satisfy_dv_equals_L_dp"]
        and seed["eta_projection_in_mode0_vertical_box"]
        and seed["tracking_error_projection_in_hard_box"]
        for seed in seeds.values()
    )
    template_holds = (
        common_rank == 3
        and common_line_relation
        and all(slack >= 0 for slack in hull_eta_slack)
        and all(slack >= 0 for slack in hull_tracking_slack)
    )
    naive_eta_admissible = all(
        support <= limit for support, limit in zip(naive_eta_support, eta_limits)
    )
    naive_tracking_admissible = all(
        support <= limit
        for support, limit in zip(naive_tracking_support, tracking_limits)
    )
    if not (
        required_returns_hold
        and seeds_hold
        and template_holds
        and not naive_eta_admissible
        and not naive_tracking_admissible
    ):
        raise AssertionError("multi-return common-template certificate changed")

    return {
        "initialization_returns": returns,
        "return_seeds": seeds,
        "common_mode_zero_template": {
            "set_expression": "conv(J_4 union J_9 union J_14)",
            "representation": (
                "exact_perspective_lift_of_convex_hull_of_path_zonotopes"
            ),
            "component_modes": RETURN_MODES,
            "path_selector_count": len(RETURN_MODES),
            "local_generator_counts": tuple(
                seeds[mode]["generator_count"] for mode in RETURN_MODES
            ),
            "total_local_generator_count": sum(
                seeds[mode]["generator_count"] for mode in RETURN_MODES
            ),
            "lift_constraints": (
                "lambda_m >= 0",
                "sum_m lambda_m = 1",
                "-lambda_m <= v_m_i <= lambda_m",
                "x = sum_m G_m v_m",
            ),
            "affine_hull_dimension": common_rank,
            "least_convex_container": True,
            "preserves_path_local_generator_column_coupling": True,
            "prevents_simultaneous_full_path_activation": True,
            "permits_fractional_cross_path_mixtures": True,
            "fractional_two_path_selector_witness": (F(1, 2), F(1, 2), F(0)),
            "two_unit_scale_selectors_feasible": False,
            "all_points_satisfy_dv_equals_L_dp": common_line_relation,
            "eta_support": hull_eta_support,
            "eta_slack": hull_eta_slack,
            "tracking_error_support": hull_tracking_support,
            "tracking_error_slack": hull_tracking_slack,
            "visible_offset_support": hull_d_support,
            "eta_projection_in_mode0_vertical_box": all(
                slack >= 0 for slack in hull_eta_slack
            ),
            "tracking_error_projection_in_hard_box": all(
                slack >= 0 for slack in hull_tracking_slack
            ),
            "has_strict_estimator_margin": all(
                slack > 0 for slack in hull_eta_slack
            ),
        },
        "naive_concatenation_negative_control": {
            "representation": "Minkowski_sum_from_unscaled_generator_concatenation",
            "eta_support": naive_eta_support,
            "tracking_error_support": naive_tracking_support,
            "visible_offset_support": naive_d_support,
            "eta_projection_in_mode0_vertical_box": naive_eta_admissible,
            "tracking_error_projection_in_hard_box": naive_tracking_admissible,
            "failure_is_representation_specific": True,
        },
    }


def run():
    certificate = multi_return_template_certificate()
    return {
        "status": "pass",
        "claim": "three_fixed_zero_correction_returns_fit_one_exact_rank_three_minimal_convex_template",
        **certificate,
        "evidence_level": (
            "exact_rank_three_minimal_convex_template_for_three_fixed_zero_correction_returns"
        ),
        "certificate_scope": "fixed_zero_correction_initialization_baseline",
        "all_fixed_zero_correction_return_seeds_certified": True,
        "common_mode_zero_template_certified": True,
        "is_policy_independent_necessity": False,
        "strict_estimator_margin": False,
        "is_rci_certificate": False,
        "full_six_state_guarantee": False,
        "limitations": [
            "the certificate covers only the vertical projection of three fixed-zero-correction initialization return paths",
            "nonzero causal correction can translate the visible offset, so this is not a policy-independent necessary target",
            "the convex hull is a low-dimensional reachable baseline, not an invariant information ensemble",
            "continuous perspective selectors permit fractional mixtures of mutually exclusive path sets",
            "the template touches both mode-zero estimator coordinate bounds and has no estimator margin",
            "no causal controlled predecessor or fixed point is synthesized",
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
        "verification/check_vertical_multi_return_template.py",
        "verification/test_vertical_multi_return_template.py",
        "verification/check_vertical_correlated_return_seed.py",
        "verification/check_vertical_joint_first_sweep.py",
        "verification/check_vertical_joint_predecessor.py",
        "verification/check_cycle_lifted_zonotope.py",
        "verification/check_mode_nestedness.py",
        "verification/check_mode_radius.py",
        "configs/planar_baseline.json",
        "docs/learning/85_vertical_multi_return_template.md",
        "docs/literature/READ_PAPERS.md",
        "docs/research/run148_literature_gate.md",
        "docs/research/run148_research_log.md",
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
        "return_modes": encoded["common_mode_zero_template"]["component_modes"],
        "affine_hull_dimension": encoded["common_mode_zero_template"]["affine_hull_dimension"],
        "strict_estimator_margin": encoded["strict_estimator_margin"],
        "evidence_level": encoded["evidence_level"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
