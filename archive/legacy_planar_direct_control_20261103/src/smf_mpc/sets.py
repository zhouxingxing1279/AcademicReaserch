"""Float64 set operations: numerical outer approximations, not interval certificates."""
from dataclasses import dataclass
import math
import numpy as np


class EmptySet(ValueError):
    pass


@dataclass(frozen=True)
class Box:
    lower: np.ndarray
    upper: np.ndarray

    def __post_init__(self):
        lo, hi = np.array(self.lower, dtype=float, copy=True), np.array(self.upper, dtype=float, copy=True)
        if lo.ndim != 1 or lo.shape != hi.shape or not np.isfinite([lo, hi]).all():
            raise ValueError('Box requires finite vectors of equal shape')
        if np.any(lo > hi):
            raise EmptySet('EMPTY_SET')
        lo.flags.writeable = hi.flags.writeable = False
        object.__setattr__(self, 'lower', lo)
        object.__setattr__(self, 'upper', hi)

    @classmethod
    def from_center(cls, center, radius):
        c, r = np.asarray(center), np.asarray(radius)
        if np.any(r < 0):
            raise ValueError('negative radius')
        return cls(c-r, c+r)

    @property
    def center(self):
        return (self.lower+self.upper)/2

    @property
    def radius(self):
        return (self.upper-self.lower)/2

    def contains(self, x, tolerance=0.0):
        x = np.asarray(x)
        return bool(x.shape == self.lower.shape and np.all(x >= self.lower-tolerance)
                    and np.all(x <= self.upper+tolerance))

    def encloses(self, other):
        return self.contains(other.lower) and self.contains(other.upper)

    def intersect(self, other):
        return Box(np.maximum(self.lower, other.lower), np.minimum(self.upper, other.upper))

    def affine(self, matrix, offset=None):
        matrix = np.asarray(matrix)
        offset = np.zeros(matrix.shape[0]) if offset is None else np.asarray(offset)
        c, r = matrix@self.center+offset, np.abs(matrix)@self.radius
        return Box.from_center(c, r)


def trig_range(lo, hi, kind):
    """Include interior critical points; libm rounding is NOT formally bounded."""
    if not math.isfinite(lo+hi) or lo > hi or kind not in ('sin', 'cos'):
        raise ValueError('invalid trigonometric interval')
    if hi-lo >= 2*math.pi:
        return -1.0, 1.0
    fn = math.sin if kind == 'sin' else math.cos
    shift = math.pi/2 if kind == 'sin' else 0.0
    values = [fn(lo), fn(hi)]
    for n in range(math.ceil((lo-shift)/math.pi), math.floor((hi-shift)/math.pi)+1):
        values.append(1.0 if n % 2 == 0 else -1.0)
    return min(values), max(values)


@dataclass
class Zonotope:
    center: np.ndarray
    generators: np.ndarray

    @property
    def box(self):
        return Box.from_center(self.center, np.abs(self.generators).sum(axis=1))

    def affine(self, matrix, noise_generators):
        return Zonotope(matrix@self.center, np.column_stack((matrix@self.generators, noise_generators)))

    def strip(self, C, y, noise_radius):
        P = self.generators@self.generators.T
        R = np.diag(np.asarray(noise_radius)**2)
        gain = np.linalg.solve(C@P@C.T+R, C@P).T
        return Zonotope(self.center+gain@(y-C@self.center),
                         np.column_stack(((np.eye(len(self.center))-gain@C)@self.generators,
                                          -gain@np.diag(noise_radius))))

    def reduce(self, max_generators):
        n, p = self.generators.shape
        if max_generators < n:
            raise ValueError('budget must be at least state dimension')
        if p <= max_generators:
            return self
        order = np.argsort(-np.linalg.norm(self.generators, axis=0), kind='stable')
        keep, drop = order[:max_generators-n], order[max_generators-n:]
        return Zonotope(self.center.copy(), np.column_stack((self.generators[:, keep],
            np.diag(np.abs(self.generators[:, drop]).sum(axis=1)))))
