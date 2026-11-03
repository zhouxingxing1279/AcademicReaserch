#!/usr/bin/env python3
"""Exact small witnesses, not a general nonlinear solver or MPC experiment."""
import argparse
import hashlib
import json
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path


def dual_upper(d, rows, rhs, multipliers, bounds):
    """Rational weak-duality bound with box support for stationarity residual."""
    d = list(map(Q,d)); rows = [list(map(Q,r)) for r in rows]
    rhs = list(map(Q,rhs)); multipliers = list(map(Q,multipliers))
    bounds = [(Q(l),Q(u)) for l,u in bounds]
    if (len(rows) != len(rhs) or len(rhs) != len(multipliers)
            or len(d) != len(bounds) or any(len(r) != len(d) for r in rows)
            or any(l > u for l,u in bounds)
            or any(v < 0 for v in multipliers)):
        raise ValueError('invalid certificate dimensions, box or multipliers')
    residual = [v-sum(lam*r[j] for lam,r in zip(multipliers,rows))
                for j,v in enumerate(d)]
    return (sum(lam*b for lam,b in zip(multipliers,rhs))
            + sum(max(v*l,v*u) for v,(l,u) in zip(residual,bounds)))


def cell_interval(l, u):
    """Exact theta projection of McCormick relaxation, q=theta*x=x+1.

    Enumerate all vertices of a known nonempty bounded 2D polygon using
    rational arithmetic. This special-case solver is not used for pruning.
    """
    l,u=Q(l),Q(u)
    if not Q(1) <= l < u <= Q(2):
        raise ValueError('cell must be a nondegenerate subinterval of [1,2]')
    # Each row is a*theta+b*x<=c; theta lies in [0,4].
    rows=[(Q(1),Q(0),Q(4)),(-Q(1),Q(0),Q(0)),
          (Q(0),Q(1),u),(Q(0),-Q(1),-l),
          (l,-Q(1),Q(1)),(u,Q(3),1+4*u),
          (-u,Q(1),-Q(1)),(-l,-Q(3),-1-4*l)]
    vertices=[]
    for (a,b,c),(d,e,f) in combinations(rows,2):
        det=a*e-b*d
        if not det:
            continue
        theta=(c*e-b*f)/det; x=(a*f-c*d)/det
        if all(aa*theta+bb*x <= cc for aa,bb,cc in rows):
            vertices.append((theta,x))
    if not vertices:
        raise RuntimeError('unexpected empty bounded polygon; no pruning allowed')
    return min(t for t,x in vertices),max(t for t,x in vertices)


def cover_interval(leaves):
    """Hull of supplied leaves ONLY; caller owns full-domain coverage."""
    values=[cell_interval(*cell) for cell in leaves]
    if not values:
        raise ValueError('empty cover')
    return min(l for l,u in values),max(u for l,u in values)


def atomic_split(leaves, index, completed_children):
    """Commit midpoint replacement only when both children are completed.

    A deterministic protocol model: no async jobs or numerical certificates
    are implemented here. The immutable old list is the interrupted fallback.
    """
    if completed_children not in (0,1,2):
        raise ValueError('expected zero, one or two completed children')
    l,u=leaves[index]; midpoint=(l+u)/2
    if completed_children < 2:
        return list(leaves)
    return leaves[:index]+[(l,midpoint),(midpoint,u)]+leaves[index+1:]


def run():
    refinements=[]
    for n in (1,2,4,8,16):
        leaves=[(1+Q(i,n),1+Q(i+1,n)) for i in range(n)]
        lo,hi=cover_interval(leaves)
        assert lo <= Q(3,2) <= Q(2) <= hi
        refinements.append({'leaves':n,'directional_extrema':2*n,
                            'interval':[str(lo),str(hi)],'width':str(hi-lo),
                            'hausdorff_error':str(max(Q(3,2)-lo,hi-2))})
    # Equal abstract cost: each task certifies two opposite support directions.
    # Both are sound disclosures for truth set [-.1,.1] x [-.5,.5].
    geometric={'halfwidths':[Q(1,10),Q(1)],'area':Q(2,5),'support_b':Q(1)}
    relevant={'halfwidths':[Q(2),Q(1,2)],'area':Q(4),'support_b':Q(1,2)}
    for task in (geometric,relevant):
        task['margin_b_le_3_over_4']=Q(3,4)-task['support_b']
    assert geometric['area'] < relevant['area']
    assert geometric['margin_b_le_3_over_4'] < 0 < relevant['margin_b_le_3_over_4']
    return {'status':'exact_scalar_relaxations_and_contract_witnesses_only',
            'safe_center_strip':['0','10/3'],'exact_marginal':['1','3'],
            'exact_joint':['3/2','2'],'uniform_cover':refinements,
            'incomplete_cover_counterexample':{'retained_cell':['1','5/4'],
                'invalid_global_interval':list(map(str,cover_interval([(Q(1),Q(5,4))]))),
                'excluded_true_theta':'3/2','true_x':'2'},
            'equal_query_count_direction_choice':{'two_queries_per_task':True,
                'volume_choice':geometric,'constraint_choice':relevant,
                'equal_wall_time_measured':False},
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}


if __name__ == '__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():
        parser.error('output must be new')
    result=run();args.output.parent.mkdir(parents=True,exist_ok=True)
    encoded=json.dumps(result,indent=2,default=str)+'\n'
    args.output.write_text(encoded);print(encoded)
