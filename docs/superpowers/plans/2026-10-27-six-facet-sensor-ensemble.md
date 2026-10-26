# Six-Facet Sensor-Ensemble Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an exact, replayable gate proving that one position-width meta coordinate represents every continuous measurement center for the configured six-facet family.

**Architecture:** A standalone rational checker consumes Run186's public `Y/G/Lambda` template, verifies the two position support identities, and returns the complete interval of compatible measurement centers. Independent tests enumerate rational configured offsets and pin the halfwidth scaling; a hash-bound artifact and research log preserve the evidence boundary.

**Tech Stack:** Python standard library `fractions/json/hashlib/unittest`; existing six-facet and vertical-adapter checkers.

**Spec:** `docs/superpowers/specs/2026-10-27-six-facet-sensor-ensemble-design.md`

## Global Constraints

- Use exact `Fraction` arithmetic for every scientific pass condition.
- Reuse `six_facet_template()`; do not duplicate or silently reorder its facets.
- Fix `Z_1=(e_0+e_3)/2` and measurement halfwidth `a=1/50` from the adapter.
- Evidence level is at most `exact_six_facet_sensor_ensemble_measurement_row`.
- Do not claim a complete `Z/H/Omega`, graph invariance, controller feasibility, terminal invariance, or six-state guarantee.

## Review Focus

- Swapping the `-p` facet index must break the width-coordinate test.
- Using diameter rather than halfwidth must fail at the exact `2a` boundary.
- A configured polytope wider than `2a` must return an empty compatible-center interval.
- A translated/asymmetric configured polytope must retain exact `+p/-p` supports.
- An offset vector outside the configuration cone must be rejected rather than reported as evidence.

---

### Task 1: Exact sensor-ensemble measurement row

**Files:**
- Create: `verification/check_six_facet_sensor_ensemble.py`
- Create: `verification/test_six_facet_sensor_ensemble.py`

**Interfaces:**
- Consumes: `check_six_facet_measurement_gate.six_facet_template() -> dict`
- Produces: `measurement_meta_row() -> list[Fraction]`, `compatible_measurement_interval(offsets, halfwidth) -> dict`, and `run() -> dict`

- [ ] **Step 1: Write failing tests** for the exact `Z_1` row, configured support endpoints, compatible-center interval, exact boundary scaling, asymmetric offsets, configuration rejection, and negative evidence flags.
- [ ] **Step 2: Run `PYTHONPATH=verification python -m unittest verification.test_six_facet_sensor_ensemble -v` and confirm RED** because the checker is absent.
- [ ] **Step 3: Implement the minimal checker** using Run186 vertex maps and `G`; reject invalid offsets before emitting any claim.
- [ ] **Step 4: Run the focused test and confirm GREEN.**
- [ ] **Step 5: Commit checker and tests.**

### Task 2: Reproducible artifact and checkpoint

**Files:**
- Create: `results/theory_six_facet_sensor_ensemble_20261027/exact_checks.json`
- Create: `docs/learning/121_six_facet_sensor_ensemble.md`
- Create: `docs/research/run187_research_log.md`
- Modify: `docs/literature/READ_PAPERS.md`
- Modify: `docs/research/current_checkpoint.md`
- Modify: `docs/research/automation_research_log.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: `verification/check_six_facet_sensor_ensemble.py --output PATH`
- Produces: a hash-bound exact artifact and the next unique `Z_2/H/Omega` template-selection question.

- [ ] **Step 1: Add a failing CLI artifact replay/hash test.**
- [ ] **Step 2: Generate the artifact and make focused replay GREEN.**
- [ ] **Step 3: Record the literature gate, algebraic proof, direction correction, evidence limits, failures, and exact next question.**
- [ ] **Step 4: Replay all literature-hash artifacts and run both complete test suites.**
- [ ] **Step 5: Commit documentation and artifact.**

## Self-review

Every spec requirement is owned by Task 1 or Task 2. The public signatures agree across tasks. The tests cover all five review-focus failures, including asymmetric centers and invalid configuration admission. The plan intentionally stops before choosing `Z_2/H/Omega`; doing so is the research question, not an implementation detail.
