# Finite-memory CZ and output-feedback tube experiment

Registered 2026-11-04 before simulation. Candidate mathematical model only; no physical calibration or PX4 guarantee.

ZOH double integrator: T=0.5, process acceleration radius 0.02, position noise radius 0.005, maximum missing generation M=1, maximum delivery delay L=1. Independent axes, initial radii (0.005,0.01), state limits (3,2), input limit 4, horizon 12. Compare finite-memory CZ, pair-only zonotope, and a full-history CZ on identical information. Keep infeasible cases. Explore M,L=0..3 without changing the main case.

Proof obligations: all-event finite-memory containment; uniform estimation bound including startup; causal common command; invariant tracking tube; nonempty terminal set; nominal shift feasibility. Float LP/QP results are numerical evidence, not directed-rounding certificates. Exact rational checks separately verify the deadbeat identities, tube margins, and Lyapunov identity.

Closed-loop cases: periodic maximum loss/delay; out-of-order arrival; random legal schedules with seeds 0..9; constant and alternating endpoint disturbances/noise. Illegal timestamp, conflicting duplicate, no second timestamp, out-of-contract noise, too-tight input, and nominal-reset counterexamples must be reported separately. Metrics: state and input violations, CZ containment residuals, estimation error, generator/equality counts, QP feasibility, time quantiles. Finite runs do not establish universal safety.
