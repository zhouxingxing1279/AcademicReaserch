# Run 98 — horizontal/vertical coupling propagation depth

## Core question

Run 97 proposed extending the dependency-preserving support comparison to two steps and suggested that the previously unchanged \(\psi\) direction might then become strictly tighter. Before implementing a nonlinear two-step SPZ/CPZ enclosure, this run checks whether the coupling can physically reach \(\psi\) in two closed-loop transitions.

This is a blocking structural question: if the Markov path has zero gain, no set representation can create a genuine two-step \(\psi\)-support improvement from this coupling.

## Frozen model

Use the Run-93 horizontal/reference closed loop
\[
x_h=(p_x,v_x,\psi,\rho),\qquad
x_h^+=F x_h+G c,
\]
where \(c\) denotes the vertical-horizontal coupling contribution (including the nonlinear \(-u_z\sin(\psi+e_\phi)\) term after reliable enclosure) and
\[
G=(0,h,0,0)^\top,\qquad h=1/50.
\]
The reference action is \(\mu=-Kx_h\) with
\[
K=10^{-4}[-1075,-1837,11637,3226],
\]
and
\[
F=A-B_\mu K.
\]

The exact nonlinear magnitude of \(c_k\) is irrelevant for the propagation-depth claim; only its injection channel \(G\) matters.

## Exact proposition

For arbitrary scalar sequence \(c_0,c_1,\ldots\),
\[
x_1=Fx_0+Gc_0,
\]
\[
x_2=F^2x_0+FGc_0+Gc_1,
\]
\[
x_3=F^3x_0+F^2Gc_0+FGc_1+Gc_2.
\]

Direct rational arithmetic gives
\[
e_\psi^\top G=0,
\qquad
e_\psi^\top FG=0,
\]
but
\[
\boxed{e_\psi^\top F^2G=\frac{1837}{25000000}=7.348\times10^{-5}>0.}
\]

Therefore:

1. the coupling cannot affect \(\psi_1\);
2. it also cannot affect \(\psi_2\);
3. the earliest possible effect on \(\psi\) is \(\psi_3\).

This is exact and does not depend on disturbance magnitude, sine approximation, Monte Carlo, or a particular set representation.

## Consequence for Run 97

The proposed target
\[
h_{\rm joint,2}(e_\psi)<h_{\rm box,2}(e_\psi)
\]
cannot be justified as a consequence of preserving the \(u_z\)-\(\psi\)-\(e_\phi\) dependency, because that coupling has identically zero transfer to \(\psi\) over two transitions.

Thus Run 97's stated expectation that the two-step horizon is the first point where \(\psi\) can improve was off by one transition. A two-step study may still show strict differences in \(v_x\) or \(\mu\), but it cannot establish the desired new \(\psi\)-direction result from this coupling.

## Literature boundary

Kochdumper and Althoff, *Sparse Polynomial Zonotopes: A Novel Set Representation for Reachability Analysis*, IEEE TAC 66(9), 2021, DOI 10.1109/TAC.2020.3024348, provides dependency-preserving nonlinear set operations and reduction aimed at reducing wrapping. Their later *Constrained polynomial zonotopes*, Acta Informatica 60, 2023, DOI 10.1007/s00236-023-00437-5, provides constrained polynomial set operations including quadratic/higher-order maps. These representations are relevant once the coupling reaches a queried direction, but no representation can overcome the exact zero Markov coefficients above.

## Verification

Run:
```bash
python verification/check_coupling_propagation_depth.py
```

Expected exact outputs include
```
e_psi^T G    = 0
e_psi^T F G  = 0
e_psi^T F^2G = 1837/25000000 = 7.348e-05
PASS
```

The verifier uses only Python `Fraction`.

## Status ledger update

- **Proved:** coupling injection through horizontal velocity has zero transfer to \(\psi\) at horizons 1 and 2.
- **Proved:** the first nonzero transfer coefficient to \(\psi\) occurs at horizon 3 and equals \(1837/25000000\).
- **Corrected:** Run 97's proposed two-step \(\psi\)-support strict-improvement target is structurally premature.
- **Still open:** whether a reliable dependency-preserving three-step nonlinear outer approximation yields a strict \(\psi\)-support reduction relative to sequential independent-box propagation.

## Next unique priority

Construct a **three-step**, not two-step, dependency-preserving joint outer approximation with a rigorous sine remainder. Keep the Run-90/93 controllers frozen. Compare only the controller-read directions \(v_x,\psi,\mu\) against the sequential scalar-box baseline. The decisive new target is
\[
h_{\rm joint,3}(e_\psi)<h_{\rm box,3}(e_\psi).
\]
If strict reduction survives the guaranteed nonlinear remainder, record it as the first multi-step propagation result; otherwise record the loss mechanism rather than retuning \(K\).
