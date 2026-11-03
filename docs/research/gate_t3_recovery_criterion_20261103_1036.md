# Gate T3 — finite-language Equalized Recovery: a verifiable sufficient condition and a counterexample

Date: 2026-11-03. Base main: `8486cac146ddabbc30caf6cc2365831167acfed8`. Scope: abstract outer-loop LTI model only; no PX4, motor, or SITL interface work.

## Precise proposition (new conditional result, not a complete Gate T3 proof)

Let posterior-to-next-prior observer error obey
`e_{k+1}=F_{q_k,σ_k} e_k + d_k`, `d_k∈D_{q_k,σ_k}`,
where the finite automaton admits transitions `q --σ--> q'`, and every mode is selected from **received** observations/timestamps, not hidden state. For a symmetric box `E_q={e: |e|≤r_q}` and a certified componentwise box `D_{q,σ}⊆[-δ_{q,σ},δ_{q,σ}]`, the finite family of inequalities

`|F_{q,σ}| r_q + δ_{q,σ} ≤ r_{q'}` (componentwise, for **every** allowed edge)

is sufficient for `e_k∈E_{q_k}` for every initial `e_0∈E_{q_0}`, every legal infinite word and every disturbance/noise sequence in the stated sets. Proof: triangle inequality on each coordinate followed by induction on the path length. These are linear inequalities in radii **only after observer gains are fixed**. Feasible finite radii and nonempty initial error inclusion must be checked, not assumed. A CZ `E_q` can replace boxes if the exact inclusion `F E_q⊕D⊆E_{q'}` is verified; a numerical sampling check is insufficient.

For a **fixed repeated recovery word** `ω=(σ_0,…,σ_{m-1})` with product `P=F_{m-1}…F_0` and accumulated disturbance `D_ω=D_{m-1}⊕F_{m-1}D_{m-2}⊕…⊕F_{m-1}…F_1D_0`, a sufficient periodic recovery test is `P E_0⊕D_ω⊆E_0`, together with bounded intermediate images. For box radii this is `|P|r_0+δ_ω≤r_0`. If `ρ(|P|)<1`, a nonnegative finite candidate is `r_0=(I-|P|)^{-1}δ_ω`; enlarge if necessary to include the specified initial error. This **does not** establish recovery for an automaton admitting other recovery words. Every allowed return word/edge or a common automaton invariant family must be checked. A mode-dependent observer may be used only if its gain is determined by observable history.

## Explicit counterexample: bounded measurement gaps alone do not imply recovery

Take `A=diag(1,2)`, `C=[1 0]`, `G W={0}`, `V={0}`, and success at **every** step (maximum miss length zero). States `x_0=(0,+1)` and `x'_0=(0,-1)` produce identical position outputs `y_k=0` for all `k`, but their hidden second-state separation grows as `2^{k+1}`. Every deterministic causal observer/control law sees identical histories, so its estimation error cannot remain within a fixed bounded set for both trajectories. Thus finite success/miss language plus bounded disturbances does **not** imply Equalized Recovery without detectability/finite-window observability or suitable initial hidden-state restrictions. This counterexample is **not** the six-state double-integrator candidate; it isolates a missing assumption in any general Gate T3 claim.

For the intended double-integrator `A=[[I,T I],[0,I]]`, `C=[I,0]`, two distinct successful timestamps yield rank-six finite-window observability when `T>0`. That removes this specific unobservable-mode obstruction but does **not** by itself prove an invariant CZ observer error family with delay, finite memory, and bounded complexity.

## CZ posterior versus observer error outer bound

The exact consistency posterior is a set of possible states conditioned on the **same observed history**. Its size may shrink after success. The fixed-gain observer error box above is an unconditional overapproximation over all allowed noise and measurement values. Even if exact CZ posterior is smaller in examples, a strict improvement in all paths is not established. A reduction must be an outer approximation (preserve truth inclusion). If a delayed measurement arrives, apply it at its timestamp using a trajectory-window set; the simple success matrix `A(I-LC)` does not model delayed correction.

## Next single proof obligation

Freeze a concrete six-state discrete `[p;v]` plant, numerical `T,A,B,G,W,V`, a **fully specified** finite success/miss automaton and initial error box; choose fixed causal gains, enumerate **all** automaton edges and permitted return words, solve/check the componentwise inequalities, and save the worst edge margins plus a failing example if infeasible. Only after this should delay augmentation and exact CZ posterior be compared. No controller, terminal-set or safety theorem is claimed here.

## Evidence classification

This note gives an original elementary induction proof and a constructed exact counterexample; it does not claim to reproduce a theorem from Scott/Rego/Hassaan/Qiu/Ji. It neither reads new papers nor adds a literature ledger entry. Numerical simulation: **not run**; the statements above are symbolic and algebraically checkable. Existing repository `src/common/numerical_sets.py` is a Box/Zonotope helper, not a verified CZ implementation.
