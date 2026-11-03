"""Run300: exhaustive finite-prefix certificate for two distinct delivered timestamps.
Contract: each H+1 consecutive generation instants has >=1 eventually delivered
sample; every such sample arrives within D steps; -1 means permanent loss.
"""
from itertools import product

def verify(N=9,H=2,D=2):
    count=0; checked=0; worst_age=0; worst_gap=0
    for choices in product(range(-1,D+1),repeat=N):
        successful=[i for i,c in enumerate(choices) if c>=0]
        if any(not any(i<=s<=i+H for s in successful)
               for i in range(N-H)):
            continue
        count+=1
        for k in range(N):
            available=[s for s in successful if s+choices[s]<=k]
            if k>=2*(H+1)+D-1:
                assert len(available)>=2,(choices,k)
                s0,s1=available[-2:]
                age=k-s1
                gap=s1-s0
                assert age<=H+D,(choices,k,age)
                assert 1<=gap<=2*H+1+D,(choices,k,gap)
                checked+=1
                worst_age=max(worst_age,age)
                worst_gap=max(worst_gap,gap)
    print(f"PASS paths={count} two_stamp_checks={checked} max_age={worst_age} max_gap={worst_gap}")
    assert count>0 and checked>0

if __name__=="__main__":
    verify()
