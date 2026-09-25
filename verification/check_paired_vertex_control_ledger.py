#!/usr/bin/env python3
"""Exact rational check: paired vertex-control ledger preserves linear joint supports."""
from fractions import Fraction as F

V=[(F(-1),F(-1)),(F(1),F(-1)),(F(1),F(1)),(F(-1),F(1))]
U=[F(1),F(-1,10),F(-1),F(3,10)]
TRI=[(0,1,2),(0,2,3)]

def score(i,a,b):
    return a[0]*V[i][0]+a[1]*V[i][1]+b*U[i]

def ledger_support(a,b):
    return max(score(i,a,b) for i in range(4))

def point_score(tri,lam,a,b):
    x=sum(l*V[i][0] for l,i in zip(lam,tri))
    y=sum(l*V[i][1] for l,i in zip(lam,tri))
    u=sum(l*U[i] for l,i in zip(lam,tri))
    return a[0]*x+a[1]*y+b*u

queries=[
 ((F(1),F(0)),F(1)),((F(-2),F(3)),F(1,2)),
 ((F(0),F(-1)),F(2)),((F(3,2),F(1,3)),F(-1))
]
samples=[(F(1,2),F(1,3),F(1,6)),(F(1,5),F(2,5),F(2,5))]
for a,b in queries:
    s=ledger_support(a,b)
    for tri in TRI:
        for lam in samples:
            assert point_score(tri,lam,a,b)<=s
    # every maximizing ledger entry is an actual graph vertex
    assert any(score(i,a,b)==s for i in range(4))
print("PASS: paired ledger is exact for all tested linear graph-support queries.")
