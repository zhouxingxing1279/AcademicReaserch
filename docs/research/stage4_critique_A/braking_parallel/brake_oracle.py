"""Exact vertex oracle for the frozen four-step braking contract (stdlib only)."""
import json
from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
from itertools import combinations, product
from math import lcm
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONTRACT_SHA = "bb72ee01afba24352a49d11fb69ce5305d1775f64cf65071a1eaed5f3c0716c4"
N = 6  # normalized p0, v0, w0, w1, w2, w3
K = 4


def position_row(s):
    # 400 times the position residual at stamp s.
    return (2, 2*s, *(max(0, 2*(s-j)-1) for j in range(K)))


IDENTITY = [tuple(int(i == j) for i in range(N)) for j in range(N)]
ROWS = IDENTITY + [position_row(s) for s in range(K+1)]


def dot(a, b):
    return sum(x*y for x,y in zip(a,b,strict=True))


def inverse_scaled(rows):
    """Integer numerators of the inverse and a common positive denominator."""
    mat = [list(map(Q, row+unit)) for row, unit in zip(rows, IDENTITY, strict=True)]
    for i in range(N):
        pivot = next((j for j in range(i,N) if mat[j][i]), None)
        if pivot is None:
            return None
        mat[i],mat[pivot] = mat[pivot],mat[i]
        mat[i] = [x/mat[i][i] for x in mat[i]]
        for j in range(N):
            if j != i and mat[j][i]:
                c = mat[j][i]
                mat[j] = [x-c*y for x,y in zip(mat[j],mat[i],strict=True)]
    inv = [row[N:] for row in mat]
    den = lcm(*(x.denominator for row in inv for x in row))
    return [[int(x*den) for x in row] for row in inv],den


def language():
    events = set()
    words = 0
    for delays in product((-1,0,1,2), repeat=K+1):
        if any(a==b==-1 for a,b in zip(delays,delays[1:])):
            continue
        words += 1
        events.add(tuple((s,s+d) for s,d in enumerate(delays) if d>=0 and s+d<=K))
    counts = Counter(sum(1<<s for s,_ in h) for h in events)
    return words,len(events),counts


def latest(mask,j):
    stamps = [s for s in reversed(range(K+1)) if mask & (1<<s)]
    return sum(1<<s for s in stamps[:j])


def peak_at_vertex(x,den):
    p = Q(12,5) + Q(dot(position_row(K),x),400*den)
    v = Q(6,5) + Q(sum(x[1:]),100*den)
    return p+Q(25,199)*v*v


def exact_oracle(readouts):
    # readouts are residuals in units of 1/400 m. Coefficients and right
    # hand sides are integers. Test all 32 potential retained stamp sets at once.
    best = {}
    for basis in combinations(range(len(ROWS)),N):
        inv = inverse_scaled([ROWS[i] for i in basis])
        if inv is None:
            continue
        M,den = inv
        used = sum(1<<(i-N) for i in basis if i>=N)
        faces = [(-1,1) if i<N else (readouts[i-N]-2,readouts[i-N]+2) for i in basis]
        for rhs in product(*faces):
            x = [dot(row,rhs) for row in M]
            if any(abs(value)>den for value in x):
                continue
            valid = sum(1<<s for s,r in enumerate(readouts)
                        if abs(dot(position_row(s),x)-den*r)<=2*den)
            if used & ~valid:
                raise ArithmeticError("basis constraint violated")
            value = peak_at_vertex(x,den)
            # A basis for one mask is a basis for all supersets that contain its
            # observation rows and admit the vertex.
            optional = valid ^ used
            subset = optional
            while True:
                mask = used | subset
                if mask not in best or best[mask][0]<value:
                    best[mask] = (value,tuple(Q(v,den) for v in x))
                if subset==0:
                    break
                subset=(subset-1)&optional
    if len(best)!=32:
        raise ValueError("incompatible readouts or missing polytope")
    return best


def panel(readouts,counts):
    best=exact_oracle(readouts)
    rows=[]
    for mask,count in sorted(counts.items()):
        B=best[mask][0]
        gaps=[best[latest(mask,j)][0]-B for j in range(6)]
        buffered=best[mask & 7][0]-B
        assert all(a>=b for a,b in zip(gaps,gaps[1:])) and gaps[-1]==0 and buffered>=0
        rows.append(dict(stamps=[s for s in range(5) if mask&(1<<s)],visible_records=count,
                         B=str(B),D=str(B-Q(12,5)),gaps=list(map(str,gaps)),
                         cutoff_gap=str(buffered),first_exact_j=gaps.index(0)))
    return dict(readouts_400=readouts,
                vertices={str(mask): dict(B=str(value),normalized_witness=list(map(str,x)))
                          for mask,(value,x) in sorted(best.items())},
                records=rows, uniform_j=max(r["first_exact_j"] for r in rows),
                max_gaps=[str(max(Q(r["gaps"][j]) for r in rows)) for j in range(6)])


def main():
    assert sha256((HERE/"CONTRACT.md").read_bytes()).hexdigest()==CONTRACT_SHA
    words,prefixes,counts=language()
    result=dict(contract_sha256=CONTRACT_SHA,words=words,visible_prefixes=prefixes,
                masks=len(counts),panels={key:panel(values,counts) for key,values in
                                         (("H0",[0]*5),("H1",[2,-2,2,-2,2]))})
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    main()
