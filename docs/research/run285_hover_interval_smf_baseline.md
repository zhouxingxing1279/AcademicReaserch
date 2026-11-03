# Run285 — 12-state ZOH interval-SMF executable baseline

Date: 2026-11-03 UTC. Base main: `9375b7d32de20233574e602ba762d889eeab8d98`.

## Research question
Can a concrete conservative 12-state interval estimator be implemented with a physically recognizable hover linearization, sparse position+yaw observations and bounded disturbances, without misrepresenting a toy filter as a robust Tube MPC?

## Executable increment
`experiments/run285_hover_interval_smf.py` uses state order `(p_xyz,v_xyz,roll,pitch,yaw,omega_xyz)` and virtual inputs `(delta T/m,tau_x/Jx,tau_y/Jy,tau_z/Jz)`. Hover continuous-time small-angle couplings: `vx_dot=g*pitch`, `vy_dot=-g*roll`, `vz_dot=delta T/m`; `eta_dot=omega`. Matrix-exponential ZOH at 20ms constructs `Ad,Bd`. A 12-step observability stack with position alone has rank 10; position+yaw rank 12. These are **local linear structural properties**, not a nonlinear observability or intermittent boundedness proof.

State sets are axis-aligned boxes `[c-r,c+r]`. Prediction `c'=Ad*c+Bd*u`, `r'=abs(Ad)*r+w_radius` is a sound box enclosure of the linear image plus bounded box disturbances. On successful coordinate observation, intersect each measured coordinate interval with `[y-v_radius,y+v_radius]`; on miss, leave the prediction. Correlations are discarded, so the filter is conservative, not an exact zonotope/CZ or full posterior intersection. An empty interval raises an error instead of silently resetting the filter.

## Reproduction and observed output
Python with NumPy and SciPy:
```bash
python experiments/run285_hover_interval_smf.py
```
Locally executed equivalent script (2026-11-03 UTC):
```
position-only rank 10 position+yaw rank 12
300-step containment PASS; max x-width 5.284954 final x-width 0.02
final yaw-width 0.016
not a bound on all legal disturbances: Monte Carlo only
```
One seeded 300-step synthetic trajectory, 20ms steps, position+yaw packets every 5 steps with every third opportunity missed (never more than one consecutive missed opportunity), bounded synthetic disturbances/noise, and known virtual control. The 5.285m **intermediate position interval width** despite 0.02m final width illustrates that occasional narrow measurement strips do not prevent severe between-update conservatism when coordinate correlations are discarded. It is not a measured tracking error or hard-constraint violation.

## Critical limitations
- Synthetic bounds are not calibrated to a physical vehicle; no actuator allocation, motor dynamics, nonlinear model mismatch or validated thrust uncertainty.
- The position+yaw measurement packet and deterministic miss schedule are chosen for a demonstration; the real sensor suite and allowable miss automaton remain unverified.
- Numerical containment checks for one seeded realization are **not** an exhaustive proof; soundness of interval prediction/intersection follows from set algebra if all assumptions hold.
- No optimizer, tube, terminal set, closed-loop plant feedback, feasibility, hardware timing/WCET or safety proof. Gate A remains **blocked**.
- Repository main contains older four-state Euler research with different dynamics; do not transfer its counterexamples to this 12-state model without a reduction proof.
- No new paper was read during this increment; unique paper ledger remains unchanged.

## Next single priority
Replace synthetic `W,V` and the measurement schedule with a justified actuator/sensor and legal-loss contract, then test whether a more expressive zonotope/CZ enclosure reduces between-update position width while maintaining certified inclusion. Do not proceed to a hard-safe Tube MPC claim until this interface is closed.
