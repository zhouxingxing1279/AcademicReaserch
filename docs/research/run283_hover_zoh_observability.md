# Run283 — 12-state hover ZOH observability and no-measurement interval-growth audit

Date: 2026-11-03 UTC. Base main: `9375b7d32de20233574e602ba762d889eeab8d98`.

## Scope and assumptions
This is a reproducible **linearized hover structural audit**, not a complete quadrotor SMF, Tube MPC, nonlinear safety or recursive-feasibility result. State ordering:
`x=[p_x,p_y,p_z,v_x,v_y,v_z,phi,theta,psi,omega_x,omega_y,omega_z]`.
Nominal hover has yaw=0, level attitude, zero angular rates and thrust mg. Input deviations are normalized `[deltaT/m,tau_x/Jx,tau_y/Jy,tau_z/Jz]`, **not actual motor commands**. Euler-angle small-perturbation linearization:
`p_dot=v; v_x_dot=g theta; v_y_dot=-g phi; v_z_dot=deltaT/m; angles_dot=omega; omega_dot=normalized_torque`.
Set `g=9.81m/s²`, `h=0.02s`. Exact ZOH `[Ad Bd;0 I]=expm(h*[A B;0 0])`.

## Verified structural result
For `C_p=[I3 0]` (only 3D position), the 12-block discrete observability matrix `O=[C; C Ad; ...; C Ad^11]` has rank **10**, with exactly zero columns at zero-based indices 8 (yaw) and 11 (yaw rate). For `C_{p,psi}` adding a direct yaw-angle output, rank is **12** under these idealized assumptions. The rank computation rescales nonzero columns to avoid unit-dependent numerical threshold artifacts. Nonzero gravitational coupling and positive sample interval are essential.

These statements are about the frozen linearized pair and measurement configuration only. They do **not** imply reliable estimation with arbitrary missing measurements, bounded estimation error, real-world sensor accessibility, or nonlinear observability. Actual IMU gyros may provide yaw rate even when absolute yaw is not measured.

## Exact ZOH checks
`Ad[p_x,v_x]=h`, `Ad[p_x,theta]=g*h²/2`, `Ad[p_x,omega_y]=g*h³/6`. These are distinct from forward-Euler discretization and affect set propagation.

## Open-loop interval growth, illustrative only
Use initial symmetric box halfwidths `[0.02]*3+[0.05]*3+[0.01]*3+[0.02]*3`; per-step additive halfwidths `[0]*3+[0.002]*3+[0.0001]*3+[0.0005]*3`, in respective state units. With **no measurements and no corrective posterior intersection**, propagate the reliable (possibly conservative) box via `r_{k+1}=abs(Ad) r_k + q`. Results below are full interval widths, not errors measured from trajectories:

| k | seconds | x-position full width (m) | x-velocity full width (m/s) | yaw full width (rad) |
|---:|---:|---:|---:|---:|
| 1 | 0.02 | 0.04203976 | 0.10800248 | 0.021 |
| 5 | 0.10 | 0.05185948 | 0.14203326 | 0.0252 |
| 10 | 0.20 | 0.06818552 | 0.18941297 | 0.0309 |
| 25 | 0.50 | 0.14979996 | 0.3685358 | 0.051 |
| 50 | 1.00 | 0.43699095 | 0.81978285 | 0.0945 |

The process boxes are **illustrative, not calibrated to the repository's frozen disturbances**. The interval formula assumes the actual linearized dynamics and disturbances lie in the declared sets; otherwise containment is not certified. Missing observations for 50 consecutive steps are **not** asserted legal under the existing repository's missing-packet automaton. These values are a diagnostic of prediction-only growth, not a bound on the full posterior under the legal success/miss schedule.

## Reproduction
The following minimal script reproduces the observability and propagation numbers; it needs NumPy and SciPy. Save as `run283_hover_zoh.py` and run `python run283_hover_zoh.py`.

```python
import numpy as np
from scipy.linalg import expm
g,h=9.81,.02
A=np.zeros((12,12)); B=np.zeros((12,4))
A[:3,3:6]=np.eye(3)
A[3,7]=g; A[4,6]=-g
A[6:9,9:12]=np.eye(3)
B[5,0]=B[9,1]=B[10,2]=B[11,3]=1.
M=np.zeros((16,16)); M[:12,:12]=A; M[:12,12:]=B
E=expm(h*M); Ad=E[:12,:12]; Bd=E[:12,12:]
Cp=np.zeros((3,12)); Cp[:3,:3]=np.eye(3)
Cy=np.zeros((4,12)); Cy[:3,:3]=np.eye(3); Cy[3,8]=1
def obs_rank(C):
    O=np.vstack([C@np.linalg.matrix_power(Ad,k) for k in range(12)])
    norms=np.linalg.norm(O,axis=0); nz=norms>1e-12
    return np.linalg.matrix_rank(O[:,nz]/norms[nz],tol=1e-8), np.where(~nz)[0].tolist()
assert obs_rank(Cp)==(10,[8,11])
assert obs_rank(Cy)==(12,[])
assert np.isclose(Ad[0,7],g*h*h/2)
assert np.isclose(Ad[0,10],g*h**3/6)
r=np.array([.02]*3+[.05]*3+[.01]*3+[.02]*3)
q=np.array([0.]*3+[.002]*3+[.0001]*3+[.0005]*3)
for k in range(1,51):
    r=np.abs(Ad)@r+q
    if k in (1,5,10,25,50):
        print(k,round(2*r[0],8),round(2*r[3],8),round(2*r[8],8))
```

## Research interpretation and next gate
Position-only sensing leaves yaw and yaw rate structurally unobservable at this hover equilibrium. A physically grounded measurement contract should include IMU angular rates and an independently justified heading reference or a declared unobservable-yaw safety specification; adding `psi` as a mathematically convenient measurement is not proof of sensor availability. Reconcile the main project's four-state negative certificates with the user-selected 12-state simulation plant without claiming that either transfers automatically.

**Next single priority:** freeze physically accessible outputs, measurement rates, noise/disturbance bounds and legal dropout automaton for the 12-state plant, then build a measurement-conditioned SMF outer approximation and test true-state containment over all declared observation patterns. Only then attempt output-feedback Tube tightening and terminal viability.

## Literature
No new paper was read in this run. The existing `docs/literature/PAPER_READING_LOG.md` remains the unique ledger and is intentionally unchanged. Related prior verified repository records include Elokda et al. (2021), DOI https://doi.org/10.1002/rnc.5686, and Yan, Cannon & Goulart (2022), DOI https://doi.org/10.1016/j.automatica.2022.110282; neither proves this deterministic 12-state claim.
