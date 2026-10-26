# Single-Slant Shape Gate Design

## Intent

Determine exactly whether one position--velocity coupled normal pair can remove the specific velocity-radius cycle obstruction certified in Run184, before building a full correlated information-ensemble LP.

## Goals and non-goals

- Preserve Run183's exact vertical adapter, packet graph, fixed disturbance and measurement halfwidth.
- Use `q=p-(1/10)v` and exact rational arithmetic.
- Determine exactly whether a 15-mode periodic radius schedule exists; preserve an exact obstruction when it does not.
- Check every legal 5/10/15-step success return, not only the shortest packet cycle.
- Derive the signed coordinate transform independently before taking support radii.
- Do not synthesize centers, controls, `G/Lambda`, `Z/H/Omega`, an invariant information ensemble, or an MPC terminal set.
- Do not claim novelty from adding a facet pair.

## Approaches considered

1. **Implement the full six-facet graph LP now.** This would answer more, but it couples configuration changes, meta-center outer approximation and endpoint preservation in one high-risk step. Rejected until the shape obstruction is known to be removable.
2. **Exact two-radius gate (selected).** Track `r_p` and `r_q` for the parallelogram outer shape. The original velocity facets may be retained as redundant hard-state checks. This isolates the one fact needed to justify a full LP.
3. **Jump directly to a constrained-zonotope graph.** CZ operations preserve correlation naturally, but this changes both representation and computational budget, preventing a clean comparison with Run184. Deferred as a strong later baseline.

The automation request explicitly asks to test whether the minimum facet pair breaks the old cycle first, so approach 2 is the least-assumption implementation.

## Exact recurrence

For `h=1/50`, `kappa=1/10`, and velocity disturbance halfwidth `w=572143/8000000`, the signed coordinate dynamics and interval-support radius map are

```math
\begin{bmatrix}p^+\\q^+\end{bmatrix}
=\begin{bmatrix}6/5&-1/5\\1/5&4/5\end{bmatrix}
\begin{bmatrix}p\\q\end{bmatrix}+\text{center translations},
```

```math
\begin{bmatrix}r_p^+\\r_q^+\end{bmatrix}
=\begin{bmatrix}6/5&1/5\\1/5&4/5\end{bmatrix}
\begin{bmatrix}r_p\\r_q\end{bmatrix}
+\begin{bmatrix}0\\\kappa w\end{bmatrix}.
```

A successful position packet outer-approximates the posterior with `r_p=nu=1/50` and unchanged `r_q`. For the maximum gap `N=15`, the exact radius power satisfies

```math
(M^{15})_{qq}=\frac{187604137722}{30517578125}>1.
```

Thus `r_q(15)-R` has positive contributions from `R`, `nu`, and disturbance for every `R>=0`; no finite nonnegative fixed return radius exists for this fixed-orientation parallelogram outer recurrence.

## Evidence and failure boundaries

The checker independently derives the transform, checks all legal return lengths, and archives all fractions. The evidence level is `exact_fixed_slant_parallelogram_shape_obstruction`. It rejects only this fixed-orientation `(p,q)` parallelogram outer recurrence, not a six-facet template retaining active velocity facets, rotating/mode-dependent facets, CZs, centers/controls, or recursive feasibility.
