"""Small exact common-input feasibility oracle, not an online MPC solver.

All geometry uses Fraction. Enumeration is complete below a declared budget;
budget exhaustion raises instead of returning a false infeasibility verdict.
See docs/research/cz_startup_predecessor.md for the quantifiers and proof.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import combinations, product
from math import comb


class EmptyInformation(ValueError):
    """The claimed information/noise set is empty; do not use vacuous safety."""


class BudgetExceeded(RuntimeError):
    """Enumeration was not attempted/completed; no feasibility conclusion."""


def vector(values):
    result = []
    for value in values:
        if not isinstance(value, (int, str, F)):
            raise TypeError('Use int, Fraction or rational string, never float')
        result.append(F(value))
    return tuple(result)


def matrix(rows, columns):
    result = tuple(vector(row) for row in rows)
    if any(len(row) != columns for row in result):
        raise ValueError('Matrix column dimension mismatch')
    return result


def dot(a, b):
    if len(a) != len(b):
        raise ValueError('Vector dimension mismatch')
    return sum((x*y for x, y in zip(a, b)), F(0))


def row_map(row, mat):
    return tuple(dot(row, column) for column in zip(*mat))


def independent_equations(rows, rhs, columns):
    """RREF of rational augmented rows, dropping redundant equalities."""
    if len(rows) != len(rhs):
        raise ValueError('Equality count mismatch')
    work = [list(row) + [value] for row, value in zip(rows, rhs)]
    pivot = 0
    for col in range(columns):
        found = next((i for i in range(pivot, len(work)) if work[i][col]), None)
        if found is None:
            continue
        work[pivot], work[found] = work[found], work[pivot]
        scale = work[pivot][col]
        work[pivot] = [v/scale for v in work[pivot]]
        for i in range(len(work)):
            if i != pivot and work[i][col]:
                scale = work[i][col]
                work[i] = [a-scale*b for a, b in zip(work[i], work[pivot])]
        pivot += 1
    if any(not any(row[:columns]) and row[columns] for row in work):
        return None
    return tuple(tuple(row[:columns]) for row in work[:pivot]), tuple(row[columns] for row in work[:pivot])


def solve_square(rows, rhs):
    n = len(rhs)
    reduced = independent_equations(rows, rhs, n)
    if reduced is None or len(reduced[0]) != n:
        return None
    return reduced[1]


def check_budget(count, maximum):
    if not isinstance(maximum, int) or maximum < 1:
        raise ValueError('max_bases must be a positive integer')
    if count > maximum:
        raise BudgetExceeded(f'{count} candidate bases exceed budget {maximum}')


@dataclass(frozen=True)
class CZ:
    center: tuple
    generators: tuple
    equalities: tuple = ()
    rhs: tuple = ()

    def __post_init__(self):
        center = vector(self.center)
        if not center or len(self.generators) != len(center):
            raise ValueError('CZ state/generator row dimension mismatch')
        ng = len(self.generators[0])
        generators = matrix(self.generators, ng)
        equalities, rhs = matrix(self.equalities, ng), vector(self.rhs)
        if len(equalities) != len(rhs):
            raise ValueError('CZ equality count mismatch')
        for key, value in (('center', center), ('generators', generators),
                           ('equalities', equalities), ('rhs', rhs)):
            object.__setattr__(self, key, value)

    def vertices(self, max_bases=20000):
        """All images of coefficient-polytope vertices (may include nonvertices)."""
        ng = len(self.generators[0])
        reduced = independent_equations(self.equalities, self.rhs, ng)
        if reduced is None:
            return ()
        eq, rhs = reduced
        rank = len(eq)
        check_budget(comb(ng, rank) * 2**(ng-rank), max_bases)
        images = set()
        for free in combinations(range(ng), rank):
            fixed = tuple(i for i in range(ng) if i not in free)
            block = tuple(tuple(row[i] for i in free) for row in eq)
            for signs in product((F(-1), F(1)), repeat=len(fixed)):
                remaining = tuple(b-sum((row[i]*s for i,s in zip(fixed,signs)), F(0)) for row,b in zip(eq,rhs))
                solution = solve_square(block, remaining)
                if solution is None or any(abs(v) > 1 for v in solution):
                    continue
                xi = [F(0)]*ng
                for i,v in zip(free, solution): xi[i] = v
                for i,v in zip(fixed, signs): xi[i] = v
                images.add(tuple(c+dot(row, xi) for c,row in zip(self.center,self.generators)))
        return tuple(sorted(images))

    def support(self, direction, max_bases=20000):
        points = self.vertices(max_bases)
        if not points:
            raise EmptyInformation('Empty CZ: inconsistent information contract')
        return max(dot(vector(direction), p) for p in points)


def bounded_feasible_point(rows, bounds, dimension, max_bases):
    """Complete for bounded polytopes, including faces/singletons.

    Called only after explicit finite command-box inequalities were appended.
    """
    zero = (F(0),)*dimension
    if all(b >= 0 for b in bounds):
        return zero
    if any(not any(row) and b < 0 for row,b in zip(rows,bounds)):
        return None
    check_budget(comb(len(rows), dimension), max_bases)
    for selected in combinations(range(len(rows)), dimension):
        point = solve_square(tuple(rows[i] for i in selected), tuple(bounds[i] for i in selected))
        if point is not None and all(dot(row,point) <= b for row,b in zip(rows,bounds)):
            return point
    return None


@dataclass(frozen=True)
class GateResult:
    status: str
    command: tuple | None
    rows: tuple
    bounds: tuple
    state_supports: tuple
    noise_supports: tuple
    initial_margins: tuple
    state_vertex_count: int
    noise_vertex_count: int


def startup_gate(a, b, d, information, disturbance, state_rows, state_limits,
                 input_radii, *, extra_input_rows=(), extra_input_limits=(),
                 max_bases=20000):
    """Exact startup gate for x+ = A x + B u + D w and product S x W.

    U is a finite axis-aligned box intersected with optional coupled halfspaces.
    Targets use state_rows*x <= state_limits. Initial containment is checked
    separately. 'infeasible' concerns the supplied sets, not physical viability.
    """
    n, nw = len(information.center), len(disturbance.center)
    radii = vector(input_radii)
    nu = len(radii)
    if not nu or any(r < 0 for r in radii):
        raise ValueError('Input box needs nonnegative finite radii')
    a,b,d = matrix(a,n),matrix(b,nu),matrix(d,nw)
    if any(len(mat) != n for mat in (a,b,d)):
        raise ValueError('Dynamics row dimension mismatch')
    hx,h = matrix(state_rows,n),vector(state_limits)
    hu,bu = matrix(extra_input_rows,nu),vector(extra_input_limits)
    if len(hx) != len(h) or len(hu) != len(bu):
        raise ValueError('Halfspace count mismatch')
    xp,wp = information.vertices(max_bases),disturbance.vertices(max_bases)
    if not xp or not wp:
        raise EmptyInformation('Empty state/noise CZ cannot certify startup')
    initial = tuple(limit-max(dot(row,x) for x in xp) for row,limit in zip(hx,h))
    sx = tuple(max(dot(row_map(row,a),x) for x in xp) for row in hx)
    sw = tuple(max(dot(row_map(row,d),w) for w in wp) for row in hx)
    rows = tuple(row_map(row,b) for row in hx) + hu
    limits = tuple(limit-ex-w for limit,ex,w in zip(h,sx,sw)) + bu
    for i,radius in enumerate(radii):
        for sign in (1,-1):
            rows += (tuple(F(sign if j == i else 0) for j in range(nu)),)
            limits += (radius,)
    if any(m < 0 for m in initial):
        status,command = 'initial_unsafe',None
    else:
        command = bounded_feasible_point(rows,limits,nu,max_bases)
        status = 'feasible' if command is not None else 'infeasible'
    return GateResult(status,command,rows,limits,sx,sw,initial,len(xp),len(wp))
