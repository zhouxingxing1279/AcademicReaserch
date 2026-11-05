"""Verify four-sample feasibility witnesses with standard-library rational arithmetic.

Run from any directory. The search program proposes plans and multipliers. This
checker rebuilds the trajectory and all constraints directly from the stored
decimal controller data; it never calls an LP solver or the MPC implementation.
"""

import json
from dataclasses import dataclass
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "experiments/results/oit_mrpi_20261105/controller.json"
PROOF = ROOT / "experiments/results/oit_window4_certificate.json"
WINDOW, N = 4, 15
STATE_LIMIT = (5, 3, 5, 3)
REFERENCE = ("4.0233", "1.20805")
ACTION_STATE = (Q("4.6"), Q(".1"))
ACTION = Q(".024")
OPT_STATE = (Q("3.5"), Q("-1.25"))
PREFIX_COMMAND = Q("-.75")
# State probes after directional boundary search; only zero uses the old point.
CASES = {
    "zero": (REFERENCE, ("0",) * 4, ("0",) * 4),
    "plus": (("4.001790", "1.202079"), ("0",) * 4, ("0", "0", "0", ".02")),
    "minus": (("4.043005", "1.215178"), ("0",) * 4, ("0", "0", "0", "-.02")),
    "mixed": (
        ("3.999708", "1.205349"),
        (".01", "-.015", ".01", "-.005"),
        ("-.03", ".02", "-.01", ".015"),
    ),
}


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def dot(a, b):
    return sum((x * y for x, y in zip(a, b, strict=True)), Q(0))


def rational(values):
    return tuple(map(Q, values))


def step(z, accel):
    p, v = z
    return p + v + accel / 2, v + accel


def solve_square(matrix, rhs):
    """Small exact systems only, with row pivoting."""
    n = len(rhs)
    aug = [list(row) + [value] for row, value in zip(matrix, rhs, strict=True)]
    for i in range(n):
        pivot = next(j for j in range(i, n) if aug[j][i])
        aug[i], aug[pivot] = aug[pivot], aug[i]
        aug[i] = [v / aug[i][i] for v in aug[i]]
        for j in range(n):
            if i != j:
                factor = aug[j][i]
                aug[j] = [v - factor * w for v, w in zip(aug[j], aug[i], strict=True)]
    return [row[-1] for row in aug]


class Contract:
    def __init__(self):
        archive = json.loads(ARCHIVE.read_text(encoding="utf-8"), parse_float=Q)
        self.K = rational(archive["K"][0])
        self.L = tuple(Q(row[0]) for row in archive["L"])
        box = archive["S"]
        require(not box["Aeq"] and not any(box["c"]), "centered unconstrained tail expected")
        self.G = tuple(map(rational, box["G"]))
        self._lifts = {}
        self.terminal = list(
            zip(map(rational, archive["terminal_H"]), rational(archive["terminal_h"]), strict=True)
        )
        self.P = tuple(map(rational, archive["P"]))
        (a, b), (c, d) = self.P
        require(b == c and a > 0 and a * d > b * b, "terminal cost must be positive definite")
        self.directions = (
            (1, 0, 1, 0),
            (0, 1, 0, 1),
            (-1, 0, -1, 0),
            (0, -1, 0, -1),
            (0, 0, *self.K),
            (0, 0, -self.K[0], -self.K[1]),
        )
        self.static = tuple(sum(abs(dot(q, col)) for col in zip(*self.G)) for q in self.directions)

    def error_step(self, eta, w, noise):
        ep, ev, dp, dv = eta
        ep_pred, ev_pred = step((ep, ev), w)
        r = ep_pred + noise
        dp_pred, dv_pred = step((dp, dv), dot(self.K, (dp, dv)))
        lp, lv = self.L
        return (ep_pred - lp * r, ev_pred - lv * r, dp_pred + lp * r, dv_pred + lv * r), r

    def lift(self, past, future, full):
        """Images of the cube generators, preserving shared process/measurement noise."""
        key = (past, future, full)
        if key in self._lifts:
            return self._lifts[key]
        columns = list(zip(*self.G))
        size = len(columns)
        eqcols, objective_cols = [], []
        length = past + future
        for j in range(size + 2 * length):
            eta = columns[j] if j < size else (Q(0),) * 4
            eq = list(eta[2:])
            for k in range(length):
                w = Q(j == size + 2 * k, 20)
                noise = Q(j == size + 2 * k + 1, 10)
                eta, r = self.error_step(eta, w, noise)
                if k < past and full:
                    eq.append(r)
                if k + 1 == past and not full:
                    eq.extend(eta[2:])
            eqcols.append(eq)
            objective_cols.append([dot(q, eta) for q in self.directions])
        self._lifts[key] = tuple(zip(*eqcols)), tuple(zip(*objective_cols))
        return self._lifts[key]

    def admit_error(self, eta, disturbances):
        # First finite-sum generators approximate the true disturbance history.
        # Correct the decimal archive's rounding in four independent columns.
        coeff = [Q(0)] * len(self.G[0])
        for j, (w, v) in enumerate(reversed(disturbances)):
            coeff[2 * j : 2 * j + 2] = [20 * w, 10 * v]
        error = [value - dot(row, coeff) for row, value in zip(self.G, eta, strict=True)]
        repair = solve_square([row[:4] for row in self.G], error)
        for j, correction in enumerate(repair):
            coeff[j] += correction
        require(
            max(map(abs, coeff)) <= 1 and tuple(dot(row, coeff) for row in self.G) == eta,
            "true error outside certified boundary representation",
        )


@dataclass
class History:
    ds: list
    rs: list
    inputs: list
    positions: list

    def equality_rhs(self, k, past, full):
        start = k - past
        data = self.rs[start:k] if full else (self.ds[k] if past else ())
        return (*self.ds[start], *data)


def earlier_state(target, steps, command):
    return (target[0] - steps * target[1] + steps**2 * command / 2, target[1] - steps * command)


def history(model, target, ws, noises, command=Q(0)):
    """Replay a constant nominal command; measurements use the actual input."""
    z = earlier_state(target, len(ws), command)
    x = estimate = z
    ds, rs, inputs, positions = [(Q(0), Q(0))], [], [], [x]
    model.admit_error((Q(0),) * 4, [])
    for k, (w, v) in enumerate(zip(ws, noises, strict=True)):
        u = command + dot(model.K, ds[-1])
        require(abs(u) <= 1 and abs(w) <= Q(1, 20) and abs(v) <= Q(1, 10), "input/noise bound")
        x = step(x, u + w)
        prediction = step(estimate, u)
        innovation = x[0] + v - prediction[0]
        estimate = tuple(a + l * innovation for a, l in zip(prediction, model.L))
        z = step(z, command)
        d = tuple(a - b for a, b in zip(estimate, z))
        eta = tuple(a - b for a, b in zip(x, estimate)) + d
        model.admit_error(eta, list(zip(ws[: k + 1], noises[: k + 1])))
        ds.append(d)
        rs.append(innovation)
        inputs.append(u)
        positions.append(x)
    require(
        z == target and all(abs(p) <= 5 and abs(v) <= 3 for p, v in positions), "prefix state bound"
    )
    return History(ds, rs, inputs, positions)


def upper_bound(E, b, q, dual):
    """For E*x=b, |x|<=1: q*x <= dual*b + ||q-dual*E||_1."""
    return dot(dual, b) + sum(abs(c - dot(dual, col)) for c, col in zip(q, zip(*E), strict=True))


def lower_bound(E, b, q, coeff):
    require(len(coeff) == len(q) and max(map(abs, coeff)) <= 1, "primal coefficient box")
    require(tuple(dot(row, coeff) for row in E) == tuple(b), "primal equality")
    return dot(q, coeff)


def plan_slack(model, z, inputs, margins):
    """Includes stage-zero admission, all 15 inputs, all states, and terminal rows."""
    require(len(inputs) == N and len(margins) == N + 1, "horizon")
    slacks = []
    for k, m in enumerate(margins):
        p, v = z
        slacks.extend(
            limit - val - error
            for limit, val, error in zip(STATE_LIMIT, (p, v, -p, -v), m[:4], strict=True)
        )
        if k < N:
            u = inputs[k]
            slacks.extend((1 - u - m[4], 1 + u - m[5]))
            z = step(z, u)
    slacks.extend(h - dot(row, z) for row, h in model.terminal)
    return min(slacks)


def origin_prefix(model):
    # Relax every observed equality. The resulting upper margins cover every
    # prefix and branch for which the true boundary error belongs to S.
    for k in range(WINDOW + 1):
        margins = []
        for i in range(WINDOW):
            _, rows = model.lift(min(k, WINDOW - i), i, False)
            margins.append([sum(map(abs, row)) for row in rows])
        require(
            plan_slack(model, (Q(0), Q(0)), [Q(0)] * N, margins + [model.static] * (N + 1 - WINDOW))
            > 0,
            "zero plan not feasible",
        )


def certified_margins(model, h, k, duals, endpoints_only):
    require(len(duals) == WINDOW, "missing stage")
    margins = []
    for i, stage in enumerate(duals):
        full = i > 0 and not endpoints_only
        past = min(k, WINDOW - i)
        E, rows = model.lift(past, i, full)
        b = h.equality_rhs(k, past, full)
        margins.append(
            [upper_bound(E, b, q, rational(y)) for q, y in zip(rows, stage, strict=True)]
        )
    return margins + [model.static] * (N + 1 - WINDOW)


def check_prefix(model, h, target, command, steps):
    prefix_slacks = []
    for k, step_proof in enumerate(steps):
        z = earlier_state(target, WINDOW - k, command)
        plan = rational(step_proof["plan"])
        require(plan[0] == command, "prefix input differs from executed nominal input")
        # Endpoints at *each* layer; any full-window plan using this sequence
        # has the same or weaker tightenings. At startup only available data enter.
        margins = certified_margins(model, h, k, step_proof["duals"], True)
        prefix_slacks.append(plan_slack(model, z, plan, margins))
    require(len(prefix_slacks) == WINDOW and min(prefix_slacks) > 0, "prefix not robust feasible")
    return min(prefix_slacks)


def verify_action(model, h, record, future_margins, endpoint_lower):
    prefix_slack = check_prefix(model, h, ACTION_STATE, Q(0), record["prefix"])
    fallback = rational(record["common_plan"])
    endpoint_margins = certified_margins(model, h, WINDOW, record["endpoint_duals"], True)
    common_slack = plan_slack(model, ACTION_STATE, fallback, endpoint_margins)
    selected = rational(record["action_plan"])
    require(selected[0] == ACTION and fallback[0] == 0, "wrong first move")
    action_slack = plan_slack(model, ACTION_STATE, selected, future_margins)
    violation = sum(ACTION_STATE) + ACTION / 2 + endpoint_lower - 5
    require(
        min(common_slack, action_slack, violation - (ACTION - Q(".018")) / 2) > 0,
        "action interval separation failed",
    )
    return {
        "prefix_slack": prefix_slack,
        "common_slack": common_slack,
        "action_slack": action_slack,
        "action_violation": violation,
        "actual_action": ACTION + dot(model.K, h.ds[-1]),
    }


def cost_gradient(model, z, inputs):
    states = [z]
    for u in inputs:
        states.append(step(states[-1], u))
    gp, gv = (2 * dot(row, states[-1]) for row in model.P)
    grad = []
    for (p, v), u in reversed(list(zip(states[:-1], inputs, strict=True))):
        grad.append(u / 5 + gp / 2 + gv)
        gp, gv = 2 * p + gp, 2 * v + gp + gv
    return grad[::-1]


def optimal_first_range(model, margins, lower):
    """Relax to just v[1] <= cap. Check full KKT sufficiency for all possible caps."""
    upper = margins[1][4]
    require(lower <= upper, "inverted support bounds")
    free = [j for j in range(N) if j != 1]
    cols = []
    for j in free:
        unit = [Q(0)] * N
        unit[j] = Q(1)
        cols.append(cost_gradient(model, (Q(0), Q(0)), unit))
    hessian = [[col[i] for col in cols] for i in free]
    first = []
    for cap in (1 - upper, 1 - lower):
        plan = [Q(0)] * N
        plan[1] = cap
        grad = cost_gradient(model, OPT_STATE, plan)
        for j, value in zip(free, solve_square(hessian, [-grad[i] for i in free]), strict=True):
            plan[j] = value
        grad = cost_gradient(model, OPT_STATE, plan)
        require(all(grad[j] == 0 for j in free) and grad[1] < 0, "invalid active-set signs")
        bounds = [list(row) for row in margins]
        bounds[1][4] = 1 - cap
        require(plan_slack(model, OPT_STATE, plan, bounds) >= 0, "inactive constraints violated")
        first.append(plan[0])
    # The equality-constrained optimum, its gradient and all row residuals
    # are affine in cap. Both endpoint checks therefore cover the whole interval.
    return min(first), max(first)


def check_case(model, name, record):
    target, ws, noises = map(rational, CASES[name])
    h = history(model, target, ws, noises)
    closed = history(model, (Q(0), Q(0)), ws, noises)
    require(h.rs == closed.rs and h.ds == closed.ds, "information depends on nominal translation")
    # The current admission test is endpoint-only on both sides.
    margins = certified_margins(model, h, WINDOW, record["dual_by_stage_and_direction"], False)
    plan = rational(record["nominal_inputs"])
    slack = plan_slack(model, target, plan, margins)
    E, rows = model.lift(3, 1, False)
    lower = lower_bound(
        E, h.equality_rhs(4, 3, False), rows[0], rational(record["endpoint_primal"])
    )
    # Current input is v_nom + K*d. Its lower bound limits possible braking.
    braking_floor = -1 - dot(model.K, h.ds[-1])
    obstruction = sum(target) + braking_floor / 2 + lower - 5
    gap = lower - margins[1][0]
    require(min(slack, obstruction, gap) > 0, "strict separation missing")
    # At the previous decision, the recorded d_4 is one admissible successor.
    # Input and position are separate robust rows and may use different witnesses.
    E, rows = model.lift(2, 2, True)
    previous_lower = lower_bound(
        E, h.equality_rhs(3, 2, True), rows[0], rational(record["previous_primal"])
    )
    previous_obstruction = sum(target) + braking_floor / 2 + previous_lower - 5
    require(previous_obstruction > 0, "previous-plan obstruction missing")
    result = {
        "feasible_slack": slack,
        "endpoint_violation": obstruction,
        "support_gap": gap,
        "previous_violation": previous_obstruction,
        "innovations": h.rs,
        "inputs": h.inputs,
    }
    if name in ("mixed", "plus"):
        E, rows = model.lift(3, 1, True)
        ref_lower = lower_bound(
            E, h.equality_rhs(4, 3, True), rows[0], rational(record["reference_full_primal"])
        )
        violation = sum(rational(REFERENCE)) + braking_floor / 2 + ref_lower - 5
        require(violation > 0, "reference point may still be feasible")
        result["reference_full_violation"] = violation
    if name == "minus":
        ref_margins = certified_margins(model, h, 4, record["reference_endpoint_duals"], True)
        ref_slack = plan_slack(
            model, rational(REFERENCE), rational(record["reference_endpoint_plan"]), ref_margins
        )
        require(ref_slack > 0, "reference point lacks common plan")
        result["reference_common_slack"] = ref_slack
    if name == "mixed":
        action = record["reachable_action"]
        ha = history(model, ACTION_STATE, ws, noises)
        ho = history(model, OPT_STATE, ws, noises, PREFIX_COMMAND)
        require(ha.rs == ho.rs == h.rs and ha.ds == ho.ds == h.ds, "observation mismatch")
        result.update(verify_action(model, ha, action, margins, lower))
        opt = record["optimal_separation"]
        result["optimal_prefix_slack"] = check_prefix(
            model, ho, OPT_STATE, PREFIX_COMMAND, opt["prefix"]
        )
        end = certified_margins(model, ho, 4, action["endpoint_duals"], True)
        for label, full, up in (("full", True, margins), ("end", False, end)):
            E, rows = model.lift(3, 1, full)
            lb = lower_bound(
                E, ho.equality_rhs(4, 3, full), rows[4], rational(opt[label + "_input_primal"])
            )
            lo, hi = optimal_first_range(model, up, lb)
            result[label + "_first_min"], result[label + "_first_max"] = lo, hi
        result["optimal_input_gap"] = result["end_first_min"] - result["full_first_max"]
        require(result["optimal_input_gap"] > 0, "optimal first-command intervals overlap")
    return result


def verify(path=PROOF):
    payload = json.loads(path.read_text(encoding="utf-8"))
    require(
        payload["schema"] == "oit-window4-separation-v1"
        and payload["controller_sha256"] == sha256(ARCHIVE.read_bytes()).hexdigest(),
        "wrong certificate or controller version",
    )
    require(set(payload["cases"]) == set(CASES), "case list changed")
    model = Contract()
    origin_prefix(model)
    return {name: check_case(model, name, payload["cases"][name]) for name in CASES}


if __name__ == "__main__":
    for name, res in verify().items():
        print(name, {k: float(v) for k, v in res.items() if isinstance(v, Q)})
