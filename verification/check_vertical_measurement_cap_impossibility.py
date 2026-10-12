#!/usr/bin/env python3
"""Exact obstruction to meeting the Run166 visible cap by measurement alone."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

from check_vertical_correlated_return_seed import correlated_return_seed


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_CAP = F(58684997, 145000000)


def measurement_cap_certificate():
    seed = correlated_return_seed()
    q_halfwidth = seed["initialization_reachability"]["mode14_q_halfwidth"]
    config = json.loads((ROOT / "configs/planar_baseline.json").read_text())
    noise_halfwidth = F(str(config["sensing"]["observed_noise_halfwidth"]["pz"]))

    visible_halfwidth = q_halfwidth + noise_halfwidth
    noiseless_excess = q_halfwidth - REQUIRED_CAP
    required_q = REQUIRED_CAP - noise_halfwidth
    required_reduction = q_halfwidth - required_q
    required_scale = required_q / q_halfwidth

    if not (
        q_halfwidth == F(23312147, 48000000)
        and noise_halfwidth == F(1, 50)
        and visible_halfwidth == F(24272147, 48000000)
        and noiseless_excess == F(563381459, 6960000000)
        and required_q == F(55784997, 145000000)
        and required_reduction == F(702581459, 6960000000)
        and required_scale == F(2677679856, 3380261315)
    ):
        raise AssertionError("vertical measurement-cap certificate changed")

    return {
        "forced_return_support": {
            "identity": "d_p_plus=q+n_p",
            "mode14_q_halfwidth": q_halfwidth,
            "measurement_noise_halfwidth": noise_halfwidth,
            "visible_halfwidth": visible_halfwidth,
        },
        "noiseless_counterexample": {
            "q": q_halfwidth,
            "n_p": F(0),
            "d_p_plus": q_halfwidth,
            "required_cap": REQUIRED_CAP,
            "strict_excess": noiseless_excess,
            "admissible_under_current_contract": True,
        },
        "necessary_source_contract": {
            "q_halfwidth_max": required_q,
            "absolute_reduction": required_reduction,
            "scale_max": required_scale,
        },
        "measurement_noise_halfwidth_max_with_current_source": REQUIRED_CAP - q_halfwidth,
    }


def run():
    return {
        "status": "pass",
        "claim": "current_measurement_intersection_cannot_guarantee_run166_global_visible_cap",
        **measurement_cap_certificate(),
        "measurement_only_global_cap_impossible": True,
        "seed_measurement_branch_terminated": True,
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
        "verification/check_vertical_measurement_cap_impossibility.py",
        "verification/test_vertical_measurement_cap_impossibility.py",
        "verification/check_vertical_center_contract_tradeoff.py",
        "verification/check_vertical_correlated_return_seed.py",
        "verification/check_cycle_lifted_zonotope.py",
        "configs/planar_baseline.json",
        "docs/learning/103_vertical_measurement_cap_impossibility.md",
        "docs/literature/READ_PAPERS.md",
        "docs/research/run167_literature_gate.md",
        "docs/research/run167_research_log.md",
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
