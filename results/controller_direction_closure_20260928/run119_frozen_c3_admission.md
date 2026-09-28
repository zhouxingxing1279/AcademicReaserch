# Run 119 — frozen C3 instance and measurement-row reduction admission

Base: Run 118 branch `research/run118-terminal-support-budget`.

## Core question

Run 118 showed that stage/input/terminal support-loss budgets plus a compatible invariant terminal ingredient are sufficient to preserve a fixed shifted candidate, but the repository did not contain a complete C3 OCP. This run freezes one reproducible C3 instance on the existing Run-93/114 four-state abstraction and asks a single question: do the two Run-116 pure measurement-row deletions pass the Run-117/118 admission test on the same baseline plan?

This is a newly frozen verification instance, not a claim that an older unpersisted MPC plan has been reconstructed.

## Frozen C3 instance

State is x=(p_x,v_x,psi,rho). Sampling h=0.02, g=9.81. Nominal dynamics are z+=Az+Bv with
A=[[1,h,0,0],[0,1,-hg,0],[0,0,1,h],[0,0,0,1]], B=(0,0,0,1)^T.
Ancillary feedback is u=v-Ke with
K=(-0.1075,-0.1837,1.1637,0.3226), so F=A-BK is exactly the Run-93 closed-loop matrix.

Hard symmetric bounds are frozen as
|p_x|<=5, |v_x|<=3, |psi|<=0.44, |rho|<=2, |u|<=0.0672.
The first three state bounds and action bound come from the repository horizontal/reference contract; rho uses the existing angular-rate envelope 2 as the C3 verification bound.

Horizon N=30, initial nominal state z0=(0.001,0,0,0), stage cost z^T diag(1,0.2,1,0.1) z + 0.05 v^2, and terminal equality z_N=0. The terminal nominal set is therefore {0}.

The current error set C is the corrected Run-114 601-latent, two-position-packet posterior with y0=0.01, y1=0.012, radius 0.02. Future disturbance sets are the frozen Run-93 scalar injection W=D0 G[-1,1], D0=3403343/1600000, G=(0,0.02,0,0)^T.

## Terminal contract

Let S be the infinite mRPI
S = direct_sum_{j>=0} D0 F^j G[-1,1].
By construction F S + W = S. The unreduced C and either pure row-deletion outer set R remain subsets of the underlying 601-generator prediction, which is a finite partial sum of S. Therefore every propagated admitted terminal error tube remains inside S.

A 5000-term numerical diagnostic gives coordinate supports approximately
(2.34719570, 2.48462294, 0.36439760, 0.70073783)
and h_S(K) approximately 0.05567584, all strictly below the frozen state/input bounds. These decimals are numerical diagnostics, not the proof of invariance; invariance is the series identity above. The repository already contains the exact-tail machinery needed to replace these diagnostics by rational upper certificates if this C3 instance is retained.

Thus {0} with terminal law v=0 and dominating error tube S supplies a deliberately conservative but explicit terminal append contract.

## Baseline solve and admission result

The baseline OCP was solved numerically with SciPy SLSQP while every robust tightening support was computed by HiGHS on the same lifted posterior. The solve terminates successfully with terminal infinity norm below 1.1e-16. The minimum state-facet robust slack is about 9.52e-2. At least one input facet is active to numerical tolerance; the nominal action ranges approximately from -0.01494624 to 0.01256636.

For each stage i and each state/input facet, the Run-117 quantity
delta_i(q)=h_R((F^i)^T q)-h_C((F^i)^T q)
was compared with the baseline robust slack.

**Delete older packet y0:** rejected. Violations occur at stage 0 and stage 1 on the upper input-tightening direction, with excesses about 1.0187e-4 and 1.0606e-4, and at stage 29 on the opposite input direction with excess about 9.04e-7. Hence the same baseline candidate is not certified feasible after this deletion.

**Delete newer packet y1:** admitted for every tested stage state/input facet; no positive delta-minus-slack violation above 1e-8 was found. Since the row-deletion set is contained in S and z_N=0, the fixed dominating terminal contract also passes for this verification instance.

This gives the first project-instance numerical separation in which two safe outer reductions have different MPC admissibility despite both preserving true-set containment.

## What is proved and what is numerical

Proved from Runs 116-118 and reused here: pure row deletion preserves C subset R subset P; support loss propagates as delta_i(q); delta_i<=slack is the exact fixed-candidate facet admission test; the infinite-series S satisfies F S + W = S.

Numerical observation in this run: the particular SLSQP baseline plan, its slacks, and the pass/fail classification above. Solver tolerances are not a formal proof. Before elevating this instance to a theorem-quality benchmark, persist the executable verifier and replace the 5000-term terminal admissibility diagnostic with the repository's rational tail certificate.

## Literature boundary

Mayne, Rakovic, Findeisen and Allgower, *Robust output feedback model predictive control of constrained linear systems*, Automatica 42(7), 2006, DOI 10.1016/j.automatica.2006.03.005, already couples bounded estimator error to invariant tubes and tightened nominal constraints.

Koehler, Koetting, Soloperto, Allgower and Mueller, *A robust adaptive model predictive control framework for nonlinear uncertain systems*, IJ Robust Nonlinear Control 31, 2021, DOI 10.1002/rnc.5147, already derives monotonic/non-increasing estimation/tube update conditions sufficient for robust recursive feasibility and constraint satisfaction.

Therefore neither online set shrinking nor terminal invariance is an innovation claim. The narrower candidate remains MPC-slack-aware admission of estimator/CZ representation reduction using controller-direction support loss.

## Status and next unique priority

- PROVED previously and instantiated here: the admission inequalities and fixed-dominating-terminal logic.
- NUMERICAL: baseline optimal plan and deletion separation.
- REJECTED on this instance: deleting the older packet without re-optimization.
- ADMITTED numerically on this instance: deleting the newer packet without re-optimization.
- OPEN: proof-quality rational terminal support bounds and an executable persisted verifier; repeated closed-loop updates with changing centers/measurements; ISS/stability.

Next unique priority: make this Run-119 C3 benchmark proof-quality and reproducible. Persist an executable verifier, replace the long-sum terminal checks by exact/rational tail upper bounds, and independently recompute the baseline/admission result. Only after that should the work move to repeated online reductions or stability.
