# Background run 2026-11-03 — direct quadrotor SMF, zonotopic reachability and multirotor Tube-MPC evidence

## Repository and checkpoint audit

- Repository: zhouxingxing1279/AcademicReaserch.
- Main SHA checked before this run: 0601ab7e571c200543a43fcc60651380dda94705.
- Background branch: research/model-background-20261103-tube-mpc-crosspaper, based on that main; prior three background commits include the Parsi/Michel paper-log and model-matrix additions.
- Read the current CURRENT_CHECKPOINT.md, unique PAPER_READING_LOG.md, MODEL_SELECTION_EVIDENCE.md, and the latest model-selection logs. The main checkpoint remains Run278; newer Runs 283–287 and several model-background PRs are open but not merged. They are not treated as current main evidence.
- Concurrent PR #158 also edits the unique paper ledger and model matrix. This creates a shared-file merge-order risk; do not merge blindly. Our branch is kept isolated pending reconciliation.

## Single research question

What direct evidence already exists for (i) set-membership state estimation combined with quadrotor MPC, (ii) constrained-zonotope reachability/tube MPC on quadrotor or multirotor platforms, and (iii) the remaining gap relevant to intermittent position-only measurements and physically realizable rotor inputs?

## Papers actually verified this run

**Five paper records were checked: 3 full-text reads, 1 partial full-text read, and 1 abstract/secondary-summary-only candidate.** A doctoral dissertation was also read selectively and is reported separately, not counted as a paper.

### A. Ji, Geng & Driggs-Campbell (CDC 2022) — direct 12-state quadrotor SMF + robust output-feedback MPC
- Full paper and code audit described in the unique paper ledger.
- Key finding: a direct 12-state hover-linearized quadrotor example already combines ellipsoidal set-membership state estimation with tube-based robust output-feedback MPC. The four inputs are total thrust deviation plus three moments, not four rotor thrusts. C=I12 assumes all 12 state components are measured every step with bounded noise. The paper's Theorem 1 provides recursive feasibility, constraint satisfaction, nominal exponential stability and convergence of the actual state to an RPI set, under initial feasibility and terminal cost/set Assumption 1.
- The code repository is MIT-licensed and exposes SSE.py, sm_mpc.py, and sm_mpc_qr.py; static inspection shows CasADi 3.5/IPOPT and N=15. No code execution, timing benchmark or real flight is claimed.

### B. Ping et al. (Journal of the Franklin Institute 2020) — general LPV zonotopic SMF + output-feedback RMPC
- Partial text only: abstract, introduction, problem definition, observer, algorithm and CSTR example preview. Full publisher PDF was inaccessible.
- Uses time-varying zonotope estimation-error sets, offline observer sub-gains, an ellipsoidal minimal-RPI outer bound, and online output-feedback RMPC. Abstract states recursive feasibility and robust-stability properties under the paper's LMI and initial-feasibility conditions. Numerical example is a 2-state CSTR, not a UAV; no intermittent measurements were found.
- This is a strong transferable zonotope-SMF/RMPC theory reference, but not quadrotor evidence and not Constrained Zonotope.

### C. Delansnay, Dewasme & Vande Wouwer (CoDIT 2025) — hexacopter CZ Tube-MPC real flight
- Complete 6-page conference PDF read.
- Outdoor DJI F550 hexacopter with Pixhawk 4 and Raspberry Pi 5. The identified closed-loop model is 4-state (vx,vy,vz,yaw), with desired three-axis velocity and yaw commands; Pixhawk retains the low-level motor/attitude loop. Nominal MPC augments position integrators, while ancillary feedback uses the 4-state velocity/yaw model.
- CORA/constrained-zonotope reachability computes an RPI tube and tightens nominal constraints. Sampling is 200 ms, horizon 10; do-mpc/IPOPT. Average complete-loop computation is 52 ms and observed maximum 77 ms, both within the 200 ms period. Four outdoor experiments under wind were performed.
- This is genuine multirotor CZ Tube-MPC flight evidence, but not a quadrotor, not 6-DOF/motor-level MPC, and not a set-membership state posterior. The paper does not provide a full formal recursive-feasibility theorem.

### D. Andrade, Normey-Rico & Raffo (IEEE Access 2024) — 24-state tiltrotor CZ Tube-MPC HIL
- Full article read; its existing unique ledger entry was expanded rather than duplicated.
- The object is a tiltrotor UAV with suspended load, not a quadrotor: 20 physical states from 10 generalized coordinates plus four tracking integrators, four inputs (two rotor thrusts and two tilt-servo torques). HIL uses ProVANT/Gazebo with a virtual sensor reading the full simulator state; no actual output-feedback observer or intermittent measurement.
- Gurobi on Jetson TX2; 12 ms sampling. CZ-MPC most commonly takes 20.9 ms vs 29 ms for the polytope baseline, so even the faster typical solve exceeds the sampling period. HIL, not real flight.

### E. Patel, Kaya & Subbarao (AIAA SciTech 2026) — abstract-only candidate
- Only bibliographic metadata and a secondary database summary were available; AIAA full text, DOI and page numbers remain unverified. Not counted as a full-text paper.
- The summary describes zonotopic reachable sets for safe quadrotor trajectory tracking. It appears related to Patel's 2026 dissertation Chapter 8.3, but exact overlap is unverified.

## Additional non-paper source: Patel (2026) PhD dissertation

- Targeted reading of Chapter 6.1–6.2.5 and Chapter 8.3.1–8.3.4.
- Chapter 6 integrates ellipsoidal/zonotopic SMF with MPC for LTV spacecraft relative dynamics; it is not a quadrotor case. It explicitly avoids claiming asymptotic stability in that application and focuses on boundedness/terminal velocity constraints.
- Chapter 8.3 separately gives a Crazyflie 2.1 12-state quadrotor with four propeller-speed inputs and online zonotopic reachable-set/safe-corridor MPC. It assumes motor speed can change instantaneously, uses a point state estimate as initial condition, and does not include a state SMF posterior or intermittent measurement model. Sampling 50 ms, MPC horizon 5, reachability horizon 15, zonotope order 29; soft constraints include slack. Simulation only.
- Therefore the dissertation does not demonstrate a unified quadrotor SMF/CZ output-feedback controller; it demonstrates two adjacent applications in different chapters.

## Corrected cross-paper conclusions and model impact

1. Direct quadrotor SMF+MPC precedent exists. Ji et al. (2022) is a direct 12-state quadrotor ellipsoidal-SMF/output-feedback-RMPC paper. It invalidates any blanket statement that no quadrotor state-SMF/MPC precedent exists. It does not use partial/intermittent position measurements, CZ posterior sets or motor-level inputs.
2. Direct quadrotor CZ reachability-MPC precedent also exists in a dissertation case study. Patel (2026) Chapter 8.3 uses a 12-state Crazyflie model and four rotor-speed inputs, but the initial state is a point estimate, motor dynamics are omitted, and no state SMF is coupled to the controller. The associated AIAA 2026 paper is currently abstract-only.
3. Direct multirotor CZ Tube-MPC has real-flight evidence. Delansnay et al. (2025) demonstrate a low-dimensional velocity/yaw outer loop with Pixhawk inner control on a hexacopter. This does not establish full 12-state quadrotor motor-level feasibility or 20 ms computation.
4. General zonotopic SMF+output-feedback RMPC theory already exists. Ping et al. (2020) gives a time-varying zonotope-estimation-error / ellipsoidal-RPI / online RMPC architecture for LPV systems, but its example is a 2-state CSTR. The already-registered Ping/Sun 2015 and Qiu et al. ellipsoidal SMF-MPC papers remain relevant cross-checks; no duplicate records were added.
5. The research gap is narrower than “first SMF+MPC.” Current evidence does not establish a quadrotor method combining partial/intermittent position-only observations, bounded state posterior (SMF/CZ), hidden-velocity recovery, one shared causal command over every admissible posterior state, physically feasible four-rotor inputs and a hard safety/terminal-RCI recursive-feasibility proof. This is the defensible innovation boundary to test, not a claim of first general integration.
6. Model ranking does not change. The 12-state nonlinear six-DOF plant remains the primary high-fidelity simulation object; the six-state planar (T,τ) model remains the conditional proof candidate; four-state stays a finite-safety baseline and two-state an inner-loop fallback. Ji strengthens 12-state virtual-wrench output-feedback evidence; Patel strengthens 12-state rotor-speed/CZ-reachability evidence. Neither closes the current intermittent-measurement, motor-dynamics or terminal-safety gap. Gate A remains blocked.

## Parsi supplementary-material follow-up

The prior run's ETH bitstream result is corrected: the direct /bitstreams/{uuid}/download route returns the article PDF, deposited with ETH DOI 10.3929/ethz-b-000582916, not the supplementary material DOI 10.3929/ethz-b-000559871. The latter's DOI/metadata route still returned 403. The author's visible public GitHub repositories did not reveal a code mirror. No supplementary archive was obtained and no Parsi code was run. Preserve the reproduction status as blocked.

## Repository edits and checks

- Continue on branch research/model-background-20261103-tube-mpc-crosspaper, based on main SHA 0601ab7e571c200543a43fcc60651380dda94705.
- Updated the unique paper ledger: add Ji 2022, Ping 2020, Delansnay 2025; expand the existing Andrade 2024 record; clarify Parsi supplement retrieval; add the Patel dissertation and AIAA abstract candidate in clearly separated non-paper/pending sections.
- Append one model-evidence correction section clarifying that Ji 2022 already demonstrates direct quadrotor ellipsoidal SMF+RMPC, and distinguishing Patel's CZ reachability from SMF.
- No controller, validation script, plant, experiment or simulation code was changed or run.
- Run Markdown whitespace/heading/DOI de-duplication checks and inspect the branch diff. PR #158 concurrently edits the shared paper ledger and matrix; create an isolated PR but do not merge until that concurrent append is reconciled.

## Next single priority

Read Patel (2026) dissertation Chapter 7 in full (hybrid zonotopic set-membership Kalman filter plus MPC for 6-DOF spacecraft) and audit its measurement assumptions, set update, terminal constraints and robustness claims. Determine which parts transfer to intermittent position-only quadrotor measurements, and which require new proofs. Keep the AIAA 2026 quadrotor paper abstract-only until the publisher full text is obtained.
