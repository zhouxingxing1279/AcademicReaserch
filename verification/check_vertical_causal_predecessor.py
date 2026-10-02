#!/usr/bin/env python3
"""Exact 2-D causal predecessor primitives for the vertical product-fiber class.

The controller observes ``d=(d_pz,d_vz)`` but not the Run136 estimation
error.  Every outgoing edge of a mode is therefore projected with one shared
input variable.  This module starts with the exact polygon and predecessor
primitives; the complete mode iteration is added only after those primitives
have independent regression coverage.
"""
from __future__ import annotations

from dataclasses import dataclass
import argparse
from fractions import Fraction as F
from functools import reduce
import hashlib
from math import gcd
from pathlib import Path
import json

from check_cycle_lifted_zonotope import age_zonotopes, least_mode_zero_box, lift_cycle, problem_data


ROOT = Path(__file__).resolve().parents[1]
H = F(1, 50)
POSITION_GAIN = F(9, 2)


def _lcm(a, b):
    return abs(a * b) // gcd(a, b) if a and b else 0


def _normalize(inequality):
    values = tuple(F(value) for value in inequality)
    common = reduce(_lcm, (value.denominator for value in values), 1)
    integers = [value.numerator * (common // value.denominator) for value in values]
    divisor = reduce(gcd, (abs(value) for value in integers if value), 0) or 1
    return tuple(F(value // divisor) for value in integers)


def _cross(origin, first, second):
    return ((first[0] - origin[0]) * (second[1] - origin[1])
            - (first[1] - origin[1]) * (second[0] - origin[0]))


def _convex_hull(points):
    ordered = sorted(set(points))
    if len(ordered) <= 1:
        return ordered
    lower = []
    for point in ordered:
        while len(lower) >= 2 and _cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    upper = []
    for point in reversed(ordered):
        while len(upper) >= 2 and _cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]


@dataclass(frozen=True)
class ExactPolygon:
    facets: tuple[tuple[F, F, F], ...]
    vertices: tuple[tuple[F, F], ...]
    is_empty: bool = False

    @classmethod
    def empty(cls):
        return cls((), (), True)

    @classmethod
    def box(cls, x_halfwidth, y_halfwidth):
        return cls.from_inequalities([
            (F(1), F(0), F(x_halfwidth)),
            (F(-1), F(0), F(x_halfwidth)),
            (F(0), F(1), F(y_halfwidth)),
            (F(0), F(-1), F(y_halfwidth)),
        ])

    @classmethod
    def from_inequalities(cls, inequalities):
        cleaned = []
        for raw in inequalities:
            a, b, c = (F(value) for value in raw)
            if a == 0 and b == 0:
                if c < 0:
                    return cls.empty()
                continue
            cleaned.append(_normalize((a, b, c)))
        cleaned = sorted(set(cleaned))
        if len(cleaned) < 3:
            raise ValueError("bounded full-dimensional polygon needs at least three halfspaces")

        candidates = []
        for index, (a1, b1, c1) in enumerate(cleaned):
            for a2, b2, c2 in cleaned[index + 1:]:
                determinant = a1 * b2 - a2 * b1
                if determinant == 0:
                    continue
                point = (
                    (c1 * b2 - c2 * b1) / determinant,
                    (a1 * c2 - a2 * c1) / determinant,
                )
                if all(a * point[0] + b * point[1] <= c for a, b, c in cleaned):
                    candidates.append(point)
        hull = _convex_hull(candidates)
        if len(hull) < 3:
            return cls.empty()

        facets = []
        for first, second in zip(hull, hull[1:] + hull[:1]):
            dx = second[0] - first[0]
            dy = second[1] - first[1]
            facets.append(_normalize((dy, -dx, dy * first[0] - dx * first[1])))
        return cls(tuple(facets), tuple(hull), False)

    def contains(self, point):
        if self.is_empty:
            return False
        x, y = map(F, point)
        return all(a * x + b * y <= c for a, b, c in self.facets)


def robust_predecessor(source, edges, input_bounds):
    """Project one input shared by every edge, then intersect with ``source``."""
    if source.is_empty or any(edge["target"].is_empty for edge in edges):
        return ExactPolygon.empty()
    inequalities = []
    for edge in edges:
        A = edge["A"]
        B = edge["B"]
        direction = edge["disturbance_direction"]
        halfwidth = F(edge["disturbance_halfwidth"])
        for a, b, c in edge["target"].facets:
            state_a = a * A[0][0] + b * A[1][0]
            state_b = a * A[0][1] + b * A[1][1]
            input_coefficient = a * B[0] + b * B[1]
            disturbance_support = abs(a * direction[0] + b * direction[1]) * halfwidth
            inequalities.append((state_a, state_b, input_coefficient, c - disturbance_support))

    lower, upper = map(F, input_bounds)
    inequalities.extend([
        (F(0), F(0), F(1), upper),
        (F(0), F(0), F(-1), -lower),
    ])
    zero_input = []
    positive = []
    negative = []
    for row in inequalities:
        if row[2] > 0:
            positive.append(row)
        elif row[2] < 0:
            negative.append(row)
        else:
            zero_input.append((row[0], row[1], row[3]))

    projected = list(zero_input)
    for lower_row in negative:
        for upper_row in positive:
            beta_lower = lower_row[2]
            beta_upper = upper_row[2]
            projected.append((
                beta_upper * lower_row[0] - beta_lower * upper_row[0],
                beta_upper * lower_row[1] - beta_lower * upper_row[1],
                beta_upper * lower_row[3] - beta_lower * upper_row[3],
            ))
    projected.extend(source.facets)
    return ExactPolygon.from_inequalities(projected)


def vertical_problem_data():
    config, A0, G0, A1, G1, _ = problem_data()
    cycles = [lift_cycle(length, A0, G0, A1, G1) for length in (5, 10, 15)]
    mode_zero_box = least_mode_zero_box(cycles)
    zonotopes = age_zonotopes(mode_zero_box, A0, G0)
    q_halfwidths = [
        sum(abs(Z[1][column] + H * Z[3][column]) for column in range(len(Z[0])))
        for Z in zonotopes
    ]
    vertical_eta_supports = [
        (
            sum(abs(value) for value in Z[1]),
            sum(abs(value) for value in Z[3]),
        )
        for Z in zonotopes
    ]
    nominal = config["mpc"]["ancillary_rci_contract"]["nominal_state_domain"]
    position_error_limit = min(
        config["domain"]["state_upper"][1] - nominal["upper"][1],
        nominal["lower"][1] - config["domain"]["state_lower"][1],
    )
    velocity_error_limit = min(
        config["domain"]["state_upper"][3] - nominal["upper"][3],
        nominal["lower"][3] - config["domain"]["state_lower"][3],
    )
    source_halfwidths = [
        (position_error_limit - eta_position, velocity_error_limit - eta_velocity)
        for eta_position, eta_velocity in vertical_eta_supports
    ]
    return {
        "q_halfwidths": q_halfwidths,
        "vertical_eta_supports": vertical_eta_supports,
        "source_halfwidths": source_halfwidths,
        "input_bounds": tuple(config["mpc"][key][0] for key in (
            "ancillary_correction_lower", "ancillary_correction_upper"
        )),
        "measurement_noise_halfwidth": config["sensing"]["observed_noise_halfwidth"]["pz"],
    }


def _same_polygon(first, second):
    return first.is_empty == second.is_empty and set(first.facets) == set(second.facets)


def iterate_vertical_product_fiber(max_iterations):
    """Run the descending exact predecessor sequence for the product-fiber class."""
    if max_iterations < 0:
        raise ValueError("max_iterations must be nonnegative")
    data = vertical_problem_data()
    config = json.loads((ROOT / "configs/planar_baseline.json").read_text(), parse_float=F)
    graph = config["mpc"]["ancillary_rci_contract"]["mode_graph"]["edges"]
    outgoing = {mode: [] for mode in range(15)}
    for source, target, label in graph:
        outgoing[source].append((target, label))
    edge_counts = {mode: len(rows) for mode, rows in outgoing.items()}
    sources = [ExactPolygon.box(*halfwidths) for halfwidths in data["source_halfwidths"]]
    current = list(sources)
    fixed_point = False
    completed = 0
    dynamics = ((F(1), H), (F(0), F(1)))
    input_map = (F(0), H)
    for iteration in range(max_iterations):
        next_sets = []
        for mode in range(15):
            edge_models = []
            for target, label in outgoing[mode]:
                success = label == "success"
                edge_models.append({
                    "A": dynamics,
                    "B": input_map,
                    "target": current[target],
                    "disturbance_direction": (
                        F(1) if success else F(0),
                        POSITION_GAIN if success else F(0),
                    ),
                    "disturbance_halfwidth": (
                        data["q_halfwidths"][mode] + data["measurement_noise_halfwidth"]
                        if success else F(0)
                    ),
                })
            next_sets.append(robust_predecessor(
                sources[mode], edge_models, data["input_bounds"]
            ))
        completed = iteration + 1
        fixed_point = all(_same_polygon(old, new) for old, new in zip(current, next_sets))
        current = next_sets
        if fixed_point or any(polygon.is_empty for polygon in current):
            break
    return {
        "iterations": completed,
        "sets": current,
        "source_sets": sources,
        "outgoing_edge_counts": edge_counts,
        "fixed_point": fixed_point,
        "is_rci_certificate": fixed_point and all(not polygon.is_empty for polygon in current),
        "evidence_level": (
            "exact_product_fiber_rci_fixed_point_certificate"
            if fixed_point and all(not polygon.is_empty for polygon in current)
            else "finite_outer_predecessor_prefix_not_an_rci_certificate"
        ),
    }


def mode14_product_fiber_obstruction():
    """Return the exact width obstruction on the forced mode-14 success edge."""
    data = vertical_problem_data()
    success_velocity_spread = POSITION_GAIN * (
        data["q_halfwidths"][14] + data["measurement_noise_halfwidth"]
    )
    largest_mode_zero_velocity_halfwidth = data["source_halfwidths"][0][1]
    strict_excess = success_velocity_spread - largest_mode_zero_velocity_halfwidth

    first_step = iterate_vertical_product_fiber(max_iterations=1)
    config = json.loads((ROOT / "configs/planar_baseline.json").read_text(), parse_float=F)
    edges = config["mpc"]["ancillary_rci_contract"]["mode_graph"]["edges"]
    mandatory_miss_path = all([mode, mode + 1, "miss"] in edges for mode in range(14))
    forced_success = [14, 0, "success"] in edges
    mode14_empty = first_step["sets"][14].is_empty
    if not (strict_excess > 0 and mode14_empty and mandatory_miss_path and forced_success):
        raise AssertionError("mode-14 product-fiber obstruction did not close")
    return {
        "success_velocity_spread": success_velocity_spread,
        "largest_mode_zero_velocity_halfwidth": largest_mode_zero_velocity_halfwidth,
        "strict_excess": strict_excess,
        "mode14_predecessor_is_empty": mode14_empty,
        "mandatory_mode_zero_to_fourteen_miss_path": mandatory_miss_path,
        "mode14_success_is_forced": forced_success,
        "required_initialization_is_impossible": True,
        "evidence_level": "exact_nonexistence_for_product_fiber_candidate_class",
    }


def run():
    data = vertical_problem_data()
    first_step = iterate_vertical_product_fiber(max_iterations=1)
    obstruction = mode14_product_fiber_obstruction()
    negative_control = run141_negative_control()
    return {
        "status": "pass",
        "claim": "no_nonempty_required_product_fiber_rci_multiset",
        "candidate_class": "mode_indexed_Run136_estimation_zonotope_times_observed_d_polygon",
        "evidence_level": obstruction["evidence_level"],
        "mode14_obstruction": obstruction,
        "run141_negative_control": negative_control,
        "first_predecessor": {
            "empty_modes": [mode for mode, polygon in enumerate(first_step["sets"])
                            if polygon.is_empty],
            "facet_counts": [len(polygon.facets) for polygon in first_step["sets"]],
            "non_axis_aligned_modes": [
                mode for mode, polygon in enumerate(first_step["sets"])
                if any(a != 0 and b != 0 for a, b, _ in polygon.facets)
            ],
            "outgoing_edge_counts": first_step["outgoing_edge_counts"],
            "is_rci_certificate": first_step["is_rci_certificate"],
        },
        "run136_vertical_supports": {
            "q_halfwidths": data["q_halfwidths"],
            "eta_coordinate_supports": data["vertical_eta_supports"],
            "largest_admissible_d_halfwidths": data["source_halfwidths"],
        },
        "general_output_feedback_rci_nonexistence_proved": False,
        "limitations": [
            "joint_eta_d_information_set_remains_open",
            "history_dependent_output_feedback_policy_remains_open",
            "horizontal_attitude_and_torque_coordinates_are_not_synthesized",
            "no_terminal_shift_or_recursive_feasibility_certificate",
            "no_conservatism_or_closed_loop_performance_advantage_claim",
        ],
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
        "verification/check_vertical_causal_predecessor.py",
        "verification/test_vertical_causal_predecessor.py",
        "verification/check_cycle_lifted_zonotope.py",
        "verification/check_vertical_fiber_causality_gap.py",
        "configs/planar_baseline.json",
        "docs/research/run142_literature_gate.md",
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
        "empty_modes": encoded["first_predecessor"]["empty_modes"],
        "strict_excess": encoded["mode14_obstruction"]["strict_excess"],
        "evidence_level": encoded["evidence_level"],
    }, ensure_ascii=False, indent=2))


def run141_negative_control():
    from check_vertical_fiber_causality_gap import run as run_gap

    gap = run_gap()
    q_halfwidth = vertical_problem_data()["q_halfwidths"][4]
    noise_halfwidth = F(1, 50)
    source = ExactPolygon.box(F(1), F(1))
    target = ExactPolygon.box(q_halfwidth + noise_halfwidth, F(13, 20))
    predecessor = robust_predecessor(source, [{
        "A": ((F(1), H), (F(0), F(1))),
        "B": (F(0), H),
        "target": target,
        "disturbance_direction": (F(1), POSITION_GAIN),
        "disturbance_halfwidth": q_halfwidth + noise_halfwidth,
    }], vertical_problem_data()["input_bounds"])
    return {
        "full_state_hidden_policy_feasible": gap["full_state_fiber_policy"]["success_target_ok"],
        "causal_product_fiber_contains_origin": predecessor.contains((F(0), F(0))),
        "required_hidden_policy_extreme": gap["full_state_fiber_policy"]["required_extreme_correction"],
    }


if __name__ == "__main__":
    main()
