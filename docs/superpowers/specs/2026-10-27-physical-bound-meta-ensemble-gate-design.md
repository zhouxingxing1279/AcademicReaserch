# Physical-Bound Meta-Ensemble Gate Design

## Intent

Test the Run188 next-step proposal at its weakest sufficient point: does bounding the six direct offsets only through the certified physical tracking-error box produce a useful multi-extreme information ensemble?

## Approaches

1. **Physical containment only (selected for audit):** define the parameter domain by the Run186 configuration cone and require every configured vertex to lie in the Run183 error box. It is exact and uses no invented tuning bounds.
2. **Independent coordinate caps:** add arbitrary lower/upper bounds on six offsets. Rejected this round because their values are not fixed by the physical contract and would predetermine the extreme-set budget.
3. **Mode/history-conditioned shape constraints:** potentially preserves multiple incomparable maximal polytopes, but belongs to the next design problem after the physical-only baseline is audited.

## Exact claim

Let `X=[-1,1] x [-11/4,11/4]`, let `P(y)={x:Yx<=y}` use the configured six normals, and let `Q_X` contain every configured `y` with `P(y) subseteq X`. The tight support vector of `X` is

`y_X=(1,11/4,51/40,1,11/4,51/40)`.

For every `y in Q_X`, tightness of the configured facets gives `y_i=h_{P(y)}(Y_i)<=h_X(Y_i)=(y_X)_i`; and `P(y_X)=X`. Therefore every member of the induced ensemble lies in `P(y_X)`, so its extreme-set boundary is the singleton `{X}`. Physical containment makes the parameter domain bounded but removes all intrinsic information discrimination.

## Evidence boundary

The certificate is `exact_physical_bound_meta_ensemble_singleton_extreme_set`. It rejects only the physical-containment-only meta domain. It does not reject direct offsets with additional information-conditioned constraints, CZ ensembles, or existence of an invariant output-feedback controller.
