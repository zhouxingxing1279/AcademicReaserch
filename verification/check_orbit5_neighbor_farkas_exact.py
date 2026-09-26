#!/usr/bin/env python3
"""Repository-reproducible exact Farkas certificate for the orbit-5 neighbor.

Unlike the compact Chapter-59 metadata checker, this script reconstructs the
orbit-5 162-vertex incidence, rebuilds every selected primal row with exact
Fraction/SymPy arithmetic, eliminates paired offsets q_{2k}=q_{2k+1}, and
verifies y^T A = 0 and y^T b = -1 exactly.

Floating-point H/V enumeration is used only to recover the audited active-set
labels.  Once those labels are frozen, the Farkas identity is exact.
"""
from fractions import Fraction as F
from itertools import combinations
import argparse, json
import numpy as np
import sympy as sp
import check_19pair_cc_seed_cone as cc
import check_19pair_symmetric_boundary_orbits as sb

TARGET=((89,29),(78,28))
WITNESS=[
 F('6496979/1000000'),F('124545509499943/750000000000'),
 F('20494169/62500'),F('382262997/500000'),F('555623/100000'),
 F('161890421/1000000'),F('39202023/125000'),F('553209/100000'),
 F('1073061/200000'),F('184454083/1000000'),F('23258533/100000'),
 F('117294627/500000'),F('286720501/1000000'),F('20492919/62500'),
 F('1514927/200000'),F('1753551/250000'),F('21002363/100000'),
 F('46741143/125000'),F('42894653/125000')]
EPS=F(1424999829,625000001924722)
SUPPORT=[
 ('config',15,5,None),('config',17,5,None),
 ('inv',2,7,'981/200'),('inv',2,21,'981/200'),('inv',3,5,'981/200'),
 ('inv',20,11,'981/200'),('inv',34,11,'981/200'),('inv',35,11,'981/200'),
 ('inv',56,6,'981/200'),('inv',56,24,'2943/200'),
 ('inv',102,6,'981/200'),('inv',102,34,'2943/200'),('hard',0,3,1)]
MULT=[
 F(981000,3069803),F(981000,3069803),F(29430,3069803),
 F(15000000,3069803),F(5886000,3069803),F(10000000,3069803),
 F(10000000,3069803),F(5000000,3069803),F(78480,3069803),
 F(40000000,9209409),F(470880,3069803),F(80000000,9209409),
 F(88290,3069803)]
EXPECTED_ACTS={
 0:[0,3,5,6],2:[0,3,6,11],3:[0,3,7,11],15:[0,6,11,19],
 17:[0,6,19,33],20:[0,6,25,35],34:[0,21,23,25],
 35:[0,21,23,33],56:[1,6,24,34],102:[5,6,30,34]}

def sf(x): return F(int(x.p),int(x.q))
def canon(r):
 f=next((x for x in r if x),None)
 return r if f is None else tuple(x/abs(f) for x in r)
def norm(r):
 f=next(x for x in r if x); return tuple(x/f for x in r)

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True); args=ap.parse_args()
 S2=cc.build_s2(); reps=cc.orientation_reps(S2); H0=cc.seed_H(reps)
 _,_,_,acts0=cc.enumerate_vertices(H0)
 Ce0=[[F(v) for v in a] for a,_ in H0]
 def erow(i,j):
  ids=acts0[i]
  M=sp.Matrix([[sp.Rational(v.numerator,v.denominator) for v in Ce0[k]] for k in ids])
  L=M.inv(); o=[F(0)]*38
  for k in range(4):
   for t,col in enumerate(ids): o[col]+=Ce0[j][k]*sf(L[k,t])
  o[j]-=1; return tuple(o)
 uniq={}
 for i in range(160):
  for j in range(38):
   r=erow(i,j)
   if any(r): uniq.setdefault(canon(r),[]).append((i,j))
 rows=list(uniq); rid={r:i for i,r in enumerate(rows)}
 prows=[tuple(r[2*k]+r[2*k+1] for k in range(19)) for r in rows]
 restricted={}
 for idx,r in enumerate(prows):
  if any(r):
   f=next(x for x in r if x); restricted.setdefault(tuple(x/abs(f) for x in r),[]).append(idx)
 rr=list(restricted)
 ka=rid[canon(erow(*TARGET[0]))]
 kt=next(i for i,r in enumerate(rr) if norm(r)==norm(prows[ka]))
 rt=rr[kt]
 assert sum(rt[k]*WITNESS[k] for k in range(19))==0
 assert min(WITNESS)>0
 # Recheck that the stored epsilon is a certified one-class crossing.
 splus=[WITNESS[k]+EPS*rt[k] for k in range(19)]
 assert min(splus)>0
 assert sum(rt[k]*splus[k] for k in range(19))>0
 for i,r in enumerate(rr):
  if i==kt: continue
  assert sum(r[k]*splus[k] for k in range(19))<0
 # Lift paired offsets and recover the audited orbit-5 incidence.
 H=[]
 for k,a in enumerate(reps):
  H += [(a,splus[k]),(tuple(-v for v in a),splus[k])]
 C,q,V,acts=cc.enumerate_vertices(H)
 assert len(H)==38 and len(V)==162 and all(len(a)==4 for a in acts)
 for i,a in EXPECTED_ACTS.items(): assert acts[i]==a
 Ce=[[F(v) for v in a] for a,_ in H]
 nq=38; nv=162; nfull=nq+nv
 def Linv(i):
  ids=acts[i]
  M=sp.Matrix([[sp.Rational(v.numerator,v.denominator) for v in Ce[k]] for k in ids])
  return ids,M.inv()
 def row(meta):
  typ,i,j,z=meta; ids,L=Linv(i); out=[F(0)]*nfull
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
  # Eliminate q_{2k}=q_{2k+1}; this is the actual 19-pair variable space.
  reduced=[out[2*k]+out[2*k+1] for k in range(19)]+out[38:]
  return reduced,rhs
 selected=[row(m) for m in SUPPORT]
 combo=[sum(MULT[i]*selected[i][0][j] for i in range(13))
        for j in range(19+nv)]
 bsum=sum(MULT[i]*selected[i][1] for i in range(13))
 assert all(y>0 for y in MULT)
 assert all(v==0 for v in combo)
 assert bsum==F(-1)
 result={
  'status':'repository_reproducible_exact_orbit5_farkas',
  'orbit5_vertices':len(V),'raw_facets':len(H),'entirely_simple':True,
  'crossing_epsilon':str(EPS),'support_rows':13,
  'reduced_pair_offset_variables':19,'vertex_control_variables':nv,
  'all_multipliers_strictly_positive':True,'weighted_lhs_zero_exact':True,
  'weighted_rhs_exact':str(bsum),'torque_bound_rows_used':0,
  'support':[{'row':list(m),'active_set':acts[m[1]],'multiplier':str(y)}
             for m,y in zip(SUPPORT,MULT)],
  'certificate_statement':
   'After exact elimination of paired offsets, the 13 selected valid inequalities have positive rational multipliers with y^T A = 0 and y^T b = -1. Hence the audited orbit-5 neighboring CC-RCI system is infeasible by Farkas lemma, even without vertex torque bounds.',
  'scope':
   'Exact conditional on the numerically enumerated 162-vertex active-set incidence; the selected primal rows and Farkas identity are reconstructed and checked exactly from repository code.'
 }
 open(args.output,'w').write(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))

if __name__=='__main__': main()
