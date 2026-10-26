# Box Ensemble Graph LP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and independently replay a timing-correct 15-mode box information-ensemble LP baseline.

**Architecture:** An exact template module constructs `Y/G/Lambda` and `Z/H/Omega`. A focused LP builder uses one predicted ensemble and one control vector per source mode, then applies edge-specific post-transition measurement constraints; a hash-bound artifact stores exact primal checks and numerical solver diagnostics.

**Tech Stack:** Python, `fractions.Fraction`, NumPy, SciPy HiGHS, `unittest`, JSON.

**Spec:** `docs/superpowers/specs/2026-10-26-box-ensemble-graph-lp-design.md`

## Global Constraints

- Preserve Run183's exact `A/B/C/W`, tracking box, correction-input box, 15 modes, and 17 labeled edges.
- Current controls are indexed by source mode and source extreme set, never by successor edge.
- Measurement is applied after propagation because `control_precedes_successor_edge=true`.
- Numerical optimization success alone is not a mathematical certificate.

## Review Focus

- Sign/order errors in the `y <-> (c,r)` maps.
- Treating all 16 meta vertices as extreme information sets instead of the 4 maximal-radius vertices.
- Applying success measurement before dynamics or allocating edge-specific current controls.
- Reporting a float-tolerance LP solution as exact feasibility/optimality.
- Omitting state/input constraints on any extreme-set vertex.

---

### Task 1: Exact box and meta-template maps

**Files:**
- Create: `verification/check_houska_box_ensemble_lp.py`
- Create: `verification/test_houska_box_ensemble_lp.py`

**Interfaces:**
- Consumes: `verification/check_houska_vertical_adapter.py`.
- Produces: `box_template()` and `meta_template()` with exact rational matrices and vertex maps.

- [ ] Write failing tests for `P(y)` vertices, `Gy<=0`, the 16 meta vertices, the 4 maximal-radius extreme sets, and `Z1=r_p`.
- [ ] Run the targeted test and confirm failure because the module is absent.
- [ ] Implement the smallest exact template construction and rerun targeted tests.
- [ ] Commit the template task.

### Task 2: Timing-correct graph LP and replay artifact

**Files:**
- Modify: `verification/check_houska_box_ensemble_lp.py`
- Modify: `verification/test_houska_box_ensemble_lp.py`
- Create: `results/theory_houska_box_ensemble_lp_20261026/exact_checks.json`

**Interfaces:**
- Consumes: Task 1 maps and Run183 adapter contract.
- Produces: `build_graph_lp()`, `solve_graph_lp()`, exact inequality replay, and numerical dual diagnostics.

- [ ] Write failing tests for variable ownership, 15 predicted ensembles, 17 post-transition edges, shared mode-4/9 controls, and exact certificate scope.
- [ ] Run targeted tests and observe the intended failures.
- [ ] Implement the LP builder, HiGHS solve, rational candidate recovery, exact replay, and hash-bound CLI artifact.
- [ ] Rerun targeted tests; if exact primal replay cannot pass, record a numerical-only result without upgrading the evidence level.
- [ ] Commit the LP task.

### Task 3: Literature gate, derivation, and checkpoint

**Files:**
- Create: `docs/research/run184_literature_gate.md`
- Create: `docs/research/run184_research_log.md`
- Create: `docs/learning/118_houska_box_ensemble_graph_lp.md`
- Modify: `docs/literature/READ_PAPERS.md`
- Modify: `docs/research/current_checkpoint.md`
- Modify: `docs/research/automation_research_log.md`
- Modify: `README.md`

**Interfaces:**
- Consumes: Task 2 artifact and primary-paper equations.
- Produces: bounded claims, reproducible commands, and one unique next question.

- [ ] Record the actual sections read, the timing difference, strongest baseline, and admission verdict.
- [ ] Document exact maps, LP dimensions, solver/replay result, evidence level, and limitations.
- [ ] Update the short checkpoint and indexes; replay literature-hash-bound artifacts if needed.
- [ ] Run full project and verification suites plus `git diff --check`.
- [ ] Commit the documentation task.
