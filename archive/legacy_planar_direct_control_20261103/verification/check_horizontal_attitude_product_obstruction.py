from fractions import Fraction as F
h=F(1,50); Dx=F(47,25); dv=h*Dx
vx=F(0); px=F(0); first=None
for k in range(80):
    px += h*vx
    vx += dv
    if first is None and abs(vx)>F(3): first=k+1
assert dv==F(47,1250)
assert first==80
assert vx==F(376,125)
assert px==F(14852,6250)
assert abs(px)<F(5)
print('PASS', first, vx, px)
