# 55 Homothetic route correction

Date: 2026-09-26. Base: main@1c49659c762dcb96dadeb8fe7a6216570951b774.

## Core result

The previously proposed next experiment, a homothetic RCI LP on a predecessor-derived seed, is redundant with stronger certificates already present in the repository.

For S2, Chapter 43 already proves exactly that alpha*S2 is not RCI for every 0<alpha<=1. Its Fraction verifier gives alpha_crit=6254383/5940463>1.

For the Chapter-48 19-pair entirely-simple seed with offset vector q0, every configuration inequality is homogeneous: e_ij^T q<=0. Hence e_ij^T(alpha q0)=alpha e_ij^T q0<=0 for every alpha>0. The positive homothetic seed ray therefore remains in the same audited configuration cone (apart from the degenerate alpha=0 limit). Chapter 49 proves that this entire cone's endpoint-robust CC-RCI system is infeasible even with unbounded vertex torque, using an exact rational 25-row Farkas certificate:
y^T A=0, y>=0, y^T b=-3069803/88290<0.

Therefore a homothetic LP on either natural predecessor-derived seed cannot be the next useful experiment.

## Evidence

Re-run:
- verification/check_s2_homothetic_rci_obstruction.py
- verification/check_19pair_cc_exact_farkas.py
- verification/check_19pair_exact_exposed_antecedents.py

The first two provide exact rational obstructions. Chapter 53 additionally proves exact exposure certificates for 16 antecedent rows, reduced by central symmetry to eight boundary orbits.

## Literature boundary

Mejari, Mulagaleti, Bemporad, Data-Driven Synthesis of Configuration-Constrained Robust Invariant Sets for Linear Parameter-Varying Systems, IEEE Control Systems Letters 7 (2023), 3818-3823, DOI 10.1109/LCSYS.2023.3346128, supplies the fixed-orientation/variable-offset configuration-constrained polytope and vertex-control LP framework.

Gupta, Koroglu, Falcone, Computation of robust control invariant sets with predefined complexity for uncertain systems, IJRNLC 31(5), 2021, DOI 10.1002/rnc.5378, computes predefined-complexity RCI sets without a fixed feedback structure and notes that initial shape affects the outcome.

## Status

Proved/re-audited: no contraction alpha*S2, 0<alpha<=1, is RCI.

Proved by implication from Chapters 48-49: every positive homothetic scaling of the Chapter-48 seed lies in its audited configuration cone, and the exact cone-wide Farkas certificate excludes it.

Not proved: the full 19-pair orientation family is infeasible.

## Next single priority

Follow Chapter 53, not the superseded homothetic proposal: for one representative of each of the eight exact-certified symmetry orbits, construct a center-symmetry-preserving rational perturbation across the exposed boundary pair, re-enumerate global H/V incidence, retain only bounded 38-active entirely-simple seeds, and rebuild the endpoint-exact CC-RCI LP. Stop the exclusion route immediately if a feasible neighboring cone is found.
