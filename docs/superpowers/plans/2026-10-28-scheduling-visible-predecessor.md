# Scheduling-visible predecessor audit implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Correct the four-state Gate-A predecessor information timing and determine whether allowing the torque to depend on the measured current thrust changes the first four robust predecessor layers.

**Architecture:** Build one independent checker that reuses the frozen planar contract but implements two scalar-input projections: a common-torque quantifier and a scheduling-visible endpoint-conditioned quantifier. Exact `Fraction` arithmetic constructs inequalities; scaled HiGHS LPs only classify redundancy. The result is a finite-layer numerical audit, not an RCI certificate.

**Tech Stack:** Python standard library, NumPy, SciPy/HiGHS, `unittest`.

**Spec:** `docs/research/run193_literature_gate.md`

## Global Constraints

- Current thrust is measured before torque is selected; future thrust may jump arbitrarily in `[4.905,14.715]` N.
- Use `W(T)=1.880+T*0.45^3/6`, all four state bounds, and `|tau|<=0.08`.
- Keep conclusions inside the four-state reduced benchmark.
- Finite predecessor equality must not be reported as infinite-horizon RCI or recursive feasibility.

## Review Focus

- Accidentally pairing inequalities from different thrust endpoints in the scheduling-visible projection.
- Omitting the torque bounds from one endpoint-specific elimination.
- Treating floating redundancy decisions as exact certificates.
- Claiming endpoint-conditioned controls for interior thrust without stating the affine interpolation policy.
- Upgrading four matching predecessor layers to an infinite-horizon equality.

---

### Task 1: Quantifier-separated predecessor checker

**Files:**
- Create: `verification/check_scheduling_visible_predecessor.py`
- Test: `verification/test_scheduling_visible_predecessor.py`

**Interfaces:**
- Produces: `audit(root: Path, max_depth: int = 4) -> dict` and a CLI writing one JSON artifact.

- [x] Write failing tests for the two projection pairings, frozen contract, expected depth-1--4 facet counts, finite-scope labels, and archive reproduction.
- [x] Run the focused tests and verify failure because the checker is absent.
- [x] Implement the minimal checker with exact inequality construction and endpoint-local Fourier--Motzkin pairing.
- [x] Run focused tests and verify they pass.

### Task 2: Research record and checkpoint

**Files:**
- Create: `docs/learning/126_scheduling_visible_predecessor_audit.md`
- Create: `docs/research/run193_research_log.md`
- Modify: `docs/literature/READ_PAPERS.md`
- Modify: `docs/research/current_checkpoint.md`
- Modify: `docs/research/automation_research_log.md`
- Create: `results/scheduling_visible_predecessor_20261028/checks.json`

- [x] Generate the archived artifact from the checker.
- [x] Record the literature admission card, derivation, evidence levels, commands, limitations, and next unique question.
- [x] Run focused, project, and full research verification plus `git diff --check`.
- [ ] Commit and synchronize the research branch, then verify the remote tree.
