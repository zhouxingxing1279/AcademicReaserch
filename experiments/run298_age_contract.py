"""Exhaustive finite-prefix age check under bounded generation gap and delivery latency."""
from itertools import product

def verify(H=2,D=2,N=9):
    cases=0; max_age=0
    for bits in product((0,1),repeat=N):
        if any(not any(bits[j:j+H+1]) for j in range(N-H)):
            continue
        samples=[i for i,b in enumerate(bits) if b]
        for delays in product(range(D+1),repeat=len(samples)):
            cases+=1
            latest=None
            for k in range(N):
                delivered=[s for s,d in zip(samples,delays) if s+d==k]
                if delivered: latest=max([latest if latest is not None else -1]+delivered)
                if k>=H+D:
                    assert latest is not None
                    age=k-latest
                    max_age=max(max_age,age)
                    assert age<=H+D,(bits,delays,k,age)
    assert cases>0
    return cases,max_age

if __name__=='__main__':
    n,a=verify()
    print(f'PASS: {n} admissible finite schedules; max post-transient age={a}')
