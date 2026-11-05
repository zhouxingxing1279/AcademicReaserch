"""Offline stage-4 packet screen. HiGHS proposes witnesses, Fraction verifies them."""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
import json
from pathlib import Path
import platform

import control_prefix_optimum as opt

case = opt.case
est = case.estimation
HERE = Path(__file__).resolve().parent
E = Q(3, 50), Q(31, 600)
DELTA, LIMITS, INPUT = case.design(E)
N = case.NOISE
dot = est.dot


def signed_support(target, rows, values, box, saved):
    """Max q*xi with |xi|<=box and |P*xi-y|<=N; exact matching upper/lower."""
    if saved is None:
        from scipy.optimize import linprog
        matrix = rows + [[-c for c in row] for row in rows]
        rhs = [N+y for y in values] + [N-y for y in values]
        lp = linprog([-c for c in target], A_ub=matrix, b_ub=rhs,
                     bounds=[(-r, r) for r in box], method="highs")
        if not lp.success:
            raise ValueError(lp.message)
        dual = lp.ineqlin.marginals
        lam = [Q(float(dual[i+len(rows)]-dual[i])).limit_denominator(10**6)
               for i in range(len(rows))]
        xi = [Q(float(v)).limit_denominator(10**6) for v in lp.x]
    else:
        xi, lam = (list(map(Q, saved[key])) for key in ("xi", "lambda"))
    assert all(abs(a) <= b for a, b in zip(xi, box, strict=True))
    assert all(abs(dot(row, xi)-y) <= N for row, y in zip(rows, values, strict=True))
    residual = [c-dot(column, lam) for c, column in zip(target, zip(*rows), strict=True)]
    upper = dot(box, map(abs, residual)) + dot(values, lam) + N*sum(map(abs, lam))
    assert upper == dot(target, xi)
    return {"value": upper, "xi": xi, "lambda": lam}


def posterior(k, data, saved):
    positions, velocity = est.rows(k)
    rows = [positions[s] for s in data]
    box = [*est.INITIAL, *([case.W]*k)]
    certs = {}
    intervals = []
    for axis, row in (("p", positions[-1]), ("v", velocity)):
        bounds = []
        for sign in (-1, 1):
            name = axis + str(sign)
            archive = saved["supports"][name] if saved is not None else None
            proof = signed_support([sign*v for v in row], rows, list(data.values()), box, archive)
            certs[name] = proof
            bounds.append(sign * proof["value"])
        intervals.append(tuple(bounds))
    return intervals, {"k": k, "data": list(data.items()), "supports": certs}


def check_plan(z, plan, intervals):
    """Current intervals are deviations from z. Check actual command and tail."""
    center = tuple((lo+hi)/2 for lo, hi in intervals)
    correction = case.gain(center)
    actual = plan[0] + correction
    assert abs(actual) <= case.UMAX
    states = opt.trajectory(z, plan)
    for error in product(*intervals):
        assert case.gauge(error) <= DELTA
        for j in (0, 1):
            assert abs(z[j] + error[j]) <= case.LIMIT[j]
        for w in (-case.W, case.W):
            nxt = case.step(error, correction+w)
            assert case.gauge(nxt) <= DELTA
            for j in (0, 1):
                assert abs(states[1][j]+nxt[j]) <= case.LIMIT[j]
    assert all(abs(b) <= INPUT for b in plan[1:])
    assert all(abs(coord) <= limit for x in states[2:]
               for coord, limit in zip(x, LIMITS, strict=True))
    case.terminal_check(states[-1], LIMITS, INPUT)
    return actual


def active_plan(eps, intervals, seeds):
    # Affine candidate from two archived plans; verify KKT even for extrapolation.
    first = Q(98, 25) + 7*eps
    a, b = (list(map(Q, seeds["main_"+key]["optimal_plan"]))
            for key in ("immediate", "deadline"))
    t = (first-b[0])/(a[0]-b[0])
    plan = [y+t*(x-y) for x, y in zip(a, b, strict=True)]
    actual = check_plan(opt.Z8, plan, intervals)
    states = opt.trajectory(opt.Z8, plan)
    assert intervals[1][1] + case.T*(actual+case.W) == case.LIMIT[1]
    assert states[2][1] == LIMITS[1]
    grad = []
    for j in range(case.N):
        impulse = list(opt.FRACTION_ZERO)
        impulse[j] = Q(1)
        grad.append(2*opt.cost_pair(states, plan, opt.trajectory(case.ZERO, impulse), impulse))
    mu = (grad[1]-grad[0])/case.T, -grad[1]/case.T
    assert min(mu) > 0 and grad[0]+case.T*sum(mu) == grad[1]+case.T*mu[1] == 0
    assert all(g == 0 for g in grad[2:])
    assert actual == Q(98, 25)-2*eps
    return {"nominal": first, "actual": actual, "multipliers": mu}


def pair_bounds(k, stamps):
    bounds = []
    for s, t in combinations(stamps, 2):
        span, age = (t-s)*case.T, (k-t)*case.T
        end_velocity = 2*N/span + case.W*span/2
        bounds.append((N+age*end_velocity+case.W*age**2/2, end_velocity+case.W*age))
    return tuple(map(min, zip(*bounds, strict=True)))


def future_widths():
    levels = {}
    for k in range(10, 14):
        branches = []
        for flags in product((0, 1), repeat=max(0, k-11)):
            if any(x == y == 0 for x, y in zip(flags, flags[1:])):
                continue
            stamps = set(range(7)) | {8, 9} | {10+j for j, flag in enumerate(flags) if flag}
            window = sorted(s for s in stamps if k-6 <= s <= k)
            bounds = pair_bounds(k, window)
            assert all(b <= e for b, e in zip(bounds, E, strict=True))
            branches.append({"stamps": window, "bounds": bounds})
        levels[k] = branches
    failed = pair_bounds(13, [9, 10])
    assert failed[0] > E[0] and failed[1] > E[1]
    return {"covered": levels, "pair_test_unresolved_without_stamp8": failed}


def audit(archive):
    results = {}
    def get(name, k, data):
        old = archive["cases"][name] if archive is not None else None
        intervals, record = posterior(k, data, old)
        results[name] = record
        return intervals

    base = dict.fromkeys(range(7), Q(0))
    seeds = json.loads((HERE/"control_prefix_optimum.json").read_text())["solutions"]
    zero = opt.FRACTION_ZERO
    decisions = {}
    for eps in (-N, Q(0), N):
        bounds = get("epsilon_"+str(eps), 8, {**base, 7: eps})
        assert bounds == [(3*eps/2-Q(7,400), 3*eps/2+Q(7,400)),
                          (eps-Q(3,100), eps+Q(3,100))]
        assert check_plan(case.ZERO, zero, bounds) == -9*eps
        for sign in (-1, 1):
            first = sign*Q(98,25)+7*eps
            plan = [first*v for v in case.PROFILE]
            assert check_plan(case.ZERO, plan, bounds) == sign*Q(98,25)-2*eps
        decisions[str(eps)] = active_plan(eps, bounds, seeds)

    successors = {}
    for keep in (False, True):
        data = {**base, 9: N}
        if keep:
            data[7] = Q(0)
        bounds = get("successor_keep_"+str(keep), 9, dict(sorted(data.items())))
        successors[str(keep)] = {"intervals": bounds, "actual": check_plan(case.ZERO, zero, bounds)}
    assert successors["True"]["actual"] == -Q(7,200)
    assert successors["False"]["actual"] == -Q(3,100)
    schedule = (*case.MAIN, 0)
    available = case.available(schedule, 9, deadline=True)
    assert available == tuple(range(8))
    buffered = get("successor_deadline", 9, dict.fromkeys(available, Q(0)))
    successors["deadline"] = {"intervals": buffered, "actual": check_plan(case.ZERO, zero, buffered)}
    assert successors["deadline"]["actual"] == 0
    dry = get("no_arrival_through_10_after_erasure", 10, base)
    assert dry[1] == (-Q(3,50), Q(3,50))
    assert all(case.gauge(e) <= DELTA for e in product(*dry))
    sources = [Path(__file__), HERE/"packet_screen_protocol.md", HERE/"control_prefix_check.py",
               HERE/"control_prefix_optimum.py", HERE/"control_prefix_optimum.json",
               HERE/"cdc22_reduction_check.py", HERE/"reduction_protocol.json",
               opt.ROOT/"experiments/oit_window4_certificate.py"]
    return {"cases": results, "active_plans": decisions, "successors": successors,
            "no_arrival_box": dry, "forgetting": future_widths(),
            "source_sha256": {p.name: sha256(p.read_bytes()).hexdigest() for p in sources}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", type=Path)
    mode.add_argument("--verify", type=Path)
    args = parser.parse_args()
    if not __debug__:
        raise RuntimeError("Exact assertions require standard Python without -O")
    saved = json.loads(args.verify.read_text(encoding="utf8")) if args.verify else None
    evidence = saved["evidence"] if saved is not None else None
    result = json.loads(json.dumps(audit(evidence), default=str))
    if args.verify:
        assert result == saved["evidence"]
        print("Verified signed supports, interval endpoints, KKT, successor, coverage and hashes.")
    else:
        import numpy
        import scipy
        env = dict(python=platform.python_version(), scipy=scipy.__version__,
                   numpy=numpy.__version__, random_seed=None)
        args.write.write_text(json.dumps({"environment": env, "evidence": result}, indent=2)
                              + "\n", encoding="utf8")
