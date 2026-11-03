#!/usr/bin/env python3
"""Exact/seeded checks for posterior shrink versus recentered tube containment.

The experiment isolates a proof obligation that is easy to miss in output-feedback
Tube MPC: X_new subset X_old does not imply X_new-z_new subset X_old-z_old when
the nominal/observer center changes.
"""
from __future__ import annotations

from fractions import Fraction as Q
from pathlib import Path
import argparse
import hashlib
import json
import random


def interval_contains(lo_outer, hi_outer, lo_inner, hi_inner):
    return lo_outer <= lo_inner and hi_inner <= hi_outer


def exact_counterexample():
    # X_new=[-9/10,9/10] is a strict subset of X_old=[-1,1].
    old = (Q(-1), Q(1))
    new = (Q(-9, 10), Q(9, 10))
    z_old = Q(0)
    z_new = Q(9, 10)
    e_old = (old[0]-z_old, old[1]-z_old)
    e_new = (new[0]-z_new, new[1]-z_new)
    shrink_plus = old[1]-new[1]
    shrink_minus = (-old[0])-(-new[0])
    delta = z_new-z_old
    budget_ok = (-delta <= shrink_plus and delta <= shrink_minus)
    return {
        'old_set': [str(v) for v in old],
        'new_set': [str(v) for v in new],
        'old_error_set': [str(v) for v in e_old],
        'new_error_set': [str(v) for v in e_new],
        'posterior_nested': interval_contains(*old, *new),
        'recentered_error_nested': interval_contains(*e_old, *e_new),
        'center_shift': str(delta),
        'support_shrink_plus': str(shrink_plus),
        'support_shrink_minus': str(shrink_minus),
        'support_budget_ok': budget_ok,
    }


def seeded_stress(seed=20260923, cases=10000):
    rng = random.Random(seed)
    failures = 0
    budget_matches = 0
    midpoint_failures = 0
    examples = []
    for _ in range(cases):
        a, b = sorted((rng.uniform(-1.0, 1.0), rng.uniform(-1.0, 1.0)))
        z = rng.uniform(a, b)
        contained = (a-z >= -1.0-1e-12 and b-z <= 1.0+1e-12)
        # p=+1: -delta <= h_old(+)-h_new(+)=1-b
        # p=-1: +delta <= h_old(-)-h_new(-)=1+a
        budget = (-z <= 1.0-b+1e-12 and z <= 1.0+a+1e-12)
        budget_matches += int(budget == contained)
        if not contained:
            failures += 1
            if len(examples) < 5:
                examples.append({'new': [a,b], 'center': z, 'error': [a-z,b-z]})
        midpoint = (a+b)/2.0
        midpoint_ok = (a-midpoint >= -1.0-1e-12 and b-midpoint <= 1.0+1e-12)
        midpoint_failures += int(not midpoint_ok)
    return {
        'seed': seed,
        'cases': cases,
        'arbitrary_posterior_center_containment_failures': failures,
        'failure_fraction': failures/cases,
        'support_budget_equivalence_matches': budget_matches,
        'midpoint_center_failures_for_nested_intervals': midpoint_failures,
        'first_counterexamples': examples,
    }


def run(seed=20260923, cases=10000):
    exact = exact_counterexample()
    assert exact['posterior_nested'] and not exact['recentered_error_nested']
    assert not exact['support_budget_ok']
    stress = seeded_stress(seed, cases)
    assert stress['support_budget_equivalence_matches'] == cases
    assert stress['midpoint_center_failures_for_nested_intervals'] == 0
    return {
        'scope': 'recentered posterior containment proof-obligation check',
        'theorem_checked': 'for protected directions p, h_Xnew(p)-p*znew <= h_Xold(p)-p*zold iff the recentered support does not grow in those directions',
        'exact_counterexample': exact,
        'seeded_interval_stress': stress,
        'interpretation': [
            'posterior set shrinkage alone is insufficient after an arbitrary nominal-center update',
            'direction-wise center shift must be paid for by direction-wise support shrinkage',
            'midpoint recentering is safe for nested one-dimensional intervals but this special fact must not be generalized to arbitrary CZ/nominal updates',
        ],
    }


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--seed', type=int, default=20260923)
    parser.add_argument('--cases', type=int, default=10000)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('output must not already exist')
    result = run(args.seed, args.cases)
    result['source_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
