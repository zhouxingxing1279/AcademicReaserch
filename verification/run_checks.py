#!/usr/bin/env python3
"""Reproducible finite algebra checks; not control experiments or certificates."""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import linprog

SEED = 20260908
RNG = np.random.default_rng(SEED)
CHECKS = []


def record(name, passed, **details):
    CHECKS.append({"name": name, "passed": bool(passed), **details})


def planar_step(x, u):
    # State [px,pz,vx,vz,phi,omega], input [T,tau].
    dt, mass, inertia, gravity = 0.02, 1.0, 0.02, 9.81
    px, pz, vx, vz, phi, omega = x
    thrust, torque = u
    return x + dt * np.array([vx, vz, -thrust / mass * np.sin(phi),
                             thrust / mass * np.cos(phi) - gravity,
                             omega, torque / inertia])


def finite_difference(fun, x, h=1e-6):
    return np.column_stack([(fun(x + h * d) - fun(x - h * d)) / (2 * h)
                            for d in np.eye(len(x))])


def check_planar():
    x = np.zeros(6)
    u = np.array([9.81, 0.0])
    A = np.eye(6)
    A[0, 2] = A[1, 3] = A[4, 5] = 0.02
    A[2, 4] = -0.02 * 9.81
    B = np.zeros((6, 2))
    B[3, 0], B[5, 1] = 0.02, 1.0
    err_a = float(np.max(np.abs(A - finite_difference(lambda t: planar_step(t, u), x))))
    err_b = float(np.max(np.abs(B - finite_difference(lambda t: planar_step(x, t), u))))
    hover_error = float(np.max(np.abs(planar_step(x, u) - x)))
    # A displaced horizontal position is not accidentally accelerated by gravity.
    record("planar_hover_and_jacobians", max(err_a, err_b, hover_error) < 1e-8,
           max_A_error=err_a, max_B_error=err_b, hover_error=hover_error,
           tolerance=1e-8, state_order=["px", "pz", "vx", "vz", "phi", "omega"])


def check_augmented_identity():
    max_error = 0.0
    negative_control_error = 0.0
    for _ in range(100):
        n, nu, ny = 6, 2, 3
        A = RNG.normal(size=(n, n)) / 4
        B, K = RNG.normal(size=(n, nu)), RNG.normal(size=(nu, n))
        C, L = RNG.normal(size=(ny, n)), RNG.normal(size=(n, ny)) / 10
        x, z, hatx, w = RNG.normal(size=(4, n))
        v, noise = RNG.normal(size=nu), RNG.normal(size=ny)
        e, eta = x - z, x - hatx
        u = v + K @ (e - eta)
        x_next = A @ x + B @ u + w
        z_next = A @ z + B @ v
        prior = A @ hatx + B @ u
        y_next = C @ x_next + noise
        hat_next = prior + L @ (y_next - C @ prior)
        direct = np.concatenate([x_next - z_next, x_next - hat_next])
        expected = np.concatenate([(A + B @ K) @ e - B @ K @ eta + w,
            (np.eye(n) - L @ C) @ A @ eta + (np.eye(n) - L @ C) @ w - L @ noise])
        max_error = max(max_error, float(np.max(np.abs(direct - expected))))
        # Omitting estimation-to-tracking coupling must be detected.
        wrong_e = (A + B @ K) @ e + w
        negative_control_error = max(negative_control_error, float(np.max(np.abs(direct[:n] - wrong_e))))
    record("linear_augmented_error_identity", max_error < 1e-11 and negative_control_error > 1e-2,
           trials=100, max_error=max_error, tolerance=1e-11,
           omitted_coupling_negative_control_error=negative_control_error,
           scope="Observer corrects y[k+1] after predicting with actual applied u[k].")


def check_zonotope():
    n, ng, ny = 4, 7, 2
    c, G = RNG.normal(size=n), RNG.normal(size=(n, ng))
    C, gain = RNG.normal(size=(ny, n)), RNG.normal(size=(n, ny)) / 5
    vbar = np.array([0.1, 0.2])
    transform = np.eye(n) - gain @ C
    Gnew = np.column_stack([transform @ G, -gain @ np.diag(vbar)])
    max_reconstruction_error = 0.0
    for _ in range(500):
        xi, nu = RNG.uniform(-1, 1, ng), RNG.uniform(-1, 1, ny)
        state = c + G @ xi
        y = C @ state + vbar * nu
        cnew = c + gain @ (y - C @ c)
        reconstructed = cnew + Gnew @ np.concatenate([xi, nu])
        max_reconstruction_error = max(max_reconstruction_error, float(np.max(np.abs(state - reconstructed))))
    record("measurement_strip_outer_update", max_reconstruction_error < 1e-11,
           samples=500, max_reconstruction_error=max_reconstruction_error, tolerance=1e-11,
           scope="Each feasible state has an explicit bounded generator witness; outer update is not exact intersection.")
    max_lp_error, max_sample_excess, max_box_excess = 0.0, 0.0, 0.0
    samples = c[:, None] + G @ RNG.uniform(-1, 1, (ng, 500))
    box_radius = np.sum(np.abs(G), axis=1)
    for _ in range(30):
        a = RNG.normal(size=n)
        result = linprog(-(G.T @ a), bounds=[(-1, 1)] * ng, method="highs")
        if not result.success:
            raise RuntimeError(result.message)
        exact = float(a @ c + np.sum(np.abs(G.T @ a)))
        lp = float(a @ c - result.fun)
        box_support = float(a @ c + np.abs(a) @ box_radius)
        max_lp_error = max(max_lp_error, abs(lp - exact))
        max_sample_excess = max(max_sample_excess, float(np.max(a @ samples) - lp))
        max_box_excess = max(max_box_excess, lp - box_support)
    record("zonotope_support_lp_and_box", max(max_lp_error, max_sample_excess, max_box_excess) < 1e-10,
           directions=30, samples_per_direction=500, max_lp_error=max_lp_error,
           max_sample_excess=max_sample_excess, max_box_excess=max_box_excess,
           tolerance=1e-10, scope="Ordinary zonotope LP only; does not test constrained-zonotope equality constraints.")


def affine_interval(W, b, lower, upper):
    wp, wn = np.maximum(W, 0), np.minimum(W, 0)
    return wp @ lower + wn @ upper + b, wp @ upper + wn @ lower + b


def check_network():
    W1, b1 = RNG.normal(size=(5, 2)), RNG.normal(size=5)
    W2, b2 = RNG.normal(size=(3, 5)), RNG.normal(size=3)
    lower, upper = np.array([-0.4, -0.8]), np.array([0.7, 0.3])
    lo, hi = affine_interval(W1, b1, lower, upper)
    lo, hi = affine_interval(W2, b2, np.tanh(lo), np.tanh(hi))
    lo, hi = np.tanh(lo), np.tanh(hi)
    points = RNG.uniform(lower[:, None], upper[:, None], (2, 1000))
    vals = np.tanh(W2 @ np.tanh(W1 @ points + b1[:, None]) + b2[:, None])
    excess = max(0.0, float(np.max(lo[:, None] - vals)), float(np.max(vals - hi[:, None])))
    record("tanh_mlp_interval_sample_check", excess < 1e-12, samples=1000,
           max_interval_excess=excess, tolerance=1e-12,
           scope="Random samples can falsify implementation but cannot certify an interval or physical residual.")
    # Independent one-dimensional toy truth. This is not flight data.
    a, b, coeff = RNG.normal(size=(3, 4))
    def residual(t):
        return np.sin(t) - coeff @ np.tanh(a[:, None] * np.atleast_1d(t) + b[:, None])
    grid = np.linspace(-1, 1, 41)
    cover_radius = float(np.max(np.diff(grid)) / 2)
    lip = float(1 + np.sum(np.abs(coeff * a)))
    bound = float(np.max(np.abs(residual(grid))) + lip * cover_radius)
    probe = RNG.uniform(-1, 1, 2000)
    sampled_max = float(np.max(np.abs(residual(probe))))
    record("toy_lipschitz_grid_margin", sampled_max <= bound + 1e-12,
           grid_points=41, probe_points=2000, covering_radius=cover_radius,
           analytic_residual_lipschitz_bound=lip, grid_margin_bound=bound,
           sampled_residual_max=sampled_max,
           scope="Toy sin truth has a known derivative bound; this does not establish a physical model residual bound.")


def check_schedule():
    period, max_missed_opportunities = 5, 2
    # Samples at t=0 and t=15 arrive; the opportunities t=5,10 are lost.
    next_arrival = period * (max_missed_opportunities + 1)
    empty_ticks = [t for t in range(1, next_arrival) if t not in {0, next_arrival}]
    record("sensor_schedule_max_empty_ticks", len(empty_ticks) == 14 and next_arrival == 15,
           base_dt_seconds=0.02, measurement_period_ticks=period,
           max_consecutive_missed_opportunities=max_missed_opportunities,
           max_empty_ticks=len(empty_ticks), arrival_gap_ticks=next_arrival,
           arrival_gap_seconds=next_arrival * 0.02,
           scope="14 ticks without correction, but 15 prediction transitions between delivered measurements.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Write JSON here; defaults to stdout.")
    args = parser.parse_args()
    check_planar()
    check_augmented_identity()
    check_zonotope()
    check_network()
    check_schedule()
    report = {
        "kind": "finite_algebra_smoke_checks_not_controller_validation",
        "seed": SEED,
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "environment": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
        "all_passed": all(c["passed"] for c in CHECKS),
        "checks": CHECKS,
        "limitations": ["No closed-loop controller is implemented or evaluated.",
                        "No high-fidelity or flight results are produced.",
                        "Finite sampled checks are not formal proofs or safety certificates.",
                        "No physical neural-model residual envelope has been certified."]}
    content = json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content, encoding="utf-8")
    else:
        print(content, end="")
    raise SystemExit(0 if report["all_passed"] else 1)


if __name__ == "__main__":
    main()
