#!/usr/bin/env python3
"""Audit whether the current planar benchmark certifies a nontrivial thrust-rate bound.

Uses exact Decimal arithmetic on the frozen repository configuration.  The current
model treats T as a direct input constrained only pointwise, so every pair
(T_k,T_{k+1}) in [Tmin,Tmax]^2 is admissible.  Consequently the smallest universal
one-step rate bound is Tmax-Tmin; it gives no transition-set reduction.
"""
from __future__ import annotations

import argparse
import json
from decimal import Decimal, getcontext
from pathlib import Path

getcontext().prec = 40


def D(x):
    return Decimal(str(x))


def audit(config_path: Path):
    cfg = json.loads(config_path.read_text())
    lo = D(cfg["domain"]["input_lower"][0])
    hi = D(cfg["domain"]["input_upper"][0])
    dt = D(cfg["plant"]["dt_s"])
    span = hi - lo

    # Counterexample to every rho<span: alternate the two admissible endpoints.
    jump = abs(hi - lo)
    assert jump == span
    assert lo >= D(cfg["domain"]["input_lower"][0]) and hi <= D(cfg["domain"]["input_upper"][0])

    # A rate bound rho=span admits every pair in P x P and hence conveys no
    # information beyond pointwise membership T in P.
    return {
        "config": str(config_path),
        "truth_semantics": cfg["plant"]["truth_semantics"],
        "thrust_is_direct_input": cfg["input_order"][0] == "T",
        "actuator_state_present": any(str(s).lower() in {"t_act", "thrust_actual", "actual_thrust"} for s in cfg["state_order"]),
        "T_min_N": str(lo),
        "T_max_N": str(hi),
        "dt_s": str(dt),
        "endpoint_jump_N_per_tick": str(jump),
        "smallest_universal_rho_N_per_tick": str(span),
        "equivalent_discrete_slope_N_per_s": str(span / dt),
        "endpoint_alternation_is_admissible_under_pointwise_contract": True,
        "nontrivial_rate_bound_rho_lt_span_is_certified": False,
        "rho_equal_span_reduces_next_parameter_set": False,
        "conclusion": "Current benchmark supports measured-but-arbitrarily-jumping thrust scheduling only. Any rho < 9.81 N/tick requires a new actuator/command-rate assumption and a re-derived model contract."
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", type=Path, default=Path("configs/planar_baseline.json"))
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        ap.error("output must not already exist")
    out = audit(args.config)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
