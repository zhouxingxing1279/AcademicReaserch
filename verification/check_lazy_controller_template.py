#!/usr/bin/env python3
"""Run 102: exact checks for lazy/selective fixed-template update contracts."""
from fractions import Fraction as Q

# Toy set X = {(t,-t): |t|<=1}; exact support h_X(d)=|d1-d2|.
def h_x(d):
    return abs(d[0]-d[1])

# Reliable prior caps in directions H.
H=[(Q(1),Q(0)),(Q(-1),Q(0)),(Q(0),Q(1)),(Q(0),Q(-1)),(Q(1),Q(1)),(Q(-1),Q(-1))]
beta=[h_x(d) for d in H]

# Measurement/update consistent set C = X intersect {|x1|<=1/2}.
# Parametrically C={(t,-t): |t|<=1/2}; exact supports halve.
def h_c(d):
    return Q(1,2)*abs(d[0]-d[1])

U=[h_c(d) for d in H]
refresh={0,1}  # only +/- e1 refreshed
beta_new=[min(U[i],beta[i]) if i in refresh else beta[i] for i in range(len(H))]

# Theorem checks: C retained and new template nested in old template.
assert all(h_c(H[i]) <= beta_new[i] <= beta[i] for i in range(len(H)))
assert beta_new[0] == beta_new[1] == Q(1,2)
assert beta_new[2] == beta_new[3] == Q(1)
# Unrefreshed correlation facets remain valid; no false tightening is claimed.
assert beta_new[4] == beta_new[5] == 0

# Affine propagation: A=[[1,1],[0,1]], q=e1 requires A^T q=(1,1),
# which is in H. Stored zero cap proves exact zero next support without an LP.
q=(Q(1),Q(0))
Atq=(Q(1),Q(1))
idx=H.index(Atq)
assert beta_new[idx] == 0
assert h_c(Atq) == 0

print("PASS selective refresh containment/nestedness")
print("PASS unrefreshed facets remain valid old caps")
print("PASS backward-closed stored direction answers affine successor support without new optimization")
print("refreshed_facets",len(refresh),"total_facets",len(H))
