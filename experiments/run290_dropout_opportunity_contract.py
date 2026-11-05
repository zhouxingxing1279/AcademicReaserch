"""Explicit measurement-opportunity schedules; S=success, M=miss.

Not a reconstruction of the repository's formal dropout automaton.
"""
from itertools import product


def opportunity_schedule(pattern: str, steps: int = 150, period: int = 5):
    assert pattern and set(pattern) <= {'S', 'M'}
    assert steps >= 0 and period > 0
    opportunities = range(period, steps + 1, period)
    return [(k, pattern[(k // period - 1) % len(pattern)]) for k in opportunities]


def audit():
    for pattern, expected in [('S', 30), ('MMS', 10), ('SMM', 10), ('SMS', 20)]:
        seq = opportunity_schedule(pattern)
        assert len(seq) == 30
        assert sum(flag == 'S' for _, flag in seq) == expected
        assert ''.join(flag for _, flag in seq[:len(pattern)]) == pattern
    assert opportunity_schedule('MMS')[:3] == [(5,'M'),(10,'M'),(15,'S')]
    assert opportunity_schedule('SMM')[:3] == [(5,'S'),(10,'M'),(15,'M')]
    assert len(opportunity_schedule('S')) == 30 != 150
    for p in product('SM', repeat=3):
        schedule = opportunity_schedule(''.join(p))
        assert len(schedule) == 30
        assert sum(v == 'S' for _, v in schedule) == 10 * p.count('S')
    print('PASS: 4 schedule counts, 2 phase anchors, cadence, 8 exhaustive 3-symbol patterns')


if __name__ == '__main__':
    audit()
