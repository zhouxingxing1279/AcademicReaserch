"""Run275: exact two-success measurement sufficient speed gate, no MPC solver."""
from fractions import Fraction as F
from itertools import product
from collections import Counter
import argparse, json
H=F(1,50); T=F(981,100); R=F(3246383,1600000)
EPS=F(1,50); PHI=F(1,125); OMEGA=F(1,100)
G=F(187678479,80000000); SMM_V=F(7841778593,5000000000)
def q(x): return f'{x.numerator}/{x.denominator}'
def accel(k):
    assert 60<=k<90
    return R+T*(PHI+(k-60)*H*OMEGA)
def patterns():
    return [''.join(x) for x in product('SM',repeat=6) if 'MMM' not in ''.join(x)]
def pair(s):
    assert len(s)==6 and 'MMM' not in s
    hits=[60]+[65+5*i for i,c in enumerate(s) if c=='S']
    return hits[-2],hits[-1]
def radius(a,b):
    n=b-a
    assert n in (5,10,15) and 60<=a<b<=90
    return 2*EPS/(n*H)+H/n*sum((i-a+1)*accel(i) for i in range(a,b))+H*sum(accel(i) for i in range(b,90))
def threshold(a,b): return (b-a)*H*(G-radius(a,b))
def witness():
    p=F(0); v=F(3,2); pp={60:p}
    for k in range(60,90):
        p,v=p+H*v,v+H*R
        pp[k+1]=p
    a,b=pair('MMSMMS'); d=abs(pp[b]-pp[a])
    assert F(3,2)<SMM_V and v>G and v<3 and p<5 and d>threshold(a,b)
    return dict(scope='SMM outer-box only; actual Run260 posterior membership unproved',
                pattern='MMSMMS',a=a,b=b,v90=q(v),p90=q(p),displacement=q(d),gate=q(threshold(a,b)))
def certificate():
    rows=[]; counts=Counter()
    for s in patterns():
        a,b=pair(s); n=b-a; j=90-b; t=threshold(a,b)
        assert n<=15 and j<=10 and t>0
        counts[(n,j)]+=1; rows.append((s,a,b,t))
    assert len(rows)==44
    return dict(run='275',model='frozen four-state Euler, tau=0, position successes at 60 and selected later packets',
                lemma='|v90| <= |yb-ya|/((b-a)*h) + radius(a,b); if |yb-ya| <= threshold(a,b), then |v90| <= G',
                constants={k:q(v) for k,v in dict(h=H,T=T,R=R,eps=EPS,phi60=PHI,omega60=OMEGA,G=G).items()},
                count=44, counts={f'{n},{j}':v for (n,j),v in sorted(counts.items())},
                min_gate=q(min(t for _,_,_,t in rows)),max_gate=q(max(t for _,_,_,t in rows)),
                witness=witness(),limitations='sufficient only; no exact SMF posterior, information RCI, MPC or infinite safety')
if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True); args=ap.parse_args()
    with open(args.output,'w',encoding='utf-8') as f:
        json.dump(certificate(),f,indent=2,sort_keys=True,ensure_ascii=False);f.write('\n')
