"""12-state hover ZOH and conservative interval SMF demonstration (not Tube MPC)."""
import numpy as np
from scipy.linalg import expm

DT = 0.02
G = 9.81
A = np.zeros((12, 12))
B = np.zeros((12, 4))
for i in range(3):
    A[i, i+3] = 1.0
A[3, 7] = G
A[4, 6] = -G
for i in range(3):
    A[6+i, 9+i] = 1.0
B[5, 0] = 1.0  # delta thrust per unit mass
for i in range(3):
    B[9+i, 1+i] = 1.0  # torque per unit inertia
E = np.zeros((17, 17))
E[:12, :12] = A
E[:12, 12:16] = B
F = expm(E * DT)
AD, BD = F[:12, :12], F[:12, 12:16]

def rank(C):
    return np.linalg.matrix_rank(np.vstack([C @ np.linalg.matrix_power(AD, k) for k in range(12)]), tol=1e-8)

CP = np.eye(12)[[0,1,2]]
CPY = np.eye(12)[[0,1,2,8]]
assert rank(CP) == 10, rank(CP)
assert rank(CPY) == 12, rank(CPY)

rng = np.random.default_rng(285)
rad = np.array([.02]*3 + [.04]*3 + [.015]*3 + [.025]*3)
proc = np.array([.0002]*3 + [.001]*3 + [.0001]*3 + [.0005]*3)
meas = np.array([.01,.01,.01,.008])
center = np.zeros(12)
true = rng.uniform(-rad,rad)
max_width = 0.
for k in range(1,301):
    u = np.array([.1*np.sin(.02*k), .02*np.cos(.03*k), .015*np.sin(.04*k), .01*np.cos(.01*k)])
    w = rng.uniform(-proc,proc)
    true = AD @ true + BD @ u + w
    center = AD @ center + BD @ u
    rad = np.abs(AD) @ rad + proc
    # At every fifth step, allow at most two consecutive missed packets.
    if k % 5 == 0 and (k//5) % 3 != 2:
        y = true[[0,1,2,8]] + rng.uniform(-meas,meas)
        for j, idx in enumerate([0,1,2,8]):
            lo = max(center[idx]-rad[idx], y[j]-meas[j])
            hi = min(center[idx]+rad[idx], y[j]+meas[j])
            assert lo <= hi + 1e-12
            center[idx] = (lo+hi)/2
            rad[idx] = max(0.,(hi-lo)/2)
    assert np.all(np.abs(true-center) <= rad+1e-9), (k, true-center, rad)
    max_width = max(max_width,2*rad[0])
print('position-only rank',rank(CP),'position+yaw rank',rank(CPY))
print('300-step containment PASS; max x-width',round(max_width,6),'final x-width',round(2*rad[0],6))
print('final yaw-width',round(2*rad[8],6))
print('not a bound on all legal disturbances: Monte Carlo only')
