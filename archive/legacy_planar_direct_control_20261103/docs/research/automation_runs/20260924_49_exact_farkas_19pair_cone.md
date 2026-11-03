# Run 49 — exact Farkas closure for the first 19-pair CC cone

- Repository start: `568b0481c3783dc554ecc43c1634de7dc759e039`.
- Core question: upgrade chapter-48 numerical infeasibility of one audited 19-pair configuration cone to an exact certificate.
- Literature checked: Mejari–Mulagaleti–Bemporad (IEEE L-CSS 2023, DOI `10.1109/LCSYS.2023.3346128`) for the configuration-constrained domain; Gleixner et al., *Iterative Refinement for Linear Programming* (Optimization Online, 2015) for high-precision/rational Farkas proof methodology; HiGHS documentation/background only for solver provenance.
- Result: a numerical auxiliary Farkas LP isolated 25 original inequalities. Exact rational reconstruction gives positive multipliers with `y^T A = 0` and `y^T b = -3069803/88290 < 0`.
- Support: 4 configuration rows + 20 endpoint-robust invariance rows + 1 hard-state row. No torque-bound rows, pair-offset equality rows, or q-nonnegativity rows are required.
- Proven conclusion: the chapter-48 audited configuration cone is rigorously incompatible with the stated endpoint-robust CC-RCI and hard-state conditions, even with unbounded vertex torque.
- Scope limitation: this does not exclude other configuration cones of the same 19-pair orientation family.
- Failed/avoided path: do not interpret a solver `infeasible` status or a single-cone certificate as a global orientation-family obstruction.
- Verification: `verification/check_19pair_cc_exact_farkas.py`; archived result `results/cc_19pair_exact_farkas_20260924/checks.json`.
- Next unique priority: construct minimal adjacent configuration cones by crossing one incidence boundary around the 18 vertex maps appearing in the exact witness, and test whether the obstruction persists or disappears.
