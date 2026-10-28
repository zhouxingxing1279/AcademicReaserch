# Parameter-dependent offset endpoint counterexample — design

## Intent

Before extending the fixed 19-pair CC-RCI LP with scheduling-dependent facet
offsets, determine whether checking only the two thrust endpoints can certify
the resulting parameter-dependent family.  The deliverable is a small exact
counterexample plus an independent exact verifier, not a new RCI synthesis
algorithm and not a claim about the six-state quadrotor.

## Goals

- Freeze the arbitrary-future-scheduling quantifier: every current slice must
  map into every admissible successor slice, hence into their intersection.
- Exhibit an exact rational scalar LPV example whose endpoint conditions pass
  while an interior scheduling value violates the common-target inclusion.
- Implement an exact `Fraction`-based quadratic interval maximizer that checks
  endpoints and the stationary point when applicable.
- Archive machine-readable evidence, dependency hashes, scope limitations, and
  a reproduction command.

## Non-goals and anti-goals

- Do not synthesize parameter-dependent offsets for the 19-pair template.
- Do not treat the scalar example as evidence that PD-RCI sets are impossible.
- Do not replace exact interval verification with sampling or floating-point
  optimizer output.
- Do not claim Gate A, six-state safety, or recursive MPC feasibility.

## Frozen example

Let `p in [0,1]`, `S(p)=[-(1+p),1+p]`, and
`x+ = (1-p/2)x`, with no control or disturbance.  The future parameter may
jump arbitrarily in `[0,1]`, so the required target is
`intersection_{p+} S(p+)=[-1,1]`.  The worst positive successor magnitude is

`g(p)=(1-p/2)(1+p)=1+p/2-p^2/2`.

Both endpoints give `g(0)=g(1)=1`, but the exact stationary point `p=1/2`
gives `g(1/2)=9/8>1`.  Endpoint-only certification is therefore unsound.

## Approaches considered

1. **Endpoint-only LP.** Rejected: affine plant matrices multiplied by affine
   vertices/controls create quadratic scheduling dependence.
2. **General SDP/S-procedure synthesis.** Valid as a sufficient route and used
   by the closest literature, but too large before the certification interface
   is frozen and would not independently diagnose endpoint unsoundness.
3. **Exact scalar counterexample plus rational quadratic verifier.** Selected:
   it is minimal, independently checkable, and directly determines what any
   later 19-pair candidate verifier must inspect.

## Verification interface

The checker returns the quadratic coefficients, interval, all exact candidate
maximizers, the exact maximum, endpoint verdict, global verdict, evidence
label `COUNTEREXAMPLE`, and explicit non-claims.  Unit tests perturb the
contract, exercise concave/convex/linear quadratics, and reproduce the archived
JSON byte-for-semantics via parsed equality.

## Consequence for the next synthesis step

For a fixed candidate, each facet/vertex inequality in a scalar scheduling
parameter can be audited exactly by maximizing its rational quadratic over the
closed interval.  Joint synthesis remains non-linear because the stationary
point depends on decision coefficients; later work must use an independently
verified candidate from an SDP/polynomial relaxation or another sound global
construction, rather than relabeling endpoint checks as a proof.
