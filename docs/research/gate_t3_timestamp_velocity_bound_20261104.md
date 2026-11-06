# Gate T3 — two timestamped positions: finite velocity-error envelope (conditional lemma)

Status: independent analytic lemma and exact-rational arithmetic sanity check; NOT Equalized Recovery, a CZ posterior certificate, or project-level hard safety. Based on main 8486cac146ddabbc30caf6cc2365831167acfed8. Related open PR #208 (delivery language), #209 (startup indistinguishability), #210 (common-command feasibility); reconcile before merging.

## Contract and time indices
One axis of the six-state [p;v] translation baseline; three axes follow componentwise. Sampling T>0; discrete zero-order-held acceleration residual a_j with |a_j|<=a_bar:

p_{j+1}=p_j+T v_j+(T²/2)a_j + known deterministic input contribution;
v_{j+1}=v_j+T a_j + known deterministic input contribution.

Two distinct timestamped measurements y_s=p_s+n_s, y_t=p_t+n_t, t=s+d, d>=1, |n_i|<=nu_bar. Known input contributions between timestamps are subtracted exactly. At controller time k=t+h (h>=0), the known input propagation is also subtracted. Delayed samples are processed by their *generation* timestamps; no current-time reinterpretation. Assume both readings have arrived by time k and the acceleration contract holds throughout [s,k).

## Lemma (uniform deterministic bound for a finite gap and age)
Define vhat_t=(y_t-y_s - known input position increment)/(dT) + known input velocity correction relative to s, and vhat_k=vhat_t+known input velocity increment from t to k. For all initial states, all residual accelerations in [-a_bar,a_bar], and all noises in [-nu_bar,nu_bar],

|v_k-vhat_k| <= 2 nu_bar/(dT) + a_bar T (d/2+h).

Proof: after subtracting known inputs, the position secant is v_s + T sum_{j=0}^{d-1}(d-j-1/2)a_{s+j}/d plus (n_t-n_s)/(dT). Meanwhile v_t=v_s+T sum a_j. Their difference is T/d sum_{j=0}^{d-1}(j+1/2)a_{s+j} minus the measurement-noise secant. All coefficients are nonnegative and sum d²/2, giving a_bar dT/2 + 2nu_bar/(dT). Propagating h further steps adds at most h T a_bar. This is a conservative outer bound, not necessarily a tight posterior. In 3D apply coordinatewise infinity norms.

If every admissible controller history *after startup* contains two received distinct timestamps with 1<=d<=D and latest generation age 0<=h<=H, then a uniform (loose) bound is 2nu_bar/T + a_bar T(D/2+H). This requires a proved delivery-language guarantee; a bound on generated misses alone does not imply one if generated samples can be dropped in transit. It also does not bound the pre-two-sample startup uncertainty; initial X0 must be specified.

## Exact-arithmetic sanity check
Executed locally with Python 3 standard library fractions.Fraction:
T=1/10, d=4, nu_bar=1/100, a_bar=1/5, h=3.
Noise contribution 2nu/(dT)=1/20; acceleration contribution aT(d/2+h)=1/10; total 3/20=0.15.
Coefficients (j+1/2) for j=0..3 are [1/2,3/2,5/2,7/2], sum 8=d²/2. Assertions passed. This checks arithmetic only, not the infinite family of modes or a full simulator.

## Proof boundary and next obligation
This bound supplies a candidate finite-error initialization *after two valid observations*. It does not establish a phase-indexed observer invariant, equalized recovery, CZ containment under delayed reconditioning, common causal terminal viability, or robust stability. Next: reconcile #208 timestamp-language invariants, prove every admissible post-startup information history has the required (D,H), and search boundary words for counterexamples before claiming a phase envelope. No new literature was read or reproduced in this work package (R0-R4: no change).
