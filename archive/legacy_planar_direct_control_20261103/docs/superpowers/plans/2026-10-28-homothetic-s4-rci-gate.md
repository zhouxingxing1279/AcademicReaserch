# Homothetic S4 RCI Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce an exact, reproducible counterexample showing whether any positive homothetic scale of Run193 `S4` can be RCI under scheduling-visible vertex torque.

**Architecture:** Reconstruct the deterministic Run193 four-layer template, then verify a frozen exact vertex and two exact successor-facet torque bounds using `Fraction`. Archive a JSON result with dependency hashes; use SciPy only in the inherited row-redundancy selection.

**Tech Stack:** Python standard library, NumPy, SciPy/HiGHS, `unittest`.

**Spec:** `docs/superpowers/specs/2026-10-28-homothetic-s4-rci-gate-design.md`

## Global Constraints

- Scope is the four-state reduced lateral-attitude benchmark only.
- Current thrust is measured before torque; future thrust may jump arbitrarily in `[4.905,14.715]` N.
- Use `W(T)=1.880+T*0.45^3/6`, all state bounds, and `|tau|<=0.08`.
- Reject only the homothetic frozen-`S4` vertex-control class.

## Review Focus

- A witness outside `S4` must fail membership.
- Fewer than four independent active facets must not be called a vertex certificate.
- Torque lower/upper signs must respect division by negative/positive input coefficients.
- The gap must be strictly positive for every `alpha>0`, not only sampled scales.
- The artifact must refuse general-RCI and six-state conclusions.

---

### Task 1: Exact homothetic-template obstruction

**Files:**
- Create: `verification/check_homothetic_s4_rci_gate.py`
- Test: `verification/test_homothetic_s4_rci_gate.py`

**Interfaces:**
- Produces: `audit(root: Path) -> dict` and a CLI writing one JSON artifact.

- [x] Write tests for exact `S4` membership, active-row rank, the positive affine torque gap, claim scope, dependency hashes, and archive reproduction.
- [x] Run focused tests and verify RED because the checker is absent.
- [x] Implement deterministic `S4` reconstruction and exact witness verification.
- [x] Run focused tests and verify GREEN.

### Task 2: Research record and verification

**Files:**
- Create: `docs/learning/127_homothetic_s4_rci_gate.md`
- Create: `docs/research/run194_research_log.md`
- Modify: `docs/literature/READ_PAPERS.md`
- Modify: `docs/research/current_checkpoint.md`
- Modify: `docs/research/automation_research_log.md`
- Create: `results/homothetic_s4_rci_gate_20261028/checks.json`

- [x] Archive the hash-bound checker result and document evidence limits.
- [x] Run focused, project, full research verification, artifact reproduction, and `git diff --check`.
- [x] Commit, synchronize the research branch, and verify the remote tree.
