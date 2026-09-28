from fractions import Fraction as Q

h,g=Q(1,50),Q(981,100)
K=[Q(-1075,10000),Q(-1837,10000),Q(11637,10000),Q(3226,10000)]
F=[[Q(1),h,0,0],[0,Q(1),-h*g,0],[0,0,Q(1),h],[-K[0],-K[1],-K[2],Q(1)-K[3]]]
G=[Q(0),h,Q(0),Q(0)]
D0=Q(3403343,1600000)

def mv(A,x):
    return [sum(A[i][j]*x[j] for j in range(len(x))) for i in range(len(A))]
def mm(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def pw(A,n):
    m=len(A); R=[[Q(i==j) for j in range(m)] for i in range(m)]
    while n:
        if n&1: R=mm(R,A)
        A=mm(A,A); n//=2
    return R
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def ni(A): return max(sum(abs(z) for z in row) for row in A)

# Exact block contraction reused from Run 106.
M=139
alpha=ni(pw(F,M))
assert alpha < 1

# For S = sum_{i>=0} D0 F^i G [-1,1], certify support in q by
# first M exact terms plus a geometric block tail.
def support_upper(q):
    x=G[:]; head=Q(0)
    for _ in range(M):
        head += abs(dot(q,x))
        x=mv(F,x)
    # For block t>=1, |q^T F^(tM+j)G| <= ||q||_1 ||F^(tM)||_inf ||F^jG||_inf.
    # ||F^(tM)||_inf <= alpha^t. Bound the within-block state sequence exactly.
    y=G[:]; block=Q(0)
    for _ in range(M):
        block += max(abs(v) for v in y)
        y=mv(F,y)
    tail = sum(abs(v) for v in q) * block * alpha/(1-alpha)
    return D0*(head+tail)

dirs={
 "px":[Q(1),0,0,0],
 "vx":[0,Q(1),0,0],
 "psi":[0,0,Q(1),0],
 "rho":[0,0,0,Q(1)],
 "K":K,
}
bounds={name:support_upper(q) for name,q in dirs.items()}

limits={"px":Q(5),"vx":Q(3),"psi":Q(11,25),"rho":Q(2),"K":Q(84,1250)}
for name,b in bounds.items():
    assert b < limits[name], (name,float(b),float(limits[name]))

print("alpha =", float(alpha))
for name,b in bounds.items():
    print(name, "<=", float(b), "margin >=", float(limits[name]-b))
print("PASS: exact-rational block-tail bounds certify nonempty Run-119 terminal state/input margins")
