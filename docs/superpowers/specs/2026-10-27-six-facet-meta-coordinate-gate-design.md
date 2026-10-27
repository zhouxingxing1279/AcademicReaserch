# Six-Facet Meta-Coordinate Gate Design

## Intent

Determine whether replacing six facet offsets by center/radius coordinates can reduce the fixed
meta-template budget without losing measurement posteriors. Preserve an exact stopping result before
constructing another graph LP.

## Approaches

1. **Direct six offsets (selected):** preserves every configured six-facet set and provides the reference
   representation for later `H/Omega` enumeration.
2. **Five center/radius coordinates (rejected):** cheaper only by imposing zero skew, hence must be tested
   for closure under the actual position measurement.
3. **Six center/radius/skew coordinates (comparison):** exact and interpretable, but an invertible linear
   reparameterization of direct offsets; it has no automatic extreme-set budget advantage.

## Exact contract

For `kappa=1/10`, map offsets `y=(y0,...,y5)` to

```text
c_p=(y0-y3)/2, c_v=(y1-y4)/2, c_q=(y5-y2)/2,
r_p=(y0+y3)/2, r_v=(y1+y4)/2, r_q=(y2+y5)/2.
```

The map is invertible. Define `delta=c_q-c_p+kappa*c_v`. The five-coordinate family is the slice
`delta=0`. Starting from `y=(3/200,...,3/200)`, intersect with the actual-noise strip of halfwidth
`a=1/50` and center `eta=-23/4000`. The lower strip facet is inactive and the upper facet changes only
`y0`, giving canonical posterior

```text
y+=(57/4000,3/200,3/200,3/200,3/200,3/200).
```

It remains strictly inside the Run186 configuration cone with all six facets active, but has
`delta=3/8000`. Thus the five-coordinate slice is not measurement closed.

For any fixed parameter polytope `Q={y | A y<=b}` and invertible coordinate map `w=S y`, the transformed
polytope is `{w | A S^{-1}w<=b}` and its vertices are exactly `S vert(Q)`. Therefore an exact coordinate
change preserves the number of `Omega` maps/extreme candidates; a smaller budget requires a different
outer approximation, not notation.

## Evidence boundary

Success yields `exact_six_facet_meta_coordinate_nonclosure_certificate`. It does not construct a useful
bounded meta polytope, exact `H/Omega`, graph invariance, controls, terminal ingredients, recursive
feasibility, or a six-state guarantee.
