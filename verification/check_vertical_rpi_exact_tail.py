from fractions import Fraction as Q
D,U=Q(1043,500),Q(981,200)
F=[[Q(1),Q(1,50)],[Q(-3,50),Q(2,5)]]
B=[Q(0),Q(1,50)]; K=[Q(3),Q(30)]; N=5000; M=20
def mm(A,C): return [[sum(A[i][k]*C[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def mv(A,x): return [sum(A[i][j]*x[j] for j in range(2)) for i in range(2)]
def pw(A,n):
 R=[[Q(1),Q(0)],[Q(0),Q(1)]]; X=A
 while n:
  if n&1:R=mm(R,X)
  X=mm(X,X); n//=2
 return R
def ni(A): return max(sum(abs(z) for z in r) for r in A)
alpha=ni(pw(F,M)); assert alpha<1
dirs={"p":([Q(1),Q(0)],Q(3,2)),"v":([Q(0),Q(1)],Q(3)),"u":(K,U)}
s={n:Q(0) for n in dirs}; x=B[:]
for _ in range(N):
 for n,(q,_) in dirs.items(): s[n]+=abs(sum(q[j]*x[j] for j in range(2)))
 x=mv(F,x)
block=Q(0); y=x[:]
for _ in range(M):
 block+=max(abs(y[0]),abs(y[1])); y=mv(F,y)
print("alpha",alpha,float(alpha))
for n,(q,lim) in dirs.items():
 fin=D*s[n]; tail=D*sum(abs(z) for z in q)*block/(1-alpha); cert=fin+tail
 assert cert<lim
 print(n,"finite",float(fin),"tail",float(tail),"cert",float(cert),"limit",float(lim),"margin",float(lim-cert))
print("PASS exact-rational infinite-horizon certificate")
