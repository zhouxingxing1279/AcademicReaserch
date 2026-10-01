"""Vertical terminal RPI gate: necessary authority and a numerical linear-feedback witness.
Run: python verification/check_vertical_general_rpi_gate.py
The finite-horizon sums are numerical evidence, NOT an exact RPI certificate.
"""
import numpy as np

h=0.02
D=2.086
U=4.905
A=np.array([[1.0,h],[0.0,1.0]])
B=np.array([[0.0],[h]])
K=np.array([[3.0,30.0]])
F=A-B@K
eig=np.linalg.eigvals(F)
assert np.max(np.abs(eig))<1.0
N=20000
x=B[:,0].copy()
sp=sv=su=0.0
for _ in range(N):
    sp += abs(x[0]); sv += abs(x[1]); su += abs(float(K@x))
    x=F@x
print("authority necessary U>=D:",U>=D,"margin",U-D)
print("K",K.tolist(),"eig",eig.tolist())
print("N",N,"mRPI partial supports p,v,u",D*sp,D*sv,D*su)
print("limits p,v,u",1.5,3.0,U)
print("tail state norm",np.linalg.norm(x,np.inf))
assert D*sp < 1.5 and D*sv < 3.0 and D*su < U
