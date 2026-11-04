# Run303 — common-causal one-step startup feasibility gate (2026-11-04 UTC)

**Scope:** abstract 1D projection of six-state [p;v] translational outer loop; NOT PX4/SITL or a quadrotor hard-safety certificate. Continues Run302's unbounded-initial-velocity counterexample. Main baseline SHA: `8486cac146ddabbc30caf6cc2365831167acfed8`.

## Claim and quantifiers

For every initial state `(p0,v0) in [-P,P] x [-V,V]` and every `w0 in [-A,A]`, find **one common command** `u0 in [-U,U]`, measurable with respect to the same received observation history, such that `|p1|<=Xp`, `|v1|<=Xv`. Assume exact discrete double-integrator with `T>0`, `p1=p0+T v0+(T²/2)(u0+w0)`, `v1=v0+T(u0+w0)`; boxes centered at zero, nonnegative radii, and no additional constraints.

Exact robust one-step conditions for a **fixed** command are

`|T² u0/2| + P + T V + T² A/2 <= Xp` and
`|T u0| + V + T A <= Xv`, with `|u0|<=U`.

Necessity follows by choosing box vertices whose signs align with the commanded offset; sufficiency follows from the triangle inequality and attainability of interval endpoints. For symmetric centered boxes, a feasible common command exists **iff**

`P+T V+T² A/2 <= Xp` AND `V+T A <= Xv`.

Indeed, `u0=0` is feasible whenever these hold; a nonzero common command cannot reduce the worst-case radius of a symmetric initial information set. The exact feasible common command interval is the intersection of `[-U,U]`, `[-2(Xp-P-TV-T²A/2)/T², +2(Xp-P-TV-T²A/2)/T²]` and `[-(Xv-V-TA)/T, +(Xv-V-TA)/T]`, with the understanding that negative radius makes the intersection empty.

**Important:** this is a one-step robust safety feasibility test, not a terminal-set, viability, MPC horizon, observer, or recursive feasibility theorem. A state-dependent command selected separately for hidden initial velocities is prohibited. Non-centered posterior sets, additional physical coupling, nonzero reference and delayed measurements require new calculations. A one-step infeasible symmetric information set cannot be rescued by later Equalized Recovery without a separately certified safe startup mechanism.

## Reproducible exact test

`python experiments/run303_startup_one_step_gate.py` (Python standard library, fractions.Fraction; no seed or solver). Frozen: `T=1/10,P=1/5,A=1/2,Xp=1/4,Xv=1,U=2`; vary `V in {1/10,2/5,1}`. Enumerate all 8 box vertices for each feasible case and check exact rational constraints. Expected common feasible command intervals: `[-2,2]`, `[-3/2,3/2]`, `empty`; zero assertion failures. This verifies the implemented arithmetic at those parameter choices, not the universal theorem (proved above).

## Relation to research gates

Gate T3 (delayed CZ/SMF Equalized Recovery) remains open; the startup information gate is logically prior to any claimed all-time hard safety. Next single obligation: lift the exact common-input robust predecessor from 1D symmetric boxes to 6D coupled position/velocity initial CZ information sets, and check whether any common input exists with input/state tightening, before attempting terminal shift arguments.

No new paper was read in this increment; this is an independent derivation, not a theorem attributed to Scott, Rego, or Hassaan. The full abstract end-to-end MPC+SMF closed loop is not implemented.
