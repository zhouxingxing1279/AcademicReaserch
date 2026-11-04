"""Run302: one position measurement cannot bound hidden initial velocity."""
from fractions import Fraction
T=Fraction(1,10)
for M in (1,10,100,1000):
    # Same p0, y0, applied command and disturbance; opposite hidden velocities.
    p_plus=T*M
    p_minus=-T*M
    assert p_plus-p_minus==2*T*M
    print(f'M={M}: indistinguishable y0=0; next-position diameter={float(2*T*M):g}')
print('PASS: unbounded initial velocity implies no uniform finite one-step position bound')
