#!/usr/bin/env python3
"""Exact sensor-ensemble row for the configured six-facet family."""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

from check_houska_vertical_adapter import run as adapter_run
from check_six_facet_measurement_gate import six_facet_template


ZERO = F(0)
ONE = F(1)
HALF = F(1, 2)
ROOT = Path(__file__).resolve().parents[1]


def _matvec(matrix, vector):
    return [sum(a * b for a, b in zip(row, vector)) for row in matrix]


def measurement_meta_row():
    """Return Z_1 y = (upper_p + negative_lower_p)/2."""
    return [HALF, ZERO, ZERO, HALF, ZERO, ZERO]


def compatible_measurement_interval(offsets, halfwidth):
    """Return all position-measurement centers compatible with P(offsets)."""
    if len(offsets) != 6:
        raise ValueError("six facet offsets are required")
    if halfwidth < 0:
        raise ValueError("measurement halfwidth must be nonnegative")
    template = six_facet_template()
    if any(value > 0 for value in _matvec(template["G"], offsets)):
        raise AssertionError("offsets are outside the six-facet configuration cone")
    vertices = [_matvec(vertex_map, offsets) for vertex_map in template["Lambda"]]
    position_max = max(vertex[0] for vertex in vertices)
    position_min = min(vertex[0] for vertex in vertices)
    if position_max != offsets[0] or position_min != -offsets[3]:
        raise AssertionError("configured position facets are not exact supports")
    lower_center = position_max - halfwidth
    upper_center = position_min + halfwidth
    meta_coordinate = sum(
        coefficient * offset
        for coefficient, offset in zip(measurement_meta_row(), offsets)
    )
    compatible = lower_center <= upper_center
    meta_compatible = meta_coordinate <= halfwidth
    if compatible != meta_compatible:
        raise AssertionError("measurement-center interval and meta row disagree")
    return {
        "position_max": position_max,
        "position_min": position_min,
        "center_interval": [lower_center, upper_center],
        "compatible": compatible,
        "measurement_meta_coordinate": meta_coordinate,
        "meta_compatible": meta_compatible,
    }


def run():
    adapter = adapter_run()
    halfwidth = adapter["measurement_operators"]["success"]["noise_halfwidth"]
    translated_boundary_offsets = [
        F(53, 150), F(-2, 5), F(-109, 300),
        F(-47, 150), F(3, 5), F(121, 300),
    ]
    witness = compatible_measurement_interval(translated_boundary_offsets, halfwidth)
    if witness["center_interval"] != [F(1, 3), F(1, 3)]:
        raise AssertionError("translated exact-boundary witness changed")
    return {
        "claim": "continuous_position_measurement_centers_need_no_enumeration",
        "evidence_level": "exact_six_facet_sensor_ensemble_measurement_row",
        "facet_order": six_facet_template()["facet_order"],
        "Z1": measurement_meta_row(),
        "measurement_halfwidth": halfwidth,
        "assumptions": [
            "G*y <= 0 for the Run186 six-facet configuration",
            "P(y) is nonempty",
            "C = [1, 0] and measurement noise is [-a, a]",
        ],
        "exact_equivalence": (
            "under the stated assumptions, exists eta: eta-C*P(y) subset [-a,a] iff "
            "[y_0-a,-y_3+a] is nonempty iff Z1*y<=a"
        ),
        "translated_boundary_witness": {
            "offsets": translated_boundary_offsets,
            **witness,
        },
        "continuous_measurement_centers_represented": True,
        "complete_Z_H_Omega_certified": False,
        "graph_invariant_information_ensemble_certified": False,
        "input_feasibility_certified": False,
        "terminal_invariance_certified": False,
        "mpc_recursive_feasibility_certified": False,
        "full_six_state_guarantee": False,
        "limitations": [
            "the equivalence requires G*y <= 0 and a nonempty configured polytope",
            "Z1 is only the measurement-compatible width coordinate",
            "the remaining Z2 rows and a fixed H/Omega configuration are unselected",
            "the control-before-packet 15-mode/17-edge graph LP is unconstructed",
            "the result is an exact representation lemma, not a controller contribution",
        ],
    }


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
        "verification/check_six_facet_sensor_ensemble.py",
        "verification/test_six_facet_sensor_ensemble.py",
        "verification/check_six_facet_measurement_gate.py",
        "verification/check_houska_vertical_adapter.py",
        "configs/planar_baseline.json",
        "docs/superpowers/specs/2026-10-27-six-facet-sensor-ensemble-design.md",
    ]
    result["source_sha256"] = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
        for name in sources
    }
    encoded = _encode(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(encoded, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "claim": encoded["claim"],
        "evidence_level": encoded["evidence_level"],
        "boundary_center": encoded["translated_boundary_witness"]["center_interval"][0],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
