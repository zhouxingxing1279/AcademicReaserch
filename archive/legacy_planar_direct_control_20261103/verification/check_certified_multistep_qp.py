#!/usr/bin/env python3
"""Real LP queries and dense four-stage QP certificates at fixed initial posteriors.

No synthetic support inflation. Not a rolling partial-observation controller.
Timing includes rational audit overhead and is not a real-time certificate.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import time
import sys
import numpy as np
import scipy
from scipy.optimize import linprog, minimize, LinearConstraint, nnls
import check_multidim_tube_qp as base
from check_compression_performance import cz_support_certificate

ROOT=Path(__file__).resolve().parents[1]
STRIP=Q(1,50)
M=np.array([Q(1,10),Q(1,10),STRIP],dtype=object)
HSET=np.array([[Q(1,10),Q(0),Q(0)],[Q(0),Q(1,10),Q(0)]],dtype=object)


def exact_support(p):
    return cz_support_certificate(STRIP,tuple(p))[0]


def query(p):
    """One numerical LP; certify dual upper and reconstruct a feasible vertex."""
    p=np.array(p,dtype=object)
    objective=p@HSET
    result=linprog(-np.array(objective,dtype=float),A_eq=np.array([M],dtype=float),
                   b_eq=[0.0],bounds=(-1,1),method='highs')
    lam=Q(0)
    point=np.array([Q(0),Q(0)],dtype=object)
    if result.success:
        lam=Q(float(-result.eqlin.marginals[0])).limit_denominator(10**9)
        # Three latent variables, one equality: choose two proposed bound coordinates.
        for active in combinations(range(3),2):
            if not all(abs(abs(result.x[j])-1)<1e-7 for j in active): continue
            xi=np.full(3,Q(0),dtype=object)
            for j in active: xi[j]=Q(1 if result.x[j]>0 else -1)
            free=next(j for j in range(3) if j not in active)
            xi[free]=-sum(M[j]*xi[j] for j in active)/M[free]
            if all(abs(x)<=1 for x in xi) and M@xi==0:
                candidate=HSET@xi
                if p@candidate>p@point: point=candidate
    upper=sum(abs(v) for v in objective-lam*M)
    lower=p@point
    assert all(abs(v)<=Q(1,10) for v in point) and abs(sum(point))<=STRIP
    assert lower<=upper
    return lower,upper,point


def inverse(matrix):
    n=len(matrix)
    augmented=np.hstack((matrix.copy(),base.eye(n)))
    for j in range(n):
        pivot=next(i for i in range(j,n) if augmented[i,j])
        augmented[[j,pivot]]=augmented[[pivot,j]]
        augmented[j]=augmented[j]/augmented[j,j]
        for i in range(n):
            if i!=j: augmented[i]-=augmented[i,j]*augmented[j]
    return augmented[:,n:]


def build(z,scenario='regulation'):
    assert scenario in ('regulation','active_maneuver')
    z=np.array(z,dtype=object)
    zero=base.zeros(base.N,2)
    state=z.copy()
    plan=[]
    for _ in range(base.N):
        plan.append(base.K@state)
        state=base.AC@state
    fallback=np.array(plan,dtype=object).ravel()
    zero_rows=list(base.control_rows(z,zero))
    b=np.array([bound for _,_,bound in zero_rows]+[Q(1,5)-s*x
         for x in base.nominal(z,zero)[-1] for s in (-1,1)],dtype=object)
    directions=[]
    constants=[]
    for q,i,_ in zero_rows:
        p,noise=base.pull_noise(q,i)
        directions.append(p[:2])  # known current d=0
        constants.append(noise)
    directions.extend([np.array([Q(0),Q(0)],dtype=object)]*4)
    constants.extend([Q(0)]*4)
    columns=[]
    for j in range(8):
        unit=zero.copy(); unit.flat[j]=Q(1)
        bounds=np.array([bound for _,_,bound in base.control_rows(z,unit)]+
                        [Q(1,5)-s*x for x in base.nominal(z,unit)[-1] for s in (-1,1)],dtype=object)
        columns.append(b-bounds)
    D=np.array(columns,dtype=object).T
    c=base.objective(z,zero)
    f=base.zeros(8,1).ravel()
    H=base.zeros(8,8)
    plus=[]
    for j in range(8):
        unit=zero.copy();unit.flat[j]=Q(1)
        jp=base.objective(z,unit); jm=base.objective(z,-unit)
        plus.append(jp); f[j]=(jp-jm)/2; H[j,j]=jp+jm-2*c
    for i in range(8):
        for j in range(i):
            unit=zero.copy();unit.flat[i]=unit.flat[j]=Q(1)
            H[i,j]=H[j,i]=base.objective(z,unit)-plus[i]-plus[j]+c
    if scenario=='active_maneuver':
        # State limit .5 retains the same R/Zf terminal containment exactly.
        b[:4*(base.N+1)]-=Q(3,2)
        # One known input-reference pulse at the present absolute time only.
        H[0,0]+=Q(200);f[0]-=Q(80);c+=Q(16)
    inv=inverse(H)
    assert np.array_equal(H@inv,base.eye(8))
    true_support=np.array([exact_support(p)+w for p,w in zip(directions,constants)],dtype=object)
    assert min(b-D@fallback-true_support)>=0
    return dict(z=z,b=b,D=D,H=H,Hinv=inv,f=f,c=c,fallback=fallback,
                directions=directions,constants=np.array(constants,dtype=object),
                true_support=true_support)


def cost(d,v): return d['c']+d['f']@v+v@d['H']@v/2


def dual_value(d,bound,lam):
    if any(x<0 for x in lam): raise ValueError('Dual multipliers must be nonnegative')
    gradient=d['f']+d['D'].T@lam
    return d['c']-lam@bound-gradient@d['Hinv']@gradient/2


def optimize(d,bound,incumbent):
    D=np.array(d['D'],dtype=float)
    H=np.array(d['H'],dtype=float); f=np.array(d['f'],dtype=float)
    varying=np.any(D!=0,axis=1)
    slack=bound-d['D']@incumbent
    assert min(slack)>=0
    inset=np.array([min(Q(1,10**6),s/10) for s in slack],dtype=float)
    result=minimize(lambda v:float(d['c'])+f@v+v@H@v/2,
                    np.array(incumbent,dtype=float),jac=lambda v:f+H@v,method='SLSQP',
                    constraints=[LinearConstraint(D[varying],-np.inf,
                                  np.array(bound,dtype=float)[varying]-inset[varying])],
                    options={'ftol':1e-11,'maxiter':150})
    chosen=incumbent
    if np.all(np.isfinite(result.x)):
        proposed=np.array([Q(round(float(v)*10**8),10**8) for v in result.x],dtype=object)
        if min(bound-d['D']@proposed)>=0 and cost(d,proposed)<cost(d,incumbent): chosen=proposed
    # Multiplier proposal only; any rational nonnegative result gives weak duality.
    active=np.flatnonzero(varying & (np.array(bound-d['D']@chosen,dtype=float)<=1e-5))
    lam=np.full(len(bound),Q(0),dtype=object)
    if len(active):
        try:
            coefficients,_=nnls(D[active].T,-np.array(d['f']+d['H']@chosen,dtype=float),maxiter=1000)
            for j,value in zip(active,coefficients): lam[j]=Q(float(max(0,value))).limit_denominator(10**8)
        except RuntimeError:
            pass  # Zero multipliers remain a valid, possibly weak certificate.
    return chosen,lam


def execute(mode,z=(Q(4,5),-Q(2,5)),budget=36,tolerance=Q(1,10000),batch=4,initial_bounds='box',scenario='regulation'):
    assert mode in ('all_at_once','priority','fixed_order')
    assert initial_bounds in ('caps_only','box')
    started=time.perf_counter()
    d=build(z,scenario)
    setup_seconds=time.perf_counter()-started
    upper={};lower={};row_keys=[];scales=[]
    for j,p in enumerate(d['directions']):
        key,scale=base.canonical(p)
        row_keys.append(key);scales.append(scale)
        if not any(key): continue
        cap=(d['b'][j]-d['D'][j]@d['fallback']-d['constants'][j])/scale
        if initial_bounds=='box': cap=min(cap,sum(abs(v) for v in key)/10)
        upper[key]=min(upper.get(key,cap),cap)
        lower[key]=Q(0)  # The verified CZ point e=0.
    remaining=set(upper)
    queried=[];records=[]
    v=d['fallback'].copy()
    best_lower=Q(0)  # All objectives in these experiments are sums of squares.
    count=0
    previous_primal=cost(d,v)
    while True:
        if mode=='all_at_once' and count==0:
            selected=sorted(remaining)[:budget]
            for key in selected:
                lo,hi,point=query(key);count+=1;queried.append(key);remaining.remove(key)
                upper[key]=min(upper[key],hi)
                for other in lower: lower[other]=max(lower[other],np.array(other,dtype=object)@point)
        sU=np.array([d['constants'][j]+(scales[j]*upper[key] if any(key) else 0)
                     for j,key in enumerate(row_keys)],dtype=object)
        sL=np.array([d['constants'][j]+(scales[j]*lower[key] if any(key) else 0)
                     for j,key in enumerate(row_keys)],dtype=object)
        assert all(sL<=d['true_support']) and all(d['true_support']<=sU)
        v,lam=optimize(d,d['b']-sU,v)
        primal=cost(d,v)
        assert primal<=previous_primal
        previous_primal=primal
        g=dual_value(d,d['b']-sL,lam)
        optimizer_gap=primal-dual_value(d,d['b']-sU,lam)
        support_gap=lam@(sU-sL)
        assert optimizer_gap>=0 and support_gap>=0
        assert primal-g==optimizer_gap+support_gap
        best_lower=max(best_lower,g)
        gap=primal-best_lower
        assert gap>=0
        records.append({'queries':count,'primal_value':float(primal),'lower_value':float(best_lower),
                        'certified_gap':float(gap),'current_optimizer_gap':float(optimizer_gap),
                        'current_support_gap':float(support_gap)})
        if gap<=tolerance or count>=budget or not remaining or mode=='all_at_once': break
        scores={key:Q(0) for key in remaining}
        for j,key in enumerate(row_keys):
            if key in scores: scores[key]+=lam[j]*scales[j]*(upper[key]-lower[key])
        order=sorted(remaining,key=lambda key:(-scores[key],key)) if mode=='priority' else sorted(remaining)
        selected=order[:min(batch,budget-count)]
        for key in selected:
            lo,hi,point=query(key);count+=1;queried.append(key);remaining.remove(key)
            upper[key]=min(upper[key],hi)
            for other in lower: lower[other]=max(lower[other],np.array(other,dtype=object)@point)
    plan=v.reshape(4,2)
    next_z=base.A@d['z']+plan[0]
    stage=10*(d['z']@d['z'])+plan[0]@plan[0]
    if scenario=='active_maneuver': stage+=100*(plan[0,0]-Q(2,5))**2
    # The pulse is removed after this absolute time, not restarted at every solve.
    shift_slack=primal-stage-base.objective(next_z,base.shifted(d['z'],plan))
    assert shift_slack>=0
    return {'mode':mode,'scenario':scenario,'initial_bounds':initial_bounds,'initial_z':[str(x) for x in z],'query_budget':budget,
            'support_lp_calls':count,'available_directions':len(upper),'qp_calls':len(records),
            'tolerance':float(tolerance),'tolerance_met':bool(gap<=tolerance),
            'stop_reason':'certified_tolerance' if gap<=tolerance else
                           ('all_queries_completed' if not remaining else 'query_budget_exhausted'),
            'objective_improvement':float(cost(d,d['fallback'])-primal),
            'shift_cost_slack':float(shift_slack),
            'minimum_robust_margin':float(min(d['b']-d['D']@v-d['true_support'])),
            'certificate_gap_exact':str(gap),'final_plan':[[str(x) for x in row] for row in v.reshape(4,2)],
            'query_order':[[str(x) for x in key] for key in queried],
            'setup_seconds':setup_seconds,'wall_seconds':time.perf_counter()-started,'records':records}


def run():
    sources=['check_certified_multistep_qp.py','check_multidim_tube_qp.py',
             'check_compression_performance.py','check_constrained_zonotope.py']
    cases=[(Q(4,5),-Q(2,5)),(Q(2,5),Q(4,5)),(Q(3,4),Q(11,20))]
    runs=[execute(mode,z,initial_bounds=initial) for initial in ('caps_only','box')
          for z in cases for mode in ('all_at_once','fixed_order','priority')]
    runs.extend(execute('priority',cases[0],budget=b,initial_bounds='caps_only') for b in (0,4,8))
    runs.extend(execute(mode,(Q(1,5),Q(1,5)),scenario='active_maneuver')
                for mode in ('all_at_once','fixed_order','priority'))
    runs.append(execute('priority',(Q(1,5),Q(1,5)),scenario='active_maneuver',budget=0))
    return {'scope':'Fixed-posterior four-step MPC snapshots; not a rolling partial-observation experiment',
            'versions':{'python':sys.version.split()[0],'numpy':np.__version__,'scipy':scipy.__version__},
            'source_sha256':{name:hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest()
                             for name in sources},'runs':runs}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();result=run()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps([{k:v for k,v in r.items() if k not in ('records','final_plan')}
                       for r in result['runs']],indent=2))
