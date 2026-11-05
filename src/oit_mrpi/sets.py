"""Exact set identities with numerical LPs; no formal floating-point certificate.

Containment is deliberately tri-state: an infeasible sufficient lifting LP does
not establish noncontainment. Finite direction checks are diagnostics only.
"""
from dataclasses import dataclass
from itertools import combinations
import numpy as np
from scipy.optimize import linprog
from scipy.linalg import block_diag
from scipy.spatial import ConvexHull


@dataclass
class LinearSystem:
    A: np.ndarray
    B: np.ndarray
    Bw: np.ndarray
    C: np.ndarray


@dataclass
class MPCConfig:
    K: np.ndarray
    Q: np.ndarray
    R: np.ndarray
    N: int
    X: object
    U: object
    Xf: object = None
    oit_window: int = 3
    max_generators: int = 64
    reduction_method: str = 'fixed_basis_box'


@dataclass
class ConstrainedZonotope:
    c: np.ndarray
    G: np.ndarray
    Aeq: np.ndarray = None
    beq: np.ndarray = None

    def __post_init__(self):
        self.c = np.asarray(self.c, dtype=float).reshape(-1)
        self.G = np.asarray(self.G, dtype=float).reshape(len(self.c), -1)
        self.Aeq = (np.empty((0, self.g)) if self.Aeq is None
                    else np.asarray(self.Aeq, dtype=float).reshape(-1, self.g))
        self.beq = np.empty(0) if self.beq is None else np.asarray(self.beq, dtype=float).reshape(-1)
        if len(self.beq) != len(self.Aeq):
            raise ValueError('Equality dimensions disagree')

    @property
    def g(self):
        return self.G.shape[1]

    @property
    def n(self):
        return len(self.c)

    def lp(self, obj, extra=None, rhs=None):
        eq, b = self.Aeq, self.beq
        if extra is not None:
            eq, b = np.vstack([eq, extra]), np.r_[b, rhs]
        result = linprog(obj, A_eq=eq if len(eq) else None,
                         b_eq=b if len(eq) else None, bounds=[(-1., 1.)]*self.g,
                         method='highs')
        return result

    def support(self, q):
        q = np.asarray(q)
        if len(self.beq) == 0:
            return float(q@self.c+np.abs(q@self.G).sum())
        r = self.lp(-(q@self.G))
        if not r.success:
            raise ValueError('CZ support unresolved/empty: '+r.message)
        return float(q@self.c-r.fun)

    def support_many(self, Q):
        Q = np.atleast_2d(Q)
        if not len(self.beq):
            return Q@self.c+np.abs(Q@self.G).sum(axis=1)
        return np.array([self.support(q) for q in Q])

    def point_contains(self, x, tol=2e-7):
        r = self.lp(np.zeros(self.g), self.G, np.asarray(x)-self.c)
        return bool(r.success and np.max(np.abs(self.G@r.x+self.c-x), initial=0) <= tol
                    and np.max(np.abs(self.Aeq@r.x-self.beq), initial=0) <= tol)

    def slice(self, H, y):
        return ConstrainedZonotope(self.c.copy(), self.G.copy(),
                                   np.vstack([self.Aeq, H@self.G]),
                                   np.r_[self.beq, np.asarray(y)-H@self.c])

    def translate(self, t):
        return ConstrainedZonotope(self.c+np.asarray(t), self.G.copy(), self.Aeq.copy(), self.beq.copy())

    def record(self):
        return {k: getattr(self, k).tolist() for k in ('c', 'G', 'Aeq', 'beq')}


@dataclass
class HPolytope:
    H: np.ndarray
    h: np.ndarray
    vertices: np.ndarray = None

    def support(self, q):
        if self.vertices is not None:
            return float(np.max(self.vertices@q))
        r = linprog(-np.asarray(q), A_ub=self.H, b_ub=self.h,
                    bounds=[(None, None)]*self.H.shape[1], method='highs')
        if not r.success:
            raise ValueError('Polytope empty or unbounded: '+r.message)
        return -float(r.fun)

    def support_many(self, Q):
        if self.vertices is not None:
            return np.max(np.asarray(Q)@self.vertices.T, axis=1)
        return np.array([self.support(q) for q in Q])


def box(low, high):
    low, high = np.asarray(low), np.asarray(high)
    if np.any(low > high):
        raise ValueError('Empty box')
    return ConstrainedZonotope((low+high)/2, np.diag((high-low)/2))


def linear_map(M, Z):
    return ConstrainedZonotope(M@Z.c, M@Z.G, Z.Aeq.copy(), Z.beq.copy())


def minkowski_sum(Z1, Z2):
    return ConstrainedZonotope(Z1.c+Z2.c, np.c_[Z1.G, Z2.G],
                               block_diag(Z1.Aeq, Z2.Aeq), np.r_[Z1.beq, Z2.beq])


def generalized_intersection(Z, R, Y):
    """{x in Z : R x in Y}; noise latent variables stay shared."""
    G = np.c_[Z.G, np.zeros((Z.n, Y.g))]
    eq = np.vstack([block_diag(Z.Aeq, Y.Aeq), np.c_[R@Z.G, -Y.G]])
    return ConstrainedZonotope(Z.c, G, eq, np.r_[Z.beq, Y.beq, Y.c-R@Z.c])


def support(Z, direction):
    return Z.support(direction)


def interval_hull(Z):
    eye = np.eye(Z.n)
    return box(-Z.support_many(-eye), Z.support_many(eye))


def outer_reduce(Z, max_generators, basis=None):
    """Set-monotone fixed-basis hull; conservative and explicit complexity.

    Always computes the same hull, even for small inputs. A representation-
    dependent 'skip if small' shortcut would invalidate set monotonicity.
    """
    if max_generators < Z.n:
        raise ValueError('A full-dimensional box needs at least n generators')
    P = np.eye(Z.n) if basis is None else np.asarray(basis)
    Pinv = np.linalg.inv(P)
    lo, hi = -Z.support_many(-Pinv), Z.support_many(Pinv)
    return ConstrainedZonotope(P@((lo+hi)/2), P@np.diag((hi-lo)/2))


def pontryagin_inner(X, Z):
    """For H-polytope X this support tightening is exact, up to LP numerics."""
    return HPolytope(X.H.copy(), X.h-Z.support_many(X.H))


def polygon(Z):
    """Explicit 2D zonotope or H-polytope polygon, without vertex sign explosion."""
    if isinstance(Z, HPolytope):
        if Z.vertices is not None:
            return Z.vertices
        candidates = []
        for a, b in combinations(range(len(Z.h)), 2):
            H = Z.H[[a, b]]
            if abs(np.linalg.det(H)) < 1e-12:
                continue
            x = np.linalg.solve(H, Z.h[[a, b]])
            if np.max(Z.H@x-Z.h) <= 2e-7:
                candidates.append(x)
        if len(candidates) < 3:
            raise ValueError('Polygon empty/degenerate')
        points = np.unique(np.round(candidates, 12), axis=0)
    else:
        if Z.n != 2 or len(Z.beq):
            raise ValueError('Exact polygon requires unconstrained 2D zonotope')
        G = Z.G[:, np.linalg.norm(Z.G, axis=0) > 1e-13].copy()
        G[:, (G[1] < 0) | ((abs(G[1]) < 1e-14) & (G[0] < 0))] *= -1
        G = G[:, np.argsort(np.arctan2(G[1], G[0]))]
        start = Z.c-G.sum(axis=1)
        points = np.vstack([start, start+np.cumsum(2*G.T, axis=0),
                            start+2*G.sum(axis=1)-np.cumsum(2*G.T, axis=0)])
    return points[ConvexHull(points).vertices]


def to_polytope(Z):
    v = polygon(Z)
    ch = ConvexHull(v)
    return HPolytope(ch.equations[:, :-1], -ch.equations[:, -1], v)


class LPBuilder:
    """Small sparse linear-model builder used by both lifting certificates."""
    def __init__(self):
        self.bounds, self.cost, self.eq, self.eb, self.ub, self.ubv = [], [], [], [], [], []

    def var(self, shape, bound=(None, None), cost=0.):
        n = int(np.prod(shape)); start = len(self.bounds)
        self.bounds.extend([bound]*n); self.cost.extend([cost]*n)
        return np.arange(start, start+n).reshape(shape)

    def row(self, terms, rhs=0., equal=True):
        row = {}
        for idx, val in terms:
            for i, v in zip(np.asarray(idx).reshape(-1), np.broadcast_to(val, np.shape(idx)).reshape(-1)):
                if v: row[int(i)] = row.get(int(i), 0.)+float(v)
        (self.eq if equal else self.ub).append(row)
        (self.eb if equal else self.ubv).append(float(rhs))

    def solve(self):
        from scipy.sparse import coo_matrix
        def matrix(rows):
            rr, cc, vv = [], [], []
            for i, row in enumerate(rows):
                for j, v in row.items():
                    rr.append(i); cc.append(j); vv.append(v)
            return coo_matrix((vv, (rr, cc)), shape=(len(rows), len(self.bounds))).tocsr()
        return linprog(self.cost, A_eq=matrix(self.eq) if self.eq else None,
                       b_eq=self.eb if self.eq else None,
                       A_ub=matrix(self.ub) if self.ub else None,
                       b_ub=self.ubv if self.ub else None,
                       bounds=self.bounds, method='highs')


def affine_containment(inner, outer):
    """Sufficient containment via zeta=M xi+t on the inner constrained box.

    Geometry uses a global affine identity (sufficient). Target equalities are
    enforced on the source affine hull. Dual row support bounds exploit source
    equalities. All decision variables enter linearly for fixed sets.
    """
    a, b, g, q = inner, outer, outer.g, inner.g
    e = len(a.beq); qe = len(b.beq)
    model = LPBuilder()
    M = model.var((g, q)); t = model.var((g,))
    mu = model.var((qe, e))
    lam = model.var((2*g, e)); slack = model.var((2*g, q), (0., None))
    for i in range(a.n):
        for j in range(q):
            model.row([(M[:, j], b.G[i])], a.G[i, j])
        model.row([(t, b.G[i])], a.c[i]-b.c[i])
    for i in range(qe):
        for j in range(q):
            model.row([(M[:, j], b.Aeq[i]), (mu[i], -a.Aeq[:, j])])
        model.row([(t, b.Aeq[i]), (mu[i], a.beq)], b.beq[i])
    for i in range(g):
        for s, sign in enumerate((1., -1.)):
            r = 2*i+s
            for j in range(q):
                model.row([(M[i, j], sign), (lam[r], -a.Aeq[:, j]), (slack[r, j], -1.)], equal=False)
                model.row([(M[i, j], -sign), (lam[r], a.Aeq[:, j]), (slack[r, j], -1.)], equal=False)
            model.row([(t[i], sign), (lam[r], a.beq), (slack[r], 1.)], 1., equal=False)
    result = model.solve()
    if not result.success:
        return {'status': 'uncertified', 'solver_status': result.message}
    MM, tt = result.x[M], result.x[t]
    geom = max(np.max(abs(b.G@MM-a.G), initial=0), np.max(abs(b.G@tt+b.c-a.c), initial=0))
    # Independent maximizations over the source constrained domain.
    latent = ConstrainedZonotope(np.zeros(q), np.eye(q), a.Aeq, a.beq)
    box_res = max(latent.support(sign*MM[i])+sign*tt[i]-1
                  for i in range(g) for sign in (1, -1))
    eq_res = 0.
    for row, value in zip(b.Aeq, b.beq):
        direction, offset = row@MM, row@tt-value
        eq_res = max(eq_res, latent.support(direction)+offset, latent.support(-direction)-offset)
    return {'status': 'certified_float' if max(geom, box_res, eq_res) <= 2e-7 else 'residual_failed',
            'geometry_residual': float(geom), 'box_residual': float(box_res),
            'equality_residual': float(eq_res), 'M': MM, 't': tt,
            'variables': len(model.bounds)}


def contains(Z1, Z2):
    """Does Z1 contain Z2? General CZ result is a sufficient certificate."""
    if isinstance(Z1, HPolytope):
        violation = float(np.max(Z2.support_many(Z1.H)-Z1.h))
        return {'status': 'certified_float' if violation <= 2e-7 else 'counterexample',
                'max_facet_violation': violation}
    return affine_containment(Z2, Z1)


def homothetic_cz_rpi(F, W, template):
    """Optimize a scalar scale of a FIXED CZ template by an affine lifting LP.

    tau=scale*zeta removes the scale/lifting product. This is not unrestricted
    optimization over generator directions or equality geometry.
    """
    Z=template; n,g,p=Z.n,Z.g,W.g
    E=block_diag(Z.Aeq,W.Aeq); f=np.r_[Z.beq,W.beq]
    r=g+p; e=len(f); qe=len(Z.beq)
    mdl=LPBuilder()
    scale=mdl.var((1,),(1e-9,None),cost=1.)
    M=mdl.var((g,r));t=mdl.var((g,));mu=mdl.var((qe,e))
    lam=mdl.var((2*g,e));slack=mdl.var((2*g,r),(0.,None))
    FG=F@Z.G;fc=(F-np.eye(n))@Z.c
    for i in range(n):
        for j in range(g):
            mdl.row([(M[:,j],Z.G[i]),(scale,-FG[i,j])])
        for j in range(p):
            mdl.row([(M[:,g+j],Z.G[i])],W.G[i,j])
        mdl.row([(t,Z.G[i]),(scale,-fc[i])],W.c[i])
    for i in range(qe):
        for j in range(r):
            mdl.row([(M[:,j],Z.Aeq[i]),(mu[i],-E[:,j])])
        mdl.row([(t,Z.Aeq[i]),(mu[i],f),(scale,-Z.beq[i])])
    for i in range(g):
        for ss,sign in enumerate((1.,-1.)):
            rr=2*i+ss
            for j in range(r):
                mdl.row([(M[i,j],sign),(lam[rr],-E[:,j]),(slack[rr,j],-1.)],equal=False)
                mdl.row([(M[i,j],-sign),(lam[rr],E[:,j]),(slack[rr,j],-1.)],equal=False)
            mdl.row([(t[i],sign),(lam[rr],f),(slack[rr],1.),(scale,-1.)],equal=False)
    sol=mdl.solve()
    if not sol.success:
        return None,{'status':'uncertified','message':sol.message}
    value=float(sol.x[scale[0]])
    result=CZ_ALIAS=ConstrainedZonotope(value*Z.c,value*Z.G,Z.Aeq,Z.beq)
    cert=affine_containment(minkowski_sum(linear_map(F,result),W),result)
    cert.update(scale=value,variables=len(mdl.bounds),
                scope='LP synthesis of a homothetic fixed constrained template; global shape optimality not claimed')
    return result,cert
