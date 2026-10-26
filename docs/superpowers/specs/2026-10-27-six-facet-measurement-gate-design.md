# Six-Facet Measurement Gate Design

## Intent

Replace Run185's under-expressive fixed `(p,q)` parallelogram gate with an exact geometry interface that retains `+/-p`, `+/-v`, and `+/-(p-kappa*v)`. The result decides whether position measurement can tighten slant support through the retained velocity facets before any full graph/meta LP is built.

## Goals

- derive the cyclic six-facet matrix `Y`, all adjacent-pair vertex maps `Lambda`, and the exact configuration cone `G`;
- verify `P(Y,y)=conv(Lambda_i y)` throughout the cone on exact rational witnesses;
- derive the exact canonical supports after intersecting a centrally symmetric six-facet set with `|p|<=a`;
- exhibit an exact witness where the raw measurement offsets leave the six-facet configuration cone but canonical support tightening strictly reduces the slant offset;
- keep evidence flags below information-ensemble, controller, terminal, and six-state guarantees.

## Non-goals

- no `Z/H/Omega` meta-template or 15-mode/17-edge invariant LP;
- no center/recentering or input-feasibility certificate;
- no claim that adding facets is novel or that one local support reduction lowers closed-loop conservatism.

## Approaches considered

1. **Directly extend Run184's full LP.** Rejected for this round because an incorrect configuration or measurement branch would be difficult to isolate inside the large model.
2. **Reuse Run185's `(p,q)` recurrence.** Rejected because it discards the velocity facets whose effect is the question under test.
3. **Geometry-first exact gate (selected).** Build and test `Y/G/Lambda` and the measurement support identities independently, then expose them as the sole input to a later graph/meta LP.

## Exact contract

For symmetric offsets `(r_p,r_v,r_q)` and measurement cap `a`, the intersection

```math
|p|\le a,\quad |v|\le r_v,\quad |p-\kappa v|\le r_q
```

has tight supports

```math
h_p=\min(a,r_q+\kappa r_v),\qquad
h_v=\min(r_v,(a+r_q)/\kappa),\qquad
h_q=\min(r_q,a+\kappa r_v).
```

These identities will be verified by exact vertex enumeration, not floating-point sampling. A strict `h_q<r_q` witness proves only that active velocity facets can remove Run185's local unchanged-`q` obstruction.

## Failure conditions

- any candidate vertex violates a configuration inequality;
- exact vertex enumeration disagrees with a support formula;
- the strict witness is outside the pre-measurement six-facet configuration cone;
- artifact or limitation flags drift from the stated evidence scope.
