from fractions import Fraction as Q

h,g=Q(1,50),Q(981,100)
K=[Q(-1075,10000),Q(-1837,10000),Q(11637,10000),Q(3226,10000)]
F=[[Q(1),h,0,0],[0,Q(1),-h*g,0],[0,0,Q(1),h],[-K[0],-K[1],-K[2],Q(1)-K[3]]]
G=[Q(0),h,Q(0),Q(0)]; D0=Q(3403343,1600000)
Dz=Q(1043,500); Fz=[[Q(1),Q(1,50)],[Q(-3,50),Q(2,5)]]
Bz=[Q(0),Q(1,50)]; Kz=[Q(3),Q(30)]

def mv(A,x): return [sum(A[i][j]*x[j] for j in range(len(x))) for i in range(len(A))]
def mm(A,B): return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def pw(A,n):
    m=len(A); R=[[Q(i==j) for j in range(m)] for i in range(m)]
    while n:
        if n&1:R=mm(R,A)
        A=mm(A,A); n//=2
    return R
def tr(A): return [list(x) for x in zip(*A)]
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def ni(A): return max(sum(abs(z) for z in r) for r in A)

# Run-90 exact vertical-input support used by the Run-99 q+/q- seeds.
az=ni(pw(Fz,20)); x=Bz[:]; sz=Q(0)
for _ in range(5000):
    sz+=abs(dot(Kz,x)); x=mv(Fz,x)
bz=Q(0); y=x[:]
for _ in range(20):
    bz+=max(abs(v) for v in y); y=mv(Fz,y)
Uz=Dz*sz+Dz*sum(abs(v) for v in Kz)*bz/(1-az)

epsi=[Q(0),Q(0),Q(1),Q(0)]
m=dot(epsi,mv(pw(F,2),G)); assert m==Q(1837,25000000)
a=mv(tr(pw(F,3)),epsi); C=m*Uz
seeds=[[Q(0),Q(1),Q(0),Q(0)],epsi,K[:],
       [a[i]+C*epsi[i] for i in range(4)],
       [a[i]-C*epsi[i] for i in range(4)]]

# Unsigned H15; symmetry certifies the corresponding negative facet.
dirs=[]
Ft=tr(F)
for si,seed in enumerate(seeds):
    q=seed
    for depth in range(16):
        dirs.append((si,depth,q))
        q=mv(Ft,q)
assert len(dirs)==80

# First 600 exact generators.
gens=[]; x=G[:]
for _ in range(600):
    gens.append([D0*v for v in x]); x=mv(F,x)

# Certified absolute p_x radius of every generator after index 599.
M=139; alpha=ni(pw(F,M)); assert alpha<1
b=Q(0); y=x[:]
for _ in range(M):
    b+=abs(y[0]); y=mv(F,y)
tail=D0*b/(1-alpha)

strip=Q(1,50)
threshold=Q(139,500) # 0.278; implies separation > 0.258 from the strip.
minimum=None
for si,depth,q in dirs:
    center=Q(0); free=Q(0)
    for gen in gens:
        s=dot(q,gen)
        if s>0: center+=gen[0]
        elif s<0: center-=gen[0]
        else: free+=abs(gen[0])
    # Zero q-dot generators are free on the exposed face. All unmaterialized
    # generators are conservatively free, so this is a lower bound on |p_x|
    # for every point of the infinite q-exposed face.
    lower=abs(center)-free-tail
    assert lower>threshold
    if minimum is None or lower<minimum[0]:
        minimum=(lower,si,depth)

assert minimum[1:] in ((3,15),(4,15))
assert minimum[0]-strip>Q(129,500) # strict separation > 0.258
print("tail600 <=",float(tail))
print("minimum exposed-face |px| lower bound =",float(minimum[0]),"seed/depth",minimum[1:])
print("minimum separation from |px|<=0.02 >",float(minimum[0]-strip))
print("PASS: all 160 signed H15 infinite-mRPI exposed faces are disjoint from the position strip")
