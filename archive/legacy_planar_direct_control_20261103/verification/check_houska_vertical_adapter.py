#!/usr/bin/env python3
"""Exact admission contract for a vertical Houska-style baseline.

The current plant has an actual-thrust-dependent vertical residual and an
edge-dependent measurement operator.  This checker freezes the residual at
the actuator-wide maximum and retains the packet graph explicitly.  It does
not synthesize a polytopic information ensemble.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_RESIDUAL_FORMULA = "1043/500 + (81/800) * actual_thrust"
EXPECTED_RESIDUAL_REALIZATION = "(1043/500 + (81/800) * actual_thrust) * rho_z"
EXPECTED_EDGES = (
    [[mode, mode + 1, "miss"] for mode in range(14)]
    + [[4, 0, "success"], [9, 0, "success"], [14, 0, "success"]]
)


def _symmetric_error_margin(plant_lower, plant_upper, nominal_lower, nominal_upper):
    return min(nominal_lower - plant_lower, plant_upper - nominal_upper)


def adapter_contract(config):
    dt = config["plant"]["dt_s"]
    actual_lower, actual_upper = config["domain"]["input_lower"][0], config["domain"]["input_upper"][0]
    nominal_lower, nominal_upper = config["mpc"]["nominal_input_lower"][0], config["mpc"]["nominal_input_upper"][0]
    nominal_state = config["mpc"]["ancillary_rci_contract"]["nominal_state_domain"]
    plant_lower = config["domain"]["state_lower"]
    plant_upper = config["domain"]["state_upper"]

    disturbance = config["mpc"]["ancillary_rci_contract"]["disturbance_graph"]
    formula = disturbance["physical_residual_halfwidth"].get("r_z")
    realization = disturbance["primitive_vector"]["realizations"].get("r_z")
    if formula != EXPECTED_RESIDUAL_FORMULA or realization != EXPECTED_RESIDUAL_REALIZATION:
        raise ValueError("vertical residual formula does not match the frozen adapter")

    residual = F(1043, 500) + F(81, 800) * actual_upper
    lower_correction_margin = nominal_lower - actual_lower
    upper_correction_margin = actual_upper - nominal_upper
    if lower_correction_margin != upper_correction_margin:
        raise ValueError("symmetric nominal input allocation is required by this adapter")
    correction = lower_correction_margin
    position_margin = _symmetric_error_margin(
        plant_lower[1], plant_upper[1], nominal_state["lower"][1], nominal_state["upper"][1]
    )
    velocity_margin = _symmetric_error_margin(
        plant_lower[3], plant_upper[3], nominal_state["lower"][3], nominal_state["upper"][3]
    )
    return {
        "state_order": ["e_pz", "e_vz"],
        "input": "delta_thrust",
        "A": [[F(1), dt], [F(0), F(1)]],
        "B": [[F(0)], [dt]],
        "C": [[F(1), F(0)]],
        "continuous_residual_halfwidth": residual,
        "discrete_W_velocity_halfwidth": dt * residual,
        "tracking_error_box": {
            "position_halfwidth": position_margin,
            "velocity_halfwidth": velocity_margin,
        },
        "correction_input_halfwidth": correction,
        "lower_correction_margin": lower_correction_margin,
        "upper_correction_margin": upper_correction_margin,
    }


def run_from_config(config):
    adapter = adapter_contract(config)
    contract = config["mpc"]["ancillary_rci_contract"]
    graph = contract["mode_graph"]
    if graph.get("mode_count") != 15 or graph.get("edges") != EXPECTED_EDGES:
        raise ValueError("15-mode packet graph does not match the frozen adapter")
    sensing = config.get("sensing", {})
    if not (
        sensing.get("position_period_ticks") == 5
        and sensing.get("max_consecutive_missed_packets") == 2
        and sensing.get("position_indices") == [0, 1]
        and sensing.get("observed_noise_halfwidth", {}).get("pz") == F(1, 50)
    ):
        raise ValueError("position sensing schedule does not match the frozen adapter")
    outgoing = {}
    for source, target, label in graph["edges"]:
        outgoing.setdefault(source, []).append((target, label))
    branch_modes = sorted(mode for mode, edges in outgoing.items() if len(edges) > 1)

    expected_residual = F(572143, 160000)
    if adapter["continuous_residual_halfwidth"] != expected_residual:
        raise AssertionError("global residual envelope drifted from the exact actuator maximum")
    if adapter["correction_input_halfwidth"] != expected_residual:
        raise AssertionError("frozen correction authority drifted from the expected value")
    if branch_modes != [4, 9] or graph.get("control_precedes_successor_edge") is not True:
        raise AssertionError("packet graph does not preserve pre-branch control causality")

    return {
        "status": "pass",
        "claim": "vertical_fixed_envelope_houska_adapter_is_fully_instantiated",
        **adapter,
        "mode_count": graph["mode_count"],
        "edge_count": len(graph["edges"]),
        "edges": graph["edges"],
        "measurement_operators": {
            "miss": {"intersection": "identity", "noise_halfwidth": None},
            "success": {
                "intersection": "position_strip",
                "noise_halfwidth": config["sensing"]["observed_noise_halfwidth"]["pz"],
            },
        },
        "shared_control_branch_modes": branch_modes,
        "control_precedes_packet_outcome": True,
        "houska_equation_29_extension": "one_source_ensemble_per_mode_and_one_successor_inclusion_per_edge",
        "evidence_level": "exact_houska_vertical_adapter_contract",
        "invariant_information_ensemble_certified": False,
        "recursive_feasibility_certified": False,
        "full_six_state_guarantee": False,
        "limitations": [
            "the actuator-wide fixed residual envelope is conservative",
            "Y/G/Lambda and Z/H/Omega templates have not been selected",
            "no extreme information-set controls or terminal ensemble have been synthesized",
        ],
    }


def run():
    config = json.loads((ROOT / "configs/planar_baseline.json").read_text(), parse_float=F)
    return run_from_config(config)


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
        "verification/check_houska_vertical_adapter.py",
        "verification/test_houska_vertical_adapter.py",
        "configs/planar_baseline.json",
        "docs/superpowers/specs/2026-10-26-houska-baseline-adapter-design.md",
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
        "residual": encoded["continuous_residual_halfwidth"],
        "branch_modes": encoded["shared_control_branch_modes"],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
