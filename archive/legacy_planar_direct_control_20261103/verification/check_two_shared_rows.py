"""Run220: rational-certified dual upper bound for one/two shared-history rows.

HiGHS only proposes nonnegative multipliers; final support is recomputed
with Fraction. This is an outer support bound, NOT an exact posterior or
recursive MPC certificate.
"""
from fractions import Fraction as Q

Z = Q(0)


def dot(a, b):
    if len(a) != len(b):
        raise ValueError('dimension mismatch')
    return sum((Q(x)*Q(y) for x,y in zip(a,b)), Z)


def support(pv, ao, q):
    if not pv or not ao or len(q) != 4:
        raise ValueError('invalid support input')
    return max(dot(q[:2],p) for p in pv)+max(dot(q[2:],a) for a in ao)


def exact_dual_upper(pv, ao, q, rows, multipliers):
    """h_{P intersect H}(q) <= h_P(q-Sum lambda*c)+Sum lambda*b."""
    if len(rows)!=len(multipliers) or len(q)!=4:
        raise ValueError('dimension mismatch')
    lam=tuple(Q(x) for x in multipliers)
    if any(x<0 for x in lam) or any(len(c)!=4 for c,_ in rows):
        raise ValueError('invalid row or negative multiplier')
    shifted=tuple(Q(q[j])-sum((l*Q(c[j]) for l,(c,_) in zip(lam,rows)),Z)
                  for j in range(4))
    return support(pv,ao,shifted)+sum((l*Q(rhs) for l,(_,rhs) in zip(lam,rows)),Z)


def propose_dual(pv, ao, q, rows, max_denominator=1000000):
    """Float LP for candidate multipliers, followed by exact certificate."""
    from scipy.optimize import linprog
    if not 1<=len(rows)<=2:
        raise ValueError('one or two rows required')
    m=len(rows)
    A=[]; rhs=[]
    for p in pv:
        A.append([-float(dot(c[:2],p)) for c,_ in rows]+[-1.,0.])
        rhs.append(-float(dot(q[:2],p)))
    for a in ao:
        A.append([-float(dot(c[2:],a)) for c,_ in rows]+[0.,-1.])
        rhs.append(-float(dot(q[2:],a)))
    obj=[float(v) for _,v in rows]+[1.,1.]
    res=linprog(obj,A_ub=A,b_ub=rhs,
                bounds=[(0,None)]*m+[(None,None)]*2,method='highs')
    if not res.success:
        return {'solver_success':False,'message':str(res.message),
                'multipliers':tuple(Q(0) for _ in rows),
                'certified_upper':support(pv,ao,q)}
    lam=tuple(Q(max(0.,float(v))).limit_denominator(max_denominator)
              for v in res.x[:m])
    return {'solver_success':True,'message':str(res.message),
            'multipliers':lam,
            'certified_upper':min(support(pv,ao,q),
                                  exact_dual_upper(pv,ao,q,rows,lam))}


def halfspaces(form):
    """Convert |constant+c@x|<=radius to both necessary halfspaces."""
    c,constant,radius=form
    if Q(radius)<0 or len(c)!=4:
        raise ValueError('invalid strip')
    return ((tuple(map(Q,c)),Q(radius)-Q(constant)),
            (tuple(-Q(v) for v in c),Q(radius)+Q(constant)))


def audit_tick193():
    """Optional actual full-checkout replay using ONLY causal observations."""
    import check_rolling_history_support as prior
    import check_joint_history_strips as hist
    import check_joint_support_backup as joint
    import check_shared_disturbance_support as shared
    box,truth,positions,attitudes,thrusts,torques=prior.replay_to_193(return_controls=True)
    vb,_=prior.rolling_support(positions,attitudes,thrusts,192,6)
    pb=hist.position_support_three_packets(
        tuple((i,positions[i]) for i in (105,165,180)),
        attitudes,thrusts,192,Q(7,3))
    pv,ao=joint.history_polygons(box,positions,attitudes,thrusts,torques,192,
                                 position_bound=pb,velocity_bound=vb)
    q=(Z,Q(-1),Q(2943,2000),Q(2943,50000))
    baseline=support(pv,ao,q)
    weights=(
        {135:1,165:-6,180:5},
        {105:1,150:-5,180:4},
        {120:1,165:-3,180:2},
        {135:1,150:-3,180:2},
        {120:1,150:-2,180:1},
        {135:1,150:-2,165:1},
        {150:1,165:-2,180:1},
    )
    rows=[]
    for w in weights:
        if any(a not in positions for a in w):
            raise AssertionError('missing causal packet')
        form=shared.shared_packet_form(w,positions,thrusts,torques,192)
        for row in halfspaces(form):
            if dot(row[0],truth)>row[1]:
                raise AssertionError('true state excluded by historical row')
            rows.append(row)
    old_cert=shared.certify_direction(
        pv,ao,q,shared.shared_packet_form(weights[0],positions,thrusts,torques,192),truth)
    if not old_cert['all_maximizers_excluded']:
        raise AssertionError('Run219 certificate changed')
    primary=(old_cert['signed_row'],old_cert['signed_rhs'])
    single=propose_dual(pv,ao,q,(primary,))
    one_upper=min(single['certified_upper'],old_cert['new_support_upper'])
    best={'upper':one_upper,'second_index':None,'lambda':[]}
    attempts=0;failures=0
    for i,row in enumerate(rows[2:],start=2):
        attempts+=1
        sol=propose_dual(pv,ao,q,(primary,row))
        if not sol['solver_success']:
            failures+=1
        if sol['certified_upper']<best['upper']:
            best={'upper':sol['certified_upper'],'second_index':i,
                  'lambda':list(map(str,sol['multipliers']))}
    obstruction=joint.obstruction_witness(pv,ao)
    # This is a LOWER bound on the refined slack. Negative is INCONCLUSIVE.
    slack_lower=Q(obstruction['best_case_slack_exact'])+baseline-best['upper']
    return {'tick':193,'original_support_exact':str(baseline),
            'one_row_support_upper_exact':str(one_upper),
            'two_row_support_upper_exact':str(best['upper']),
            'extra_certified_gain_exact':str(one_upper-best['upper']),
            'best_second_row_index':best['second_index'],
            'best_multipliers':best['lambda'],
            'certified_slack_lower_bound_exact':str(slack_lower),
            'certified_slack_lower_bound_approx':float(slack_lower),
            'candidate_rows_checked':attempts,'solver_failures':failures,
            'truth_contained':True,
            'interpretation':'Negative slack LOWER bound is inconclusive; positive clears only this single row.'}


if __name__=='__main__':
    import json
    print(json.dumps(audit_tick193(),indent=2))
