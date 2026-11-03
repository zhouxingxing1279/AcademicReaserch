# Continuation: Hu printed-model and RFIT proof-chain audit
Date: 2026-11-03, Asia/Shanghai.

## Repository provenance
Remote main remains 6ef4960fca63b2b2cf0301d169b3a5a6a8e92b3a. PR #180 was open/draft, mergeable=true, head c89042983c17ffd1532ee8b8d0e091244ad1cd44 at restart. Continue its independent branch rather than duplicate the same work. Re-read checkpoint and current branch ledger/matrix; Run278 and model priorities unchanged. Previous code/JSON inspection remains historical, not rerun evidence.

## Actual reading and sources
Four body sources partially checked: two direct quadrotor MPC conference papers (Hu, Didier), one original quadrotor MPC technical report (Bouffard), one general RFIT theory paper (Villanueva). Full 0 / partial 4 / abstract-only 1 including Alexis. No new unique-paper count asserted. No full-read upgrade.

### Hu — printed discrepancy confirmed
Haimin Hu, Xuhui Feng, Rien Quirynen, Mario Eduardo Villanueva, Boris Houska, *Real-Time Tube MPC Applied to a 10-State Quadrotor Model*, ACC 2018:3135–3140, DOI 10.23919/ACC.2018.8431112.
[Author PDF](https://haiminhu.org/wp-content/uploads/2018/11/2018acc_1123_fi.pdf). This run: rendered pp.2,4; text p.6 references [10],[21].
Equation (5) visibly prints final drift rows -d0*x3 and -d0*x7. This is not OCR corruption. It also prints dot(x7)=-d1*x7+x9 and dot(x8)=-d1*x8+x10 while describing x9/x10 as rates.
**Our algebraic inference:** x9=dot(x7)+d1*x7, so it cannot simultaneously be the physical pitch rate. At tabulated reference x3=10, x7=0, the printed ninth equation requires u1=d0*10/n0=10, exceeding pi/9. Thus the printed reference is not a feasible equilibrium of the printed model. This does not establish what simulation code used.
Section III-C visibly imposes invariant-ellipsoid containment throughout the horizon. No author correction or code has been verified; do not silently substitute corrected indices.

### Bouffard — source model reveals coordinate issue
Patrick Bouffard, *On-board Model Predictive Control of a Quadrotor Helicopter: Design, Implementation, and Experiments*, UCB/EECS-2012-241, 2012-12-13 (technical report, not a separate journal paper).
[Berkeley PDF](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2012/Archive/EECS-2012-241.pdf).
Read printed pp.12–17, §§2.3.2–2.4.1; visually checked printed p.12 / PDF p.26.
Equation (2.3) has A=[-d1,1;-d0,0], B=[0;n0], output [1,0]; commanded attitude is input. **Derived:** its second coordinate equals angular-rate+d1*angle. Earlier physical-rate notation therefore requires an explicit coordinate transformation. The standalone second-order equation also omits the command term present in the transfer function/state model.
Lateral g*tan(theta) uses fast vertical equilibrium T*cos(theta)=mg before small-angle linearization. Identified n0=40,d1=8,d0=80 and 25ms discretization differ from Hu's parameters. These are not bare torque dynamics or motor-level authority. This targeted reading does not re-audit the report's MPC experiments or guarantees.

### Villanueva — actual terminal condition and theorem assumptions
Mario E. Villanueva, Rien Quirynen, Moritz Diehl, Benoit Chachuat, Boris Houska, *Robust MPC via min-max differential inequalities*, Automatica 77:311–321 (2017), DOI 10.1016/j.automatica.2016.11.022.
[Accepted preprint v1](https://arxiv.org/pdf/1611.03924), targeted pp.3–7 §§2–5, Appendix B pp.11–12 through (B.3); visually checked p.7. Remaining proof steps not fully audited.
Assumptions require compact convex input/disturbance sets, regular dynamics, disturbance outer/input inner ellipsoids, valid nonlinear remainder and G-variation bounds. Theorem 5 requires center propagation, shape differential inequality, positive lambda/kappa and S*S-transpose<=I; it establishes RFIT containment, not output-feedback estimation.
Section 5 equation (16) requires **Y(t+T) subset Yref**, with Yref inside state constraints and robust invariant. This differs from Hu's all-time containment statement. The analysis explicitly ignores computational delay and assumes instantaneous feedback. The example is a spring-mass-damper, not quadrotor validation.
A state-dependent policy existing on the RFIT does not imply one executable action for all states sharing a noisy observation history.

### Didier — close the previously pending experiment distinction
Alexandre Didier, Anilkumar Parsi, Jeremy Coulson, Roy S. Smith, *Robust Adaptive Model Predictive Control of Quadrotors*, ECC 2021, DOI 10.23919/ECC54610.2021.9654893.
[Author v3](https://arxiv.org/pdf/2102.13544). This run: pp.4–6 §§III-B–E, IV-C/V.
The decoupled architecture outputs total-thrust deviation and body-rate references; RAMPC only controls altitude, while lateral/yaw LQR and faster PID handle remaining channels. The full direct-thrust model is 12-state hover linearization, four rotor inputs; simulation uses 100ms Euler discretization and reports 90ms mean solve plus update on i5.
The experimental failure is implemented by reducing requested thrust by 30% at 17s. It is not a measured independent rotor degradation model or arbitrary asymmetric motor failure. Mass/efficiency set identification is not a state posterior. Combined with the previously checked equilibrium-update caveat, the flight result cannot certify the project's deterministic actuator contract.

### Alexis access remains unresolved
Kostas Alexis, George Nikolakopoulos, Anthony Tzes, *On Trajectory Tracking Model Predictive Control of an Unmanned Quadrotor Helicopter Subject to Aerodynamic Disturbances*, Asian Journal of Control 16(1):209–224 (2014), DOI 10.1002/asjc.587.
[Publisher abstract](https://onlinelibrary.wiley.com/doi/abs/10.1002/asjc.587) rechecked: online 2012-08-16, issue 2014. PWA translational integral MPC plus attitude MPC, simulation evidence. Full-access page does not grant download; author bibliography and targeted repository search yielded no usable body. No body pages claimed.

## Cross-source decision and research boundary
| Evidence | What it resolves | What remains open |
|---|---|---|
| Hu rendered equation + Bouffard canonical realization | The coordinate/index issue is real and reproducibility-relevant | Author-intended dynamics and actual simulation implementation |
| Villanueva terminal condition + Hu presentation | End-point containment differs from all-time containment | Certified sampled-data/solver-error treatment |
| Didier direct/decoupled cases | Simulation authority differs from flown authority | Physical actuator uncertainty bounds and full-state flight |
| Alexis abstract | Cascaded PWA architecture exists | Detailed model, constraints, solver and terminal proof |

No model promotion: 12-state nonlinear primary simulation plant; six-state conditional physical proof candidate; four-state finite mathematical baseline; two-state fallback. Hu should remain an external methodological comparison, not a copy-ready plant or a 20ms safety certificate.

**Transfer requirement (our synthesis):** a reliable SMF/CZ posterior must contain every observation-consistent state; the control must be implementable from that shared history; tube/terminal arguments must cover all legal measurement branches, actuator errors and computation/hold delays. The audited RFIT theorem does not establish these interfaces. No claim of novelty or impossibility follows merely from this gap.

## Reproducibility and checks
Author PDFs downloaded without modification; Poppler rendering and PyMuPDF page identification used. No controller/verification script developed.
SHA256:
- Hu: 8db3070b18fe10ad6a95398bbecfe3ebde1f063090109e3a3f93f598bda9b088
- Bouffard: 32169a56167c8cfe1a9fc2d0ba4ff123296581a180e75c228ec91dab6b950289
- Villanueva: f02e8af16a604b386bf7e542149fc1bd3779cd100e4fe387d0f234f8c8b9e1db
PDFs remain scratch research assets; no copyrighted full texts committed. Markdown addition checks and GitHub diff/status review recorded in the chat; no CI success presumed.

## Precise continuation
Topic **in progress**. Printed-equation verification is complete; author-intended correction is not.
**Next single priority:** locate a second authoritative Hu version, erratum or author implementation and reconcile equation (5) with Bouffard's coordinate transform before judging reproducibility. Resume Villanueva Appendix B after (B.3) and check the final journal version only as needed for that transfer audit. Alexis remains at abstract, awaiting reliable full text. No controller implementation is authorized by this background task.
