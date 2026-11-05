"""Bounded-memory CZ estimator for a declared ZOH mathematical benchmark.

All numerical LP operations are float64, NOT outward-rounded certificates.
No hidden true state or future packet schedule enters the estimator.
"""
from dataclasses import dataclass
from collections import deque
import numpy as np
from scipy.optimize import linprog


class ContractError(ValueError):
    pass


@dataclass(frozen=True)
class Contract:
    T: float = 0.5
    acceleration: float = 0.02
    noise: float = 0.005
    missing: int = 1
    delay: int = 1
    initial_p: float = 0.005
    initial_v: float = 0.01

    def __post_init__(self):
        if self.T <= 0 or min(self.acceleration, self.noise, self.initial_p, self.initial_v) < 0:
            raise ValueError('Positive sampling time and nonnegative radii required')
        if any(type(v) is not int or v < 0 for v in (self.missing, self.delay)):
            raise ValueError('Nonnegative integer M and L required')

    @property
    def span(self):
        return 2*self.missing + self.delay + 1

    @property
    def age(self):
        return self.missing + self.delay

    def matrices(self):
        return np.array([[1., self.T], [0., 1.]]), np.array([self.T**2/2, self.T])

    def pair_radius(self, d, h):
        beta = 2*self.noise/(d*self.T) + d*self.T*self.acceleration/2
        return np.array([self.noise+h*self.T*beta+(h*self.T)**2*self.acceleration/2,
                         beta+h*self.T*self.acceleration])

    def uniform_error(self):
        # A feasible representative of a subset of a pair zonotope can be
        # at its boundary: use diameter, not the pair center's radius.
        radii = [2*self.pair_radius(d, h)
                 for h in range(self.age+1) for d in range(1, self.span-h+1)]
        for k in range(self.span):
            radii.append(np.array([self.initial_p+k*self.T*self.initial_v
                                   +(k*self.T)**2*self.acceleration/2,
                                   self.initial_v+k*self.T*self.acceleration]))
        return np.max(radii, axis=0)


@dataclass
class FloatCZ:
    center: np.ndarray
    generators: np.ndarray
    equalities: np.ndarray
    rhs: np.ndarray

    def solve(self, objective=None, extra_rows=None, extra_rhs=None):
        n = self.generators.shape[1]
        obj = np.zeros(n) if objective is None else np.asarray(objective)
        eq, rhs = self.equalities, self.rhs
        if extra_rows is not None:
            eq = np.vstack([eq, extra_rows])
            rhs = np.r_[rhs, extra_rhs]
        result = linprog(obj, A_eq=eq if len(eq) else None,
                         b_eq=rhs if len(eq) else None,
                         bounds=[(-1., 1.)]*n, method='highs')
        if result.status == 2:
            raise ContractError('Empty CZ: data/model/noise contract inconsistent')
        if not result.success:
            raise RuntimeError('LP unresolved: '+result.message)
        return result

    def bounds(self):
        low, high = [], []
        for c, row in zip(self.center, self.generators):
            low.append(c+self.solve(row).fun)
            high.append(c-self.solve(-row).fun)
        return np.array(low), np.array(high)

    def representative(self):
        # First try the natural pair center; if infeasible project to the CZ
        # in scaled infinity norm. Never assume constrained center is feasible.
        n = self.generators.shape[1]
        scale = np.maximum(np.abs(self.generators).sum(axis=1), 1e-10)
        rows = self.generators/scale[:, None]
        result = linprog(np.r_[np.zeros(n), 1.],
                         A_ub=np.vstack([np.c_[rows, -np.ones(len(rows))],
                                         np.c_[-rows, -np.ones(len(rows))]]),
                         b_ub=np.zeros(2*len(rows)),
                         A_eq=np.c_[self.equalities, np.zeros(len(self.rhs))] if len(self.rhs) else None,
                         b_eq=self.rhs if len(self.rhs) else None,
                         bounds=[(-1., 1.)]*n+[(0., None)], method='highs')
        if result.status == 2:
            raise ContractError('Empty CZ during representative selection')
        if not result.success:
            raise RuntimeError(result.message)
        xi = result.x[:n]
        residual = max(float(np.max(np.abs(self.equalities@xi-self.rhs), initial=0)),
                       float(np.max(np.abs(xi)-1, initial=0)))
        if residual > 1e-7:
            raise RuntimeError('LP witness fails residual check')
        return self.center+self.generators@xi

    def contains(self, point, tolerance=2e-7):
        try:
            r = self.solve(extra_rows=self.generators, extra_rhs=np.asarray(point)-self.center)
        except ContractError:
            return False
        return (np.max(np.abs(self.generators@r.x+self.center-point), initial=0) <= tolerance
                and np.max(np.abs(self.equalities@r.x-self.rhs), initial=0) <= tolerance)


def arrival_graph(missing, delay):
    """Enumerate ALL reachable finite delivery states, including startup.

    State = (capped clock, consecutive missed generations, pending(age,remaining),
    two freshest received ages). Delay choices are adversarial graph labels.
    """
    span = 2*missing+delay+1
    start = (0, 0, (), ())
    queue, seen, edges, pairs = deque([start]), {start}, 0, set()
    while queue:
        clock, gap, pending, received = queue.popleft()
        options = list(range(delay+1))+([-1] if gap < missing else [])
        for event in options:
            delivered = [a+1 for a in received]
            waiting = []
            for age, remaining in pending:
                if remaining == 1:
                    delivered.append(age+1)
                else:
                    waiting.append((age+1, remaining-1))
            if event == 0:
                delivered.append(0)
            elif event > 0:
                waiting.append((0, event))
            fresh = tuple(sorted(set(delivered))[:2])
            state = (min(clock+1, span+1), gap+1 if event == -1 else 0,
                     tuple(sorted(waiting)), fresh)
            if state[0] == span+1:
                assert len(fresh) == 2 and fresh[0] <= missing+delay and fresh[1] <= span
            if len(fresh) == 2:
                pairs.add((fresh[1]-fresh[0], fresh[0]))
            edges += 1
            if state not in seen:
                seen.add(state)
                queue.append(state)
    return {'states': len(seen), 'edges': edges, 'pairs': sorted(pairs), 'span': span}


def pair_window(contract, now, packets, commands, constrained=True):
    """Exact recent-measurement CZ with unrestricted state at oldest timestamp.

    It encloses the full-history posterior by deliberately forgetting older
    constraints. This is NOT exact for the complete received history.
    """
    stamps = sorted(packets)
    if len(stamps) < 2:
        raise ContractError('Two distinct timestamps required')
    s, t = stamps[0], stamps[-1]
    d, length = t-s, now-s
    interior = stamps[1:-1] if constrained else []
    if length > contract.span or now-t > contract.age:
        raise ContractError('Timestamp coverage contract violated')
    T, a, nu = contract.T, contract.acceleration, contract.noise
    ng = 2+length+len(interior)
    u = np.array([commands[j] for j in range(s, now)])
    vel = (packets[t]-packets[s]-sum(T*T*(d-j-.5)*u[j] for j in range(d)))/(d*T)
    c = np.array([packets[s], vel])
    G = np.zeros((2, ng))
    G[0, 0] = -nu
    G[1, 0], G[1, 1] = nu/(d*T), -nu/(d*T)
    for j in range(d):
        G[1, 2+j] = -T*(d-j-.5)*a/d
    trajectory = {s: (c.copy(), G.copy())}
    A, B = contract.matrices()
    for j in range(length):
        c = A@c+B*u[j]
        G = A@G
        G[:, 2+j] += B*a
        trajectory[s+j+1] = (c.copy(), G.copy())
    equalities, rhs = [], []
    for i, stamp in enumerate(interior):
        cj, gj = trajectory[stamp]
        row = gj[0].copy()
        row[2+length+i] += nu
        equalities.append(row)
        rhs.append(packets[stamp]-cj[0])
    return FloatCZ(c, G, np.asarray(equalities).reshape(-1, ng), np.array(rhs))


def full_history(contract, now, packets, commands, initial_center):
    """Independent batch model from initial state, for offline comparison only."""
    stamps = sorted(packets)
    ng = 2+now+len(stamps)
    G = np.zeros((2, ng))
    G[:, :2] = np.diag([contract.initial_p, contract.initial_v])
    c = np.array(initial_center, dtype=float)
    trajectory = {0: (c.copy(), G.copy())}
    A, B = contract.matrices()
    for j in range(now):
        c = A@c+B*commands[j]
        G = A@G
        G[:, 2+j] += B*contract.acceleration
        trajectory[j+1] = (c.copy(), G.copy())
    eq, rhs = [], []
    for i, stamp in enumerate(stamps):
        cj, gj = trajectory[stamp]
        row = gj[0].copy()
        row[2+now+i] = contract.noise
        eq.append(row)
        rhs.append(packets[stamp]-cj[0])
    return FloatCZ(c, G, np.asarray(eq).reshape(-1, ng), np.array(rhs))


class FiniteMemoryEstimator:
    def __init__(self, contract, initial_center, constrained=True):
        self.contract = contract
        self.initial_center = np.array(initial_center, dtype=float)
        self.commands, self.packets = {}, {}
        self.now, self.constrained = 0, constrained

    def observe(self, arrivals):
        for timestamp, value in arrivals:
            if type(timestamp) is not int or not max(0, self.now-self.contract.delay) <= timestamp <= self.now:
                raise ContractError('Future, expired, or noninteger timestamp')
            if not np.isfinite(value):
                raise ContractError('Nonfinite measurement')
            if timestamp in self.packets and self.packets[timestamp] != value:
                raise ContractError('Conflicting duplicate')
            self.packets[timestamp] = value
        oldest = self.now-self.contract.span
        self.packets = {s: y for s, y in self.packets.items() if s >= oldest}
        if len(self.packets) >= 2:
            return pair_window(self.contract, self.now, self.packets, self.commands, self.constrained)
        if self.now >= self.contract.span:
            raise ContractError('Recovery deadline missed: fewer than two timestamps')
        # Explicit startup fallback: propagate compact initial prior without
        # claiming a single position packet determines velocity.
        return full_history(self.contract, self.now, {}, self.commands, self.initial_center)

    def advance(self, command):
        if not np.isfinite(command):
            raise ContractError('Nonfinite command')
        self.commands[self.now] = float(command)
        self.now += 1
        self.commands = {j: u for j, u in self.commands.items() if j >= self.now-self.contract.span}
