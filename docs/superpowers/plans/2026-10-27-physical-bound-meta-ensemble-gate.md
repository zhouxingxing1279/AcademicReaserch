# Physical-Bound Meta-Ensemble Gate Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an exact replayable certificate that physical box containment alone yields a singleton extreme-set boundary for the six-offset meta ensemble.

**Architecture:** A small rational checker consumes the existing vertical adapter and six-facet template, computes the physical-box support vector, verifies it represents exactly the physical box, and certifies componentwise domination for configured polytopes through support monotonicity. Tests independently evaluate the six directions and enforce negative evidence flags.

**Tech Stack:** Python standard library `fractions/json/hashlib/unittest`; existing Run183/186 verification modules.

**Spec:** `docs/superpowers/specs/2026-10-27-physical-bound-meta-ensemble-gate-design.md`

## Global Constraints

- Use exact `Fraction` arithmetic.
- Reuse physical halfwidths `1` and `11/4`; do not introduce tuning caps.
- Preserve facet order `+p,+v,-q,-p,-v,+q` and `kappa=1/10`.
- Stop before variable-family `H/Omega`, graph invariance, control feasibility, or recursive feasibility.

## Review Focus

- Verify `51/40` in both slant directions independently.
- Verify the support vector satisfies the configuration cone.
- Distinguish all vertices of the bounded parameter domain from extreme sets of the induced information ensemble.
- Ensure the singleton claim uses physical containment, not sampled offsets.
- Preserve explicit negative evidence flags.

---

### Task 1: Exact singleton-extreme certificate

**Files:**
- Create: `verification/test_physical_bound_meta_ensemble_gate.py`
- Create: `verification/check_physical_bound_meta_ensemble_gate.py`
- Create: `results/theory_physical_bound_meta_ensemble_gate_20261027/exact_checks.json`

**Interfaces:**
- Consumes: `check_houska_vertical_adapter.run()` and `check_six_facet_measurement_gate.six_facet_template()`.
- Produces: `physical_support_vector()`, `run()`, and a hash-bound JSON artifact.

- [ ] Write tests for the exact support vector, box equality through six configured vertices/supports, singleton boundary logic, negative flags, and artifact replay.
- [ ] Run `PYTHONPATH=verification python -m unittest verification.test_physical_bound_meta_ensemble_gate -v`; expect RED because the checker is absent.
- [ ] Implement the minimal exact checker and CLI writer.
- [ ] Generate the artifact; rerun focused and complete suites.
- [ ] Commit the exact certificate.

### Task 2: Research record and checkpoint

**Files:** create Chapter 123, Run189 literature gate and research log; update reading table, checkpoint, automation log, README, and historical literature hashes.

- [ ] Record the literature admission, theorem, evidence boundary, and rejected physical-only baseline.
- [ ] Rebind historical literature hashes and replay all tests.
- [ ] Commit, independently review, perform final verification, and push the research branch.

## Self-review

The plan proves only the structural stopping result needed before any costly `H/Omega` enumeration. It deliberately leaves the design of information-conditioned meta constraints to the next run.
