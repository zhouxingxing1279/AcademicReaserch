#!/usr/bin/env python3
from fractions import Fraction as F
import argparse,json,sympy as sp
import check_19pair_cc_seed_cone as cc
def sf(x): return F(int(x.p),int(x.q))
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--output",required=True);args=ap.parse_args()
 S2=cc.build_s2();H=cc.seed_H(cc.orientation_reps(S2));_,_,V,acts=cc.enumerate_vertices(H)
 Ce=[[F(v) for v in a] for a,_ in H]
 def erow(i,j):
  ids=acts[i];M=sp.Matrix([[sp.Rational(v.numerator,v.denominator) for v in Ce[k]] for k in ids]);L=M.inv();out=[F(0)]*38
  for k in range(4):
   for t,col in enumerate(ids): out[col]+=Ce[j][k]*sf(L[k,t])
  out[j]-=1;return out
 rels=[((15,5),[((0,19),F(5000,981)),((2,19),F(5000,981))]),((17,5),[((2,5),F(1,2)),((15,5),F(1,2)),((17,3),F(5000,981))]),((60,4),[((38,18),F(5000,981)),((42,18),F(5000,981))]),((62,4),[((40,4),F(1,2)),((60,4),F(1,2)),((62,2),F(5000,981))])]
 checks=[]
 for target,terms in rels:
  r=erow(*target);c=[F(0)]*38
  for meta,lam in terms:c=[a+lam*b for a,b in zip(c,erow(*meta))]
  ok=(r==c);assert ok;checks.append({"target":target,"terms":[(m,str(l)) for m,l in terms],"exact_identity":ok})
 result={"status":"exact_critical_boundary_redundancy","critical_rows":4,"all_exact_nonnegative_combinations":True,"relations":checks,"conclusion":"The four certificate-critical configuration rows are exact nonnegative combinations of other configuration rows; none is an independently exposed single boundary. Chapter 50's 12 determinant-only flips are not directly adjacent cones.","limitation":"This corrects adjacency only; it does not prove global infeasibility of the 19-pair orientation family."}
 open(args.output,"w").write(json.dumps(result,indent=2)+"\n");print(json.dumps(result,indent=2))
if __name__=="__main__":main()
