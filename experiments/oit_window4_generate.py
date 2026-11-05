"""Regenerate the solver proposals for oit_window4_certificate.py, then verify exactly."""

import json
import os
import sys
from hashlib import sha256
from pathlib import Path
from tempfile import NamedTemporaryFile

import numpy as np
import scipy
from oit_window4_certificate import (
    ACTION,
    ACTION_STATE,
    ARCHIVE,
    CASES,
    OPT_STATE,
    PREFIX_COMMAND,
    PROOF,
    REFERENCE,
    ROOT,
    WINDOW,
    Contract,
    N,
    Q,
    dot,
    earlier_state,
    history,
    rational,
    solve_square,
    upper_bound,
    verify,
)
from scipy.linalg import qr
from scipy.optimize import linprog

sys.path.insert(0, str(ROOT / "src"))
from oit_mrpi.control import TubeMPC


def rounded(value):
    return Q(f"{float(value):.12f}")


def support_lp(E, b, q, bound):
    result = linprog(
        -np.asarray(q, dtype=float),
        A_eq=np.asarray(E, dtype=float),
        b_eq=np.asarray(b, dtype=float),
        bounds=(-bound, bound),
        method="highs",
    )
    if not result.success:
        raise RuntimeError(result.message)
    return result


def primal(E, b, q):
    # A little room inside the box lets rational reconstruction fix equalities.
    result = support_lp(E, b, q, 0.99998)
    x = [rounded(v) for v in result.x]
    _, _, perm = qr(np.asarray(E, dtype=float), pivoting=True, mode="economic")
    pivots = perm[: len(E)]
    correction = solve_square(
        [[row[i] for i in pivots] for row in E], [beta - dot(row, x) for beta, row in zip(b, E)]
    )
    for j, delta in zip(pivots, correction):
        x[j] += delta
    return list(map(str, x))


def stage_bounds(model, h, endpoints_only, k=WINDOW):
    duals = []
    margins = []
    for i in range(WINDOW):
        full = i > 0 and not endpoints_only
        past = min(k, WINDOW - i)
        E, rows = model.lift(past, i, full)
        b = h.equality_rhs(k, past, full)
        stage = []
        bounds = []
        for row in rows:
            res = support_lp(E, b, row, 1.0)
            y = [rounded(-v) for v in res.eqlin.marginals]
            stage.append(list(map(str, y)))
            bounds.append(float(upper_bound(E, b, row, y)))
        margins.append(bounds)
        duals.append(stage)
    tail = np.asarray(model.static, dtype=float)
    margins = np.vstack((margins, np.tile(tail, (N + 1 - WINDOW, 1))))
    return duals, margins


def nominal_plan(ctrl, target, margins, first=None):
    z = np.asarray(target, dtype=float)
    H = np.vstack((np.zeros((4, N)), ctrl.constraint))
    b = np.r_[ctrl.hx - ctrl.Hx @ z - margins[0, :4], ctrl.bounds(z, margins)]
    bounds = [(None, None)] * (N + 1)
    if first is not None:
        bounds[0] = (float(first), float(first))
    res = linprog(
        np.r_[np.zeros(N), 1.0],
        A_ub=np.c_[H, -np.ones(len(H))],
        b_ub=b,
        bounds=bounds,
        method="highs",
    )
    if not res.success or res.fun >= 0:
        raise ValueError(f"no strict plan at {target}: {res.message}")
    return [str(rounded(x)) for x in res.x[:N]]


def build():
    model = Contract()
    ctrl = TubeMPC(window=WINDOW)
    records = {}
    for name, (target, ws, noises) in CASES.items():
        z = rational(target)
        h = history(model, z, rational(ws), rational(noises))
        duals, margins = stage_bounds(model, h, False)
        E, rows = model.lift(3, 1, False)
        endpoint = primal(E, h.equality_rhs(4, 3, False), rows[0])
        E, rows = model.lift(2, 2, True)
        previous = primal(E, h.equality_rhs(3, 2, True), rows[0])
        record = {
            "nominal_inputs": nominal_plan(ctrl, z, margins),
            "dual_by_stage_and_direction": duals,
            "endpoint_primal": endpoint,
            "previous_primal": previous,
        }
        if name in ("mixed", "plus"):
            E, rows = model.lift(3, 1, True)
            record["reference_full_primal"] = primal(E, h.equality_rhs(4, 3, True), rows[0])
        if name == "minus":
            end_duals, end_margins = stage_bounds(model, h, True)
            record["reference_endpoint_duals"] = end_duals
            record["reference_endpoint_plan"] = nominal_plan(ctrl, rational(REFERENCE), end_margins)
        if name == "mixed":
            steps = []
            opt_steps = []
            for k in range(WINDOW):
                ds, ms = stage_bounds(model, h, True, k)
                for target, cmd, records_list in (
                    (ACTION_STATE, Q(0), steps),
                    (OPT_STATE, PREFIX_COMMAND, opt_steps),
                ):
                    zpre = earlier_state(target, WINDOW - k, cmd)
                    records_list.append(
                        {"duals": ds, "plan": nominal_plan(ctrl, zpre, ms, first=cmd)}
                    )
            end_duals, end_margins = stage_bounds(model, h, True)
            record["reachable_action"] = {
                "prefix": steps,
                "endpoint_duals": end_duals,
                "common_plan": nominal_plan(ctrl, ACTION_STATE, end_margins, first=0),
                "action_plan": nominal_plan(ctrl, ACTION_STATE, margins, first=ACTION),
            }
            opt = {"prefix": opt_steps}
            for label, full in (("full", True), ("end", False)):
                E, rows = model.lift(3, 1, full)
                opt[label + "_input_primal"] = primal(E, h.equality_rhs(4, 3, full), rows[4])
            record["optimal_separation"] = opt
        records[name] = record
    return {
        "schema": "oit-window4-separation-v1",
        "controller_sha256": sha256(ARCHIVE.read_bytes()).hexdigest(),
        "proposal_environment": {
            "python": sys.version.split()[0],
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
        "cases": records,
    }


if __name__ == "__main__":
    payload = build()
    with NamedTemporaryFile(mode="w", dir=PROOF.parent, delete=False, encoding="utf-8") as f:
        tmp = Path(f.name)
        json.dump(payload, f, indent=2)
        f.write("\n")
    try:
        results = verify(tmp)
        os.replace(tmp, PROOF)
        print("Verified and saved:", ", ".join(results))
    finally:
        tmp.unlink(missing_ok=True)
