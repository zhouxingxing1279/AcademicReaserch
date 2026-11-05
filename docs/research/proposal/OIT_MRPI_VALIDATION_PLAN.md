# OIT–CZ–mRPI verification: frozen first-stage plan

Date: 2026-11-05, Asia/Shanghai. Authorized by the user's pasted task specification and request to begin verification. This plan precedes the new numerical runs. Existing experiments and production controllers remain separate.

## Questions and decision rules

1. A: establish batch-versus-sequential reduction under an outer, set-monotone reduction; search a 2D counterexample when monotonicity is absent. A finite reach set is not labelled RPI.
2. B: prove tube containment for the stated error dynamics; derive the actual output-feedback joint error dynamics. Audit union-envelope and window-reset claims with explicit witnesses.
3. C: prove monotonicity of mRPI under nested disturbance sets. Demonstrate why arbitrary time-varying disturbances cannot be learned by intersection of past realizations; implement nested identification only for a declared constant bias plus bounded residual model.
4. D: derive and implement a sufficient affine-lifting LP for CZ containment/RPI. Failed feasibility means uncertified, not noncontainment. Check returned equality, box-support and sampled successor residuals independently.

## Benchmarks fixed before execution

- User's controlled double integrator: A=[[1,1],[0,1]], B=Bw=[[.5],[1]], C=[[1,0]], disturbance amplitude .05, sensor noise .10, X=[-5,5]x[-3,3], U=[-1,1], Q=I, R=.1, horizon 15. LQR gain uses u=v+K(hat_x-z). Observer gain is fixed and explicitly recorded.
- Weakly stable feedback: real poles .90 and .95.
- Generated n=4,8,16,32 stable diagonalizable systems, m=p=ceil(n/4), declared seeded construction. These are a controlled scaling family, not a representative sample of all stabilizable/detectable systems.
- Spectral-radius sweep .5,.7,.9,.95,.98. Poor-observability sweep scales measurement sensitivity while keeping sensor noise fixed.
- Paper Eq. (25): A=[[1,1],[0,1]], Bw=[[.5],[1]], C=[[1,0]], W=V=[-1,1], true initial box [1,3]^2. Replicate observable finite-window reconstruction, distinguish literal OIT from joint-trajectory consistency, and report original noise records unavailable rather than claim exact figure reproduction.
- Global seed 20261105. Repeated trajectories are paired across methods; timesteps are not independent replicates. Keep failed and negative results.

## Six required algorithm tracks

Long finite Minkowski reference (explicit 2D vertices where possible); Rakovic-style scaled finite sum with a full-dimensional disturbance block for rank-deficient input disturbance; iterative zonotope/parallelotope invariant enclosure; Raghuraman–Koeln fixed-generator one-step LP; CZ finite batch reach (no RPI claim without tail certificate); OIT-informed output-feedback joint tube with an explicit finite-memory propagation contract.

For mRPI references, report a tail bound. Tight 2D/4D methods are compared against support tolerance 1e-3; coarse methods may fail and are retained. Finite sampled directions give a support diagnostic, not a general inclusion certificate or exact Hausdorff distance. General CZ volume is not inferred from generator norm.

## Closed-loop and information accounting

Use joint error eta=(epsilon,d), epsilon=x-hat_x, d=hat_x-z, with post-measurement observer timing. Current d is known. Future measurement/process noise use shared variables. First compare sets on identical observations and applied controls; separately run feedback controllers with common exogenous disturbances.

Prediction must anticipate finite-window forgetting. All terminal and shift checks refer to the same nominal coordinates. A fixed certified joint RPI tail provides the terminal baseline; any adaptive controller is admitted only after its propagation/shift conditions are established. A safe fixed-tube fallback must be identified if an adaptive branch is not certified.

Run 10,000 independent disturbance/noise trajectories for a controller with a documented proof chain, logging initial admission, constraint/shift failures and whether nominal QPs or an exact unconstrained-optimum shortcut were used. Monte Carlo is a numerical sanity check, not proof. Detailed adaptive LP simulations can have a smaller separately reported count; do not transfer baseline results to them.

## Outputs

New package src/oit_mrpi, focused tests, executable experiments, JSON/CSV including requested fields (unavailable quantities null with reason), serialized per-time sets/controls, proof/audit report, and eight requested figure types. Record versions, source/data hashes, timings and limitations. Wall-time screens are empirical; no WCET claim. Performance novelty requires a matched-information strong baseline and must survive compute/storage accounting.

## Source checks already completed

Cong et al., arXiv:2203.13966v2, Def. 7, Algorithm 3, Proposition 3, Eq. (25). Raghuraman–Koeln, arXiv:2009.06039v1, Sections 7.1–7.2, Theorem 23. Rakovic et al., TAC 2005, DOI 10.1109/TAC.2005.843854. Previous chat's checked Brunner 2018 and Ji 2022 remain novelty constraints. The pasted citation tokens are not bibliographic evidence.

Experimental planning used the local experimental-design skill. Procedural reference: Kassis, Agarwal, He, Patel, Brueckner (2026), Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents, https://arxiv.org/abs/2609.00065 (metadata checked 2026-11-05; this is workflow provenance, not evidence for control claims).
