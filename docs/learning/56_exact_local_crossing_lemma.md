# 56 Exact local crossing lemma

Date: 2026-09-26. Base: Chapter 55 on the parent branch.

## Question

Chapter 55 certifies eight exposed facets after restricting the 38 offsets to 19 center-symmetric pair offsets. Does each exact exposed witness admit a rational perturbation that crosses only the selected old-cone class, without accidentally crossing another class?

## Proposition

Let the distinct restricted configuration inequalities be r_i^T s <= 0. For target t, assume a rational witness s* satisfies r_t^T s*=0, r_l^T s*<0 for every l!=t, and every component of s* is positive. Choose rational d with r_t^T d>0; d=r_t is always valid.

For every non-target row with r_l^T d>0 form

    mu_l = -(r_l^T s*)/(r_l^T d),

and for every component with d_k<0 form

    nu_k = s*_k/(-d_k).

All defined mu_l and nu_k are strictly positive rationals. Hence a positive rational epsilon smaller than all of them exists. For s+=s*+epsilon d:

- r_t^T s+ > 0;
- r_l^T s+ < 0 for every l!=t;
- every component of s+ remains positive.

Proof: the target becomes epsilon r_t^T d>0. If r_l^T d<=0 its old strict negative slack cannot increase through zero. If r_l^T d>0, epsilon<mu_l preserves strict negativity. The component argument is identical using nu_k.

## Consequence

The exact Chapter-55 certificates satisfy these hypotheses. Therefore every one of the eight symmetry orbits admits an arbitrarily small rational, symmetry-preserving escape that violates only the selected restricted old-cone class while keeping positive pair offsets.

This closes only the local crossing step. It does not prove that the lifted 38-halfspace polytope after crossing is bounded, has all 38 facets active, is entirely simple, or supports an RCI certificate. Those properties require global H/V re-enumeration after crossing.

## Literature boundary

Mejari, Mulagaleti, Bemporad, "Data-Driven Synthesis of Configuration-Constrained Robust Invariant Sets for Linear Parameter-Varying Systems", IEEE Control Systems Letters 7 (2023), 3818-3823, DOI 10.1109/LCSYS.2023.3346128, supplies the fixed-orientation/variable-offset configuration-constrained RCI framework. Badalamenti et al., "Efficient Configuration-Constrained Tube MPC via Variables Restriction and Template Selection", arXiv:2505.14440 (2025), studies template refinement and complexity/conservatism trade-offs. The elementary local crossing lemma is baseline polyhedral geometry, not a claimed innovation.

## Status

Proved previously: Chapter-49 cone infeasible by exact Farkas certificate; Chapter-53 full-space antecedents exposed; Chapter-55 eight symmetric restricted orbits exposed.

Proved here: every Chapter-55 orbit has a finite-margin rational one-class crossing preserving center symmetry and positive offsets.

Still open: which crossed points are genuine bounded, 38-active, entirely-simple neighboring configurations, and whether any neighbor makes the endpoint-exact CC-RCI LP feasible.

## Next single priority

Use each stored Chapter-55 rational witness, choose a deterministic rational epsilon below the exact row and positivity margins, lift to paired 38 offsets, globally enumerate H/V incidence, and retain only bounded, 38-active, entirely-simple neighbors. Rebuild the endpoint-exact CC-RCI LP for those neighbors and stop the exclusion route immediately if a feasible primal RCI certificate appears.
