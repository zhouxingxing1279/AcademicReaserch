"""Output-feedback tube baseline with a nilpotent auxiliary controller.

This conservative construction closes a mathematical benchmark; it is not a
quadrotor/PX4 model or a formal floating-point safety implementation.
"""
from dataclasses import dataclass
from itertools import product
import numpy as np
import scipy.sparse as sp
import osqp


@dataclass
class TubeDesign:
    contract: object
    state_limits: tuple = (3., 2.)
    input_limit: float = 4.

    def __post_init__(self):
        c = self.contract
        self.A, self.B = c.matrices()
        self.K = np.array([-1/c.T**2, -1.5/c.T])
        self.F = self.A+np.outer(self.B, self.K)
        assert np.max(np.abs(self.F@self.F)) < 1e-12
        self.E = c.uniform_error()
        self.delta = c.acceleration+np.abs(self.K)@self.E
        self.S = np.column_stack([self.B, self.F@self.B])*self.delta
        self.state_margin = np.abs(self.S).sum(axis=1)
        self.input_margin = np.abs(self.K@self.S).sum()+np.abs(self.K)@self.E
        self.z_limit = np.array(self.state_limits)-self.state_margin
        self.v_limit = self.input_limit-self.input_margin
        if np.any(self.z_limit <= 0) or self.v_limit <= 0:
            raise ValueError('Conservative tube exhausts nominal constraint budget')
        self.Q, self.R = np.diag([4., 1.]), 0.2
        stage = self.Q+self.R*np.outer(self.K, self.K)
        self.P = stage+self.F.T@stage@self.F
        base = np.vstack([np.eye(2), -np.eye(2), self.K, -self.K])
        budget = np.r_[self.z_limit, self.z_limit, self.v_limit, self.v_limit]
        self.Hf, self.hf = np.vstack([base, base@self.F]), np.r_[budget, budget]
        for signs in product([-1, 1], repeat=2):
            point = np.array(signs)*[c.initial_p, c.initial_v]
            if not self.in_tube(point):
                raise ValueError('Initial prior is not admitted to tracking tube')

    def in_tube(self, error, tolerance=1e-7):
        if self.delta == 0:
            return bool(np.max(np.abs(error)) <= tolerance)
        return bool(np.max(np.abs(np.linalg.solve(self.S, error))) <= 1+tolerance)

    def terminal_contains(self, z, tolerance=1e-7):
        return bool(np.max(self.Hf@z-self.hf) <= tolerance)


class NominalMPC:
    def __init__(self, design, horizon=12):
        self.d, self.N = design, horizon
        A, B, N = design.A, design.B, horizon
        self.Phi = np.vstack([np.linalg.matrix_power(A, i+1) for i in range(N)])
        self.Gamma = np.zeros((2*N, N))
        for i in range(N):
            for j in range(i+1):
                self.Gamma[2*i:2*i+2, j] = np.linalg.matrix_power(A, i-j)@B
        W = sp.block_diag([design.Q]*(N-1)+[design.P]).toarray()
        H = 2*(design.R*np.eye(N)+self.Gamma.T@W@self.Gamma)
        self.linear = 2*self.Gamma.T@W@self.Phi
        self.constraint = np.vstack([np.eye(N), self.Gamma, design.Hf@self.Gamma[-2:]])
        self.solver = osqp.OSQP()
        low, high = self.bounds(np.zeros(2))
        self.solver.setup(P=sp.csc_matrix(np.triu(H)), q=np.zeros(N),
                          A=sp.csc_matrix(self.constraint), l=low, u=high,
                          verbose=False, eps_abs=1e-8, eps_rel=1e-8,
                          max_iter=20000, polishing=False)

    def bounds(self, z):
        d, N = self.d, self.N
        pred = self.Phi@z
        limit = np.tile(d.z_limit, N)
        return (np.r_[-np.full(N, d.v_limit), -limit-pred, np.full(len(d.hf), -np.inf)],
                np.r_[np.full(N, d.v_limit), limit-pred, d.hf-d.Hf@pred[-2:]])

    def violation(self, z, sequence):
        low, high = self.bounds(z)
        value = self.constraint@sequence
        return max(float(np.max(value-high)), float(np.max(low-value)),
                   float(np.max(np.abs(z)-self.d.z_limit)))

    def solve(self, z):
        low, high = self.bounds(z)
        if np.any(np.abs(z) > self.d.z_limit+1e-7):
            raise RuntimeError('Initial nominal state violates tightened constraints')
        self.solver.update(q=self.linear@z, l=low, u=high)
        result = self.solver.solve(raise_error=False)
        if result.info.status != 'solved':
            raise RuntimeError('Nominal QP unresolved: '+result.info.status)
        if self.violation(z, result.x) > 2e-6:
            raise RuntimeError('Nominal QP residual fails independent check')
        return result.x.copy()

    def shifted(self, z, sequence):
        terminal = (self.Phi@z+self.Gamma@sequence)[-2:]
        return np.r_[sequence[1:], self.d.K@terminal]

    def cost(self, z, sequence):
        value = 0.
        for u in sequence:
            value += z@self.d.Q@z+self.d.R*u*u
            z = self.d.A@z+self.d.B*u
        return float(value+z@self.d.P@z)
