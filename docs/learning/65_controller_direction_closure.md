# Run 100 — controller-direction closure for fixed-complexity templates

## Core question

Run 99 proved a strict three-step support-certificate advantage from preserving dependency, while the older fixed-template work (09–10) proved rolling outer-approximation and shifted-cap contracts but showed that an arbitrary 18-direction template loses too much geometry. The missing question is therefore not whether fixed templates exist, but **which finite directions are sufficient to avoid immediately discarding controller-relevant dependency under affine propagation**.

This run freezes the Run-93 horizontal/reference closed loop and does not retune any controller.

## Theorem: finite backward direction closure

For an affine uncertain step
[
X^+=FX\oplus W
]
the support identity is
[
h_{X^+}(q)=h_X(F^Tq)+h_W(q).
]
Let Q be the finite set of directions actually read by state/input tightening or by a certified nonlinear-coupling bound. For an integer L define
[
H_L(Q)=\{\pm(F^T)^j q:q\in Q, j=0,\ldots,L\}.
]

If the template at the current step stores exact supports in every direction of H_L(Q), then for every q in Q the affine propagation support can be evaluated without template loss for L consecutive steps: at depth i it only needs the stored direction (F^T)^i q. This follows immediately by repeated application of the support identity.

With reliable upper bounds rather than exact supports, the same recursion remains a reliable outer certificate, but equality with the exact reachable support is no longer claimed.

The construction is fixed-complexity for fixed L and Q. It does **not** imply finite closure for arbitrary time: in general (F^T)^(L+1)q is a new direction. Hence this is a finite-gap/horizon result, not an invariant finite-direction theorem.

## Why the preimage directions are necessary

A two-dimensional exact counterexample shows why coordinate templates can destroy correlation. Let
[
A=\begin{bmatrix}1&1\\0&1\end{bmatrix},\quad q=e_1,
]
and X={(t,-t): |t|<=1}. X and its coordinate-box outer approximation [-1,1]^2 have identical coordinate supports. But A^T q=(1,1)^T, so
[
h_{AX}(e_1)=h_X(1,1)=0,
]
whereas the coordinate box gives 2. The missing backward direction is exactly the correlation direction needed by the next controller query. Thus outer containment alone does not protect tightening precision.

## Current four-state direction library

The repository contract allows at most 15 ticks between successful position packets. For the frozen Run-93 matrix F, use L=15.

Base controller-read seeds are e_v, e_psi and K^T (the mu direction). To preserve the specific Run-99 three-step psi certificate, also include its two dependency queries
[
q_\pm=(F^3)^Te_\psi\pm C e_\psi,
\qquad C=(e_\psi^TF^2G)U_z^{cert}.
]

Thus Q has five seeds. Exact rational generation of H_15(Q) gives 160 signed facets; no duplicates occur in this instance. The count is independent of runtime and of the number of filter updates. This is larger than the 18-facet template rejected in Chapter 10, so it is a theoretical sufficiency candidate, **not yet a 20 ms design**.

Because q_+ and q_- themselves are template directions, the two support queries used in Run 99 are not discarded at the compression boundary. Therefore the previously proved strict comparison between the joint and scalar-box certificate can be exported as two distinct stored certified bounds in those directions. This statement concerns the published certificate values; it does not claim that a redundant template facet equals the exact nonlinear reachable support.

## Shifted-set compatibility

Chapters 09–10 already proved the correct rolling contract: a new reliable bound may be capped by the valid old shifted template bound. The present direction choice is compatible with that result because H is fixed. If beta^n <= beta^o componentwise, then
[
P_H(\beta^n)\subseteq P_H(\beta^o).
]
More generally, if a newly propagated/updated set C is known to lie in the old shifted template and U_i >= h_C(H_i), publishing
[
\beta_i^n=\min\{U_i,\beta_i^o\}
]
retains C and cannot enlarge the old shifted template. This is exactly the cap theorem of Chapter 09; the new result here is the controller-derived finite direction library, not a new recursive-feasibility theorem.

Full MPC recursive feasibility remains blocked by the terminal append/control-side tube obligations already listed in Chapter 09.

## Literature boundary

Template polyhedra and support-function reachability are established tools; SpaceEx-style reachability uses predefined support directions, and Bogomolov, Frehse, Giacobbe and Henzinger (TACAS 2017, DOI 10.1007/978-3-662-54577-5_34) explicitly study refinement of template directions to remove spurious counterexamples. Scott et al. (Automatica 2016, DOI 10.1016/j.automatica.2016.02.036) already provide conservative constrained-zonotope complexity reduction. Therefore neither fixed templates nor direction refinement is an innovation claim.

The project-specific candidate contribution remains narrower: derive directions from the MPC/terminal controller's finite support queries, preserve only the dependency needed by those queries, and combine that bounded interface with the shifted-cap contract so that certified tightening improvement is not lost at compression.

## Status ledger

- **Proved:** H_L(Q) is sufficient to avoid template-direction loss for Q over L affine propagation steps when exact supports are stored.
- **Proved:** coordinate-only/insufficient templates can lose correlation even though they remain reliable outer sets.
- **Exact rational instance check:** the Run-93/99 five-seed, L=15 library has 160 signed facets and contains every required one-step backward successor through depth 15.
- **Proved previously and reused:** fixed-H componentwise caps preserve shifted-template inclusion when the old cap is valid.
- **Not proved:** 160 facets meet the 20 ms budget.
- **Not proved:** nonlinear measurement/update/remainder operations preserve Run-99's numerical advantage after all 15 ticks.
- **Not proved:** full MPC recursive feasibility.

## Next unique priority

Do not add more directions heuristically. Benchmark nested libraries H_L for L in {1,3,5,10,15} on the same observation/dropout contract and equal solver budget. For each L, record certified v_x, psi and mu bounds, first physical-domain failure, support-query time, and whether the Run-99 strict joint-vs-box witness survives. The target is the smallest L that preserves the controller-relevant advantage and keeps the shifted-cap contract while satisfying the online budget; if none does, record that fixed-template compression is not viable for this interface and retain a CZ/CPZ object instead.
