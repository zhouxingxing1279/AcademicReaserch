# Scalar scheduling interval exact-SDP contract — design

## Intent

Choose a sound convex synthesis contract for the fixed-active-set 19-pair
affine-offset candidate before installing any numerical SDP solver.  The
deliverable isolates the only new algebraic difficulty exposed by Run196:
each vertex/facet residual is quadratic in the one measured thrust parameter.

## Goals

- Normalize the thrust interval to `s in [-1,1]`.
- Derive an exact `2 x 2` PSD representation for one scalar quadratic being
  nonnegative on the complete interval.
- Freeze a sound 19-pair synthesis template: affine offsets and vertex torques,
  endpoint-exact affine constraints, a conservative common-successor core,
  and one exact interval LMI per vertex/facet residual.
- Implement a pure-`Fraction` checker for a proposed scalar S-lemma
  certificate and bind the archived result to its direct dependencies.
- Preserve Run196's exact full-interval maximizer as the independent verifier
  for every numerical candidate returned later.

## Non-goals and anti-goals

- Do not install or run an SDP solver in this increment.
- Do not claim that the fixed 19-pair configuration cone is feasible.
- Do not call the whole synthesis exact: fixed normals/configuration and the
  common-core target remain conservative choices.
- Do not infer six-state safety, output-feedback containment, or recursive MPC
  feasibility from this four-state local contract.

## Exact scalar interval representation

For `f(s)=a*s^2+b*s+c`, the condition `f(s)>=0` for every `s in [-1,1]`
is equivalent, by the S-lemma with the strict point `s=0` for
`1-s^2>=0`, to existence of `lambda>=0` such that

`Q=[[c-lambda,b/2],[b/2,a+lambda]]` is positive semidefinite.

Equivalently,

`f(s)=[1,s] Q [1,s]^T + lambda*(1-s^2)`.

All entries are affine in `(a,b,c,lambda)`, so this is a convex LMI.  For a
candidate with rational coefficients and multiplier, PSD and the coefficient
identity can be checked exactly using principal minors.

## Sound 19-pair synthesis template

Inside the audited fixed configuration cone, let each symmetric pair radius
and each vertex torque be affine in normalized thrust `s`.  Configuration,
state, and input constraints are affine in `s`, hence endpoint checks are
exact.  Each invariance residual combines affine dynamics, affine vertices,
affine torque, and affine disturbance support, hence is quadratic in `s` and
uses the exact LMI above.

Arbitrary future thrust requires the successor to lie in every future slice.
Introduce a common-core offset `r` constrained below both endpoint offsets.
Mapping into `{x:Cx<=r}` is sound but may be conservative.  It strictly
contains the parameter-independent candidate class by setting all slopes to
zero and `r` equal to the fixed offsets.

## Approaches considered

1. **Reuse the multi-constraint S-procedure from the nearest PD-RCI paper.**
   Sound but needlessly conservative for a single interval and does not exploit
   the exact one-constraint S-lemma.
2. **Use endpoint constraints plus Run196 verification.** Rejected for
   synthesis: verification can reject an unsound candidate but endpoint
   constraints do not prevent the solver from returning one.
3. **Use one exact interval LMI per quadratic residual, then independently
   maximize every returned rationalized residual.** Selected.  It is convex,
   exact for the scalar interval subproblem, and retains an independent final
   audit rather than trusting solver status.

## Evidence boundary

The algebraic equivalence is `DERIVED` from the classical S-lemma under the
nonempty interval/Slater condition.  The 19-pair formulation is
`CONDITIONAL`: it is sound only under the frozen affine plant/support contract,
fixed active sets, and exact satisfaction of all LMIs.  Numerical feasibility,
Gate A, and the six-state embedding remain `OPEN`.
