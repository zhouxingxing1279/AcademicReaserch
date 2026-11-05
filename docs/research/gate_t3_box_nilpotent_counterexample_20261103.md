# Gate T3: componentwise-box obstruction despite nilpotent observer (2026-11-03)

## Scope and checkpoint
Read main at `8486cac146ddabbc30caf6cc2365831167acfed8`: `CURRENT_CHECKPOINT.md`, `THEORY_FRAMEWORK.md`, `MODEL_CONTRACT.md`, `RESEARCH_MAP.md`, `MODEL_SELECTION_EVIDENCE.md`, and `PAPER_READING_LOG.md` (first 85 lines of each). Current Gate T3 remains phase-dependent bounded observer error / Equalized Recovery for abstract [p;v] with position-only measurement; PX4 interface work excluded.

## Mathematical question
Does the coordinatewise absolute-value box criterion `|F_sigma| r_q + delta_sigma <= r_q'` certify bounded observer error even for a stabilizing/noiseless finite-memory observer?

Consider one axis of the six-state model (three independent copies):
`T=0.1; A=[[1,T],[0,1]]; C=[1,0]; L=[1,1/T]^T`.
For the correction-before-propagation convention,
`F=A(I-LC)=[[-1,T],[-1/T,1]]`.
Direct multiplication gives `F^2=0` (up to floating point). Thus under two consecutive successful measurements, the initial error contribution is eliminated exactly, and with bounded additive disturbances `d_k`, the true error recursion `e_{k+1}=F e_k+d_k` admits a bounded two-step memory expression `e_{k+2}=F d_k+d_{k+1}`.

However `|F|=[[1,T],[1/T,1]]` has eigenvalues 2 and 0, hence spectral radius 2. A time-invariant componentwise box `r>=0` satisfying `|F|r+delta<=r` for strictly positive `delta` cannot exist. Indeed with positive left Perron eigenvector `z>0`, `z^T |F|r=2 z^T r`, so the inequality implies `z^T r + z^T delta <=0`, impossible. A finite automaton allowing success every step contains a success self-cycle, so phase boxes indexed only by the number of consecutive misses inherit this obstruction at the success phase.

**Interpretation:** Failure of this axis-aligned one-step absolute-value certificate is NOT failure of actual observer boundedness, nor evidence that physical recovery is impossible. It is a representation/conservatism counterexample: coordinatewise boxes lose sign correlations and the nilpotent cancellation. A path/finite-memory or zonotopic error set retains these correlations; an explicitly two-step blocked map can exploit `F^2=0`. For miss branches, `F_m=A` and the complete admissible-word products must still be checked; this example alone does not certify boundedness under all miss/delay paths.

## Reproducible arithmetic check
Executed locally with Python/numpy:
```python
import numpy as np
T=.1; A=np.array([[1,T],[0,1.]])
C=np.array([[1.,0.]])
L=np.array([[1.],[1/T]])
F=A@(np.eye(2)-L@C)
print(F, F@F, max(abs(np.linalg.eigvals(abs(F)))))
```
Observed `F=[[-1,0.1],[-10,1]]`, `F@F` entries at most `5.6e-17` in magnitude, and `rho(|F|)=2.0`. This is an exact algebraic counterexample supported by a floating-point sanity check, **not** a Monte Carlo result, a CZ certificate, or a complete six-state closed-loop test.

## Gate status and implications
- **Proved analytically for this frozen example:** `F^2=0`, `rho(|F|)=2`, impossibility of finite nonnegative invariant one-step box under strictly positive disturbance radii.
- **Not proved:** phase-dependent finite-language Equalized Recovery, delayed-measurement updates, general CZ truth containment, causal output-feedback Tube, terminal invariance or recursive feasibility.
- **Research decision:** do not reject a viable observer merely because componentwise one-step box LP is infeasible. Compare a two-step blocked observer bound or correlation-preserving zonotope/CZ with the one-step box baseline, using identical information and disturbances. Report failed certificate as a negative result.
- **Literature:** no new original papers read in this run; no new bibliographic claim or total-ledger modification.
- **Simulation integration:** no end-to-end simulation implemented in this run. Retain the existing Gate T3 priority; the example can become a minimal regression test in the unified abstract-model simulator.

## Next single priority
Freeze the six-state sampled double-integrator, disturbance and measurement boxes and max-two-miss automaton; enumerate all admissible words up to a recovery horizon and test correlation-preserving blocked error-set bounds against one-step box certificates, including worst-case success self-cycles. Only then assert or reject Equalized Recovery for that specified language.
