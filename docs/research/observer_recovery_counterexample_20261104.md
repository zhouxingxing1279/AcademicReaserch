# Observer Equalized Recovery: necessary contraction check (2026-11-04)

Status: independent analytic counterexample and exact-rational finite calculation; **not** a proof of the project Equalized Recovery or physical quadrotor safety.

## Narrow obligation

For a fixed-gain observer, post-correction error at a success event is
(e_k^+=(I-LC)e_k^- - Lv_k), and the next prior error is
(e_{k+1}^-=A e_k^+ + Gw_k).
Consequently the success transition is
(e_{k+1}^-=A(I-LC)e_k^-+Gw_k-ALv_k).
For miss it is (e_{k+1}^-=Ae_k^-+Gw_k).
These identities presume contemporaneous measurement and a fixed applied input shared by plant and observer. Delayed packets require a different augmented-state model.

## Exact scalar counterexample (all-success language)

Choose scalar (A=2,C=1,L=1/2,G=1), process disturbances (w_k\in[-1/10,1/10]), and noiseless success measurements (v_k=0) on **every** step. Thus (F_s=A(1-LC)=1). Starting from the prior-error interval (E_0=[-1,1]), the exact symmetric interval radius satisfies
[
r_{k+1}=|F_s|r_k+1/10=r_k+1/10,quad r_k=1+k/10.
]
The all-success sequence is admissible under any maximum-consecutive-miss bound, including zero misses. For each (k), choose aligned initial error and disturbances to attain (r_k). No fixed bounded interval (nor bounded set) can contain all reachable errors for all (k). Hence **bounded dropout length and finite-window observability alone do not imply Equalized Recovery for an arbitrary observer gain**. A gain/mode-word contraction or a stronger set-inclusion certificate is necessary for this fixed-gain construction; this does not prove a universal spectral-radius necessity for all alternative observers.

The exact-rational local check executed with Python 3 (stdlib fractions):
```
from fractions import Fraction as F
A=F(2); L=F(1,2); w=F(1,10); r=F(1)
for k in range(5):
    r=abs(A*(1-L))*r+w
    print(k+1,r)
assert r==F(3,2)
```
Output: `11/10, 6/5, 13/10, 7/5, 3/2`. This checks five steps only; unboundedness follows from the displayed closed form, not the test.

## Implications and next proof obligation

For each admissible transition (q\xrightarrow{\sigma}q'), certify (F_{q,\sigma}E_q\oplus D_{q,\sigma}\subseteq E_{q'}) with correctly indexed pre/post correction sets. For every admissible recovery word, certify a **uniform** block-end inclusion into the designated recovery set, including intermediate-step containment. A single favorable word or a Monte Carlo zero-violation rate is insufficient. The first computational target is a frozen no-delay success/miss automaton with explicit maximum miss count and fixed gains, checking all reachable edges and recovery blocks before adding delay.

Evidence: this counterexample is original algebra for the abstract scalar system, not a reproduction of Scott/Rego/Hassaan and not a direct four-rotor result. R-level: not applicable to a paper reproduction. End-to-end simulation, terminal MPC, and 12-state mapping remain unproved.
