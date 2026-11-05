"""Fixed and compatible finite-memory output-feedback tube MPC."""
import time
import numpy as np
import scipy.sparse as sp
from scipy.linalg import solve_discrete_are, solve_discrete_lyapunov
from scipy.optimize import linprog
import osqp
from .sets import LinearSystem, HPolytope
from .estimation import JointObserver


def double_integrator():
    return LinearSystem(np.array([[1., 1.], [0., 1.]]),
                        np.array([[.5], [1.]]), np.array([[.5], [1.]]),
                        np.array([[1., 0.]]))


def lqr(A, B):
    P = solve_discrete_are(A, B, np.eye(len(A)), .1*np.eye(B.shape[1]))
    return -np.linalg.solve(.1*np.eye(B.shape[1])+B.T@P@B, B.T@P@A)


def terminal_polytope(F, H, h):
    """Maximal admissible fixed-feedback nominal set, with redundancy stopping."""
    HH, hh = H.copy(), h.copy()
    for depth in range(101):
        added = []
        for row, bound in zip(HH@F, hh):
            r = linprog(-row, A_ub=HH, b_ub=hh, bounds=[(None, None)]*len(F), method='highs')
            if not r.success:
                raise ValueError('Terminal set unresolved')
            if -r.fun > bound+1e-9:
                added.append((row, bound))
        if not added:
            return HPolytope(HH, hh), depth
        HH = np.vstack([HH, [a[0] for a in added]])
        hh = np.r_[hh, [a[1] for a in added]]
    raise ValueError('Terminal closure not reached')


class TubeMPC:
    def __init__(self, horizon=15, window=3):
        self.sys = double_integrator(); A, B = self.sys.A, self.sys.B
        self.K = lqr(A, B); self.L = np.array([[.7075], [.1925]])
        self.joint = JointObserver(self.sys, self.K, self.L)
        self.N, self.window = horizon, window
        if window > horizon:
            raise ValueError('Prediction horizon must reach invariant tail')
        self.Hx = np.vstack([np.eye(2), -np.eye(2)]); self.hx = np.array([5., 3., 5., 3.])
        self.Hu = np.array([[1.], [-1.]]); self.hu = np.ones(2)
        self.Qdir = np.vstack([self.Hx@self.joint.Tx, self.Hu@self.joint.Tu])
        self.static = self.joint.S.support_many(self.Qdir)
        H = np.vstack([self.Hx, self.Hu@self.K]); h = np.r_[self.hx, self.hu]-self.static
        self.terminal, self.terminal_depth = terminal_polytope(A+B@self.K, H, h)
        self.P = solve_discrete_lyapunov((A+B@self.K).T, np.eye(2)+.1*self.K.T@self.K)
        N = horizon
        self.Phi = np.vstack([np.linalg.matrix_power(A, i+1) for i in range(N)])
        self.Gamma = np.zeros((2*N, N))
        for i in range(N):
            for j in range(i+1):
                self.Gamma[2*i:2*i+2, j] = (np.linalg.matrix_power(A, i-j)@B).ravel()
        Q = sp.block_diag([np.eye(2)]*(N-1)+[self.P]).toarray()
        Hess = 2*(.1*np.eye(N)+self.Gamma.T@Q@self.Gamma)
        self.qmap = 2*self.Gamma.T@Q@self.Phi
        self.optmap = -np.linalg.solve(Hess, self.qmap)
        self.Umat = np.vstack([np.eye(N), -np.eye(N)])
        self.Xmat = np.kron(np.eye(N), self.Hx)@self.Gamma
        self.Xmap = np.kron(np.eye(N), self.Hx)@self.Phi
        self.Tmat = self.terminal.H@self.Gamma[-2:]
        self.Tmap = self.terminal.H@self.Phi[-2:]
        self.constraint = np.vstack([self.Umat, self.Xmat, self.Tmat])
        self.solver = osqp.OSQP()
        self.solver.setup(P=sp.csc_matrix(np.triu(Hess)), q=np.zeros(N),
                          A=sp.csc_matrix(self.constraint),
                          l=np.full(len(self.constraint), -np.inf),
                          u=np.ones(len(self.constraint)), verbose=False,
                          eps_abs=1e-8, eps_rel=1e-8, max_iter=10000, polishing=False)

    def margins(self, innovations, ds, adaptive):
        start = time.perf_counter()
        if not adaptive:
            return np.tile(self.static, (self.N+1, 1)), None, 0.
        if adaptive=='known_d':
            initial=self.joint.initial(ds[-1])
            tube=[initial]+[self.joint.S]*self.N
            margins=np.tile(self.static,(self.N+1,1))
            margins[0]=initial.support_many(self.Qdir)
            return margins,tube,time.perf_counter()-start
        tube = self.joint.compatible_tube(innovations, ds, self.window, self.N)
        margins = np.tile(self.static, (self.N+1, 1))
        for i in range(self.window):
            margins[i] = tube[i].support_many(self.Qdir)
        return margins, tube, time.perf_counter()-start

    def bounds(self, z, margins):
        u = np.r_[1-margins[:-1, 4], 1-margins[:-1, 5]]
        x = (self.hx[None, :]-margins[1:, :4]).ravel()-self.Xmap@z
        return np.r_[u, x, self.terminal.h-self.Tmap@z]

    def feasible(self, z, sequence, margins, tol=2e-6):
        residual = max(np.max(self.constraint@sequence-self.bounds(z, margins)),
                       np.max(self.Hx@z+margins[0, :4]-self.hx))
        return bool(residual <= tol), float(residual)

    def solve(self, z, margins):
        unconstrained = self.optmap@z
        ok, residual = self.feasible(z, unconstrained, margins, 2e-8)
        if ok:
            return unconstrained, 'exact_unconstrained', residual
        if np.max(self.Hx@z+margins[0, :4]-self.hx) > 2e-6:
            return None, 'initial_infeasible', np.inf
        self.solver.update(q=self.qmap@z, u=self.bounds(z, margins))
        result = self.solver.solve(raise_error=False)
        if result.info.status != 'solved':
            return None, result.info.status, np.inf
        ok, residual = self.feasible(z, result.x, margins)
        return (result.x.copy() if ok else None), result.info.status, residual

    def shifted(self, z, sequence):
        end = (self.Phi@z+self.Gamma@sequence)[-2:]
        return np.r_[sequence[1:], (self.K@end).item()]

    def cost(self, z, sequence):
        result = 0.
        for v in sequence:
            result += z@z+.1*v*v
            z = self.sys.A@z+self.sys.B.ravel()*v
        return float(result+z@self.P@z)
