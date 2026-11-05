# Run289 — Run288 dropout-pattern semantics audit (2026-11-03)

## Scope and evidence
Reviewed `experiments/run288_multiseed_zonotope_stress.py` on PR #178 (`research/run288-multiseed-zonotope-stress`) against current `main` checkpoint. This is a **static, independently enumerated schedule audit**, not an execution of the full NumPy/SciPy benchmark and not a proof of closed-loop feasibility. Main checkpoint continues to concern a frozen four-state Euler problem; the PR #178 twelve-state ZOH synthetic example uses independent, illustrative uncertainty bounds. The two models' safety claims cannot be transferred.

## Exact observation schedule
The Run288 code has `receive = (k % 5 == 0) and ...`, so measurement opportunities occur only at k=5,10,...,150. The `all` label means **all 30 scheduled opportunities received**, *not* all 150 simulation steps observed.

For `pattern=="mms"`, the code accepts scheduled packet index `j=k//5` when `j % 3 != 2`. At j=1,2,3,4,5,6 this is `S M S S M S`: the actual repeating phase is **SMS**, not MMS. It has 20 successes and 10 misses among 30 opportunities. For `pattern=="smm"`, success occurs only when `j % 3 == 0`: `M M S M M S`, i.e. **MMS**, not SMM. It has 10 successes and 20 misses. This is a naming/phase mismatch and may invalidate comparison to a formally specified dropout automaton; it does **not** by itself imply invalid trajectories because cyclic shifts may be permitted depending on the automaton's initial phase and history.

A simple deterministic independent enumeration over `k=1..150` gives:
| code label | scheduled opportunities | received | actual first six opportunity symbols |
| --- | ---: | ---: | --- |
| all | 30 | 30 | SSSSSS |
| mms | 30 | 20 | SMS SMS |
| smm | 30 | 10 | MMS MMS |

## Required correction and tests
1. Freeze the actual formal dropout automaton, initial mode, and whether k=0 is a packet opportunity. Derive accepted sequences from that automaton rather than string labels.
2. Refactor `receive` into a pure schedule function; test expected six-symbol prefixes and 150-step counts. Rename modes or adjust the phase and verify both the initial and all transition states.
3. Re-run all 36 combinations after correction, recording actual accepted packet sequences, estimator widths, containment failures, per-step runtime distribution and generator count. Previous Run288 numerical widths/timings are **not validated for correctly named MMS/SMM modes**.
4. Do not use synthetic 12-state bounded-noise containment checks as evidence of the four-state mainline hard-safety/terminal-information-RCI gate. Continue toward measurement-conditioned SMF-to-Tube-MPC feedback and causal feasibility.
5. Merge PR #178 only after resolving divergence from main and obtaining relevant CI evidence. No CI or merge is asserted by this audit.

## Literature
No new paper was read for this static code audit; the unique paper reading ledger is unchanged. The existing literature on intermittent observation does not validate this schedule implementation.

## Next single priority
Implement and test an automaton-driven schedule in Run288, then rerun the 36-case stress benchmark with the corrected semantics and report any changed conclusions.
