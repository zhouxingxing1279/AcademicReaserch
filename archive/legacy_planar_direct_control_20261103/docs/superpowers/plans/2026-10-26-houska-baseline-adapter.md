# Houska Baseline Adapter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an exact, executable admission gate for the frozen-envelope vertical Houska baseline adapter.

**Architecture:** A focused checker derives the two-state LTI matrices, global residual envelope, measurement operators, hard margins, and graph causality from the existing configuration. Unit tests pin exact fractions and reject decision-dependent or noncausal substitutions.

**Tech Stack:** Python standard library, `fractions.Fraction`, `unittest`, JSON artifacts.

**Spec:** `docs/superpowers/specs/2026-10-26-houska-baseline-adapter-design.md`

## Global Constraints

- Preserve the 15 modes and 17 edges from `mpc.ancillary_rci_contract.mode_graph`.
- Freeze process noise at the maximum actual thrust; never use estimation error as future disturbance.
- The artifact must say that no invariant ensemble, terminal set, or recursive feasibility is certified.

## Review Focus

- Float-to-rational drift: parse configuration with `Fraction` and assert exact values.
- Unknown packet branch: mode 4 and 9 outgoing edges share the current control.
- Miss semantics: no artificial measurement intersection.
- Hard-state margins: derive them from the nominal and physical boxes, not hand-entered constants.
- Evidence scope: explicit negative flags for terminal and six-state claims.

---

### Task 1: Exact adapter checker and regression tests

**Files:**
- Create: `verification/check_houska_vertical_adapter.py`
- Create: `verification/test_houska_vertical_adapter.py`
- Create: `results/theory_houska_vertical_adapter_20261026/exact_checks.json`

**Interfaces:**
- Consumes: `configs/planar_baseline.json` and the existing ancillary RCI contract.
- Produces: `adapter_contract(config)` and `run()` dictionaries with exact rational data.

- [ ] **Step 1: Write failing tests** for exact LTI matrices, residual envelope, graph/measurement semantics, hard margins, and evidence scope.
- [ ] **Step 2: Run** `PYTHONPATH=verification python -m unittest verification.test_houska_vertical_adapter` and confirm failure because the checker is absent.
- [ ] **Step 3: Implement** the minimal checker, including a hash-bound JSON CLI.
- [ ] **Step 4: Regenerate the artifact and rerun the targeted tests.**
- [ ] **Step 5: Run full project and verification suites.**

### Task 2: Literature gate and research checkpoint

**Files:**
- Create: `docs/research/run183_literature_gate.md`
- Create: `docs/research/run183_research_log.md`
- Create: `docs/learning/117_houska_vertical_adapter_contract.md`
- Modify: `docs/literature/READ_PAPERS.md`
- Modify: `docs/research/current_checkpoint.md`
- Modify: `docs/research/automation_research_log.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: Task 1 exact artifact and primary-paper equations.
- Produces: bounded claims, reproducible commands, and one next research question.

- [ ] **Step 1: Record** actual sections read and the strict difference between fixed-`W` Houska and the current graph.
- [ ] **Step 2: Document** the adapter derivation and state that this is a baseline contract, not a terminal certificate.
- [ ] **Step 3: Update** the short checkpoint and indexes, keeping the checkpoint concise.
- [ ] **Step 4: Run** artifact reproduction and `git diff --check`.
