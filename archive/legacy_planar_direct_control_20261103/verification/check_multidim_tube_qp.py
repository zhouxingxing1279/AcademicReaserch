#!/usr/bin/env python3
"""Two-state output-feedback QP pilot. Rational safety checks, numerical proposals.

Every mode uses the same measurement history conditioning, known d graph,
certified shifted-plan caps, and objective. Timings are observations, not WCET.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import hashlib
import json
import time
import numpy as np
from scipy.optimize import minimize, LinearConstraint
from check_constrained_zonotope import CZ, eye, zeros

ROOT = Path(__file__).resolve().parents[1]
A = np.array([[Q(4,5), Q(1,5)], [-Q(1,5), Q(4,5)]], dtype=object)
I = eye(2)
K = -I/2
AC = A+K
F = np.block([[A/2, zeros(2,2)], [A/2, AC]])
G = np.block([[I/2, -I/2], [I/2, I/2]])
RAD = np.array([Q(1,100)]*2+[Q(1,50)]*2, dtype=object)
TX = np.hstack((I,I))
TU = np.hstack((zeros(2,2),K))
RR = np.array([Q(1,10)]*2+[Q(1,5)]*2, dtype=object)
N = 4
P = 12*I


def canonical(p):
    p = np.array(p, dtype=object)
    scale = next((abs(x) for x in p if x), Q(1))
    return tuple(p/scale), scale


class Estimator:
    def __init__(self, cz, caps=()):
        self.cz = cz
        self.caps = {}
        self.cache = {}
        self.lp_count = 0
        self.compression_lp_count = 0
        for p, b in caps:
            key, scale = canonical(p)
            self.caps[key] = min(self.caps.get(key, b/scale), b/scale)

    def support(self, p):
        key, scale = canonical(p)
        if key not in self.cache:
            value, _ = self.cz.support_certificate(key)
            self.lp_count += bool(len(self.cz.b))
            self.cache[key] = min(value, self.caps.get(key, value))
        return scale*self.cache[key]


def pull_noise(q, i):
    p = np.array(q, dtype=object)
    noise = Q(0)
    for _ in range(i):
        noise += sum(abs(x)*r for x,r in zip(p@G,RAD))
        p = p@F
    return p, noise


def predicted_support(est, d, q, i):
    p, noise = pull_noise(q,i)
    return est.support(p[:2])+p[2:]@d+noise


def nominal(z, plan):
    states = [z]
    for v in plan:
        states.append(A@states[-1]+v)
    return states


def control_rows(z, plan):
    states = nominal(z,plan)
    for i in range(N+1):
        for axis in range(2):
            for sign in (-1,1):
                yield sign*TX[axis],i,Q(2)-sign*states[i][axis]
    for i in range(N):
        for axis in range(2):
            for sign in (-1,1):
                yield sign*TU[axis],i,Q(2,5)-sign*plan[i][axis]
    for axis in range(4):
        for sign in (-1,1):
            yield sign*eye(4)[axis],N,RR[axis]


def margins(z, d, est, plan):
    result = [b-predicted_support(est,d,q,i) for q,i,b in control_rows(z,plan)]
    result += [Q(1,5)-sign*x for x in nominal(z,plan)[-1] for sign in (-1,1)]
    return result


def objective(z, plan):
    states = nominal(z,plan)
    return sum(10*(s@s) for s in states[:-1])+states[-1]@P@states[-1]+sum(v@v for v in plan)


def optimize(z,d,est,fallback):
    # The margin map is affine in the nominal controls; the support cache is fixed.
    zero = zeros(N,2)
    bq = np.array(margins(z,d,est,zero),dtype=object)
    columns = []
    for j in range(2*N):
        unit = zero.copy()
        unit.flat[j] = Q(1)
        columns.append(np.array(margins(z,d,est,unit),dtype=object)-bq)
    matrix = np.array(columns,dtype=float).T
    b = np.array(bq,dtype=float)
    variable = np.any(matrix != 0,axis=1)
    zf = np.array(z,dtype=float)
    af = np.array(A,dtype=float)

    def fun(flat):
        vs = flat.reshape(N,2)
        state = zf.copy()
        val = 10*state@state
        for v in vs:
            state = af@state+v
            val += 10*state@state+v@v
        val += 2*state@state
        return val

    proposal = minimize(fun,np.array(fallback,dtype=float).ravel(),method='SLSQP',
        constraints=[LinearConstraint(matrix[variable],1e-6-b[variable],np.inf)],
        options={'ftol':1e-10,'maxiter':100})
    est.last_qp_reason = 'nonfinite_proposal'
    if np.all(np.isfinite(proposal.x)):
        plan = np.array([Q(round(float(v)*10**8),10**8) for v in proposal.x],
                        dtype=object).reshape(N,2)
        # Safety and objective acceptance do not depend on the solver success flag.
        if min(margins(z,d,est,plan)) < 0:
            est.last_qp_reason = 'failed_exact_constraint_check'
        elif objective(z,plan) >= objective(z,fallback):
            est.last_qp_reason = 'no_strict_objective_improvement'
        else:
            est.last_qp_reason = 'accepted'
            return plan, True
    return fallback, False


def shifted(z,plan):
    states = nominal(z,plan)
    return np.vstack((plan[1:], K@states[-1]))


def candidate_caps(z,d,plan):
    # Valid only after shift/append from the previously verified feasible plan.
    return [(p[:2], b-noise-p[2:]@d)
            for q,i,b in control_rows(z,plan)
            for p,noise in [pull_noise(q,i)]]


def template(cz,caps,r,missing=False):
    # Measurement equation gives e+ = r/2 - nu, hence this box contains P.
    center = r/2
    width = I*Q(1,50)
    rows = {}
    compression_lp_count = 0
    for p,b in caps:
        key,scale = canonical(p)
        if not any(key):
            assert b >= 0
            continue
        bound = b/scale
        if not missing:
            upper,_ = cz.support_certificate(key)
            compression_lp_count += bool(len(cz.b))
            bound = min(bound,upper)
        rows[key] = min(rows.get(key,bound),bound)
    # Exact halfspace-to-CZ conversion using bounded slack, chapter 15.
    m = len(rows)
    eq = zeros(m,2+m)
    rhs = []
    for j,(key,bound) in enumerate(rows.items()):
        p = np.array(key,dtype=object)
        slack = bound-p@center+sum(abs(x) for x in p@width)
        assert slack >= 0, 'A valid nonempty posterior must intersect every cap.'
        eq[j,:2] = p@width
        eq[j,2+j] = slack/2
        rhs.append(bound-p@center-slack/2)
    result = CZ(center,np.hstack((width,zeros(2,m))),eq,np.array(rhs,dtype=object))
    estimator = Estimator(result,list(rows.items()))
    estimator.compression_lp_count = compression_lp_count
    return estimator


def initial():
    z = np.array([Q(4,5),-Q(2,5)],dtype=object)
    d = np.array([Q(0),Q(0)],dtype=object)
    est = Estimator(CZ(d.copy(),I*Q(1,10)))
    state = z.copy()
    plan = []
    for _ in range(N):
        plan.append(K@state)
        state = AC@state
    return z,d,est,np.array(plan,dtype=object)


def terminal_check():
    image = np.abs(F)@RR+np.abs(G)@RAD
    decrease = P-AC.T@P@AC-10*I-K.T@K
    return bool(all(image <= RR) and all(np.abs(AC)@np.full(2,Q(1,5)) <= Q(1,5))
                and all(Q(1,5)+np.abs(TX)@RR <= Q(2))
                and all(Q(1,10)+np.abs(TU)@RR <= Q(2,5))
                and np.array_equal(decrease,I*Q(19,100)))


def replay(mode,steps=32,phase=0):
    assert mode in ('full_cz','template','template_missing')
    assert terminal_check()
    z,d,est,plan = initial()
    x = z+np.array([Q(1,10),-Q(1,10)],dtype=object)
    hat = z.copy()
    records=[]
    total_cost=Q(0)
    shift_rejections=violations=accepted=0
    initial_error_norm=max(abs(np.concatenate((x-hat,d)))/RR)
    started=time.perf_counter()
    for t in range(steps):
        tick=time.perf_counter()
        check=min(margins(z,d,est,plan))
        shift_rejections += check < 0
        assert check >= 0, ('shift failed',mode,t,float(check))
        before=objective(z,plan)
        plan,ok=optimize(z,d,est,plan)
        accepted += ok
        after=objective(z,plan)
        u=plan[0]+K@d
        physical=min([Q(2)-abs(a) for a in x]+[Q(2,5)-abs(a) for a in u])
        violations += physical < 0
        assert physical >= 0
        total_cost += 10*(x@x)+u@u
        w=np.array([Q(1 if (t+phase)%3 else -1,100),
                    Q(1 if (t+phase)%4 < 2 else -1,100)],dtype=object)
        nu=np.array([Q(1 if (t+phase)%5 < 2 else -1,50),
                     Q(1 if (t+phase)%7 < 3 else -1,50)],dtype=object)
        xnew=A@x+u+w
        pred=A@hat+u
        r=xnew+nu-pred
        hatnew=pred+r/2
        znew=A@z+plan[0]
        dnew=hatnew-znew
        fallback=shifted(z,plan)
        decrease_slack=after-10*(z@z)-plan[0]@plan[0]-objective(znew,fallback)
        assert decrease_slack >= 0
        prior=est.cz.predict(A,I*Q(1,100))
        post=prior.observe([0,1],r,[Q(1,50)]*2).recenter(r/2)
        caps=candidate_caps(znew,dnew,fallback)
        truth=xnew-hatnew
        joint_norm=max(abs(np.concatenate((truth,dnew)))/RR)
        iss_bound=Q(3,4)**(t+1)*initial_error_norm+Q(3,5)*(1-Q(3,4)**(t+1))
        assert joint_norm <= iss_bound
        assert all(np.array(p,dtype=object)@truth <= b for p,b in caps)
        if mode=='full_cz':
            new_est=Estimator(post,caps)
        else:
            new_est=template(post,caps,r,missing=mode=='template_missing')
        # Check every represented template row and its containing measurement box.
        assert all(np.array(p,dtype=object)@truth <= b for p,b in new_est.caps.items())
        assert all(abs(truth-r/2) <= Q(1,50))
        records.append({'step':t,'generators':est.cz.g.shape[1],
            'equalities':len(est.cz.b),'control_support_lp_calls':est.lp_count,
            'compression_support_lp_calls':new_est.compression_lp_count,
            'seconds':time.perf_counter()-tick,'accepted_qp':bool(ok),
            'qp_decision':est.last_qp_reason,
            'objective_improvement':float(before-after),
            'terminal_decrease_slack':float(decrease_slack),
            'joint_error_weighted_norm':float(joint_norm),'iss_bound':float(iss_bound),
            'physical_margin':float(physical),'certificate_margin':float(min(margins(z,d,est,plan)))})
        x,hat,z,d,est,plan=xnew,hatnew,znew,dnew,new_est,fallback
    assert min(margins(z,d,est,plan)) >= 0
    violations += any(abs(v)>Q(2) for v in x)
    durations=[r['seconds'] for r in records]
    return {'mode':mode,'phase':phase,'steps':steps,'violations':int(violations),
        'shift_rejections':int(shift_rejections),'accepted_qp':int(accepted),
        'fallback_count':steps-int(accepted),'realized_cost':float(total_cost),
        'wall_seconds':time.perf_counter()-started,'median_step_seconds':float(np.median(durations)),
        'max_step_seconds':max(durations),'max_generators':max(r['generators'] for r in records),
        'max_equalities':max(r['equalities'] for r in records),
        'total_support_lp_calls':sum(r['control_support_lp_calls']+r['compression_support_lp_calls'] for r in records)+est.lp_count,
        'final_certificate_lp_calls':est.lp_count,
        'final_generators':est.cz.g.shape[1],'final_equalities':len(est.cz.b),'records':records}


def run(steps=32):
    return {'scope':'2-state LTI, 4D joint error; exact rational certificate verification; not quadrotor',
        'steps_per_run':steps,'terminal_verified':terminal_check(),
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'cz_dependency_sha256':hashlib.sha256((ROOT/'verification/check_constrained_zonotope.py').read_bytes()).hexdigest(),
        'runs':[replay(mode,steps,phase) for phase in (0,3)
                for mode in ('full_cz','template','template_missing')]}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--steps',type=int,default=32)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result=run(args.steps)
    payload=json.dumps(result,indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(payload)
    print(json.dumps([{k:v for k,v in r.items() if k!='records'} for r in result['runs']],indent=2))
