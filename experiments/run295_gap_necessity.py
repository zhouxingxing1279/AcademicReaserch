"""Run295 finite-window endpoint-velocity bound: finite vertex regression, not a proof."""
from itertools import product

T, A_BAR, NU_BAR = 0.1, 0.2, 0.05
checks = 0
for d in range(1, 7):
    for accelerations in product((-A_BAR, A_BAR), repeat=d):
        for n0, nd in product((-NU_BAR, NU_BAR), repeat=2):
            p = v = 0.0
            for a in accelerations:
                p += T * v + 0.5 * T * T * a
                v += T * a
            vhat = (p + nd - n0) / (d * T)
            beta = 2 * NU_BAR / (d * T) + 0.5 * d * T * A_BAR
            assert abs(v - vhat) <= beta + 1e-12
            checks += 1
print(f"PASS: endpoint velocity envelope, 6 horizons, vertex noise/accelerations; {checks} cases")
