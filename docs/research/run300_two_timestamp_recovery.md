# Run300 — two distinct timestamps from bounded delivery language (2026-11-03)

## Claim and quantifiers
For every infinite generation/delivery path, assume (i) each sliding window of H+1 consecutive sampling instants contains at least one sample that will **eventually be delivered** (not merely generated); (ii) each non-lost sample is delivered within D integer steps after its own timestamp; (iii) timestamps are correct, and the receiver retains all arrived samples, sorted by original timestamp. Losses are allowed, including permanent losses of other samples. H,D are nonnegative integers.

For all k >= K=2(H+1)+D-1, the receiver has at least two **distinct original timestamps** s0<s1<=k. In addition,
- latest-sample age k-s1 <= H+D;
- conservative gap bound 1<=s1-s0<=2H+1+D.

**Proof:** Two disjoint blocks of length H+1 ending no later than k-D are [k-D-2(H+1)+1,k-D-(H+1)] and [k-D-(H+1)+1,k-D]. Each contains a eventually-delivered sample, both of which must have arrived by k. The samples have different timestamps. The earliest of the two is >= k-D-2(H+1)+1, while the latest received timestamp is <=k; thus the gap between the two latest received timestamps is <=2H+1+D. The last H+1 block contains a delivered sample with timestamp >=k-D-H, giving the age bound. QED.

The gap bound is intentionally conservative; it is not asserted tight. If H or D are unbounded, no finite uniform K follows. A bound on age alone does not ensure two distinct timestamps during startup.

## Consequence for the exact discrete double-integrator
Assume p+=p+Tv+T²a/2, v+=v+Ta, ||a||∞<=abar, y_s=p_s+noise_s with ||noise_s||∞<=nubar, and all applied commands are known and subtracted in finite differencing. With the two newest received timestamps s0<s1, d=s1-s0, estimate velocity at s1 using the two positions and the known-input contribution. A conservative error bound is beta_d=2*nubar/(d*T)+(d*T/2)*abar. At current k, h=k-s1, propagate using recorded inputs:
||e_v(k)||∞ <= beta_d+h*T*abar,
||e_p(k)||∞ <= nubar+h*T*beta_d+(h*T)^2*abar/2.
This is a **conditional box outer bound**, not a CZ posterior, observer-gain synthesis, Equalized Recovery, or terminal safety proof. Delayed measurements must be applied at their original timestamp; the finite-difference estimator here explicitly uses historical samples.

## Reproducibility and limits
Run `python3 experiments/run300_two_timestamp_contract.py` (Python standard library, no random seeds). Exhaustive finite-prefix enumeration N=9,H=2,D=2 with each sample either permanently lost (-1) or delivered at lag 0,1,2. Expected result: 239868 admissible paths, 479736 post-acquisition checks, max observed age 4 and gap 4; zero assertions. The analytic proof, not finite enumeration, supplies the infinite-horizon statement. This is a synthetic contract and **not yet the repository's frozen success/miss/delay automaton**.

Prior related Run295 finite-difference recovery, Run296 no-success-cycle criterion, Run297 stale timestamp counterexample, Run298/299 age/delivery audits are complementary. No new paper was fully read for this narrow lemma; the established Rego CZ and Hassaan finite-language work remains methodological context only.

## Open obligations
Certify a concrete reachable joint finite automaton, including permanent loss and delivery queues, against this sliding-window contract. Next, establish path/phase-dependent estimation error inclusion with delayed timestamp replay. Do not infer a physical quadrotor hard bound or claim MPC recursive feasibility.
