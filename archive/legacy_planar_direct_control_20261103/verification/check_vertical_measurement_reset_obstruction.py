#!/usr/bin/env python3
"""Exact five-step obstruction to reusing the absolute initial-state contract.

The witness follows the configured nonlinear plant on the vertical invariant
slice ``vx = phi = omega = 0``.  Choosing ``wind_z = vz`` makes both relative
air-speed components zero, so the aerodynamic term is exactly zero.  A
successful position measurement is then consistent with the truth but cannot
change its physical velocity.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _fraction(value):
    return F(str(value))


def certificate():
    config = json.loads((ROOT / "configs/planar_baseline.json").read_text())
    plant = config["plant"]
    initial = config["initial_set"]
    constraints = config["domain"]

    h = _fraction(plant["dt_s"])
    gravity = _fraction(plant["gravity_m_s2"])
    mass = _fraction(plant["mass_kg"])
    thrust = _fraction(constraints["input_upper"][0])
    velocity_halfwidth = _fraction(initial["halfwidth"][3])
    vertical_acceleration = thrust / mass - gravity

    pz = _fraction(initial["center"][1])
    vz = F(0)
    trajectory = []
    for tick in range(5):
        wind_z = vz
        trajectory.append({
            "tick": tick,
            "vertical_position": pz,
            "vertical_velocity": vz,
            "vertical_wind": wind_z,
            "vertical_aerodynamic_acceleration": F(0),
        })
        pz = pz + h * vz
        vz = vz + h * vertical_acceleration

    state_lower = tuple(map(_fraction, constraints["state_lower"]))
    state_upper = tuple(map(_fraction, constraints["state_upper"]))
    input_lower = tuple(map(_fraction, constraints["input_lower"]))
    input_upper = tuple(map(_fraction, constraints["input_upper"]))
    wind_lower = _fraction(plant["wind_bounds_m_s"][1][0])
    wind_upper = _fraction(plant["wind_bounds_m_s"][1][1])
    admissible = (
        input_lower[0] <= thrust <= input_upper[0]
        and input_lower[1] <= 0 <= input_upper[1]
        and all(
            wind_lower <= row["vertical_wind"] <= wind_upper
            for row in trajectory
        )
        and all(
            state_lower[1] <= row["vertical_position"] <= state_upper[1]
            and state_lower[3] <= row["vertical_velocity"] <= state_upper[3]
            for row in trajectory
        )
        and state_lower[0] <= 0 <= state_upper[0]
        and state_lower[1] <= pz <= state_upper[1]
        and state_lower[2] <= 0 <= state_upper[2]
        and state_lower[3] <= vz <= state_upper[3]
        and state_lower[4] <= 0 <= state_upper[4]
        and state_lower[5] <= 0 <= state_upper[5]
    )
    strict_excess = vz - velocity_halfwidth
    if not (
        h == F(1, 50)
        and vertical_acceleration == F(981, 200)
        and pz == F(100981, 50000)
        and vz == F(981, 2000)
        and strict_excess == F(781, 2000)
        and admissible
    ):
        raise AssertionError("five-step measurement-reset witness changed")

    return {
        "five_step_physical_witness": {
            "success_edge": "mode_4_to_mode_0",
            "thrust_each_step": thrust,
            "torque_each_step": F(0),
            "horizontal_wind_each_step": F(0),
            "trajectory_before_each_step": trajectory,
            "vertical_acceleration_each_step": vertical_acceleration,
            "vertical_position_after_success": pz,
            "vertical_velocity_after_success": vz,
            "all_inputs_winds_and_states_admissible": admissible,
        },
        "successful_measurement": {
            "measured_position": pz,
            "position_noise": F(0),
            "truth_remains_in_posterior": True,
            "measurement_changes_physical_state": False,
        },
        "reset_comparison": {
            "configured_initial_velocity_center": F(0),
            "configured_initial_velocity_halfwidth": velocity_halfwidth,
            "post_success_true_vertical_velocity": vz,
            "strict_excess": strict_excess,
            "same_absolute_initial_window_contract_rejected": strict_excess > 0,
        },
    }


def run():
    result = certificate()
    return {
        "status": "pass",
        "claim": "successful_measurement_alone_does_not_reset_truth_into_absolute_initial_window_contract",
        **result,
        "evidence_level": "exact_quantifier_correction_for_measurement_only_reset_witness",
        "same_initial_window_reset_closure_proved": False,
        "measurement_only_reset_implication_rejected": True,
        "controlled_return_to_initial_box_impossible": False,
        "control_exists_quantifier_not_tested": True,
        "recursive_tube_invariance_proved": False,
        "next_required_object": "causal_controlled_return_predecessor_over_observation_fibers",
        "limitations": [
            "rejects only inferring absolute-box reset from measurement success alone",
            "does not test existence of a causal controlled-return policy",
            "does not reject recentered or mode-dependent information tubes",
            "does not prove terminal invariance or recursive MPC feasibility",
            "does not provide a full six-degree-of-freedom guarantee",
        ],
    }


def _encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, list):
        return [_encode(item) for item in value]
    if isinstance(value, tuple):
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
        "verification/check_vertical_measurement_reset_obstruction.py",
        "verification/test_vertical_measurement_reset_obstruction.py",
        "src/smf_mpc/plant.py",
        "configs/planar_baseline.json",
        "docs/learning/109_vertical_measurement_reset_obstruction.md",
        "docs/literature/READ_PAPERS.md",
        "docs/research/run174_literature_gate.md",
        "docs/research/run174_research_log.md",
        "docs/research/run175_literature_gate.md",
        "docs/research/run175_research_log.md",
    ]
    result["source_sha256"] = {
        source: hashlib.sha256((ROOT / source).read_bytes()).hexdigest()
        for source in sources
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(_encode(result), indent=2) + "\n")
    print(json.dumps(_encode({"status": "pass", "claim": result["claim"]}), indent=2))


if __name__ == "__main__":
    main()
