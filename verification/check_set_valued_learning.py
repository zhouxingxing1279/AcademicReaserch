#!/usr/bin/env python3
"""Exact scalar counterexamples for identification quantifiers and feature versions.
Not a trained model, controller, or novelty certificate.
"""
import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path


def run():
    # theta in [0,4], x in [1,2], z in [2,3], z=theta*x.
    prior=(Q(0),Q(4));x=(Q(1),Q(2));z=(Q(2),Q(3))
    existential=(z[0]/x[1],z[1]/x[0])
    universal=(z[0]/x[0],z[1]/x[1])
    point=((z[0]+z[1])/(x[0]+x[1]))
    true=Q(1)
    assert existential==(Q(1),Q(3))
    assert universal[0]>universal[1]
    assert true!=point and true*x[1]==z[0]
    # Safe center strip: |zbar-theta*xbar| <= rz + max|theta|*rx.
    xb=sum(x)/2;zb=sum(z)/2;rx=(x[1]-x[0])/2;rz=(z[1]-z[0])/2
    width=rz+max(abs(t) for t in prior)*rx
    strip=(max(prior[0],(zb-width)/xb),min(prior[1],(zb+width)/xb))
    assert strip[0]<=existential[0]<=existential[1]<=strip[1]
    # Additional independently certified relation z=x+1.
    correlated=(1+1/x[1],1+1/x[0])
    assert correlated==(Q(3,2),Q(2))
    assert existential[0]<correlated[0]<correlated[1]<existential[1]
    # A later pair is compatible with true theta=1 and shrinks [1,3].
    next_x=(Q(2),Q(3));next_z=(Q(2),Q(3))
    local=(next_z[0]/next_x[1],next_z[1]/next_x[0])
    updated=(max(existential[0],local[0]),min(existential[1],local[1]))
    assert updated==(Q(1),Q(3,2)) and updated[0]<=true<=updated[1]
    # Same function, different feature coordinates: theta*x=(theta/2)*(2*x).
    old_theta=Q(1);new_theta=old_theta/2
    assert old_theta*Q(3)==new_theta*(2*Q(3)) and old_theta!=new_theta
    def pair(v):return list(map(str,v))
    return {'status':'exact_identification_contract_examples_only',
            'marginal_existential':pair(existential),'incorrect_universal':pair(universal),
            'incorrect_center_parameter':str(point),'true_parameter':str(true),
            'safe_center_strip':pair(strip),'joint_relation_parameter_set':pair(correlated),
            'second_record_intersection':pair(updated),
            'feature_version':{'old':'psi=x, theta=1','new':'psi=2x, theta=1/2',
                               'reuse_old_parameter_cut_without_transport':'invalid'},
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists():p.error('output must be new')
    result=run();a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
