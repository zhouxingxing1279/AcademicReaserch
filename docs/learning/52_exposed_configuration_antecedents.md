# 52 Exposed configuration antecedents

Date: 2026-09-25. Base revision: `c1697773a3ddf24cb333f520b518aeef46136d73`.

Chapter 51 showed that the four configuration rows in the Chapter-49 exact Farkas circuit are redundant consequences. This chapter audits the true exposed antecedents.

For 160 vertex maps and 38 halfspace orientations, the generated system has 6080 rows `C_j V_i q-q_j <= 0`. Exact positive-scaling deduplication gives 2803 nonzero row classes; 640 generated rows are identically zero. A normalized HiGHS redundancy audit classifies 54 classes as exposed facets of the audited homogeneous cone.

Each of the four Farkas-critical rows is then verified, coefficient by coefficient over rational arithmetic, as a nonnegative combination of six rows from those exposed classes. For `e_(15,5)`, the exposed antecedents `(2,19),(54,32),(63,20),(71,22),(85,31),(89,29)` have multipliers `10000/981,1/150,1/150,2500/2943,1,10000/981`. The other three exact decompositions are archived in the result JSON and verification script.

Thus a path in offset space cannot invalidate a critical consequence while all its exposed antecedents remain satisfied. Genuine neighboring-cone search must cross an exposed antecedent facet or a higher-codimension face, not the redundant critical row itself.

Evidence boundary: 2803 and 54 are numerical geometry facts because exposed-facet classification uses floating-point HiGHS. The four six-term decompositions are exact rational identities once candidate exposed rows are selected. We do not claim 54 as an exact irredundant-facet theorem.

Literature: M. Mejari, S. K. Mulagaleti, A. Bemporad, *Data-Driven Synthesis of Configuration-Constrained Robust Invariant Sets for Linear Parameter-Varying Systems*, IEEE Control Systems Letters 7 (2023), 3818-3823, DOI 10.1109/LCSYS.2023.3346128. It supplies the fixed-orientation/variable-offset CC-polytope and vertex-map machinery; the exposed-antecedent audit is benchmark-specific.

Next priority: construct globally consistent entirely-simple seeds across the lowest-complexity exposed antecedent facets occurring in the four exact decompositions, then rebuild the endpoint-exact CC-RCI LP for each genuine neighbor.
