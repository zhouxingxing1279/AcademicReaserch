# Run298 — generation/delivery contract and information-age bound

## Conditional analytic proposition
At each integer time a new observation is generated or absent. Assume (i) each length-(H+1) window contains a generated sample; (ii) **every generated** sample with timestamp s is delivered at s+d, 0<=d<=D; (iii) timestamps are authentic and the receiver retains the largest delivered timestamp. Let s*(k) be the largest received timestamp and a(k)=k-s*(k). For every k>=H+D, s*(k) exists and a(k)<=H+D.

Proof: window [k-D-H,k-D] contains a generated sample s>=k-D-H; its delivery is no later than s+D<=k. Hence s*(k)>=s and a(k)<=H+D. Works for all admissible paths including reordered deliveries. A latency bound only for packets that happen to arrive is insufficient.

Sharpness: generate at 0,H+1,2(H+1),... and delay each by D; at k=H+D the newest received timestamp can be 0, giving age H+D.

## Limits
An age bound alone does not prove observer contraction, CZ inclusion, Equalized Recovery or MPC feasibility. Two-position velocity recovery needs two distinct authentic timestamps and known applied inputs; the estimator must retain sufficient history and correctly account for delayed conditioning. This is an abstract measurement contract, **not** a certified repository-specific success/miss/delay automaton. No PX4/SITL work.

## Executable regression
Run `python experiments/run298_age_contract.py` (Python 3 standard library). Exhaustively enumerate N=9,H=2,D=2 generation schedules satisfying every sliding-window constraint and all 0..D delays: **239868** schedules; maximum post-transient age **4**; zero assertion failures. Finite-prefix cross-check only, not proof of all infinite paths. No random seeds or solver dependencies.

## Evidence and next task
Direct proof; not attributed to Scott/Rego/Hassaan without auditing their exact assumptions. Next unique task: freeze a machine-readable joint generation/delivery automaton with initial state and packet semantics, then certify reachable timestamp progress and cycles before CZ Equalized Recovery.
