#!/usr/bin/env python3
"""Exact first-edge counterexample to the Run168 local aerodynamic target."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

from check_cycle_lifted_zonotope import (
    CYCLE_LENGTHS,
    age_zonotopes,
    least_mode_zero_box,
    lift_cycle,
    problem_data,
)


ROOT = Path(__file__).resolve().parents[1]
RUN168_TARGET = F(89401829, 65520000)


def _support(row):
    return sum((abs(value) for value in row), F(0))


def local_aerodynamic_counterexample_certificate():
    config, A0, G0, A1, G1, _ = problem_data()
    cycles = [lift_cycle(length, A0, G0, A1, G1) for length in CYCLE_LENGTHS]
    mode14 = age_zonotopes(least_mode_zero_box(cycles), A0, G0)[14]

    horizontal_source = mode14[2]
    vertical_source = mode14[3]
    disjoint = all(not (x and z) for x, z in zip(horizontal_source, vertical_source))
    horizontal_halfwidth = _support(horizontal_source) + abs(G1[2][0])
    vertical_halfwidth = _support(vertical_source) + abs(G1[3][1])

    # Choose independent source/residual signs for +e_vx and -e_vz.
    source_signs = []
    for x, z in zip(horizontal_source, vertical_source):
        if x:
            source_signs.append(F(1) if x > 0 else F(-1))
        elif z:
            source_signs.append(F(-1) if z > 0 else F(1))
        else:
            source_signs.append(F(0))
    reached_x = sum((g * s for g, s in zip(horizontal_source, source_signs)), F(0)) + abs(G1[2][0])
    reached_z = sum((g * s for g, s in zip(vertical_source, source_signs)), F(0)) - abs(G1[3][1])
    jointly_reached = reached_x == horizontal_halfwidth and reached_z == -vertical_halfwidth

    nominal_vx = F(3) - horizontal_halfwidth
    nominal_vz = F(-1, 4)
    physical_vx = nominal_vx + horizontal_halfwidth
    physical_vz = nominal_vz - vertical_halfwidth
    wind_x, wind_z = F(-1, 2), F(1, 2)
    relative_x = physical_vx - wind_x
    relative_z = physical_vz - wind_z
    pitch = F(0)

    nominal = config["mpc"]["ancillary_rci_contract"]["nominal_state_domain"]
    domain = config["domain"]
    wind_bounds = config["plant"]["wind_bounds_m_s"]
    domains_ok = (
        F(str(nominal["lower"][2])) <= nominal_vx <= F(str(nominal["upper"][2]))
        and F(str(nominal["lower"][3])) <= nominal_vz <= F(str(nominal["upper"][3]))
        and F(str(domain["state_lower"][2])) <= physical_vx <= F(str(domain["state_upper"][2]))
        and F(str(domain["state_lower"][3])) <= physical_vz <= F(str(domain["state_upper"][3]))
        and F(str(wind_bounds[0][0])) <= wind_x <= F(str(wind_bounds[0][1]))
        and F(str(wind_bounds[1][0])) <= wind_z <= F(str(wind_bounds[1][1]))
        and F(str(domain["state_lower"][4])) <= pitch <= F(str(domain["state_upper"][4]))
    )

    # At phi=0 the thrust/cosine mismatch vanishes.  Since
    # sqrt(r_z^2+0.04) > |r_z|, the exact aerodynamic magnitude is strictly
    # greater than this rational expression for r_z<0.
    rational_lower_bound = F(3, 20) * relative_z * relative_z + F(1, 50) * relative_x * relative_x
    strict_excess = rational_lower_bound - RUN168_TARGET

    expected = (
        disjoint
        and jointly_reached
        and horizontal_halfwidth == F(113619923, 40000000)
        and vertical_halfwidth == F(152955031, 72000000)
        and nominal_vx == F(6380077, 40000000)
        and physical_vz == F(-170955031, 72000000)
        and relative_z == F(-206955031, 72000000)
        and rational_lower_bound == F(51297584856210961, 34560000000000000)
        and strict_excess == F(376792429915197451, 3144960000000000000)
        and domains_ok
        and strict_excess > 0
    )
    if not expected:
        raise AssertionError("local aerodynamic counterexample changed")

    return {
        "j14_return_velocity_seed": {
            "horizontal_halfwidth": horizontal_halfwidth,
            "vertical_halfwidth": vertical_halfwidth,
            "source_generator_supports_disjoint": disjoint,
            "opposite_vertical_and_horizontal_endpoints_jointly_reachable": jointly_reached,
        },
        "admissible_first_edge_witness": {
            "nominal_velocity": (nominal_vx, nominal_vz),
            "physical_velocity": (physical_vx, physical_vz),
            "wind": (wind_x, wind_z),
            "relative_velocity": (relative_x, relative_z),
            "pitch": pitch,
            "all_configured_domains_satisfied": domains_ok,
        },
        "first_edge_obstruction": {
            "identity": "abs(aero_z)>3/20*r_z^2+1/50*r_x^2_at_negative_r_z_and_zero_pitch",
            "rational_lower_bound": rational_lower_bound,
            "run168_target": RUN168_TARGET,
            "strict_excess": strict_excess,
            "strictly_exceeds_target": strict_excess > 0,
        },
    }


def run():
    return {
        "status": "pass",
        "claim": "reachable_j14_return_state_breaks_run168_local_residual_target_on_first_edge",
        **local_aerodynamic_counterexample_certificate(),
        "frozen_j14_local_residual_route_impossible": True,
        "all_alternative_seed_or_model_contracts_ruled_out": False,
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
        "verification/check_vertical_local_aerodynamic_counterexample.py",
        "verification/test_vertical_local_aerodynamic_counterexample.py",
        "verification/check_cycle_lifted_zonotope.py",
        "configs/planar_baseline.json",
        "src/smf_mpc/plant.py",
        "docs/learning/105_vertical_local_aerodynamic_counterexample.md",
        "docs/literature/READ_PAPERS.md",
        "docs/research/run169_literature_gate.md",
        "docs/research/run169_research_log.md",
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
