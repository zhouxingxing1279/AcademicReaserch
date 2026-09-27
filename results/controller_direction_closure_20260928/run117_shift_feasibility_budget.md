# Run 117 — horizon-wise support-loss budget for shifted feasibility

Base: Run 116 commit 93ab78a406bf9d2944917cde90f287c9d848b525.

## Core result

Let the ancillary error dynamics be e^+=F e+w and let C_k be the unreduced current error/estimation set while R_k is a safe outer reduction, C_k subset R_k. With the same future disturbance sets W_0,..., define
E_i(C)=F^i C + sum_{t=0}^{i-1} F^{i-1-t} W_t,
E_i(R)=F^i R + sum_{t=0}^{i-1} F^{i-1-t} W_t.
For every direction q,
delta_i(q):=h_{E_i(R)}(q)-h_{E_i(C)}(q)
=h_R((F^i)^T q)-h_C((F^i)^T q) >= 0.
Thus future common disturbances cancel exactly from the support-loss budget.

For state half-space a_l^T x <= b_l, a nominal point z_i feasible under C obeys
a_l^T z_i + h_{E_i(C)}(a_l) <= b_l.
Define its old robust slack
s^x_{i,l}=b_l-a_l^T z_i-h_{E_i(C)}(a_l).
The SAME shifted nominal point remains feasible after replacing C by R iff
delta_i(a_l) <= s^x_{i,l}.
For input half-space d_m^T u <= g_m and ancillary law u=v+K e, define
s^u_{i,m}=g_m-d_m^T v_i-h_{E_i(C)}(K^T d_m).
The same shifted input remains feasible if
delta_i(K^T d_m) <= s^u_{i,m}.
These inequalities are sufficient direction-wise certificates for preserving the standard shifted candidate. They do not prove recursive feasibility if the terminal ingredient is changed; terminal facets need the same check or an invariant terminal construction compatible with R.

## Counterexample: nesting alone is insufficient

X=[-1,1], old error tube E=[-0.2,0.2], reduced outer tube R=[-0.3,0.3], nominal z=0.75. Although E subset R, old robust feasibility is 0.75+0.2=0.95<=1 with slack 0.05. The support loss is 0.1>0.05, so the same shifted candidate violates the new tightened constraint: 0.75+0.3=1.05>1.

Therefore C subset R subset P_old is NOT sufficient by itself to preserve shifted feasibility. The missing quantity is available robust slack in the controller-relevant propagated directions.

## Literature boundary

Mayne, Seron, Rakovic (2005), "Robust model predictive control of constrained linear systems with bounded disturbances", Automatica 41(2), 219-224, DOI 10.1016/j.automatica.2004.08.019: tube tightening and shifted recursive-feasibility framework; not our novelty.

Mayne, Rakovic, Findeisen, Allgower (2006), "Robust output feedback model predictive control of constrained linear systems", Automatica 42(7), 1217-1222, DOI 10.1016/j.automatica.2006.03.005: estimator-error bounds coupled to tube tightening and robust constraint satisfaction.

Koehler, Koetting, Soloperto, Allgower, Mueller (2021), "A robust adaptive model predictive control framework for nonlinear uncertain systems", IEEE TAC: set-membership uncertainty updates with monotonic/non-increasing compatibility conditions to preserve recursive feasibility. This is close prior art; our candidate contribution must be narrower: controller-direction support-loss certificates for representation reduction, not merely online shrinking uncertainty.

## Status

PROVED under linear ancillary dynamics, common future disturbance sets, unchanged K/model/nominal shifted candidate: exact support-loss propagation and facet-wise slack certificate.
COUNTEREXAMPLE: set nesting alone does not preserve feasibility of the shifted candidate.
OPEN: terminal-set compatibility and time-varying center/model/update effects.
NUMERICAL: the scalar counterexample is exact arithmetic, intended as a falsification test rather than a performance simulation.

## Next unique priority

Apply the certificate to the frozen Run-114/116 workload: reconstruct the actual old shifted nominal plan/slacks (or, if not persisted, add a reproducible MPC solve), compute delta_i in every active state/input facet over the horizon after deleting each measurement row, and determine whether either deletion is admissible without re-optimization. Do not claim recursive feasibility until terminal compatibility is checked.
