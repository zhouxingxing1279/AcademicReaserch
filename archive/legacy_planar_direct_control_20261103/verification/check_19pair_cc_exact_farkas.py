#!/usr/bin/env python3
"""Exact Farkas certificate for the chapter-48 19-pair CC cone.

The 25-row support was discovered numerically from the unbounded-torque LP.
This script rebuilds the seed active sets, reconstructs every selected row with
Fraction/SymPy rational arithmetic, and verifies y^T A = 0 and y^T b < 0.
Thus the final infeasibility check is exact; numerical geometry is used only to
identify the audited seed configuration/vertex labels from chapter 48.
"""
from fractions import Fraction as F
import argparse, json
import numpy as np
import sympy as sp
import check_19pair_cc_seed_cone as cc

# (kind, vertex index, target facet, thrust/sign).  For hard rows the last two
# entries are state coordinate and sign.
SUPPORT = [
 ('config',15,5,None),('config',17,5,None),('config',60,4,None),('config',62,4,None),
 ('inv',2,7,'981/200'),('inv',2,21,'981/200'),('inv',3,5,'981/200'),
 ('inv',8,7,'981/200'),('inv',8,25,'2943/200'),('inv',20,11,'981/200'),
 ('inv',34,11,'981/200'),('inv',35,11,'981/200'),('inv',40,4,'981/200'),
 ('inv',42,6,'981/200'),('inv',42,20,'981/200'),('inv',65,10,'981/200'),
 ('inv',72,10,'981/200'),('inv',73,10,'981/200'),('inv',96,7,'981/200'),
 ('inv',96,35,'2943/200'),('inv',102,6,'981/200'),('inv',102,34,'2943/200'),
 ('inv',121,6,'981/200'),('inv',121,24,'2943/200'),('hard',3,3,-1),
]
MULT = [
 F(100,27),F(100,27),F(200,27),F(200,27),F(1,9),F(500000,8829),F(200,9),
 F(8,27),F(4000000,79461),F(1000000,26487),F(1000000,26487),F(500000,26487),
 F(400,9),F(2,9),F(1000000,8829),F(2000000,26487),F(2000000,26487),
 F(1000000,26487),F(32,9),F(16000000,79461),F(16,9),F(8000000,79461),
 F(16,27),F(8000000,79461),F(1),
]
EXPECTED_ACTS = {
 2:[0,3,6,11],3:[0,3,7,11],8:[0,4,7,35],15:[0,6,11,19],17:[0,6,19,33],
 20:[0,6,25,35],34:[0,21,23,25],35:[0,21,23,33],40:[1,2,6,10],
 42:[1,2,7,10],60:[1,7,10,18],62:[1,7,18,32],65:[1,7,24,34],
 72:[1,20,22,24],73:[1,20,22,32],96:[4,7,31,35],102:[5,6,30,34],
 121:[6,24,30,34],
}

def sf(x):
    return F(int(x.p),int(x.q))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True); args=ap.parse_args()
    S2=cc.build_s2(); reps=cc.orientation_reps(S2); H=cc.seed_H(reps)
    C,q,V,acts=cc.enumerate_vertices(H)
    assert len(H)==38 and len(V)==160 and all(len(a)==4 for a in acts)
    for i,a in EXPECTED_ACTS.items(): assert acts[i]==a
    Ce=[[F(v) for v in a] for a,_ in H]
    nq=38; nv=160; nvar=nq+nv
    def Linv(i):
        ids=acts[i]
        M=sp.Matrix([[sp.Rational(v.numerator,v.denominator) for v in Ce[k]] for k in ids])
        return ids,M.inv()
    def row(meta):
        typ,i,j,z=meta; ids,L=Linv(i); out=[F(0)]*nvar
        if typ=='config':
            for k in range(4):
                for t,col in enumerate(ids): out[col]+=Ce[j][k]*sf(L[k,t])
            out[j]-=1; rhs=F(0)
        elif typ=='inv':
            T=F(z); ra=cc.base.mm(Ce[j],cc.base.A(T))
            for k in range(4):
                for t,col in enumerate(ids): out[col]+=ra[k]*sf(L[k,t])
            out[j]-=1
            out[nq+i]=sum(Ce[j][k]*cc.base.B[k] for k in range(4))
            rhs=-abs(sum(Ce[j][k]*cc.base.E[k] for k in range(4)))*(cc.base.d0+cc.base.c*T)
        else:
            k=j; sg=F(z)
            for t,col in enumerate(ids): out[col]+=sg*sf(L[k,t])
            rhs=[F(5),F(3),F('0.45'),F(2)][k]
        return out,rhs
    rows=[]; rhs=[]
    for m in SUPPORT:
        r,b=row(m); rows.append(r); rhs.append(b)
    combo=[sum(MULT[k]*rows[k][j] for k in range(len(rows))) for j in range(nvar)]
    bsum=sum(MULT[k]*rhs[k] for k in range(len(rows)))
    assert all(y>0 for y in MULT)
    assert all(v==0 for v in combo)
    assert bsum==F(-3069803,88290) and bsum<0
    result={
      'status':'exact_farkas_certificate_for_audited_19pair_cone',
      'support_rows':len(SUPPORT),'all_multipliers_strictly_positive':True,
      'torque_bound_rows_used':0,'pair_offset_equality_rows_used':0,'q_nonnegativity_rows_used':0,
      'weighted_lhs_zero_exact':True,'weighted_rhs':str(bsum),'weighted_rhs_float':float(bsum),
      'certificate_statement':'The 25 selected valid inequalities have positive rational multipliers whose weighted left-hand side is identically zero while the weighted right-hand side is -3069803/88290 < 0. Hence this audited configuration-cone robust-invariance system is infeasible by Farkas lemma, even with unbounded vertex torque.',
      'scope':'Exact for the chapter-48 audited configuration cone and its stated endpoint-robust/hard-state inequalities; it does not exclude other configuration cones of the same 19-pair orientation family.',
      'support':[{'row':list(m),'active_set':acts[m[1]],'multiplier':str(y)} for m,y in zip(SUPPORT,MULT)]
    }
    open(args.output,'w').write(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2))
if __name__=='__main__': main()
