#!/usr/bin/env python3
"""Exact active-constraint witness; single-time comparison, NOT a closed-loop test.

Partial measurement cuts a prior square. Exact rational polygon operations
audit the entire posterior. The one-step QP separates into two input intervals,
so its optimum and dual multipliers are algebraic, without solver tolerances.
"""
from fractions import Fraction as Q
from pathlib import Path
from itertools import product
import argparse
import hashlib
import json

A=((Q(4,5),Q(1,5)),(-Q(1,5),Q(4,5)))
TARGET=(Q(9,50),Q(0))
STATE=Q(1,5)
NOISE=Q(1,100)
INPUT=Q(2,5)
BOX=[(-Q(1,10),-Q(1,10)),(Q(1,10),-Q(1,10)),
     (Q(1,10),Q(1,10)),(-Q(1,10),Q(1,10))]


def dot(a,b): return sum(x*y for x,y in zip(a,b))


def clip(vertices,p,b):
    """Closed-halfspace clipping of a counterclockwise convex polygon."""
    if not vertices: return []
    result=[]
    previous=vertices[-1]
    hp=dot(p,previous)-b
    for current in vertices:
        hc=dot(p,current)-b
        if (hp<=0)!=(hc<=0):
            t=hp/(hp-hc)
            result.append(tuple(a+t*(c-a) for a,c in zip(previous,current)))
        if hc<=0: result.append(current)
        previous,hp=current,hc
    return list(dict.fromkeys(result))


def support(vertices,p):
    if not vertices: raise ValueError('Empty uncertainty set')
    return max(dot(p,x) for x in vertices)


def posterior(strip):
    # Prior center is zero; y=e1+e2+nu=0, |nu|<=strip.
    return clip(clip(BOX,(Q(1),Q(1)),strip),(-Q(1),-Q(1)),strip)


def cz_support_certificate(strip,p):
    # H=diag(.1,.1) with a zero third column, M=(.1,.1,strip), b=0.
    # Dual is piecewise linear with breakpoints 0,p1,p2; a minimum occurs there.
    def dual(lam):
        return abs((p[0]-lam)/10)+abs((p[1]-lam)/10)+abs(strip*lam)
    multiplier=min((Q(0),p[0],p[1]),key=dual)
    vertex=max(posterior(strip),key=lambda v:dot(p,v))
    lower=dot(p,vertex)
    upper=dual(multiplier)
    assert lower==upper
    return lower,upper,multiplier,vertex


def quadratic_dual(target,weights,normals,bounds,multipliers):
    """Certified dual lower value for a diagonal positive quadratic objective."""
    if len(weights)!=len(target) or any(w<=0 for w in weights):
        raise ValueError('Positive diagonal objective required')
    if not len(normals)==len(bounds)==len(multipliers):
        raise ValueError('Mismatched constraint rows')
    if any(len(a)!=len(target) for a in normals) or any(lam<0 for lam in multipliers):
        raise ValueError('Invalid dimensions or negative multiplier')
    gradient=[sum(lam*a[j] for lam,a in zip(multipliers,normals))
              for j in range(len(target))]
    return sum(lam*(dot(a,target)-b) for lam,a,b in zip(multipliers,normals,bounds))-sum(
        g*g/(4*w) for g,w in zip(gradient,weights))


def rows():
    return [(axis,sign,tuple(sign*a for a in A[axis]))
            for axis in range(2) for sign in (-1,1)]


def action_intervals(vertices):
    bounds=[]
    for p in A:
        lower=max(-INPUT,-STATE+NOISE+support(vertices,tuple(-a for a in p)))
        upper=min(INPUT,STATE-NOISE-support(vertices,p))
        if lower>upper: raise ValueError('Empty robust action interval')
        bounds.append((lower,upper))
    return bounds


def cost(u): return sum((x-r)**2 for x,r in zip(u,TARGET))


def solve(vertices):
    bounds=action_intervals(vertices)
    u=tuple(max(lo,min(hi,r)) for (lo,hi),r in zip(bounds,TARGET))
    return {'u':u,'cost':cost(u),'intervals':bounds}


def feasible(vertices,u):
    return all(lo<=v<=hi for (lo,hi),v in zip(action_intervals(vertices),u))


def interpolation_factor(deltas,margins):
    if len(deltas)!=len(margins): raise ValueError('Mismatched rows')
    theta=Q(0)
    for delta,margin in zip(deltas,margins):
        if delta<0 or margin<0 or delta>margin:
            raise ValueError('Outer inclusion and candidate retention are required')
        if margin: theta=max(theta,delta/margin)
    return theta


def compressed(vertices,candidate,epsilon):
    result=BOX.copy()
    halfspaces=[]
    for axis,sign,p in rows():
        cap=STATE-NOISE-sign*candidate[axis]
        bound=cap if epsilon is None else min(cap,support(vertices,p)+epsilon)
        assert all(dot(p,v)<=bound for v in vertices)
        halfspaces.append((p,bound))
        result=clip(result,p,bound)
    assert result
    # Convexity + all original vertices verifies inclusion of the whole posterior.
    assert all(all(dot(p,v)<=b for p,b in halfspaces) for v in vertices)
    return result,halfspaces


def case(strip=Q(1,50),margin=Q(3,500),epsilon=Q(3,1000)):
    original=posterior(strip)
    full=solve(original)
    candidate=(full['u'][0]-margin,Q(0))
    assert feasible(original,candidate)
    outer,halfspaces=compressed(original,candidate,epsilon)
    approximate=solve(outer)
    assert feasible(outer,candidate)
    deltas=[]
    margins=[]
    for axis,sign,p in rows():
        lower,upper,_,_=cz_support_certificate(strip,p)
        assert lower==support(original,p)==upper
        delta=support(outer,p)-support(original,p)
        slack=STATE-NOISE-sign*candidate[axis]-support(original,p)
        assert 0<=delta<=slack
        if epsilon is not None: assert delta<=epsilon
        deltas.append(delta)
        margins.append(slack)
    theta=interpolation_factor(deltas,margins)
    blended=tuple((1-theta)*u+theta*c for u,c in zip(full['u'],candidate))
    assert feasible(outer,blended)
    gap=approximate['cost']-full['cost']
    interpolation=theta*(cost(candidate)-full['cost'])
    quadratic=interpolation-theta*(1-theta)*sum((a-b)**2 for a,b in zip(candidate,full['u']))
    assert 0<=gap<=quadratic<=interpolation
    # Here only the upper first-state row is active; certify its exact multiplier.
    assert full['u'][1]==approximate['u'][1]==0
    old_lam=2*(TARGET[0]-full['u'][0])
    new_lam=2*(TARGET[0]-approximate['u'][0])
    assert old_lam>=0 and new_lam>=0
    active_delta=deltas[1]
    old_linear=old_lam*active_delta
    dual_upper=new_lam*active_delta
    assert old_linear<=gap<=dual_upper
    # A usable posterior support lower bound is a maximising posterior vertex.
    primal_witness=max(original,key=lambda v:dot(A[0],v))
    lower_support=dot(A[0],primal_witness)
    relaxed_upper=STATE-NOISE-lower_support
    # g(lambda) for min ||u-TARGET||² subject to u1<=relaxed_upper.
    lower_value=quadratic_dual(TARGET,(Q(1),Q(1)),[(Q(1),Q(0))],[relaxed_upper],[new_lam])
    a_posteriori=approximate['cost']-lower_value
    assert a_posteriori==dual_upper
    assert lower_value<=full['cost']
    return {'strip':strip,'candidate_margin':margin,'epsilon':epsilon,
        'u':approximate['u'],'cost':approximate['cost'],'full_cost':full['cost'],
        'candidate':candidate,'candidate_cost':cost(candidate),'cost_gap':gap,
        'theta':theta,'interpolation_bound':interpolation,
        'quadratic_interpolation_bound':quadratic,
        'old_dual_linear_term':old_linear,'new_dual_bound':dual_upper,
        'a_posteriori_bound':a_posteriori,'certified_original_value_lower':lower_value,
        'support_lower_witness':primal_witness,'support_deltas':deltas,
        'row_margins':margins,'box_retains_candidate':feasible(BOX,candidate),
        'posterior_vertices':original,'outer_vertices':outer,
        'protected_halfspaces':halfspaces}


def witness():
    original=posterior(Q(1,50))
    queried=case()
    return {'full':solve(original),'box':solve(BOX),
            'missing':case(epsilon=None),'queried':queried,
            'box_retains_candidate':queried['box_retains_candidate']}


def sweep():
    widths=[Q(1,200),Q(1,100),Q(1,50),Q(1,20),Q(1,10),Q(1,5)]
    margins=[Q(0),Q(1,1000),Q(3,1000),Q(3,500),Q(1,50),Q(1,20)]
    epsilons=[Q(0),Q(1,1000),Q(3,1000),Q(1,100),Q(1,10),None]
    records=[case(s,m,e) for s,m,e in product(widths,margins,epsilons)]
    return {'cases':len(records),'failures':0,
            'box_candidate_losses':sum(not r['box_retains_candidate'] for r in records),
            'strict_cost_loss_cases':sum(r['cost_gap']>0 for r in records),
            'old_dual_underestimates':sum(r['old_dual_linear_term']<r['cost_gap'] for r in records),
            'records':records}


def stopping_probe(tolerance=Q(1,2500),budget=2):
    """Synthetic query rounds at one fixed posterior, not wall-clock interruption."""
    if tolerance<0 or budget<0: raise ValueError('Nonnegative tolerance/budget required')
    trace=[]
    settings=[None]+[Q(1,100),Q(3,1000),Q(1,1000),Q(0)][:budget]
    for round_index,epsilon in enumerate(settings):
        r=case(epsilon=epsilon)
        trace.append({'query_rounds':round_index,'epsilon':epsilon,'u':r['u'],
                      'cost':r['cost'],'certified_gap':r['a_posteriori_bound'],
                      'actual_gap_for_audit':r['cost_gap']})
        assert r['cost_gap']<=r['a_posteriori_bound']
        if r['a_posteriori_bound']<=tolerance:
            return {'tolerance_met':True,'reason':'certificate','trace':trace}
    return {'tolerance_met':False,'reason':'query_budget_exhausted','trace':trace}


def encode(value):
    if isinstance(value,Q): return str(value)
    if isinstance(value,dict): return {k:encode(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [encode(v) for v in value]
    return value


def run():
    return {'scope':'Single-time exact robust QP comparison; partial measurement; not closed-loop or quadrotor',
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'witness':witness(),'sweep':sweep(),
            'stopping_probe':stopping_probe(),'zero_budget_probe':stopping_probe(budget=0)}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result=run()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(encode(result),indent=2)+'\n')
    print(json.dumps(encode({'witness':result['witness'],
          'sweep':{k:v for k,v in result['sweep'].items() if k!='records'}}),indent=2))
