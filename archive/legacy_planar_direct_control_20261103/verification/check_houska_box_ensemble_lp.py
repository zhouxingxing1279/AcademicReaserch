#!/usr/bin/env python3
"""Exact box templates and a causal graph-indexed information-ensemble LP."""
from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as F
from itertools import product
from pathlib import Path

import numpy as np
from scipy.optimize import linprog

from check_houska_vertical_adapter import run as adapter_run


ZERO = F(0)
ONE = F(1)
HALF = F(1, 2)
ROOT = Path(__file__).resolve().parents[1]


def box_template():
    """Return exact facets, configuration cone, and four box vertex maps."""
    return {
        "parameter_order": ["upper_p", "upper_v", "negative_lower_p", "negative_lower_v"],
        "Y": [
            [ONE, ZERO],
            [ZERO, ONE],
            [-ONE, ZERO],
            [ZERO, -ONE],
        ],
        "G": [
            [-ONE, ZERO, -ONE, ZERO],
            [ZERO, -ONE, ZERO, -ONE],
        ],
        "Lambda": [
            [[ONE, ZERO, ZERO, ZERO], [ZERO, ONE, ZERO, ZERO]],
            [[ONE, ZERO, ZERO, ZERO], [ZERO, ZERO, ZERO, -ONE]],
            [[ZERO, ZERO, -ONE, ZERO], [ZERO, ONE, ZERO, ZERO]],
            [[ZERO, ZERO, -ONE, ZERO], [ZERO, ZERO, ZERO, -ONE]],
        ],
    }


def _add(left, right):
    return [a + b for a, b in zip(left, right)]


def _sub(left, right):
    return [a - b for a, b in zip(left, right)]


def meta_template():
    """Return a compact center/radius meta-template for two-dimensional boxes."""
    Z = [
        [HALF, ZERO, HALF, ZERO],
        [HALF, ZERO, -HALF, ZERO],
        [-HALF, ZERO, HALF, ZERO],
        [ZERO, HALF, ZERO, -HALF],
        [ZERO, -HALF, ZERO, HALF],
        [ZERO, HALF, ZERO, HALF],
    ]
    H = [
        [ZERO, -ONE, -ONE, ZERO, ZERO, ZERO],
        [ZERO, ZERO, ZERO, -ONE, -ONE, ZERO],
        [-ONE, ZERO, ZERO, ZERO, ZERO, ZERO],
        [ZERO, ZERO, ZERO, ZERO, ZERO, -ONE],
    ]
    rp_max = [ONE, ZERO, ZERO, ZERO, ZERO, ZERO]
    rv_max = [ZERO, ZERO, ZERO, ZERO, ZERO, ONE]
    cp_choices = (
        [ZERO, ONE, ZERO, ZERO, ZERO, ZERO],
        [ZERO, ZERO, -ONE, ZERO, ZERO, ZERO],
    )
    cv_choices = (
        [ZERO, ZERO, ZERO, ONE, ZERO, ZERO],
        [ZERO, ZERO, ZERO, ZERO, -ONE, ZERO],
    )
    omega = []
    extreme_indices = []
    for cp_index, cv_index, use_rp, use_rv in product(range(2), range(2), (True, False), (True, False)):
        cp = cp_choices[cp_index]
        cv = cv_choices[cv_index]
        rp = rp_max if use_rp else [ZERO] * 6
        rv = rv_max if use_rv else [ZERO] * 6
        omega.append([
            _add(cp, rp),
            _add(cv, rv),
            _sub(rp, cp),
            _sub(rv, cv),
        ])
        if use_rp and use_rv:
            extreme_indices.append(len(omega) - 1)
    return {
        "parameter_order": [
            "position_radius",
            "position_center_upper",
            "negative_position_center_lower",
            "velocity_center_upper",
            "negative_velocity_center_lower",
            "velocity_radius",
        ],
        "Z": Z,
        "H": H,
        "Omega": omega,
        "extreme_indices": extreme_indices,
        "measurement_row_count": 1,
    }


def _matmul(left, right):
    return [
        [sum(left[row][inner] * right[inner][column] for inner in range(len(right)))
         for column in range(len(right[0]))]
        for row in range(len(left))
    ]


class _LP:
    def __init__(self):
        self.names = []
        self.objective = []
        self.rows = []

    def variable(self, name, objective=ZERO):
        index = len(self.names)
        self.names.append(name)
        self.objective.append(objective)
        return index

    def variables(self, prefix, count, objective=ZERO):
        return [self.variable(f"{prefix}[{index}]", objective) for index in range(count)]

    def le(self, name, coefficients, rhs):
        cleaned = {index: value for index, value in coefficients.items() if value}
        self.rows.append({"name": name, "coefficients": cleaned, "rhs": rhs})


def _add_coefficient(row, index, value):
    if value:
        row[index] = row.get(index, ZERO) + value


def _linear_row(matrix_row, variables):
    return {index: value for index, value in zip(variables, matrix_row) if value}


def build_graph_lp():
    """Build the fixed-point LP with control-before-packet timing."""
    adapter = adapter_run()
    box = box_template()
    meta = meta_template()
    extreme_omega = [meta["Omega"][index] for index in meta["extreme_indices"]]
    extreme_state_maps = [
        [_matmul(vertex_map, omega) for vertex_map in box["Lambda"]]
        for omega in extreme_omega
    ]
    model = _LP()
    source_z = {}
    predicted_z = {}
    controls = {}
    auxiliary = {}
    for mode in range(adapter["mode_count"]):
        source_z[mode] = model.variables(f"z[{mode}]", 6, objective=ONE)
        predicted_z[mode] = model.variables(f"pred[{mode}]", 6)
        controls[mode] = model.variables(f"u[{mode}]", 4)
        auxiliary[mode] = [model.variables(f"xi[{mode},{j}]", 4) for j in range(4)]

    success_posterior = {}
    for edge_index, (source, target, label) in enumerate(adapter["edges"]):
        if label == "success":
            success_posterior[edge_index] = model.variables(
                f"post[{source}->{target}]", 6
            )

    state_rhs = [
        adapter["tracking_error_box"]["position_halfwidth"],
        adapter["tracking_error_box"]["velocity_halfwidth"],
        adapter["tracking_error_box"]["position_halfwidth"],
        adapter["tracking_error_box"]["velocity_halfwidth"],
    ]
    input_halfwidth = adapter["correction_input_halfwidth"]
    disturbance_parameter = [
        ZERO,
        adapter["discrete_W_velocity_halfwidth"],
        ZERO,
        adapter["discrete_W_velocity_halfwidth"],
    ]

    for mode in range(adapter["mode_count"]):
        for row_index, row in enumerate(meta["H"]):
            model.le(f"source_meta[{mode},{row_index}]", _linear_row(row, source_z[mode]), ZERO)
            model.le(
                f"predicted_meta[{mode},{row_index}]",
                _linear_row(row, predicted_z[mode]),
                ZERO,
            )
        for extreme_index, state_maps in enumerate(extreme_state_maps):
            control = controls[mode][extreme_index]
            model.le(f"input_upper[{mode},{extreme_index}]", {control: ONE}, input_halfwidth)
            model.le(f"input_lower[{mode},{extreme_index}]", {control: -ONE}, input_halfwidth)
            xi = auxiliary[mode][extreme_index]
            for state_vertex, state_map in enumerate(state_maps):
                next_state_map = _matmul(adapter["A"], state_map)
                for facet, normal in enumerate(box["Y"]):
                    state_coefficients = [
                        sum(normal[axis] * state_map[axis][column] for axis in range(2))
                        for column in range(6)
                    ]
                    model.le(
                        f"state[{mode},{extreme_index},{state_vertex},{facet}]",
                        _linear_row(state_coefficients, source_z[mode]),
                        state_rhs[facet],
                    )
                    dynamic_coefficients = [
                        sum(normal[axis] * next_state_map[axis][column] for axis in range(2))
                        for column in range(6)
                    ]
                    dynamic_row = _linear_row(dynamic_coefficients, source_z[mode])
                    _add_coefficient(
                        dynamic_row,
                        control,
                        sum(normal[axis] * adapter["B"][axis][0] for axis in range(2)),
                    )
                    _add_coefficient(dynamic_row, xi[facet], -ONE)
                    model.le(
                        f"dynamics[{mode},{extreme_index},{state_vertex},{facet}]",
                        dynamic_row,
                        -disturbance_parameter[facet],
                    )
            for row_index, row in enumerate(box["G"]):
                model.le(
                    f"aux_configuration[{mode},{extreme_index},{row_index}]",
                    _linear_row(row, xi),
                    ZERO,
                )
            for row_index, row in enumerate(meta["Z"]):
                inclusion = _linear_row(row, xi)
                _add_coefficient(inclusion, predicted_z[mode][row_index], -ONE)
                model.le(
                    f"aux_to_predicted[{mode},{extreme_index},{row_index}]",
                    inclusion,
                    ZERO,
                )

    edge_constraints = []
    measurement_halfwidth = adapter["measurement_operators"]["success"]["noise_halfwidth"]
    for edge_index, (source, target, label) in enumerate(adapter["edges"]):
        edge_constraints.append({
            "source": source,
            "target": target,
            "label": label,
            "control_block": controls[source],
            "measurement_stage": "after_transition",
        })
        if label == "miss":
            for component in range(6):
                model.le(
                    f"miss[{source}->{target},{component}]",
                    {predicted_z[source][component]: ONE, source_z[target][component]: -ONE},
                    ZERO,
                )
            continue
        posterior = success_posterior[edge_index]
        for row_index, row in enumerate(meta["H"]):
            model.le(
                f"success_meta[{source}->{target},{row_index}]",
                _linear_row(row, posterior),
                ZERO,
            )
        model.le(
            f"success_measurement[{source}->{target}]",
            {posterior[0]: -ONE},
            -measurement_halfwidth,
        )
        model.le(
            f"success_position_upper_endpoint[{source}->{target}]",
            {
                predicted_z[source][1]: ONE,
                predicted_z[source][0]: ONE,
                posterior[1]: -ONE,
                posterior[0]: -ONE,
            },
            ZERO,
        )
        model.le(
            f"success_position_lower_endpoint[{source}->{target}]",
            {
                predicted_z[source][2]: ONE,
                predicted_z[source][0]: ONE,
                posterior[2]: -ONE,
                posterior[0]: -ONE,
            },
            ZERO,
        )
        for component in range(3, 6):
            model.le(
                f"success_predicted_shape[{source}->{target},{component}]",
                {predicted_z[source][component]: ONE, posterior[component]: -ONE},
                ZERO,
            )
        for component in range(6):
            model.le(
                f"success_to_target[{source}->{target},{component}]",
                {posterior[component]: ONE, source_z[target][component]: -ONE},
                ZERO,
            )

    return {
        "mode_count": adapter["mode_count"],
        "source_controls": controls,
        "predicted_ensembles": predicted_z,
        "success_posterior_ensembles": success_posterior,
        "edge_constraints": edge_constraints,
        "variable_count": len(model.names),
        "constraint_count": len(model.rows),
        "_lp": model,
    }


def _rationalize(value):
    if abs(value) < 1e-9:
        return ZERO
    return F(float(value)).limit_denominator(10**9)


def _exact_primal_replay(lp, candidate):
    violations = []
    for row in lp.rows:
        lhs = sum(value * candidate[index] for index, value in row["coefficients"].items())
        violations.append(lhs - row["rhs"])
    max_violation = max([ZERO] + violations)
    return max_violation == 0, max_violation


def numerical_dual_diagnostics(c, A, b, primal, scipy_marginals):
    """Return HiGHS inequality-dual residuals using SciPy's marginal sign convention."""
    stationarity = c - A.T @ scipy_marginals
    return {
        "duality_gap": abs(float(c @ primal - b @ scipy_marginals)),
        "stationarity_residual": float(np.max(np.abs(stationarity))),
        "dual_sign_violation": float(max(0.0, np.max(scipy_marginals))),
    }


def exact_velocity_radius_cycle_farkas_certificate(public=None):
    """Aggregate LP rows into ``0 <= -10*w_v`` on the shortest packet cycle."""
    public = build_graph_lp() if public is None else public
    lp = public["_lp"]
    by_name = {row["name"]: row for row in lp.rows}
    cycle_edges = [(0, 1, "miss"), (1, 2, "miss"), (2, 3, "miss"),
                   (3, 4, "miss"), (4, 0, "success")]
    multipliers = []
    for source, target, label in cycle_edges:
        multipliers.extend([
            (f"dynamics[{source},0,0,1]", F(1)),
            (f"dynamics[{source},0,1,3]", F(1)),
            (f"aux_to_predicted[{source},0,5]", F(2)),
        ])
        if label == "miss":
            multipliers.append((f"miss[{source}->{target},5]", F(2)))
        else:
            multipliers.extend([
                (f"success_predicted_shape[{source}->{target},5]", F(2)),
                (f"success_to_target[{source}->{target},5]", F(2)),
            ])
    aggregate = {}
    aggregate_rhs = ZERO
    for name, multiplier in multipliers:
        row = by_name[name]
        aggregate_rhs += multiplier * row["rhs"]
        for variable, coefficient in row["coefficients"].items():
            aggregate[variable] = aggregate.get(variable, ZERO) + multiplier * coefficient
    aggregate = {
        lp.names[variable]: coefficient for variable, coefficient in aggregate.items() if coefficient
    }
    disturbance = adapter_run()["discrete_W_velocity_halfwidth"]
    expected_rhs = -F(10) * disturbance
    if aggregate or aggregate_rhs != expected_rhs or aggregate_rhs >= 0:
        raise AssertionError("velocity-radius Farkas rows do not close exactly")
    return {
        "cycle": [0, 1, 2, 3, 4, 0],
        "per_edge_velocity_radius_growth": disturbance,
        "row_multipliers": [
            {"row": name, "multiplier": multiplier} for name, multiplier in multipliers
        ],
        "aggregate_coefficients": aggregate,
        "aggregate_rhs": aggregate_rhs,
        "contradiction": True,
        "interpretation": "zero linear left-hand side is bounded above by a negative number",
    }


def solve_graph_lp():
    """Solve numerically, then independently replay a rational primal candidate."""
    public = build_graph_lp()
    lp = public["_lp"]
    variable_count = len(lp.names)
    A = np.zeros((len(lp.rows), variable_count))
    b = np.zeros(len(lp.rows))
    for row_index, row in enumerate(lp.rows):
        for variable, value in row["coefficients"].items():
            A[row_index, variable] = float(value)
        b[row_index] = float(row["rhs"])
    c = np.array([float(value) for value in lp.objective])
    solution = linprog(
        c,
        A_ub=A,
        b_ub=b,
        bounds=[(None, None)] * variable_count,
        method="highs",
    )
    if not solution.success:
        if solution.status == 2:
            certificate = exact_velocity_radius_cycle_farkas_certificate(public)
            return {
                "solver_status": "infeasible",
                "solver_message": solution.message,
                "variable_count": variable_count,
                "constraint_count": len(lp.rows),
                "exact_primal_feasible": False,
                "exact_farkas_certificate": certificate,
                "invariant_information_ensemble_certified": False,
                "exact_optimality_certified": False,
                "mpc_recursive_feasibility_certified": False,
                "full_six_state_guarantee": False,
                "evidence_level": (
                    "exact_axis_aligned_box_information_ensemble_infeasibility_certificate"
                ),
                "limitations": [
                    "the certificate rejects this axis-aligned box/meta-template only",
                    "correlated polytopes or lifted state-measurement templates may remain feasible",
                    "the frozen actuator-wide disturbance envelope remains conservative",
                ],
            }
        return {
            "solver_status": "infeasible_or_failed",
            "solver_message": solution.message,
            "exact_primal_feasible": False,
            "invariant_information_ensemble_certified": False,
            "mpc_recursive_feasibility_certified": False,
            "evidence_level": "numerical_lp_failure_only",
        }
    candidate = [_rationalize(value) for value in solution.x]
    exact_feasible, exact_violation = _exact_primal_replay(lp, candidate)
    marginals = np.asarray(solution.ineqlin.marginals)
    dual_diagnostics = numerical_dual_diagnostics(c, A, b, solution.x, marginals)
    return {
        "solver_status": "optimal",
        "solver_message": solution.message,
        "objective_value_float": float(solution.fun),
        "objective_value_exact_candidate": sum(
            coefficient * value for coefficient, value in zip(lp.objective, candidate)
        ),
        "variable_count": variable_count,
        "constraint_count": len(lp.rows),
        "exact_primal": {name: value for name, value in zip(lp.names, candidate)},
        "exact_primal_feasible": exact_feasible,
        "exact_max_primal_violation": exact_violation,
        "numerical_dual": dual_diagnostics,
        "evidence_level": (
            "exact_primal_feasible_box_information_ensemble_graph_certificate"
            if exact_feasible
            else "numerical_box_information_ensemble_candidate_only"
        ),
        "invariant_information_ensemble_certified": exact_feasible,
        "exact_optimality_certified": False,
        "mpc_recursive_feasibility_certified": False,
        "full_six_state_guarantee": False,
        "limitations": [
            "the fixed actuator-wide disturbance envelope remains conservative",
            "the numerical dual is diagnostic and is not an exact optimality certificate",
            "terminal integration and shifted MPC recursive feasibility are not certified",
        ],
    }


def _encode(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {str(key): _encode(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_encode(item) for item in value]
    return value


def run():
    result = solve_graph_lp()
    result["claim"] = (
        "causal_axis_aligned_box_graph_lp_is_exactly_infeasible"
        if result["solver_status"] == "infeasible"
        else "causal_box_information_ensemble_graph_lp_result"
    )
    result["template"] = {
        "box_facets": len(box_template()["Y"]),
        "box_vertices": len(box_template()["Lambda"]),
        "meta_parameters": len(meta_template()["Z"]),
        "meta_vertices": len(meta_template()["Omega"]),
        "extreme_information_sets": len(meta_template()["extreme_indices"]),
        "measurement_coordinate": "position_radius",
    }
    result["graph"] = {
        "modes": 15,
        "edges": 17,
        "miss_edges": 14,
        "success_edges": 3,
        "control_indexing": "source_mode_and_extreme_set",
        "measurement_stage": "after_transition",
        "shared_control_branch_modes": [4, 9],
    }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError(args.output)
    result = run()
    sources = [
        "verification/check_houska_box_ensemble_lp.py",
        "verification/test_houska_box_ensemble_lp.py",
        "verification/check_houska_vertical_adapter.py",
        "configs/planar_baseline.json",
        "docs/superpowers/specs/2026-10-26-box-ensemble-graph-lp-design.md",
    ]
    result["source_sha256"] = {
        name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in sources
    }
    encoded = _encode(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(encoded, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "solver_status": encoded["solver_status"],
        "evidence_level": encoded["evidence_level"],
        "exact_primal_feasible": encoded["exact_primal_feasible"],
        "objective": encoded.get("objective_value_exact_candidate"),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
