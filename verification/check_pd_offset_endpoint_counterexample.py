#!/usr/bin/env python3
"""Exact counterexample to endpoint-only checks for affine-offset PD-RCI.

The checker is deliberately scalar.  It isolates the certification error:
an affine scheduling-dependent set vertex multiplied by affine dynamics is a
quadratic function of the scheduling parameter, so endpoint checks need not
bound the interval interior.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
from fractions import Fraction as F
from pathlib import Path


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _value(a: F, b: F, c: F, point: F) -> F:
    return a * point * point + b * point + c


def quadratic_max_on_interval(a: F, b: F, c: F, lower: F, upper: F) -> dict:
    """Return the exact maximum of ``a*p^2+b*p+c`` on ``[lower, upper]``."""
    if lower > upper:
        raise ValueError("lower endpoint exceeds upper endpoint")
    candidates = [lower] if lower == upper else [lower, upper]
    if a < 0:
        stationary = -b / (2 * a)
        if lower < stationary < upper:
            candidates.append(stationary)
    candidates = sorted(set(candidates))
    values = {point: _value(a, b, c, point) for point in candidates}
    maximum = max(values.values())
    return {
        "candidates": candidates,
        "values": values,
        "maximum": maximum,
        "maximizers": [point for point in candidates if values[point] == maximum],
    }


def _assert_frozen_example(
    *,
    parameter_lower: F,
    parameter_upper: F,
    radius_intercept: F,
    radius_slope: F,
    dynamics_intercept: F,
    dynamics_slope: F,
) -> None:
    assert parameter_lower == 0
    assert parameter_upper == 1
    assert radius_intercept == 1
    assert radius_slope == 1
    assert dynamics_intercept == 1
    assert dynamics_slope == F(-1, 2)


def _as_text(value: F) -> str:
    return str(value)


def build_report(root: Path) -> dict:
    pl, pu = F(0), F(1)
    q0, q1 = F(1), F(1)
    a0, a1 = F(1), F(-1, 2)
    _assert_frozen_example(
        parameter_lower=pl,
        parameter_upper=pu,
        radius_intercept=q0,
        radius_slope=q1,
        dynamics_intercept=a0,
        dynamics_slope=a1,
    )

    # (a0+a1*p)(q0+q1*p) = qa*p^2+qb*p+qc.
    qa = a1 * q1
    qb = a0 * q1 + a1 * q0
    qc = a0 * q0
    exact = quadratic_max_on_interval(qa, qb, qc, pl, pu)
    endpoint_values = {
        _as_text(pl): _as_text(_value(qa, qb, qc, pl)),
        _as_text(pu): _as_text(_value(qa, qb, qc, pu)),
    }
    common_target_radius = min(q0 + q1 * pl, q0 + q1 * pu)
    maximum = exact["maximum"]

    dependencies = [
        "verification/check_pd_offset_endpoint_counterexample.py",
        "verification/test_pd_offset_endpoint_counterexample.py",
        "docs/research/run196_literature_gate.md",
        "docs/superpowers/specs/2026-10-29-pd-offset-endpoint-counterexample-design.md",
    ]
    return {
        "run": 196,
        "question": "Are thrust-endpoint checks sound for affine-offset parameter-dependent RCI slices under arbitrary future scheduling jumps?",
        "counterexample": {
            "parameter_interval": ["0", "1"],
            "slice": "S(p)=[-(1+p),1+p]",
            "dynamics": "x+=(1-p/2)x",
            "future_parameter_contract": "p+ may be any value in [0,1]",
            "common_successor_target": "intersection_{p+ in [0,1]} S(p+)=[-1,1]",
            "common_target_radius": _as_text(common_target_radius),
            "quadratic": [_as_text(qa), _as_text(qb), _as_text(qc)],
            "endpoint_values": endpoint_values,
            "endpoint_only_condition_passes": all(F(value) <= common_target_radius for value in endpoint_values.values()),
            "global_maximizer": _as_text(exact["maximizers"][0]),
            "global_maximum": _as_text(maximum),
            "global_condition_passes": maximum <= common_target_radius,
            "violation": _as_text(maximum - common_target_radius),
        },
        "certification_interface": {
            "fixed_candidate": "maximize every exact rational quadratic facet/vertex residual over the full closed scheduling interval",
            "candidate_points": "both endpoints plus an interior stationary point only when the quadratic is concave and the point lies in the interval",
            "joint_synthesis": "not an LP in general; a sound global polynomial/SDP construction or independently verified returned candidate is required",
        },
        "evidence_level": "COUNTEREXAMPLE",
        "gate_A_status": "blocked",
        "proves_pd_rci_nonexistence": False,
        "proves_six_state_safety": False,
        "proves_recursive_feasibility": False,
        "dependencies_sha256": {path: _sha256(root / path) for path in dependencies},
        "runtime": {"python": platform.python_version()},
        "next_problem": "choose a sound synthesis relaxation for the 19-pair affine-offset family and require the returned candidate to pass exact full-interval quadratic verification",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = build_report(args.root.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
