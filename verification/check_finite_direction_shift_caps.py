#!/usr/bin/env python3
from fractions import Fraction as F
import json,argparse
old=[(-F(1),F(1)),(-F(1),F(1))]
outer=[(-F(1,2),F(1,2)),(-F(2),F(2))]
conditioned=[(-F(1,2),F(1,2)),(F(0),F(0))]
def support(box,q): return sum((hi if a>=0 else lo)*a for (lo,hi),a in zip(box,q))
q=(F(1),F(0)); qm=(-q[0],-q[1]); r=(F(0),F(1))
assert support(outer,q)<=support(old,q)
assert support(outer,qm)<=support(old,qm)
assert outer[1][1]>old[1][1]
assert support(outer,r)>support(old,r)
assert support(conditioned,q)<=support(old,q)
out={"status":"exact_fraction_checks","full_inclusion_fails":True,"protected_support_old":str(support(old,q)),"protected_support_new":str(support(outer,q)),"omitted_support_old":str(support(old,r)),"omitted_support_new":str(support(outer,r)),"conclusion":"Full tube inclusion is unnecessary for a nonterminal tightened constraint when every controller-read support direction is dominated; omitted readout directions are not protected."}
ap=argparse.ArgumentParser();ap.add_argument("--output");a=ap.parse_args();s=json.dumps(out,indent=2)+"\n"
if a.output: open(a.output,"x").write(s)
print(s,end="")
