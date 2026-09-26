from fractions import Fraction as Q
g=Q(981,100); Tmin=g/2; Dx=Q(47,25)
eps=Q(1,100); psi=Q(41,100); phi=psi-eps
sin_lb=phi-phi**3/Q(6)
margin=Tmin*sin_lb-Dx
assert psi<Q(44,100)
assert psi+eps<Q(45,100)
assert margin==Q(371,12500) and margin>0
print("psi",psi,"phi_min",phi,"sin_lb",sin_lb)
print("horizontal authority margin",margin,float(margin))
print("PASS")
