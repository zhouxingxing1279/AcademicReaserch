#!/usr/bin/env python3
"""Audit the chapter-45 five-pair augmentation at inherited S3 offsets.

This is deliberately a numerical geometry audit, not an RCI certificate.  It
reuses the endpoint-exact predecessor construction from chapter 45, appends the
10 selected S3 halfspaces with their inherited offsets, removes redundant
halfspaces, enumerates vertices, and checks whether each vertex admits one
bounded torque that robustly maps it back into the same augmented set at both
thrust endpoints.
"""
from fractions import Fraction as F
import argparse, json
import check_s3_minimal_normal_cover as base

SELECTED = [
    (["1","3/50","-2943/500000","-981/25000000"],"39981236851/8000000000"),
    (["1","3/50","-8829/500000","-2943/25000000"],"39979806553/8000000000"),
    (["-1","-3/50","2943/500000","981/25000000"],"39981236851/8000000000"),
    (["-1","-3/50","8829/500000","2943/25000000"],"39979806553/8000000000"),
    (["0","1","-2943/10000","-2943/500000"],"2306309823/800000000"),
    (["0","-1","2943/10000","2943/500000"],"2306309823/800000000"),
    (["0","1","-8829/10000","-8829/500000"],"2299409469/800000000"),
    (["0","0","-1","-3/50"],"1137/2500"),
    (["0","-1","8829/10000","8829/500000"],"2299409469/800000000"),
    (["0","0","1","3/50"],"1137/2500"),
]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True); args=ap.parse_args()
    X=[]
    for i,w in enumerate([F(5),F(3),F('0.45'),F(2)]):
        e=[F(0)]*4; e[i]=1; X.append((tuple(e),w))
        e=[F(0)]*4; e[i]=-1; X.append((tuple(e),w))
    S1=base.reduce(X+base.pre(X)); S2=base.reduce(X+base.pre(S1))
    selected=[(tuple(F(x) for x in a),F(b)) for a,b in SELECTED]
    augmented_raw=S2+selected
    H=base.reduce(augmented_raw)
    V=base.vertices(H)
    bad=[i for i,x in enumerate(V) if not base.viable(x,H)]
    result={
      'status':'numerical_fixed_offset_augmented_template_audit',
      'S2_facets':len(S2),
      'selected_new_halfspaces':len(selected),
      'raw_augmented_halfspaces':len(augmented_raw),
      'nonredundant_augmented_facets':len(H),
      'augmented_vertices':len(V),
      'nonviable_augmented_vertices':len(bad),
      'viable_augmented_vertices':len(V)-len(bad),
      'all_vertices_one_step_viable':len(bad)==0,
      'conclusion':'At inherited S3 offsets, the chapter-45 five-pair augmentation is not RCI: after redundancy removal it has 30 facets and 128 vertices, of which 96 fail the endpoint-robust one-step admissible-torque test back into the same set.',
      'limitation':'This only rejects the inherited-offset realization. It does not reject the same 19 normal pairs with independently optimized offsets or a different configuration incidence.'
    }
    with open(args.output,'w') as f: json.dump(result,f,indent=2); f.write('\n')
    print(json.dumps(result,indent=2))
    assert len(S2)==28 and len(H)==30 and len(V)==128 and len(bad)==96

if __name__=='__main__': main()
