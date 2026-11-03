"""Contract timing and observations, shared by offline replay and online filter."""
from dataclasses import dataclass
import numpy as np


class ContractViolation(ValueError):
    pass


@dataclass(frozen=True)
class Observation:
    tick: int
    indices: tuple
    values: np.ndarray
    noise_radius: np.ndarray

    def __post_init__(self):
        v, r = np.array(self.values, dtype=float, copy=True), np.array(self.noise_radius, dtype=float, copy=True)
        if self.tick < 0 or len(set(self.indices)) != len(self.indices):
            raise ValueError('invalid observation tick or duplicate index')
        if v.shape != (len(self.indices),) or r.shape != v.shape or not np.isfinite([v, r]).all() or np.any(r < 0):
            raise ValueError('invalid observation values or bounds')
        if any(not isinstance(i, (int, np.integer)) or i < 0 or i >= 6 for i in self.indices):
            raise ValueError('invalid state index')
        v.flags.writeable = r.flags.writeable = False
        object.__setattr__(self, 'values', v)
        object.__setattr__(self, 'noise_radius', r)


class PacketSchedule:
    def __init__(self, period=5, max_missing=2):
        if period < 1 or max_missing < 0:
            raise ValueError('invalid schedule')
        self.period, self.max_missing = period, max_missing
        self.last_tick, self.missed = -1, 0

    def step(self, tick, drop=False):
        if tick != self.last_tick+1:
            raise ContractViolation('ticks must be consecutive, starting at zero')
        if drop and tick % self.period:
            raise ContractViolation('cannot drop a packet outside its opportunity')
        new_missed = self.missed
        position = False
        if tick % self.period == 0:
            new_missed = self.missed+1 if drop else 0
            if new_missed > self.max_missing:
                raise ContractViolation('TOO_MANY_MISSING_PACKETS')
            position = not drop
        self.last_tick, self.missed = tick, new_missed
        return (0, 1, 4, 5) if position else (4, 5)


def enumerate_masks(start_tick, prior_missed, horizon, period=5, max_missing=2):
    """Returns arrival ticks for future start_tick+1..start_tick+horizon."""
    if start_tick < 0 or horizon < 0 or period < 1 or not 0 <= prior_missed <= max_missing:
        raise ValueError('invalid mask contract')
    branches = [(prior_missed, ())]
    for tick in range(start_tick+1, start_tick+horizon+1):
        if tick % period:
            continue
        next_branches = []
        for missed, arrivals in branches:
            next_branches.append((0, arrivals+(tick,)))
            if missed < max_missing:
                next_branches.append((missed+1, arrivals))
        branches = next_branches
    return [arrivals for _, arrivals in branches]
