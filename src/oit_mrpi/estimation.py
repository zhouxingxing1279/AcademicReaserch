"""Observable window reconstructions and correctly timed joint observer errors."""
import numpy as np
from .sets import (ConstrainedZonotope as CZ, HPolytope, box, linear_map,
                   generalized_intersection, minkowski_sum, outer_reduce)
from .rpi import invariant_tail, finite_reach


def measure(Z, C, y, noise):
    y = np.atleast_1d(y)
    return generalized_intersection(Z, C, box(y-noise, y+noise))


class ConstantBiasLearner:
    """Nested identification for q_k=b+e_k, fixed b, bounded e_k.

    An observed disturbance interval refers to q_k. Removing the bounded
    residual gives a constraint on the SAME b at every time. No such inference
    is allowed for unrelated arbitrary q_k.
    """
    def __init__(self, low, high, residual):
        self.low, self.high, self.residual = low, high, residual

    def update(self, observed_low, observed_high):
        self.low = max(self.low, observed_low-self.residual)
        self.high = min(self.high, observed_high+self.residual)
        if self.low > self.high:
            raise ValueError('Constant-bias model inconsistent with data')
        return self.low-self.residual, self.high+self.residual


def window_estimate(A, B, C, ys, us, amplitude, noise):
    """Exact 2D trajectory-consistency CZ with unrestricted oldest state.

    Eliminate the initial state using two distinct position measurements.
    This is the observable unrestricted-prior option of Algorithm 3, not the
    looser intersection of individually propagated OIT strips.
    """
    from src.outerloop.finite_memory import Contract, pair_window
    delta = len(ys)-1
    if delta < 1 or A.shape != (2, 2) or not np.allclose(C, [[1., 0.]]):
        raise ValueError('This exact elimination implements the double integrator')
    dt = float(A[0, 1])
    if not np.allclose(B.reshape(-1), [dt*dt/2, dt]):
        raise ValueError('Input and disturbance must use ZOH double-integrator channel')
    c = Contract(T=dt, acceleration=amplitude, noise=noise,
                 missing=0, delay=delta-1)
    zz = pair_window(c, delta, dict(enumerate(ys)), dict(enumerate(us)), True)
    return CZ(zz.center, zz.generators, zz.equalities, zz.rhs)


def literal_oit(A, B, C, ys, us, amplitude, noise):
    """Literal intersection of propagated single-measurement information sets."""
    delta = len(ys)-1; H, h = [], []
    for i in range(delta+1):
        j = delta-i
        normal = (C@np.linalg.matrix_power(np.linalg.inv(A), j)).ravel()
        center, radius = float(ys[i]), noise
        for r in range(j):
            coefficient = float((C@np.linalg.matrix_power(np.linalg.inv(A), r+1)@B).item())
            center += coefficient*us[i+r]
            radius += abs(coefficient)*amplitude
        H.extend([normal, -normal]); h.extend([center+radius, -center+radius])
    return HPolytope(np.array(H), np.array(h))


class JointObserver:
    """eta=(epsilon,d), with posterior observer update at k+1.

    r=y+ - C(A hat_x+B u), epsilon+=(I-LC)(A epsilon+Bw w)-L v,
    d+=(A+BK)d+L r. Same w,v variables are used in both rows.
    """
    def __init__(self, system, K, L, amplitude=.05, noise=.10, tail_tol=1e-8):
        self.sys, self.K, self.L = system, K, L
        A, B, Bw, C = system.A, system.B, system.Bw, system.C
        n = len(A); I = np.eye(n)
        self.F = np.block([[(I-L@C)@A, np.zeros((n, n))], [L@C@A, A+B@K]])
        self.D = np.block([[(I-L@C)@Bw*amplitude, -L*noise],
                           [L@C@Bw*amplitude, L*noise]])
        self.Hinnovation = np.c_[C@A, np.zeros((len(C), n))]
        self.noise_innovation = np.c_[C@Bw*amplitude, np.eye(len(C))*noise]
        self.Tx = np.c_[I, I]; self.Tu = np.c_[np.zeros((len(K), n)), K]
        self.Hd = np.c_[np.zeros((n, n)), I]
        self.S, self.tail = invariant_tail(self.F, self.D, tail_tol)

    def initial(self, d, ordinary=False):
        if ordinary:
            G, H = self.S.G, self.Hd
            gain = G@G.T@H.T@np.linalg.pinv(H@G@G.T@H.T)
            return CZ(gain@d, (np.eye(len(self.F))-gain@H)@G)
        return self.S.slice(self.Hd, d)

    def update(self, Z, innovation, ordinary=False):
        p = self.D.shape[1]
        c = self.F@Z.c
        G = np.c_[self.F@Z.G, self.D]
        row = np.c_[self.Hinnovation@Z.G, self.noise_innovation]
        rhs = np.atleast_1d(innovation)-self.Hinnovation@Z.c
        if ordinary:
            gain = G@row.T@np.linalg.pinv(row@row.T)
            return CZ(c+gain@rhs, G-gain@row)
        eq = np.vstack([np.c_[Z.Aeq, np.zeros((len(Z.beq), p))], row])
        return CZ(c, G, eq, np.r_[Z.beq, rhs])

    def window(self, innovations, d_history, count, ordinary=False):
        k = len(innovations); start = max(0, k-count)
        Z = self.initial(d_history[start], ordinary)
        for r in innovations[start:]:
            Z = self.update(Z, r, ordinary)
        return Z

    def predict(self, Z, steps):
        return minkowski_sum(linear_map(np.linalg.matrix_power(self.F, steps), Z),
                             finite_reach(self.F, self.D, steps))

    def compatible_tube(self, innovations, d_history, window, horizon):
        """Forget one past innovation at each prediction step; RPI after window.

        P_i=F^i J_k^(window-i)+reach_i for i<window, P_i=S otherwise.
        New P_i is contained in old P_(i+1) for every possible innovation,
        because both use the same oldest boundary and new data only condition.
        No future observation is predicted as if already known.
        """
        return [self.predict(self.window(innovations, d_history, window-i), i)
                if i < window else self.S for i in range(horizon+1)]
