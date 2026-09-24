# 53 Exact exposed-facet certificates for the Farkas antecedents

Date: 2026-09-25. Base: Chapter 52 (`a0abc759c5b3ad28ffc9d74ae0dc4c677a5a47be`).

## Core question

Chapter 52 used HiGHS to classify 54 configuration-row classes as exposed and then expressed each Chapter-49 Farkas-critical row as a nonnegative combination of six of them. The remaining gap was whether the 16 distinct witness-relevant antecedent rows are genuinely exposed facets or numerical false positives.

For each distinct configuration class
[
e_k^Tq\le 0,
]
we seek a rational relative-interior witness satisfying
[
e_k^Tq^\star=0,\qquad e_\ell^Tq^\star<0\quad\forall \ell\ne k.
]
Such a point proves that the target inequality supports a codimension-one exposed face of the audited cone and is not implied as equality by another class.

## Exact certificate construction

HiGHS is used only for discovery: solve `e_k q=0` with every other distinct class constrained by `e_l q<=-1`. The returned point is rounded to 1e-5 and then projected **exactly** onto the target rational hyperplane by solving one offset coordinate with `Fraction` arithmetic. Finally all 2802 other distinct nonzero classes are reevaluated exactly.

All 16 witness-relevant rows pass. The largest (least negative) exact slack among all non-target classes remains strictly negative for every certificate. Representative margins include:

- `(2,19)`: `-11478953/16350000`;
- `(54,32)`: `-147044879/147150000`;
- `(85,31)`: `-2344801/2452500`;
- `(15,33)`: `-435/436`;
- `(42,18)`: `-98072239/98100000`;
- `(60,32)`: `-1955/1962`.

Therefore the Chapter-52 exposure claim for the 16 Farkas-relevant antecedents is upgraded from numerical evidence to exact rational certification.

## Symmetry quotient

The 16 certified facets form eight center-symmetry pairs:
`(2,19)<->(42,18)`, `(54,32)<->(25,33)`, `(63,20)<->(18,21)`, `(71,22)<->(33,23)`, `(85,31)<->(76,30)`, `(89,29)<->(78,28)`, `(15,33)<->(60,32)`, and `(23,21)<->(52,20)`.

Hence a center-symmetry-preserving one-facet escape search from the Chapter-49 obstruction needs only eight inequivalent boundary orbits, not 16 rows or the original 6080 generated inequalities.

## What is and is not proved

**Proved for the audited seed cone:** all 16 witness-relevant antecedents are exposed facets, with rational relative-interior witnesses and strict exact separation from every other distinct configuration-row class.

**Not proved:** crossing one of these facets yields a globally consistent entirely-simple neighboring configuration; nor is any neighbor yet proved RCI feasible/infeasible. The result also does not exclude the full 19-pair orientation family.

## Literature boundary

Mejari, Mulagaleti, Bemporad, *Data-Driven Synthesis of Configuration-Constrained Robust Invariant Sets for Linear Parameter-Varying Systems*, IEEE Control Systems Letters 7 (2023), 3818–3823, DOI 10.1109/LCSYS.2023.3346128, provides the fixed-orientation/variable-offset configuration-constrained polytope and vertex-map framework. Recent configuration-constrained Tube MPC work (Badalamenti et al., arXiv:2505.14440, 2025) additionally shows that template selection and complexity/conservatism tradeoffs are already active research topics. Therefore our potential contribution cannot be merely “use a configuration-constrained tube”; it must rest on the SMF-certified online-set interface and a provable conservatism comparison.

## Reproduction

Run:

`python verification/check_19pair_exact_exposed_antecedents.py --output results/cc_19pair_exact_exposed_antecedents_20260925/checks.json`

The final exposure checks use rational arithmetic only; HiGHS only discovers candidate interior points.

## Next single priority

For one representative from each of the eight exact-certified boundary orbits, cross the facet by a controlled rational offset perturbation, re-enumerate the global H/V incidence, and retain only seeds that are bounded, 38-facet-active and entirely simple. For each genuine neighboring cone, rebuild the endpoint-exact CC-RCI LP. Stop the exclusion route immediately if a feasible neighbor is found and archive its primal RCI certificate.
