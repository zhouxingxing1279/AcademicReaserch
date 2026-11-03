# Run284 — 12-state hover model: reliable SMF update and yaw observability contract

Date: 2026-11-03 UTC. Base main: `9375b7d32de20233574e602ba762d889eeab8d98`.
Status: mathematical derivation, **not** a closed-loop or numerical experiment.

## Scope and prior evidence
The Run282/283 12-state hover observability reports are available in prior task results but their proposed files were **not found on main** when queried in this run. Do not claim their scripts are merged. The existing main checkpoint mainly concerns a separate 4-state Euler benchmark; its finite-horizon and negative results do not establish 12-state infeasibility.

## System contract
For a discrete linearized hover model with a **known applied** input (after actuator allocation), assume
`x[k+1] = A_d x[k] + B_d u[k] + w[k]`, `w[k] in W`,
and at successful measurement instants
`y[k] = C x[k] + v[k]`, `v[k] in V`.
Assume initial set `X[0]` contains the true initial state, bounded W and V are valid for all times, and the reported measurement is correctly time-stamped. A known bounded allocation/model mismatch must be included in W (or modeled as an augmented state), not silently ignored.

Define `X^-_{k+1} = A_d X^+_k (+) {B_d u_k} (+) W` (Minkowski sum).
On success define `X^+_{k+1} = X^-_{k+1} intersect {x: y_{k+1}-Cx in V}`.
On miss define `X^+_{k+1}=X^-_{k+1}`. Empty intersection is a **contract violation or inconsistent data**, not a license to reset the state estimate.

**Containment proof (induction).** If `x_k in X^+_k`, known applied input and `w_k in W` imply `x_{k+1} in X^-_{k+1}`. A successful observation with `v_{k+1} in V` places the true state in the measurement strip, so it remains in the intersection. A miss makes no correction. Hence true-state inclusion holds for any measurement success/miss sequence for which the assumptions hold. This says nothing about set boundedness, nonemptiness of a robust MPC feasible region, computational tractability, or recursive feasibility.

## Structural yaw obstruction
For standard zero-yaw, hover small-angle linearization with 12-state `(p,v,phi,theta,psi,omega_x,omega_y,omega_z)`, the yaw subsystem is `dot psi=omega_z`, `dot omega_z=tau_z/J_z`, while the **linearized** position output is independent of `psi,omega_z`. With position-only `C_p=[I_3,0_{3x9}]`, the two-dimensional yaw subspace lies in the unobservable subspace. Two admissible initial states differing only in yaw/yaw rate, under identical applied inputs and matched disturbances, produce identical position measurements in this linear model. Thus no position-only SMF update can shrink uncertainty in yaw from measurement information alone. Adding direct yaw measurement removes this specific structural obstruction (full-rank observability still requires the remaining model parameters and sensor assumptions to be checked).

This statement is local to the hover linearization; nonlinear trajectories, heading-dependent drag, and different sensors may alter observability. It does not show all position-only closed-loop control is impossible.

## Exact missing contract for the next implementation
1. Freeze state ordering, mass/inertia, continuous A/B, ZOH sampling time, and numerical discretization tolerance.
2. Freeze C for position plus heading or attitude sensing; specify whether gyro measurements are included and when each sensor is available.
3. Freeze non-probabilistic initial X0, process W and sensor V with units; define a legal dropout automaton for each sensor stream, not just one aggregate flag.
4. Freeze applied-input mapping and saturation: actual actuator commands must satisfy the assumed `u_k` or allocation error must enter W.
5. Implement set propagation and measurement intersection (initially H-polytope or interval overapproximation); test deterministic inclusion for synthetic bounded disturbances and every enumerated legal dropout word over a finite horizon. A Monte Carlo pass alone is not a proof of infinite-horizon containment.
6. Report emptiness, set growth, computation time, and numerical outward-rounding strategy. Only then attempt tube tightening and a terminal information-state invariant family.

## Literature relationship
The existing ledger cites Qiu et al., *Output feedback model predictive control based on set-membership state estimation* (2020), DOI 10.1049/iet-cta.2019.0881, and Yan/Cannon/Goulart (2022), DOI 10.1016/j.automatica.2022.110282. No new paper was read in this run; these are background references, not evidence that the proposed 12-state SMF or Tube MPC has been implemented.

## Status
Mathematical set-containment interface documented. No new source code, executed test, SMF numerical instance, MPC solve, RPI certificate, recursive-feasibility proof, nonlinear flight simulation, or WCET. **Gate A remains blocked.**
Next priority: implement an executable 12-state ZOH plus bounded-set SMF measurement update using explicit yaw measurement and enumerated legal packet patterns; validate against the current main before integration.
