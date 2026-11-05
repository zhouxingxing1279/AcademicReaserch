# Run287 — Reliable zonotope generator reduction benchmark (2026-11-03)

## Question and inherited evidence
Follow Run285 interval SMF PR #171 and Run286 unreduced zonotope PR #173. Those branches are **not assumed merged into main**. The main checkpoint still contains a different four-state Euler robust safety line; no transfer of its proofs or counterexamples to this 12-state hover toy is justified. Gate A remains blocked.

## Set-theoretic certificate
Given zonotope Z(c,G), choose q columns by descending Euclidean norm (stable tie-break). Denote retained matrix G_K and discarded G_D. Set
G_reduced = [G_K, diag(sum_j |(G_D)_{ij}|)].
For every discarded coefficient vector ||xi_D||_inf <= 1, each coordinate of G_D xi_D lies in [-sum_j |G_D_ij|, +sum_j |G_D_ij|]. Therefore Z(c,G) is contained in Z(c,G_reduced), independently of the heuristic column ordering. The output has at most q+12 generators after reduction. It is an outer enclosure, not a minimal-volume reduction. Prediction and measurement strip update retain Run286's sound algebra under known applied input and bounded disturbances.

## Reproducible local test
Run `python experiments/run287_zonotope_reduction.py` (NumPy/SciPy). Locally executed equivalent source in Python on 2026-11-03 with fixed seed 285, 300 steps, 20 ms ZOH, synthetic process/measurement boxes and position+yaw packet opportunities every 5 steps, skipping every third opportunity. Results:

| Retained q | Max x-width (m) | Final x-width (m) | Peak generators | Truth containment failures |
|---:|---:|---:|---:|---:|
| 12 | 0.570129 | 0.023037 | 24 | 0 |
| 24 | 1.079127 | 0.022278 | 36 | 0 |
| 48 | 0.423671 | 0.032017 | 60 | 0 |
| 96 | 0.261001 | 0.046778 | 108 | 0 |
| unreduced | 0.235276 | 0.126867 | 3772 | 0 |

Also passed 300 independent random-point checks per q (100 each for q=12,24,48) against the reduced box support bounds. The source was locally executed before GitHub upload; **remote CI has not been confirmed**. Runtime measurements were approximately 0.02–0.03 s for the **whole 300-step Python loop** in the local environment, not a reproducible worst-case 20 ms per-step latency guarantee; hardware and runtime conditions are not calibrated. Generator reduction is not monotonically better as q increases because the strip-update gain and later geometry change.

## Interpretation and remaining limitations
This supplies a bounded-complexity reliable outer enclosure for the synthetic linear model, not an exact posterior or an invariant bound. At q=96, the maximum x-width is 0.261 m versus 0.235 m unreduced (about 11% larger), while generators are capped at 108 rather than 3772. q=12/24 can be significantly worse at intermediate times. These figures are single seeded simulations; no exhaustive all-path containment, nonlinear plant mismatch bounds, physical thrust allocation, real sensor/noise calibration, legal dropout automaton verification, robust Tube MPC solver, terminal information-RCI, recursive feasibility or hard-safety certificate. No new paper was read in this run, so do not modify PAPER_READING_LOG.md.

## Next single priority
Run this script under repository CI and compare q=48/96 against unreduced on multiple bounded adversarial traces and all legal packet patterns, including per-step runtime distributions and reduction inflation. Then freeze physical process/measurement bounds and actuator/sensor interfaces before integrating into Tube MPC.
