# Scheduling-visible 19-pair Farkas Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Independently determine whether the audited 19-pair cone remains infeasible when current-thrust-visible endpoint torques are modeled correctly.

**Architecture:** Extend only the vertex-control variables of the existing CC-RCI LP, then pair the numerical audit with a dependency-light exact rational Farkas checker. Archive one machine-readable result and bind it to the frozen contract and source hashes.

**Tech Stack:** Python 3, NumPy, SciPy HiGHS, `fractions.Fraction`, `unittest`.

**Spec:** `docs/superpowers/specs/2026-10-28-scheduling-visible-19pair-farkas-design.md`

## Global Constraints

- Preserve the existing 19-pair normals, 160 vertices and parameter-independent offsets.
- Give every vertex separate low/high current-thrust torque decisions.
- Exact verification must not require SymPy.
- Do not generalize the result beyond this reduced four-state candidate class.

## Review Focus

- Frozen config drift must fail before an LP or certificate is accepted.
- Low/high torque columns must remain distinct in the exact residual.
- The certificate must not silently use torque bounds.
- Floating infeasibility must never be labeled as the proof.
- Archived output must reproduce byte-for-byte in semantic JSON content.

---

### Task 1: Tests for the corrected LP and exact circuit

**Files:**
- Create: `verification/test_scheduling_visible_19pair_farkas.py`
- Test: `verification/test_scheduling_visible_19pair_farkas.py`

**Interfaces:**
- Consumes: existing `seed_cone()` and vertex enumeration helpers.
- Produces: pinned expectations for `build_scheduling_visible_lp()`, `verify_exact_certificate()` and `build_report()`.

- [x] **Step 1: Write failing tests** for 358 variables, 19,520 bounded inequalities, bounded/unbounded infeasibility, the 24-row rank-23 exact circuit, zero residual, exact RHS, positive multipliers, no torque-bound support and artifact reproduction.
- [x] **Step 2: Run the focused test and verify import/function failures.**
- [x] **Step 3: Preserve the observed RED result before implementation.**

### Task 2: Corrected numerical LP and exact verifier

**Files:**
- Create: `verification/check_scheduling_visible_19pair_farkas.py`
- Modify: `verification/test_scheduling_visible_19pair_farkas.py`

**Interfaces:**
- Consumes: repository root and optional artifact output path.
- Produces: `build_scheduling_visible_lp(include_torque_bounds: bool)`, `verify_exact_certificate()`, `build_report(root)` and a JSON CLI.

- [x] **Step 1: Implement frozen-contract assertions and endpoint-specific LP assembly.**
- [x] **Step 2: Implement exact 4x4 vertex reconstruction, rational rank and Farkas residual checks using `Fraction`.**
- [x] **Step 3: Run focused tests and require all assertions to pass.**
- [x] **Step 4: Generate `results/scheduling_visible_19pair_farkas_20261028/checks.json` and rerun artifact reproduction.**

### Task 3: Evidence ledger and checkpoint

**Files:**
- Create: `docs/learning/128_scheduling_visible_19pair_farkas.md`
- Create: `docs/research/run195_research_log.md`
- Modify: `docs/literature/READ_PAPERS.md`
- Modify: `docs/research/current_checkpoint.md`
- Modify: `docs/research/automation_research_log.md`

**Interfaces:**
- Consumes: the archived JSON and exact checker output.
- Produces: scoped `COUNTEREXAMPLE` claim, literature trace and the next unique Gate A blocker.

- [x] **Step 1: Record the corrected quantifier, exact certificate and all non-implications.**
- [x] **Step 2: Update the short checkpoint to under roughly 800 Chinese characters.**
- [x] **Step 3: Run focused and full verification; rebuild historical hash-bound artifacts only if the documented dependency changed.**
- [x] **Step 4: Review diff, commit, push and record the remote status.**

