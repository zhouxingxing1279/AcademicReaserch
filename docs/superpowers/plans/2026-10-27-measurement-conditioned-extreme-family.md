# Measurement-Conditioned Extreme Family Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Certify an exact measurement-generated continuum of incomparable extreme information sets and its two-vertex affine offset parameter segment.

**Architecture:** A focused exact-rational checker consumes the existing vertical adapter and six-facet template. A focused unittest module independently verifies measurement coverage, support offsets, inclusion geometry, parameter vertices, and claim limits; a hash-bound JSON archives the evidence.

**Tech Stack:** Python standard library, `fractions.Fraction`, `unittest`, JSON, existing repository verification modules.

**Spec:** `docs/superpowers/specs/2026-10-27-measurement-conditioned-extreme-family-design.md`

## Global Constraints

- Use only the certified `P=1`, `V=11/4`, `a=1/50`, `kappa=1/10` contract.
- Keep true extreme sets distinct from extreme vertex polytopes.
- Do not claim graph invariance, control feasibility, recursive feasibility, or a full six-state guarantee.
- Do not add runtime dependencies.

## Review Focus

- Boundary measurements `eta=±(P+a)` must yield nonempty singleton-position posteriors covered by endpoint rectangles.
- Interior/boundary transition `eta=±(P-a)` must agree exactly.
- Distinct translated maximal rectangles must be incomparable in both directions.
- Six-direction offsets must be tight even when slant inequalities are redundant.
- The two parameter vertices must not be reported as the cardinality of the true extreme boundary.

---

### Task 1: Exact checker and RED/GREEN tests

**Files:**
- Create: `verification/check_measurement_conditioned_extreme_family.py`
- Create: `verification/test_measurement_conditioned_extreme_family.py`
- Create: `results/theory_measurement_conditioned_extreme_family_20261027/exact_checks.json`

**Interfaces:**
- Consumes: `check_houska_vertical_adapter.run()`, `check_six_facet_measurement_gate.six_facet_template()`.
- Produces: `posterior_interval(eta)`, `clamped_center(eta)`, `tight_offsets(center)`, `rectangle_contains(c_outer,c_inner)`, and `run()`.

- [ ] **Step 1: Write failing tests**

Add tests for the exact admissible measurement interval, five representative posterior strips including both outer boundaries, affine tight offsets at center/endpoints, pairwise incomparability, two parameter vertices versus continuum boundary, configuration membership, and explicit negative control claims.

- [ ] **Step 2: Run RED test**

Run: `PYTHONPATH=verification python -m unittest -q verification.test_measurement_conditioned_extreme_family`

Expected: import failure because the checker does not exist.

- [ ] **Step 3: Implement the minimal checker**

Use exact interval arithmetic and existing `Y/G/Lambda`; reject measurement centers outside `[-P-a,P+a]`. Report the continuous center interval symbolically and use the inclusion identity for equal-width rectangles as the universal maximality certificate.

- [ ] **Step 4: Run GREEN test and archive**

Run the focused test, generate JSON to a temporary path, then add the exact regenerated artifact under the result directory.

- [ ] **Step 5: Commit task 1**

Commit checker, tests, design, plan, gate, and result artifact.

### Task 2: Research record and repository integration

**Files:**
- Create: `docs/learning/124_measurement_conditioned_extreme_family.md`
- Create: `docs/research/run190_research_log.md`
- Modify: `docs/research/current_checkpoint.md`
- Modify: `docs/literature/READ_PAPERS.md`
- Modify: `docs/research/automation_research_log.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: Task 1 artifact and exact formulas.
- Produces: auditable claim statement, evidence classification, limitations, and one next priority.

- [ ] **Step 1: Document the proof and literature comparison**

State the posterior coverage proof, maximality/incomparability proof, affine parameter-segment formula, continuum-boundary versus two-vertex distinction, and slant-facet degeneracy.

- [ ] **Step 2: Update indexes and short checkpoint**

Keep the checkpoint below about 800 Chinese characters and set the unique next question to a nondegenerate correlated source family before any full graph LP.

- [ ] **Step 3: Rebind historical artifacts if `READ_PAPERS.md` changes**

Regenerate every archived artifact whose source hash includes `docs/literature/READ_PAPERS.md`; do not hand-edit JSON hashes.

- [ ] **Step 4: Run full verification**

Run project tests, all verification tests, and artifact replay. Expected: all pass with the new focused tests added.

- [ ] **Step 5: Commit task 2**

Commit documentation, checkpoint, re-bound artifacts, and final test record.
