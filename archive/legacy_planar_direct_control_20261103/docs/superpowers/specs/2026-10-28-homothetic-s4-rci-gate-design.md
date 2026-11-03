# Homothetic S4 RCI Gate Design

## Intent

Test whether the strongest finite Run193 template currently available can be upgraded to a genuine
RCI without changing its shape: use `alpha*S4`, measured-current-thrust endpoint vertex controls,
the frozen `W(T)`, all four state constraints, and `|tau|<=0.08`.

## Goals and non-goals

- Produce an executable, hash-bound exact witness if one `S4` vertex makes the torque interval empty
  for every `alpha>0`.
- Verify the witness belongs to the exact frozen `S4` rows and that four active rows are independent.
- Keep the conclusion limited to the homothetic `S4` template class.
- Do not claim general RCI nonexistence, six-state safety, terminal invariance, or recursive feasibility.

## Approaches considered

1. Continue the descending predecessor recursion. Rejected: another finite layer does not resolve the
   RCI proof obligation and conflicts with the current stop rule.
2. Jointly synthesize arbitrary configuration offsets and vertex inputs. Deferred: this is the correct
   strong baseline but is a larger optimization problem; first audit whether the existing shape can be
   salvaged by one scalar scale.
3. **Selected:** freeze the deterministic exact-row `S4`, derive exact torque lower/upper affine
   functions at one exact vertex and the low-thrust endpoint, and prove they are disjoint for all
   `alpha>0`.

## Evidence boundary

Run193 uses HiGHS to select the 102 nonredundant rows, so selection of the frozen template remains a
`NUMERIC_CHECK`. Once those rows are frozen, vertex membership, active-row independence, disturbance
support, and the torque-gap identity are checked with `Fraction` arithmetic. The final result is an
exact `COUNTEREXAMPLE` to that frozen candidate class, conditional on the deterministic Run193 row set.
