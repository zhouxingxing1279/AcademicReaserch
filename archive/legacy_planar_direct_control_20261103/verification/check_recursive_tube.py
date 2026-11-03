#!/usr/bin/env python3
"""Exact feasible-tail replay for a scalar plant, not an MPC optimizer."""
import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path

N=4


def terminal_certificate():
    re,rd=Q(2,5),Q(4,5)
    image=[re/2+Q(3,20),re/2+rd/2+Q(3,20)]
    assert image[0]<=re and image[1]<=rd
    return {'radii':[re,rd],'image_radii':image,
            'state_bound':Q(1,2)+re+rd,
            'input_bound':Q(1,4)+rd/2,'nominal_image_radius':Q(1,4)}


def support(g,q):return sum(abs(q[0]*a+q[1]*b) for a,b in g)
def fmap(p):return (p[0]/2,(p[0]+p[1])/2)


def candidate(z,e,d):
    c=((e[0]+e[1])/2,d);g=[((e[1]-e[0])/2,Q(0))]
    rows=[];zs=[];vs=[];feasible=True
    for i in range(N+1):
        sx=abs(z+c[0]+c[1])+support(g,(Q(1),Q(1)))
        feasible &= sx<=2
        row={'state_bound':sx};zs.append(z)
        if i<N:
            v=-z/2;vs.append(v)
            su=abs(v-c[1]/2)+support(g,(Q(0),-Q(1,2)))
            row['input_bound']=su;feasible &= su<=1
            z+=v;c=fmap(c);g=[fmap(p) for p in g]+[(Q(1,20),Q(1,20)),(-Q(1,10),Q(1,10))]
        rows.append(row)
    te=abs(c[0])+support(g,(Q(1),Q(0)))
    td=abs(c[1])+support(g,(Q(0),Q(1)))
    feasible &= abs(z)<=Q(1,2) and te<=Q(2,5) and td<=Q(4,5)
    return {'feasible':bool(feasible),'rows':rows,'terminal_e':te,'terminal_d':td,
            'z':zs,'v':vs}


def posterior(e,r):
    # t=e+w, r=t+nu. Then e_new=t-r/2.
    lo=max(e[0]-Q(1,10),r-Q(1,5))
    hi=min(e[1]+Q(1,10),r+Q(1,5))
    if lo>hi:raise ValueError('innovation inconsistent with certified bounds')
    return lo-r/2,hi-r/2


def replay():
    count=0;max_x=Q(0);max_u=Q(0);max_te=Q(0);max_td=Q(0)
    for case in range(16):
        z=Q(1,2);hat=z;x=hat+(Q(1) if case%2 else -Q(1))
        e=(-Q(1),Q(1));d=Q(0)
        old=candidate(z,e,d);assert old['feasible']
        for k in range(64):
            v=old['v'][0];u=v-d/2
            w=Q(1 if ((k+case)>>(case%3))%2 else -1,10)
            nu=Q(1 if ((3*k+case)>>(case%4))%2 else -1,5)
            x_next=x+u+w;hat_pred=hat+u
            r=x_next+nu-hat_pred;hat_next=hat_pred+r/2
            z_next=z+v;e_next=posterior(e,r);d_next=hat_next-z_next
            assert abs(x)<=2 and abs(u)<=1 and abs(x_next)<=2
            assert e_next[0]<=x_next-hat_next<=e_next[1]
            new=candidate(z_next,e_next,d_next);assert new['feasible']
            # Explicitly verify this is the shifted old plan plus terminal law.
            assert new['v'][:-1]==old['v'][1:]
            assert new['v'][-1]==-old['z'][-1]/2
            max_x=max(max_x,abs(x),abs(x_next));max_u=max(max_u,abs(u))
            max_te=max(max_te,new['terminal_e']);max_td=max(max_td,new['terminal_d'])
            x,hat,z,e,d=x_next,hat_next,z_next,e_next,d_next;old=new;count+=1
    return {'steps':count,'trajectories':16,'steps_per_trajectory':64,'violations':0,
            'max_abs_x':max_x,'max_abs_u':max_u,'max_terminal_e':max_te,'max_terminal_d':max_td,
            'scope':'feasible_shifted_candidate_only_no_MPC_optimization'}


def run():
    return {'terminal':terminal_certificate(),
            'initial':candidate(Q(1,2),(-Q(1),Q(1)),Q(0)),
            'replay':replay(),
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists():p.error('output must be new')
    a.output.parent.mkdir(parents=True,exist_ok=True)
    result=json.dumps(run(),default=str,indent=2)+'\n';a.output.write_text(result);print(result)
