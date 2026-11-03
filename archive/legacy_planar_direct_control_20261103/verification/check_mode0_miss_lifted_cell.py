#!/usr/bin/env python3
"""Exact target-normal certificate for one lifted mode-0 miss cell.

The source cell uses coordinates ``(eta, d)`` with ``e=eta+d`` and the
controller sees only ``d``.  The affine fibre policy is identically zero.
The nonlinear vertical plant is represented by its certified shared residual
graph ``r_z=(1043/500+81*T/800) rho``; the same realization enters eta and e.
This is a one-edge implementation lemma, not an RCI certificate.
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
    _residual_halfwidth,
    _tracking_limits,
    _vertical_generators,
    _vertical_problem,
    _zonotope_polygon,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MODE = 0
TARGET_MODE = 1
POLICY_POSITION_GAIN = F(0)
POLICY_VELOCITY_GAIN = F(0)
POLICY_OFFSET = F(0)


def _eta_support(generators, normal):
    a, b = normal
    return sum(abs(a * (x + H * y) + b * y) for x, y in generators)


def mode0_miss_certificate():
    config, zonotopes = _vertical_problem()
    source_generators = _vertical_generators(zonotopes[SOURCE_MODE])
    target = _zonotope_polygon(zonotopes[TARGET_MODE])
    d_position, d_velocity = OBSERVATION_HALFWIDTHS
    position_limit, velocity_limit = _tracking_limits(config)

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

    eta_normal_rows = []
    for a, b, bound in target.facets:
        support = _eta_support(source_generators, (a, b)) + abs(b * H) * residual_halfwidth
        eta_normal_rows.append({
            "normal": (a, b, F(0), F(0)),
            "support_upper": support,
            "target_bound": bound,
            "slack": bound - support,
        })

    eta_p = sum(abs(x) for x, _ in source_generators)
    eta_v = sum(abs(y) for _, y in source_generators)
    q = sum(abs(x + H * y) for x, y in source_generators)
    tracking_rows = [
        {
            "normal": (F(0), F(0), sign, F(0)),
            "support_upper": q + d_position + H * d_velocity,
            "target_bound": position_limit,
        }
        for sign in (F(1), F(-1))
    ] + [
        {
            "normal": (F(0), F(0), F(0), sign),
            "support_upper": eta_v + d_velocity + H * residual_halfwidth,
            "target_bound": velocity_limit,
        }
        for sign in (F(1), F(-1))
    ]
    for row in tracking_rows:
        row["slack"] = row["target_bound"] - row["support_upper"]

    current_slacks = (
        position_limit - eta_p - d_position,
        velocity_limit - eta_v - d_velocity,
    )
    all_rows = eta_normal_rows + tracking_rows
    edge_present = [SOURCE_MODE, TARGET_MODE, "miss"] in config["mpc"][
        "ancillary_rci_contract"
    ]["mode_graph"]["edges"]
    passed = (
        edge_present
        and correction_interval[0] <= POLICY_OFFSET <= correction_interval[1]
        and plant_interval[0] <= actual_interval[0] <= actual_interval[1] <= plant_interval[1]
        and all(value > 0 for value in current_slacks)
        and all(row["slack"] >= 0 for row in all_rows)
    )
    if not passed:
        raise AssertionError("mode-0 lifted source cell does not close on the miss edge")

    return {
        "source_mode": SOURCE_MODE,
        "target_mode": TARGET_MODE,
        "edge_label": "miss",
        "edge_present_in_contract": edge_present,
        "coordinates": "source=(eta_p,eta_v,d_p,d_v), e=eta+d",
        "source_cell": "eta in exact Run136 mode-0 projection, |d_p|<=1/5, |d_v|<=1/4",
        "affine_fibre_policy": {
            "delta_T": "0*d_p + 0*d_v + 0",
            "position_gain": POLICY_POSITION_GAIN,
            "velocity_gain": POLICY_VELOCITY_GAIN,
            "offset": POLICY_OFFSET,
        },
        "policy_uses_hidden_eta": False,
        "nominal_thrust_interval": nominal_interval,
        "actual_thrust_interval": actual_interval,
        "plant_thrust_interval": plant_interval,
        "residual_graph": "r_z=(1043/500+(81/800)*actual_thrust)*rho_z, |rho_z|<=1",
        "residual_halfwidth_at_actual_thrust_upper": residual_halfwidth,
        "shared_residual_realization": True,
        "current_source_domain_slacks": current_slacks,
        "target_normal_count": len(all_rows),
        "eta_target_normal_rows": eta_normal_rows,
        "tracking_target_normal_rows": tracking_rows,
        "minimum_target_normal_slack": min(row["slack"] for row in all_rows),
        "positive_volume_source_cell": d_position > 0 and d_velocity > 0,
        "one_edge_closed": passed,
    }


def run():
    certificate = mode0_miss_certificate()
    return {
        "status": "pass",
        "claim": "one_fixed_lifted_mode0_cell_closes_on_the_mode0_to1_miss_edge",
        **certificate,
        "evidence_level": "exact_one_edge_target_normal_support_certificate",
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
        "verification/check_mode0_miss_lifted_cell.py",
        "verification/test_mode0_miss_lifted_cell.py",
        "verification/check_vertical_joint_predecessor.py",
        "verification/check_cycle_lifted_zonotope.py",
        "configs/planar_baseline.json",
        "docs/learning/114_mode0_miss_lifted_cell.md",
        "docs/literature/READ_PAPERS.md",
        "docs/research/run180_literature_gate.md",
        "docs/research/run180_research_log.md",
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
        "minimum_target_normal_slack": encoded["minimum_target_normal_slack"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
