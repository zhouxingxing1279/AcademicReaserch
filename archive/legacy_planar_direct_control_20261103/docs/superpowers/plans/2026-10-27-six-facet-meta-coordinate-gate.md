# Six-Facet Meta-Coordinate Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an exact replayable certificate showing that five center/radius coordinates are not measurement closed and six-coordinate completion is budget-neutral under exact reparameterization.

**Architecture:** A standalone rational checker consumes the existing Run186 six-facet template, implements the explicit offset/paired-coordinate bijection, and validates one actual-noise posterior counterexample. Tests use an independent facet-pair oracle and a small parameter-polytope vertex map to prevent circular verification.

**Tech Stack:** Python standard library `fractions/json/hashlib/unittest`; existing six-facet checker.

**Spec:** `docs/superpowers/specs/2026-10-27-six-facet-meta-coordinate-gate-design.md`

## Global Constraints

- Use exact `Fraction` arithmetic for every pass condition.
- Preserve facet order `+p,+v,-q,-p,-v,+q` and `kappa=1/10`.
- Use actual measurement halfwidth `a=1/50` from the vertical adapter.
- Evidence level is at most `exact_six_facet_meta_coordinate_nonclosure_certificate`.
- Do not construct or claim complete `H/Omega`, graph invariance, controller feasibility, terminal invariance, or six-state guarantees.

## Review Focus

- The paired-coordinate map and inverse must compose to identity for general noncentral offsets.
- Zero skew must characterize the translation-consistent five-coordinate slice.
- The posterior witness must use an actual measurement strip, not an arbitrary offset perturbation.
- Every posterior facet must remain active and the configuration inequalities must be strict.
- Budget neutrality applies only to the same polytope under an invertible coordinate change.

---

### Task 1: Exact coordinate and nonclosure certificate

**Files:**
- Create: `verification/check_six_facet_meta_coordinate_gate.py`
- Create: `verification/test_six_facet_meta_coordinate_gate.py`
- Create: `results/theory_six_facet_meta_coordinate_gate_20261027/exact_checks.json`

**Interfaces:**
- Consumes: `check_six_facet_measurement_gate.six_facet_template() -> dict` and adapter halfwidth.
- Produces: `paired_coordinates(offsets)`, `offsets_from_paired(coordinates)`, `skew(coordinates)`, and `run()`.

- [ ] **Step 1: Write failing tests** for bijection, zero-skew source, actual-strip posterior, independent vertex/facet activity, strict configuration margin, budget-neutral vertex mapping, negative evidence flags, and artifact replay.
- [ ] **Step 2: Run `PYTHONPATH=verification python -m unittest verification.test_six_facet_meta_coordinate_gate -v`; expect RED because the checker is absent.**
- [ ] **Step 3: Implement the minimal exact checker and CLI artifact writer.**
- [ ] **Step 4: Generate the artifact and rerun the focused suite; expect GREEN.**
- [ ] **Step 5: Run both full suites and commit.**

### Task 2: Research record and checkpoint

**Files:**
- Create: `docs/learning/122_six_facet_meta_coordinate_gate.md`
- Create: `docs/research/run188_research_log.md`
- Modify: `docs/literature/READ_PAPERS.md`
- Modify: `docs/research/current_checkpoint.md`
- Modify: `docs/research/automation_research_log.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: Task 1 evidence artifact and test counts.
- Produces: bounded claim, literature comparison, failure rationale, and one next question.

- [ ] **Step 1: Record the exact algebra, witness, literature gate, and rejection of coordinate-only budget claims.**
- [ ] **Step 2: Rebind and replay all literature-hash artifacts.**
- [ ] **Step 3: Run focused and complete suites, update the short checkpoint, and commit.**

## Self-review

Task 1 owns every numerical and algebraic claim; Task 2 only reports Task 1 outputs. The plan deliberately
stops before choosing a bounded direct-offset meta polytope, because that choice determines `H/Omega` and
is the next research question rather than an implementation detail.
