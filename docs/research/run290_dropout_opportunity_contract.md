# Run290 — measurement opportunity and dropout phase contract (2026-11-03)

## Scope and provenance
Base main `eb18e857090b0babe531c13c61aea944793af428`. Run289/PR #182 identified a labeling error in Run288/PR #178: code-labeled `mms` generated `SMS` (20/30 successes), code-labeled `smm` generated `MMS` (10/30 successes), and `all` meant success at each fifth-step opportunity (30/150), not each dynamics step. The Run288 script is **not on main** at the time of this audit, so this change does not pretend to patch or rerun it.

## Executable regression contract
`experiments/run290_dropout_opportunity_contract.py` defines explicit opportunity indices `5,10,...,150`, with the first pattern symbol anchored at the first opportunity, and no implicit state update on non-opportunity steps. Expected counts: `S=30`, `MMS=10`, `SMM=10`, `SMS=20`. Exhaustively checks all eight three-symbol patterns and first-three-opportunity phases. Local invocation: `python experiments/run290_dropout_opportunity_contract.py`. Local execution in Python succeeded: `PASS: 4 schedule counts, 2 phase anchors, cadence, 8 exhaustive 3-symbol patterns`.

## Critical limits
This is a **schedule-definition unit test**, not certification against the repository's formal finite-state dropout automaton. The latter's permitted initial state, phase transitions and any switching restrictions must be read and implemented before declaring the `MMS`/`SMM` trajectories legal. It does not execute Run288, prove zonotope state containment, or rerun the 36 configurations/5,400 steps. Prior Run288 numerical labels must not be reused as corrected MMS/SMM results. No new literature was read; the unique paper ledger is unchanged.

## Integration and next priority
When PR #178's implementation is accessible on a safe integration branch, replace ad hoc `mms`/`smm` booleans with an explicit automaton-validated opportunity trace; compare the generated trace with this phase regression and the formal automaton; rerun all 36 configurations with archived seeds and record widths, runtime and inclusion checks. Do not merge this branch if required CI or concurrent integration checks fail. Gate A remains blocked; neither an SMF-to-MPC interface nor robust terminal feasibility is established.
