"""Exact optimality and reachability audit for the additional nonzero-prefix case."""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
import sys
from pathlib import Path

import control_prefix_check as case

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0,str(ROOT/"experiments"))
from oit_window4_certificate import solve_square  # rational elimination only

R = Q(1,5)
Z8 = (Q(-5,2),Q(0))
CAP = case.N
FRACTION_ZERO = tuple(Q(0) for _ in range(CAP))


def trajectory(z, commands):
    states = [z]
    for u in commands:
        states.append(case.step(states[-1],u))
    return states


def closed(x):
    return case.step(x,case.gain(x))


def stage_pair(x,y):
    return 4*x[0]*y[0]+x[1]*y[1]


def terminal_pair(x,y):
    return sum(stage_pair(a,b)+R*case.gain(a)*case.gain(b)
               for a,b in ((x,y),(closed(x),closed(y))))


def cost_pair(xs,us,ys,vs):
    return sum(stage_pair(x,y)+R*u*v for x,u,y,v in
               zip(xs[:-1],us,ys[:-1],vs,strict=True))+terminal_pair(xs[-1],ys[-1])


def prefix_proof(start, steady):
    c = Q(5,8)
    # From z_0=0 to Z8 and back to zero. Not every early decision has to
    # commit to that entire excursion. At k=0 it can turn back immediately.
    route = [-c]*4+[c]*8+[-c]*4+[Q(0)]*CAP
    nominal = trajectory(case.ZERO,route)
    assert nominal[8]==Z8
    margins=[]
    for k in range(8):
        plan = route[k:k+CAP] if k else [-c,c,c,-c]+[Q(0)]*(CAP-4)
        assert len(plan)==CAP and plan[0]==route[k]
        xs=trajectory(nominal[k],plan)
        slacks=[]
        for i,z in enumerate(xs):
            _,limits,u_limit = start if k+i<8 else steady
            slacks.extend(b-abs(a) for a,b in zip(z,limits,strict=True))
            if i<CAP:
                slacks.append(u_limit-abs(plan[i]))
        case.terminal_check(xs[-1],steady[1],steady[2])
        assert min(slacks)>0
        margins.append(min(slacks))
    return {"commands":route[:8],"positions":[x[0] for x in nominal[:9]],
            "min_prefix_state_input_slack_numeric_units":min(margins)}


def optimal(plan_cap, radii, steady):
    delta,limits,u_limit=steady
    # Float reconnaissance predicted two active rows. Only the exact
    # subsequent KKT test decides whether that conjecture is valid.
    impulses=[]
    for j in range(CAP):
        unit=list(FRACTION_ZERO)
        unit[j]=Q(1)
        impulses.append((trajectory(case.ZERO,unit),unit))
    us=list(FRACTION_ZERO)
    us[0]=plan_cap
    us[1]=limits[1]/case.T-us[0]
    initial=trajectory(Z8,us)
    free=impulses[2:]
    hessian=[[2*cost_pair(*x,*y) for y in free] for x in free]
    rhs=[-2*cost_pair(initial,us,*x) for x in free]
    us[2:]=solve_square(hessian,rhs)
    xs=trajectory(Z8,us)
    gradient=[2*cost_pair(xs,us,*x) for x in impulses]
    mu2=-gradient[1]/case.T
    mu1=(gradient[1]-gradient[0])/case.T
    assert min(mu1,mu2)>0
    assert gradient[0]+case.T*(mu1+mu2)==gradient[1]+case.T*mu2==0
    assert all(v==0 for v in gradient[2:])
    # Exact one-step speed support, conservative p row (slack here).
    rp,rv=radii
    p1=rp+case.T*rv+case.T**2*case.W/2
    v1=rv+case.T*case.W
    assert abs(xs[1][0])+p1 < case.LIMIT[0]
    assert xs[1][1]+v1 == case.LIMIT[1] and xs[2][1] == limits[1]
    assert 4*p1+v1<=delta and 4*rp+rv<=delta
    assert all(abs(a)+r<=b for a,r,b in zip(Z8,radii,case.LIMIT,strict=True))
    assert abs(us[0])<=case.UMAX
    tail_input=min(u_limit-abs(u) for u in us[1:])
    assert tail_input>0
    tail_state=[min(b-abs(x[i]) for x in xs[2:]) for i,b in enumerate(limits)]
    assert tail_state[0]>0 and tail_state[1]==0
    case.terminal_check(xs[-1],limits,u_limit)
    appended = case.gain(xs[-1])
    shifted = xs[1:]
    assert abs(appended)<=u_limit
    case.terminal_check(closed(shifted[-1]),limits,u_limit)
    # For *every* successor, the physical second speed error uses
    # (Fe1)_v=-2*ep-ev/2, plus B_v times a bounded omega.
    physical_second_slack=case.LIMIT[1]-abs(xs[2][1])-(2*p1+v1/2+delta/2)
    assert physical_second_slack>0
    return {"first":us[0],"second":us[1],"optimal_plan":us,"terminal":xs[-1],
            "speed_multipliers":(mu1,mu2),"tail_nominal_slack":tail_state,
            "tail_input_slack":tail_input,"all_successors_second_speed_slack":physical_second_slack,
            "appended_nominal":appended,"cost":cost_pair(xs,us,xs,us)}


def main():
    first_file=HERE/"control_prefix_certificate.json"
    first=json.loads(first_file.read_text(encoding="utf8"))
    steady=case.design((Q(3,50),Q(31,600)))
    start=case.design((Q(37,400),Q(3,50)))
    result={"prefix":prefix_proof(start,steady),"solutions":{}}
    for word,cases in first["cases"].items():
        for label,r in cases.items():
            # Actual commands at earlier decisions equal the known prefix
            # commands on the zero-innovation witness. Subtract their forced
            # response from both trajectory and delivered output equations.
            certs=r["certs"]
            for axis,cert in certs.items():
                case.estimation.support(8,tuple(r["stamps"]),axis,cert)
            radii=tuple(Q(certs[a]["radius"]) for a in ("p","v"))
            cap=(case.LIMIT[1]-radii[1])/case.T-case.W
            assert cap==Q(r["first_max"])
            result["solutions"][word+"_"+label]=optimal(cap,radii,steady)
    assert result["solutions"]["late_deadline"]==result["solutions"]["late_immediate"]
    result["hashes"]={p.name:sha256(p.read_bytes()).hexdigest() for p in
                      (first_file,Path(__file__),HERE/"control_prefix_cost_extension.md",
                       ROOT/"experiments/oit_window4_certificate.py")}
    return result


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify",type=Path)
    args=parser.parse_args()
    result=json.dumps(main(),indent=2,default=str)
    if args.verify:
        assert json.loads(result)==json.loads(args.verify.read_text(encoding="utf-8-sig"))
        print("Verified all eight prefix continuations, four rational KKT solutions and shifted tails.")
    else:
        print(result)
