from fractions import Fraction as Q

h = Q(1, 50)
g = Q(981, 100)
K = [Q(-1075,10000), Q(-1837,10000), Q(11637,10000), Q(3226,10000)]

A = [
    [Q(1), h, Q(0), Q(0)],
    [Q(0), Q(1), -h*g, Q(0)],
    [Q(0), Q(0), Q(1), h],
    [Q(0), Q(0), Q(0), Q(1)],
]
Bmu = [Q(0), Q(0), Q(0), Q(1)]
F = [[A[i][j] - Bmu[i]*K[j] for j in range(4)] for i in range(4)]
G = [Q(0), h, Q(0), Q(0)]  # scalar horizontal coupling enters v_x only

def mv(M, v):
    return [sum(M[i][j]*v[j] for j in range(4)) for i in range(4)]

FG = mv(F, G)
F2G = mv(F, FG)

# x1 = F x0 + G c0
# x2 = F^2 x0 + F G c0 + G c1
# x3 = F^3 x0 + F^2 G c0 + F G c1 + G c2
assert G[2] == 0
assert FG[2] == 0
assert F2G[2] == Q(1837, 25000000)
assert F2G[2] > 0

print("e_psi^T G    =", G[2])
print("e_psi^T F G  =", FG[2])
print("e_psi^T F^2G =", F2G[2], "=", float(F2G[2]))
print("PASS: coupling cannot change psi at horizons 1 or 2; first possible effect is horizon 3.")
