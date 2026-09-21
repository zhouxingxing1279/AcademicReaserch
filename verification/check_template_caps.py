#!/usr/bin/env python3
"""Certified candidate caps, scalar joint-error graph, exact rational replay.

Coarse support queries are synthetic safe upper bounds; no solver timing claim.
"""
import argparse
import hashlib
import json
from fractions import Fraction as Q
from functools import lru_cache
from pathlib import Path
from check_recursive_tube import candidate as base_candidate, posterior, N

# A tighter, independently invariant terminal box stresses numerical margins.
TERMINAL_E=Q(9,25)
TERMINAL_D=Q(7,10)


def candidate(z,e,d):
    c=base_candidate(z,e,d)
    c['feasible'] &= c['terminal_e']<=TERMINAL_E and c['terminal_d']<=TERMINAL_D
    return c


def pull(q):return ((q[0]+q[1])/2,q[1]/2)


@lru_cache(None)
def noise_support(q,i):
    value=Q(0)
    for _ in range(i):
        value+=abs((q[0]+q[1])/20)+abs((-q[0]+q[1])/10)
        q=pull(q)
    return value


def back(q,i):
    for _ in range(i):q=pull(q)
    return q


def plan_caps(z):
    """Caps for the shifted feasible nominal plan v=-z/2.

    Validity requires the previous feasible certificate and fixed model/terminal
    assumptions; these are verified in replay, not inferred from arbitrary z.
    """
    rows=[]
    for i in range(N+1):
        zi=z/Q(2)**i
        for sign in (Q(1),-Q(1)):
            q=(sign,sign)
            rows.append((back(q,i),2-sign*zi-noise_support(q,i)))
            if i<N:
                q=(Q(0),-sign/2)
                rows.append((back(q,i),1-sign*(-zi/2)-noise_support(q,i)))
    for q,b in [((Q(1),Q(0)),TERMINAL_E),((Q(0),Q(1)),TERMINAL_D)]:
        for sign in (Q(1),-Q(1)):
            qs=(sign*q[0],sign*q[1])
            rows.append((back(qs,N),b-noise_support(qs,N)))
    return rows


def intersect_graph(bounds,d,rows):
    lo,hi=bounds
    for (a,b),rhs in rows:
        residual=rhs-b*d
        if a>0:hi=min(hi,residual/a)
        elif a<0:lo=max(lo,residual/a)
        elif residual<0:raise ValueError('empty graph intersection')
    if lo>hi:raise ValueError('empty interval')
    return lo,hi


def support_graph(e,d,q):return max(q[0]*e[0],q[0]*e[1])+q[1]*d


def compress(old_e,r,d,z,inflation):
    # P is the exact scalar posterior; B ignores the new measurement strip.
    p=posterior(old_e,r)
    box=(old_e[0]-Q(1,10)-r/2,old_e[1]+Q(1,10)-r/2)
    certified=[];uncapped=[];caps=plan_caps(z)
    for q,cap in caps:
        truth=support_graph(p,d,q)
        # An independent oracle check for this experiment, not a needed online LP.
        assert truth<=cap
        if inflation is None:
            certified.append((q,cap))
        else:
            proposed=truth+inflation
            assert proposed>=truth
            certified.append((q,min(proposed,cap)))
            uncapped.append((q,proposed))
    out=intersect_graph(box,d,certified)
    raw=intersect_graph(box,d,uncapped)
    assert out[0]<=p[0]<=p[1]<=out[1]
    assert all(support_graph(out,d,q)<=b for q,b in certified)
    return out,raw,len(caps)


def replay(inflation):
    count=0;rejects=0;max_x=Q(0);max_u=Q(0);max_width=Q(0)
    for case in range(16):
        z=Q(1,2);hat=z;x=hat+(Q(1) if case%2 else -Q(1))
        e=(-Q(1),Q(1));d=Q(0);old=candidate(z,e,d)
        assert old['feasible']
        for k in range(64):
            v=old['v'][0];u=v-d/2
            w=Q(1 if ((k+case)>>(case%3))%2 else -1,10)
            nu=Q(1 if ((3*k+case)>>(case%4))%2 else -1,5)
            xn=x+u+w;hp=hat+u;r=xn+nu-hp;hn=hp+r/2;zn=z+v;dn=hn-zn
            en,raw,rows=compress(e,r,dn,zn,inflation)
            new=candidate(zn,en,dn)
            assert new['feasible']
            assert new['v'][:-1]==old['v'][1:] and new['v'][-1]==-old['z'][-1]/2
            assert en[0]<=xn-hn<=en[1]
            assert abs(x)<=2 and abs(xn)<=2 and abs(u)<=1
            rejects+=not candidate(zn,raw,dn)['feasible']
            count+=1;max_x=max(max_x,abs(x),abs(xn));max_u=max(max_u,abs(u))
            max_width=max(max_width,en[1]-en[0])
            x,hat,z,e,d,old=xn,hn,zn,en,dn,new
    return {'query_inflation':'all_queries_missing' if inflation is None else inflation,
            'steps':count,'violations':0,'uncapped_candidate_rejections':rejects,
            'max_abs_x':max_x,'max_abs_u':max_u,'max_posterior_width':max_width,
            'cap_rows_before_deduplication':rows,
            'scope':'feasible_candidate_replay_no_objective_optimization'}


def raw_clip_counterexamples():
    # P=[-.2,.2] cannot be clipped by .1 just because a plan asks for .1.
    # Initial support=1, future noise support=.1, constraint=1.1 is feasible.
    # Subtracting an inflated noise bound .2 invents an invalid cap .9.
    return {'arbitrary_cap':Q(1,10),'true_endpoint':Q(1,5),
            'valid_initial_support':Q(1),'cap_from_inflated_noise':Q(11,10)-Q(1,5)}


def run():
    image=(TERMINAL_E/2+Q(3,20),TERMINAL_E/2+TERMINAL_D/2+Q(3,20))
    assert image[0]<=TERMINAL_E and image[1]<=TERMINAL_D
    return {'modes':[replay(v) for v in (Q(0),Q(1,20),Q(1),None)],
            'terminal_radii':[TERMINAL_E,TERMINAL_D],'terminal_image_radii':image,
            'negative_examples':raw_clip_counterexamples(),
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'dependency_sha256':hashlib.sha256(Path(__file__).with_name('check_recursive_tube.py').read_bytes()).hexdigest()}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    if a.output.exists():p.error('output must be new')
    a.output.parent.mkdir(parents=True,exist_ok=True)
    encoded=json.dumps(run(),default=str,indent=2)+'\n';a.output.write_text(encoded);print(encoded)
