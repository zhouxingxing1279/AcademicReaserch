# Run 95 — product-set correlation limit for vertical/horizontal coupling

## Core question

Run 94 showed that the coarse bound `|u_z sin(phi)| <= 0.45 U_z` makes the frozen Run-93 horizontal/reference certificate fail. The next task proposed retaining `S_z x S_h x K_fin` and exploiting correlation. This round checks whether that product representation actually contains correlation between vertical thrust correction and horizontal/reference state.

## Key correction

It does not. In a Cartesian product, a vertical state in `S_z`, a horizontal/reference state in `S_h`, and an attitude tracking error in `K_fin` can be selected independently. Therefore any state-independent scalar interval that must cover `u_z sin(psi+e_phi)` over the full product must cover independent extremizers. A tighter angle bound than 0.45 helps, but it cannot create cross-factor correlation.

To avoid relying on floating-point maxima, use finite reachable sums, which are subsets of the certified infinite mRPIs.

Run 90 gives after 5000 exact rational terms a reachable input-support witness
[
U_{z,mathrm{lo}}=2.099654935716497ldots .
]
Run 93 gives after 1390 exact rational terms
[
psi_{mathrm{lo}}=0.364397600295972ldots .
]
Because `K_fin` independently permits `e_phi=0.01`, the product contains a point with angle at least
[
a_{mathrm{lo}}=psi_{mathrm{lo}}+0.01.
]
For `0<=a<=0.45`, the alternating Taylor bound gives
[
sin age a-a^3/6.
]
Hence every independent scalar box covering the product coupling has halfwidth at least
[
D_{mathrm{cpl,lo}}
=U_{z,mathrm{lo}}left(a_{mathrm{lo}}-a_{mathrm{lo}}^3/6ight)
=0.767740561602929ldots .
]
The total horizontal additive radius must therefore satisfy
[
D_{mathrm{box}}ge D_{x,0}+D_{mathrm{cpl,lo}}
=2.894829936602929ldots .
]

## Exact failure of the frozen Run-93 box route

For the frozen linear horizontal system, reachable-set support is positively homogeneous in the scalar disturbance radius. Scaling the 1390-term exact rational lower witnesses from `D_{x,0}` to the mandatory radius above gives

| direction | finite-sum lower witness | limit |
|---|---:|---:|
| v_x | 3.3814098044 | 3 |
| psi | 0.4959213724 | 0.44 |
| mu | 0.0757711890 | 0.0672 |

All three exceed their hard limits. These are lower witnesses from finite Minkowski sums, not tail upper bounds. Therefore adding a more accurate independent scalar interval cannot rescue the frozen Run-93 certificate while the uncertainty representation remains the full Cartesian product.

## Proved / not proved

**Proved:** preserving `S_z x S_h x K_fin` does not preserve cross-factor correlation. Any state-independent scalar-box replacement of `u_z sin(psi+e_phi)` that is valid on that full product is already large enough to make the frozen Run-93 linear RPI fail velocity, reference-angle, and reference-action gates.

**Not proved:** the true coupled nonlinear terminal RCI is infeasible. Physical closed-loop trajectories can correlate `u_z` with horizontal/reference states. To exploit that, the terminal uncertainty object itself must be joint (for example a coupled polytope/CZ/reachable set or a certified state-dependent coupling bound); merely computing a sharper support on the old Cartesian product cannot recover information that the product discarded.

This corrects the Run-94 next-step wording: the useful research question is not “find a correlated support function while keeping the product”, but “construct a joint representation that retains the relevant cross-channel dependence and compare its controller-read supports against the product outer approximation.”

## Literature boundary

Le, Stoica, Alamo, Camacho and Dumur (2013), *Tube Model Predictive Control Based on Zonotopic Set-Membership Estimation*, DOI 10.1002/9781118761588.ch4, already combines zonotopic set-membership estimation with tube MPC. Ping (2015), DOI 10.1155/2015/875850, explicitly uses zonotope order reduction as an outer approximation in output-feedback robust MPC. Thus “zonotope/CZ + MPC” and complexity reduction are not innovations by themselves. Our remaining candidate contribution must be stated as a narrower comparison: whether retaining certified joint geometry in the finite directions actually read by the controller avoids a demonstrable false infeasibility introduced by a product/box interface, while preserving recursive-feasibility obligations.

## Reproducibility

Run:

```bash
python verification/check_product_correlation_limit.py
```

The script uses only Python `Fraction`. Every pass/fail comparison is rational; decimals are display only.

## Next unique priority

Construct the smallest **joint** vertical-horizontal terminal uncertainty object needed to retain the dependence relevant to `u_z sin(psi+e_phi)`. Do not retune `K` yet. First use a finite-horizon coupled reachable set (preferably CZ/polytope with an explicit outer-approximation contract) and compare the three failed controller-read directions `v_x, psi, mu` against the Cartesian-product lower obstruction above. The target result is either (i) a certified strict support reduction that restores at least one failed gate, or (ii) a proof/finite counterexample that the joint geometry still cannot restore the gates. Only after this comparison should controller redesign resume.
