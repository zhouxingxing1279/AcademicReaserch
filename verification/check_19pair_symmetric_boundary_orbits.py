#!/usr/bin/env python3
"""Exact center-symmetric exposure certificates for the eight Chapter-53 boundary orbits.

The full 38-offset configuration cone is restricted to q_{2k}=q_{2k+1}.
Each Chapter-53 symmetry pair then collapses to one row in 19 pair-offset
coordinates. HiGHS only discovers a positive relative-interior point; the
reported target equality, positivity, and strict separation from every other
restricted row class are checked with Fraction arithmetic.
"""
from fractions import Fraction as F
import argparse,json,numpy as np,sympy as sp
from scipy.optimize import linprog
import check_19pair_cc_seed_cone as cc

ORBITS=[((2,19),(42,18)),((54,32),(25,33)),((63,20),(18,21)),((71,22),(33,23)),
        ((85,31),(76,30)),((89,29),(78,28)),((15,33),(60,32)),((23,21),(52,20))]
def sf(x): return F(int(x.p),int(x.q))
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--output",required=True);args=ap.parse_args()
 S2=cc.build_s2();H=cc.seed_H(cc.orientation_reps(S2));_,_,_,acts=cc.enumerate_vertices(H)
 Ce=[[F(v) for v in a] for a,_ in H]
 def erow(i,j):
  ids=acts[i];M=sp.Matrix([[sp.Rational(v.numerator,v.denominator) for v in Ce[k]] for k in ids]);L=M.inv();o=[F(0)]*38
  for k in range(4):
   for t,col in enumerate(ids):o[col]+=Ce[j][k]*sf(L[k,t])
  o[j]-=1;return tuple(o)
 def canon(r):
  f=next((x for x in r if x),None)
  return r if f is None else tuple(x/abs(f) for x in r)
 uniq={}
 for i in range(160):
  for j in range(38):
   r=erow(i,j)
   if any(r):uniq.setdefault(canon(r),[]).append((i,j))
 rows=list(uniq);rid={r:i for i,r in enumerate(rows)}
 def pairrow(r): return tuple(r[2*k]+r[2*k+1] for k in range(19))
 prows=[pairrow(r) for r in rows]
 def norm(r):
  f=next(x for x in r if x);return tuple(x/f for x in r)
 certs=[]
 for oa,ob in ORBITS:
  ka=rid[canon(erow(*oa))];kb=rid[canon(erow(*ob))]
  assert norm(prows[ka])==norm(prows[kb])
  restricted={}
  for idx,r in enumerate(prows):
   if any(r):
    f=next(x for x in r if x);cr=tuple(x/abs(f) for x in r);restricted.setdefault(cr,[]).append(idx)
  rr=list(restricted);kt=next(i for i,r in enumerate(rr) if norm(r)==norm(prows[ka]))
  A=np.array([[float(x) for x in r] for r in rr]);mask=[i for i in range(len(rr)) if i!=kt]
  z=linprog(np.zeros(19),A_ub=A[mask],b_ub=-np.ones(len(mask)),A_eq=A[[kt]],b_eq=[0.],
            bounds=[(1,None)]*19,method="highs")
  assert z.success
  s=[F(round(float(x)*1000000),1000000) for x in z.x];rt=rr[kt];p=next(i for i,a in enumerate(rt) if a)
  s[p]=-sum(rt[j]*s[j] for j in range(19) if j!=p)/rt[p]
  assert min(s)>0
  assert sum(rt[j]*s[j] for j in range(19))==0
  vals=[sum(rr[i][j]*s[j] for j in range(19)) for i in mask];mx=max(vals);assert mx<0
  certs.append({"orbit":[list(oa),list(ob)],"restricted_classes":len(rr),"min_pair_offset":str(min(s)),
                "max_other_slack_exact":str(mx),"pair_offset_witness":[str(x) for x in s]})
 out={"status":"exact_center_symmetric_exposed_orbits","full_nonzero_classes":len(rows),
      "restricted_nonzero_classes":len(rr),"orbits":len(certs),
      "all_positive_pair_offsets":True,"all_target_equalities_exact":True,
      "all_other_restricted_classes_strict_exact":True,"certificates":certs,
      "conclusion":"After imposing central symmetry q_{2k}=q_{2k+1}, each Chapter-53 row pair collapses to one genuinely exposed facet of the 19-dimensional pair-offset cone. All eight have exact positive relative-interior witnesses.",
      "limitation":"Exposure is proved only for the audited seed configuration cone restricted to central symmetry. Crossing a facet is not yet proved to yield a bounded, 38-active, entirely-simple neighboring configuration or an RCI-feasible cone."}
 open(args.output,"w").write(json.dumps(out,indent=2)+"\n");print(json.dumps(out,indent=2))
if __name__=="__main__":main()
