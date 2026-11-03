# 57 Horizontal-attitude Cartesian-product obstruction

Date: 2026-09-27. Base: `6933dd56378e9f61df85b296fca3ec1fb0ccff2b`.

## Question and result

Run 90 certified the vertical terminal mRPI and Chapter 05 certified the attitude-error RPI. This run checks whether they can be completed by any bounded horizontal factor while the attitude terminal policy is independently held at zero.

**No.** This is a policy/coupling obstruction, not a claim that no coupled six-state terminal set exists.

Use the repository reduced model
[
p_x^+=p_x+h v_x,qquad v_x^+=v_x-h(T/m)sinphi+h d_x,
]
with (h=1/50), (|d_x|le47/25). Choose the legal world
[
phi=omega=psi=ho=0,quad T=mg,quad mu=	au=0,quad d_z=0,quad d_x=47/25.
]
Zero attitude/error belongs to the Chapter-05 RPI and zero vertical error belongs to the Run-90 mRPI. Since (sin0=0),
[
v_x^+=v_x+47/1250.
]

## Proposition

For any nonempty bounded horizontal factor (X_x), a product (X_x	imes S_z	imes K_{m fin}) cannot be RPI under a terminal backup policy that keeps attitude/reference independently at zero and does not tilt in response to horizontal state/disturbance.

Proof: with constant admissible (d_x=47/25),
[
v_{x,k}=v_{x,0}+k,47/1250,
]
which is unbounded. Hence no bounded (X_x) contains all successors. The conclusion is independent of vertical feedback and thrust magnitude because horizontal thrust is zero at (phi=0). QED.

This does **not** rule out Cartesian set geometry under a coupled policy that moves the attitude reference from horizontal state; that policy must certify horizontal and reference dynamics jointly.

## Exact finite witness

From (p_x=v_x=0), exact rational arithmetic gives
[
v_{x,80}=376/125=3.008>3,qquad
p_{x,80}=14852/6250=2.37632<5.
]
Thus the demonstrated first task-domain violation is horizontal velocity, not position, attitude, vertical state, torque, or thrust saturation.

## Literature boundary

Santos and Lagoa, *Wayset-based guidance of multirotor aerial vehicles using robust tube-based model predictive control*, ISA Transactions 128 (2022), DOI 10.1016/j.isatra.2021.12.002, uses a hierarchical reduced-order translation model while assuming stabilizing lower-level position/attitude loops and time-scale separation. That assumption cannot be silently imported into the present proof because our model retains horizontal acceleration through attitude.

Hu, Feng, Quirynen, Villanueva, Houska, *Real-time tube MPC applied to a 10-state quadrotor model*, ACC 2018, pp. 3135–3140, treats a higher-order coupled quadrotor tube-MPC model. Neither paper is claimed to contain the proposition above.

## Status

Proved: independent zero-attitude terminal backup plus any bounded horizontal factor cannot close the six-state robust terminal product under the current nonzero horizontal disturbance contract.

Retained: Chapter-05 attitude-error RPI; Run-90 vertical mRPI state/input admissibility.

Not proved: nonexistence of a coupled horizontal-attitude terminal set; full six-state recursive feasibility; any guarantee for the full nonlinear 6-DoF vehicle.

Reproduce:
```bash
python verification/check_horizontal_attitude_product_obstruction.py
```

## Next unique priority

Construct the smallest coupled horizontal-reference-attitude terminal model. Include (c=(psi,ho)), use a causal horizontal feedback that generates admissible (mu), retain (e=(phi-psi,omega-ho)in K_{m fin}), and certify an RPI/RCI set for the coupled horizontal/reference subsystem under (d_x). The first gate is whether required reference actions remain inside the Chapter-05 braking kernel and (|mu|le0.0672).
