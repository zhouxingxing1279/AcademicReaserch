# Shifted Reachable-Set Inclusion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prove and mechanically check the cross-time reachable-set inclusion needed to connect the reliable CZ estimator interface to recursive-feasibility reasoning under intermittent measurements.

**Architecture:** Add one exact-rational verification module for affine set propagation and support bounds, then document the theorem that separates estimator-set nesting from MPC shifted-candidate feasibility. The certificate uses the old shifted control tail as the reference, treats center translations as absolute-set translations, permits no-measurement updates without fictitious contraction, and accepts disturbance updates only when set inclusion is independently certified.

**Tech Stack:** Python standard library (`fractions`, `json`, `hashlib`, `unittest`), NumPy object arrays for exact rational matrix bookkeeping, Markdown/LaTeX theory documentation.

**Spec:** `docs/learning/08_constrained_zonotope_interface.md`

## Global Constraints

- Use the six-state planar model and intermittent-position-measurement contract in `configs/planar_baseline.json`.
- Do not restore the superseded Transformer/jerk research direction.
- Do not claim that a newly optimized MPC trajectory is nested in the old optimum; prove feasibility only for the old shifted candidate.
- Do not shrink future disturbance sets from observed samples; nesting must be an explicit assumption or certificate.
- Preserve exact rational pass/fail decisions; floating-point optimization may propose but not certify.
- Do not claim full recursive feasibility until a terminal robust invariant condition and a valid control-side tube are separately established.

---

### Task 1: Analytic Contract Regressions

**Files:**
- Create: `verification/test_shifted_reachable_inclusion.py`
- Create: `verification/check_shifted_reachable_inclusion.py`

**Interfaces:**
- Consumes: affine set recurrence `R^+ = F R + B u + W`, posterior inclusion, and the dropout automaton contract.
- Produces: `AffineBox`, `shifted_inclusion_certificate(...)`, and counterexample records used by the research document.

- [ ] **Step 1: Write failing tests**

  Cover: posterior intersection contracts the absolute state set; recentering alone does not contract an absolute set; equal shifted controls plus nested disturbances preserve inclusion; a changed control can break inclusion; a larger disturbance set can break inclusion; no measurement is identity rather than contraction; and an allowed dropout successor has the expected path-prefix relation.

- [ ] **Step 2: Run the focused test and confirm failure**

  Run: `python -m unittest discover -s verification -p test_shifted_reachable_inclusion.py -v`

- [ ] **Step 3: Implement the minimum exact-rational contract checker**

  Use axis-aligned affine boxes so all inclusions and counterexamples are exact. Return named Boolean obligations rather than a single opaque pass flag.

- [ ] **Step 4: Run the focused test and confirm pass**

  Run the command from Step 2 and require all tests to pass.

### Task 2: Six-State Shift Certificate

**Files:**
- Modify: `verification/check_shifted_reachable_inclusion.py`
- Create: `results/theory_shifted_reachable_20260917/exact_checks.json`

**Interfaces:**
- Consumes: the exact `dt`, gravity, state order, sensing period, dropout bound, and physical affine remainder bounds from `configs/planar_baseline.json`.
- Produces: a JSON certificate containing positive cases, necessary counterexamples, source hashes, and an explicit control-gate status.

- [ ] **Step 1: Add a failing six-state horizon test**

  Check stages `0..25` for two allowed actual successors: a position success and a position miss. Use a strictly smaller posterior box, the identical shifted control sequence, and a nested disturbance box.

- [ ] **Step 2: Implement exact stage propagation and inclusion checks**

  Record every coordinate margin `old_radius - (abs(new_center-old_center)+new_radius)`. Include counterexamples for changed control, non-nested disturbance, and comparing radii while omitting center displacement.

- [ ] **Step 3: Generate the immutable result artifact**

  Run: `python verification/check_shifted_reachable_inclusion.py --output results/theory_shifted_reachable_20260917/exact_checks.json`

- [ ] **Step 4: Re-run and independently inspect certificate gates**

  Require `status=pass`, `shifted_reachable_gate=pass_for_declared_affine_contract`, and `recursive_feasibility_gate=blocked_pending_control_terminal_certificate`.

### Task 3: Theorem and Repository Integration

**Files:**
- Create: `docs/learning/09_shifted_reachable_inclusion.md`
- Modify: `docs/learning/08_constrained_zonotope_interface.md`
- Modify: `README.md`
- Modify: `verification/README.md`

**Interfaces:**
- Consumes: the exact certificate from Task 2 and the template-sandwich result from the literature analysis.
- Produces: a theorem with assumptions, proof, failure cases, six-state instantiation, and the precise remaining route to Theorem D (recursive feasibility).

- [ ] **Step 1: State the absolute-set shifted-inclusion theorem**

  Define old and new reachable sets, distinguish estimator center from absolute state, and prove inclusion by affine-map/Minkowski-sum monotonicity under the same shifted input tail and nested disturbance sets.

- [ ] **Step 2: Connect the theorem to fixed-template support bounds**

  State `b_new = min(beta, b_old)` only after proving the true reachable set is inside both operands. Explain why this is an interface certificate, not generic CZ reduction.

- [ ] **Step 3: State recursive-feasibility corollary conditionally**

  List the still-missing control-side tube, terminal invariant set, domain validity, and terminal append-law obligations. Mark full MPC admission blocked until these exist.

- [ ] **Step 4: Update navigation and reproduction commands**

  Link the new document and exact artifact without changing the declared primary research architecture.

### Task 4: Verification and Version Control

**Files:**
- Verify all files changed in Tasks 1–3.

**Interfaces:**
- Consumes: all new tests, certificate generator, result, and documentation.
- Produces: a reviewed commit on `main` suitable for pushing to `origin/main`.

- [ ] **Step 1: Run focused tests**

  Run: `python -m unittest discover -s verification -p test_shifted_reachable_inclusion.py -v`

- [ ] **Step 2: Run the existing CZ and radius regressions**

  Run the constrained-zonotope and mode-radius test files to ensure the new theorem does not weaken prior contracts.

- [ ] **Step 3: Run the full verification suite**

  Run: `python -m unittest discover -s verification -p 'test_*.py' -v` and `python -m unittest discover -s tests -v`.

- [ ] **Step 4: Review diff and generated hashes**

  Confirm there are no placeholders, unsupported theorem claims, or accidental changes to physical parameters.

- [ ] **Step 5: Commit and push**

  Commit the theorem, verifier, tests, result, and navigation updates together, then push `main` to `origin/main`.
