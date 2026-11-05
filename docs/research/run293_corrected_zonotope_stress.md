# Run293 — corrected opportunity-phase zonotope stress (2026-11-03)

## Scope and provenance
Main base: `eb18e857090b0babe531c13c61aea944793af428`. Integrated the Run288 prototype from branch `research/run288-multiseed-zonotope-stress` into one executable file on a new branch, correcting the mislabeled measurement schedule. This is a **synthetic 12-state hover linearization**, not the repository's certified 4-state dropout automaton, physical quadrotor contract, or MPC feedback loop.

## Explicit provisional schedule
Dynamics step 0.02 s; measurement opportunities at k=5,10,...,150 (30 opportunities). Opportunity index j=k/5-1, first pattern character applies at j=0. S=success, M=miss. all=30 successes, MMS=10, SMM=10, SMS=20. First MMS success k=15; first SMM success k=5. These assertions are in the executable. Formal automaton initial state, admissible transitions, and maximum consecutive misses have **not** been verified; the pattern names must not be called certified.

## Executed local reproduction
Command: `OPENBLAS_NUM_THREADS=1 python experiments/run293_corrected_zonotope_stress.py` (equivalent local reconstruction executed as `python /mnt/data/run293/stress.py`; same numerical model, reduction, receive rule, and 36-case matrix). NumPy/SciPy installed; no hardware timing guarantee.

3 seeds (7,19,285) x 3 patterns (all,MMS,SMM) x 4 generator budgets (24,48,96,unreduced) x 150 steps = 36 runs, 5400 state updates.

| q | worst peak x interval width (m) | max generators | sample truth containment failures |
|---|---:|---:|---:|
| 24 | 0.414791 | 36 | 0 |
| 48 | 0.332731 | 60 | 0 |
| 96 | 0.305563 | 108 | 0 |
| none | 0.240829 | 1932 | 0 |

Run288 previously reported q=48 width 0.326592 m under mislabeled patterns. Under the corrected phase and actual MMS/SMM patterns the value is 0.332731 m. These are finite synthetic checks only; neither set boundedness nor robust closed-loop safety follows. Wall-clock timing is deliberately not reported as real-time/WCET evidence.

## Mathematical guarantee and open gap
The generator reduction replaces discarded generators by coordinatewise interval generators: `G_red=[G_keep,diag(sum(abs(G_discard),axis=1))]`, so `Z(c,G) subseteq Z(c,G_red)`. The measurement strip outer update also preserves inclusion under the declared bounded-noise linear model, provided the initial set contains truth. Neither result proves a finite invariant tube, admissibility of the schedule under the main automaton, physical actuator bounds, or MPC recursive feasibility.

## Literature
No newly read paper this run. Existing canonical `docs/literature/PAPER_READING_LOG.md` remains unchanged; do not claim a new full-text reading.

## Next single gate
Cross-check the **actual main-branch dropout automaton** (initial phase, transition graph, observation opportunities) against this runner; if inconsistent, change the runner and rerun 36 cases before using it as an SMF-to-MPC interface. Gate A remains blocked.
