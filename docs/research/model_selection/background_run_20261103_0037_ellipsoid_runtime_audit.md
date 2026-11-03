# Background run 2026-11-03 — Parsi ETMPC timing and theorem scope audit

Base main SHA: `9375b7d32de20233574e602ba762d889eeab8d98`. Topic: can 12-state four-rotor ellipsoidal Tube MPC substantiate a 20 ms output-feedback safety controller?

## Primary source
Parsi, Anilkumar; Iannelli, Andrea; Smith, Roy S., *Scalable tube model predictive control of uncertain linear systems using ellipsoidal sets*, International Journal of Robust and Nonlinear Control, **35(7), 2499–2520 (2025 issue)**; first published online **21 Nov 2022**. DOI https://doi.org/10.1002/rnc.6485 . Open publisher full text https://onlinelibrary.wiley.com/doi/10.1002/rnc.6485 . This run read publisher HTML §§2, 3.1, 3.4, 4.1, 5.2 and Appendix A.4; not a complete line-by-line reading.

## Directly verified
- Model in §5.2: 12-state hover-linearized discrete quadrotor, state [position deviation 3, velocity deviation 3, Euler angles 3, angular rates 3], **four individual rotor thrust inputs**; Ts=0.1 s, N=15; uncertain mass 27–37 g; wind bounded by assumed relative velocity; each rotor thrust in [0,0.157] N; Crazyflie simulation, not physical flight.
- Ellipsoidal state tubes and affine feedback; terminal ellipsoid and offline K,P designed with SDP/line search. Theorem guarantees are for the paper's **uncertain LTI/LFT model**, disturbance and constraint assumptions, not for arbitrary nonlinear quadrotor or intermittent output feedback. §4.1 uses regional input-to-state practical stability; Appendix A.4 terminal invariance and disturbance-free convergence.
- **Critical compute budget finding**: §5.2 explicitly reports average online ETMPC solve time **0.16 s**, PTMPC **0.04 s**. Both exceed a 20 ms target even on reported averages; no WCET or real-time feasibility evidence. ETMPC achieved feasible xy setpoint 0.68 m versus PTMPC 0.55 m; closed-loop costs 109.3 vs 121.4 at 0.55 m. These are numerical simulations under the authors' setup, not universal comparisons.
- Publisher data availability links example code https://doi.org/10.3929/ethz-b-000559871 . Reproduction remains unverified.

## Cross-paper context (prior work; NOT newly re-read in this run)
Santos & Lagoa (2022), DOI https://doi.org/10.1016/j.isatra.2021.12.002: outer-loop reduced-order navigation Tube MPC, inner-loop stabilization assumption. Elokda et al. (2021), DOI https://doi.org/10.1002/rnc.5686: DeePC outer-loop angular-rate/thrust references with independent inner loop. These do not transfer direct four-rotor constraints or output-feedback safety theorems.

## Decision and limits
Retain 12-state nonlinear plant as simulation target and 6-state physical planar model as tractable proof candidate. Do not select Parsi online SDP as 20 ms baseline without independent benchmarking and redesign; paper average 160 ms is a negative feasibility signal, not a formal impossibility. The paper's full-state initialization and state tube cannot be directly substituted for a measurement-conditioned SMF/CZ posterior. Need a mathematically sound map from posterior to initial tube and a recursively feasible information-state terminal condition. Existing main checkpoint Run278 documents finite-horizon four-state posterior ambiguity, not proof of 12-state closed-loop safety. Gate A remains blocked.

## Reading ledger and model matrix
No DOI duplicate added; this is a deepening of an already discussed paper. This run deliberately leaves shared files unchanged to avoid concurrent main edits. Evidence for future matrix: runtime ETMPC 160 ms average, PTMPC 40 ms average at 100 ms sampling, versus 20 ms research budget. No new code, tests, SMF estimator, or theorem produced.

## Next priority
Retrieve and run the author's published example code, document exact solver/hardware, benchmark time distribution and feasibility under identical 12-state constraints; then investigate a QP/polytope or reduced-order MPC that can meet 20 ms while retaining a reliable SMF/CZ interface. Separately read original polytope Tube MPC reference cited as [26] in §5.2.
