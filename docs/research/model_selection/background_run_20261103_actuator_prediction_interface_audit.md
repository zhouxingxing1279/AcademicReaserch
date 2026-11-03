# 2026-11-03 — actuator-state and physical command-interface audit

## 1. Repository baseline and scope

- Repository: https://github.com/zhouxingxing1279/AcademicReaserch
- Latest main SHA read before editing: 9459ffe25440648504f382f5f3b74e98879dbbf0
- The unique paper ledger and model-selection matrix were reread from this main. This run adds an append-only audit; it does not modify controller code, proof code or experiment scripts.
- The latest CURRENT_CHECKPOINT still identifies Run278 as the latest main research checkpoint and leaves Gate A blocked. The checkpoint's analytical certificate is a four-state frozen-Euler object. In contrast, the current src/smf_mpc/plant.py is a six-state planar truth generator with state [p_x,p_z,v_x,v_z,phi,omega], virtual inputs [T,tau] and a bounded aerodynamic-acceleration residual. These are not the same model and their results must not be conflated.
- Run246's viability counterexample and Run260/261 terminal-safety results were checked as existing four-state evidence. They are not automatically transferable to the six-state truth generator, a full 12-state six-DOF plant, or an actuator-augmented plant.
- PR #177 remains open but is stale: its base is 0601ab7e571c200543a43fcc60651380dda94705, its head is 03bb0c2b13d492d5104a7a050ec99e5fd932dc3a, and relative to current main it is behind by 7 commits and ahead by 1. Its sole changed file is an older model-selection background log. It was not merged or rewritten; this run uses a new branch based on current main.

## 2. Primary-source reading accounting

Five original quadrotor/multirotor MPC papers received targeted body reading from primary full-text sources. **0 were read cover-to-cover; 5 were partial body reads; 0 were abstract-only among these five.** One additional 2026 paper was checked only at metadata/abstract level and is not used as model evidence.

| Paper | Reading scope in this run | Status |
|---|---|---|
| Pengkai Ru and Kamesh Subbarao (2017), Nonlinear Model Predictive Control for Unmanned Aerial Vehicles | Rigid-body model and rotor allocation; actuator equation (7); explicit prediction/state-propagation statement; simulation and Appendix A parameters | Partial full-text |
| Bicego et al. (2020), Nonlinear Model Predictive Control with Enhanced Actuator Model for Multi-Rotor Aerial Vehicles with Generic Designs | Actuator response identification; state/input definition; OCP constraints; frozen state-dependent force-rate bounds; stability/feasibility discussion; quadrotor hardware, sensors and timing | Partial full-text |
| Fang Nan, Sihao Sun, Philipp Foehn and Davide Scaramuzza (2022), Nonlinear MPC for Quadrotor Fault-Tolerant Control | Quaternion rigid-body model; first-order rotor-thrust lag; per-rotor input bounds; INDI post-processing; SQP-RTI implementation, compute time and real-flight sensors | Partial full-text |
| Jad Wehbeh and Inna Sharf (2024), Nonlinear scenario-based model predictive control for quadrotors with bidirectional thrust | SO(3) local error state; bidirectional thrust and nonlinear motor-rate constraints; scenario uncertainty; estimator/sensor assumptions; simulation and timing tables | Partial full-text |
| Parakh M. Gupta et al. (2025), LoL-NMPC | Low-level controller/mixer/motor model, constraints, embedded implementation and flight experiments; inspected public Acados model/configuration | Partial full-text plus code review |
| Bin Wang et al. (2026), Meta-Learning Augmented Model Predictive Control for Quadrotor UAV Flight in Strong Wind | Metadata/abstract only; publisher full-text retrieval was rate-limited. Public repository tree inspected, but no core ML-MPC implementation was visible. | Abstract-only candidate; excluded from conclusions |

Existing ledger entries for Ru, Bicego, Nan and Wehbeh were re-read and cross-referenced; they were not duplicated. LoL-NMPC is a new full-text partial-read record. The 2026 paper is explicitly marked abstract-only.

## 3. Primary-source findings

### 3.1 Ru & Subbarao (2017): motor dynamics only in plant propagation

- Bibliography: Pengkai Ru and Kamesh Subbarao, “Nonlinear Model Predictive Control for Unmanned Aerial Vehicles,” Aerospace, 4(2), 31 (2017), DOI https://doi.org/10.3390/aerospace4020031.
- State: x=[p(3), V_B(3), Euler angles(3), body rates(3)] = 12 coordinates. Input u=[F_1,F_2,F_3,F_4] is four individual rotor thrusts. The rigid-body model neglects aerodynamic and gyroscopic effects.
- The paper writes a first-order actuator equation F_i_dot=lambda_F(F_i^c-F_i), lists lambda_F=50 in Appendix A, but explicitly states actuator dynamics are ignored for prediction and used only for state propagation. In the equation lambda_F is a rate coefficient (effective time constant 1/lambda_F), notwithstanding the paper's “time constant” label.
- Evidence: simulation only; no physical quadrotor flight. This is a direct example of why actuator dynamics in a plant simulator do not establish actuator-aware MPC prediction.

### 3.2 Bicego et al. (2020): direct force-rate NMPC with real quadrotor flight

- Bibliography: “Nonlinear Model Predictive Control with Enhanced Actuator Model for Multi-Rotor Aerial Vehicles with Generic Designs,” Journal of Intelligent & Robotic Systems, 100, 1213–1247 (2020), DOI https://doi.org/10.1007/s10846-020-01250-9.
- For the quadrotor case, x=[p(3), p_dot(3), eta(3), omega(3), gamma(4)] = 16; gamma is actual rotor force and u=gamma_dot is the four-dimensional force-rate input. The orientation uses a minimal three-angle representation.
- The OCP constrains actuator-force amplitude and force rate. The force-rate limits are identified from measured actuator response and depend on current force. To keep the OCP constraints linear, the authors use a force estimate independent of current OCP decision variables, e.g. freezing each predicted rate bound at the current measured force across the horizon or using a previous solution.
- The paper says slightly tightened constraints are softened using slack variables to support recursive feasibility in practice; it does not provide a formal closed-loop stability proof and leaves this to future work.
- Physical setup: an under-actuated quadrotor with four collinear rotors and a separate tilted hexarotor. The controller runs on a ground-station i7 PC; horizon 1 s, 11 shooting points, 0.1 s internal prediction interval, mean solver time about 3.5 ms. Internal prediction is 10 Hz while the actuator command interface runs above 200 Hz. Measurements are MoCap position/orientation, gyros and ESC rotor speeds converted to force; linear velocity is estimated numerically from multiple position samples; accelerometers are omitted due to measured bias/offset.
- Transfer: strong evidence that an actuator-force state and per-rotor force-rate limits can be flown. Weakness: frozen rate-bound approximation, softened constraints, no terminal/recursive-feasibility theorem, and Euler singularity.

### 3.3 Nan et al. (2022): first-order motor lag in a 17-coordinate quaternion NMPC

- Bibliography: Fang Nan, Sihao Sun, Philipp Foehn and Davide Scaramuzza, “Nonlinear MPC for Quadrotor Fault-Tolerant Control,” IEEE Robotics and Automation Letters, 7(3) (2022), DOI https://doi.org/10.1109/LRA.2022.3154033.
- State x=[p(3), q(4), v(3), omega(3), T(4)] = 17 coordinates; q is a unit quaternion and T_i are actual rotor thrusts. OCP input u=[u_1,...,u_4] is commanded rotor thrust. Motor dynamics are inside the prediction: T_i_dot=(u_i-T_i)/sigma, with sigma identified from data. The OCP constrains each rotor command.
- Solver: ACADO plus qpOASES, SQP real-time iteration, 1 s horizon and 20 steps. Jetson TX2 simulation timing is 6.431 ms average and 25.75 ms maximum; the maximum is associated with the first iteration after rotor-failure constraint reinitialization. The paper reports average frequency above 150 Hz.
- Real flight: 0.75 kg quadrotor, four 5-inch propellers, 8.5 N maximum thrust per motor, Jetson TX2, Radix FC, IMU and motor-speed feedback at 500 Hz, Vicon at 400 Hz, EKF state estimation. Rotor failure and agile-flight recovery are demonstrated.
- Important interface gap: the real system is NMPC -> INDI -> drone. INDI recomputes the final four rotor commands through a pseudoinverse based on measured angular acceleration and the reduced effectiveness matrix. The paper does not prove that the post-INDI command always remains inside the original NMPC per-rotor command box. Do not claim an observed violation; the correct conclusion is that constraint inheritance after post-processing is not certified.

### 3.4 Wehbeh & Sharf (2024): local SO(3) error model with motor-rate constraints

- Bibliography: Jad Wehbeh and Inna Sharf, “Nonlinear scenario-based model predictive control for quadrotors with bidirectional thrust,” International Journal of Robust and Nonlinear Control (2024), DOI https://doi.org/10.1002/rnc.7627.
- The 12-dimensional state is a local error state [position error(3), velocity error(3), SO(3) tangent attitude error(3), angular-rate error(3)], not a global 12-coordinate quaternion rigid-body state. The OCP input is four signed rotor thrusts.
- No motor state is augmented. Motor response is represented by nonlinear, thrust-dependent upper/lower thrust-rate constraints derived from a bidirectional motor/propeller ramp model and locally linearized for the OCP. Example hardware uses bidirectional thrust; this is not directly equivalent to standard unidirectional quadrotor motors.
- Scenario MPC samples state and parameter uncertainty; the study does not include external environmental disturbances and reports simulation rather than physical flight. Its state estimation uses an MEKF/covariance model, not set-membership filtering. The timing table lists a 50 Hz frequency and 0.04 s sampling step, an apparent internal inconsistency requiring clarification before reuse.

### 3.5 Gupta et al. (2025): cascade-integrated 20-coordinate LoL-NMPC

- Bibliography: Parakh M. Gupta, Ondřej Procházka, Jan Hřebec, Matej Novosad, Robert Pěnička and Martin Saska, “LoL-NMPC: Low-Level Dynamics Integration in Nonlinear Model Predictive Control for Unmanned Aerial Vehicles,” IROS 2025, pp. 1186–1193, DOI https://doi.org/10.1109/IROS60139.2025.11246583; author preprint https://arxiv.org/abs/2506.02169.
- State: [position(3), quaternion(4), velocity(3), body rates(3), rate-controller integral state(3), normalized motor-speed states(4)] = 20 coordinates. OCP input is collective throttle plus three desired body rates, not four independent rotor commands.
- The model explicitly integrates the low-level rate controller, mixer and first-order motor-speed lag; constraints are placed on the mixed per-motor commands. The public Acados model code at commit 4526fe9443464bf7f33f942577e18ed3f6b78cee uses x=vertcat(p,q,v,w,z,thr), u=vertcat(t,wc), tau_c=Kp(wc-w)+Ki*z (the derivative term is commented out), and thr_dot=(thr_c-thr)/tau_mot. The public base configuration sets tau_mot=0.05 s, controller_dt=0.01 s and a 1 s horizon. Thus the released prediction model is PI in this torque expression, although the paper describes a PID-type low-level controller.
- Real platform: approximately 1.2 kg custom quadrotor, Cube Orange+/PX4, Khadas VIM3 Pro embedded ARM computer, RTK GNSS/IMU and ESC RPM feedback around 65 Hz. The paper reports 100 Hz real-time operation, speeds up to 98.57 km/h and 3.5 g, and average trajectory error reduction of 21.97%.
- Transfer: best evidence for including the actual low-level interface and motor dynamics when the implementation accepts body-rate/collective-throttle setpoints. Limitation: stack-specific 20-coordinate model; not direct per-rotor OCP; no SMF/CZ or robust recursive-feasibility proof.

## 4. Cross-paper synthesis

The five papers reveal four distinct levels that must not be conflated:

1. **Ideal instantaneous rotor thrust**: 12-state rigid-body predictor with four thrust inputs. Ru (2017) writes a motor lag but explicitly omits it from prediction; the direct-thrust simulations in the existing Didier (2021) and Parsi (2025) records also do not establish motor-state prediction.
2. **Actuator-force state with force-rate input**: Bicego's 16-state model. The actuator force is a state and the control is its derivative, with measured state-dependent rise/fall limits. This has direct quadrotor flight evidence, but its horizon approximation and soft constraints are not a hard safety certificate.
3. **Actual-thrust state with first-order lag**: Nan's 17-coordinate model. Four independent rotor command inputs and first-order thrust states are directly in the prediction, with real flight. The INDI post-processing layer must be incorporated or constrained separately.
4. **Integrated cascade and motor-speed model**: LoL-NMPC's 20-coordinate model. It preserves the real high-level interface and models the PI controller, mixer and motor lag; it does not optimize four motor commands independently.

Wehbeh's 12-dimensional local SO(3) error model provides a fifth useful approach—state-dependent thrust-rate constraints without actuator state augmentation—but it is bidirectional-thrust simulation evidence, not direct validation on a standard quadrotor.

## 5. Model-selection and thesis-scope impact

- Keep the 12-state six-DOF rigid-body model as the physical backbone, but classify the version with instantaneous four-rotor thrust inputs as an ideal-actuator baseline only.
- For actuator-aware full-vehicle simulation, the best clean candidate is a 17-coordinate quaternion model with four actual rotor-thrust states and first-order lag. Identify each motor time constant on the target platform and model it as an interval. A 16-state Bicego-style Euler/force-rate model is the strongest real-flight alternative when the target attitude envelope stays away from Euler singularities.
- The 20-coordinate LoL structure is the appropriate comparator if the target hardware interface is PX4 body-rate/collective-throttle commands; it is not the preferred thesis plant unless the low-level firmware/mixer is fixed and accessible.
- The current six-state planar model remains a conditional proof candidate only if the virtual pair (T,tau_y) is restricted to the projection of the four-motor feasible set. For a conventional allocation matrix B, a longitudinal request must satisfy Bf=[T,0,tau_y,0]^T, together with per-rotor amplitude and dynamic constraints. If actuator lag is not a proof state, its tracking error must be bounded and included in the tube disturbance.
- A possible 10-coordinate planar-plus-actuator extension (six planar rigid-body coordinates plus four actual rotor-thrust states) is a distinct candidate from the Bouffard/Mo-Chen 10-state near-hover model. It is not yet selected: zero-roll/zero-yaw invariance must be checked under unequal motor time constants, parameter mismatch and saturation.
- The current repository code is six-state planar truth with virtual total thrust/pitch torque; Run278's certificate remains a four-state frozen-Euler object. Run246/260/261 four-state evidence is not automatically transferable to the six-state truth plant or any 12/16/17-coordinate actuator-augmented model.
- No controller, validation script, experiment or mathematical proof was added in this independent literature task.

## 6. SMF/CZ opportunity and unresolved evidence

None of the five body-read actuator-level papers combines SMF/CZ estimation with intermittent position measurements and a robust Tube-MPC recursive-feasibility proof. Bicego uses measured MoCap pose, gyros and ESC RPM-derived force without a dedicated observer; Nan uses EKF with IMU/Vicon and ESC RPM; LoL uses GNSS/IMU and ESC RPM. These provide realistic asynchronous measurement channels but not set-membership guarantees.

A rotor-thrust measurement derived from RPM is f_i=c_f,i*Omega_i^2. The observer must include uncertainty in the force coefficient c_f,i and RPM measurement. For first-order motor lag, an interval in tau_m,i produces a set-valued state transition for each actual thrust. This can be represented in a constrained-zonotope observer and passed to Tube MPC as actuator-state uncertainty, but no direct quadrotor implementation was found in the five papers read this run. Wehbeh's scenario sampling is covariance/probability-based and is not SMF/CZ.

## 7. Repository and next step

- Baseline main SHA: 9459ffe25440648504f382f5f3b74e98879dbbf0.
- The existing open PR #177 was left untouched because it is stale and contains only an older background log.
- This run changes only the paper ledger, model-selection evidence matrix and a new independent background log. No main research controller or proof files are modified.
- **Next single priority**: determine whether actual rotor-thrust states are observable/set-identifiable when position updates are intermittent but IMU and ESC RPM arrive asynchronously. Compare SMF/CZ/set-valued observer methods, derive the correct measurement maps including uncertainty in RPM-to-thrust coefficients, and decide which actuator-augmented state set can initialize a Tube-MPC error tube without assuming full-state measurement.
