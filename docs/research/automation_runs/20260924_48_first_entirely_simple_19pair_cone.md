# Run 48 — first entirely-simple 19-pair configuration cone

- Repository start: `8d9908f72bef2c4a831cf687d2422b5bbc52771b`.
- Core question: construct one legal entirely-simple seed for the 19-pair orientation family and test endpoint-exact CC-RCI feasibility strictly inside its configuration cone.
- Literature: Mejari, Mulagaleti, Bemporad (2023), *Data-Driven Synthesis of Configuration-Constrained Robust Invariant Sets for Linear Parameter-Varying Systems*, IEEE Control Systems Letters 7:3818–3823, DOI `10.1109/LCSYS.2023.3346128`, arXiv:2309.06998. Reused only the configuration-constrained polytope geometry; not the paper's data-driven invariance condition.
- New result: a reproducible generic symmetric seed has 38/38 active halfspaces and 160 numerically enumerated vertices, each with exactly four active facets. Its CC LP has 198 variables, 6080 configuration inequalities, 18240 inequalities after endpoint-exact invariance, and 19520 after hard-state containment.
- Outcome: infeasible with `|tau|<=0.08`; still infeasible after removing vertex torque bounds. This numerically excludes this single configuration cone and shows its failure is not caused solely by the torque bound.
- Evidence boundary: seed geometry and infeasibility are floating-point NumPy/HiGHS results. No exact Farkas witness yet; do not extrapolate to other configuration cones or the full 19-pair orientation family.
- Files: `docs/learning/48_first_entirely_simple_19pair_cone.md`, `verification/check_19pair_cc_seed_cone.py`, `results/cc_19pair_seed_cone_20260924/checks.json`.
- Failed/avoided route: did not reuse the inherited-offset seed maps across changing incidence, and did not interpret a single-cone infeasibility as orientation-family infeasibility.
- Next unique priority: extract and rationally verify a small infeasibility core / dual Farkas witness for this 198-variable cone LP, preferably one independent of torque bounds; map the witness back to active sets and dynamical facet chains.
