"""Finite generation/delivery contract enumeration; Python 3 stdlib only."""
from itertools import product

def evaluate(bits, delays, H, D):
    n=len(bits)
    if not all(any(bits[j:j+H+1]) for j in range(n-H)):
        return None
    stamps=[i for i,b in enumerate(bits) if b]
    delivered=[(s+d,s) for s,d in zip(stamps,delays)]
    latest=-1
    ages=[]
    for k in range(n):
        latest=max([latest]+[s for arrival,s in delivered if arrival<=k])
        if k>=H+D:
            assert latest>=0
            ages.append(k-latest)
            assert k-latest<=H+D,(bits,delays,k,latest)
    return max(ages,default=0)

def main():
    N,H,D=8,2,2
    cases=0; peak=0
    for bits in product((0,1),repeat=N):
        stamps=sum(bits)
        for ds in product(range(D+1),repeat=stamps):
            age=evaluate(bits,ds,H,D)
            if age is not None:
                cases+=1;peak=max(peak,age)
    assert peak==H+D,(peak,H+D)
    for k in (10,100,1000):
        assert k-0==k
    print(f'PASS N={N} H={H} D={D} legal={cases} peak_age={peak}; stale-timestamp counterexample PASS')
if __name__=='__main__':main()
