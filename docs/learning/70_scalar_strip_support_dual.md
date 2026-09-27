# Run 108 — scalar dual for controller support after one strip measurement

## Core question

Run 107 showed that generic LP support queries can miss the 20 ms target for a nonzero position packet. Before adding solver-specific warm starts, this run asks whether the actual measurement geometry admits a smaller exact optimization problem.

Freeze a zonotopic prediction
\[
Z=\{c+G\xi:\|\xi\|_\infty\le1\}
\]
and one bounded-error scalar measurement strip
\[
M=\{x:|h^Tx-y|\le r\}.
\]
For a controller direction q, define
\[
d_j=q^Tg_j,\qquad a_j=h^Tg_j,\qquad \bar y=y-h^Tc.
\]

## Proposition: exact one-dimensional dual

If Z intersects M, then
\[
h_{Z\cap M}(q)
=q^Tc+\min_{\lambda\in\mathbb R}
\left[
\lambda\bar y+r|\lambda|+
\sum_j|d_j-\lambda a_j|
\right].
\]

Proof: introduce z with a^T xi-z=bar y and |z|<=r. The primal is a feasible bounded LP. With equality multiplier lambda, maximizing the Lagrangian over the independent boxes |xi_j|<=1 and |z|<=r gives
\[
\lambda\bar y+\sum_j|d_j-\lambda a_j|+r|\lambda|.
\]
Strong LP duality gives equality.

The objective is convex piecewise linear. Therefore a minimizer can be chosen at a breakpoint
\[
\lambda\in\{0\}\cup\{d_j/a_j:a_j\ne0\},
\]
or anywhere on a flat interval whose endpoints are such breakpoints. Thus a generic high-dimensional LP is not mathematically necessary for a single scalar strip update.

## Consequences

This changes the Run-107 bottleneck. The six signed base controller queries do not intrinsically require six independent 600-variable LP solves. They share the same a_j and differ only in d_j. A direct breakpoint/slope implementation has O(m log m) comparison complexity per direction (and admits preprocessing/reuse of a_j), where m is the generator count.

This is an exact support computation for a zonotope intersected with one strip. It is not yet a result for a general constrained zonotope with multiple accumulated equalities. After several measurements are retained jointly, the dual dimension grows with the number of independent measurement constraints; generic LP/CZ machinery may again be required.

## Verification status

A standalone exact-rational verifier was prepared to compare the scalar dual against exhaustive LP-vertex enumeration on small random box-plus-strip instances, including a nonzero measurement center. Repository write of that executable was blocked by the GitHub safety layer in this run, so the code is not claimed as synchronized.

## Literature boundary

Classical zonotopic set-membership estimation already studies zonotope-strip intersection and its efficient outer approximation; Scott et al. (Automatica 2016, DOI 10.1016/j.automatica.2016.02.036) establishes constrained-zonotope intersection machinery. HiGHS provides high-performance LP/simplex infrastructure and hot-start examples. Hence neither LP duality nor strip intersection is an innovation claim.

The project-specific value is narrower: the controller-visible support interface can exploit scalar-measurement geometry before paying for a generic CZ support LP.

## Status ledger

- PROVED: exact scalar dual formula for one zonotope plus one scalar strip, under nonempty intersection.
- PROVED: minimization reduces to a one-dimensional convex piecewise-linear problem with the stated breakpoint set.
- CORRECTED: Run 107's generic-LP timing is an implementation baseline, not an intrinsic lower bound for exact support queries.
- NOT PROVED: the direct scalar solver is below 20 ms on the project machine.
- NOT PROVED: the scalar reduction survives multiple retained measurement equalities without increasing dual dimension.
- NOT PROVED: full nonlinear recursive feasibility.

## Next unique priority

Implement and benchmark the direct scalar-dual support evaluator on the frozen Run-107 nonzero packet for the six signed base controller queries. Compare exact support values against HiGHS and record median/p95 time. Then extend the derivation to k retained scalar measurement constraints and determine the largest k compatible with the 20 ms budget before CZ reduction or constraint elimination is required.
