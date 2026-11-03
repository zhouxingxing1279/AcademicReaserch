#!/usr/bin/env python3
from fractions import Fraction as F
import argparse,json,numpy as np,sympy as sp
from scipy.optimize import linprog
import check_19pair_cc_seed_cone as cc
def sf(x): return F(int(x.p),int(x.q))
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--output",required=True);args=ap.parse_args()
 S2=cc.build_s2();H=cc.seed_H(cc.orientation_reps(S2));_,_,V,acts=cc.enumerate_vertices(H);Ce=[[F(v) for v in a] for a,_ in H]
 def erow(i,j):
  ids=acts[i];M=sp.Matrix([[sp.Rational(v.numerator,v.denominator) for v in Ce[k]] for k in ids]);L=M.inv();o=[F(0)]*38
  for k in range(4):
   for t,col in enumerate(ids):o[col]+=Ce[j][k]*sf(L[k,t])
  o[j]-=1;return tuple(o)
 def canon(r):
  f=next((x for x in r if x),None)
  return r if f is None else tuple(x/abs(f) for x in r)
 uniq={};zero=0
 for i in range(160):
  for j in range(38):
   r=erow(i,j)
   if not any(r):zero+=1;continue
   uniq.setdefault(canon(r),[]).append((i,j))
 rows=list(uniq);A=np.array([[float(x) for x in r] for r in rows]);S=A/np.max(np.abs(A),axis=1)[:,None];ex=[]
 for i in range(len(rows)):
  m=np.arange(len(rows))!=i;z=linprog(-S[i],A_ub=S[m],b_ub=np.zeros(m.sum()),bounds=[(-1,1)]*38,method="highs")
  if z.success and -z.fun>1e-8:ex.append(i)
 D={(15,5):[((2,19),F(10000,981)),((54,32),F(1,150)),((63,20),F(1,150)),((71,22),F(2500,2943)),((85,31),F(1)),((89,29),F(10000,981))],(17,5):[((2,19),F(10000,981)),((15,33),F(1,75)),((23,21),F(1,150)),((25,33),F(1,75)),((85,31),F(1)),((89,29),F(10000,981))],(60,4):[((18,21),F(1,150)),((25,33),F(1,150)),((33,23),F(2500,2943)),((42,18),F(10000,981)),((76,30),F(1)),((78,28),F(10000,981))],(62,4):[((42,18),F(10000,981)),((52,20),F(1,150)),((54,32),F(1,75)),((60,32),F(1,75)),((76,30),F(1)),((78,28),F(10000,981))]}
 E={rows[k] for k in ex};checks=[]
 for target,terms in D.items():
  acc=[F(0)]*38
  for meta,lam in terms:
   rr=canon(erow(*meta));assert rr in E;acc=[a+lam*b for a,b in zip(acc,rr)]
  assert tuple(acc)==erow(*target);checks.append({"target":target,"terms":[(m,str(l)) for m,l in terms],"exact":True})
 out={"status":"numerical_exposed_reduction_exact_identities","generated_rows":6080,"zero_rows":zero,"unique_nonzero_classes":len(rows),"numerically_exposed_classes":len(ex),"critical_rows":4,"terms_each":6,"all_exact":True,"decompositions":checks,"limitation":"54-class exposure uses floating-point HiGHS; rational identities are exact."}
 open(args.output,"w").write(json.dumps(out,indent=2)+"\n");print(json.dumps(out,indent=2))
if __name__=="__main__":main()
