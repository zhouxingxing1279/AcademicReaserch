# Chapter 62 — Support-local Farkas transfer closes three immediate neighbors

## Core question

Chapter 61's full-system column-permutation condition is sufficient but stronger than necessary: orbit 5 has 162 vertex-control variables, while the other valid immediate neighbors have 160. A full column permutation therefore cannot exist even when the rows touched by the certificate are identical after relabeling. The correct object is the submatrix touched by the Farkas support.

## Support-local transfer lemma

Let a rational certificate use row support S and let C be the columns nonzero in A_S. If a target system contains rows S' and there is a bijection of the supported columns C to C', together with positive row scalings, such that the restricted rows and right-hand sides coincide after relabeling, then the correspondingly scaled multipliers form a Farkas certificate in the target. Columns outside C' are zero in all selected rows and are irrelevant to y^T A.

This weakens Chapter 61's full-system permutation requirement and permits exact transfer between systems with different total numbers of vertex-control variables.

## Exact audit

Each neighbor was reconstructed from its Chapter-55 exposed-facet witness and Chapter-56 half-margin rational crossing. Global H/V incidence was re-enumerated; the selected primal rows were rebuilt with Fraction/SymPy arithmetic; q_(2k)=q_(2k+1) was eliminated exactly; and the weighted identities were recomputed.

For immediate neighbors 1, 4, and 7, the 13-row orbit-5 circuit transfers with unit row scaling. The only supported control-column relabelings needed are:

- orbit 1: source vertex-control 56 -> 48; 102 -> 102;
- orbit 4: source 56 -> 48; 102 -> 103;
- orbit 7: source 56 -> 48; 102 -> 102.

All other supported vertex-control columns retain their indices. In all three cases,

y^T A = 0,    y^T b = -1,

exactly, with the same 13 positive rational multipliers as orbit 5 and no torque-bound rows. Hence the audited CC-RCI systems for orbits 1, 4, and 7 are exactly infeasible even with unbounded vertex torque.

## Negative result for the remaining neighbors

Under the identity mapping of the 19 pair-offset columns, exact rowwise matching of the orbit-5 support fails for at least one selected row in each of orbits 0, 3, and 6. This is not a feasibility result. It only excludes the simplest support-local transfer. A nontrivial pair-offset symmetry may still work; otherwise a target-specific dual circuit is required.

## Literature boundary

Gupta, Köroğlu, and Falcone, "Computation of robust control invariant sets with predefined complexity for uncertain systems", International Journal of Robust and Nonlinear Control 31(5), 2021, DOI 10.1002/rnc.5378, already compute predefined-complexity symmetric RCI sets for rationally parameter-dependent systems with additive disturbances and assign independent controls to extreme points.

Mejari, Mulagaleti, and Bemporad, "Data-Driven Synthesis of Configuration-Constrained Robust Invariant Sets for Linear Parameter-Varying Systems", 2023/2024, parameterize configuration-constrained polytopes by fixed facet orientations and variable offsets and jointly compute vertex controls. The present result is therefore an exact benchmark exclusion/verification result, not a new general RCI synthesis principle.

## Evidence status

Repository-certified exact exclusion before this run: seed cone (Chapter 49) and orbit 5.

New exact calculation this run: immediate neighbors 1, 4, 7.

Still numerical infeasibility only: immediate neighbors 0, 3, 6.

Invalid 38-facet neighbor: orbit 2 (36 active facets).

## Next unique priority

Resolve orbit 0 first. Search the finite orientation-family symmetries for a nontrivial pair-offset permutation mapping the orbit-5 supported rows. If none exists, discover a target-specific numerical dual support and exactify it. Do not enter distance-two configuration search before orbit 0 is resolved.
