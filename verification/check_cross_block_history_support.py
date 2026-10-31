"""Run217: exact-rational cross-block history strips and one-strip support dual.

A necessary 4D history constraint is derived by eliminating historical
attitudes using *logged applied torques* and exact Euler attitude dynamics.
It is not a full constrained-zonotope posterior. The one-strip Lagrangian
support bound is safe, and exact for one strip intersecting a product of
nonempty compact convex polygons. Several strips are audited separately:
their minimum is an OUTER support bound, not the joint optimum.
"""
from fractions import Fraction as Q
from itertools import combinations

Z=Q(0)
H=J=Q(1,50)
SIGMA_P=Q(1,50)


def residual_radius(t):
    return Q(47,25)+Q(243,16000)*Q(t)


def cross_block_packet_strip(packet_tick, packet_position, end_tick,
                             thrusts, applied_torques,
                             h=H, inertia=J, position_noise=SIGMA_P,
                             radius_fn=residual_radius):
    """Return (c,center,radius) for |c @ (p,v,phi,omega)-center|<=radius.

    Model: p+=p+h*v; v+=v+h*(-T*phi+r); phi+=phi+h*omega;
    omega+=omega+h/J*u. Past thrust and torque MUST be known, applied values.
    Only position packet at tick a is required. Assumes exact attitude
    double-integrator dynamics and |r_i|<=radius_fn(T_i).
    """
    a,k=packet_tick,end_tick
    if not isinstance(a,int) or not isinstance(k,int) or not 0<=a<k:
        raise ValueError('invalid packet/end tick')
    if not (h>0 and inertia>0 and position_noise>=0):
        raise ValueError('invalid model/noise bounds')
    if any(i not in thrusts or i not in applied_torques for i in range(a,k)):
        raise ValueError('missing applied causal history')
    n=k-a
    A=B=D=R=Z
    # Compute phi_i=phi_k-(k-i)*h*omega_k+C_i exactly.
    for i in range(a,k):
        t=Q(thrusts[i]); w=i-a+1
        if t<0:raise ValueError('negative thrust')
        ci=h*h/inertia*sum(((j-i+1)*Q(applied_torques[j])
                             for j in range(i,k)),Z)
        A+=h*h*w*t
        B+=h*h*h*w*(k-i)*t
        D+=h*h*w*t*ci
        R+=h*h*w*Q(radius_fn(t))
    return ((Q(1),-n*h,-A,B),Q(packet_position)+D,
            Q(position_noise)+R)


def _dot(a,b):
    return sum((Q(x)*Q(y) for x,y in zip(a,b)),Z)


def strip_residual(state,strip):
    c,center,radius=strip
    return abs(_dot(c,state)-center)-radius


def product_support(pv,ao,q):
    if not pv or not ao or len(q)!=4:raise ValueError('empty polygon or wrong direction')
    return max(_dot(q[:2],v) for v in pv)+max(_dot(q[2:],v) for v in ao)


def one_strip_dual(pv,ao,direction,strip):
    """Exact one-strip support via scalar LP dual, no numerical optimizer.

    min_lam h_P(q-lam*c)+lam*center+abs(lam)*radius.
    Every breakpoint of the piecewise-linear convex objective comes from a
    crossing of vertex affine functions in one polygon, or lam=0. Requires
    feasible intersection for finite optimum; caller must verify nonempty.
    """
    c,center,radius=strip
    if len(c)!=4 or len(direction)!=4 or radius<0:
        raise ValueError('bad strip/direction')
    candidates={Z}
    for poly,qpart,cpart in ((pv,direction[:2],c[:2]),(ao,direction[2:],c[2:])):
        lines=[(_dot(qpart,v),-_dot(cpart,v)) for v in poly]
        for (a,b),(d,e) in combinations(lines,2):
            if b!=e:candidates.add((d-a)/(b-e))
    def bound(lam):
        qnew=tuple(Q(x)-lam*Q(y) for x,y in zip(direction,c))
        return product_support(pv,ao,qnew)+lam*center+abs(lam)*radius
    best=min(((bound(lam),lam) for lam in candidates),key=lambda x:x[0])
    return {'upper':best[0],'lambda':best[1],
            'independent_upper':product_support(pv,ao,direction),
            'candidate_count':len(candidates)}


def multiple_strip_outer_support(pv,ao,direction,strips):
    """Safe outer support using one cross-strip at a time, not joint 4D LP."""
    base=product_support(pv,ao,direction)
    best={'upper':base,'lambda':Z,'strip_index':None,'candidate_count':0}
    for i,strip in enumerate(strips):
        r=one_strip_dual(pv,ao,direction,strip)
        if r['upper']<best['upper']:
            best={'upper':r['upper'],'lambda':r['lambda'],
                  'strip_index':i,'candidate_count':r['candidate_count']}
    return best


def run_tick193():
    """Full-repository integration entry point; no future measurements.

    This computes ONLY the Run216 obstructing direction's outer support.
    It does not declare backup feasible from a single-row improvement.
    """
    import check_joint_support_backup as joint
    import check_rolling_history_support as prior
    import check_joint_history_strips as hist
    box,truth,positions,attitudes,thrusts,torques=prior.replay_to_193(return_controls=True)
    vb,_=prior.rolling_support(positions,attitudes,thrusts,192,6)
    pb=hist.position_support_three_packets(
        tuple((i,positions[i]) for i in (105,165,180)),attitudes,thrusts,192,Q(7,3))
    pv,ao=joint.history_polygons(box,positions,attitudes,thrusts,torques,192,
                                  position_bound=pb,velocity_bound=vb)
    strips=[cross_block_packet_strip(a,positions[a],192,thrusts,torques)
            for a in sorted(i for i in positions if i<192)[-6:]]
    assert all(strip_residual(truth,s)<=0 for s in strips)
    # Reproduce Run216's single row: all five future thrusts high,
    # fifth-step negative velocity hard constraint.
    seq=(joint.TMAX,)*5
    basis=[tuple(Q(int(i==j)) for i in range(4)) for j in range(4)]
    for t in seq:basis=[joint.step(v,t) for v in basis]
    direction=tuple(-basis[j][1] for j in range(4))
    old=product_support(pv,ao,direction)
    improved=multiple_strip_outer_support(pv,ao,direction,strips)
    old_ob=joint.obstruction_witness(pv,ao)
    assert old_ob['physical_step']==5 and old_ob['state_index']==1
    gain=old-improved['upper']
    return {'tick':193,'history_end_tick':192,'packets':len(strips),
            'cross_block_true_state_contained':True,
            'critical_support_gain_exact':str(gain),
            'critical_support_gain_approx':float(gain),
            'critical_support_dual_multiplier':str(improved['lambda']),
            'best_packet_index':improved['strip_index'],
            'old_slack_exact':old_ob['best_case_slack_exact'],
            'new_slack_upper_bound_exact':str(Q(old_ob['best_case_slack_exact'])+gain),
            'new_slack_upper_bound_approx':float(Q(old_ob['best_case_slack_exact'])+gain),
            'note':'single-row necessary test only; positive slack does NOT certify backup feasibility'}

if __name__=='__main__':
    import json
    print(json.dumps(run_tick193(),indent=2))
