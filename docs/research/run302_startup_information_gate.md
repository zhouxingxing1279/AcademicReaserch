# Run302 — Initial information gate before two-timestamp recovery (2026-11-04)

## Claim and quantifiers
Consider one axis of the six-state position/velocity abstraction, with exact sampled double-integrator dynamics p_{k+1}=p_k+Tv_k+(T²/2)(u_k+w_k), v_{k+1}=v_k+T(u_k+w_k), T>0, known applied u, bounded w, and position-only y_k=p_k+nu_k. Assume at startup only y_0 is received and no finite prior bound on v_0 is specified.

**Counterexample (proved):** For every finite candidate one-step position uncertainty radius R, there exist two initial states consistent with the same y_0 and the same causal u_0, with their next positions separated by more than 2R. Take p_0=0, nu_0=w_0=u_0=0 and v_0=+M versus -M; their observations coincide and |p_1^+-p_1^-|=2TM. Choose M>R/T. Consequently neither a bounded startup posterior nor an unconditional all-time hard-state constraint follows from a later two-timestamp recovery lemma.

The two trajectories have identical received histories, hence a causal output-feedback controller must issue the same u_0. The counterexample does not assert that every bounded-velocity plant is unsafe: a physically justified finite initial set X_0 or a pre-control measurement acquisition/recovery phase may close the initialization gap.

## Required gate for MPC
Choose and explicitly certify one of: (i) bounded initial position/velocity set X_0 and X_0 subset the estimator's initial posterior, with initial robust MPC feasibility; or (ii) a separate safe acquisition policy and invariant admissible region until two distinct timestamped position observations have arrived, followed by a certified transfer into the MPC feasible set. The Run300/301 eventual two-sample guarantee alone does not provide (ii). A safe acquisition policy cannot be presumed from the two-sample theorem.

## Reproduction and evidence
Command: python experiments/run302_startup_counterexample.py. Python standard library only, no random seed. T=1/10, M in {1,10,100,1000}. Expected next-position diameters 0.2, 2, 20, 200. Exact Fraction arithmetic checks equality; finite examples illustrate, while unboundedness is established by the symbolic quantifier proof. No controller, CZ posterior, full automaton, SITL or hard-safety certificate was tested.

## Literature status
This is a direct elementary construction, not attributed to Scott, Rego, Hassaan or other papers. Existing literature log is unchanged; no new full-text reading is claimed. Applies to the abstract double-integrator model, not yet to a specific quadrotor autopilot.

## Proof status and next task
Startup impossibility without an initial velocity bound: **proved** for this abstraction. Eventual finite-window velocity recovery: conditional on earlier measurement-generation/delivery assumptions. Uniform all-time Equalized Recovery, safe acquisition, terminal invariance and recursive MPC feasibility: **unproved**.

**Only next priority:** specify a finite initial information set X_0 and prove (or refute) nonempty robust initialization/transfer into the first output-feedback Tube MPC feasible set, before using eventual recovery as an all-time guarantee.
