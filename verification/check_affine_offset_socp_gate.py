#!/usr/bin/env python3
"""Exact SOCP reformulation and reproducibility gate for Run198.

This checker deliberately does not solve the affine-offset synthesis problem.
It proves the algebraic equivalence between every 2 by 2 S-lemma LMI and one
three-dimensional Lorentz-cone constraint, inventories the frozen problem
size, and records whether this runtime has a genuine conic solver.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import platform
import shutil
from fractions import Fraction as F
from pathlib import Path


CONIC_MODULES = ("clarabel", "scs", "cvxpy", "cvxopt", "ecos")
CONIC_EXECUTABLES = ("clarabel", "scs", "mosek", "gurobi_cl", "cplex")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_psd_soc_identity(q00: F, q01: F, q11: F) -> dict:
    """Check the exact algebra behind ``[[q00,q01],[q01,q11]] >= 0``.

    The Lorentz form is ``||(2*q01, q00-q11)||_2 <= q00+q11``.  Squaring
    introduces no ambiguity once the right hand side is constrained nonnegative.
    """
    trace = q00 + q11
    norm_squared = (2 * q01) ** 2 + (q00 - q11) ** 2
    trace_squared = trace**2
    determinant = q00 * q11 - q01**2
    lhs_minus_rhs = trace_squared - norm_squared
    return {
        "identity": lhs_minus_rhs == 4 * determinant,
        "trace": trace,
        "norm_squared": norm_squared,
        "determinant": determinant,
        "lhs_minus_rhs": lhs_minus_rhs,
        "psd_by_minors": q00 >= 0 and q11 >= 0 and determinant >= 0,
        "psd_by_soc_squared": trace >= 0 and trace_squared >= norm_squared,
    }


def problem_size(facets: int, vertices: int, state_dimension: int) -> dict:
    """Return counts for the frozen, uneliminated affine-offset formulation.

    There are two coefficients per facet offset, two per scalar vertex torque,
    one common-core offset per facet, and one S-lemma multiplier per
    vertex/facet pair.  Opposite facet offsets are tied coefficient-wise by
    ``facets`` scalar equalities (two equalities for each of ``facets/2`` pairs).
    """
    interval_pairs = facets * vertices
    raw_variables = 2 * facets + 2 * vertices + facets + interval_pairs
    pair_equalities = facets
    return {
        "facets": facets,
        "vertices": vertices,
        "state_dimension": state_dimension,
        "soc_constraints": interval_pairs,
        "soc_dimension_each": 3,
        "offset_coefficient_variables": 2 * facets,
        "vertex_torque_coefficient_variables": 2 * vertices,
        "common_core_offset_variables": facets,
        "slemma_multiplier_variables": interval_pairs,
        "raw_scalar_variables": raw_variables,
        "pair_offset_coefficient_equalities": pair_equalities,
        "effective_scalar_variables_after_pair_equalities": raw_variables - pair_equalities,
        "configuration_endpoint_inequalities": 2 * facets * vertices,
        "hard_state_endpoint_inequalities": 2 * vertices * state_dimension * 2,
        "torque_endpoint_inequalities": 2 * vertices * 2,
        "common_core_endpoint_inequalities": facets * 2,
        "offset_nonnegativity_endpoint_inequalities": facets * 2,
        "slemma_multiplier_nonnegativity_inequalities": interval_pairs,
        "counting_scope": (
            "raw formulation; no common-core pair symmetry is imposed and no redundant "
            "linear row is removed"
        ),
    }


def solver_inventory() -> dict:
    modules = {name: importlib.util.find_spec(name) is not None for name in CONIC_MODULES}
    executables = {name: shutil.which(name) is not None for name in CONIC_EXECUTABLES}
    return {
        "python_modules": modules,
        "executables": executables,
        "usable_conic_solver": any(modules.values()) or any(executables.values()),
        "scipy_linprog_is_not_conic": True,
    }


def _json_fractions(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {key: _json_fractions(item) for key, item in value.items()}
    return value


def build_report(root: Path) -> dict:
    examples = {
        "positive_definite": verify_psd_soc_identity(F(3, 2), F(-2, 3), F(5, 4)),
        "indefinite": verify_psd_soc_identity(F(1), F(2), F(1)),
        "negative_definite": verify_psd_soc_identity(F(-1), F(0), F(-1)),
    }
    dependencies = [
        "verification/check_affine_offset_socp_gate.py",
        "verification/test_affine_offset_socp_gate.py",
        "verification/check_scalar_interval_slemma.py",
        "docs/research/run198_literature_gate.md",
    ]
    inventory = solver_inventory()
    return {
        "run": 198,
        "question": "Can the frozen 6080 small LMIs be posed and solved reproducibly in this runtime?",
        "soc_equivalence": {
            "matrix": "Q=[[q00,q01],[q01,q11]]",
            "lorentz_constraint": "norm([2*q01,q00-q11],2) <= q00+q11",
            "exact_identity": "(q00+q11)^2-(4*q01^2+(q00-q11)^2)=4*det(Q)",
            "equivalence_exact_for_2_by_2_psd": True,
        },
        "identity_examples": _json_fractions(examples),
        "problem_size": problem_size(facets=38, vertices=160, state_dimension=4),
        "solver_inventory": inventory,
        "evidence_level": "DERIVED",
        "numerical_feasibility": "OPEN",
        "solver_gate": "blocked" if not inventory["usable_conic_solver"] else "available",
        "gate_A_status": "blocked",
        "invalid_substitutes": [
            "scipy.optimize.linprog/HiGHS because the Lorentz cones are nonpolyhedral",
            "finite scheduling grids because they do not certify the full interval",
            "generic nonlinear local optimization because success is not a conic feasibility certificate",
        ],
        "proves_four_state_rci": False,
        "proves_six_state_safety": False,
        "proves_recursive_feasibility": False,
        "dependencies_sha256": {path: _sha256(root / path) for path in dependencies},
        "runtime": {"python": platform.python_version()},
        "next_problem": (
            "provide a locked SOCP solver, solve the frozen formulation, and independently audit "
            "all returned interval quadratics and linear endpoint constraints"
        ),
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
