"""Run216: exact-rational joint H-polytope support for finite causal backup.

The current posterior is OUTER-approximated by two independent 2D polygons
(p,v) and (phi,omega).  This is NOT a full 4D CZ, nor an exact SMF posterior.
The initial joint support is retained throughout five physical transitions;
there is no predicted-box reset.  Future residuals remain independent bounded
primitives.  No terminal or recursive-feasibility claim is made.
"""
from fractions import Fraction as Q
from itertools import product

Z=Q(0)
H=J=Q(1,50)
TMIN,TMAX=Q(981,200),Q(2943,200)
UMAX=Q(2,25)
LIMITS=(Q(5),Q(3),Q(9,20),Q(2))


def rad(t):
    return Q(47,25)+Q(243,16000)*Q(t)


def polygon(box2, strips=()):
    """Exact intersection of an axis-aligned rectangle and a*x+b*y<=c.

    Returns counterclockwise vertices (possibly a line/point), or empty tuple.
    Never drops constraints for numerical tolerance or approximates vertices.
    """
    (xl,xh),(yl,yh)=box2
    if xl>xh or yl>yh: return ()
    vertices=list(dict.fromkeys(((Q(xl),Q(yl)),(Q(xh),Q(yl)),
                                 (Q(xh),Q(yh)),(Q(xl),Q(yh)))))
    for a,b,c in strips:
        a,b,c=Q(a),Q(b),Q(c)
        if not vertices: return ()
        out=[]
        for prev,cur in zip(vertices[-1:]+vertices[:-1],vertices):
            fp=a*prev[0]+b*prev[1]-c
            fc=a*cur[0]+b*cur[1]-c
            if (fp<0 and fc>0) or (fp>0 and fc<0) or (fp>0 and fc==0) or (fp==0 and fc>0):
                # Only strict crossing from inside/outside is relevant; for
                # on-boundary endpoints the interpolation returns the endpoint.
                if fp!=fc:
                    ratio=fp/(fp-fc)
                    out.append((prev[0]+ratio*(cur[0]-prev[0]),
                                prev[1]+ratio*(cur[1]-prev[1])))
            if fc<=0:out.append(cur)
        vertices=[]
        for v in out:
            if not vertices or v!=vertices[-1]:vertices.append(v)
        if len(vertices)>1 and vertices[0]==vertices[-1]:vertices.pop()
    return tuple(vertices)


def contains(vertices, point):
    """Exact membership in a CCW convex polygon, including degeneracies."""
    if not vertices:return False
    x,y=map(Q,point)
    if len(vertices)==1:return (x,y)==vertices[0]
    if len(vertices)==2:
        (ax,ay),(bx,by)=vertices
        return ((bx-ax)*(y-ay)-(by-ay)*(x-ax)==0 and
                min(ax,bx)<=x<=max(ax,bx) and min(ay,by)<=y<=max(ay,by))
    return all((b[0]-a[0])*(y-a[1])-(b[1]-a[1])*(x-a[0])>=0
               for a,b in zip(vertices,vertices[1:]+vertices[:1]))


def support(vertices, a, b):
    if not vertices:raise ValueError('empty joint outer polytope')
    return max(Q(a)*x+Q(b)*y for x,y in vertices)


def strip_rows(center,radius,ax,ay):
    """|ax*x+ay*y-center|<=radius as two exact halfspaces."""
    if radius<0:raise ValueError('negative uncertainty radius')
    return ((ax,ay,center+radius),(-ax,-ay,-center+radius))


def history_polygons(box,positions,attitudes,thrusts,torques,end_tick,
                     max_packets=6,position_bound=None,velocity_bound=None):
    """Causal H-outer set; every included strip is a necessary history bound.

    If an optional position/velocity support is supplied, the caller must
    establish its history consistency.  This routine checks causality and
    interval shape, not the derivation of external bounds.
    """
    from check_joint_history_strips import position_velocity_strip,attitude_rate_strip
    if end_tick<1 or max_packets<1:raise ValueError('invalid history horizon')
    pv=[]
    for a in sorted(t for t in positions if t<end_tick)[-max_packets:]:
        c,r=position_velocity_strip(a,positions[a],end_tick,attitudes,thrusts)
        pv.extend(strip_rows(c,r,Q(1),-(end_tick-a)*H))
    for bound,axis in ((position_bound,(Q(1),Z)),(velocity_bound,(Z,Q(1)))):
        if bound is not None:
            lo,hi=map(Q,bound)
            if lo>hi:raise ValueError('inconsistent external bound')
            pv.extend(((axis[0],axis[1],hi),(-axis[0],-axis[1],-lo)))
    if end_tick-1 not in attitudes or end_tick-1 not in torques:
        raise ValueError('missing last causal attitude or torque')
    c,r=attitude_rate_strip(attitudes[end_tick-1],torques[end_tick-1])
    po=polygon(box[:2],pv)
    ao=polygon(box[2:],strip_rows(c,r,Q(1),-H))
    if not po or not ao:raise ValueError('empty history outer set')
    return po,ao


def step(x,t):
    p,v,phi,omega=x
    return (p+H*v,v-H*Q(t)*phi,phi+H*omega,omega)


def clip(interval,a,d):
    lo,hi=interval
    if a>0:hi=min(hi,d/a)
    elif a<0:lo=max(lo,d/a)
    elif d<0:return Q(1),Z
    return lo,hi


def project(rows,interval):
    """Eliminate the next thrust-contingent u1 via exact Fourier-Motzkin."""
    lower={};upper={}
    for a,b,d in rows:
        if b==0:interval=clip(interval,a,d)
        else:
            slope=-a/b;intercept=d/b
            if b>0:upper[slope]=min(upper.get(slope,intercept),intercept)
            else:lower[slope]=max(lower.get(slope,intercept),intercept)
    if not lower or not upper:raise AssertionError('missing u1 actuator bounds')
    for ls,li in lower.items():
        for us,ui in upper.items():interval=clip(interval,ls-us,ui-li)
    return interval


def rows_for_future(pv,ao,thrust_sequence):
    """Signed hard constraints after each of five physical transitions.

    Current u0 at step 0, next u1 at step 1, later torques fixed zero.
    All initial-state correlations within each pair are preserved.
    """
    basis=[tuple(Q(int(i==j)) for i in range(4)) for j in range(4)]
    c0=(Z,)*4;c1=(Z,)*4;dist=[]
    rows=[]
    for k,t in enumerate(thrust_sequence):
        basis=[step(v,t) for v in basis]
        c0=step(c0,t)
        c1=step(c1,t)
        dist=[step(g,t) for g in dist]
        if k==0:c0=tuple(c0[i]+(Q(1) if i==3 else Z) for i in range(4))
        if k==1:c1=tuple(c1[i]+(Q(1) if i==3 else Z) for i in range(4))
        dist.append((Z,H,Z,Z))
        for i in range(4):
            coeff=tuple(basis[j][i] for j in range(4))
            for sign in (-1,1):
                sup=support(pv,sign*coeff[0],sign*coeff[1])+support(ao,sign*coeff[2],sign*coeff[3])
                disturbance=sum(abs(g[i])*rad(thrust_sequence[j]) for j,g in enumerate(dist))
                rows.append((sign*c0[i],sign*c1[i],LIMITS[i]-sup-disturbance))
    return rows


def joint_backup(box,t0,pv=None,ao=None):
    """Two-stage robust 5-step certificate, exact for factorized H-outer set.

    u1 is allowed to depend on next visible T1, not on future measurements.
    For fixed other thrusts, signed supports are separately convex in each
    future thrust. Checking all endpoint combinations is sufficient; affine
    interpolation of endpoint u1 gives a causal feasible response for T1.
    """
    if not TMIN<=t0<=TMAX:raise ValueError('invalid current thrust')
    if pv is None:pv=polygon(box[:2])
    if ao is None:ao=polygon(box[2:])
    if not pv or not ao:return {'feasible':False,'reason':'empty_outer_set'}
    for i in range(4):
        a=Q(1) if i%2==0 else Z
        b=Z if i%2==0 else Q(1)
        poly=pv if i<2 else ao
        if support(poly,a,b)>LIMITS[i] or support(poly,-a,-b)>LIMITS[i]:
            return {'feasible':False,'reason':'current_outer_set_outside_hard_limits'}
    interval=(-UMAX,UMAX)
    details=[]
    for t1 in (TMIN,TMAX):
        merged={(Z,Q(1)):UMAX,(Z,-Q(1)):UMAX}
        for rest in product((TMIN,TMAX),repeat=3):
            for a,b,d in rows_for_future(pv,ao,(t0,t1)+rest):
                key=(a,b);merged[key]=min(merged.get(key,d),d)
        interval=project(((a,b,d) for (a,b),d in merged.items()),interval)
        details.append({'t1':str(t1),'rows':len(merged)})
    return {'feasible':interval[0]<=interval[1],
            'reason':'admitted_finite_joint_backup' if interval[0]<=interval[1] else 'empty_finite_joint_backup',
            'lower':str(interval[0]),'upper':str(interval[1]),
            'endpoint_details':details,
            'scope':'5 physical steps; future thrust endpoints; no terminal guarantee'}


def obstruction_witness(pv,ao,t0=TMAX):
    """A single exact row that no admissible (u0,u1) can satisfy.

    Strictly negative slack d+UMAX*(|a|+|b|) is a proof of failure of
    this outer-set 5-step backup, NOT physical nonviability.  A fixed
    high-thrust continuation suffices for the negative witness.
    """
    seq=(Q(t0),TMAX,TMAX,TMAX,TMAX)
    rows=rows_for_future(pv,ao,seq)
    worst=min(enumerate(rows),key=lambda pair:pair[1][2]+UMAX*(abs(pair[1][0])+abs(pair[1][1])))
    index,(a,b,d)=worst
    slack=d+UMAX*(abs(a)+abs(b))
    return {'future_thrusts':list(map(str,seq)),
            'physical_step':index//8+1,'state_index':(index%8)//2,
            'constraint_sign':(-1,1)[index%2],
            'a_u0':str(a),'b_u1':str(b),'rhs':str(d),
            'best_case_slack_exact':str(slack),
            'best_case_slack_approx':float(slack),
            'individually_impossible':slack<0}


def integration_tick193():
    """Optional full-checkout audit; fails if Run214 dependencies unavailable."""
    import check_reachable_smf_backup_rollout as m
    import check_rolling_history_support as previous
    import check_joint_history_strips as hist
    assert (m.H,m.J,m.TMIN,m.TMAX,m.UMAX,m.LIMITS)==(H,J,TMIN,TMAX,UMAX,LIMITS)
    box,truth,positions,attitudes,thrusts,torques=previous.replay_to_193(return_controls=True)
    vbound,_=previous.rolling_support(positions,attitudes,thrusts,192,6)
    pbound=hist.position_support_three_packets(
        tuple((i,positions[i]) for i in (105,165,180)),attitudes,thrusts,192,Q(7,3))
    pv,ao=history_polygons(box,positions,attitudes,thrusts,torques,192,
                           position_bound=pbound,velocity_bound=vbound)
    assert all(a<=z<=b for (a,b),z in zip(box,truth))
    assert contains(pv,truth[:2]) and contains(ao,truth[2:])
    old=joint_backup(box,m.TMAX)
    new=joint_backup(box,m.TMAX,pv,ao)
    witness=obstruction_witness(pv,ao)
    box_witness=obstruction_witness(polygon(box[:2]),polygon(box[2:]))
    support_gain=Q(witness['rhs'])-Q(box_witness['rhs'])
    assert support_gain==Q(57617501,1440000000)
    assert witness['individually_impossible'] and witness['physical_step']==5
    assert witness['state_index']==1 and witness['constraint_sign']==-1
    return {'tick':193,'baseline':old,'joint':new,'pv_vertices':len(pv),
            'attitude_vertices':len(ao),'truth_in_joint_outer':True,
            'obstruction':witness,
            'critical_row_support_gain_exact':str(support_gain),
            'critical_row_support_gain_approx':float(support_gain),
            'caveat':'history outer polytope, not exact posterior or full CZ'}

if __name__=='__main__':
    import json
    print(json.dumps(integration_tick193(),indent=2))
