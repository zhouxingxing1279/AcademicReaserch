# Run292 — dropout phase regression (2026-11-03)

## Scope and source
Checked main commit `eb18e857090b0babe531c13c61aea944793af428`. Both `experiments/run288_multiseed_zonotope_stress.py` and `experiments/run290_dropout_opportunity_contract.py` returned 404 on main. Read Run288 source from branch `research/run288-multiseed-zonotope-stress`; its `mms` and `smm` labels do not match the generated opportunity sequences. This commit adds an independent, dependency-free regression, **not** an integrated SMF benchmark or certification against the formal dropout automaton.

## Exact contract
Dynamics steps start at 1. Measurement opportunities occur at steps 5,10,...,150 (30 opportunities). The first character of a pattern applies at step 5; S=success, M=miss. Pattern `all` means all **opportunities** succeed, not all dynamics steps. Pattern names are uppercase to distinguish from the earlier mislabelled code.

## Reproduction and result
Command: `python experiments/run292_schedule_regression.py`. Executed locally with Python 3, standard library only; PASS. Counts: all=30/30, MMS=10/30, SMM=10/30, SMS=20/30. First six opportunity symbols respectively SSSSSS, MMSMMS, SMMSMM, SMSSMS. All non-opportunity steps assert no measurement. Negative result retained: no numerical SMF stress rerun and no CI evidence from this run.

## Evidence limits and next gate
This regression verifies a **specified schedule convention** only. The repository's authoritative dropout automaton (states, transitions, initialization and allowed patterns) must be located and matched before any claim of admissibility. Run288 also requires integration into main and rerunning 36 cases with corrected schedules. No full-text paper was newly read; do not update the literature ledger merely for this test. No 12-state MPC closed loop, physical disturbance contract, recursive feasibility or robust safety proof is established. Gate A remains blocked.
