#!/usr/bin/env python3
"""Solve and independently audit the frozen 19-pair affine-offset SOCP.

The synthesis is only for the four-state lateral-attitude benchmark and the
single configuration cone frozen in Run195.  Clarabel provides a numerical
conic solve.  Candidate constraints are then recomputed independently from
the returned primal vector; no solver status is promoted to an exact proof.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import time
from dataclasses import dataclass
from fractions import Fraction as F
from pathlib import Path

import clarabel
import numpy as np
import scipy
from scipy import sparse

import check_19pair_cc_seed_cone as cc
import check_scheduling_visible_19pair_farkas as frozen


@dataclass(frozen=True)
class Layout:
    facets: int = 38
    vertices: int = 160

    @property
    def q0(self): return slice(0, self.facets)
    @property
    def q1(self): return slice(self.facets, 2 * self.facets)
    @property
    def u0(self): return slice(2 * self.facets, 2 * self.facets + self.vertices)
    @property
    def u1(self): return slice(2 * self.facets + self.vertices, 2 * self.facets + 2 * self.vertices)
    @property
    def core(self): return slice(2 * self.facets + 2 * self.vertices, 3 * self.facets + 2 * self.vertices)
    @property
    def multipliers(self): return slice(3 * self.facets + 2 * self.vertices, self.variables)
    @property
    def variables(self): return 3 * self.facets + 2 * self.vertices + self.facets * self.vertices


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _exact_inverse(matrix: list[list[F]]) -> list[list[F]]:
    size = len(matrix)
    work = [row[:] + [F(i == j) for j in range(size)] for i, row in enumerate(matrix)]
    for column in range(size):
        pivot = next(row for row in range(column, size) if work[row][column])
        work[column], work[pivot] = work[pivot], work[column]
        value = work[column][column]
        work[column] = [item / value for item in work[column]]
        for row in range(size):
            if row == column or not work[row][column]:
                continue
            factor = work[row][column]
            work[row] = [work[row][j] - factor * work[column][j] for j in range(2 * size)]
    return [row[size:] for row in work]


def frozen_geometry() -> tuple[np.ndarray, list[np.ndarray], list[list[list[F]]]]:
    halfspaces, c_float, active_sets = frozen._seed_geometry()
    normals_f = [list(normal) for normal, _ in halfspaces]
    maps_float = []
    maps_exact = []
    for active in active_sets:
        exact_active = [normals_f[index] for index in active]
        inverse = _exact_inverse(exact_active)
        exact_map = [[F(0) for _ in range(38)] for _ in range(4)]
        float_map = np.zeros((4, 38))
        for local, facet in enumerate(active):
            for row in range(4):
                exact_map[row][facet] = inverse[row][local]
                float_map[row, facet] = float(inverse[row][local])
        maps_exact.append(exact_map)
        maps_float.append(float_map)
    return c_float, maps_float, maps_exact


class Builder:
    def __init__(self, variables: int):
        self.variables = variables
        self.rows: list[int] = []
        self.columns: list[int] = []
        self.values: list[float] = []
        self.rhs: list[float] = []
        self.cones = []
        self.labels: list[str] = []

    def _append_expression(self, coefficients: dict[int, float], constant: float = 0.0):
        row = len(self.rhs)
        for column, value in coefficients.items():
            if value:
                self.rows.append(row)
                self.columns.append(column)
                self.values.append(-float(value))
        self.rhs.append(float(constant))

    def equality(self, coefficients: dict[int, float], rhs: float, label: str):
        # slack = rhs - coefficients*x = 0
        self._append_expression({key: -value for key, value in coefficients.items()}, rhs)
        self.cones.append(clarabel.ZeroConeT(1))
        self.labels.append(label)

    def nonnegative_expression(self, coefficients: dict[int, float], constant: float, label: str):
        # expression = constant + coefficients*x >= 0
        self._append_expression(coefficients, constant)
        self.cones.append(clarabel.NonnegativeConeT(1))
        self.labels.append(label)

    def soc(self, expressions: list[tuple[dict[int, float], float]], label: str):
        for coefficients, constant in expressions:
            self._append_expression(coefficients, constant)
        self.cones.append(clarabel.SecondOrderConeT(len(expressions)))
        self.labels.append(label)

    def matrix(self) -> sparse.csc_matrix:
        return sparse.csc_matrix((self.values, (self.rows, self.columns)), shape=(len(self.rhs), self.variables))


def _add(target: dict[int, float], index: int, value: float) -> None:
    target[index] = target.get(index, 0.0) + float(value)


def build_problem() -> dict:
    layout = Layout()
    C, maps, maps_exact = frozen_geometry()
    builder = Builder(layout.variables)
    nq, nv = layout.facets, layout.vertices

    # Paired opposite facets retain identical affine offsets.
    for pair in range(19):
        for block, name in ((layout.q0.start, "q0"), (layout.q1.start, "q1")):
            builder.equality({block + 2 * pair: 1.0, block + 2 * pair + 1: -1.0}, 0.0, f"pair_{name}_{pair}")

    # Endpoint-exact affine constraints.
    for vertex, vertex_map in enumerate(maps):
        product = C @ vertex_map
        for endpoint in (-1.0, 1.0):
            for facet in range(nq):
                expr = {}
                for column, coefficient in enumerate(product[facet]):
                    _add(expr, layout.q0.start + column, -coefficient)
                    _add(expr, layout.q1.start + column, -endpoint * coefficient)
                _add(expr, layout.q0.start + facet, 1.0)
                _add(expr, layout.q1.start + facet, endpoint)
                builder.nonnegative_expression(expr, 0.0, f"config_v{vertex}_s{endpoint:+g}_f{facet}")

            for coordinate, bound in enumerate((5.0, 3.0, 0.45, 2.0)):
                for sign in (-1.0, 1.0):
                    expr = {}
                    for column, coefficient in enumerate(vertex_map[coordinate]):
                        _add(expr, layout.q0.start + column, -sign * coefficient)
                        _add(expr, layout.q1.start + column, -sign * endpoint * coefficient)
                    builder.nonnegative_expression(expr, bound, f"state_v{vertex}_s{endpoint:+g}_x{coordinate}_{sign:+g}")

            for sign in (-1.0, 1.0):
                expr = {
                    layout.u0.start + vertex: -sign,
                    layout.u1.start + vertex: -sign * endpoint,
                }
                builder.nonnegative_expression(expr, float(cc.base.taum), f"torque_v{vertex}_s{endpoint:+g}_{sign:+g}")

    for facet in range(nq):
        for endpoint in (-1.0, 1.0):
            # q(endpoint) - core >= 0 and q(endpoint) >= 0.
            builder.nonnegative_expression(
                {layout.q0.start + facet: 1.0, layout.q1.start + facet: endpoint, layout.core.start + facet: -1.0},
                0.0,
                f"core_s{endpoint:+g}_f{facet}",
            )
            builder.nonnegative_expression(
                {layout.q0.start + facet: 1.0, layout.q1.start + facet: endpoint},
                0.0,
                f"offset_s{endpoint:+g}_f{facet}",
            )

    # Dynamics polynomial in normalized s, T=Tmid+Tspan*s.
    tmid = (float(cc.base.TL) + float(cc.base.TU)) / 2.0
    tspan = (float(cc.base.TU) - float(cc.base.TL)) / 2.0
    Amid = np.array([[float(value) for value in row] for row in cc.base.A(F(str(tmid)))])
    As = np.zeros((4, 4))
    As[1, 2] = -float(cc.base.h) * tspan
    B = np.array([float(value) for value in cc.base.B])
    E = np.array([float(value) for value in cc.base.E])
    support_mid = float(cc.base.d0) + float(cc.base.c) * tmid
    support_slope = float(cc.base.c) * tspan

    polynomial_data = []
    for vertex, vertex_map in enumerate(maps):
        for facet in range(nq):
            normal = C[facet]
            m0 = normal @ Amid @ vertex_map
            m1 = normal @ As @ vertex_map
            beta = float(normal @ B)
            scale = abs(float(normal @ E))
            multiplier = layout.multipliers.start + vertex * nq + facet

            a: dict[int, float] = {}
            b: dict[int, float] = {}
            c: dict[int, float] = {layout.core.start + facet: 1.0}
            for column in range(nq):
                _add(a, layout.q1.start + column, -m1[column])
                _add(b, layout.q1.start + column, -m0[column])
                _add(b, layout.q0.start + column, -m1[column])
                _add(c, layout.q0.start + column, -m0[column])
            _add(b, layout.u1.start + vertex, -beta)
            _add(c, layout.u0.start + vertex, -beta)
            a0, b0, c0 = 0.0, -scale * support_slope, -scale * support_mid

            trace = dict(a)
            for index, value in c.items(): _add(trace, index, value)
            trace0 = a0 + c0
            difference = dict(c)
            for index, value in a.items(): _add(difference, index, -value)
            _add(difference, multiplier, -2.0)
            difference0 = c0 - a0
            builder.soc([(trace, trace0), (b, b0), (difference, difference0)], f"interval_v{vertex}_f{facet}")
            builder.nonnegative_expression({multiplier: 1.0}, 0.0, f"lambda_v{vertex}_f{facet}")
            polynomial_data.append((a, a0, b, b0, c, c0))

    return {
        "layout": layout,
        "C": C,
        "maps": maps,
        "maps_exact": maps_exact,
        "A": builder.matrix(),
        "b": np.array(builder.rhs),
        "cones": builder.cones,
        "labels": builder.labels,
        "polynomials": polynomial_data,
    }


def _affine_value(coefficients: dict[int, float], constant: float, x: np.ndarray) -> float:
    return constant + sum(value * x[index] for index, value in coefficients.items())


def audit_candidate(problem: dict, x: np.ndarray) -> dict:
    layout: Layout = problem["layout"]
    minima = []
    worst = None
    for index, (a, a0, b, b0, c, c0) in enumerate(problem["polynomials"]):
        aa = _affine_value(a, a0, x)
        bb = _affine_value(b, b0, x)
        cc_value = _affine_value(c, c0, x)
        points = [-1.0, 1.0]
        if aa > 0.0:
            stationary = -bb / (2.0 * aa)
            if -1.0 < stationary < 1.0:
                points.append(stationary)
        values = [aa * point * point + bb * point + cc_value for point in points]
        minimum = min(values)
        minima.append(minimum)
        if worst is None or minimum < worst["minimum"]:
            worst = {"index": index, "vertex": index // layout.facets, "facet": index % layout.facets,
                     "minimum": minimum, "points": points, "values": values,
                     "coefficients_abc": [aa, bb, cc_value]}

    slack = problem["b"] - problem["A"] @ x
    cursor = 0
    worst_cone_margin = float("inf")
    worst_linear = float("inf")
    cone_counts = {"zero": 0, "nonnegative": 0, "soc": 0}
    for cone in problem["cones"]:
        size = cone.dim
        block = slack[cursor:cursor + size]
        name = type(cone).__name__
        if name == "ZeroConeT":
            margin = -float(np.max(np.abs(block)))
            cone_counts["zero"] += 1
        elif name == "NonnegativeConeT":
            margin = float(np.min(block))
            worst_linear = min(worst_linear, margin)
            cone_counts["nonnegative"] += 1
        else:
            margin = float(block[0] - np.linalg.norm(block[1:]))
            cone_counts["soc"] += 1
        worst_cone_margin = min(worst_cone_margin, margin)
        cursor += size
    return {
        "full_interval_minimum": float(min(minima)),
        "worst_interval_quadratic": worst,
        "worst_all_cone_margin": worst_cone_margin,
        "worst_linear_slack": worst_linear,
        "cone_counts": cone_counts,
        "candidate_passes_tolerance_1e_7": min(minima) >= -1e-7 and worst_cone_margin >= -1e-7,
    }


def audit_dual_ray(problem: dict, z: np.ndarray) -> dict:
    """Independently replay a numerical conic infeasibility certificate."""
    if z.shape != (problem["A"].shape[0],):
        raise ValueError("dual ray has the wrong dimension")
    stationarity = np.asarray(problem["A"].T @ z).reshape(-1)
    b_dot_z = float(problem["b"] @ z)
    cursor = 0
    worst_dual_margin = float("inf")
    margins = {"nonnegative": float("inf"), "soc": float("inf")}
    counts = {"zero": 0, "nonnegative": 0, "soc": 0}
    for cone in problem["cones"]:
        block = z[cursor:cursor + cone.dim]
        name = type(cone).__name__
        if name == "ZeroConeT":
            counts["zero"] += 1  # the dual of {0} is free
        elif name == "NonnegativeConeT":
            margin = float(np.min(block))
            margins["nonnegative"] = min(margins["nonnegative"], margin)
            worst_dual_margin = min(worst_dual_margin, margin)
            counts["nonnegative"] += 1
        elif name == "SecondOrderConeT":
            margin = float(block[0] - np.linalg.norm(block[1:]))
            margins["soc"] = min(margins["soc"], margin)
            worst_dual_margin = min(worst_dual_margin, margin)
            counts["soc"] += 1
        else:
            raise TypeError(f"unsupported cone in audit: {name}")
        cursor += cone.dim
    stationarity_inf = float(np.max(np.abs(stationarity)))
    return {
        "dimension": int(z.size),
        "b_dot_z": b_dot_z,
        "stationarity_inf_norm": stationarity_inf,
        "dual_ray_l2_norm": float(np.linalg.norm(z)),
        "worst_dual_cone_margin": worst_dual_margin,
        "dual_cone_margins": margins,
        "cone_counts": counts,
        "passes_tolerance_1e_7": b_dot_z < -0.99 and stationarity_inf <= 1e-7 and worst_dual_margin >= -1e-7,
    }


def solve_problem(problem: dict, *, equilibrate: bool = True) -> tuple[object, float]:
    n = problem["layout"].variables
    P = sparse.csc_matrix((n, n))
    q = np.zeros(n)
    settings = clarabel.DefaultSettings()
    settings.verbose = False
    settings.max_iter = 300
    settings.tol_feas = 1e-9
    settings.tol_gap_abs = 1e-9
    settings.tol_gap_rel = 1e-9
    settings.tol_infeas_abs = 1e-9
    settings.tol_infeas_rel = 1e-9
    settings.equilibrate_enable = equilibrate
    start = time.perf_counter()
    solution = clarabel.DefaultSolver(P, q, problem["A"], problem["b"], problem["cones"], settings).solve()
    return solution, time.perf_counter() - start


def _finite_or_none(value: float) -> float | None:
    """Keep archived reports strict-JSON compliant for infeasible solves."""
    converted = float(value)
    return converted if np.isfinite(converted) else None


def build_report(root: Path, dual_output: Path | None = None) -> dict:
    problem = build_problem()
    solution, elapsed = solve_problem(problem)
    status = str(solution.status)
    candidate = np.array(solution.x) if solution.x is not None and len(solution.x) == problem["layout"].variables else None
    audit = audit_candidate(problem, candidate) if candidate is not None and status in ("Solved", "AlmostSolved") else None
    dual_ray = np.array(solution.z) if solution.z is not None and len(solution.z) == problem["A"].shape[0] else None
    dual_audit = audit_dual_ray(problem, dual_ray) if dual_ray is not None and status in ("PrimalInfeasible", "AlmostPrimalInfeasible") else None
    dual_artifact = None
    if dual_audit is not None and dual_output is not None:
        dual_output.parent.mkdir(parents=True, exist_ok=True)
        np.save(dual_output, dual_ray, allow_pickle=False)
        dual_artifact = {"path": str(dual_output.relative_to(root)), "sha256": _sha256(dual_output)}
    alternate, alternate_elapsed = solve_problem(problem, equilibrate=False)
    alternate_ray = np.array(alternate.z) if alternate.z is not None and len(alternate.z) == problem["A"].shape[0] else None
    alternate_audit = audit_dual_ray(problem, alternate_ray) if alternate_ray is not None else None
    dependencies = [
        "verification/check_affine_offset_socp_solve.py",
        "verification/test_affine_offset_socp_solve.py",
        "verification/requirements.txt",
        "docs/research/run199_literature_gate.md",
    ]
    return {
        "run": 199,
        "question": "Is the frozen 19-pair affine-offset SOCP numerically feasible, and does a returned candidate pass an independent audit?",
        "scope": "four-state reduced lateral-attitude benchmark; one frozen 19-pair configuration cone",
        "problem": {
            "variables": problem["layout"].variables,
            "rows": int(problem["A"].shape[0]),
            "nonzeros": int(problem["A"].nnz),
            "cone_objects": len(problem["cones"]),
            "soc_constraints": sum(type(cone).__name__ == "SecondOrderConeT" for cone in problem["cones"]),
        },
        "solver": {
            "name": "Clarabel",
            "version": clarabel.__version__,
            "status": status,
            "iterations": int(solution.iterations),
            "solve_time_seconds": elapsed,
            "primal_cost": _finite_or_none(solution.obj_val),
            "primal_residual": float(solution.r_prim),
            "dual_residual": float(solution.r_dual),
        },
        "candidate_audit": audit,
        "dual_infeasibility_ray_audit": dual_audit,
        "dual_ray_artifact": dual_artifact,
        "robustness_solve_no_equilibration": {
            "status": str(alternate.status),
            "iterations": int(alternate.iterations),
            "solve_time_seconds": alternate_elapsed,
            "dual_ray_audit": alternate_audit,
        },
        "evidence_level": "NUMERIC_CHECK",
        "gate_A_status": "partial" if audit and audit["candidate_passes_tolerance_1e_7"] else "blocked",
        "proves_exact_feasibility": False,
        "proves_six_state_safety": False,
        "proves_recursive_feasibility": False,
        "dependencies_sha256": {path: _sha256(root / path) for path in dependencies},
        "runtime": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
        "next_problem": "rationalize a strictly feasible candidate or extract and independently certify an infeasibility ray before changing the configuration family",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--dual-output", type=Path, required=True)
    args = parser.parse_args()
    report = build_report(args.root.resolve(), args.dual_output.resolve())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
