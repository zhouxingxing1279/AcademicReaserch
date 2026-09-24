# 51 Farkas-critical rows are not exposed adjacent boundaries

Date: 2026-09-25. Base revision: `923bfc2a83d42f35b066743bdb16b2516375cae3`.

## Core question

Chapter 50 reduced the exact Farkas obstruction to four configuration rows and listed 12 nonsingular local active-set replacements. This chapter checks the missing prerequisite: are those four rows actually exposed one-boundary faces of the audited configuration cone?

For a seed vertex map (x_i(q)=V_iq), write the configuration inequality as
[
e_{ij}^Tq := C_jV_iq-q_j\le0.
]

## Exact result

Rebuilding all rows with rational facet normals and exact active-set inverses gives

[
e_{15,5}=\frac{5000}{981}(e_{0,19}+e_{2,19}),
]

[
e_{17,5}=\frac12e_{2,5}+\frac12e_{15,5}+\frac{5000}{981}e_{17,3},
]

[
e_{60,4}=\frac{5000}{981}(e_{38,18}+e_{42,18}),
]

[
e_{62,4}=\frac12e_{40,4}+\frac12e_{60,4}+\frac{5000}{981}e_{62,2}.
]

All coefficients are nonnegative. Therefore every point satisfying the antecedent configuration inequalities automatically satisfies each Farkas-critical row. In particular, none of the four critical rows is an independently exposed single boundary of this H-representation of the configuration cone.

This corrects the interpretation of Chapter 50: its 12 determinant-nonsingular replacements are algebraically valid local active sets, but they cannot be treated as 12 directly adjacent configuration cones reached by crossing only the listed critical inequality.

## Consequence for the search

The Chapter-49 Farkas circuit can only be destroyed by crossing an antecedent/exposed configuration boundary (or a higher-codimension face) that makes at least one critical consequence invalid. The next search should therefore work on the irredundant configuration-cone representation, not on determinant flips of redundant rows.

This does **not** prove the full 19-pair orientation family infeasible. It only removes an invalid adjacency shortcut and narrows the correct next computation.

## Literature boundary

Mejari, Mulagaleti, Bemporad, *Data-Driven Synthesis of Configuration-Constrained Robust Invariant Sets for Linear Parameter-Varying Systems*, IEEE Control Systems Letters 7 (2023), 3818--3823, DOI 10.1109/LCSYS.2023.3346128, supplies the fixed-orientation/variable-offset configuration-constrained polytope and vertex-map machinery. The exact redundancy identities above are specific to our audited 19-pair cone and are not claimed as a new general CC-polytope theorem.

## Evidence

Run:
`python verification/check_19pair_critical_boundary_redundancy.py --output results/cc_19pair_critical_boundary_redundancy_20260925/checks.json`.

The four identities are checked with `Fraction` and exact SymPy inverses; no LP tolerance is used in the final identities.

## Next single priority

Construct an irredundant configuration-cone description around the current seed, identify which exposed rays/facets are antecedents of the four Farkas-critical rows, and test only those true neighboring cones. For each neighbor, rebuild the global entirely-simple incidence and endpoint-exact CC-RCI LP; save a primal certificate if feasible, otherwise rationalize the new Farkas witness.
