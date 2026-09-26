# 58 Rational exactification of neighboring-cone infeasibility

Date: 2026-09-26. Parent: Chapter 57.

## Core question

Chapter 57 reports HiGHS infeasibility for the seven valid immediate symmetric neighbors, but correctly labels this as numerical evidence. Before searching distance-two configurations, determine whether an infeasible neighboring CC-RCI LP can, in principle and in implementation, be upgraded to an exact certificate without exactifying the floating-point H/V enumeration itself.

## Proposition: support exactification is sufficient

Write a fixed neighboring-cone CC-RCI feasibility problem as

\[
A z \le b,
\]

where \(z\) contains pair offsets and vertex controls. Once the active sets of the audited neighboring configuration are frozen, all rows can be rebuilt from the repository's rational orientation normals, rational thrust endpoints, rational disturbance bounds, rational hard-state bounds, and inverses of rational active-normal matrices. Hence the rebuilt \(A,b\) are rational.

If a candidate nonnegative dual ray has support \(S\), it is unnecessary to rationalize the floating-point multipliers directly. Rebuild only the selected rows exactly and solve

\[
A_S^\top y_S=0,\qquad
b_S^\top y_S=-1,\qquad
y_S\ge0.
\]

Any feasible rational \(y_S\) is an exact Farkas certificate, because multiplying the primal inequalities by \(y_S\) gives \(0\le-1\). The normalization \(b_S^\top y_S=-1\) removes arbitrary ray scaling. Conversely, failure on one discovered support does **not** prove primal feasibility: enlarge/change the support and retry.

This separates the roles of floating-point and exact arithmetic:

1. numerical H/V enumeration identifies a candidate neighboring incidence;
2. HiGHS identifies an infeasible LP and a sparse candidate dual support;
3. the selected primal rows are reconstructed from exact rational data;
4. an exact nullspace/LP solve produces \(y_S\);
5. the final audit checks \(y_S\ge0\), \(A_S^\top y_S=0\), and \(b_S^\top y_S<0\) with rational arithmetic.

Only step 5 upgrades the neighboring cone from "numerically infeasible" to "exactly excluded".

## Why this matters for orbit 5

Orbit 5 has 162 vertices rather than 160, so the Chapter-49 certificate cannot be transferred merely by reusing vertex indices. Its own active sets must be frozen and its selected rows rebuilt. However, the 162-vertex geometry does not obstruct exact certification: every vertex map is an inverse of a 4-by-4 rational active-normal matrix, hence remains rational.

Therefore the current blocker is not existence of an exact representation; it is extraction of a useful sparse dual support from the orbit-5 LP and exact reconstruction of those rows.

## Existing certificate as regression case

The Chapter-49 script `verification/check_19pair_cc_exact_farkas.py` already implements the final pattern for the seed cone: 25 exact rows, positive rational multipliers,

\[
y^\top A=0,\qquad
y^\top b=-3069803/88290<0.
\]

That script should be treated as the regression oracle for the orbit-5 exactifier. The new implementation should first reproduce the Chapter-49 certificate through the generic support-exactification path, then consume the orbit-5 support.

## Evidence status

**Proved:** for any frozen neighboring incidence whose CC-RCI rows are rebuilt from the stated rational benchmark data, a rational Farkas vector satisfying the three checks above is an exact infeasibility certificate. Exactification needs only the selected support rows, not the whole LP.

**Numerical only:** Chapter 57's claim that orbit 5 (and the other six valid immediate neighbors) is infeasible. No orbit-5 dual support or rational multiplier vector is committed yet.

**Not implied:** inability to exactify one numerical support does not invalidate HiGHS' observation and does not exclude or certify the cone.

## Literature boundary

Mejari, Mulagaleti and Bemporad, *Data-Driven Synthesis of Configuration-Constrained Robust Invariant Sets for Linear Parameter-Varying Systems*, IEEE Control Systems Letters 7 (2023), 3818-3823, DOI 10.1109/LCSYS.2023.3346128, parameterizes RCI sets as configuration-constrained polytopes and computes the set plus vertex controls through an LP. The present exactification is a verification layer for our benchmark, not a new RCI synthesis principle.

Gupta et al., *Computation of Robust Control Invariant Sets with Predefined Complexity for Uncertain Systems*, IJRNLC 31 (2021), DOI 10.1002/rnc.5378, likewise establishes that vertex-wise controls can induce a PWA controller without a prescribed feedback gain. This remains baseline machinery.

## Repository correction

The current run71 branch does contain `verification/check_19pair_symmetric_boundary_orbits.py`. Earlier prose saying that this verifier had not entered the remote repository is stale and must not be propagated to later logs. Chapter 57's neighbor-crossing verifier itself is still absent from the branch.

## Next single priority

Reconstruct the orbit-5 neighbor deterministically, export its complete rational CC-RCI matrix together with HiGHS' infeasibility dual support, and exactify that support by solving the normalized rational system above. Commit the support metadata and a Fraction/SymPy verifier. Only after an exact orbit-5 certificate exists should we test support transfer to the other six immediate neighbors or move to distance-two configurations.
