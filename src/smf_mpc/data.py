"""Deterministic episode-level data isolation; window after splitting only."""
import hashlib
import numpy as np

SPLITS = {'train': (10000,11199), 'validation': (20000,20199),
          'bound_diagnostic': (30000,30199), 'test': (40000,40199),
          'stress': (50000,50199), 'g1_pilot': (70001,70003)}


def split_for(seed):
    for name, (lo, hi) in SPLITS.items():
        if lo <= seed <= hi:
            return name
    raise ValueError('seed outside registered splits')


def rng_for(seed, stream):
    raw = hashlib.sha256(f'{seed}:{stream}'.encode()).digest()
    return np.random.default_rng(int.from_bytes(raw[:16], 'little'))


def windows(episode_id, seed, length, horizon, stride=1):
    if length <= horizon or horizon < 1 or stride < 1:
        raise ValueError('invalid episode/window length')
    split = split_for(seed)
    return [{'episode_id':episode_id, 'seed':seed, 'split':split, 'start':start,
             'stop_exclusive':start+horizon+1}
            for start in range(0, length-horizon, stride)]
