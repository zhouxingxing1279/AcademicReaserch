#!/usr/bin/env python3
"""Exact exposed-facet certificates for the 16 Chapter-52 witness-relevant rows.

HiGHS is used only to discover a point in the relative interior of each target
facet. The point is rounded to 1e-5, projected exactly onto the target rational
hyperplane, then every other distinct configuration-row class is checked with
Fraction arithmetic. A strictly negative exact maximum proves exposure.
"""
from fractions import Fraction as F
import argparse,json,numpy as np,sympy as sp
from scipy.optimize import linprog
import check_19pair_cc_seed_cone as cc

TARGETS=[(2,19),(54,32),(63,20),(71,22),(85,31),(89,29),(15,33),(23,21),
         (42,18),(25,33),(18,21),(33,23),(76,30),(78,28),(60,32),(52,20)]
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
 A=np.array([[float(x) for x in r] for r in rows]);certs=[]
 for meta in TARGETS:
  k=rid[canon(erow(*meta))];mask=[i for i in range(len(rows)) if i!=k]
  z=linprog(np.zeros(38),A_ub=A[mask],b_ub=-np.ones(len(mask)),A_eq=A[[k]],b_eq=[0.],
            bounds=[(None,None)]*38,method="highs")
  assert z.success
  q=[F(round(float(x)*100000),100000) for x in z.x];rt=rows[k];p=next(i for i,a in enumerate(rt) if a)
  q[p]=-sum(rt[j]*q[j] for j in range(38) if j!=p)/rt[p]
  assert sum(rt[j]*q[j] for j in range(38))==0
  vals=[sum(rows[i][j]*q[j] for j in range(38)) for i in mask];mx=max(vals)
  assert mx<0
  certs.append({"row":list(meta),"class_index":k,"pivot":p,"max_other_slack_exact":str(mx),
                "witness_q":[str(x) for x in q]})
 out={"status":"exact_exposed_certificates","unique_nonzero_classes":len(rows),"certified_rows":len(certs),
      "symmetry_orbits":8,"orbits":[[list(a),list(b)] for a,b in ORBITS],
      "all_target_equalities_exact":True,"all_other_classes_strict_exact":True,"certificates":certs,
      "conclusion":"All 16 Chapter-52 witness-relevant antecedent rows are exact exposed facets of the audited configuration cone. Under the recorded central symmetry they form 8 search orbits.",
      "limitation":"The certificates concern the audited seed configuration cone only. They do not prove any neighboring cone is globally consistent, entirely simple, or RCI-feasible."}
 open(args.output,"w").write(json.dumps(out,indent=2)+"\n");print(json.dumps(out,indent=2))
if __name__=="__main__":main()
