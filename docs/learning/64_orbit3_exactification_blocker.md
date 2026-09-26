# 64 Orbit-3 exactification: reproducibility blocker and required artifact

Date: 2026-09-26. Parent branch: research/run79-orbit0-exact-farkas.

## Single question

Can the Chapter-57 numerical infeasibility of immediate neighbor orbit 3 be upgraded to a repository-reproducible exact Farkas exclusion?

## Repository audit

The current branch contains `check_orbit0_neighbor_farkas_exact.py`, but that checker stores only the already-selected 14 reduced rational rows and multipliers. It does **not** contain the program that reconstructs an arbitrary orbit crossing, enumerates its 160-vertex incidence, assembles the complete CC-RCI LP, and extracts a dual support. The Chapter-57 document likewise records only the numerical result for orbit 3.

Therefore the orbit-0 checker cannot be parameter-switched from orbit 0 to orbit 3. Inventing orbit-3 rows from orbit-0 metadata would be invalid.

## Evidence ledger

- Exact/repository-checkable: orbit 0 frozen 14-row Farkas identity; orbit 5 and transferred circuits as recorded on prior research branches.
- Numerical only: Chapter-57 orbit 3 and orbit 6 CC-RCI infeasibility.
- Geometric numerical audit: orbit 3 has 160 vertices, 38 active facets and is entirely simple.
- Missing for orbit 3: deterministic neighbor reconstruction, full rational primal-row generator, numerical dual support, and selected exact primal rows.

This run therefore does **not** upgrade orbit 3 to exact infeasible.

## Why the missing generator matters

For a certificate to prove infeasibility of the intended orbit-3 problem rather than of an unrelated frozen subsystem, the chain must be

```
orbit-3 crossing data
 -> active sets
 -> rational vertex maps
 -> complete 19-pair CC-RCI rows
 -> numerical dual support discovery
 -> exact selected rows
 -> y >= 0, y^T A = 0, y^T b < 0.
```

The final identity alone is insufficient if the selected rows cannot be traced back to the orbit-3 LP.

## New validation interface

`verification/check_frozen_rational_farkas.py` checks a JSON artifact containing every selected primal row `a`, right-hand side `b`, and multiplier `y`. It deliberately rejects metadata-only artifacts. All arithmetic uses Python `Fraction`.

This is not a substitute for the missing orbit-3 row generator; it is the exact terminal checker to be used once the generator emits the support artifact.

## Literature boundary

Gupta, Köroğlu and Falcone, *Computation of robust control invariant sets with predefined complexity for uncertain systems*, IJRNLC 31(5), 2021, DOI 10.1002/rnc.5378, already computes predefined-complexity symmetric RCI sets for uncertain systems with additive disturbances and assigns controls at extreme points.

Mejari, Mulagaleti and Bemporad, *Data-Driven Synthesis of Configuration-Constrained Robust Invariant Sets for Linear Parameter-Varying Systems*, IEEE Control Systems Letters 7, 2023, DOI 10.1109/LCSYS.2023.3346128, already uses fixed facet orientations, variable offsets and vertex controls in a configuration-constrained RCI LP.

Hence exactification is verification infrastructure, not the intended SMF/TMPC novelty.

## Failed attempt

Directly adapting the orbit-0 exact checker was rejected because its `ROWS` are frozen orbit-0 coefficients. No repository file on the audited parent branch exposes a parameterized orbit-neighbor LP constructor from which orbit-3 rows can be regenerated.

## Next single priority

Recover or implement the deterministic arbitrary-orbit neighbor/CC-RCI constructor in the repository. First target orbit 3 and make it emit a complete rational support artifact accepted by `check_frozen_rational_farkas.py`. Do not enter distance-two search before orbit 3 and 6 are closed.
