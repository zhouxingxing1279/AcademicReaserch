# Parameter-dependent Offset Endpoint Counterexample Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an exact verifier proving that thrust-endpoint checks do not certify an affine-offset parameter-dependent RCI family.

**Architecture:** A dependency-light Python checker uses `fractions.Fraction` to maximize scalar quadratics on a closed rational interval and instantiates the frozen counterexample. A unittest module fixes the mathematical contract and checks archived JSON reproducibility; research documents record the literature gate and scope.

**Tech Stack:** Python standard library (`Fraction`, `json`, `argparse`, `hashlib`, `unittest`), Markdown.

**Spec:** `docs/superpowers/specs/2026-10-29-pd-offset-endpoint-counterexample-design.md`

## Global Constraints

- All mathematical claims use exact rational arithmetic.
- The frozen example is `p in [0,1]`, `q(p)=1+p`, `a(p)=1-p/2`, common target radius `1`.
- Evidence is `COUNTEREXAMPLE`; Gate A remains blocked.
- No claim about general PD-RCI nonexistence, six-state safety, or recursive MPC feasibility.

## Review Focus

- Concave quadratic with an interior stationary maximum must inspect that point.
- Convex quadratic must maximize at an endpoint and not treat its stationary point as a maximum.
- Linear and constant degeneracies must remain exact.
- Reversed or empty intervals must fail explicitly.
- Archived results must bind the checker, test, literature gate, and design by SHA-256.

---

### Task 1: Exact interval maximizer and counterexample tests

**Files:**
- Create: `verification/check_pd_offset_endpoint_counterexample.py`
- Create: `verification/test_pd_offset_endpoint_counterexample.py`

**Interfaces:**
- Produces: `quadratic_max_on_interval(a: Fraction, b: Fraction, c: Fraction, lower: Fraction, upper: Fraction) -> dict`
- Produces: `build_report(root: Path) -> dict`

- [x] Write failing tests for the frozen `9/8` interior violation, concave/convex/linear cases, invalid intervals, scope labels, dependency hashes, CLI reproduction, and perturbation of the frozen algebra.
- [x] Run `python -m unittest verification.test_pd_offset_endpoint_counterexample -v`; expect import/failure because the checker does not exist.
- [x] Implement the exact interval maximizer, frozen-contract assertions, report construction, and CLI JSON writer.
- [x] Re-run the focused test; expect all tests to pass after the result artifact exists in Task 2.

### Task 2: Literature gate, archived evidence, and research state

**Files:**
- Create: `docs/research/run196_literature_gate.md`
- Create: `docs/learning/129_pd_offset_endpoint_counterexample.md`
- Create: `docs/research/run196_research_log.md`
- Create: `results/pd_offset_endpoint_counterexample_20261029/checks.json`
- Modify: `docs/literature/READ_PAPERS.md`
- Modify: `docs/research/current_checkpoint.md`
- Modify: `docs/research/automation_research_log.md`

**Interfaces:**
- Consumes: `build_report(root)` and the checker CLI from Task 1.
- Produces: hash-bound archived JSON and a short checkpoint with the next single blocker.

- [x] Write the literature gate from targeted full-text reading of Gupta et al. 2023 and Mulagaleti et al. 2025, distinguishing arbitrary successor scheduling, common-target intersection, and polynomial/LMI certification.
- [x] Run the checker CLI to create the archived JSON, then run the focused test suite.
- [x] Record derivation, exact result, limitations, commands, and source hashes in the learning note and detailed log.
- [x] Update the paper ledger, short checkpoint, and cumulative automation log without expanding historical geometry branches.
- [x] Re-run the checker after all hash-bound files are final, then run project and verification test suites.

### Task 3: Final verification and repository delivery

**Files:**
- Modify only files required to repair verification failures.

**Interfaces:**
- Consumes: all Task 1–2 artifacts.
- Produces: a clean commit and synchronized research branch.

- [x] Run `python -m unittest discover -s tests -v` and require all tests pass.
- [x] Run `python -m unittest discover -s verification -p 'test_*.py' -v` and require all tests pass.
- [x] Run the checker into a temporary path and compare parsed JSON with the archive.
- [x] Inspect `git diff --check`, status, and diff scope.
- [x] Commit the verified increment and push `research/run196-pd-offset-contract`; independently compare remote and local tree hashes.
