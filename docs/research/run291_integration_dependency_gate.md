# Run291 — 12-state dropout/SMF integration dependency gate (2026-11-03)

## Scope and independently checked evidence

- Default `main` latest observed commit: `eb18e857090b0babe531c13c61aea944793af428` (GitHub commit search, 2026-11-03). This is a snapshot, not a guarantee against concurrent updates.
- GitHub contents API on this `main` returned **404** for both `experiments/run288_multiseed_zonotope_stress.py` and `experiments/run290_dropout_opportunity_contract.py`. Thus neither can be treated as a main-branch regression dependency today; 404 does not prove a file is absent from all PR branches.
- PR #185 exists and explicitly states that its standalone schedule-phase test does **not** patch Run288, certify the formal dropout automaton, or rerun SMF stress tests. Prior Run288 PR #178 remains a separate integration dependency. No PR merge status, CI success or main landing is inferred from the PR description.
- `docs/literature/PAPER_READING_LOG.md` exists on main (blob `1de02df818e5d9b0ecbe183c159c58ac2f1ef4e0`); the record includes Yan, Cannon & Goulart (2022), DOI 10.1016/j.automatica.2022.110282, but this audit does not claim a fresh full-paper reading.

## Reproducible integration acceptance gate (not yet executed)

1. On fresh main, verify `git rev-parse HEAD` and inspect PR #178 and #185 file diffs, heads, reviews and checks. Never assume their reported earlier base SHA is current.
2. Recover Run288 script from its exact PR head; inspect measurement-opportunity timing and the actual success/miss sequence. Compare against the *formal* repository dropout automaton, including initial state and phase. Do not infer legality merely from counts or three-character labels.
3. Integrate a single canonical schedule generator with the SMF stress harness; explicitly test the first 12 opportunities, counts over 30 opportunities, and legal automaton transitions. Require `all` to mean all **scheduled opportunities** succeed, not every dynamics step.
4. Run the full 3-seed × 3-mode × 4-budget (36-case) stress matrix on the integrated code, log NumPy/SciPy/Python versions and BLAS thread settings, and archive widths, true-state containment failures, generator counts and per-step timings. Any changed data supersede Run288's mislabeled summary, rather than silently reusing it.
5. Require passing CI, review exact changed files and verify the fresh main SHA immediately before safe merge. Confirm the resulting main SHA and file contents after merge. Do not force push.

## Mathematical scope

A successful finite-run containment test is evidence only for sampled trajectories. Zonotope reduction by enclosing discarded generators in a diagonal interval is an outer-approximation step, but neither a bounded estimation-error invariant nor a robust output-feedback Tube MPC terminal feasibility certificate follows from it. This gate does not close the 12-state physical disturbance, actuator allocation or information-state viability gaps. Gate A remains **blocked**.

## This round's limitation and next unique priority

This round verifies repository/PR integration dependencies, not new simulation results. **No numeric tests executed**, because Run288 and Run290 executable files are absent from the inspected main snapshot and their source/automaton integration has not been reconstructed. Next priority: reconcile Run288 and Run290 on the latest main through an explicitly checked legal dropout automaton and rerun the 36-case matrix before accepting any revised performance claim.
