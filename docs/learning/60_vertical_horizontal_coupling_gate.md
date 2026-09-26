# Run 94 — vertical-thrust / horizontal terminal coupling gate

## Core question
Run 90 certifies the vertical terminal feedback and Run 93 found a hover-thrust horizontal/reference RPI candidate. This round asks whether the same horizontal certificate survives when the certified vertical thrust correction is restored.

## Reliable coupling contract
The real horizontal acceleration is
[
-(g+u_z)sinphi+d_x.
]
Run 93 used (-gpsi+w) and the certified hover-thrust radius
[
ar D_{x,0}=3403343/1600000=2.127089375.
]
Run 90 gives the exact-rational infinite-horizon support certificate
[
|u_z|<U_z^{cert}=2.10973895345387ldots .
]
With the already-certified attitude envelope (|phi|le 0.45), the elementary bound (|sinphi|le|phi|) yields
[
|u_zsinphi|le0.45U_z^{cert}.
]
Hence a valid state-independent outer contract is
[
ar D_{x,1}=ar D_{x,0}+0.45U_z^{cert}
=3.07647190405424ldots .
]

## Frozen Run-93 certificate audit
Keep the Run-93 feedback unchanged:
[
K=10^{-4}[-1075,-1837,11637,3226].
]
Because its linear mRPI support is positively homogeneous in the scalar disturbance radius, the Run-93 exact-tail bounds scale by
[
r=ar D_{x,1}/ar D_{x,0}=1.44632940214571ldots .
]
Re-evaluating with the same Fraction-based block-contraction certificate gives:

| direction | certified support | limit | status |
|---|---:|---:|---|
| horizontal position | 3.394818154 | 5 | pass |
| horizontal velocity | 3.593583211 | 3 | **fail** |
| reference angle psi | 0.527038963 | 0.44 | **fail** |
| reference rate rho | 1.013497720 | 1.92 | pass |
| reference action mu | 0.080525606 | 0.0672 | **fail** |

Thus the frozen Run-93 RPI certificate does **not** compose with the Run-90 vertical terminal controller under this uniform product outer bound.

## What is proved / not proved
**Proved:** the particular compositional proof route “replace vertical-thrust coupling by one independent additive horizontal box and reuse the frozen Run-93 RPI” fails three hard gates (v, psi, mu).

**Not proved:** the true nonlinear coupled six-state terminal RCI is impossible. The outer box discards the correlation between (u_z), (psi), the attitude error, and the horizontal state. A coupled support/CZ treatment may be materially less conservative.

This is therefore a useful negative interface result: enlarging an independent disturbance box is too conservative for the existing terminal certificate.

## Literature boundary
Santos & Lagoa (ISA Transactions 128, 2022, DOI 10.1016/j.isatra.2021.12.002) obtain tube-MPC guarantees for a reduced translational model under lower-level stabilization/time-scale separation; those assumptions do not remove the coupling audited here. Mayne (IJRNC 2011, DOI 10.1002/rnc.1758) treats nonlinear tube MPC via an ancillary controller, so retaining nonlinear/correlated coupling is established methodology rather than an innovation claim.

## Reproducibility
The numbers above are obtained by rerunning the Run-90 rational tail certificate for (U_z^{cert}), then the Run-93 rational block-contraction certificate ((M=139,N=1390)) with (ar D_{x,1}). All pass/fail comparisons are rational comparisons; decimals are display only.

## Next unique priority
Do **not** retune K yet. Preserve the product structure (S_z\times S_h\times K_{fin}) and compute support bounds for the correlated term (u_zsin(psi+e_phi)) without replacing it by an independent scalar box. First test the three failed directions (v, psi, mu). If correlation-aware bounds still fail, only then redesign the coupled terminal feedback/set.
