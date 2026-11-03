# Run282 — 12-state hover output observability: a structural gate (2026-11-03 UTC)

## Scope and evidence level
This is a **symbolic structural calculation**, not a numerical simulation, set-membership filter, or recursive-feasibility proof. Base main: `e592dfd266e4fd08eea55903233836e4b21304f4`. Run281's 12-state draft is currently PR #161, **not in main**; this note independently tests an assumption required before promoting that draft.

## Continuous-time hover model
Use inertial coordinates, small roll/pitch, hover yaw zero, known positive mass `m`, gravity `g>0`, positive principal inertias, and no actuator dynamics. Order states
`x=(p_x,p_y,p_z,v_x,v_y,v_z,phi,theta,psi,p,q,r)`.
Control perturbations `u=(delta T,tau_phi,tau_theta,tau_psi)`, with `delta T=T-mg`. At the nominal hover,
`p_dot=v`,
`v_x_dot=g theta`, `v_y_dot=-g phi`, `v_z_dot=delta T/m`,
`phi_dot=p`, `theta_dot=q`, `psi_dot=r`,
`p_dot_ang=tau_phi/J_x`, `q_dot_ang=tau_theta/J_y`, `r_dot_ang=tau_psi/J_z`.
The last three rates are body angular rates (avoid confusing position `p` with roll rate `p`).

## Exact position-only observability obstruction
For output `y=(p_x,p_y,p_z)`, the linearized `A` is block diagonal between the translational/roll/pitch subsystem and the yaw chain `(psi,r)`. Its yaw columns are zero in `C`, and the yaw block does not drive any other state. Thus `C A^k e_{psi}=C A^k e_r=0` for **all** integers `k>=0`. The continuous-time observability matrix has a nullspace containing these two independent directions and rank at most **10**, regardless of sample period, finite observation horizon, or a pattern of successful position measurements. The exact same conclusion holds for `A_d=exp(A h)`, `h>0`. This is a structural, not a solver-dependent, counterexample to claiming all 12 hover states are observable from position alone.

In fact, for `g>0`, the two horizontal four-state chains `(p_x,v_x,theta,q)` and `(p_y,v_y,phi,p)` have observability ranks 4 each; the vertical position/velocity chain has rank 2. Therefore the total position-only rank is **exactly 10**. For the horizontal chain, successive output derivatives are `p_x, v_x, g theta, g q`; their coefficient matrix has nonzero determinant magnitude `g^2`. The vertical chain is rank 2. The yaw pair remains unobservable.

## Consequences for SMF/MPC design
1. An assumption that position-only measurements make the complete 12-state linear hover model observable is false. A full-state estimation-error bound cannot be justified from position observations alone without additional yaw prior bounds, bounded yaw disturbances, and a finite horizon, or another yaw sensor.
2. Position-only measurements do not imply **impossibility** of finite-horizon set containment: bounded initial yaw sets and bounded process disturbances can still propagate as valid outer sets. Infinite-horizon bounded yaw error under arbitrary bounded yaw acceleration disturbance is not guaranteed by this open-loop double-integrator yaw chain.
3. Candidate repair: explicitly add measured yaw (magnetometer, vision orientation, or equivalent) and specify noise/dropout assumptions. For `C_+=(p_x,p_y,p_z,psi)`, the yaw chain contributes rank 2; under the stated idealized hover model the combined continuous-time and uniformly sampled discrete-time pair is rank **12** for any `h>0`. This **does not** prove uniformly bounded estimation errors under arbitrary dropouts, nor nonlinear observability, nor motor feasibility.
4. A more realistic IMU rate/attitude output is another option, but its sampling, bias and bounded-error model must be explicitly stated. Do not silently equate commanded angular rate with measured angular rate.
5. Exact discretization and finite-horizon observability should be checked against the actual sensor matrix before running an SMF, then test the allowed bounded-dropout automaton. Measurement noise must be propagated as sets, not replaced by a covariance guarantee.

## Reproduction (symbolic, no external dependencies)
Let `A` have nonzero entries `A[0,3]=A[1,4]=A[2,5]=1`, `A[3,7]=g`, `A[4,6]=-g`, `A[6,9]=A[7,10]=A[8,11]=1` (zero-based). Let `C_pos` select rows 0,1,2. Form `O=stack(C A^k, k=0,...,11)`; exact symbolic rank is 10 for nonzero g. Add row selecting state 8 (yaw) to `C`: rank is 12. This is an algebraic calculation reproducible by hand; **no executable test was run in this round**.

## Research gate and next single action
Gate A remains **blocked**: physical rotor allocation, bounded disturbances, sampling/dropout contract, SMF set containment, and robust terminal information-state invariance are unproved. The immediate next action is to implement a version-pinned exact-discrete 12-state `(A_d,B_d,C)` test with two sensor configurations and permitted dropout histories, reporting rank and finite-horizon set-width growth. Do not claim the original position-only model supports 12-state observer convergence.
