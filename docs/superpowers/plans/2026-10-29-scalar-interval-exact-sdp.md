# Scalar Scheduling Interval Exact-SDP Contract Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Freeze and independently audit the exact scalar interval LMI used by the next 19-pair affine-offset synthesis run.

**Architecture:** A pure-standard-library checker verifies the coefficient identity and PSD principal minors using `Fraction`.  Tests drive the API and exercise valid, boundary, invalid, and malformed certificates.  Research notes separate the exact scalar subcondition from the conservative full synthesis template.

**Tech Stack:** Python standard library, `fractions.Fraction`, `unittest`, Markdown, JSON.

**Spec:** `docs/superpowers/specs/2026-10-29-scalar-interval-exact-sdp-design.md`

## Global Constraints

- No SDP solver installation or numerical feasibility claim.
- Preserve exact rational arithmetic in the checker.
- Keep fixed-19-pair, four-state, and six-state claims explicitly separated.
- Every later numerical candidate must still pass Run196's independent full-interval maximizer.

## Review Focus

- Wrong S-lemma sign: test `1-s^2` with `lambda=1` and zero Gram matrix.
- Boundary PSD rank loss: test `1+s` with a rank-one Gram matrix.
- Interior negativity hidden by endpoints: reject the normalized Run196 residual.
- Negative multiplier: reject even when the Gram matrix is PSD.
- Coefficient mismatch: reject a supplied Gram matrix that does not reconstruct the polynomial.

---

### Task 1: Exact certificate checker

**Files:**
- Create: `verification/test_scalar_interval_slemma.py`
- Create: `verification/check_scalar_interval_slemma.py`

**Interfaces:**
- Produces: `verify_slemma_certificate(a, b, c, multiplier, gram) -> dict` and `build_report(root) -> dict`.

- [x] **Step 1: Write tests for valid, boundary, invalid, and malformed certificates.**
- [x] **Step 2: Run the focused tests and confirm RED because the checker module is absent.**
- [x] **Step 3: Implement the minimal exact verifier and report builder.**
- [x] **Step 4: Run focused tests and confirm GREEN.**

### Task 2: Traceable evidence and research record

**Files:**
- Create: `docs/research/run197_literature_gate.md`
- Create: `docs/learning/130_scalar_interval_exact_sdp.md`
- Create: `docs/research/run197_research_log.md`
- Create: `results/scalar_interval_slemma_20261029/checks.json`
- Modify: `docs/literature/READ_PAPERS.md`
- Modify: `verification/README.md`
- Modify: `docs/research/current_checkpoint.md`

**Interfaces:**
- Consumes: Task 1 report schema and the frozen design.
- Produces: literature admission card, evidence labels, reproduction commands, and the next unique blocker.

- [x] **Step 1: Record the S-lemma theorem and targeted PD-RCI reread without a novelty claim.**
- [x] **Step 2: Archive the checker output and add reproduction documentation.**
- [x] **Step 3: Update the short checkpoint to Run197 and keep it concise.**

### Task 3: Verification and synchronization

**Files:**
- Modify mechanically only if dependency-hash tests require archived-result regeneration.

**Interfaces:**
- Consumes: all Run197 files.
- Produces: clean focused/full test results, commit, and remote branch.

- [x] **Step 1: Run focused tests and reproduce archived JSON.**
- [x] **Step 2: Run project and full research suites plus `git diff --check`.**
- [x] **Step 3: Commit and push `research/run197-affine-offset-exact-sdp`; compare local and remote tree hashes.**
