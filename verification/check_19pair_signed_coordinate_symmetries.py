#!/usr/bin/env python3
"""Audit signed-coordinate projective symmetries of the 19-pair orientation family.

This is deliberately a restricted symmetry class: coordinate permutations and
coordinate sign flips. It does not claim to enumerate arbitrary PGL(4,Q)
automorphisms. For the present quadrotor state coordinates this is the natural
first class because it preserves the coordinate interpretation rather than
mixing physical states by a dense transformation.
"""
from fractions import Fraction as F
from itertools import permutations, product
import argparse, json
import check_19pair_cc_seed_cone as cc

def normdir(a):
    k=next(i for i,x in enumerate(a) if x)
    s=a[k]
    return tuple(x/s for x in a)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--output",required=True); args=ap.parse_args()
    reps=cc.orientation_reps(cc.build_s2())
    lookup={normdir(a):i for i,a in enumerate(reps)}
    autos=[]
    for p in permutations(range(4)):
        for sg in product((F(1),F(-1)),repeat=4):
            image=[]; ok=True
            for a in reps:
                b=tuple(sg[j]*a[p[j]] for j in range(4))
                nb=normdir(b)
                if nb not in lookup:
                    ok=False; break
                image.append(lookup[nb])
            if ok:
                autos.append({"coordinate_permutation":list(p),
                              "coordinate_signs":[int(x) for x in sg],
                              "pair_permutation":image})
    distinct_pair_maps=sorted({tuple(a["pair_permutation"]) for a in autos})
    identity=tuple(range(19))
    result={
      "status":"exact_signed_coordinate_symmetry_audit",
      "orientation_pairs":len(reps),
      "signed_coordinate_candidates":24*16,
      "accepted_signed_coordinate_actions":len(autos),
      "distinct_projective_pair_permutations":len(distinct_pair_maps),
      "only_identity_pair_permutation":distinct_pair_maps==[identity],
      "actions":autos,
      "conclusion":"Among all 384 signed coordinate permutations, the 19-pair orientation family admits no nontrivial pair-offset permutation. The two accepted actions are global sign +/-I and induce the same identity permutation on unoriented pairs.",
      "scope":"Exact for signed coordinate permutations only. This does not exclude a dense rational projective automorphism of the 19 projective directions, nor does it by itself prove orbit-0 infeasibility."
    }
    open(args.output,"w").write(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))
    assert len(reps)==19 and len(autos)==2
    assert distinct_pair_maps==[identity]

if __name__=="__main__": main()
