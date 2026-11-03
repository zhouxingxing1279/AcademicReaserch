# Run 51 — critical boundary redundancy

Base: `923bfc2a83d42f35b066743bdb16b2516375cae3`.

Question: whether the four Chapter-50 Farkas-critical configuration inequalities are exposed one-boundary faces suitable for direct neighboring-cone flips.

Result: no. Exact rational reconstruction proves all four are nonnegative combinations of other configuration inequalities. Hence Chapter 50's 12 nonsingular determinant flips are not directly adjacent cones. This is a correction/narrowing result, not a positive RCI result.

Evidence: `verification/check_19pair_critical_boundary_redundancy.py` and `results/cc_19pair_critical_boundary_redundancy_20260925/checks.json`.

Literature: Mejari, Mulagaleti, Bemporad (2023), IEEE Control Systems Letters 7:3818–3823, DOI 10.1109/LCSYS.2023.3346128. It justifies the CC vertex-map framework; it does not supply these benchmark-specific redundancy identities.

Next only priority: reduce the configuration cone itself to an irredundant/exposed-boundary representation and trace which exposed antecedent boundaries can invalidate the four critical consequence rows; then audit those true neighboring cones.
