# Six-Facet Measurement Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an exact replayable six-facet configuration and measurement-support gate that determines whether retained velocity facets can tighten slant support after a position measurement.

**Architecture:** A standalone rational checker derives the cyclic facet matrix, adjacent-pair vertex maps, configuration cone, and canonical measurement supports. Its tests independently enumerate vertices and pin a strict support-reduction witness; a hash-bound artifact and research record preserve the evidence boundary.

**Tech Stack:** Python standard library `fractions/json/hashlib/unittest`; existing vertical adapter checker.

**Spec:** `docs/superpowers/specs/2026-10-27-six-facet-measurement-gate-design.md`

## Global Constraints

- Use exact `Fraction` arithmetic for all scientific pass conditions.
- Fix `kappa=1/10` and cyclic normals `+p,+v,-q,-p,-v,+q`.
- Verify support formulas by exact vertex enumeration, not samples or solver tolerances.
- Evidence level is at most `exact_six_facet_measurement_support_map`.
- Do not claim a graph-invariant ensemble, input feasibility, terminal set, recursive feasibility, or six-state guarantee.

## Review Focus

- A changed cyclic normal order must invalidate the adjacent-pair vertex maps.
- A configuration matrix that omits a non-adjacent containment row must fail an exact vertex-in-polytope test.
- A support formula using the raw slant offset instead of `min(r_q,a+kappa*r_v)` must fail the strict witness.
- A strict witness outside the pre-measurement configuration cone must be rejected.
- Artifact flags must prevent upgrading a local measurement map into a controller theorem.

---

### Task 1: Exact configuration triple and measurement support

**Files:**
- Create: `verification/check_six_facet_measurement_gate.py`
- Create: `verification/test_six_facet_measurement_gate.py`

**Interfaces:**
- Consumes: `check_houska_vertical_adapter.run() -> dict`
- Produces: `six_facet_template() -> dict`, `canonical_measurement_support(a, r_v, r_q) -> dict`, and `run() -> dict`

- [ ] **Step 1: Write failing tests** for cyclic `Y`, six exact `Lambda` maps, every `G` containment row, exact reference vertices, all three canonical support identities, strict slant reduction, witness admission, and evidence limitations.
- [ ] **Step 2: Run `PYTHONPATH=verification python -m unittest verification/test_six_facet_measurement_gate.py -v` and confirm RED** because the checker module is absent.
- [ ] **Step 3: Implement the minimal exact checker** using adjacent 2-by-2 inverses and exhaustive pairwise vertex feasibility for independent support replay.
- [ ] **Step 4: Run the focused test and confirm GREEN.**
- [ ] **Step 5: Commit checker and tests.**

### Task 2: Artifact and research checkpoint

**Files:**
- Create: `results/theory_six_facet_measurement_gate_20261027/exact_checks.json`
- Create: `docs/learning/120_six_facet_measurement_support.md`
- Create: `docs/research/run186_research_log.md`
- Modify: `docs/literature/READ_PAPERS.md`
- Modify: `docs/research/current_checkpoint.md`
- Modify: `docs/research/automation_research_log.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: `verification/check_six_facet_measurement_gate.py --output PATH`
- Produces: a hash-bound exact artifact and the next unique graph/meta-LP question.

- [ ] **Step 1: Add a failing artifact replay/hash test.**
- [ ] **Step 2: Generate the artifact and make focused replay GREEN.**
- [ ] **Step 3: Record literature coverage, exact derivation, strict witness, limitations, and why this is baseline infrastructure rather than innovation.**
- [ ] **Step 4: Replay every literature-hash artifact and run both complete test suites.**
- [ ] **Step 5: Commit documentation and artifact.**

## Self-review

The plan covers every design requirement with exact tests. The configuration and measurement modules share only the public template maps; no full ensemble variables are introduced. The strict witness is separately checked for pre-measurement configuration feasibility, and every theorem-level limitation is represented by a false evidence flag.
