#!/usr/bin/env python3
"""Exact finite polytope certificate for angular tracking, not six-state closure."""

import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

from check_coupled_theory import verify as verify_previous


ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def matrix_product(left, right):
    require(bool(left) and bool(right), "Empty matrix")
    require(all(len(row) == len(right) for row in left), "Matrix product dimensions")
    require(all(len(row) == len(right[0]) for row in right), "Ragged right matrix")
    return [[sum((a * b for a, b in zip(row, col)), F(0)) for col in zip(*right)] for row in left]


def matrix_vector(matrix, vector):
    return [row[0] for row in matrix_product(matrix, [[v] for v in vector])]


def exact_inclusion(A, G, H_from, d_from, H_to, d_to, noise, multiplier, offset):
    """Sufficient certificate for A*P+offset+G*box(noise) contained in Q.

    The caller must separately prove that this affine relation covers the
    physical dynamics and that the controller is causal. No such claim is
    inferred from the declared matrices.
    """
    n, m_from, m_to = len(A), len(H_from), len(H_to)
    require(n > 0 and all(len(row) == n for row in A), "A must be square")
    require(len(G) == n and all(len(row) == len(noise) for row in G), "G shape")
    require(all(len(row) == n for row in H_from + H_to), "H shape")
    require(len(d_from) == m_from and len(d_to) == m_to, "Offset shape")
    require(len(multiplier) == m_to and all(len(row) == m_from for row in multiplier), "Multiplier shape")
    require(len(offset) == n and all(w >= 0 for w in noise), "Offset or noise invalid")
    require(all(v >= 0 for row in multiplier for v in row), "Negative multiplier")
    require(matrix_product(multiplier, H_from) == matrix_product(H_to, A), "Face identity failed")
    HG = matrix_product(H_to, G)
    disturbance_support = matrix_vector([[abs(v) for v in row] for row in HG], noise)
    propagated = matrix_vector(multiplier, d_from)
    shift = matrix_vector(H_to, offset)
    slack = [limit - value - delta - support for limit, value, delta, support in zip(d_to, propagated, shift, disturbance_support)]
    require(all(v >= 0 for v in slack), "Containment inequality failed")
    return slack


def text_values(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, list):
        return [text_values(v) for v in value]
    if isinstance(value, dict):
        return {k: text_values(v) for k, v in value.items()}
    return value


def reference_faces(angle, rate, torque, h, J):
    ratio = rate / (h * torque / J)
    n_max = (ratio.numerator + ratio.denominator - 1) // ratio.denominator
    H, d = [], []
    for n in range(n_max + 1):
        bound = angle + h * h * (torque / J) * n * (n - 1) / 2
        H.extend([[F(1), h * n], [F(-1), -h * n]])
        d.extend([bound, bound])
    H.extend([[F(0), F(1)], [F(0), F(-1)]])
    d.extend([rate, rate])
    return n_max, H, d


def verify():
    previous = verify_previous()
    h = J = F(1, 50)
    r, epsilon = F(23, 25), F(2, 625)
    M = [[F(1), h], [-F(8, 25), F(21, 25)]]
    G = [[F(0)], [F(1)]]
    transform = [[F(1), F(0)], [F(4), F(1)]]
    inverse = [[F(1), F(0)], [-F(4), F(1)]]
    transformed = matrix_product(matrix_product(transform, M), inverse)
    require(transformed == [[r, h], [F(0), r]], "Triangular transformation failed")
    a = h * epsilon / (1 - r)**2
    b = epsilon / (1 - r)
    require((a, b) == (F(1, 100), F(1, 25)), "Minimal rectangle differs")
    H = [[F(1), F(0)], [F(-1), F(0)], [F(4), F(1)], [F(-4), F(-1)]]
    d = [a, a, b, b]
    multiplier = [[r, F(0), h, F(0)], [F(0), r, F(0), h], [F(0), F(0), r, F(0)], [F(0), F(0), F(0), r]]
    slack = exact_inclusion(M, G, H, d, H, d, [epsilon], multiplier, [F(0), F(0)])
    require(slack == [0] * 4, "Expected tight face certificates")
    initial_radius = [F(1, 200), F(1, 100)]
    initial_support = matrix_vector([[abs(v) for v in row] for row in H], initial_radius)
    initial_slack = [limit - value for limit, value in zip(d, initial_support)]
    require(all(v > 0 for v in initial_slack), "Initial set not contained")
    # A malformed face identity and a truly too-small rectangle must be rejected.
    bad_multiplier = [row[:] for row in multiplier]
    bad_multiplier[0][0] += F(1, 100)
    rejected = []
    for name, bounds, lam in [("incorrect_multiplier", d, bad_multiplier), ("too_small_rectangle", [a / 2, a / 2, b, b], multiplier)]:
        try:
            exact_inclusion(M, G, H, bounds, H, bounds, [epsilon], lam, [F(0), F(0)])
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError("Invalid certificate accepted: " + name)

    correction_q = matrix_product([[-F(8, 25), -F(4, 25)]], inverse)[0]
    correction = sum((abs(k) * radius for k, radius in zip(correction_q, [a, b])), F(0)) + epsilon
    omega_bound = b + 4 * a
    require(correction == F(8, 625) and omega_bound == F(2, 25), "New support bounds differ")
    reference_limits = [F(9, 20) - a, F(2) - omega_bound, F(2, 25) - correction]
    require(reference_limits == [F(11, 25), F(48, 25), F(42, 625)], "New reference limits differ")
    index, Hc, dc = reference_faces(*reference_limits, h, J)
    require(index == 29, "Reference facet index differs")
    reference_witness = [F(43, 100), F(0)]
    require(all(v <= limit for v, limit in zip(matrix_vector(Hc, reference_witness), dc)), "New reference witness rejected")
    require(reference_witness[0] > F(171, 400), "Witness not strict against old reference bound")
    action_witness = F(3, 50)
    next_reference = [F(0), action_witness]
    require(action_witness <= reference_limits[2] and action_witness > F(63, 1250), "Action witness not strict")
    require(all(v <= limit for v, limit in zip(matrix_vector(Hc, next_reference), dc)), "Next reference outside kernel")

    # Same 40-step reference and same actual feedback law as theory/04.
    g, d_x, d_z = F(981, 100), F(47, 25), F(1043, 500)
    n = previous["horizon_ticks"]
    angle_sum = F(previous["reference_angle_sum"])
    weighted_sum = F(previous["reference_weighted_angle_sum"])
    new_vx = F(1, 10) + h * (g * (angle_sum + n * a) + n * d_x)
    new_px = F(1, 50) + n * h / 10 + h * h * (g * (weighted_sum + a * n * (n - 1) / 2) + d_x * n * (n - 1) / 2)
    alpha_z = g * (F(1, 5) + a)**2 / 2 + d_z
    new_vz = F(1, 10) + n * h * alpha_z
    new_pz = F(1, 50) + n * h / 10 + h * h * n * (n - 1) * alpha_z / 2
    new_bounds = [new_px, new_pz, new_vx, new_vz, F(1, 5) + a, F(1, 2) + omega_bound]
    old_bounds = list(map(F, previous["uniform_bounds_relative_to_hover"]))
    require(all(new < old for new, old in zip(new_bounds, old_bounds)), "Expected stricter analytic bounds")

    return text_values({
        "status": "EXACT_FINITE_ANGULAR_POLYTOPE_CERTIFICATE_PASSED",
        "scope": "Finite angular RPI, minimal within one transformed rectangle class, strict reference-certificate expansion; not full six-state terminal closure",
        "inclusion_certificate": {"A": M, "G": G, "H_from": H, "d_from": d, "H_to": H, "d_to": d,
                                  "noise": [epsilon], "multiplier": multiplier, "offset": [F(0), F(0)]},
        "transformation": transform, "transformed_matrix": transformed,
        "minimal_transformed_radii": [a, b], "face_slack": slack, "initial_set_slack": initial_slack,
        "angular_absolute_bounds": [a, omega_bound], "torque_correction_bound": correction,
        "negative_certificate_cases_rejected": rejected,
        "reference_limits_angle_rate_torque": reference_limits, "reference_max_braking_index": index,
        "reference_kernel": {"H": Hc, "d": dc},
        "strict_reference_witness": reference_witness, "strict_action_witness_at_origin": action_witness,
        "same_maneuver_old_uniform_bounds": old_bounds, "same_maneuver_new_uniform_bounds": new_bounds,
        "same_maneuver_new_torque_bound": F(1, 40) + correction,
        "global_minimal_RPI_claimed": False, "new_polytope_subset_of_old_infinite_set_proved": False,
        "full_six_state_infinite_horizon_invariance_proved": False, "neural_superiority_proved": False,
        "config_sha256": previous["config_sha256"], "plant_source_sha256": previous["plant_source_sha256"],
        "previous_checker_sha256": previous["checker_sha256"],
        "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.output and args.output.exists():
        parser.error("Use a new output file")
    result = verify()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in {"reference_kernel", "inclusion_certificate"}}, indent=2))


if __name__ == "__main__":
    main()
