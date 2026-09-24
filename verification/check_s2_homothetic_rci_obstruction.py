#!/usr/bin/env python3
"""Exact certificate that no contraction alpha*S2, 0<alpha<=1, is RCI.

The witness and offending S2 facet come from the endpoint-exact projected
predecessor audit in Chapter 42. Fraction arithmetic only; no optimizer.
"""
from fractions import Fraction as F
import json
from pathlib import Path
import argparse


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    h = F(1, 50)
    TL = F(981, 200)  # 4.905
    d0 = F(47, 25)    # 1.880
    c = F(9, 20) ** 3 / 6

    # S2 facet r^T x <= q retained by the Chapter-42 audit.
    r = [F(-1), F(-1, 25), F(981, 500000), F(0)]
    q = F(39993745617, 8000000000)

    # Exact S2 vertex: intersection of -p<=5, -p-hv<=5,
    # omega<=2 and the facet above.
    phi = F(-6254383, 15696000)
    vtx = [F(-5), F(0), phi, F(2)]

    # A(T) for x=[p,v,phi,omega].
    A = [[F(1), h, F(0), F(0)],
         [F(0), F(1), -h*TL, F(0)],
         [F(0), F(0), F(1), h],
         [F(0), F(0), F(0), F(1)]]
    Av = [sum(A[i][j]*vtx[j] for j in range(4)) for i in range(4)]
    nominal_slack_coefficient = q - sum(r[i]*Av[i] for i in range(4))

    # d enters v+ as h*d, so support is |r_v| h dbar(TL).
    dbar = d0 + c*TL
    disturbance_support = abs(r[1]) * h * dbar
    gap = disturbance_support - nominal_slack_coefficient

    assert nominal_slack_coefficient == F(5940463, 4000000000)
    assert disturbance_support == F(6254383, 4000000000)
    assert gap == F(981, 12500000)
    assert gap > 0

    # For alpha*S2 at alpha*vtx, the robust facet condition is
    # alpha*(q-r^T A vtx) >= support. Since alpha<=1 and coeff<support,
    # it fails for every 0<alpha<=1. r^T B=0, so torque cannot repair it.
    result = {
        "status": "exact_obstruction",
        "witness_vertex": [str(x) for x in vtx],
        "offending_facet_r": [str(x) for x in r],
        "offending_facet_q": str(q),
        "thrust_endpoint": str(TL),
        "nominal_slack_coefficient": str(nominal_slack_coefficient),
        "disturbance_support": str(disturbance_support),
        "support_minus_slack": str(gap),
        "support_minus_slack_decimal": float(gap),
        "critical_alpha": str(disturbance_support / nominal_slack_coefficient),
        "critical_alpha_decimal": float(disturbance_support / nominal_slack_coefficient),
        "torque_coefficient": "0",
        "conclusion": "No homothetic contraction alpha*S2 with 0<alpha<=1 is robust control invariant."
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
