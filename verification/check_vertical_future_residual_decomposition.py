#!/usr/bin/env python3
"""Exact Run168 decomposition of the vertical future-residual contract."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN166_SCALE_MAX = F(16254878, 42598647)


def future_residual_decomposition_certificate():
    config = json.loads(
        (ROOT / "configs/planar_baseline.json").read_text(),
        parse_float=F,
        parse_int=F,
    )
    graph = config["mpc"]["ancillary_rci_contract"]["disturbance_graph"]
    formula = graph["physical_residual_halfwidth"]["r_z"]
    if formula != "1043/500 + (81/800) * actual_thrust":
        raise AssertionError("vertical residual formula changed")

    aerodynamic_core = F(1043, 500)
    attitude_slope = F(81, 800)
    thrust_max = config["domain"]["input_upper"][0]
    attitude_term = attitude_slope * thrust_max
    total = aerodynamic_core + attitude_term
    target = RUN166_SCALE_MAX * total
    best_scale = aerodynamic_core / total
    excess = aerodynamic_core - target
    core_scale_max = target / aerodynamic_core

    expected = (
        thrust_max == F(2943, 200)
        and attitude_term == F(238383, 160000)
        and total == F(572143, 160000)
        and target == F(89401829, 65520000)
        and excess == F(47272891, 65520000)
        and best_scale == F(333760, 572143)
        and core_scale_max == F(89401829, 136674720)
    )
    if not expected:
        raise AssertionError("vertical future-residual certificate changed")

    return {
        "current_contract": {
            "truth_semantics": config["plant"]["truth_semantics"],
            "external_process_halfwidth_z": config["plant"]["external_process_halfwidth"][3],
            "aerodynamic_core": aerodynamic_core,
            "attitude_thrust_slope": attitude_slope,
            "thrust_max": thrust_max,
            "attitude_thrust_term_at_tmax": attitude_term,
            "total_halfwidth": total,
        },
        "run166_target": {
            "scale_max": RUN166_SCALE_MAX,
            "absolute_halfwidth_max": target,
        },
        "attitude_only_obstruction": {
            "best_case": "remove_entire_attitude_thrust_term",
            "best_halfwidth": aerodynamic_core,
            "strict_excess": excess,
            "best_scale": best_scale,
        },
        "necessary_aerodynamic_contract": {
            "core_halfwidth_max_if_attitude_zero": target,
            "core_scale_max_if_attitude_zero": core_scale_max,
            "core_reduction_min": 1 - core_scale_max,
            "quantifier": "all_15_future_ticks_and_all_information_consistent_trajectories",
        },
    }


def run():
    return {
        "status": "pass",
        "claim": "attitude_only_reduction_cannot_meet_run166_future_residual_scale",
        **future_residual_decomposition_certificate(),
        "attitude_only_route_impossible": True,
        "local_aerodynamic_route_ruled_out": False,
        "is_recursive_feasibility_proof": False,
        "is_full_six_state_guarantee": False,
    }


def _encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _encode(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_encode(item) for item in value]
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    result = run()
    sources = [
        "verification/check_vertical_future_residual_decomposition.py",
        "verification/test_vertical_future_residual_decomposition.py",
        "src/smf_mpc/plant.py",
        "src/smf_mpc/filter.py",
        "configs/planar_baseline.json",
        "docs/learning/104_vertical_future_residual_decomposition.md",
        "docs/literature/READ_PAPERS.md",
        "docs/research/run168_literature_gate.md",
        "docs/research/run168_research_log.md",
    ]
    result["source_sha256"] = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in sources
    }
    encoded = _encode(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(encoded, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"status": encoded["status"], "claim": encoded["claim"]}, indent=2))


if __name__ == "__main__":
    main()
