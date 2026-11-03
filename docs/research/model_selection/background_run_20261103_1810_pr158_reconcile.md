# Background reconciliation 2026-11-03 — transplant PR #158 after PR #176

## Repository state

- Main before reconciliation: ddce07a4cfbecbd8fba180222489065726d9d8e7.
- PR #176 was safely squash-merged first as commit ddce07a4cfbecbd8fba180222489065726d9d8e7; this added the later direct quadrotor SMF/TMPC and Patel Chapter 7 evidence.
- PR #158 remained open but GitHub then reported mergeable=false and compare status diverged (3 commits ahead, 4 behind). Its changes were not present in main: DOI 10.3390/aerospace4020031 absent from the unique paper ledger, the Ru/Subbarao model-matrix section absent, and its dedicated run log absent.
- To preserve rather than overwrite that concurrent work, this branch was created directly from the post-PR176 main SHA above. Only the three documentation increments from PR #158 were transplanted; the original stale branch was not rewritten.

## Literature verification and correction

- One existing primary quadrotor paper was partially rechecked against the full 26-page ResearchGate author-uploaded text and publisher metadata: Pengkai Ru and Kamesh Subbarao, “Nonlinear Model Predictive Control for Unmanned Aerial Vehicles,” Aerospace 4(2), Article 31 (2017), DOI https://doi.org/10.3390/aerospace4020031. MDPI confirms the authors, date, model, open-access version and 26-page article; the ResearchGate full-text page exposes the paper body and Appendix A.
- Actual scope checked: §2 model/input equations (3)–(7); §3 sampled MPC and constraints; §4 SDC-NMPC and sampled-data tracking-error analysis; §6 simulation hardware/results; §7 conclusions; Appendix A parameters. Status remains **partial full-text reading**, not a complete equation-by-equation audit.
- State is 12-dimensional x=[p_I(3), V_B(3), Euler angles(3), body rates(3)], with four individual rotor thrust inputs F1–F4 and the mixing relation to total thrust/three torques. The continuous model neglects aerodynamic and gyroscopic effects.
- Actuator model: dot(F_i)=lambda_F(F_i^c-F_i), lambda_F=50 s^-1. The paper explicitly says actuator dynamics are used for plant-state propagation but ignored in the MPC prediction. Appendix A gives Δt=0.05 s, prediction/control horizons 25, Q=I12, R=I4; mass 0.8 kg, J=diag(0.0224,0.0224,0.0436) kg m², arm length 0.165 m, rotor-momentum/thrust coefficient 0.002167 m, g=9.8 m/s².
- Derived under a zero-order-held command and the paper's assumed first-order actuator: over 50 ms, response fraction 1-exp(-50*0.05)=91.79%, residual 8.21%; over 20 ms, response fraction 1-exp(-50*0.02)=63.21%, residual 36.79%. This is a calculation from the paper's assumed lambda_F, not a measured or certified ESC bound for the project vehicle.
- All simulations are reported on a Fujitsu America i7 laptop, 8 GB RAM, 2.8 GHz, MATLAB R2016a. The paper does not report per-solve runtime or WCET. The SDC-NMPC uses SQP; the hover linear MPC uses a QP formulation. No real flight, no observer/SMF/CZ, no intermittent position measurement, and no actuator state in the MPC prediction.

## Files preserved

- Unique paper ledger: appended one Ru/Subbarao 2017 record; no DOI duplicate existed in post-PR176 main.
- Unique model evidence matrix: appended the matching model/actuator evidence and clarified that the one-step lag percentages are model-derived, not measured.
- Original historical run log from PR #158 retained unchanged, including its original base-main provenance.
- No controller, plant, validation script, or experiment code changed. No new MPC simulation, SITL, HIL or flight experiment was run.

## Next single priority

Determine whether measured per-rotor thrust step-response data for the target vehicle can support a deterministic 20 ms actuator-error outer bound, and compare those data with the paper's assumed first-order lag; if not, specify the required bench-identification contract. This background task will not implement the controller or validation script.
