"""Offline exact replay of already delivered strips for the stage-4 deletion test."""
import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import platform

import packet_screen_check as screen

case = screen.case


def hull(points):
    points = sorted(set(points))
    if len(points) < 2:
        return points

    def lower(ordered):
        chain = []
        for p, v in ordered:
            while len(chain) >= 2:
                (x, y), (a, b) = chain[-2:]
                if (a - x) * (v - y) > (b - y) * (p - x):
                    break
                chain.pop()
            chain.append((p, v))
        return chain

    return lower(points)[:-1] + lower(reversed(points))[:-1]


def clip(vertices, sign, limit):
    out = []
    for a, b in zip(vertices, vertices[1:] + vertices[:1]):
        da, db = sign * a[0] - limit, sign * b[0] - limit
        if da <= 0:
            out.append(a)
        if da * db < 0:
            t = da / (da - db)
            out.append(tuple(x + t * (y - x) for x, y in zip(a, b, strict=True)))
    return hull(out)


def posterior(data, k):
    vertices = hull(case.corners(case.estimation.INITIAL))
    for s in range(k + 1):
        if s:
            vertices = hull(case.step(x, w) for x in vertices for w in (-case.W, case.W))
        if s in data:
            for sign in (-1, 1):
                vertices = clip(vertices, sign, case.NOISE + sign * data[s])
        assert vertices, "registered trajectory must be compatible"
    return vertices


def fixed_window_bounds():
    """Worst coordinate half-width with raw ages 0..5 or 0..6, after startup."""
    upper = {}
    for width in (6, 7):
        radii = []
        # k=16 represents any steady decision. The last two generation flags
        # need not yet be observable. Earlier generated stamps have arrived.
        for flags in product((0, 1), repeat=width - 2):
            if any(a == b == 0 for a, b in zip(flags, flags[1:])):
                continue
            guaranteed = [17 - width + j for j, present in enumerate(flags) if present]
            radii.append(screen.pair_bounds(16, guaranteed))
        upper[width] = tuple(map(max, zip(*radii, strict=True)))
    assert upper[7] == screen.E
    assert upper[6] == (Fraction(13, 200), Fraction(11, 200))

    # At block end 16 the two signed paths emit identical retained values.
    # Stamps 11,14,16 were skipped and 15 arrives at 17. Earlier packets,
    # including 10, have arrived but their values are outside the six slots.
    missed = {11, 14, 16}
    assert all(s + 1 not in missed for s in missed)
    arrived = {s for s in range(17) if s not in missed and s != 15}
    retained = sorted(s for s in arrived if 11 <= s <= 16)
    assert retained == [12, 13]
    acceleration = [0] * 6 + [-Fraction(13, 1800)] * 3 + [Fraction(31, 1800)] * 3 + [case.W] * 4
    paths = []
    for sign in (-1, 1):
        path = [case.ZERO]
        for w in acceleration:
            assert abs(w) <= case.W
            path.append(case.step(path[-1], sign * w))
        assert all(abs(path[s][0]) <= case.NOISE for s in retained)
        assert path[-1] == tuple(sign * radius for radius in upper[6])
        paths.append([path[s] for s in (*retained, 16)])
    return dict(six_and_seven_upper=upper, retained=retained, signed_paths=paths)


def audit(check_lp):
    n = case.NOISE
    panel = []
    for a, b in product((-1, 0, 1), repeat=2):
        data = {**dict.fromkeys(range(8), Fraction(0)), 8: a * n, 9: b * n}
        full = posterior(data, 10)
        reduced = posterior({s: y for s, y in data.items() if s != 7}, 10)
        # Deletion enlarges the set. A reduced vertex strictly beyond a full
        # polygon edge certifies strict inclusion, even with equal axis bounds.
        for first, last in zip(full, full[1:] + full[:1]):
            normal = (last[1] - first[1], first[0] - last[0])
            upper = screen.dot(normal, first)
            assert all(screen.dot(normal, x) <= upper for x in full)
            witness = max(reduced, key=lambda x: screen.dot(normal, x))
            excess = screen.dot(normal, witness) - upper
            if excess > 0:
                panel.append(dict(readouts=[data[8], data[9]], normal=normal,
                                  full_upper=upper, reduced_vertex=witness, excess=excess))
                break
        else:
            raise AssertionError("No separating edge in the registered panel")

    decisions = []
    for k in (10, 11):
        data = dict.fromkeys(range(10), Fraction(0))
        if k == 11:
            data[10] = Fraction(3, 400)
        # The constant state (1/400, 0), zero commands and disturbances
        # witness every released measurement. Stamp 11 may be absent.
        assert all(abs(y - Fraction(1, 400)) <= n for y in data.values())
        for keep in (True, False):
            used = {s: y for s, y in data.items() if keep or s != 7}
            vertices = posterior(used, k)
            intervals = [(min(x[j] for x in vertices), max(x[j] for x in vertices))
                         for j in (0, 1)]
            if check_lp:
                lp_intervals, _ = screen.posterior(k, used, None)
                assert intervals == lp_intervals
            actual = screen.check_plan(case.ZERO, screen.opt.FRACTION_ZERO, intervals)
            decisions.append(dict(k=k, keep=keep, intervals=intervals, actual=actual))
    assert [r["actual"] for r in decisions] == [0, 0, -Fraction(43, 600), -Fraction(59, 800)]
    paths = [Path(__file__), Path(screen.__file__), Path(case.__file__),
             Path(case.estimation.__file__), Path(screen.opt.__file__),
             screen.opt.ROOT / "experiments/oit_window4_certificate.py"]
    return dict(python=platform.python_version(), source_sha256={
        path.name: sha256(path.read_bytes()).hexdigest() for path in paths
    }, panel=panel, decisions=decisions, fixed_windows=fixed_window_bounds())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cross-check-lp", action="store_true",
                        help="Verify the 16 signed decision supports with a separate trajectory LP.")
    args = parser.parse_args()
    if not __debug__:
        raise RuntimeError("Use Python without -O for certificate verification")
    print(json.dumps(audit(args.cross_check_lp), indent=2, default=str))
