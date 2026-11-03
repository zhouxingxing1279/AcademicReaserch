# Hu Tube MPC primary-source audit — 2026-11-03 (Asia/Shanghai)

## Provenance and scope
Base main: 6ef4960fca63b2b2cf0301d169b3a5a6a8e92b3a. Read CURRENT_CHECKPOINT, unique paper ledger, model matrix, Run278 log/source/archived JSON, and later 1240 three-paper and 1810 reconciliation logs. Root AGENTS.md returned 404. Git transport failed; GitHub connector used.
PR #177 is open/unmerged, head 03bb0c2b13d492d5104a7a050ec99e5fd932dc3a; compare against main: diverged, ahead 1/behind 2, mergeable=false. Do not merge or overwrite that branch.
Run278 remains an inner-slice velocity-diameter lower bound and shared-open-loop obstruction, not causal-feedback impossibility. No experiments rerun.

## Reading accounting
Three original quadrotor MPC papers were directly checked against author PDFs: Hu, Didier, Falanga. Conservative grades: **full 0, partial 3, abstract-only 0**. Targeted sections below were read, not every line/reference/proof. Alexis 2014 additionally received metadata/abstract-only checking (four candidates total: **0/3/1**). Publisher access was robots-denied; author publication page confirms identity but supplies no accessible article link. Michel's ONERA PDF timed out and is not counted. Existing ledger entries must not become new-paper counts.

## Hu: primary evidence and unresolved transcription
Haimin Hu, Xuhui Feng, Rien Quirynen, Mario Eduardo Villanueva, Boris Houska, *Real-Time Tube MPC Applied to a 10-State Quadrotor Model*, ACC 2018, 3135–3140, DOI 10.23919/ACC.2018.8431112.
[Author PDF](https://haiminhu.org/wp-content/uploads/2018/11/2018acc_1123_fi.pdf), targeted pp.2–6, §§II-B–IV, Theorem 1, equations (5)–(12), Tables I–II.
States: position3, velocity3, pitch/roll, two attitude-rate coordinates; inputs: commanded pitch/roll and vertical thrust. Wind enters position derivatives. No physical sensor/ESC validation.
Ellipsoidal RFIT requires shape/center ODEs, valid nonlinear remainder bound, and input support inequalities. Theorem 1 delegates proof to reference [10]. Initial shape epsilon-I is not an SMF posterior.
§III-C proposes invariant-ellipsoid containment throughout the horizon; rigorous stability is explicitly outside scope. Do not report a demonstrated terminal-information RCI.
Numerical ACADO/RTI/RK4/qpOASES: 65 augmented states, 35 optimization controls; horizon 0.6s, three shooting intervals. Table II: mean RTI 81.6ms, explicit feedback 20 microseconds, on 1.7GHz/8GB Ubuntu machine. Neither is hardware WCET.
Equation (5) text extraction has suspicious attitude-row indices; screenshot calls did not expose readable images here. Preserve this uncertainty; do not silently repair or implement the model.

## Didier: theoretical/practical boundary
Alexandre Didier, Anilkumar Parsi, Jeremy Coulson, Roy S. Smith, *Robust Adaptive Model Predictive Control of Quadrotors*, ECC 2021, DOI 10.23919/ECC54610.2021.9654893.
[Author v3](https://arxiv.org/pdf/2102.13544), pp.2–6, §§II–IV targeted.
Direct simulation: hover-linearized x=(position3,velocity3,Euler3,angle-rates3) deviations; four rotor-thrust deviations, Euler 100ms. Rotor bounds 0–0.16N, position ±0.7m, angles ±pi/2. YALMIP/MOSEK/OSQP; mean optimization plus parameter update 90ms, 3.1GHz i5.
Homothetic polytopic tubes use u=Kx+v. Assumptions require bounded disturbances/parameters and common stabilizing K; terminal condition additionally requires contraction-plus-disturbance inequality (§II-C). Noise dilation preserves parameter-identification consistency, not hidden-state SMF.
§II-D explicitly sacrifices robustness guarantees when updating equilibrium thrust for performance.
Actual Crazyflie flight: two altitude states and total thrust only; lateral/yaw LQR, inner PID, IMU and six-camera Vicon/200Hz. OSQP <5ms pertains to that reduced controller. No direct-thrust flight or experimentally applied wind.

## Falanga: ten coordinates are not the same model
Davide Falanga, Philipp Foehn, Peng Lu, Davide Scaramuzza, *PAMPC: Perception-Aware Model Predictive Control for Quadrotors*, IROS 2018, 5200–5207, DOI 10.1109/IROS.2018.8593739.
[Accepted author PDF](https://rpg.ifi.uzh.ch/docs/IROS18_Falanga.pdf), pp.4–5 §§III-B/IV/V-A and pp.7–8 §VI targeted.
x=(position3,velocity3,unit-quaternion4); u=(mass-normalized thrust,body-rate3). Unit quaternion reduces independent coordinates; no motor dynamics in this model. VIO uses IMU/camera on Snapdragon Flight. Thrust, body-rate and velocity bounds; perception is a soft cost, not guaranteed visibility. ACADO/qpOASES, multiple shooting/RK, 100Hz single-SQP updates, 0.1s grid/2s horizon. Mean 3.53ms, observed maximum <5ms; no WCET certificate. Real flight supports virtual-input feasibility, not actuator-level robust containment. No SMF/CZ or intermittent-observation terminal theorem was established in the inspected sections.

## Alexis access checkpoint
Kostas Alexis, George Nikolakopoulos, Anthony Tzes, *On Trajectory Tracking Model Predictive Control of an Unmanned Quadrotor Helicopter Subject to Aerodynamic Disturbances*, Asian Journal of Control 16(1), 209–224 (2014), DOI 10.1002/asjc.587.
[Author bibliography](https://www.autonomousrobotslab.com/publications.html); publisher fetch denied. Abstract indicates PWA translational integral MPC plus attitude MPC. State/input equations, sensors, solver, timing and terminal conditions remain unverified. No body-page reading claimed; resume at first model section once a lawful full version is available.

## Cross-paper decision
| Architecture | Actual authority | Transfer limitation |
|---|---|---|
| Hu nonlinear ellipsoidal tube | attitude references / vertical thrust | State feedback and virtual actuators; expanded tube optimization |
| Didier direct vs decoupled RAMPC | rotor thrust in simulation; total thrust in altitude flight | Parameter identification differs from state posterior; practical guarantee caveat |
| Falanga perception NMPC | thrust / body-rate references | Fast onboard execution does not establish deterministic tube safety |
| Alexis PWA cascade (abstract only) | detailed mapping unresolved | Cannot infer terminal or actuator guarantees |

Preserve current main's **12-state nonlinear primary simulation plant**, **conditional six-state planar proof candidate**, four-state finite baseline and two-state fallback. No change of preferred/backup model is justified. Hu's result cannot resolve Run278: state-dependent boundary feedback needs information unavailable to a controller sharing a noisy observation fiber. A future transfer must separately establish posterior containment, common executable input, sampled-data error and information-terminal invariance.

Topic remains **in progress**. Next single priority: resolve Hu equation (5) against a visually readable author/archival PDF and its model reference, then audit reference [10]'s invariant-set conditions against the project's observation-fiber contract. Within that same audit, obtain Alexis body text and finish Didier §III-C/III-E/IV-C; Falanga remaining perception derivations are secondary.

## Validation boundary
Documentation only; no controller or validation script developed. Static Markdown checks and exact changed-file diff are required before PR. GitHub CI status is reported separately; absence of checks is not success. Shared ledger/matrix receive only links to this scoped rereading record, preserving existing content.


## Subsequent correction checkpoint

The [continuation audit](background_run_20261103_hu_printed_model_proof_chain.md) supersedes this run's unresolved OCR hypothesis and unqualified attitude-rate labels. The original reading scope above is historical; do not interpret it as the latest model verification status.
