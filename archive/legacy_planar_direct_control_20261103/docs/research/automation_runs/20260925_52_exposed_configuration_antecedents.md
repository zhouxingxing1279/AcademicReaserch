# Research run 52 — exposed configuration antecedents

Base: c1697773a3ddf24cb333f520b518aeef46136d73.

Problem: identify true exposed configuration boundaries behind the four redundant Farkas-critical rows from Chapters 49–51.

Literature checked: Mejari, Mulagaleti, Bemporad (2023), IEEE Control Systems Letters 7:3818–3823, DOI 10.1109/LCSYS.2023.3346128; arXiv:2309.06998. It supports fixed-orientation, variable-offset configuration-constrained vertex maps and LP RCI synthesis, but does not supply this benchmark-specific antecedent reduction.

Result: 6080 generated configuration inequalities contain 640 zero rows and 2803 unique nonzero positive-scaling classes. HiGHS classifies 54 classes as exposed under the normalized homogeneous-cone redundancy test. Each of the four exact Farkas-critical rows is an exact nonnegative rational combination of six rows among those 54 classes. Therefore crossing a redundant critical row is not a valid adjacency operation; at least one exposed antecedent must fail (or a higher-codimension face must be crossed).

Evidence: class count/exposure is numerical; the four decompositions are exact Fraction/SymPy identities. No global infeasibility claim is made.

Failed/ruled-out approach: Chapter 50's 12 determinant-only flips remain algebraically nonsingular but are not justified as directly adjacent cones.

Next single priority: construct globally consistent entirely-simple neighboring seeds across the lowest-complexity exposed antecedent facets used by these exact decompositions; rebuild the endpoint-exact CC-RCI LP and save either a primal RCI certificate or a rationalized Farkas witness.
