#!/usr/bin/env python3
"""Construct one explicit entirely-simple seed for the chapter-47 19-pair
orientation family and test endpoint-exact RCI feasibility inside its CC cone.

Geometry generation is numerical (HiGHS/NumPy), while all predecessor normals
and the seed offsets are stored as rational Fractions.  Therefore infeasibility
reported here excludes this audited configuration cone numerically; it is not a
global exact obstruction for the whole orientation family.
"""
from fractions import Fraction as F
from itertools import combinations
import argparse, json
import numpy as np
from scipy.optimize import linprog
import check_s3_minimal_normal_cover as base

SELECTED_POS = [
 ["1","3/50","-2943/500000","-981/25000000"],
 ["1","3/50","-8829/500000","-2943/25000000"],
 ["0","1","-2943/10000","-2943/500000"],
 ["0","1","-8829/10000","-8829/500000"],
 ["0","0","1","3/50"],
]

def build_s2():
    X=[]
    for i,w in enumerate([F(5),F(3),F('0.45'),F(2)]):
        e=[F(0)]*4; e[i]=1; X.append((tuple(e),w))
        e=[F(0)]*4; e[i]=-1; X.append((tuple(e),w))
    S1=base.reduce(X+base.pre(X))
    return base.reduce(X+base.pre(S1))

def same_dir(a,b,tol=1e-10):
    x=np.array([float(v) for v in a]); y=np.array([float(v) for v in b])
    return np.linalg.norm(x-y)<tol or np.linalg.norm(x+y)<tol

def orientation_reps(S2):
    reps=[]
    for a,_ in S2:
        if not any(same_dir(a,z) for z in reps): reps.append(a)
    for s in SELECTED_POS:
        a=tuple(F(v) for v in s)
        if not any(same_dir(a,z) for z in reps): reps.append(a)
    assert len(reps)==19
    return reps

def seed_H(reps):
    H=[]
    for k,a in enumerate(reps):
        # Rationalized Euclidean-support seed plus a deterministic 1e-4 pair perturbation.
        n=np.linalg.norm([float(v) for v in a])
        q0=F(round(n*10**8),10**8)
        q=q0*F(10000+k+1,10000)
        H += [(a,q),(tuple(-v for v in a),q)]
    return H

def enumerate_vertices(H):
    C=np.array([[float(v) for v in a] for a,_ in H]); q=np.array([float(b) for _,b in H])
    V=[]
    for ids in combinations(range(len(H)),4):
        M=C[list(ids)]
        if abs(np.linalg.det(M))<1e-10: continue
        x=np.linalg.solve(M,q[list(ids)])
        if np.all(C@x<=q+1e-8) and not any(np.linalg.norm(x-v)<1e-6 for v in V): V.append(x)
    acts=[np.where(np.abs(C@x-q)<1e-7)[0].tolist() for x in V]
    return C,q,V,acts

def facet_count(C,q):
    n=len(q); active=0
    for i in range(n):
        m=np.arange(n)!=i
        z=linprog(-C[i],A_ub=C[m],b_ub=q[m],bounds=[(None,None)]*4,method='highs')
        if z.success and -z.fun>q[i]+1e-8: active+=1
    return active

def cc_lp(H,C,acts,torque_bound):
    nq=len(H); nv=len(acts); nvar=nq+nv
    Ls=[]
    for ids in acts:
        assert len(ids)==4
        L=np.zeros((4,nq)); L[:,ids]=np.linalg.inv(C[ids,:]); Ls.append(L)
    Aub=[]; bub=[]
    # Configuration cone: C V_i q <= q for every seed vertex map.
    for L in Ls:
        CL=C@L
        for j in range(nq):
            row=np.zeros(nvar); row[:nq]=CL[j]; row[j]-=1
            Aub.append(row); bub.append(0.)
    config_rows=len(Aub)
    B=np.array([float(v) for v in base.B]); E=np.array([float(v) for v in base.E])
    # Endpoint-exact robust invariance.
    for i,L in enumerate(Ls):
        for j in range(nq):
            r=C[j]; beta=r@B
            for T in (base.TL,base.TU):
                Af=np.array([[float(v) for v in rr] for rr in base.A(T)])
                sup=abs(r@E)*float(base.d0+base.c*T)
                row=np.zeros(nvar); row[:nq]=r@Af@L; row[j]-=1; row[nq+i]=beta
                Aub.append(row); bub.append(-sup)
    config_plus_invariance_rows=len(Aub)
    # Hard-state containment at all CC vertices.
    for L in Ls:
        for k,w in enumerate([5.,3.,.45,2.]):
            for sg in (1.,-1.):
                r=np.zeros(4); r[k]=sg
                row=np.zeros(nvar); row[:nq]=r@L
                Aub.append(row); bub.append(w)
    Aeq=[]; beq=[]
    for k in range(19):
        row=np.zeros(nvar); row[2*k]=1; row[2*k+1]=-1
        Aeq.append(row); beq.append(0.)
    ub=None if torque_bound is None else torque_bound
    lb=None if torque_bound is None else -torque_bound
    bounds=[(0,None)]*nq+[(lb,ub)]*nv
    sol=linprog(np.zeros(nvar),A_ub=np.array(Aub),b_ub=np.array(bub),
                A_eq=np.array(Aeq),b_eq=np.array(beq),bounds=bounds,method='highs')
    return sol,config_rows,config_plus_invariance_rows,len(Aub),nvar

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True); args=ap.parse_args()
    S2=build_s2(); reps=orientation_reps(S2); H=seed_H(reps)
    C,q,V,acts=enumerate_vertices(H)
    active=facet_count(C,q); simple=all(len(a)==4 for a in acts)
    assert len(S2)==28 and len(H)==38 and active==38 and len(V)==160 and simple
    bounded,crows,cirows,allrows,nvar=cc_lp(H,C,acts,0.08)
    unbounded,_,_,_,_=cc_lp(H,C,acts,None)
    result={
      'status':'numerical_single_configuration_cone_exclusion',
      'S2_facets':len(S2),'orientation_pairs':19,'raw_halfspaces':38,
      'seed_active_facets':active,'seed_vertices':len(V),'seed_entirely_simple_numerical':simple,
      'variables':nvar,'configuration_inequalities':crows,
      'configuration_plus_invariance_inequalities':cirows,'total_inequalities_with_hard_state':allrows,
      'pair_offset_equalities':19,
      'bounded_torque_0p08_feasible':bool(bounded.success),
      'unbounded_vertex_torque_feasible':bool(unbounded.success),
      'conclusion':'An explicit 38-active-facet, 160-vertex entirely-simple seed configuration was found. The endpoint-exact CC-RCI LP is infeasible in this configuration cone, even when vertex torque bounds are removed.',
      'limitation':'Seed geometry and LP infeasibility use floating-point NumPy/HiGHS. This excludes only this audited configuration cone; it neither proves exact infeasibility nor excludes other configuration cones of the same 19-pair orientation family.'
    }
    open(args.output,'w').write(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    assert not bounded.success and not unbounded.success
if __name__=='__main__': main()
