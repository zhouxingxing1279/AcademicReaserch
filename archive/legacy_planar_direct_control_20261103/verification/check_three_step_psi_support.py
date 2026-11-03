from fractions import Fraction as Q

h,g=Q(1,50),Q(981,100)
K=[Q(-1075,10000),Q(-1837,10000),Q(11637,10000),Q(3226,10000)]
F=[[Q(1),h,0,0],[0,Q(1),-h*g,0],[0,0,Q(1),h],[-K[0],-K[1],-K[2],Q(1)-K[3]]]
G=[Q(0),h,Q(0),Q(0)]
D0=Q(3403343,1600000); Dz=Q(1043,500)
Fz=[[Q(1),Q(1,50)],[Q(-3,50),Q(2,5)]]; Bz=[Q(0),Q(1,50)]; Kz=[Q(3),Q(30)]

def mv(A,x): return [sum(A[i][j]*x[j] for j in range(len(x))) for i in range(len(A))]
def mm(A,B): return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def pw(A,n):
    m=len(A); R=[[Q(i==j) for j in range(m)] for i in range(m)]
    while n:
        if n&1:R=mm(R,A)
        A=mm(A,A); n//=2
    return R
def tr(A): return [list(x) for x in zip(*A)]
def ni(A): return max(sum(abs(z) for z in r) for r in A)
def dot(a,b): return sum(x*y for x,y in zip(a,b))

# Run-90 exact vertical input support certificate.
az=ni(pw(Fz,20)); x=Bz[:]; sz=Q(0)
for _ in range(5000):
    sz+=abs(dot(Kz,x)); x=mv(Fz,x)
bz=Q(0); y=x[:]
for _ in range(20):
    bz+=max(abs(v) for v in y); y=mv(Fz,y)
Uz=Dz*sz+Dz*sum(abs(v) for v in Kz)*bz/(1-az)

# Run-93 horizontal mRPI support certificate.
ah=ni(pw(F,139)); assert ah<1
def hs(q):
    x=G[:]; s=Q(0)
    for _ in range(1390):
        s+=abs(dot(q,x)); x=mv(F,x)
    b=Q(0); y=x[:]
    for _ in range(139):
        b+=max(abs(v) for v in y); y=mv(F,y)
    return D0*s+D0*sum(abs(v) for v in q)*b/(1-ah)

epsi=[Q(0),Q(0),Q(1),Q(0)]
F2=pw(F,2); F3=pw(F,3)
m=dot(epsi,mv(F2,G))
assert m==Q(1837,25000000)
a=mv(tr(F3),epsi)
c=m*Uz
joint=m*D0+Q(1,100)*c+max(hs([a[i]+c*epsi[i] for i in range(4)]),hs([a[i]-c*epsi[i] for i in range(4)]))
box=m*D0+hs(a)+c*(hs(epsi)+Q(1,100))
assert joint < box
assert joint < Q(44,100)
print("m =",m,float(m))
print("joint psi_3 certificate =",float(joint))
print("sequential-box psi_3 certificate =",float(box))
print("strict reduction =",float(box-joint))
print("margin to 0.44 =",float(Q(44,100)-joint))
print("PASS exact-rational three-step psi support comparison")
