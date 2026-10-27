# Run 157 — scheduling-conditioned RCI endpoint gate

Date: 2026-10-27

## Repository state checked first

- Public repository: `zhouxingxing1279/AcademicReaserch`; default branch `main`.
- `main` does not contain `docs/research/current_checkpoint.md`; the current operational pointer is README.md, which names chapter 36 and asks for certificate-based ancillary/RCI synthesis under scheduling-consistent `W(T)`.
- Read the full chapter-36 contract and its verifier `verification/check_actuator_authority_and_scheduled_residual.py`. The recorded 381/160 horizons are explicitly HiGHS numerical results, not exact optimality certificates.
- Inspected RCI history: exact obstruction / predecessor work exists in the run37–run46 lineage; in particular, the run38 predecessor derivation requires mixed `p-v`, `v-phi`, and `phi-omega` facets. Run46 rejects one inherited-offset realization but does not rule out independent offset synthesis.
- The repository's branch list includes `research/run156-second-cycle-zero-policy-gate`; this round starts from that branch and does not overwrite main.

## Literature admission card

### Nearest neighbours and reading depth

1. **Köhler, Müller, Allgöwer (2021), “Robust output feedback model predictive control using online estimation bounds,”** author PDF: https://www.ist.uni-stuttgart.de/dokumente/public/Output.pdf ; arXiv: https://arxiv.org/abs/2105.03427. **Full text read**: Introduction, §II problem setup and bounded-disturbance assumption, §III estimation-bound constructions including Theorem 2, and §IV-A–C tube MPC / constraint tightening. It gives online-validated estimation-error bounds and a homothetic tube MPC with recursive feasibility and robust constraint satisfaction. It does not directly certify this repository's particular LPV thrust interval, intermittent packet automaton, or the current τ bound without a model-specific instantiation.
2. **Fleming, Hawari, Cannon (2024), “Robust Tube MPC Using Gain-Scheduled Policies for a Class of LPV Systems,”** IEEE Control Systems Letters 8, 1589–1594, DOI: https://doi.org/10.1109/LCSYS.2024.3412652 ; accepted manuscript landing page: https://ora.ox.ac.uk/objects/uuid:a40169d1-0f41-4845-ad0d-22dfcf9f2ecf . **Abstract and accepted-manuscript text excerpt checked; full theorem/proof not independently read this round.** It treats measurable scheduling parameters for LPV-A systems, optimised parameter-affine policies, tube constraints, recursive feasibility and exponential stability. Important limitation: its stated class assumes only A, not B, depends on the uncertain parameter; our (A(T)) has a thrust-dependent (v^+=v-hT\phi+hd) term, and actual scheduling preview/rate assumptions must be checked before claiming direct applicability.
3. **Bujarbaruah, Nair, Borrelli (2020 preprint), “A Semi-Definite Programming Approach to Robust Adaptive MPC under State Dependent Uncertainty,”** https://arxiv.org/abs/1910.04378. **Full text read**: §II model/constraint formulation, §III-A–B uncertainty envelopes, §IV-A–D uncertainty propagation, affine disturbance-feedback parametrisation, terminal RPI set, Algorithm 1 and Theorem 1/proof. It explicitly handles changing uncertainty envelopes by intersecting current and prior predicted envelopes to preserve the shifted policy's feasibility. Its uncertainty is a Lipschitz state-dependent function learned from data; our δ(T) is an analytic scheduling-conditioned residual, so the mechanism is a comparison baseline, not a direct replacement.
4. **Mayne, Raković, Findeisen, Allgöwer (2006), “Robust output feedback model predictive control of constrained linear systems,”** Automatica 42(7), 1217–1222, DOI: https://doi.org/10.1016/j.automatica.2006.03.005. **Abstract/metadata only this round.** Classical observer-error RPI plus tube MPC and tightened constraints. Retain as a foundational baseline, not as evidence that our particular scheduled/packet model is already solved.

### Candidate claim and strict difference

No novelty claim is admitted. The only candidate claim for this round is a **model-specific exact endpoint reduction** for checking a *fixed* ancillary gain (K) and a *fixed* polytope (S={x:Hx\le q}) against the repository's scheduling-conditioned disturbance contract.

The horizontal four-state model is
[
x^+=A(T)x+B\tau+E d,\quad
A(T)=A_0+T A_1,\quad |d|\le \bar d(T)=d_0+d_1T,
]
with (T\in[T_L,T_U]), (\tau=Kx) for the fixed-gain check, (E=e_v h) under the chapter-36 discretisation, (d_0=1.880), and (d_1=0.45^3/6). For each facet (i) and each vertex (v) of (S), robust invariance requires
[
H_i(A(T)+BK)v + |H_iE|\bar d(T)\le q_i
\quad \forall T\in[T_L,T_U].
]
For fixed (K,H,q,v), the left-hand side is affine in (T): both (A(T)) and δ(T) are affine, and the support of the scalar symmetric disturbance interval is (|H_iE|\bar d(T)). Therefore its maximum over the compact interval is attained at (T_L) or (T_U). Checking both endpoints is **necessary and sufficient for this fixed-(K), fixed-polytope facet inequality** under the stated affine contract; no thrust grid is needed.

This does **not** make joint synthesis convex: if (K) and the set geometry are decision variables, terms such as (H_i B K v) or vertex/control products may be bilinear. Nor does endpoint checking alone establish that the set is nonempty, contains the initial error set, respects input constraints, is compatible with measurement updates, or yields recursive feasibility. If scheduling has rate constraints, packet-dependent control authority, or a nonlinear/non-affine residual bound, the uncertainty set and extreme scheduling sequences must be re-derived rather than assuming endpoint sufficiency.

### Strongest same-condition baseline

- Fixed (K), fixed polytope: exact two-endpoint robust facet check with δ(T), compared against the same check using the global worst-case δ(T_U).
- Controller synthesis: configuration-constrained RCI with variable offsets and vertex controls (repository's existing RCI lineage), followed by a certificate-based test; do not count the endpoint reduction itself as an innovation.
- Output-feedback bridge: Köhler et al.'s homothetic tube/online estimation bounds, but only after matching the causal packet schedule and proving the estimator-to-tube interface.

### Falsifiers / admission result

Reject the endpoint lemma if any exact rational example of the affine left-hand side has an interior value above both endpoints. Reject any RCI claim if any vertex/facet endpoint inequality fails, if torque bounds fail for the implemented control, or if the initial error set is not contained. A successful endpoint audit is only a local certificate, not proof of a common RCI set.

**Admission: PASS for exact endpoint reduction as a verification simplification; FAIL for any new algorithm/novelty claim or any claim that the controller baseline is closed.** No new controller was implemented this round because the synthesis variables and packet/output-feedback interface are not yet jointly certified.

## Status labels

- DERIVED: endpoint sufficiency for fixed (K), fixed (S), affine (A(T)) and affine symmetric disturbance half-width.
- NUMERIC_CHECK: the chapter-36 horizon comparisons (381 vs 160) are solver results only.
- OPEN: existence of a nonempty common RCI polytope under all allowed thrust schedules and τ limits; inclusion of the actual ancillary error initial set; integration with intermittent measurement and recursive feasibility; six-state nonlinear lift.
