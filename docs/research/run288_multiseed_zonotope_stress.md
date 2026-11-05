# Run288 — 12-state Zonotope-SMF multi-seed stress audit (2026-11-03)

## Scope and reproducibility
Independent local NumPy 2.3.5 / SciPy 1.17.0, OPENBLAS_NUM_THREADS=1; executable source is committed as `experiments/run288_multiseed_zonotope_stress.py` in this PR. This document reports the actually executed experiment, not a CI result.

The experiment reimplements Run287's 12-state hover linearization, exact 20ms ZOH, 12-state initial interval half-widths, bounded synthetic process/measurement errors, and scalar zonotope measurement-strip update. For every one of 3 seeds (7,19,285), 3 measurement patterns (all success, MMS periodic, SMM periodic) and 4 generator budgets (q=24/48/96/unreduced), it executes 150 steps: **36 runs, 5400 propagation/update steps**. Every 5th step is a measurement opportunity. The reduced generator matrix retains q largest Euclidean-norm columns, replaces discarded columns by a diagonal absolute-row-sum enclosure, and therefore has at most q+12 columns. For the unbounded reference, no reduction is applied.

## Observed results
| q | Worst max horizontal position interval width (m) | Largest observed Python step duration (ms) | Peak generator columns | Sample-path containment failures |
|---|---:|---:|---:|---:|
| 24 | 0.414791 | 0.3658 | 36 | 0 |
| 48 | 0.326592 | 0.3223 | 60 | 0 |
| 96 | 0.305563 | 0.2515 | 108 | 0 |
| unreduced | 0.240829 | 0.4973 | 1932 | 0 |

These are **observed** timings, not hard WCET bounds. Small timing inversions (q=96 faster than q=24 in worst sampled step) can result from scheduling and matrix-size effects and are not a complexity theorem. Three deterministic seeds and 150 steps do not establish universal set containment, all-dropout safety, or long-horizon estimator boundedness. The algebraic reduction enclosure follows from replacing discarded generators with a diagonal box whose i-th radius is their absolute row sum; this is separate from sampled containment tests.

The experiment uses synthetic noise limits, not physically identified disturbances, and does not solve any MPC problem. The 'SMM' schedule here is merely a periodic toy schedule and must be checked against the repository's actual finite-state dropout automaton before being used as an admissible path. The 12-state model is a local hover linearization; it does not certify nonlinear 6-DOF flight or per-motor thrust feasibility.

## Research decision
q=48 and q=96 are promising for controlled comparisons, but the reduction algorithm should not be selected based only on interval width. Next prioritize running the executable multi-seed benchmark in CI, then freeze sensor/disturbance bounds and legitimate measurement automaton; only after that connect a control-relevant posterior bound to Tube MPC tightening. No claim of recursive feasibility, RPI tube, 20ms WCET or hard safety is made. Gate A remains blocked.

## GitHub hygiene
This PR adds one executable experiment and one research log; it does not duplicate or assume that Run285–287 open PR files are present on main. No new paper was read; PAPER_READING_LOG.md remains unchanged.