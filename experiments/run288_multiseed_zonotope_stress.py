"""Run288: multi-seed synthetic 12-state zonotope stress audit (not MPC)."""
import json, time
import numpy as np
from scipy.linalg import expm

DT = .02
A = np.zeros((12, 12)); B = np.zeros((12, 4))
for i in range(3):
    A[i, i+3] = 1; A[6+i, 9+i] = 1; B[9+i, 1+i] = 1
A[3, 7] = 9.81; A[4, 6] = -9.81; B[5, 0] = 1
E = np.zeros((16, 16)); E[:12, :12] = A; E[:12, 12:] = B
F = expm(E*DT); AD = F[:12, :12]; BD = F[:12, 12:]
INITIAL = np.array([.02]*3+[.04]*3+[.015]*3+[.025]*3)
PROC = np.array([.0002]*3+[.001]*3+[.0001]*3+[.0005]*3)
MEAS = np.array([.01, .01, .01, .008]); IDX = [0, 1, 2, 8]

def reduce(G, q):
    if G.shape[1] <= q: return G
    keep = np.argsort(-np.linalg.norm(G, axis=0), kind="stable")[:q]
    discard = np.ones(G.shape[1], dtype=bool); discard[keep] = False
    return np.column_stack((G[:, keep], np.diag(np.abs(G[:, discard]).sum(axis=1))))

def run(q, seed, pattern, steps=150):
    rng = np.random.default_rng(seed); truth = rng.uniform(-INITIAL, INITIAL)
    c = np.zeros(12); G = np.diag(INITIAL); maxwidth = 0.; failures = 0; peak = 0; times = []
    for k in range(1, steps+1):
        tic = time.perf_counter_ns()
        u = np.array([.1*np.sin(.02*k), .02*np.cos(.03*k), .015*np.sin(.04*k), .01*np.cos(.01*k)])
        truth = AD@truth+BD@u+rng.uniform(-PROC, PROC)
        c = AD@c+BD@u; G = np.column_stack((AD@G, np.diag(PROC)))
        receive = k%5 == 0 and (pattern == "all" or
            (pattern == "mms" and (k//5)%3 != 2) or
            (pattern == "smm" and (k//5)%3 == 0))
        if receive:
            y = truth[IDX]+rng.uniform(-MEAS, MEAS)
            for j, i in enumerate(IDX):
                v = G[i, :]; z = G@v; lam = z/(v@v+MEAS[j]**2)
                c = c+lam*(y[j]-c[i])
                G = np.column_stack((G-np.outer(lam, v), lam[:, None]*MEAS[j]))
        if q is not None: G = reduce(G, q)
        times.append((time.perf_counter_ns()-tic)/1e6)
        peak = max(peak, G.shape[1]); width = 2*np.abs(G).sum(axis=1)
        maxwidth = max(maxwidth, float(width[0]))
        failures += int(np.any(np.abs(truth-c)>width/2+1e-8))
    return dict(q=q, seed=seed, pattern=pattern,
        maximum_x_width_m=round(maxwidth, 6),
        final_x_width_m=round(float(width[0]), 6),
        peak_generators=peak, failures=failures,
        mean_step_ms=round(float(np.mean(times)), 4),
        max_observed_step_ms=round(max(times), 4))

def main():
    results = [run(q, seed, pattern) for pattern in ["all", "mms", "smm"]
        for seed in [7, 19, 285] for q in [24, 48, 96, None]]
    assert all(r["failures"] == 0 for r in results)
    assert all(r["peak_generators"] <= r["q"]+12 for r in results if r["q"] is not None)
    summary = []
    for q in [24, 48, 96, None]:
        subset = [r for r in results if r["q"] == q]
        summary.append(dict(q=q,
            worst_max_x_width_m=max(r["maximum_x_width_m"] for r in subset),
            worst_observed_step_ms=max(r["max_observed_step_ms"] for r in subset),
            peak_generators=max(r["peak_generators"] for r in subset),
            failures=sum(r["failures"] for r in subset)))
    print(json.dumps(dict(runs=len(results), steps_per_run=150, summary=summary), indent=2))

if __name__ == "__main__": main()
