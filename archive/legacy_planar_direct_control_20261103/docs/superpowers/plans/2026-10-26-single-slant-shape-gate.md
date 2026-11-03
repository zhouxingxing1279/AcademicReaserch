# Single-Slant Shape Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an exact replayable gate deciding whether one fixed coupled-normal parallelogram removes Run184's shape-level cycle obstruction.

**Architecture:** A standalone rational checker imports the frozen vertical adapter, derives the signed transform and support-radius recurrence, and checks the 5/10/15-step returns. Unit tests pin transform signs, the corrected obstruction, all three success gaps, limitations and artifact hashes.

**Tech Stack:** Python standard library `fractions/json/hashlib/unittest`; existing adapter checker.

**Spec:** `docs/superpowers/specs/2026-10-26-single-slant-shape-gate-design.md`

## Global Constraints

- Use exact `Fraction` arithmetic for every scientific pass condition.
- Keep `kappa=1/10`, `h=1/50`, `nu=1/50`, and `N=15` explicit and hash-bound.
- Preserve source-indexed control-before-packet graph semantics, while making no control-feasibility claim.
- Evidence level after review correction is exactly `exact_fixed_slant_parallelogram_shape_obstruction`.

## Review Focus

- A sign error in `q=p-kappa*v` must fail a transform identity test.
- Omitting the disturbance contribution `kappa*w` must fail the one-step recurrence test.
- Checking only the 15-step success edge must fail an all-success-edges test.
- Checking source modes but not pre-measurement predictions must fail the capacity test.
- Any accidental full-ensemble or recursive-feasibility claim must fail the limitation test.

---

### Task 1: Exact recurrence and periodic certificate

**Files:**
- Create: `verification/check_single_slant_shape_gate.py`
- Create: `verification/test_single_slant_shape_gate.py`

**Interfaces:**
- Consumes: `check_houska_vertical_adapter.run() -> dict`
- Produces: `shape_recurrence()`, `return_obstruction()`, and `run() -> dict`

- [ ] **Step 1: Write failing tests** for coordinate identities, exact return closure/obstruction, all success gaps, rejected-candidate containment, and evidence limitations.
- [ ] **Step 2: Run the focused tests and confirm RED** because the checker module is absent.
- [ ] **Step 3: Implement the minimal exact checker** using the independently derived transform; preserve an exact obstruction if closure fails.
- [ ] **Step 4: Run the focused tests and confirm GREEN.**
- [ ] **Step 5: Commit the checker and tests.**

### Task 2: Reproducible artifact and research record

**Files:**
- Create: `results/theory_single_slant_shape_gate_20261026/exact_checks.json`
- Create: `docs/learning/119_single_slant_shape_cycle.md`
- Create: `docs/research/run185_research_log.md`
- Modify: `docs/literature/READ_PAPERS.md`
- Modify: `docs/research/current_checkpoint.md`
- Modify: `docs/research/automation_research_log.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: `verification/check_single_slant_shape_gate.py --output PATH`
- Produces: hash-bound archived result and a short next-question checkpoint.

- [ ] **Step 1: Add a failing artifact replay/hash test.**
- [ ] **Step 2: Generate the artifact once and make replay GREEN.**
- [ ] **Step 3: Document derivation, literature boundary, exact margins, limitations and next unique question.**
- [ ] **Step 4: Replay all hash-bound literature artifacts and run both complete test suites.**
- [ ] **Step 5: Commit documentation and artifacts.**

## Self-review

The plan covers every design goal without adding a full polytope/meta LP. Interfaces use the existing adapter contract only. All five review risks have an owning test. The two tasks are independently reviewable: scientific checker first, archive/documentation second.
