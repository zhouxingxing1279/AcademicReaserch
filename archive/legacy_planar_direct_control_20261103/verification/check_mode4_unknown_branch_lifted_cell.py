#!/usr/bin/env python3
"""Exact joint target-normal certificate for the mode-4 unknown branch.

The controller observes ``d=e-eta`` and applies one zero affine correction
before the packet outcome is known.  Both the ``4->5 miss`` and ``4->0
success`` branches retain the certified actual-thrust-dependent residual.  On
the success branch the same measurement-noise realization is propagated in
the observer error; its innovation cancels from the true tracking error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

from check_vertical_joint_predecessor import (
    H,
    OBSERVATION_HALFWIDTHS,
    POSITION_GAIN,
    _polygon_area,
    _residual_halfwidth,
    _tracking_limits,
    _vertical_generators,
    _vertical_problem,
    _zonotope_polygon,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MODE = 4
POLICY_POSITION_GAIN = F(0)
POLICY_VELOCITY_GAIN = F(0)
POLICY_OFFSET = F(0)
BRANCHES = ((5, "miss"), (0, "success"))


def _joint_primitive_columns(source_generators, label, residual_halfwidth, noise):
    """Map normalized source/noise primitives into one joint (eta+, e+) graph."""
    success = label == "success"
    d_position, d_velocity = OBSERVATION_HALFWIDTHS
    columns = []
    for index, (x, y) in enumerate(source_generators):
        q = x + H * y
        eta_next = (
            (F(0), y - POSITION_GAIN * q)
            if success
            else (q, y)
        )
        columns.append({
            "label": f"eta_generator_{index}",
            "kind": "source",
            "vector": (*eta_next, q, y),
        })
    columns.extend((
        {
            "label": "d_position",
            "kind": "source",
            "vector": (F(0), F(0), d_position, F(0)),
        },
        {
            "label": "d_velocity",
            "kind": "source",
            "vector": (F(0), F(0), H * d_velocity, d_velocity),
        },
        {
            "label": "rho_z",
            "kind": "residual",
            "vector": (F(0), H * residual_halfwidth, F(0), H * residual_halfwidth),
        },
    ))
    if success:
        columns.append({
            "label": "n_pz",
            "kind": "noise",
            "vector": (-noise, -POSITION_GAIN * noise, F(0), F(0)),
        })
    return columns


def _normal_row(normal, bound, columns):
    contributions = {
        kind: sum(
            abs(sum(a * b for a, b in zip(normal, column["vector"])))
            for column in columns
            if column["kind"] == kind
        )
        for kind in ("source", "residual", "noise")
    }
    support = sum(contributions.values(), F(0))
    return {
        "normal": normal,
        "source_support": contributions["source"],
        "residual_support": contributions["residual"],
        "noise_support": contributions["noise"],
        "support_upper": support,
        "target_bound": bound,
        "slack": bound - support,
    }


def mode4_unknown_branch_certificate():
    config, zonotopes = _vertical_problem()
    source_generators = _vertical_generators(zonotopes[SOURCE_MODE])
    eta_projection_area = _polygon_area(_zonotope_polygon(zonotopes[SOURCE_MODE]))
    position_limit, velocity_limit = _tracking_limits(config)
    d_position, d_velocity = OBSERVATION_HALFWIDTHS

    nominal_interval = tuple(config["mpc"][key][0] for key in (
        "nominal_input_lower", "nominal_input_upper"
    ))
    correction_interval = tuple(config["mpc"][key][0] for key in (
        "ancillary_correction_lower", "ancillary_correction_upper"
    ))
    actual_interval = tuple(value + POLICY_OFFSET for value in nominal_interval)
    plant_interval = tuple(config["domain"][key][0] for key in (
        "input_lower", "input_upper"
    ))
    residual_halfwidth = _residual_halfwidth(actual_interval[1])
    noise = config["sensing"]["observed_noise_halfwidth"]["pz"]

    eta_position = sum(abs(x) for x, _ in source_generators)
    eta_velocity = sum(abs(y) for _, y in source_generators)
    current_slacks = (
        position_limit - eta_position - d_position,
        velocity_limit - eta_velocity - d_velocity,
    )
    graph_edges = config["mpc"]["ancillary_rci_contract"]["mode_graph"]["edges"]

    branches = []
    for target_mode, label in BRANCHES:
        columns = _joint_primitive_columns(
            source_generators, label, residual_halfwidth, noise
        )
        eta_rows = [
            _normal_row((a, b, F(0), F(0)), bound, columns)
            for a, b, bound in _zonotope_polygon(zonotopes[target_mode]).facets
        ]
        tracking_rows = [
            _normal_row((F(0), F(0), sign, F(0)), position_limit, columns)
            for sign in (F(1), F(-1))
        ] + [
            _normal_row((F(0), F(0), F(0), sign), velocity_limit, columns)
            for sign in (F(1), F(-1))
        ]
        all_rows = eta_rows + tracking_rows
        edge_present = [SOURCE_MODE, target_mode, label] in graph_edges
        closed = edge_present and all(row["slack"] >= 0 for row in all_rows)
        residual_vector = next(
            column["vector"] for column in columns if column["label"] == "rho_z"
        )
        shared_residual_verified = residual_vector[:2] == residual_vector[2:]
        noise_vector = next(
            (column["vector"] for column in columns if column["label"] == "n_pz"),
            None,
        )
        cancellation_verified = (
            label == "success"
            and noise_vector[:2] != (F(0), F(0))
            and noise_vector[2:] == (F(0), F(0))
        )
        branches.append({
            "source_mode": SOURCE_MODE,
            "target_mode": target_mode,
            "edge_label": label,
            "edge_present_in_contract": edge_present,
            "eta_target_normal_rows": eta_rows,
            "tracking_target_normal_rows": tracking_rows,
            "target_normal_count": len(all_rows),
            "minimum_target_normal_slack": min(row["slack"] for row in all_rows),
            "joint_primitive_columns": columns,
            "shared_residual_between_eta_and_tracking_error": shared_residual_verified,
            "shared_residual_identity_verified": shared_residual_verified,
            "success_measurement_noise_propagated": label == "success",
            "measurement_innovation_cancels_from_tracking_error": cancellation_verified,
            "measurement_cancellation_identity_verified": cancellation_verified,
            "branch_closed": closed,
        })

    positive_volume = eta_projection_area > 0 and d_position > 0 and d_velocity > 0
    passed = (
        correction_interval[0] <= POLICY_OFFSET <= correction_interval[1]
        and plant_interval[0] <= actual_interval[0] <= actual_interval[1] <= plant_interval[1]
        and positive_volume
        and all(slack > 0 for slack in current_slacks)
        and all(branch["shared_residual_identity_verified"] for branch in branches)
        and all(
            branch["measurement_cancellation_identity_verified"]
            for branch in branches
            if branch["edge_label"] == "success"
        )
        and all(branch["branch_closed"] for branch in branches)
    )
    if not passed:
        raise AssertionError("mode-4 lifted source cell does not close on both unknown branches")

    return {
        "source_mode": SOURCE_MODE,
        "coordinates": "source=(eta_p,eta_v,d_p,d_v), e=eta+d",
        "source_cell": "eta in exact Run136 mode-4 projection, |d_p|<=1/5, |d_v|<=1/4",
        "affine_fibre_policy": {
            "delta_T": "0*d_p + 0*d_v + 0",
            "position_gain": POLICY_POSITION_GAIN,
            "velocity_gain": POLICY_VELOCITY_GAIN,
            "offset": POLICY_OFFSET,
        },
        "policy_uses_hidden_eta": False,
        "policy_uses_future_edge_label": False,
        "policy_values_before_label": 1,
        "nominal_thrust_interval": nominal_interval,
        "actual_thrust_interval": actual_interval,
        "plant_thrust_interval": plant_interval,
        "residual_graph": "r_z=(1043/500+(81/800)*actual_thrust)*rho_z, |rho_z|<=1",
        "residual_halfwidth_at_actual_thrust_upper": residual_halfwidth,
        "shared_actual_thrust_residual_law": True,
        "measurement_noise_halfwidth": noise,
        "eta_projection_area": eta_projection_area,
        "current_source_domain_slacks": current_slacks,
        "positive_volume_source_cell": positive_volume,
        "branches": branches,
        "both_unknown_branches_closed": passed,
    }


def run():
    return {
        "status": "pass",
        "claim": "one_fixed_lifted_mode4_cell_closes_on_both_unknown_packet_branches",
        **mode4_unknown_branch_certificate(),
        "evidence_level": "exact_two_edge_unknown_label_target_normal_support_certificate",
        "nonlinear_plant_scope": (
            "certified actual-thrust-dependent vertical residual graph, not exact 6-DoF dynamics"
        ),
        "is_rci_certificate": False,
        "terminal_family_closed": False,
        "recursive_feasibility_certified": False,
        "full_six_state_guarantee": False,
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
        "verification/check_mode4_unknown_branch_lifted_cell.py",
        "verification/test_mode4_unknown_branch_lifted_cell.py",
        "verification/check_vertical_joint_predecessor.py",
        "verification/check_cycle_lifted_zonotope.py",
        "configs/planar_baseline.json",
        "docs/learning/115_mode4_unknown_branch_lifted_cell.md",
        "docs/literature/READ_PAPERS.md",
        "docs/research/run181_literature_gate.md",
        "docs/research/run181_research_log.md",
    ]
    result["source_sha256"] = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in sources
    }
    encoded = _encode(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(encoded, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "status": encoded["status"],
        "claim": encoded["claim"],
        "branch_minimum_slacks": {
            row["edge_label"]: row["minimum_target_normal_slack"]
            for row in encoded["branches"]
        },
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
