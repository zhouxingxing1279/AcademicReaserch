"""Finite stage-4 comparison. HiGHS proposes support certificates; Fraction checks them.

Run with no arguments for the full JSON record on stdout. --verify checks an
archived record by enumerating the words and checking the rational certificates,
without calling the optimizer. The time indices in the word are generation stamps.
"""
import argparse
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import platform

HERE = Path(__file__).resolve().parent
PROTOCOL = HERE / "reduction_protocol.json"
PARAM = json.loads(PROTOCOL.read_text(encoding="utf8"))
T, A, N = map(F, (PARAM["sample_period"], PARAM["process_radius"], PARAM["position_noise_radius"]))
INITIAL = tuple(map(F, PARAM["initial_radii"]))
TARGET = tuple(map(F, PARAM["target_radii"]))
POLICIES = ("keep", "drop", "deadline")
ABSENT = -1
LAG = 2


def masks_and_words(k):
    """Group extendible words by the effective set of constraints at decision k."""
    masks = {p: {} for p in POLICIES}
    count = 0
    for word in product((ABSENT, 0, 1, 2), repeat=k+1):
        if any(a == b == ABSENT for a, b in zip(word, word[1:])):
            continue
        count += 1
        keep = drop = deadline = 0
        for s, delay in enumerate(word):
            if delay == ABSENT or s + delay > k:
                continue
            keep |= 1 << s
            if s + delay <= PARAM["block"] * (1 + s // PARAM["block"]):
                drop |= 1 << s
            if s + LAG <= k:
                deadline |= 1 << s
        for name, mask in zip(POLICIES, (keep, drop, deadline)):
            masks[name].setdefault(mask, word)
    return count, masks


def rows(k):
    """Affine state rows in xi=(p0,v0,w0,...,w[k-1]) for zero commands."""
    position = [F(1), F(0)] + [F(0)]*k
    velocity = [F(0), F(1)] + [F(0)]*k
    positions = [position]
    for s in range(k):
        position = [p + T*v for p, v in zip(position, velocity, strict=True)]
        position[s+2] += T*T/2
        velocity = velocity.copy()
        velocity[s+2] += T
        positions.append(position)
    return positions, velocity


def dot(a, b):
    return sum((x*y for x, y in zip(a, b, strict=True)), F(0))


def support(k, stamps, axis, archived=None):
    ps, vs = rows(k)
    q = ps[-1] if axis == "p" else vs
    box = [*INITIAL] + [A]*k
    obs = [ps[s] for s in stamps]
    if archived is None:
        from scipy.optimize import linprog
        H = obs + [[-v for v in row] for row in obs]
        lp = linprog([-float(x) for x in q], A_ub=H or None,
                     b_ub=[float(N)]*len(H) or None,
                     bounds=[(-float(a), float(a)) for a in box], method="highs")
        if not lp.success:
            raise ValueError(lp.message)
        def rational(x):
            return F(float(x)).limit_denominator(1_000_000)
        xi = [rational(x) for x in lp.x]
        d = lp.ineqlin.marginals
        multipliers = [rational(d[i+len(obs)]-d[i]) for i in range(len(obs))]
    else:
        xi = list(map(F, archived["xi"]))
        multipliers = list(map(F, archived["lambda"]))
    assert len(xi) == len(box) and len(multipliers) == len(obs)
    assert all(abs(x) <= b for x,b in zip(xi,box,strict=True))
    assert all(abs(dot(row,xi)) <= N for row in obs)
    residual = [v - sum((lam*row[j] for lam,row in zip(multipliers,obs,strict=True)), F(0))
                for j,v in enumerate(q)]
    upper = dot(box,map(abs,residual)) + N*sum(map(abs,multipliers))
    lower = dot(q,xi)
    assert upper == lower, (k,stamps,axis,lower,upper)
    return {"radius":str(upper), "xi":list(map(str,xi)), "lambda":list(map(str,multipliers))}


def catalog(k, existing=None):
    count, groups = masks_and_words(k)
    certificates = {}
    @lru_cache(None)
    def solve(mask, axis):
        stamps = tuple(i for i in range(k+1) if (mask >> i) & 1)
        key = f"{mask}-{axis}"
        saved = None if existing is None else existing["certificates"][key]
        cert = support(k,stamps,axis,saved)
        certificates[key] = cert
        return F(cert["radius"])
    policies = {}
    for policy, words in groups.items():
        # Adding an independent zero-readout strip can only reduce support.
        minimal = [m for m in sorted(words) if not any(n != m and n&m == n for n in words)]
        assert all(any(m & other == m for m in minimal) for other in words)
        worst = {}
        for axis in ("p","v"):
            mask = max(minimal,key=lambda m:solve(m,axis))
            worst[axis] = {"radius":str(solve(mask,axis)), "mask":mask, "word":list(words[mask])}
        policies[policy] = {"mask_count":len(words),"minimal_masks":minimal,"worst":worst,
                            "joint_box_pass":all(F(worst[a]["radius"]) <= r for a,r in zip(("p","v"),TARGET))}
    # The earlier word, plus an all-on-time negative control.
    old = (ABSENT,0,ABSENT,2,ABSENT,2,ABSENT,2,ABSENT)[:k+1]
    controls = {}
    for label,word in (("old",old),("on_time",(0,)*(k+1))):
        masks = {}
        for pol in POLICIES:
            stamps = [s for s,d in enumerate(word) if d>=0 and s+d<=k and
                      (pol!="drop" or s+d<=PARAM["block"]*(1+s//PARAM["block"])) and
                      (pol!="deadline" or s+LAG<=k)]
            mask = sum(1<<s for s in stamps)
            assert mask in groups[pol]
            masks[pol] = [str(solve(mask,a)) for a in ("p","v")]
        controls[label]=masks
    assert controls["on_time"]["keep"] == controls["on_time"]["drop"]
    assert all(policies["keep"]["worst"][a]["radius"] == policies["deadline"]["worst"][a]["radius"]
               for a in ("p","v"))
    return {"decision":k,"word_count":count,"policies":policies,"controls":controls,
            "certificates":certificates}


def binary_alias():
    # Two legal words delivering numerical zeros at 0,1,2,5.
    stale=(0,0,0,2,2,2)
    fresh=(0,0,0,ABSENT,2,0)
    def history(word):
        return [[s for s,d in enumerate(word) if d>=0 and s+d==k] for k in range(6)]
    h1,h2=history(stale),history(fresh)
    assert h1[:-1]==h2[:-1] and h1[-1]==[3] and h2[-1]==[5]
    # Reachable under stale observations; violates the fresh zero strip at t=5.
    ps,vs=rows(5)
    xi=[F(0),F(0),F(0),F(0),F(0),A,A]
    assert all(dot(ps[s],xi)==0 for stamps in h1 for s in stamps)
    p,v=dot(ps[5],xi),dot(vs,xi)
    assert p>N and p==F(1,100) and v==F(1,50)
    return {"stale":list(stale),"fresh":list(fresh),"stale_only_state":list(map(str,(p,v)))}


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify",type=Path)
    args=parser.parse_args()
    saved = json.loads(args.verify.read_text(encoding="utf-8-sig")) if args.verify else None
    out={"protocol_sha256":sha256(PROTOCOL.read_bytes()).hexdigest(),
         "checker_sha256":sha256(Path(__file__).read_bytes()).hexdigest(),
         "alias":binary_alias(),"checks":[]}
    for i,k in enumerate(PARAM["decisions"]):
        out["checks"].append(catalog(k,None if saved is None else saved["checks"][i]))
    if saved:
        assert all(saved[key]==value for key,value in out.items())
        print("Verified all words, archived primal/dual pairs, alias witness and controls.")
    else:
        import scipy
        import numpy
        out["environment"]={"python":platform.python_version(),"numpy":numpy.__version__,
                            "scipy":scipy.__version__,"seed":None}
        print(json.dumps(out,indent=2))
