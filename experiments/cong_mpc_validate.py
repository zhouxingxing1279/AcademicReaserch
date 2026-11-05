"""Frozen, equal-facet-budget gate for the proposed control-aware compression.

Run: .venv/Scripts/python.exe -m experiments.cong_mpc_validate
This is a 2-D research experiment, not a production controller or formal certificate.
"""
from dataclasses import dataclass
from itertools import product
from pathlib import Path
import csv
import hashlib
import json
import platform
import time

import numpy as np
import scipy
import scipy.sparse as sp
from scipy.linalg import solve_discrete_lyapunov
from scipy.optimize import linprog
from scipy.spatial import ConvexHull
import osqp

from experiments.cong_mpc_screen import shape, cz_predict, cz_measure, cz_support
from src.outerloop.finite_memory import FloatCZ

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "experiments/results/cong_mpc_validation"
TOL = 2e-6
BUDGETS = (6, 8, 12)
METHODS = ("uniform", "geometry", "control")
PERIODS = (1, 3, 0)
STEPS = 30
ANGLES = (0, 45, 90, 135)
RAYS = (0, 90, 180, 270)
FRACTION = .98
AUDITS = []


@dataclass
class Polygon:
    v: np.ndarray

    def __post_init__(self):
        vertices = np.unique(np.asarray(self.v, dtype=float), axis=0)
        if len(vertices) < 3:
            raise ValueError("Empty or degenerate polygon")
        hull = ConvexHull(vertices)
        self.v = vertices[hull.vertices]
        self.H = hull.equations[:, :2]
        self.b = -hull.equations[:, 2]

    def support(self, q):
        return np.max(self.v @ np.asarray(q).T, axis=0)

    def contains(self, x):
        return bool(np.max(self.H @ x - self.b) <= TOL)

    def clip(self, q, b):
        out = []
        for a, z in zip(self.v, np.roll(self.v, -1, axis=0)):
            da, dz = float(q @ a - b), float(q @ z - b)
            if da <= 0:
                out.append(a)
            if (da <= 0) != (dz <= 0):
                out.append(a + (z - a) * (da / (da - dz)))
        return Polygon(np.asarray(out))

    def predict(self, model, u):
        nominal = self.v @ model.A.T + model.B * u
        return Polygon((nominal[:, None, :] + model.wvertices[None, :, :]).reshape(-1, 2))

    def observe(self, model, y):
        return self.clip(model.C, y + model.nu).clip(-model.C, -y + model.nu)


def box(lo, hi):
    return Polygon(np.array(list(product(*zip(lo, hi)))))


def direction_key(q):
    return tuple(np.round(q / np.linalg.norm(q), 11))


class Model:
    def __init__(self, name):
        self.name = name
        self.A = np.array([[.75, .2], [-.1, .7]]) if name == "fast" else np.array([[.91, .06], [-.04, .92]])
        self.N = 6 if name == "fast" else 10
        self.B = np.array([.15, .2])
        self.W = np.full(2, .005)
        self.C = np.array([1., .4])
        self.nu = .025
        self.L = np.array([.6, .15])
        self.H = np.array([[1., 0], [-1., 0], [0, 1.], [0, -1.], [1, 1.], [-1, -1.]])
        self.H[4:] /= np.sqrt(2)
        self.limit = np.array([1.2, 1.2, .8, .8, .85, .85])
        self.Hf = self.H[:4]
        self.wvertices = np.array(list(product(*[(-w, w) for w in self.W])))
        self.terminal = box(np.full(2, -.25), np.full(2, .25))
        self.terminal_residual = float(np.max(np.abs(self.Hf @ self.A).sum(axis=1) * .25 + np.abs(self.Hf) @ self.W - .25))
        assert self.terminal_residual <= 0
        self.powers = [np.linalg.matrix_power(self.A, j) for j in range(self.N + 1)]
        self.Gamma = np.zeros((2 * self.N, self.N))
        for j in range(self.N):
            for i in range(j + 1):
                self.Gamma[2*j:2*j+2, i] = self.powers[j-i] @ self.B
        self.Phi = np.vstack(self.powers[1:])
        P = solve_discrete_lyapunov(self.A.T, np.eye(2))
        Q = sp.block_diag([np.eye(2)] * (self.N - 1) + [P]).toarray()
        self.qmap = 2 * self.Gamma.T @ Q @ self.Phi
        self.qp_P = sp.csc_matrix(np.triu(2 * (.15 * np.eye(self.N) + self.Gamma.T @ Q @ self.Gamma)))
        dirs, limits, coeff = [self.H], [self.limit], [np.zeros((6, self.N))]
        for j in range(1, self.N + 1):
            dirs.append(self.H @ self.powers[j])
            limits.append(self.limit - self.noise(self.H, j))
            coeff.append(self.H @ self.Gamma[2*(j-1):2*j])
        dirs.append(self.Hf @ self.powers[self.N])
        limits.append(np.full(4, .25) - self.noise(self.Hf, self.N))
        coeff.append(self.Hf @ self.Gamma[-2:])
        self.raw = np.vstack(dirs)
        self.limits = np.concatenate(limits)
        self.coeff = np.vstack(coeff)
        self.norms = np.linalg.norm(self.raw, axis=1)
        pool, index, mapping = [], {}, []
        for q in self.raw:
            key = direction_key(q)
            if key not in index:
                index[key] = len(pool)
                pool.append(q / np.linalg.norm(q))
            mapping.append(index[key])
        self.pool, self.mapping = np.array(pool), np.array(mapping)
        self.solver = osqp.OSQP()
        self.solver.setup(P=self.qp_P, q=np.zeros(self.N),
                          A=sp.csc_matrix(np.vstack([np.eye(self.N), self.coeff])),
                          l=np.r_[np.full(self.N, -.35), np.full(len(self.limits), -np.inf)],
                          u=np.r_[np.full(self.N, .35), np.ones(len(self.limits))],
                          eps_abs=1e-8, eps_rel=1e-8, max_iter=30000,
                          verbose=False, polishing=False, warm_starting=False)

    def noise(self, rows, steps):
        return sum(np.abs(rows @ self.powers[j]) @ self.W for j in range(steps))

    def residual(self, S, seq):
        return max(float(np.max(S.support(self.raw) + self.coeff @ seq - self.limits)),
                   float(np.max(np.abs(seq)) - .35))

    def solve(self, S, hat):
        rhs = self.limits - S.support(self.raw)
        if np.min(rhs[:6]) < -TOL:
            return None
        self.solver.update(q=self.qmap @ hat, u=np.r_[np.full(self.N, .35), rhs])
        result = self.solver.solve(raise_error=False)
        if "infeasible" in result.info.status:
            return None
        if result.info.status != "solved":
            raise RuntimeError("QP status: " + result.info.status)
        seq = result.x.copy()
        assert self.residual(S, seq) <= TOL
        return seq

    def thresholds(self, seq):
        threshold = np.full(len(self.pool), np.inf)
        np.minimum.at(threshold, self.mapping, (self.limits - self.coeff @ seq) / self.norms)
        return threshold


def enclose(S, directions):
    values = S.support(directions)
    radius = 4 * (float(np.max(np.abs(S.v))) + 1)
    P = box(np.full(2, -radius), np.full(2, radius))
    for q, b in zip(directions, values):
        P = P.clip(q, float(b))
    assert len(P.v) <= len(directions)
    assert np.max(np.abs(P.v)) < radius - 1e-5
    return P


def compress(S, model, method, budget, shifted):
    if method == "exact":
        return S, 0
    if method == "full":
        return enclose(S, model.pool), len(model.pool)
    if method == "uniform":
        angles = np.arange(budget) * 2 * np.pi / budget
        directions = np.c_[np.cos(angles), np.sin(angles)]
        return enclose(S, directions), budget
    assert method in ("geometry", "control")
    directions = model.H[:4]
    P = enclose(S, directions)
    chosen = {direction_key(q) for q in directions}
    allowed = np.array([direction_key(q) not in chosen for q in model.pool])
    exact = S.support(model.pool) if method == "geometry" else None
    queries = len(model.pool) if method == "geometry" else 4
    target = exact if method == "geometry" else model.thresholds(shifted)
    for _ in range(budget - 4):
        scores = P.support(model.pool) - target
        scores[~allowed] = -np.inf
        j = int(np.argmax(scores))
        assert allowed[j]
        allowed[j] = False
        b = float(exact[j]) if method == "geometry" else float(S.support(model.pool[j]))
        queries += int(method == "control")
        P = P.clip(model.pool[j], b)
    assert len(P.v) <= budget
    return P, queries


def boundary_case(model, angle, ray):
    G = shape(np.deg2rad(angle))
    S = Polygon(np.array(list(product((-1., 1.), repeat=G.shape[1]))) @ G.T)
    direction = np.array([np.cos(np.deg2rad(ray)), np.sin(np.deg2rad(ray))])
    mat = np.c_[model.raw @ direction, model.coeff]
    result = linprog(np.r_[-1., np.zeros(model.N)], A_ub=mat,
                     b_ub=model.limits - S.support(model.raw),
                     bounds=[(0, None)] + [(-.35, .35)] * model.N, method="highs")
    if not result.success:
        raise RuntimeError("Frozen initial case infeasible: " + result.message)
    center = FRACTION * result.x[0] * direction
    initial = Polygon(S.v + center)
    plan = model.solve(initial, center)
    assert plan is not None
    return initial, center, G, plan, float(result.x[0])


def audit_polygon(model, S, z, key):
    queries = np.vstack([model.H, model.H[:4] @ model.powers[-1]])
    maximum = 0.
    for q in queries:
        result = linprog(-q, A_ub=S.H, b_ub=S.b, bounds=[(None, None)] * 2, method="highs")
        assert result.success
        support = float(S.support(q))
        maximum = max(maximum, abs(support + result.fun), abs(support - cz_support(z, q)))
    assert maximum < TOL
    AUDITS.append({**key, "queries": len(queries), "max_support_disagreement": maximum})


def run_case(model, angle, ray, period, method, budget, case_id, initial_data, snapshots):
    initial, center, G, plan0, boundary = initial_data
    rng = np.random.default_rng(4100 + case_id)
    x = center + G @ rng.uniform(-1, 1, G.shape[1])
    noises = rng.uniform(-1, 1, (STEPS, 2)) * model.W
    measurement_noises = rng.uniform(-model.nu, model.nu, STEPS)
    hat, anchor, exact = center.copy(), initial, initial
    age, offset, shifted = 0, np.zeros(2), plan0.copy()
    z = FloatCZ(center.copy(), G.copy(), np.empty((0, G.shape[1])), np.empty(0)) if method == "exact" and case_id == 0 else None
    total_cost, rows, fallback_count, lost_count, max_faces = 0., [], 0, 0, 0
    label = dict(model=model.name, angle=angle, ray=ray, period=period,
                 method=method, budget=budget, case_id=case_id)
    for k in range(STEPS):
        observe = bool(k > 0 and period > 0 and k % period == 0)
        y = float(model.C @ x + measurement_noises[k]) if observe else None
        if observe:
            hat = hat + model.L * (y - model.C @ hat)
        started = time.perf_counter()
        if method == "exact":
            prior = exact
        else:
            if age >= model.N:
                anchor, offset, age = model.terminal, np.zeros(2), 0
                assert np.max(np.abs(shifted)) < TOL
            prior = anchor
            for _ in range(age):
                prior = prior.predict(model, 0.)
            if age:
                prior = Polygon(prior.v + offset)
        posterior = prior.observe(model, y) if observe else prior
        # Startup shares an exactly representable six-facet prior and one plan.
        construction_started = time.perf_counter()
        if k == 0:
            candidate, queries = initial, 0
        else:
            candidate, queries = compress(posterior, model, method, budget, shifted)
        construction_ms = 1000 * (time.perf_counter() - construction_started)
        shift_residual = model.residual(candidate, shifted)
        seq = model.solve(candidate, hat)
        fallback = seq is None
        if fallback:
            seq = shifted.copy()
            assert model.residual(posterior, seq) <= TOL
        else:
            if method == "exact":
                exact = posterior
            else:
                anchor, offset, age = candidate, np.zeros(2), 0
        online_ms = 1000 * (time.perf_counter() - started)
        # Independent audit cost is excluded for every method.
        if method == "exact":
            assert not fallback
            if k in (1, 2, 3):
                snapshots.append((label.copy(), k, posterior, shifted.copy(), hat.copy()))
            if z is not None:
                if observe:
                    z = cz_measure(z, model.C, y, model.nu)
                if k in (1, 3, 12, 29):
                    audit_polygon(model, posterior, z, {**label, "k": k})
        assert prior.contains(x) and posterior.contains(x)
        assert all(candidate.contains(v) for v in posterior.v)
        if not fallback:
            assert candidate.contains(x)
        actual_violation = float(np.max(model.H @ x - model.limit))
        input_violation = float(abs(seq[0]) - .35)
        assert actual_violation <= TOL and input_violation <= TOL
        assert len(anchor.v) <= budget if method not in ("exact", "full") else True
        max_faces = max(max_faces, len(exact.v) if method == "exact" else len(anchor.v))
        stage_cost = float(x @ x + .15 * seq[0]**2)
        total_cost += stage_cost
        fallback_count += int(fallback)
        lost_count += int(shift_residual > TOL)
        rows.append({**label, "k": k, "observed": int(observe), "cost": stage_cost,
                     "fallback": int(fallback), "shift_lost": int(shift_residual > TOL),
                     "shift_residual": shift_residual, "state_violation": actual_violation,
                     "input_violation": input_violation, "support_queries": queries,
                     "candidate_faces": len(candidate.v), "anchor_faces": len(exact.v) if method == "exact" else len(anchor.v),
                     "working_vertices": max(len(prior.v), len(posterior.v), len(candidate.v)),
                     "construction_ms": construction_ms, "online_ms": online_ms})
        u = float(seq[0])
        x = model.A @ x + model.B * u + noises[k]
        hat = model.A @ hat + model.B * u
        if method == "exact":
            exact = exact.predict(model, u)
            if z is not None:
                z = cz_predict(z, model.A, model.B, u, model.W)
        else:
            offset = model.A @ offset + model.B * u
            age += 1
        shifted = np.r_[seq[1:], 0.]
    assert np.max(model.H @ x - model.limit) <= TOL
    case = {**label, "cost": total_cost, "fallback_steps": fallback_count,
            "shift_lost_steps": lost_count, "max_stored_faces": max_faces,
            "boundary_radius": boundary, "completed_steps": len(rows)}
    return rows, case


def dump_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def static_compare(model, snapshots):
    rows = []
    for label, k, S, shifted, hat in snapshots:
        assert model.residual(S, shifted) <= TOL
        for budget, method in product(BUDGETS, METHODS):
            started = time.perf_counter()
            P, queries = compress(S, model, method, budget, shifted)
            build_ms = 1000 * (time.perf_counter() - started)
            violation = model.residual(P, shifted)
            seq = model.solve(P, hat)
            assert all(P.contains(v) for v in S.v)
            rows.append({**label, "method": method, "budget": budget, "k": k,
                         "shift_preserved": int(violation <= TOL), "qp_feasible": int(seq is not None),
                         "shift_residual": violation,
                         "max_direction_gap": float(np.max(P.support(model.pool) - S.support(model.pool))),
                         "support_queries": queries, "faces": len(P.v), "construction_ms": build_ms})
    return rows


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if (OUT / "summary.json").exists():
        raise RuntimeError("Results already exist; preserve the frozen run instead of overwriting it")
    started = time.perf_counter()
    steps, cases, statics, contracts = [], [], [], {}
    for name in ("fast", "slow"):
        model, snapshots = Model(name), []
        contracts[name] = {"A": model.A.tolist(), "N": model.N,
                           "template_directions": len(model.pool), "terminal_residual": model.terminal_residual}
        for case_id, (angle, ray) in enumerate(product(ANGLES, RAYS)):
            init = boundary_case(model, angle, ray)
            for period in PERIODS:
                configurations = [(method, budget) for budget in BUDGETS for method in METHODS]
                configurations.append(("full", len(model.pool)))
                rotate = case_id % len(configurations)
                configurations = [("exact", 0)] + configurations[rotate:] + configurations[:rotate]
                for method, budget in configurations:
                    sr, cr = run_case(model, angle, ray, period, method, budget, case_id, init, snapshots)
                    steps.extend(sr)
                    cases.append(cr)
            print(json.dumps({"model": name, "case": case_id, "runs": len(cases),
                              "elapsed_s": round(time.perf_counter() - started, 1)}), flush=True)
        statics.extend(static_compare(model, snapshots))
    dump_csv(OUT / "steps.csv", steps)
    dump_csv(OUT / "cases.csv", cases)
    dump_csv(OUT / "static.csv", statics)
    (OUT / "independent_audit.json").write_text(json.dumps(AUDITS, indent=2), encoding="utf-8")
    summary = {"date": "2026-11-04", "scope": "equal persistent facet cap, not equal runtime or bytes; 2D stable LTI",
               "models": contracts, "budgets": BUDGETS, "steps": STEPS,
               "cases": len(cases), "control_steps": len(steps), "static_comparisons": len(statics),
               "all_runtime_assertions_passed": True, "independent_audits": len(AUDITS),
               "elapsed_s": time.perf_counter() - started,
               "python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__, "osqp": osqp.__version__,
               "source_sha256": {str(p.relative_to(ROOT)): sha(p) for p in (Path(__file__), ROOT / "experiments/cong_mpc_screen.py", ROOT / "src/outerloop/finite_memory.py", ROOT / "docs/research/proposal/CONG_MPC_VALIDATION_PLAN.md")},
               "artifact_sha256": {p.name: sha(p) for p in OUT.glob("*") if p.suffix in (".csv", ".json")}}
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
