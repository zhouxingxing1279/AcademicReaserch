#!/usr/bin/env python3
"""Find a minimum subset of S3\S2 facets that removes all nonviable S2 vertices.

Fraction arithmetic builds predecessor inequalities. HiGHS is used for
redundancy, vertex feasibility, and the final 0-1 set-cover MILP. The result is
therefore a numerical/combinatorial audit, not an exact RCI certificate.
"""
from fractions import Fraction as F
from itertools import combinations
import json, argparse
import numpy as np
from scipy.optimize import linprog, milp, LinearConstraint, Bounds

h=F('0.02'); J=F('0.02'); TL=F('4.905'); TU=F('14.715'); taum=F('0.08')
d0=F('1.880'); c=F(9,20)**3/6
B=[F(0),F(0),F(0),h/J]; E=[F(0),h,F(0),F(0)]

def A(T): return [[1,h,0,0],[0,1,-h*T,0],[0,0,1,h],[0,0,0,1]]
def mm(r,M): return [sum(r[k]*M[k][j] for k in range(4)) for j in range(4)]
def canon(a,b):
    first=next((x for x in a if x),None)
    if first is None: return tuple(a),b
    s=abs(F(first)); return tuple(F(x)/s for x in a),F(b)/s

def dedup(H):
    out={}
    for a,b in H:
        aa,bb=canon(a,b)
        if aa not in out or bb<out[aa]: out[aa]=bb
    return [(a,b) for a,b in out.items()]

def arrays(H):
    AA=[]; bb=[]
    for a,b in H:
        row=np.array([float(x) for x in a]); rhs=float(b)
        s=max(np.max(np.abs(row)),abs(rhs),1e-12); AA.append(row/s); bb.append(rhs/s)
    return np.array(AA),np.array(bb)

def reduce(H,tol=1e-8):
    H=dedup(H); AA,bb=arrays(H); keep=[]
    for i,item in enumerate(H):
        m=np.arange(len(H))!=i
        z=linprog(-AA[i],A_ub=AA[m],b_ub=bb[m],bounds=[(None,None)]*4,method='highs')
        if (not z.success) or -z.fun>bb[i]+tol: keep.append(item)
    return keep

def pre(H):
    cs=[]
    for r,q in H:
        for T in (TL,TU):
            a=tuple(mm(r,A(T))); beta=sum(r[i]*B[i] for i in range(4))
            sup=abs(sum(r[i]*E[i] for i in range(4)))*(d0+c*T)
            cs.append((a,beta,q-sup))
    z=(F(0),)*4; cs += [(z,F(1),taum),(z,F(-1),taum)]
    lo=[]; up=[]; zero=[]
    for a,b,r in cs: (zero if b==0 else up if b>0 else lo).append((a,b,r))
    out=[(a,r) for a,_,r in zero]
    for al,bl,rl in lo:
        for au,bu,ru in up:
            out.append((tuple(bu*al[i]-bl*au[i] for i in range(4)),bu*rl-bl*ru))
    return out

def vertices(H):
    AA=np.array([[float(x) for x in a] for a,b in H]); bb=np.array([float(b) for a,b in H]); V=[]
    for ids in combinations(range(len(H)),4):
        M=AA[list(ids)]
        if abs(np.linalg.det(M))<1e-10: continue
        x=np.linalg.solve(M,bb[list(ids)])
        if np.all(AA@x<=bb+1e-7) and not any(np.linalg.norm(x-v)<1e-6 for v in V): V.append(x)
    return V

def viable(x,H):
    lo,up=-float(taum),float(taum)
    for r,q in H:
        rf=np.array([float(v) for v in r])
        beta=float(sum(r[i]*B[i] for i in range(4)))
        for T in (TL,TU):
            sup=float(abs(sum(r[i]*E[i] for i in range(4)))*(d0+c*T))
            rhs=float(q)-sup-rf@(np.array([[float(v) for v in row] for row in A(T)])@x)
            if abs(beta)<1e-12:
                if rhs < -1e-8: return False
            elif beta>0: up=min(up,rhs/beta)
            else: lo=max(lo,rhs/beta)
    return lo<=up+1e-8

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True); args=ap.parse_args()
    X=[]
    for i,w in enumerate([F(5),F(3),F('0.45'),F(2)]):
        e=[F(0)]*4; e[i]=1; X.append((tuple(e),w)); e=[F(0)]*4; e[i]=-1; X.append((tuple(e),w))
    S1=reduce(X+pre(X)); S2=reduce(X+pre(S1)); S3=reduce(X+pre(S2))
    V=vertices(S2); bad=[i for i,x in enumerate(V) if not viable(x,S2)]
    n2={a for a,b in S2}; new=[(a,b) for a,b in S3 if a not in n2]
    C=np.zeros((len(bad),len(new)))
    for j,(a,b) in enumerate(new):
        af=np.array([float(v) for v in a]); bf=float(b)
        for ii,k in enumerate(bad): C[ii,j]=af@V[k] > bf+1e-7
    sol=milp(np.ones(len(new)),integrality=np.ones(len(new)),bounds=Bounds(0,1),
             constraints=LinearConstraint(C,np.ones(len(bad)),np.full(len(bad),np.inf)))
    assert sol.success
    chosen=np.where(sol.x>.5)[0]
    assert len(chosen)==10 and np.all(C[:,chosen].sum(axis=1)>=1)
    rows=[]
    for j in chosen:
        a,b=new[j]; rows.append({'normal':[str(v) for v in a],'rhs':str(b),'bad_vertices_cut':int(C[:,j].sum())})
    result={'status':'numerical_minimum_set_cover_audit','S2_facets':len(S2),'S3_facets':len(S3),
            'S2_vertices':len(V),'S2_nonviable_vertices':len(bad),'S2_viable_vertices':len(V)-len(bad),
            'new_S3_halfspaces':len(new),'minimum_new_halfspaces':len(chosen),'minimum_symmetric_pairs':5,
            'selected_facets':rows,
            'conclusion':'Within the audited S3\\S2 candidate pool, at least 10 halfspaces (5 symmetric pairs) are required to cut every S2 vertex that lacks an admissible endpoint-robust torque into S2.',
            'limitation':'Vertex removal is necessary geometry triage only; it does not prove the augmented template is RCI or that 5 pairs are globally minimal outside the S3 candidate pool.'}
    open(args.output,'w').write(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))
if __name__=='__main__': main()
