# Run 118 — terminal compatibility of support-loss admission

Base: Run 117 branch/commit `17da59a36d93c4f9fc2573df33845d3273f1b262`.

## Core question

Run 117 proves horizon state/input facet tests for preserving a fixed shifted candidate after replacing the current exact/less-reduced error set C by a safe outer reduction R. It explicitly leaves the terminal step open. This run closes the terminal *candidate-admission* condition under fixed linear ancillary/terminal feedback and a fixed polyhedral terminal constraint, and records what is still needed for a full recursive-feasibility theorem.

## Setup

Error dynamics are
[
e^+=F e+w,qquad F=A+BK
]
(with the sign convention adjusted if the implementation uses u=v-Ke). C is the current unreduced error set and R is a safe outer reduction, C subset R. Future disturbance sets are identical for the two comparisons. Define
[
E_i(S)=F^iSoplusigoplus_{t=0}^{i-1}F^{i-1-t}W_t.
]
For every q,
[
delta_i(q)=h_{E_i(R)}(q)-h_{E_i(C)}(q)
=h_R((F^i)^Tq)-h_C((F^i)^Tq)ge0.
]

Let the nominal terminal set be the fixed polytope
[
Z_f={z:H_fzle g_f}.
]
Let z_N be the terminal nominal point of the old shifted candidate. Robust terminal membership under error tube E_N(S) is
[
H_f z_N + h_{E_N(S)}(H_f^T)le g_f
]
row by row.

## Proposition 1 — exact terminal membership admission for the fixed candidate

For terminal row j with normal f_j^T, define old robust terminal slack
[
s^f_j=g_{f,j}-f_j^Tz_N-h_{E_N(C)}(f_j).
]
The same terminal point z_N remains robustly admissible after C -> R iff
[
delta_N(f_j)le s^f_j
]
for every terminal row.

Proof: subtract the old and new row inequalities. The only changed term is the support of E_N, and its increase is exactly delta_N(f_j). This is necessary and sufficient for the fixed z_N and fixed terminal polytope.

This completes the missing finite-horizon facet check from Run 117, but by itself is NOT a recursive-feasibility theorem.

## Proposition 2 — terminal membership alone does not certify the appended tail

A shifted-candidate proof also appends the terminal controller. Membership of z_N in the robustly tightened terminal set does not imply that its successor remains there unless a terminal invariance condition is available for the *new* tube/reduction contract.

Minimal counterexample (no disturbance): scalar nominal terminal dynamics z^+=1.2 z, terminal set Z_f=[-1,1], error set zero. z_N=0.9 satisfies terminal membership, but z_{N+1}=1.08 is outside Z_f. Therefore even delta_N=0 and all terminal-membership slack tests passing cannot replace positive invariance/contractivity of the terminal ingredient.

Hence a complete shifted recursive-feasibility proof needs one of the following explicit contracts:

1. a robust positively invariant augmented terminal pair/set valid for every admitted R; or
2. an online terminal-successor certificate checking the appended terminal action and successor tube; or
3. a fixed worst-case terminal tube/set designed for a dominating error set R_max, with every admitted R subset R_max.

## Sufficient fixed-dominating-terminal construction

Assume there exists a fixed error set E_f and terminal nominal set Z_f such that:

- every admitted horizon-terminal tube satisfies E_N(R) subset E_f;
- E_f is robust positively invariant for e^+=Fe+w under terminal ancillary feedback: F E_f + W subset E_f;
- for every z in Z_f the terminal nominal law kappa_f(z) satisfies the tightened state/input constraints based on E_f;
- nominal terminal dynamics map Z_f into itself.

Then the appended terminal action is feasible for every admitted R, because E_N(R) subset E_f and support functions are monotone. Together with Run 117's stage-wise state/input slack tests, this gives the standard shifted candidate construction. This is a sufficient construction, not claimed necessary.

Important consequence: using a fixed E_f can re-introduce conservatism. The controller-relevant reduction rule can remain adaptive over stages 0,...,N, while the terminal ingredient is certified against a common dominating set. A less conservative adaptive terminal construction requires a separate invariance proof and cannot be inferred from support-loss admission alone.

## Exact falsification tests

Test A (terminal facet budget):
X_f=[-1,1], old E_N=[-0.2,0.2], reduced E_N=[-0.3,0.3], z_N=0.75.
Old terminal slack is 1-0.75-0.2=0.05. Support loss is 0.1, so 0.1>0.05 and the reduced candidate fails: 0.75+0.3=1.05>1.

Test B (membership is not invariance):
Z_f=[-1,1], E=0, z_N=0.9, z^+=1.2z. Terminal membership passes at N, successor is 1.08 and fails. This separates the terminal facet budget from the invariant-tail obligation.

Both are exact scalar arithmetic counterexamples; no floating-point simulation is used as proof.

## Literature boundary

Mayne, Seron, Rakovic (2005), Robust model predictive control of constrained linear systems with bounded disturbances, Automatica 41(2), DOI 10.1016/j.automatica.2004.08.019: classical tube tightening/recursive-feasibility framework. The shifted candidate and invariant terminal ingredient are prior art.

Mayne, Rakovic, Findeisen, Allgower (2006), Robust output feedback model predictive control of constrained linear systems, Automatica 42(7), DOI 10.1016/j.automatica.2006.03.005: bounded estimator error is coupled to tube MPC tightening and invariant-set reasoning. SMF-to-MPC coupling itself is not our novelty.

Recent tube-MPC work also continues to formulate recursive feasibility through invariant/terminal tube conditions. Therefore the candidate novelty remains narrower: controller-direction support-loss admission for estimator/CZ representation reduction, with explicit stage and terminal budgets.

## Status

PROVED:
- exact terminal facet admission condition for a fixed shifted terminal point/polytope;
- support-loss propagation remains the Run-117 formula;
- fixed dominating terminal tube construction is sufficient when its listed invariance/tightening assumptions hold.

COUNTEREXAMPLE:
- terminal membership, even with zero support loss, does not imply appended-tail feasibility without terminal invariance/contractivity.

NOT YET PROVED:
- existence/nonemptiness of a useful E_f,Z_f pair for the frozen Run-93/114 model and its actual state/input bounds;
- full recursive feasibility for the project controller;
- ISS/stability under online reduction;
- time-varying K/F/centers.

## Reproducibility gap discovered

The Run-117 next task requested reconstructing the actual old shifted nominal MPC plan and facet slacks for the frozen Run-114/116 workload. The persisted Run-117 artifact contains the support-loss theorem/counterexample but not a complete nominal MPC OCP instance (horizon, Q/R, initial nominal state, state/input halfspaces, terminal set/cost and old optimal plan). The default-branch learning documents inspected in this run likewise separate C2 geometry from C3 control and explicitly state that terminal/control feasibility was not yet closed. Therefore this run does not invent an "actual old plan" or fabricate numerical slacks.

## Next unique priority

Freeze one reproducible C3 MPC instance for the current four-state Run-93/114 abstraction: state/input halfspaces, horizon, nominal initial condition, cost, terminal feedback and terminal set. Compute a baseline optimal plan, persist every stage robust slack and terminal slack, then apply the Run-116 measurement-row deletions and Run-117/118 propagated support-loss tests. The deliverable must report which deletion is admitted without re-optimization and whether the fixed terminal invariant contract is satisfied.
