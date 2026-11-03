# Background run 2026-11-03 — Patel Chapter 7 hybrid ZSM-KF + MPC audit

## Repository and checkpoint audit

- Repository: zhouxingxing1279/AcademicReaserch.
- Latest main at start of this run: 0601ab7e571c200543a43fcc60651380dda94705; research branch at start: b232e04187c6d7c106fc92d1c640e71fbb169882.
- Existing PR #176 is open, base main, mergeable=true, with 7 commits and 4 changed files. Existing PR #158 is also open and modifies the same unique paper ledger/model evidence matrix with a separate Ru/Subbarao actuator-prediction audit. Both shared-file changes were reviewed as separate, non-duplicated research increments; neither is merged blindly.
- Read the branch's latest prior log `background_run_20261103_1510_smf_zonotope_quadrotor_audit.md`, the unique paper ledger and model matrix, and current `docs/research/CURRENT_CHECKPOINT.md`. The checkpoint still carries Run278 provenance and an older embedded main SHA; the live main above is authoritative. This independent literature task does not overwrite the controller task's checkpoint.
- Main was re-read before editing the unique paper ledger; the live main SHA was unchanged at the time of the updates.

## Single research question

Does Patel & Subbarao (AIAA SciTech 2026) Chapter 7 provide a reusable hybrid zonotopic SMF-KF + robust MPC design for partial/intermittent position measurements, and what is actually transferred to the quadrotor thesis?

## Sources and reading grades

**本轮实际核验3个研究来源**：1篇新增原始AIAA论文全文经学位论文重印本核验；1篇既有直接四旋翼论文全文关键章节复核；1篇既有四旋翼论文部分章节复核；0篇仅摘要核验。

1. **New primary paper, full text via dissertation reprint**: Jinaykumar Patel and Kamesh Subbarao, “Robust 6-DOF State Estimation for Spacecraft Proximity Operations Using Zonotopic Set Membership based Kalman Filtering,” AIAA SCITECH 2026 Forum, vol. 48, no. 1, paper 0111, DOI https://doi.org/10.2514/6.2026-0111. Read the complete reprinted Chapter 7, pp.141–168, §§7.1–7.6, in Patel's May 2026 UTA dissertation, DOI https://doi.org/10.13140/RG.2.2.27141.51681. The chapter explicitly states that it is reprinted with permission from the AIAA paper. The independent AIAA proceedings PDF was not separately acquired; grade is “full text verified through dissertation reprint,” not “independent proceedings PDF read.”
2. **Existing direct quadrotor primary paper, targeted full-text re-check**: Tianchen Ji, Junyi Geng, Katherine Driggs-Campbell, “Robust Output Feedback MPC with Reduced Conservatism under Ellipsoidal Uncertainty,” 2022 IEEE CDC, DOI https://doi.org/10.1109/CDC51059.2022.9992704, arXiv https://arxiv.org/abs/2008.04980. Rechecked the full 8-page PDF's estimator recursion, robust constraint tightening, Theorem 1 and quadrotor example. This DOI already exists in the unique ledger and is not duplicated.
3. **Existing direct quadrotor primary paper, targeted section re-check**: Anilkumar Parsi, Andrea Iannelli, Roy S. Smith, “Scalable tube model predictive control of uncertain linear systems using ellipsoidal sets,” IJRNLC 35(7), 2499–2520 (2025 issue), DOI https://doi.org/10.1002/rnc.6485. Rechecked §§5.1–5.2 and data availability statement; existing DOI entry is corrected below, not duplicated.
4. No abstract-only source was counted in this run. Patel Chapter 6 (2025) and Chapter 8.3 (quadrotor reachable-set MPC) remain separate dissertation chapters and are not merged with Chapter 7's estimator or theorem claims.

## Patel Chapter 7 — verified model and filter

### Plant and input

- 13 coordinate states: LVLH relative position (3), relative velocity (3), quaternion (4), relative angular velocity (3). Six physical degrees of freedom; quaternion coordinates add one state relative to a minimal attitude parameterization.
- Translational subsystem: time-varying Tschauner–Hempel relative-orbit dynamics. Rotational subsystem: quaternion kinematics and relative angular-velocity dynamics.
- The combined A and B matrices are block diagonal, A=diag(A_T,A_R), B=diag(B_T,B_R). This removes translational/attitude coupling and is not the coupled quadrotor relation where body-z thrust direction depends on attitude.
- Six virtual control channels: three LVLH translational thrust/acceleration channels plus three rotational torques. No thruster geometry/allocation, actuator dynamics, or slew-state model is given. The translational input is described as acceleration in the model text while Table 7.1 labels its bounds as force in N; this unit inconsistency must be resolved before reuse.

### Measurement model and timing

- The translational output is relative position only, with C_T=[I_3 0]; translational velocity is hidden and reconstructed by the filter/model.
- The simulated measurement-noise structure also includes quaternion and angular-velocity channels, but no physical sensor hardware mapping (camera/GPS/IMU) is specified.
- Filter update period is 0.025 s. Algorithm 6 generates a measurement each base step and performs a scheduled filter update; it has no missing-measurement/dropout branch. This is periodic multirate estimation, not intermittent measurement filtering.
- MPC update period is 0.5 s (2 Hz), prediction horizon 30 steps (15 s), control horizon 5 steps. Base propagation step is 0.025 s; simulation duration is 60 s.

### Hybrid ZSM-KF mathematics

- Dynamics and measurement functions f and g are linearized at the prior estimate. Second-order Lagrange remainders are bounded using Hessian norms over the prior zonotope, generating G_delta and G_epsilon.
- The process-side UBB zonotope combines the linearization remainder and bounded process error with generators [G_delta, G_w]; the measurement-side UBB zonotope combines [G_epsilon, G_v] through exact zonotope Minkowski-sum concatenation.
- The posterior set-valued error generator is Omega_k=[(K_k H_k-I)G_delta, (K_k H_k-I)G_w, K_k G_epsilon, K_k G_v].
- The gain minimizes a trace criterion combining the Gaussian covariance contribution P_k and the zonotope term Omega_k Omega_k^T.
- Important guarantee boundary: Omega_k bounds UBB and Taylor-remainder components. Gaussian process/measurement noise is represented in covariance P_k and is unbounded in support. Thus P_k plus Omega_k is a hybrid error metric, not a deterministic finite set guaranteed to contain the true state for every Gaussian realization. A hard-safety use would need a chosen probabilistic confidence set or a bounded-noise assumption for the Gaussian component.
- The method uses ordinary zonotopes, not constrained zonotopes.

### MPC interface and guarantees

- The TV-MPC receives the state estimate xhat as its prediction initial condition. Algorithm 6 does not feed Omega_k into Tube initialization, state constraint tightening or terminal-set construction.
- Table 7.1 reports force bounds ±1 N and torque bounds ±1 Nm, plus an input-rate penalty; it does not provide a hard rate constraint. The terminal design is described as a final-time velocity bound included in the cost, not a robust positively/control invariant terminal set.
- No recursive-feasibility or asymptotic-stability theorem was found in Chapter 7; the chapter explicitly does not claim asymptotic stability.
- Quaternion normalization is performed after propagation and correction; no explicit unit-quaternion hard constraint along the MPC prediction horizon is described.
- Validation is simulation only: 50 Monte Carlo runs, no HIL or flight. Average RMSE: position 0.0763 m (EKF 0.0764 m), velocity 0.0478 m/s (0.0559 m/s), attitude 0.1268 deg (0.1268 deg), angular velocity 0.0013 rad/s (0.0068 rad/s). The main benefit is rotational angular-velocity estimation; translational dynamics are linear Tschauner–Hempel and perform almost identically under EKF.
- Average filter update time is 0.56 ms versus 0.49 ms for EKF. No hardware, WCET/percentiles or MPC solve time are reported. The 0.56 ms value is not a closed-loop MPC runtime or proof of a 20 ms deadline.

## Cross-paper synthesis

- **Ji et al. 2022** already establish a direct 12-state quadrotor ellipsoidal SMF + robust output-feedback Tube MPC precedent. The paper's quadrotor example uses 4 virtual wrench inputs [delta-T, Mx, My, Mz], C=I12 (all states measured with bounded output noise), dt=0.2 s and N=15. Its set-membership estimation error E and control error S are propagated separately; constraint tightening is explicit. Theorem 1 gives recursive feasibility, original constraint satisfaction, exponential stability of the nominal state and convergence of the real state to S_infinity, under Assumption 1 and initial feasibility. It is simulation, not real flight; it does not cover position-only intermittent sensing, physical four-rotor mapping or motor dynamics.
- **Parsi et al. 2025** establish 12-state, four-independent-rotor-thrust ellipsoidal Tube MPC with recursive-feasibility/robust-stability theory, but assume state measurements and do not implement an observer.
- **Patel & Subbarao 2026 Chapter 7** contribute a hybrid nonlinear filter that accounts for bounded Taylor remainders and UBB errors in gain selection, but the zonotope is not propagated into the MPC's robust constraints. It is spacecraft, uses decoupled block dynamics, and has no dropout model or hard terminal theorem.
- The defensible research gap is not “first SMF + MPC” or “first quadrotor state-SMF + MPC.” It is the combined requirement: partial/intermittent position measurements, bounded state posterior, posterior-to-tube inclusion, common causal input over the entire information set, physical rotor allocation and actuator amplitude/rate limits, and hard terminal RCI/recursive feasibility.

## Model selection impact

No model ranking change. The 12-state nonlinear six-DOF quadrotor remains the high-fidelity simulation plant; the six-state planar (T,tau) model remains the conditional robust-proof candidate; four-state remains a finite-safety mathematical baseline; two-state remains an inner-loop/height fallback. Patel's 13-state spacecraft model is not a substitute for a coupled quadrotor model. Gate A remains blocked.

## Repository updates and Parsi correction

- Updated the unique paper ledger with Patel & Subbarao's AIAA 2026 paper, explicitly marking the full-text route as a dissertation reprint; expanded the existing Patel dissertation source entry to record the Chapter 7 reading scope.
- Corrected the Parsi runtime note: §5.1 explicitly reports YALMIP + MOSEK on an Intel i7-8550 1.8 GHz laptop for the mass-spring-damper example. §5.2 reports quadrotor ETMPC/PTMPC averages of 0.16/0.04 s but does not restate whether the same hardware/solver applies; do not attribute the quadrotor timing unconditionally.
- The Parsi supplementary DOI 10.3929/ethz-b-000559871 remains inaccessible. The accessible ETH bitstream was the article PDF copy, not the supplementary package. No supplement download, code inspection or code execution is claimed.
- No controller, validation script, plant code or experiment result was changed. No simulation, HIL or flight experiment was run.

## Next single priority

Determine exactly what deterministic posterior inclusion guarantee the Chapter 7 Omega zonotope provides, then compare it with Ji et al.'s E/S recursion: under scheduled or missed position updates, how can the UBB set component initialize a Tube and tighten constraints while treating the Gaussian component separately, without using future unknown measurements?

