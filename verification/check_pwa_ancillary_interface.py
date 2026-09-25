#!/usr/bin/env python3
"""Exact rational check for the PWA ancillary-interface proposition."""
from fractions import Fraction as F
from itertools import product

V=[(F(-1),F(-1)),(F(1),F(-1)),(F(1),F(1)),(F(-1),F(1))]
U=[F(1),F(-1,10),F(-1),F(3,10)]
A=((F(1,2),F(0)),(F(0),F(1,2)))
B=(F(1,5),F(1,10))
W=list(product((F(-1,10),F(1,10)), repeat=2))

def succ(x,u,w):
    return tuple(sum(A[i][j]*x[j] for j in range(2))+B[i]*u+w[i] for i in range(2))

# Vertex-control robust invariance: convex E=[-1,1]^2, so disturbance vertices suffice.
for x,u in zip(V,U):
    for w in W:
        y=succ(x,u,w)
        assert all(F(-1) <= z <= F(1) for z in y), (x,u,w,y)

# All controls satisfy the convex error-input set [-1,1].
assert min(U)>=-1 and max(U)<=1

# The assignment is not one global affine law u=a*x+b.
# Solve first three equations exactly, then show failure at the fourth.
# From v0,v1: 2*a1 = u1-u0. From v1,v2: 2*a2 = u2-u1.
a1=(U[1]-U[0])/2
a2=(U[2]-U[1])/2
b=U[0]-a1*V[0][0]-a2*V[0][1]
pred4=a1*V[3][0]+a2*V[3][1]+b
assert pred4 != U[3]

# Two-triangle PWA interpolation uses convex combinations of vertex controls.
# Exact sample barycentric combinations; input remains in convex hull [min U,max U].
samples=[
    ([F(1,3),F(1,3),F(1,3)],[0,1,2]),
    ([F(1,4),F(1,2),F(1,4)],[0,2,3]),
]
for lam,ids in samples:
    assert sum(lam)==1 and all(t>=0 for t in lam)
    u=sum(lam[k]*U[i] for k,i in enumerate(ids))
    assert min(U)<=u<=max(U)

print({
 "vertex_disturbance_cases":len(V)*len(W),
 "rci_exact":True,
 "vertex_control_range":[str(min(U)),str(max(U))],
 "global_affine_fit_fails_at_v4":True,
 "affine_prediction_v4":str(pred4),
 "actual_v4":str(U[3]),
 "input_support_plus":str(max(U)),
 "input_support_minus":str(-min(U)),
})
