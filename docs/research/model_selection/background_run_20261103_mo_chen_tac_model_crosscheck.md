# 2026-11-03 — Mo Chen published-model cross-check and 10D near-hover source reconciliation

## Repository baseline and scope

- Repository: zhouxingxing1279/AcademicReaserch; working target is main.
- Baseline observed before this run: 16661dc9ef7bdf3a824d8294c926928003bdf5e6 (PR #181 merged). PR #177 remains open and is not used as current main content.
- Literature/model-selection only. No controller, validation script, experiment or mathematical safety proof was developed.
- This run rereads the Mo Chen 2018 published article and supporting 2017 dissertation, then checks Hu's printed equations and Bouffard's model/measurement details against primary PDFs.

## Reading and verification accounting

| Source | Classification | Reading scope | Status |
|---|---|---|---|
| Hu et al. (ACC 2018), Real-Time Tube MPC Applied to a 10-State Quadrotor Model | Direct quadrotor Tube MPC | Author PDF pp.1–2: Eq.(5), Table I, Theorem 1/RFIT; pp.5–6: runtime, acknowledgments, reference [21] | Partial |
| Bouffard (2012), UCB/EECS-2012-241 technical report | Direct quadrotor MPC source | Model/identification §§2.3–2.4, Eqs.(2.14)–(2.17), combined 10-state matrix/output; Appendix A.2–A.3 | Partial |
| Didier et al. (ECC 2021), Robust Adaptive Model Predictive Control of Quadrotors | Direct quadrotor RAMPC | Author PDF pp.3–6: 12-state direct-thrust simulation, decoupled controller, Crazyflie experiment, conclusion | Partial |
| Mo Chen et al. (IEEE TAC 2018), Decomposition of Reachable Sets and Tubes for a Class of Nonlinear Systems | Model provenance/reachability, not MPC | §VII-B, Eqs.(61)–(64), §VIII | Partial |
| Mo Chen (2017), UC Berkeley PhD dissertation | Supporting thesis, not counted as a separate paper | Ch.4 §4.1.5.2, Eqs.(4.58)–(4.61), pp.90–92; bibliography [25] | Partial |

**Count**: 4 paper/report sources received targeted body reading (3 direct quadrotor MPC sources and 1 model-provenance reachability paper); 0 full-text-complete upgrades, 4 partial body reads, 0 abstract-only reads. One additional dissertation was partially checked as supporting provenance, not counted as a separate MPC paper.

## Provenance and model findings

Hu calls the example a simplified 10D scaled quadrotor, acknowledges Mo Chen for providing the model, and cites Bouffard's 2012 report as reference [21]. Mo Chen et al. (2018) publish the 10D Near-Hover Quadrotor in §VII-B and state it was used for experiments involving learning-based MPC, citing Bouffard; Chen's paper itself uses it for HJ reachability, not MPC. Mo Chen's 2017 dissertation reproduces the model in Ch.4 §4.1.5.2 and identifies Bouffard as reference [25]. This supports structural lineage Bouffard -> Mo Chen -> Hu, not identical parameter calibration.

### Bouffard report

The report's 10-state discrete LTI near-hover model is Ts=25 ms, with two lateral 4-state channels and a vertical 2-state channel. Upper-level inputs are desired pitch, desired roll and collective thrust. Identified d0=80,d1=8,n0=40; Pelican mass 1.3 kg; KT=.91. The output y=[x1,theta1,x2,theta2,x3]+bounded i.i.d. noise is five-dimensional. The physical testbed uses Vicon MX at 120 Hz and an AscTec AutoPilot inner controller at 1 kHz; setpoints are sent at 40 Hz. It supports real onboard explicit MPC/LBMPC hover and ball-catching, but not direct rotor MPC or deterministic per-motor rate guarantees.

### Mo Chen 2018 published model

In axis-grouped order x=(px,vx,theta_x,omega_x,py,vy,theta_y,omega_y,pz,vz): px_dot=vx+dx; vx_dot=g tan(theta_x); theta_x_dot=-d1 theta_x+omega_x; omega_x_dot=-d0 theta_x+n0 Sx; analogous y equations; pz_dot=vz+dz; vz_dot=kT Tz-g. Inputs Sx/Sy are desired pitch/roll, Tz vertical thrust. Disturbances enter position derivatives and therefore act as velocity disturbances. Parameters d0=10,d1=8,n0=10,kT=.91; angle bounds ±10°, thrust [0,2g], disturbance bounds 0.5/0.5/1 m/s. This is a reachability model, not a new MPC implementation.

### Hu 2018 model and equilibrium check

Hu reorders the state to x=(px,py,pz,vx,vy,vz,theta_x,theta_y,omega_x,omega_y), with the same Chen coefficients but angle bounds ±pi/9 and disturbance ellipsoid Qw=diag(.01,.09,.25). It uses virtual pitch/roll and vertical-thrust inputs, ellipsoidal RFIT and ACADO RTI; the numerical example gives no physical sensor/observer or flight platform. The reference is xref=(3,3,10,0,...,0).

The Mo Chen equations after permutation require omega_x_dot=-d0*x7+n0*u1 and omega_y_dot=-d0*x8+n0*u2. Hu Eq.(5) prints -d0*x3 and -d0*x7 in the last two drift rows. At the stated reference, d0=n0=10 and u1 bounded by pi/9, the printed first rate equation would require u1=10 to make x9_dot zero. The corrected source-model equations give u1=u2=0 and u3=g/kT (about 10.77 for g=9.8,kT=.91), within [0,2g]. This establishes a printed-equation inconsistency, not proof the implementation used the printed error. No code or erratum was verified.

### Didier 2021 comparison

The direct-control simulation uses a 12-state hover-linearized quadrotor with four individual rotor-thrust deviations and per-rotor bounds [0,0.16] N, Ts=0.1 s. The authors say direct-thrust control was difficult to implement on Crazyflie; physical 27 g Crazyflie experiments therefore use a two-state altitude RAMPC with one total-thrust deviation input, LQR for x/y/yaw and IMU-based PID for the inner loop. This separates a direct-rotor simulation from an actually flown decoupled control architecture.

## Coordinate and selection conclusions

The attitude companion realization theta_dot=-d1*theta+omega; omega_dot=-d0*theta+n0*S implies omega=physical_theta_rate+d1*theta. It is not directly the gyro rate. A physical-rate realization instead has theta_dot=rate and rate_dot=-d1*rate-d0*theta+n0*S. Measurement maps, constraints, disturbance sets and terminal sets must be transformed consistently.

The 10D family is a yaw-fixed near-hover outer-loop command-response model, not a ten-physical-DOF or full six-DOF rigid-body plant. Its coordinates are 3 positions, 3 translational velocities, 2 tilt angles and 2 companion attitude states; yaw and individual motor states are absent. Three virtual inputs do not prove a feasible common four-motor command under motor lag, yaw torque, saturation and per-motor rate limits. Bouffard has a 5-output Vicon model and state estimation; Hu specifies no physical sensor equation/observer; Mo Chen's reachability example has no estimator. None establishes intermittent-position SMF/CZ posterior inclusion.

**Decision unchanged**: 10D remains a cascaded virtual-input literature comparator, not the primary plant. Keep 12-state nonlinear six-DOF as high-fidelity simulation primary, 6-state planar (T,tau) as conditional proof candidate, 4-state as finite safety baseline, 2-state as fallback. Gate A remains blocked.

The **10D model-provenance sub-question is stage-complete** (structural lineage, source equations, virtual-input semantics, parameter mismatch and Hu print inconsistency documented). Broader 10D reproducibility/actuator closure remains in progress because Hu's implementation and virtual-to-rotor mapping are unavailable.

## Unresolved items and next single priority

- Hu's actual ACADO model/code or author clarification is still unavailable.
- Parameter scaling from Bouffard's (80,40) attitude fit to Chen/Hu's (10,10) is not derived from an identified platform.
- Virtual-to-rotor mapping, inner-loop tracking error, motor lag, yaw torque, saturation and rate constraints are not certified.
- No intermittent-position measurement model, SMF/CZ posterior, terminal information-RCI or new flight experiment was added.

**Next single priority question**: among published 12-state full six-DOF quadrotor MPC studies, which actually optimize four independent rotor thrusts/RPM with actuator dynamics included in the prediction model, and which only include them in the plant simulation or hide them behind virtual wrench/attitude commands? Compare at least three original studies, distinguishing simulation from flight evidence.

## Checks and repository result

- Baseline main was reread at SHA 16661dc9ef7bdf3a824d8294c926928003bdf5e6.
- The unique paper ledger and model evidence matrix are updated append-only; no duplicate Hu/Bouffard ICRA/Didier record was created.
- New file links are relative to the model-selection directory; source links are DOI, arXiv or institutional PDF URLs.
- No controller, code, tests or experiment outputs changed. No source was upgraded to full-text-complete.
