# 58 Coupled horizontal-reference authority gate

Date: 2026-09-27. Base: `c1db4e26bd479da4ef4f9920e514822ab74ae133`.

## Core question

Run 91 proved that an independent zero-attitude terminal policy cannot reject the nonzero horizontal disturbance. Before synthesizing a coupled horizontal/reference RCI, the first necessary gate is whether the Chapter-05 reference/attitude contract has enough physical authority to oppose the full certified horizontal disturbance while respecting the original thrust and attitude limits.

## Exact result

Use the repository bounds
[
|d_x|\le 47/25,quad T\ge g/2=981/200,quad
|e_\phi|\le1/100,quad |\psi|\le 44/100,quad |\phi|\le45/100.
]
Choose the symmetric static reference candidate (psi=\pm41/100,ho=0,mu=0). For the positive-disturbance side, the least favorable actual tilt is
[
\phi_{\min}=41/100-1/100=2/5.
]
For (x=2/5), the alternating Taylor bound gives
[
\sin x\ge x-x^3/6=146/375.
]
Therefore even at the minimum allowed thrust,
[
T_{\min}\sin(\phi_{\min})-|d_x|
\ge {981\over200}{146\over375}-{47\over25}
={371\over12500}=0.02968>0.
]
The negative side follows by symmetry. Also (|\psi|=0.41<0.44), (|\phi|\le0.42<0.45), and at (ho=0,mu=0) the Chapter-05 braking-kernel successor equals the same reference state. Thus the reference kernel and torque-reference action bound do not create a static authority obstruction.

This is a **necessary-interface result only**. It does not prove a coupled horizontal/reference RCI. Arbitrarily switching (d_x), finite attitude-reference slew, horizontal position/velocity bounds, the simultaneous vertical-thrust policy, and the shifted terminal candidate remain to be certified.

## Literature boundary

Santos and Lagoa (ISA Transactions 128, 2022, DOI 10.1016/j.isatra.2021.12.002) assume stabilizing lower-level attitude/position loops and time-scale separation in their reduced translational tube MPC; that assumption is stronger than the present explicit coupling. Xue et al. (IET Control Theory & Applications, 2024, DOI 10.1049/cth2.12588) explicitly treat translational uncertainty induced by rotational tracking and generate desired attitude from the translational controller. These works support treating the horizontal-to-attitude interface explicitly, but neither supplies the exact gate above for this repository model.

## Status and next unique priority

**Proved:** there is no static control-authority obstruction from the full horizontal disturbance box to the Chapter-05 reference/attitude limits; the rational witness is (psi=\pm0.41,ho=0,mu=0).

**Not proved:** existence of a bounded coupled horizontal-reference RCI or full six-state recursive feasibility.

Reproduce with:
```bash
python verification/check_horizontal_reference_authority_gate.py
```

Next unique priority: freeze a causal horizontal feedback that generates (mu) and search/certify a bounded RCI for ((p_x,v_x,psi,ho)), treating (e_\phi\in[-0.01,0.01]) as the certified attitude-tracking uncertainty and enforcing every successor reference in (mathcal C_{\rm new}). The first failure, if any, must be reported as a facet/action certificate rather than repaired by enlarging the set.
