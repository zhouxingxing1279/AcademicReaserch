# Run281 — 12-state quadrotor contract: output-feedback tube feasibility audit (2026-11-03 UTC)

## Scope and evidence level
The user has explicitly selected a **12-state six-degree-of-freedom quadrotor** as the target graduate-thesis simulation plant. This is a **new candidate contract**, not an extension of the Run278 four-state safety theorem. This run makes a mathematical interface audit; it does not claim a closed-loop solver, nonlinear robust guarantee, or new full-text paper reading. Main base: `e592dfd266e4fd08eea55903233836e4b21304f4`.

## Physical plant and allocation
Use `x=(p_I[3],v_I[3],eta=(roll,pitch,yaw)[3],omega_B[3])` and `u=(T,tau_B[3])`. On a nonsingular Euler-angle chart,
`dot p=v`, `m dot v=T R(eta)e3-mg e3+d_f`,
`dot eta=E(eta)omega_B`,
`J dot omega_B=tau_B-omega_B cross (J omega_B)+d_tau`.
The hover equilibrium is `eta=0, v=0, T=mg, tau=0`; the linear controller must use **delta T=T-mg**. A four-motor allocation `[T;tau]=Gamma f` is required and actuator feasibility must be expressed as `f_min <= Gamma^{-1}[T;tau] <= f_max` when Gamma is invertible; independent rectangular virtual-input limits alone are not sufficient. Chart restriction and allocation rank are explicit assumptions.

## Output-feedback tube: two distinct errors
Discrete deviation model on a **specified bounded flight envelope**: `x+=Ax+Bu+w`, with `w in W` containing disturbance, parameter and *certified* nonlinear discretization residual. Nominal `z+=Az+Bv`; implemented `u=v+K(hat_x-z)`. Define `e=x-z`, `eps=x-hat_x`. Then exactly for the additive model
`e+=(A+BK)e+w-BK eps`.
Thus a time-invariant outer tube `E` is valid only if an independently established uniform estimation error outer set `S` holds for every admissible measurement/miss history and
`(A+BK)E (+) W (+) (-BK S) subset E`.
If `S` depends on the current measurement history, use an information-state / switched or time-varying tube and prove its **causal shift/terminal** condition. A mere SMF posterior center does not make the standard full-state-feedback RPI proof applicable.

The actual input correction is `K(e-eps)`; therefore robust nominal tightening is
`z in X minus E`, `v in U minus K(E (+) (-S))`, with exact motor-allocation polytope `U`. Here `minus` denotes Pontryagin difference. The expression `E (+) (-S)` is a safe outer bound on correlated `(e-eps)`, possibly conservative.

## Critical impossibility/feasibility gates
1. Full 12-state local controllability and output observability depend on the **specified** C matrix, IMU/attitude/position sensor schedule and linearization. A 12-state label alone does not supply observable velocity or yaw.
2. A uniform bounded S requires bounded dropout lengths or other sufficient detectability assumptions; arbitrary loss of all informative measurements does not imply bounded estimation error.
3. For hover linearization, lateral accelerations are proportional to small roll/pitch, but vertical loss from `T cos(roll) cos(pitch)` is second order and must be bounded over the chosen envelope; no global linear safety inference.
4. A terminal RCI set must exist for the **augmented information/nominal state**, not merely a physical-state box. Run246 and Run278 four-state counterexamples remain evidence against unqualified safe templates, not proofs that the new 12-state contract is infeasible.
5. Define motor thrust limits, mass/inertia, sampling, exact measurement channels and bounded noise before computing a numerical tube. Otherwise no quantitative tube size or 20ms runtime claim is justified.

## Verification and status
Static symbolic derivation checked by substitution: `x+=A(z+e)+B[v+K((z+e-eps)-z)]+w`, subtract `z+=Az+Bv` to recover `e+=(A+BK)e+w-BK eps`. This is an **algebraic identity**, not executable integration testing or RPI certification. No code, numerical experiment, CI, or new literature full-text review is claimed. Unique paper log unchanged.

## Literature linkage (historical repository evidence; not reread in this run)
- Hu et al., ACC 2018, DOI https://doi.org/10.23919/ACC.2018.8431112 — 10-state tube MPC; does not establish this 12-state output-feedback result.
- Xue et al., IET CTA 2024, DOI https://doi.org/10.1049/cth2.12588 — cascade stochastic MPC, measured position **and velocity**; does not satisfy position-only intermittent measurement contract.
- Miladi et al., TIMC 2020, DOI https://doi.org/10.1177/0142331219865816 — 12-state output-feedback control with hidden velocities, but not CZ set-membership hard-safety proof.

## Next single priority
Freeze a **12-state sensor and actuator contract** (C, noise sets, measurement-success automaton, Gamma and thrust limits) and test linearized controllability/observability and a nonempty bounded SMF error set **before** attempting numerical RPI tube construction.
