"""Stage 4 witness checker. No controller changes, simulation, or future measurements.

Generate JSON on stdout, or pass --verify to recheck the archived support
multipliers and all tail bounds using Fraction alone.
"""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
import platform

import cdc22_reduction_check as estimation

HERE = Path(__file__).resolve().parent
T, W, NOISE = estimation.T, estimation.A, estimation.N
K = (Q(-4), Q(-3))
LIMIT = (Q(3), Q(2))
UMAX = Q(4)
N = 12
ZERO = (Q(0), Q(0))
MAIN = (0, 0, 0, 2, 0, 0, 0, 1, 2)
LATE = (0, 0, 0, 2, 0, 0, 0, 2, 2)
PROFILE = (1, Q(-1,2), Q(-1,2), Q(-1,2), 0, 0, Q(1,2), 0, 0, 0, 0, 0)


def step(x, command):
    p, v = x
    return p + T*v + T*T*command/2, v + T*command


def gain(x):
    return estimation.dot(K, x)


def corners(radii):
    return product(*[(-r, r) for r in radii])


def tube_corners(delta):
    # B=(1/8,1/2), F B=(1/8,-1/2).
    return [((a+b)/8, (a-b)/2) for a,b in corners((delta, delta))]


def gauge(x):
    p, v = x
    return max(abs(4*p+v), abs(4*p-v))


def design(est_error):
    delta = W + max(gain(x) for x in corners(est_error))
    tube = tube_corners(delta)
    size = tuple(max(abs(x[i]) for x in tube) for i in (0,1))
    feedback_bound = max(abs(gain((p-ep, v-ev)))
                         for p,v in tube for ep,ev in corners(est_error))
    for e in tube:
        for e_est in corners(est_error):
            du = gain((e[0]-e_est[0], e[1]-e_est[1]))
            for w in (-W, W):
                assert gauge(step(e, du+w)) <= delta
    return delta, tuple(x-y for x,y in zip(LIMIT,size)), UMAX-feedback_bound


def terminal_check(x, limits, input_limit):
    # H0 z<=h0 and H0 Fz<=h0. Linear rows, F^2=0.
    for z in (x, step(x, gain(x))):
        assert all(abs(v)<=b for v,b in zip(z,limits))
        assert abs(gain(z))<=input_limit
    fx = step(x,gain(x))
    assert step(fx,gain(fx)) == ZERO


def augmented_lp(word, deadline):
    """Independent three-lag-bank LP; each packet constrains its arrival-time bank."""
    import numpy as np
    from scipy.optimize import linprog

    k = len(word)-1
    width = 6
    nw = width*(k+1)
    dim = nw+k
    eq = []
    def equality(terms):
        row = np.zeros(dim)
        for col,c in terms:
            row[col] += float(c)
        eq.append(row)
    for j in range(k):
        now, nxt, noise_col = width*j, width*(j+1), nw+j
        equality([(nxt,1),(now,-1),(now+1,-T),(noise_col,-T*T/2)])
        equality([(nxt+1,1),(now+1,-1),(noise_col,-T)])
        for col in range(4):
            equality([(nxt+2+col,1),(now+col,-1)])
    bounds = [(None,None)]*nw + [(-W,W)]*k
    bounds[:width] = [(-r,r) for r in estimation.INITIAL] + [(0,0)]*4
    strips = []
    for s,d in enumerate(word):
        if d == estimation.ABSENT:
            continue
        arrival = s+(2 if deadline else d)
        if arrival > k:
            continue
        lag = arrival-s
        row = np.zeros(dim)
        row[width*arrival+2*lag] = 1
        strips.extend((row,-row))
    result = []
    for coord, sign in product((0,1),(-1,1)):
        c = np.zeros(dim)
        c[width*k+coord] = -sign
        lp = linprog(c,A_eq=eq,b_eq=np.zeros(len(eq)),A_ub=strips,
                     b_ub=np.full(len(strips),float(NOISE)),bounds=bounds,method="highs")
        if not lp.success:
            raise ValueError(lp.message)
        result.append(-lp.fun)
    return result


def tail(first, radii, delta, limits, nominal_u):
    plan = tuple(first*m for m in PROFILE)
    assert len(plan)==N
    states = [ZERO]
    for u in plan:
        states.append(step(states[-1],u))
    assert states[-1]==ZERO and abs(first)<=UMAX
    # At the common zero-readout prefix the midpoint is zero, so du_8=0.
    for e in corners(radii):
        assert gauge(e)<=delta
    next_error = [step(e,w) for e in corners(radii) for w in (-W,W)]
    next_position_slack = LIMIT[0]-max(abs(states[1][0]+p) for p,v in next_error)
    next_speed_slack = LIMIT[1]-max(abs(states[1][1]+v) for p,v in next_error)
    entry_slack = delta-max(gauge(e) for e in next_error)
    assert min(next_position_slack,next_speed_slack,entry_slack)>=0
    u_slack = min(nominal_u-abs(u) for u in plan[1:])
    state_slack = tuple(min(bound-abs(x[i]) for x in states[2:])
                        for i,bound in enumerate(limits))
    assert min(u_slack,*state_slack)>=0
    terminal_check(states[-1],limits,nominal_u)
    return dict(next_position_slack=next_position_slack,
                next_speed_slack=next_speed_slack,entry_slack=entry_slack,
                tail_input_slack=u_slack,tail_state_slack=state_slack)


def available(word, k, deadline):
    return tuple(s for s,d in enumerate(word)
                 if d != estimation.ABSENT and s + (2 if deadline else d) <= k)


def audit(saved=None):
    assert T==Q(1,2)
    steady_error = (Q(3,50),Q(31,600))
    delta, limits, nominal_u = design(steady_error)
    start_error = (Q(37,400),Q(3,50))
    start_delta, start_limits, start_u = design(start_error)
    assert min(*start_limits,start_u)>0
    assert max(gauge(e) for e in corners(estimation.INITIAL))<=start_delta
    for e, a, b in product(tube_corners(start_delta),(-delta,delta),(-delta,delta)):
        f1=step(e,gain(e)+a)
        assert gauge(step(f1,gain(f1)+b))<=delta
    for x in corners((Q(1,4),Q(1,4))):
        terminal_check(x,limits,nominal_u)
    results={}
    for name,word in (("main",MAIN),("late",LATE)):
        cases={}
        for label,deadline in (("immediate",False),("deadline",True)):
            stamps=available(word,8,deadline)
            certs={}
            for axis in ("p","v"):
                old = saved["cases"][name][label]["certs"][axis] if saved else None
                certs[axis]=estimation.support(8,stamps,axis,old)
            radii=tuple(Q(certs[a]["radius"]) for a in ("p","v"))
            first=min(UMAX,(LIMIT[1]-radii[1])/T-W)
            margin=tail(first,radii,delta,limits,nominal_u)
            assert margin==tail(-first,radii,delta,limits,nominal_u)
            assert margin["next_speed_slack"]==0
            static=tail(nominal_u,radii,delta,limits,nominal_u)
            assert T*nominal_u<=limits[1] and T*T*nominal_u/2<=limits[0]
            assert static["next_speed_slack"]>0
            numeric = (saved["cases"][name][label]["augmented_lp"] if saved
                       else augmented_lp(word,deadline))
            assert max(abs(float(q)-v) for q,v in zip((radii[0],radii[0],radii[1],radii[1]),numeric,strict=True))<1e-10
            cases[label]=dict(stamps=stamps,certs=certs,augmented_lp=numeric,first_max=first,
                              margin=margin,static_first_max=nominal_u)
        results[name]=cases
    assert results["late"]["immediate"]["first_max"]==results["late"]["deadline"]["first_max"]
    gap=results["main"]["immediate"]["first_max"]-results["main"]["deadline"]["first_max"]
    assert gap>0
    # Stamp 8 was not delivered by decision 8. At 9 both 8 and 9 may arrive.
    arrivals=set()
    for d8,d9 in product((-1,1,2),(-1,0,1,2)):
        if d8==d9==-1:
            continue
        arrivals.add(tuple(s for s,d in ((8,d8),(9,d9)) if d>=0 and s+d==9))
    assert arrivals=={(),(8,),(9,),(8,9)}
    return dict(cases=results,first_max_gap=gap,buffer_violation_at_immediate_max=T*gap,
                steady_delta=delta,steady_limits=limits,steady_nominal_u=nominal_u,
                startup_delta=start_delta,successor_arrivals=sorted(arrivals))


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify",type=Path)
    args=parser.parse_args()
    saved=json.loads(args.verify.read_text(encoding="utf-8-sig")) if args.verify else None
    record=audit(saved)
    files=[Path(__file__).resolve(), Path(estimation.__file__).resolve(),
           HERE/"control_prefix_protocol.md", HERE/"reduction_protocol.json", HERE/"CDC22_REDUCTION.md"]
    record["hashes"]={p.name:sha256(p.read_bytes()).hexdigest() for p in files}
    if saved:
        for k,v in json.loads(json.dumps(record,default=str)).items():
            assert saved[k]==v,k
        print("Verified Fraction supports and tail margins, physical witnesses, RPI, terminal and successor cases.")
    else:
        import numpy,scipy
        record["environment"]=dict(python=platform.python_version(), numpy=numpy.__version__,
                                   scipy=scipy.__version__,seed=None)
        print(json.dumps(record,indent=2,default=str))
