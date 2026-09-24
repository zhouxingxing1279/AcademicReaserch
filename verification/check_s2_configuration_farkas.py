#!/usr/bin/env python3
"""Exact Farkas certificate for the S2 configuration-constrained RCI LP.

The certificate uses four endpoint-robust vertex inequalities from the
S2-incidence configuration and the lower torque bound. Fraction arithmetic
only; no optimizer is needed to validate the contradiction.
"""
from fractions import Fraction as F
import argparse, json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    # Reduced variables are [q3,q6,q13,u26].  These four inequalities are
    # exact rows of the full configuration-constrained LP after substituting
    # the affine vertex maps x_v(q).  All use legal thrust endpoints.
    # a^T z <= b
    rows = [
        ([F(0), F(-2943,5000), F(2943,10000), F(0)], F(-6731149,160000000)),
        ([F(981,100000), F(0), F(-2943,10000), F(0)], F(-6731149,160000000)),
        ([F(-1), F(50), F(-50), F(-1)], F(0)),
        ([F(0), F(0), F(2943,10000), F(2943,500000)], F(-6731149,160000000)),
    ]
    # Positive Farkas multipliers.
    y = [F(5,11), F(6,11), F(2943,550000), F(1)]
    combo = [sum(y[i]*rows[i][0][j] for i in range(4)) for j in range(4)]
    rhs = sum(y[i]*rows[i][1] for i in range(4))

    # The q coefficients cancel.  The only remaining coefficient is +c*u26.
    c = F(2943,5500000)
    assert combo[:3] == [F(0), F(0), F(0)]
    assert combo[3] == c
    assert rhs == F(-6731149,80000000)

    # Torque lower bound u26 >= -0.08 is -u26 <= 2/25. Multiply it by c.
    final_rhs = rhs + c*F(2,25)
    assert final_rhs == F(-370024843,4400000000)
    assert final_rhs < 0
    # Left hand side is identically zero, hence 0 <= final_rhs < 0.

    result = {
        "status": "exact_farkas_infeasibility_certificate",
        "reduced_variables": ["q3", "q6", "q13", "u26"],
        "farkas_multipliers": [str(v) for v in y],
        "combined_torque_coefficient": str(c),
        "combined_rhs_before_torque_bound": str(rhs),
        "torque_lower_bound": "u26 >= -2/25",
        "final_contradiction_rhs": str(final_rhs),
        "final_contradiction_rhs_decimal": float(final_rhs),
        "conclusion": "The S2-incidence configuration-constrained fixed-normal RCI LP is infeasible under |tau|<=0.08.",
        "scope": "This excludes the configuration cone preserving the audited S2 vertex incidence; it does not exclude every possible combinatorial configuration using the same 28 normals."
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
