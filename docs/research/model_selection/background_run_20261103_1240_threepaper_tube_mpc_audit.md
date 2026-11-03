# Background run 2026-11-03 — three-paper Tube MPC architecture and runtime audit

## Repository state and checkpoint audit

- Repository: zhouxingxing1279/AcademicReaserch.
- Previous pending PR #174 was independently checked: one Markdown file, +24/-0, branch ahead 1/behind 0, GitHub mergeable=true, zero check-runs and no review. Markdown static checks found seven headings and no trailing whitespace. No code changed, so no code test applied. It was safely squash-merged with expected head SHA defa2a6a13e92dd639eab277a04a01d13a135d7b; merge commit and new main SHA: 0601ab7e571c200543a43fcc60651380dda94705.
- This run starts from that exact main SHA. Read current CURRENT_CHECKPOINT.md, unique PAPER_READING_LOG.md, MODEL_SELECTION_EVIDENCE.md, latest model-selection log background_run_20261103_1151_alexis2012_12state_switching_mpc.md, Run278 log, verification/check_run278_exact_slice.py, and configs/planar_baseline.json.
- Checkpoint content is still Run278 and its leading provenance text cites older base main db72fb6b105a635c0b6949ed276221cb20a2973b; the live main after PR #174 is 0601ab7e571c200543a43fcc60651380dda94705. Treat the checkpoint's embedded SHA as stale provenance, not as current remote state. The current model matrix still says: 12-state nonlinear 6-DOF plant is the primary simulation target per the user's thesis workload requirement; 6-state planar model remains the conditional robust-proof candidate; 4-state is a finite-safety mathematical baseline; Gate A remains blocked.

## Single research question

What can actually be transferred from direct 12-state four-rotor Tube/RAMPC papers to a 20 ms intermittent-output-feedback SMF/CZ thesis, and what is only a reduced-order inner-loop flight result?

## Papers verified this run

Three direct quadrotor MPC primary papers were cross-checked. Reading grades: **2 full-text reads (Michel 2019 and Didier 2021), 1 partial targeted full-text read (Parsi et al.); 0 abstract-only**. Didier already has a DOI record in the unique paper ledger and is not duplicated. Parsi and Michel did not have DOI entries and are appended to the unique ledger.

### 1. Parsi, Iannelli & Smith — ellipsoidal Tube MPC (partial targeted full text)

- Full citation: Anilkumar Parsi, Andrea Iannelli, Roy S. Smith, “Scalable tube model predictive control of uncertain linear systems using ellipsoidal sets,” International Journal of Robust and Nonlinear Control, 35(7), 2499–2520 (2025 issue; first published online 21 Nov 2022), DOI https://doi.org/10.1002/rnc.6485.
- Versions actually read: author PDF https://andreaian.github.io/pub/IJRNC22_RMPC.pdf and publisher full text. Read §§2, 3.1, 3.4, 4.1, 5.2 and Appendix A.4; **partial, not a full line-by-line reading**.
- Physical model: six physical DOF, 12-state hover-linearized discrete model x=[Δs, Δdot s, ψ, dotψ], position/velocity/Euler angles/Euler-angle rates; four individual rotor thrust inputs. Ts=0.1 s, N=15.
- Uncertainty and constraints: mass 27–37 g as LFT/multiplicative uncertainty; bounded wind based on assumed maximum relative velocity 2 m/s in x/y; each rotor thrust 0–0.157 N; position hypercube and angle/rate constraints. Crazyflie example is simulation only.
- Sensors/estimation: controller uses an available state measurement xhat_k; paper does not identify a physical sensor, observer, measurement-noise model or intermittent measurement process. It is not state SMF/CZ.
- Tube and proof: homothetic fixed-shape ellipsoids, online translation/scaling and affine ancillary feedback u=K(x-z)+v; offline SDP/line search for ellipsoid, gain and terminal set. Theorem 1 gives recursive feasibility and regional ISpS for the stated uncertain LTI/LFT system, bounded disturbance and constraints, provided offline design is feasible and the initial measured state is in the feasible region. Terminal ellipsoid is robust invariant under the terminal controller. Proposition 6 adds exponential convergence if disturbance eventually becomes zero. Theorem 1's state bound is acknowledged as conservative.
- Runtime: average ETMPC 0.16 s; vertex-independent polytopic PTMPC 0.04 s; sampling 0.1 s. Thus ETMPC average exceeds the sample period; PTMPC average is below the sample period but above the current 20 ms budget. These are averages, not WCET or percentiles. ETMPC handles a 0.68 m xy target where PTMPC is infeasible; at 0.55 m costs 109.3 vs 121.4. Solver and timing hardware are not explicitly identified in the quadrotor section; YALMIP/MOSEK appear in references only, so no solver/hardware attribution is made.
- Reproducibility: paper links supplementary material DOI https://doi.org/10.3929/ethz-b-000559871. Web search locates an ETH Research Collection bitstream, but attempts to open the DOI/bitstream returned 403. No download, code inspection or execution is claimed.

### 2. Didier, Parsi, Coulson & Smith — RAMPC of quadrotors (full text reread)

- Full citation: Alexandre Didier, Anilkumar Parsi, Jeremy Coulson, Roy S. Smith, “Robust Adaptive Model Predictive Control of Quadrotors,” 2021 European Control Conference, DOI https://doi.org/10.23919/ECC54610.2021.9654893; author arXiv PDF https://arxiv.org/pdf/2102.13544.
- Actual reading: complete 6-page author PDF pp.1–6 reread this run; the DOI was already registered in the unique paper ledger.
- Simulation model: 12-state hover-linearized six-DOF quadrotor with four individual rotor thrust deviations; Euler discretization Ts=0.1 s. Unknown mass inverse is a bounded parameter; scenarios include bounded wind and all-rotor efficiency loss. Direct-thrust simulation constraints include each rotor thrust 0–0.16 N, position ±0.7 m, Euler angles ±π/2. Direct-thrust RAMPC average solve time 90 ms on a 3.1 GHz Intel i5.
- Estimation: set-membership update is for unknown model parameters (mass/rotor efficiency), not hidden position/velocity state. Measurement-noise handling dilates the non-falsified parameter set. The authors also explain that recomputing steady-state thrust from the current parameter estimate improves performance but loses the corresponding strict robustness guarantee.
- Real flight: Crazyflie 27 g; IMU and Vicon (six cameras, 200 Hz) with ground laptop optimization. Direct four-rotor thrust was difficult to implement and was not flown. The actual RAMPC experiment uses only a 2-state altitude subsystem (Δp_z, Δdot p_z) and one total-thrust-deviation input; x/y/yaw use LQR and the inner loop uses PID. OSQP is reported under 5 ms for this reduced subsystem. This is not a 12-state four-motor flight demonstration.

### 3. Michel, Bertrand, Olaru, Valmorbida & Dumur — AR.Drone 2.0 Tube MPC (full text)

- Full citation: Nathan Michel, Sylvain Bertrand, Sorin Olaru, Giorgio Valmorbida, Didier Dumur, “Design and flight experiments of a Tube-Based Model Predictive Controller for the AR.Drone 2.0 quadrotor,” IFAC-PapersOnLine, 52(22), 112–117 (2019), DOI https://doi.org/10.1016/j.ifacol.2019.11.058; ONERA full PDF https://w3.onera.fr/copernic/sites/default/files/2019_ifac_workshoprobotcontrol_design_flight_tube_mpc_ardrone.pdf.
- Actual reading: complete 6-page PDF pp.1–6, §§1–6.
- Model and control permission: one horizontal axis is a 3-state model [x,v_x,φ] with virtual roll-reference input φ_r; the y axis is a separate copy with pitch reference. Assumptions: yaw=0, vertical speed=0, small roll/pitch, decoupled x/y. The AR.Drone's onboard controller regulates roll/pitch, yaw rate and vertical speed. This is not full 12-state or motor-level MPC.
- Sensors and disturbance: OptiTrack motion capture for position, velocity and attitude; ground ROS PC sends commands over Wi-Fi. Disturbance polytope is the convex hull of one-step residuals from identification flights, including model mismatch, discretization, motion-capture error, communication delay and aerodynamic forces.
- MPC and constraints: Ts=0.05 s, N=30 (1.5 s horizon); Q=diag(0.8,1.2,1), R=5; state/attitude/speed constraints and normalized roll/pitch-reference input constraints. Ancillary gain K=−[0.5,0.4,1], RPI error tube Z, tightened nominal sets X⊖Z and U⊖KZ; Riccati terminal cost and MOAS terminal set. QP generated by CVXGEN.
- Experiment/runtime: real AR.Drone 2.0 flight in x and y; maximum compute time 4 ms per axis including waypoint-change terminal-set computation. Constraint satisfaction is conditional on actual disturbance remaining within the data-derived W; waypoints were deliberately close enough to retain feasibility. This is real Tube MPC flight evidence, but only for a reduced virtual-attitude subsystem with onboard inner loops.

## Cross-paper conclusions and model impact

1. There is now direct original-paper support for 12-state, four-rotor-thrust Tube/RAMPC in simulation (Parsi and Didier). It is incorrect to claim no direct 12-state four-rotor Tube MPC precedent exists.
2. There is still no verified real-flight demonstration of a 12-state direct-four-rotor Tube/RAMPC controller in these papers. Didier explicitly could not fly its direct-thrust mode; its flight test is 2-state altitude. Michel's real flight uses 3-state horizontal axes and virtual attitude references.
3. Runtime is not an apples-to-apples benchmark: Parsi ETMPC 160 ms/PTMPC 40 ms averages at Ts=100 ms; Didier direct-thrust simulation 90 ms on a 3.1 GHz Intel i5, but flight OSQP <5 ms only for 2-state altitude; Michel 4 ms max per 3-state axis at Ts=50 ms. These support a complexity/architecture tradeoff, not a guaranteed 12-state 20 ms solution.
4. Set-membership terms must not be conflated: Parsi's ellipsoid is a predicted state tube; Didier's set-membership is parameter identification; Michel's convex hull is an offline disturbance set. None is an online intermittent-measurement state SMF/CZ posterior or information-state terminal RCI.
5. Model selection is unchanged: 12-state nonlinear 6-DOF remains the primary simulation plant per the user's thesis workload requirement; six-state planar model remains the conditional robust-proof candidate; four-state remains finite-safety baseline; two-state is a height/inner-loop fallback. Gate A remains blocked.

## Repository edits and verification

- Base main SHA after merging previous PR #174: 0601ab7e571c200543a43fcc60651380dda94705.
- New branch: research/model-background-20261103-tube-mpc-crosspaper.
- Updated only the unique paper ledger (added Parsi and Michel; no duplicate Didier entry), unique model evidence matrix, and this non-overwriting background log.
- No controller, validation script, plant code, or experiment result was changed. No new theorem or flight experiment was produced.
- The paper supplementary-material link was not retrieved due to HTTP 403; code execution remains unverified.

## Next single priority

Retrieve and inspect the Parsi supplementary material through an alternate ETH Research Collection metadata/download route or an author-hosted mirror; establish the actual solver, hardware, runnable entry point and timing method. If it remains inaccessible, record the reproducibility limit and use Didier's polytope RAMPC and Michel's CVXGEN QP as the reproducible comparison baseline.
