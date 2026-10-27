# Run157 research log — scheduling-conditioned RCI endpoint gate

## Scope and repository provenance

The default branch README was read first. It names `docs/learning/36_actuator_authority_and_scheduled_residual.md` as the active entry and explicitly prioritizes certificate-based ancillary/RCI synthesis under scheduling-consistent `W(T)`. The chapter-36 file and `verification/check_actuator_authority_and_scheduled_residual.py` were fetched and inspected. The README's 381-tick global-box and 160-tick thrust-conditioned figures are described in the source as HiGHS numerical results without rational primal/dual certificates.

The Run156 checkpoint was fetched from `research/run156-second-cycle-zero-policy-gate`. It records an exact counterexample to a particular two-cycle zero-policy candidate, not a class-wide RCI impossibility result. The RCI lineage includes a predecessor-normal derivation (mixed p-v, v-phi, phi-omega facets) and a fixed-offset candidate rejection; neither proves that independently optimized offsets or all correlated templates fail.

The active branch for this increment is `research/run157-scheduled-rci-endpoint-gate`, based on Run156. No changes were made to `main`.

## Literature read before derivation

- Köhler, Müller, Allgöwer (2021), author PDF, https://www.ist.uni-stuttgart.de/dokumente/public/Output.pdf (also arXiv:2105.03427). Read the full 17-page paper, focusing on §II, §III estimator-bound results including Theorem 2, and §IV-A–C tube MPC, tightened constraints and recursive-feasibility construction. Relevant lesson: a current state-estimation bound is not sufficient by itself; recursive feasibility needs valid future-error and nominal-deviation bounds that align with the tube prediction.
- Bujarbaruah, Nair, Borrelli (2020 preprint), https://arxiv.org/abs/1910.04378. Read §II–IV, the uncertainty-envelope update, affine disturbance-feedback parameterization, terminal RPI set, Algorithm 1 and Theorem 1/proof. Relevant lesson: when the state-dependent uncertainty outer approximation can change non-monotonically, their recursive-feasibility argument imposes constraints against the intersection of current and previous outer envelopes. This is a caution for any future online scheduling-conditioned bound update.
- Fleming, Hawari, Cannon (2024), DOI 10.1109/LCSYS.2024.3412652, accepted manuscript landing page https://ora.ox.ac.uk/objects/uuid:a40169d1-0f41-4845-ad0d-22dfcf9f2ecf. Abstract and available manuscript text excerpt checked; theorem/proof not read in full this round. Their stated LPV-A condition (only A depends on the measurable scheduling parameter) is not assumed to automatically cover this repository's scheduling-dependent dynamics and residual.
- Mayne, Raković, Findeisen, Allgöwer (2006), DOI 10.1016/j.automatica.2006.03.005. Abstract/metadata only. Retained as foundational output-feedback tube MPC baseline, not a full-text read for this round.

## Derivation

For the reduced four-state horizontal/attitude contract, hold the ancillary gain (K) and candidate polytope (S={x:Hx\le q}) fixed. Let
[
x^+=A(T)x+B\tau+Ed,\qquad \tau=Kx,
]
where
[
A(T)=A_0+TA_1,quad |d|\le \bar d(T)=d_0+d_1T,quad T\in[T_L,T_U].
]
For every vertex (v) of (S) and facet (i), robust invariance is certified by
[
H_i(A(T)+BK)v+|H_iE|\bar d(T)\le q_i.
]
With fixed (K,S,v,i), the left side is affine in (T). Its maximum on a closed interval occurs at one of its endpoints. Hence checking both (T_L) and (T_U) is necessary and sufficient for this facet/vertex inequality over the full continuous thrust interval, provided the scheduling-dependent disturbance half-width remains the stated affine function and no extra scheduling-rate/history constraints are imposed.

This is a verification reduction only. It does not make simultaneous synthesis of (K) and (S) convex, establish nonempty invariant-set existence, ensure the implemented torque bound for a different policy class, handle packet-triggered observation updates, or prove recursive feasibility of output-feedback MPC.

## Admission decision

PASS: use the two exact scheduling endpoints to verify any fixed candidate under this affine residual contract; avoid a thrust grid.

FAIL: do not claim a new gain-scheduled tube MPC algorithm, RCI existence, or a new recursive-feasibility theorem. These are covered by established LPV and robust output-feedback MPC literature in broad form, and the current proof obligation is repository-specific instantiation and certification.

## Evidence status

- DERIVED: endpoint sufficiency for a fixed (K), fixed polytope and affine scheduling/residual contract.
- NUMERIC_CHECK: 381 vs 160 tick figures in chapter 36.
- OPEN: common RCI existence under all allowed scheduling/disturbance sequences; initial error-set inclusion; actual-input consistency; intermittent-measurement observer/tube interface; terminal append and recursive feasibility; lift from reduced four-state subsystem to the full six-state nonlinear model.

## Tests and implementation

No controller or verifier was added: the round was deliberately limited to literature admission and a proof-level simplification. No test result is claimed. Next round should implement the endpoint inequalities against an existing, precisely identified correlated RCI candidate, retaining exact/rational checking where possible; a failed candidate must not be reported as class-wide impossibility.
