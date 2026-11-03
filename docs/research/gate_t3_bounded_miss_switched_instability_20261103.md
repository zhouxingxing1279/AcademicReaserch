# Gate T3 negative result: bounded misses do NOT imply recovery for a fixed deadbeat observer (2026-11-03)

## Scope and provenance
Base main `8486cac146ddabbc30caf6cc2365831167acfed8`. Abstract 1-axis double integrator, replicated independently for 3 axes to give 6-state [p;v]; no PX4, no SITL, no closed-loop MPC. Follow-up to the earlier nilpotent-observer/Box result. This is an original analytic counterexample, not a claim from any cited paper. No new literature read.

## Frozen model and assumptions
Sample T=0.1 s, A=[[1,T],[0,1]], C=[1,0], L=[1,1/T]^T. Position-only measurements; success corrects before propagating: F_S=A(I-LC)=[[-1,T],[-1/T,1]], miss propagates F_M=A. Error recursion e_{k+1}=F_sigma e_k+d_sigma, with compact additive disturbances; first examine homogeneous d=0. Allowed language: all words with at most 2 consecutive misses, including repeating SMM. This is an explicit sublanguage of any success/miss/delay automaton that permits these words. It has no delays.

## Analytic counterexample
F_S^2=0, so two adjacent successes eliminate initial error. However, F_S A^m F_S=-m F_S for m=0,1,2 (exact algebra; m=0 gives zero). In particular, F_S A^2 F_S=-2F_S, and (F_S A^2)^2=-2(F_S A^2) (nonzero eigenvalue -2). Thus repeated legal pattern SMM has a homogeneous transition product whose norm grows exponentially (factor 2 per 3-sample cycle). A nonzero initial error on the expanding eigendirection is unbounded despite never exceeding 2 misses. With any nonzero disturbance exciting that direction, a uniform finite robust invariant estimation-error set cannot be guaranteed for this fixed gain under the entire language. This does NOT show that every observer/CZ estimator fails: an observer with mode-dependent gains or exact two-time-stamp set intersection may still succeed.

## Reproducible finite-word enumeration (actually executed)
Python 3 with NumPy, command:
```python
import numpy as np,itertools
T=.1; A=np.array([[1,T],[0,1.]])
L=np.array([[1],[1/T]]); C=np.array([[1.,0.]])
F=A@(np.eye(2)-L@C)
for n in [3,6,9,12,18]:
 best=(0,None); count=0
 for w in itertools.product('SM',repeat=n):
  if 'MMM' in ''.join(w): continue
  P=np.eye(2)
  for c in w: P=(F if c=='S' else A)@P
  val=np.linalg.norm(P,np.inf);count+=1
  if val>best[0]: best=(val,''.join(w))
 print(n,count,best)
```
Observed (n, legal words, max infinity matrix norm, maximizer):
- (3,7,11.0,SMS)
- (6,44,22.0,SMSMMS)
- (9,274,44.0,SMSMMSMMS)
- (12,1705,88.0,SMSMMSMMSMMS)
- (18,66012,352.0,SMSMMSMMSMMSMMSMMS)

Floating-point `F@F` residual ~5.55e-17. The analytical identity above, not this finite enumeration, establishes the unbounded repeating-pattern counterexample. Finite enumeration is not a proof for arbitrary modes/delays.

## Proof status and consequences
- PROVED (symbolically): fixed deadbeat gain, bounded 2-miss language admits an exponentially growing error sequence. Hence previous success-only F^2=0 does not establish Equalized Recovery for the full language.
- VERIFIED (finite enumeration): maxima for horizons 3..18 above.
- NOT PROVED: existence/nonexistence of alternate observer, reliable CZ posterior recovery, delay-inclusive automaton, terminal Tube MPC or hard safety.
- The failure is a *particular fixed observer design*, not impossibility of position-only SMF with bounded inter-success time. Do not conflate `|F|r+delta<=r` failure with this stronger true switched-product instability.

## Next unique question
Construct a mode/age-dependent observer or a two-timestamp CZ/SMF posterior update for the max-2-miss language; prove a uniform finite error bound over every admissible word, then add timestamped delay branches. Compare it against the fixed-gain counterexample using exact finite-product algebra before extending to Tube MPC.
