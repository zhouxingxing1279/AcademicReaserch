# Run299 — Joint measurement-generation/delivery contract (conditional)

Date: 2026-11-03 UTC. Scope: abstract six-state [p;v] outer-loop only; no PX4/SITL.

## Contract and quantifiers

At each integer time k a sample may be generated with immutable timestamp k. Every generated sample is delivered exactly once after a delay d in {0,...,D}; duplicates, if permitted, retain their original timestamp and do not count as fresh. At least one sample is generated in each consecutive H+1 sample slots. Receiver retains the largest *delivered original timestamp* s*(k), not the timestamp of the latest arrival. Initial transient is excluded: k >= H+D.

For **every** infinite generation/delivery sequence obeying this contract, age a(k)=k-s*(k) <= H+D. Indeed the inclusive window [k-D-H,k-D] contains a generated sample s; its arrival s+d <= s+D <= k, so s*(k)>=s>=k-D-H. This is an information-age theorem, **not** a bounded observer error theorem or Equalized Recovery.

## Finite-state implementation contract

A machine-readable implementation can store: (i) counter g in {0,...,H} of consecutive slots without generation, rejecting a transition with g=H and no generation; (ii) a pending queue of pairs (timestamp, remaining delivery delay) with maximum age D; (iii) newest received original timestamp and current age, saturating at H+D after the transient. Each tick must generate according to g, advance pending deliveries, then update newest timestamp by max, never by arrival time. A finite-state *relative-age* representation must explicitly handle initialization and delivery ordering. This document is a transition specification, not a claim that the repository has already frozen its production automaton.

## Crucial limitation: drop semantics

The theorem fails if `miss` means a generated sample may be permanently lost: bounded **generation** gaps plus bounded delay *of delivered samples only* do not guarantee bounded age. Example: generate every tick and permanently lose every sample after timestamp zero. To retain the theorem with drops, require at least one **eventually delivered** generated sample in each H+1 slot window, with delivery delay <=D. Alternatively specify a bound on consecutive permanently lost generation opportunities and derive a new effective H. An arrival event carrying an old timestamp is not a fresh success.

## Reproducible finite-prefix regression

`python3 experiments/run299_joint_automaton.py` (stdlib, no random seeds). N=8, H=2, D=2, enumerate every generation bit string meeting the sliding-window contract and every delay assignment for generated samples. Local run: 60,705 legal paths, maximum observed age 4, assertion failures 0. The enumerator checks the **bounded-delivery/no-permanent-drop** contract only; its finite enumeration is not a proof of the infinite-time result. Analytic repeated-old-timestamp counterexample also asserted at k=10,100,1000.

## Research implications / next obligation

Before claiming phase-dependent CZ/SMF recovery, freeze whether success means generation, delivery, or delivery of a *new timestamp*. Specify permanent-drop admissibility, simultaneous delivery order, buffer retention and maximum delay. Then construct and exhaustively check the reachable finite automaton and prove two-distinct-timestamp recovery with delayed replay; bounded age alone is insufficient. No terminal Tube MPC, robust safety or 12-state physical residual containment is established.

Literature status: no new paper read this run. This is a direct elementary derivation extending the Run296–298 investigation; do not attribute it to Scott/Rego/Hassaan without original-text verification.
