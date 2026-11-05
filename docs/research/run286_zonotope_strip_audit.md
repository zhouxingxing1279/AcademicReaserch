# Run286 — Measurement-strip zonotope outer enclosure versus interval SMF

Date: 2026-11-03 UTC. Base main: `9375b7d32de20233574e602ba762d889eeab8d98`.

## Scope and evidence
Independently inspected PR #171 (`experiments/run285_hover_interval_smf.py`), which remains unmerged as of this audit. This run uses the **same** 12-state hover ZOH matrices, synthetic disturbance/noise boxes, seeded 300-step trajectory, and position+yaw packet schedule to compare a correlation-preserving zonotope outer enclosure against Run285's axis-aligned interval enclosure. No new paper was read; do not add to the unique literature ledger. The PR #171 baseline is not yet main.

## Reliable measurement-strip outer enclosure
Represent the predicted set as `Z(c,G)={c+G ξ: ||ξ||∞<=1}`. Propagate
`c-=Ad c+Bd u`, `G-=[Ad G,diag(w_radius)]`.
For scalar measurement `y=h x+v, |v|<=vbar`, choose **any** gain vector `λ` and set
`c+=c-+λ(y-h c-)`,
`G+=[(I-λh)G-, λ vbar]`.
Proof: every consistent `x=c-+G-ξ` has `y-hx=v`, hence
`x=c+ +(I-λh)G-ξ-λv`, and is contained in the stated zonotope. This is a sound **outer enclosure**, not an exact posterior intersection. The numerical gain is `λ=(GGᵀh)/(hᵀGGᵀh+vbar²)`; this is a heuristic to reduce generator energy, not a certified minimum-width optimizer. Apply sequentially to x,y,z,yaw measurements. During packet loss, omit updates. This containment guarantee assumes initial enclosure, bounded process/measurement disturbances, and known applied virtual input; it does **not** establish bounded width or robust MPC safety.

## Executed numerical check
Executed locally in Python (NumPy/SciPy) on 2026-11-03 with Run285's seed 285 and 300 steps, using the same generated true states, controls, noise and success/miss sequence. The baseline interval prediction/coordinate-strip intersection and zonotope strip update both enclosed the generated truth at every step (300/300); **single-trajectory checks are not exhaustive verification**.

| Metric | Interval box | Unreduced zonotope |
|---|---:|---:|
| Maximum x-position bounding width over 300 steps | 5.284954 m | 0.235276 m |
| Final x-position bounding width | 0.020000 m | 0.126867 m |
| Observed truth containment failures | 0 | 0 |

The zonotope has **3,772 generators at step 300** because each prediction appends 12 process-noise generators and each successful 4-coordinate packet appends four measurement-noise generators. It preserves state correlation and sharply reduces *maximum between-update x-width* on this example, but has **larger final x-width** because the simple strip update does not intersect with the coordinate interval optimally. The unreduced generator count grows without bound in repeated runs, so this implementation is not a viable 20 ms online SMF without reduction and a proved outer-approximation budget. Do not report the width difference as a robust performance guarantee or as evidence of a safe Tube MPC.

## Reproduction recipe
Use Run285's `Ad,Bd`, initial radius, `proc`, `meas`, RNG seed 285 and `k=1..300` loop. Maintain `cz=zeros(12),G=diag(initial_radius)`; on every step update `cz=Ad@cz+Bd@u`, `G=column_stack((Ad@G,diag(proc)))`. On each successful position+yaw packet, for each observed coordinate `i`, calculate `g=G@G.T@e_i`, `λ=g/(e_i@g+meas_i**2)`, `cz=cz+λ*(y_i-cz_i)`, `G=column_stack((G-outer(λ,G[i,:]),λ[:,None]*meas_i))`. Check `abs(truth-cz)<=abs(G).sum(axis=1)+1e-8`. Run alongside the Run285 interval filter with **the same truth/noise draw**. This run's local command used an independent script, not a committed runnable artifact; full independent CI reproduction is still required.

## Decision and next priority
This supports testing correlation-preserving SMF rather than accepting the 5.285 m interval blow-up as inherent state uncertainty. It does not validate physical disturbance bounds, nonlinear model mismatch, the legal packet-loss automaton, actuator allocation, tube invariance, terminal feasibility, or any 12-state closed-loop controller. **Gate A=blocked.**

Next single priority: implement a deterministic, unit-tested generator-reduction/strip-intersection benchmark on the same synthetic trace, quantify reduction-induced outer-enclosure inflation and runtime, then replace toy bounds with documented physical/sensor contracts before MPC integration.
