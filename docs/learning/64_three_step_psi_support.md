# Run 99 — three-step dependency-preserving psi support certificate

## Core question

Run 98 proved that the vertical-horizontal coupling injected through horizontal velocity cannot reach the reference angle psi before the third transition. This run therefore asks the first structurally meaningful question: with the Run-90/93 controllers frozen, does preserving the dependence between the initial horizontal/reference state and the coupling give a strictly smaller reliable three-step psi support bound than sequentially replacing that coupling by an independent scalar box?

## Frozen contracts

Use the Run-93 closed loop x_h^+=F x_h+G(w_0+c), G=(0,h,0,0)^T, h=1/50, with the same rational feedback K and base disturbance radius D0=3403343/1600000. The Run-90 exact-tail certificate supplies |u_z|<=U_z. The attitude tracking contract is |e_phi|<=0.01.

For the vertical-horizontal term c=-u_z sin(psi+e_phi), use the reliable inequality |sin(theta)|<=|theta|. No controller gain is retuned.

Run 98 gives the first nonzero Markov coefficient
m=e_psi^T F^2 G=1837/25000000>0.
At psi_3, later coupling samples c_1,c_2 have zero transfer because e_psi^T F G=e_psi^T G=0. Thus only c_0 matters for the new comparison.

Let a=(F^3)^T e_psi and C=m U_z. Since u_z is independent of x_h under the current product terminal factors but psi is a component of x_h, maximizing over the sign of u_z and e_phi gives the dependency-preserving reliable bound
h_joint,3 <= m D0 + 0.01 C + max_{sigma in {-1,+1}} h_Sh(a+sigma C e_psi).

The sequential independent-box interface instead uses
h_box,3 <= m D0 + h_Sh(a) + C(h_Sh(e_psi)+0.01).

The support terms h_Sh are recomputed using the Run-93 1390-term rational finite sum plus the M=139 block-contraction infinite tail. U_z is recomputed from the Run-90 5000-term rational finite sum plus M=20 tail. Therefore all final pass/fail comparisons are Fraction comparisons.

## Result

The verifier obtains

- m = 1837/25000000 = 7.348e-05;
- dependency-preserving psi_3 certificate: 0.3644555527833823;
- sequential scalar-box psi_3 certificate: 0.3644556407666551;
- strict reduction: 8.79832728e-08;
- joint-certificate margin to |psi|<=0.44: about 0.0755444472.

Hence, for these fixed certified outer-bound constructions,
h_joint,3^cert(e_psi) < h_box,3^cert(e_psi).

The reduction is very small. It must not be presented as a practically significant performance gain or as proof that the exact reachable-set support differs by this amount. What is proved is that the dependency-preserving **reliable certificate** is strictly tighter than the specified sequential scalar-box certificate under identical system, controller and disturbance contracts. This is the first multi-step psi-direction witness; Run 97 already gave larger one-step witnesses in v_x and mu.

## Interpretation and limitation

The result validates Run 98's propagation-depth correction: the psi benefit first becomes possible at step 3, exactly when e_psi^T F^2G becomes nonzero. It also shows why a blanket claim such as "CZ/SPZ is always materially tighter" would be unjustified: the improvement is direction- and horizon-dependent and can be numerically tiny.

This run does not prove a six-dimensional RCI, recursive feasibility, or a fixed-complexity online CZ/SPZ implementation. It also uses |sin(theta)|<=|theta| rather than a polynomial sine enclosure, so it is a conservative dependency-preserving certificate rather than an exact nonlinear reachable set.

## Literature boundary

Kochdumper and Althoff, *Sparse Polynomial Zonotopes: A Novel Set Representation for Reachability Analysis*, IEEE TAC 66(9), 2021, DOI 10.1109/TAC.2020.3024348, already provides dependency-preserving nonlinear set operations, quadratic maps and representation reduction aimed at reducing wrapping. Kochdumper and Althoff, *Constrained polynomial zonotopes*, Acta Informatica 60(3), 2023, DOI 10.1007/s00236-023-00437-5, provides constrained polynomial set operations including higher-order maps and reduction. Therefore polynomial/CZ representation itself is not the innovation. The open contribution remains a controller-relevant, recursively feasible interface showing when retained dependency yields certified tightening benefits under bounded complexity.

## Verification

Run:

```bash
python verification/check_three_step_psi_support.py
```

The script uses only Python Fraction and asserts both strict certificate reduction and the psi hard constraint.

## Status ledger

- **Proved:** the specified dependency-preserving three-step psi certificate is strictly smaller than the specified sequential scalar-box certificate.
- **Proved:** the reliable joint certificate remains below |psi|<=0.44.
- **Not proved:** exact nonlinear reachable support reduction of the same magnitude.
- **Not proved:** recursive feasibility or six-dimensional terminal invariance.
- **Still open:** whether the strict advantage survives a fixed-complexity reduction rule that also preserves the cross-time shifted-set inclusion required by MPC.

## Next unique priority

Do not extend the horizon merely to make the numerical gap larger. Define a fixed-complexity controller-direction template/reduction operator R_H for the joint set and prove a one-step contract of the form X subseteq R_H(X) together with the shifted-set inclusion needed by the MPC recursion. Then test whether the certified v_x, psi and mu support advantages survive this reduction under an explicit computation budget. This directly connects the dependency result to the repository's existing CZ compression obstruction and recursive-feasibility work.
