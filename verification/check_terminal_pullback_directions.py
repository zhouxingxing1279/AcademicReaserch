#!/usr/bin/env python3
"""Exact terminal pullback-direction audit for the certified attitude RPI set."""
from fractions import Fraction as F
import json, argparse

M=((F(1),F(1,50)),(-F(8,25),F(21,25)))
H=((F(1),F(0)),(-F(1),F(0)),(F(4),F(1)),(-F(4),-F(1)))
d=(F(1,100),F(1,100),F(1,25),F(1,25))
g=(F(0),F(1)); eps=F(2,625)

# K = {e: |e_phi|<=1/100, |e_omega+4e_phi|<=1/25}.
# q=(e_phi,s), s=e_omega+4e_phi gives exact support.
def support_K(a):
    a1,a2=a
    # a^T e = (a1-4*a2)e_phi + a2*s
    return abs(a1-4*a2)*F(1,100)+abs(a2)*F(1,25)

def mt(a):
    return tuple(sum(M[i][j]*a[i] for i in range(2)) for j in range(2))

rows=[]
for j,h in enumerate(H):
    pull=mt(h)
    state=support_K(pull)
    noise=abs(sum(h[i]*g[i] for i in range(2)))*eps
    total=state+noise
    assert total <= d[j]
    rows.append({"facet":j,"pullback":[str(x) for x in pull],
                 "state_support":str(state),"noise_support":str(noise),
                 "total":str(total),"bound":str(d[j]),"margin":str(d[j]-total)})
# Terminal correction tau-mu = -8/25 e_phi -4/25 e_omega + eta.
k=(-F(8,25),-F(4,25))
corr=support_K(k)+eps
assert corr == F(8,625)
out={"status":"pass_exact_fraction","terminal_facets":rows,
     "all_terminal_margins_nonnegative":True,
     "torque_correction_support":str(corr),
     "torque_correction_bound":str(F(8,625)),
     "nominal_torque_limit_after_tightening":str(F(42,625)),
     "conclusion":"The certified 2D attitude terminal RPI set passes all terminal pullback directions exactly; all four facet margins are zero. Its exact feedback/noise torque correction support is 8/625, leaving |mu|<=42/625 under |tau|<=2/25."}
ap=argparse.ArgumentParser(); ap.add_argument("--output"); a=ap.parse_args()
s=json.dumps(out,indent=2)+"\n"
if a.output: open(a.output,"x").write(s)
print(s,end="")
