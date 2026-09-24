# Run 50 — exact Farkas circuit boundary reduction

- Repository start: `bbf22e9c65b3461b6118d334355102e9f21f5e7d`.
- Core question: before enumerating neighboring 19-pair configuration cones, determine whether chapter 49's 25-row Farkas support is support-minimal and identify the configuration boundaries that are actually essential to that exact obstruction.
- Literature checked: Mejari, Mulagaleti, Bemporad (IEEE Control Systems Letters 2023, DOI 10.1109/LCSYS.2023.3346128) for the CC-polytope scope; no novelty is claimed for CC-RCI parameterization itself.
- Exact result: the 25 selected coefficient rows have rational rank 24. Together with the chapter-49 strictly-positive null vector, this proves the support is a positive linear circuit: every selected inequality is essential to this specific Farkas contradiction.
- Boundary consequence: only four configuration inequalities occur in the circuit: `(v15, facet5)`, `(v17, facet5)`, `(v60, facet4)`, `(v62, facet4)`. A one-boundary search that leaves all four valid cannot destroy the chapter-49 certificate.
- Exact local geometry: each critical 5-row boundary incidence has three nonsingular 4-row replacement active sets, for 12 nondegenerate local flip candidates total.
- Limitation: local nonsingularity does not prove a globally valid neighboring configuration cone, and crossing a critical boundary may reveal a different Farkas obstruction.
- Verification: `python verification/check_19pair_farkas_circuit.py --output results/cc_19pair_farkas_circuit_20260924/checks.json`.
- Failure/negative attempts: no claim was made that the 12 flips are feasible cones; that requires global seed reconstruction and is deliberately deferred.
- Next unique priority: construct globally consistent entirely-simple neighboring seeds only across the four certificate-critical boundaries, then solve each complete endpoint-exact CC-RCI problem and save either a primal RCI certificate or a rationalized Farkas witness.
