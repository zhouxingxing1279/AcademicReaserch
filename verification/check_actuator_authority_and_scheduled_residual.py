#!/usr/bin/env python3
"""Actuator-authority and disturbance-contract audit for the planar LPV baseline.

This script deliberately removes the static ancillary feedback structure. It asks a
more basic question: for the worst constant horizontal residual and the hard state/
torque constraints, is the low-thrust plant itself incapable of reaching the
corresponding disturbance-balancing equilibrium?

The answer is computed with a linear program. We compare the repository's single
global residual half-width with the semantically tighter thrust-conditioned residual
half-width that follows from the same analytic remainder formula.

The LP result is numerical evidence from HiGHS, not a formal rational certificate.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import linprog

DT = 0.02
J = 0.02
T_LOW = 4.905
T_HIGH = 14.715
PHI_MAX = 0.45
AERO_X = 1.880
TAU_LIMIT = 0.08
STATE_LIMITS = np.array([5.0, 3.0, 0.45, 2.0])  # px, vx, phi, omega


def residual_halfwidth(T: float) -> float:
    """Semantic bound after keeping -T*phi in A(T): aero + T*(phi-sin(phi))."""
    return AERO_X + T * PHI_MAX**3 / 6.0


def matrices(T: float):
    A = np.eye(4)
    A[0, 1] = DT
    A[1, 2] = -DT * T
    A[2, 3] = DT
    B = np.array([0.0, 0.0, 0.0, DT / J])
    return A, B


def solve_peak_torque(T: float, horizon: int, disturbance: float):
    """Minimize peak |tau| while reaching the constant-disturbance equilibrium."""
    A, B = matrices(T)
    w = np.array([0.0, DT * disturbance, 0.0, 0.0])
    nx = 4 * (horizon + 1)
    nu = horizon
    nvar = nx + nu + 1
    t_idx = nvar - 1

    c = np.zeros(nvar)
    c[t_idx] = 1.0

    def xi(k, j):
        return 4 * k + j

    def ui(k):
        return nx + k

    Aeq = []
    beq = []
    for j in range(4):
        row = np.zeros(nvar)
        row[xi(0, j)] = 1.0
        Aeq.append(row)
        beq.append(0.0)

    for k in range(horizon):
        for j in range(4):
            row = np.zeros(nvar)
            row[xi(k + 1, j)] = 1.0
            for q in range(4):
                row[xi(k, q)] -= A[j, q]
            row[ui(k)] -= B[j]
            Aeq.append(row)
            beq.append(w[j])

    terminal = {1: 0.0, 2: disturbance / T, 3: 0.0}
    for j, value in terminal.items():
        row = np.zeros(nvar)
        row[xi(horizon, j)] = 1.0
        Aeq.append(row)
        beq.append(value)

    Aub = []
    bub = []
    for k in range(horizon + 1):
        for j, limit in enumerate(STATE_LIMITS):
            row = np.zeros(nvar)
            row[xi(k, j)] = 1.0
            Aub.append(row)
            bub.append(limit)
            Aub.append(-row)
            bub.append(limit)

    for k in range(horizon):
        row = np.zeros(nvar)
        row[ui(k)] = 1.0
        row[t_idx] = -1.0
        Aub.append(row)
        bub.append(0.0)
        row = np.zeros(nvar)
        row[ui(k)] = -1.0
        row[t_idx] = -1.0
        Aub.append(row)
        bub.append(0.0)

    bounds = [(None, None)] * (nvar - 1) + [(0.0, None)]
    result = linprog(
        c,
        A_ub=np.asarray(Aub),
        b_ub=np.asarray(bub),
        A_eq=np.asarray(Aeq),
        b_eq=np.asarray(beq),
        bounds=bounds,
        method="highs",
    )
    if not result.success:
        return {"success": False, "message": result.message}

    states = result.x[:nx].reshape(horizon + 1, 4)
    controls = result.x[nx:nx + nu]
    return {
        "success": True,
        "peak_torque_optimum": float(result.fun),
        "state_max_abs": np.max(np.abs(states), axis=0).tolist(),
        "terminal_state": states[-1].tolist(),
        "max_abs_control": float(np.max(np.abs(controls))) if len(controls) else 0.0,
        "solver_message": result.message,
    }


def first_horizon_within_limit(T: float, disturbance: float, max_horizon: int):
    """Binary-search the first horizon with optimal peak torque <= hard limit."""
    lo, hi = 1, max_horizon
    hi_res = solve_peak_torque(T, hi, disturbance)
    if (not hi_res["success"]) or hi_res["peak_torque_optimum"] > TAU_LIMIT:
        return None
    while lo < hi:
        mid = (lo + hi) // 2
        res = solve_peak_torque(T, mid, disturbance)
        ok = res["success"] and res["peak_torque_optimum"] <= TAU_LIMIT
        if ok:
            hi = mid
        else:
            lo = mid + 1
    cur = solve_peak_torque(T, lo, disturbance)
    prev = solve_peak_torque(T, lo - 1, disturbance) if lo > 1 else None
    return {"first_horizon": lo, "first": cur, "previous": prev}


def run():
    global_bound = residual_halfwidth(T_HIGH)
    scheduled_bound = residual_halfwidth(T_LOW)
    cases = {}
    for name, bound, max_h in [
        ("single_global_bound", global_bound, 500),
        ("thrust_conditioned_bound", scheduled_bound, 250),
    ]:
        threshold = first_horizon_within_limit(T_LOW, bound, max_h)
        phi_eq = bound / T_LOW
        cases[name] = {
            "disturbance_halfwidth": bound,
            "equilibrium_phi": phi_eq,
            "phi_headroom": PHI_MAX - phi_eq,
            "maximum_horizontal_deceleration_at_phi_limit": T_LOW * PHI_MAX - bound,
            "first_horizon_under_tau_limit": threshold,
        }

    global_N = cases["single_global_bound"]["first_horizon_under_tau_limit"]["first_horizon"]
    sched_N = cases["thrust_conditioned_bound"]["first_horizon_under_tau_limit"]["first_horizon"]
    return {
        "scope": "controller-structure-independent low-thrust actuator-authority audit",
        "model": "[px,vx,phi,omega], vx+=vx-dt*T*phi+dt*r_x, omega+=omega+(dt/J)*tau",
        "T_low": T_LOW,
        "T_high": T_HIGH,
        "hard_state_limits": STATE_LIMITS.tolist(),
        "hard_torque_limit": TAU_LIMIT,
        "residual_formula": "|r_x(T)| <= 1.880 + T*0.45^3/6 after retaining -T*phi in A(T)",
        "cases": cases,
        "comparison": {
            "global_first_horizon_ticks": global_N,
            "scheduled_first_horizon_ticks": sched_N,
            "global_first_horizon_seconds": global_N * DT,
            "scheduled_first_horizon_seconds": sched_N * DT,
            "horizon_reduction_ticks": global_N - sched_N,
            "relative_horizon_reduction": 1.0 - sched_N / global_N,
        },
        "interpretation": [
            "A feasible trajectory exists even under the single global disturbance bound, so failure of a particular static ancillary gain is not an actuator-authority impossibility proof.",
            "Using the same analytic residual formula conditioned on the known thrust value strictly enlarges the certified maneuver authority; this is a valid model-contract refinement, not a data-fitted shrinkage.",
            "The LPs are numerical HiGHS results. They distinguish controller-structure failure from plant-level feasibility, but they are not rational/Farkas formal certificates.",
        ],
        "versions": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
    }


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists():
        ap.error("output must not already exist")
    out = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps(out, indent=2))
