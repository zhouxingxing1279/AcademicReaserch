"""Finite sums, certified tails, scaled sums and fixed-generator RPI LPs."""
import numpy as np
from .sets import ConstrainedZonotope as CZ, LPBuilder, linear_map, minkowski_sum


def finite_reach(F, D, N):
    n = F.shape[0]
    if N == 0:
        return CZ(np.zeros(n), np.zeros((n, 1)))
    terms, current = [], D.copy()
    for _ in range(N):
        terms.append(current); current = F@current
    return CZ(np.zeros(n), np.column_stack(terms))


def contractive_block(F):
    P = np.eye(len(F)); powers = []
    for m in range(1, 5001):
        powers.append(P.copy()); P = F@P
        alpha = np.linalg.norm(P, np.inf)
        if alpha < .8:
            base = np.column_stack(powers)
            return m, float(alpha), base
    raise ValueError('No stable block found')


def invariant_tail(F, D, tol=1e-7, max_steps=20000):
    """S_N + T_N is RPI, where T_N bounds every omitted tail disturbance.

    Let a=||F^m||inf<1 and B=sum_{j<m} F^j [-1,1]^n.
    F B +(1-a)[-1,1]^n subset B. If beta=||F^N D||inf,
    T_N=beta/(1-a) B satisfies F T_N + F^N D cube subset T_N.
    """
    n = len(F); m, alpha, base = contractive_block(F)
    factor = np.max(np.abs(base).sum(axis=1))/(1-alpha)
    terms, current = [], D.copy()
    for N in range(max_steps+1):
        beta = float(np.max(np.abs(current).sum(axis=1)))
        bound = beta*factor
        if N > 0 and bound <= tol:
            tail = base*(beta/(1-alpha))
            Z = CZ(np.zeros(n), np.column_stack(terms+[tail]))
            return Z, {'horizon': N, 'tail_bound_inf': bound, 'block_length': m,
                       'block_norm': alpha, 'tail_generators': tail,
                       'certificate': 'F*T + F^N*D*cube subset T; analytic norm bound'}
        terms.append(current); current = F@current
    raise ValueError('Tail tolerance not reached')


def rakovic_scaled(F, D, epsilon=5e-4):
    """Rakovic-style scaling with explicit tiny full-dimensional regularization.

    Rank-deficient Bw W fails F^s W subset alpha W in general. Enlarge by
    delta*unit_box and include its entire invariant contribution in error bound.
    A conservative box containment certificate avoids pretending the singular
    disturbance set is full dimensional.
    """
    n = len(F); m, a, base = contractive_block(F)
    factor = np.max(abs(base).sum(axis=1))/(1-a)
    delta = epsilon/(8*factor)
    Dreg = np.c_[D, delta*np.eye(n)]
    terms, current = [], Dreg.copy()
    sums = np.zeros(n)
    for N in range(1, 20001):
        terms.append(current); sums += np.abs(current).sum(axis=1)
        current = F@current
        alpha = float(np.max(np.abs(current).sum(axis=1))/delta)
        if alpha < 1 and alpha/(1-alpha)*max(sums) <= epsilon/2:
            Z = CZ(np.zeros(n), np.column_stack(terms)/(1-alpha))
            return Z, {'horizon': N, 'alpha': alpha, 'regularization': delta,
                       'regularization_error_inf': delta*factor,
                       'scaling_error_inf': alpha/(1-alpha)*max(sums),
                       'total_error_inf_bound': delta*factor+alpha/(1-alpha)*max(sums),
                       'certificate': 'F^N Wreg subset alpha Wreg; scaled finite sum RPI'}
    raise ValueError('Scaled construction did not reach target')


def eigenbasis(F):
    values, P = np.linalg.eig(F)
    if np.max(abs(values.imag)) > 1e-8 or np.max(abs(P.imag)) > 1e-8:
        raise ValueError('Real diagonalizable benchmark required for this baseline')
    P = P.real
    if np.linalg.cond(P) > 1e8:
        raise ValueError('Eigenbasis ill-conditioned')
    return P


def iterative_rpi(F, D, tol=1e-9):
    """Monotone fixed-basis zonotope iteration with an explicit residual tail."""
    P = eigenbasis(F); inverse = np.linalg.inv(P)
    M, d = np.abs(inverse@F@P), np.abs(inverse@D).sum(axis=1)
    if max(abs(np.linalg.eigvals(M))) >= 1:
        raise ValueError('Selected template is not contractive')
    r = np.zeros(len(F))
    for i in range(20000):
        nxt = M@r+d
        if max(abs(nxt-r)) <= tol:
            correction = np.linalg.solve(np.eye(len(F))-M, nxt-r)
            radius = r+correction
            Z = CZ(np.zeros(len(F)), P@np.diag(radius))
            residual = float(max(M@radius+d-radius))
            return Z, {'iterations': i+1, 'certificate_residual': residual,
                       'certificate': 'coordinate box inclusion |P^-1 F P|r+|P^-1 D|1<=r'}
        r = nxt
    raise ValueError('Iteration did not converge')


def one_step_rpi(F, D, G=None):
    """Raghuraman–Koeln Theorem 23 for centered disturbance, fixed directions."""
    n, p = D.shape
    if G is None:
        G = np.c_[eigenbasis(F), D, F@D] if n <= 4 else eigenbasis(F)
    G = G/np.maximum(np.linalg.norm(G, axis=0), 1e-12)
    g = G.shape[1]; mdl = LPBuilder()
    phi = mdl.var((g,), (1e-10, None), cost=1.)
    gamma1 = mdl.var((g, g)); gamma2 = mdl.var((g, p))
    a1 = mdl.var((g, g), (0., None)); a2 = mdl.var((g, p), (0., None))
    FG = F@G
    for i in range(n):
        for j in range(g):
            mdl.row([(gamma1[:, j], G[i]), (phi[j], -FG[i, j])])
        for j in range(p):
            mdl.row([(gamma2[:, j], G[i])], D[i, j])
    for i in range(g):
        for gamma, ab in ((gamma1, a1), (gamma2, a2)):
            for j in range(gamma.shape[1]):
                mdl.row([(gamma[i, j], 1.), (ab[i, j], -1.)], equal=False)
                mdl.row([(gamma[i, j], -1.), (ab[i, j], -1.)], equal=False)
        mdl.row([(a1[i], 1.), (a2[i], 1.), (phi[i], -1.)], equal=False)
    r = mdl.solve()
    if not r.success:
        raise ValueError('One-step RPI LP uncertified: '+r.message)
    ph, g1, g2 = r.x[phi], r.x[gamma1], r.x[gamma2]
    res = max(np.max(abs(FG*ph-G@g1)), np.max(abs(D-G@g2)),
              np.max(abs(g1).sum(axis=1)+abs(g2).sum(axis=1)-ph))
    if res > 2e-7:
        raise ValueError('One-step certificate residual failed')
    return CZ(np.zeros(n), G*ph), {'certificate_residual': float(res),
                                   'variables': len(mdl.bounds), 'Gamma1': g1, 'Gamma2': g2,
                                   'phi': ph, 'directions': G,
                                   'certificate': 'Theorem 23 fixed-generator row-absolute-sum inclusion'}


def rpi_direction_residual(F, D, Z, Q):
    return Z.support_many(Q@F)+np.abs(Q@D).sum(axis=1)-Z.support_many(Q)
