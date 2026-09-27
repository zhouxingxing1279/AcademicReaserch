from fractions import Fraction as Q

def mv(A,x):
    return [sum(A[i][j]*x[j] for j in range(len(x))) for i in range(len(A))]

# Run-90 vertical finite reachable-sum witness
Dz=Q(1043,500)
Fz=[[Q(1),Q(1,50)],[Q(-3,50),Q(2,5)]]
Gz=[Q(0),Q(1,50)]; Kz=[Q(3),Q(30)]
x=Gz[:]; uz_sum=Q(0)
for _ in range(5000):
    uz_sum += abs(sum(Kz[j]*x[j] for j in range(2)))
    x=mv(Fz,x)
Uz_lo=Dz*uz_sum

# Run-93 horizontal/reference finite reachable-sum witnesses
h=Q(1,50); g=Q(981,100)
K=[Q(-1075,10000),Q(-1837,10000),Q(11637,10000),Q(3226,10000)]
A=[[Q(1),h,Q(0),Q(0)],
   [Q(0),Q(1),-h*g,Q(0)],
   [Q(0),Q(0),Q(1),h],
   [Q(0),Q(0),Q(0),Q(1)]]
F=[r[:] for r in A]
for j in range(4): F[3][j]-=K[j]
G=[Q(0),h,Q(0),Q(0)]
D0=Q(3403343,1600000)
dirs={"v":[Q(0),Q(1),Q(0),Q(0)],
      "psi":[Q(0),Q(0),Q(1),Q(0)],
      "mu":K}
s={n:Q(0) for n in dirs}; x=G[:]
for _ in range(1390):
    for n,q in dirs.items():
        s[n]+=abs(sum(q[j]*x[j] for j in range(4)))
    x=mv(F,x)
lo={n:D0*s[n] for n in dirs}

# Product set means vertical and horizontal/attitude factors may be selected independently.
# The finite sums are subsets of their infinite mRPIs. K_fin independently allows
# e_phi=+0.01. For 0<=a<=0.45, sin(a)>=a-a^3/6.
angle=lo["psi"]+Q(1,100)
assert Q(0)<angle<Q(45,100)
sin_lo=angle-angle**3/Q(6)
coupling_lo=Uz_lo*sin_lo
Dbox_min=D0+coupling_lo
scale=Dbox_min/D0

limits={"v":Q(3),"psi":Q(44,100),"mu":Q(672,10000)}
print("Uz finite lower witness",float(Uz_lo))
print("psi finite lower witness",float(lo["psi"]))
print("sin lower",float(sin_lo))
print("mandatory coupling-box halfwidth lower",float(coupling_lo))
print("mandatory total disturbance radius lower",float(Dbox_min))
for n in ("v","psi","mu"):
    witness=lo[n]*scale
    print(n,"scaled finite witness",float(witness),"limit",float(limits[n]))
    assert witness>limits[n]
print("PASS: every state-independent scalar box covering the product-set coupling makes the frozen Run-93 certificate fail v/psi/mu.")
