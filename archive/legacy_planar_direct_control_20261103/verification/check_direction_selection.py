"""Finite rational geometry probe; no trained selector or physical simulation."""
import argparse, hashlib, json
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

def vertices(ineq):
    out=set()
    for (a,b),(c,d) in combinations(ineq,2):
        det=a[0]*c[1]-a[1]*c[0]
        if det:
            x=((b*c[1]-a[1]*d)/det,(a[0]*d-b*c[0])/det)
            if all(sum(u*v for u,v in zip(row,x))<=bound for row,bound in ineq):out.add(x)
    assert out
    return out

def support(ineq,a):return max(sum(x*y for x,y in zip(a,v)) for v in vertices(ineq))

def verify():
    box=[((F(1),F(0)),F(1)),((F(-1),F(0)),F(1)),((F(0),F(1)),F(1)),((F(0),F(-1)),F(1))]
    rows=[]
    for sign in (-1,1):
        c=(F(1),F(sign));wrong=(F(1),F(-sign))
        for s in (F(1,4),F(1,2),F(3,4),F(1)):
            truth=box+[(c,s),(tuple(-x for x in c),s)]
            assert support(truth,c)==s and support(box,c)==2
            candidates=[('axis_x',(F(1),F(0))),('axis_y',(F(0),F(1))),('opposite_diagonal',wrong),('constraint_normal',c)]
            result={}
            for name,a in candidates:
                gamma=support(truth,a)
                refined=box+[(a,gamma)]
                assert all(sum(x*y for x,y in zip(a,v))<=gamma for v in vertices(truth))
                after=support(refined,c)
                assert after>=s
                if name=='constraint_normal':assert after==s
                else:assert after==2
                # Computing a cut over the existing box cannot remove any box point.
                redundant=box+[(a,support(box,a))]
                assert support(redundant,c)==2
                result[name]={'certified_bound':str(gamma),'target_support_after':str(after),'target_gain':str(2-after)}
            assert 1-s>F(-1)
            rows.append({'baseline_common_input_interval':['-1','-1'],'refined_common_input_interval':['-1',str(1-s)],'sign':sign,'strip_halfwidth':str(s),'true_support':str(s),'policies_one_query':result})
    # Selection approximation lemma arithmetic, not evidence of learnability.
    scores=[F(3,2),F(0)];eps=F(1,4)
    assert scores[0]-2*eps>scores[1]
    return {'status':'EXACT_DIRECTION_GEOMETRY_AND_STRONG_BASELINE_CHECK_PASSED','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'instances':rows,'query_count_per_policy':1,'selection_inference_cost_included':False,'trained_model':False,'neural_superiority_proved':False,'physical_benchmark_transfer_proved':False,'conclusion':'Constraint-normal exact support attains the single-target information lower bound; axis-only gains do not demonstrate learning value.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=verify()
    with a.output.open('x') as f:json.dump(r,f,indent=2);f.write('\n')
    print(r['status'])
