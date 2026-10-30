#!/usr/bin/env python3
"""Exact rational conditional SMF on frozen four-state lateral/attitude proxy.

Use exact constrained-zonotope equality updates (Scott et al., 2016),
exact interval-box outer bounds, and separately labelled floating LP supports.
This is NOT an MPC controller or a terminal/recursive-feasibility certificate.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZERO = F(0)


def load(root=ROOT):
    d = json.loads((root/'configs/planar_baseline.json').read_text(), parse_float=F)
    assert d['state_order'] == ['px','pz','vx','vz','phi','omega']
    assert d['sensing']['always_observed_indices'] == [4,5]
    assert d['sensing']['position_indices'] == [0,1]
    assert d['sensing']['position_period_ticks'] == 5
    assert d['sensing']['max_consecutive_missed_packets'] == 2
    assert d['mpc']['ancillary_rci_contract']['disturbance_graph']['physical_residual_halfwidth']['r_x'] == '47/25 + (243/16000) * actual_thrust'
    c = d['initial_set']; s = d['sensing']['observed_noise_halfwidth']
    return dict(h=d['plant']['dt_s'], j=d['plant']['inertia_kg_m2'],
                tmin=d['domain']['input_lower'][0],tmax=d['domain']['input_upper'][0],
                center=tuple(c['center'][i] for i in (0,2,4,5)),
                widths=tuple(c['halfwidth'][i] for i in (0,2,4,5)),
                noise={0:s['px'],2:s['phi'],3:s['omega']},
                hard=tuple(d['domain']['state_upper'][i] for i in (0,2,4,5)))


def radius(t):
    return F(47,25)+F(243,16000)*t


def dyn(x,t,tau,h,j):
    p,v,phi,omega=x
    return (p+h*v, v-h*t*phi, phi+h*omega, omega+h*tau/j)


def box_predict(box,t,tau,c):
    mid,rad=box
    nxt=dyn(mid,t,tau,c['h'],c['j'])
    p,v,phi,omega=rad
    h=c['h']
    return nxt,(p+h*v, v+h*t*phi+h*radius(t), phi+h*omega, omega)


def box_observe(box,i,y,noise):
    mid,rad=box
    lo=max(mid[i]-rad[i],y-noise)
    hi=min(mid[i]+rad[i],y+noise)
    if lo>hi: raise ValueError('inconsistent observation for box')
    m=list(mid); r=list(rad)
    m[i]=(lo+hi)/2; r[i]=(hi-lo)/2
    return tuple(m),tuple(r)


def contains(box,x):
    m,r=box
    return all(abs(x[i]-m[i])<=r[i] for i in range(4))


def pair_floor(n,t,c):
    h=c['h'];p0,v0=c['widths'][:2]
    return p0+n*h*v0+h*h*radius(t)*n*(n-1)/2


def cz_initial(c):
    center=c['center']; widths=c['widths']
    generators=tuple(tuple(widths[i] if j==i else ZERO for j in range(4)) for i in range(4))
    return center,generators,(),()


def cz_predict(cz,t,tau,c):
    center,gens,rows,rhs=cz
    center=dyn(center,t,tau,c['h'],c['j'])
    gens=tuple(dyn(g,t,ZERO,c['h'],c['j']) for g in gens)
    gens=gens+((ZERO,c['h']*radius(t),ZERO,ZERO),)
    rows=tuple(row+(ZERO,) for row in rows)
    return center,gens,rows,rhs


def cz_observe(cz,i,y,noise):
    """Exact constrained-zonotope intersection with |x_i-y|<=noise.
    Introduces virtual measurement-noise generator with zero state effect,
    and equality e_i'(center+G*eps)+noise*nu=y, |nu|<=1.
    """
    center,gens,rows,rhs=cz
    gens=gens+((ZERO,)*4,)
    rows=tuple(row+(ZERO,) for row in rows)
    rows=rows+(tuple(g[i] for g in gens[:-1])+(noise,),)
    rhs=rhs+(y-center[i],)
    return center,gens,rows,rhs


def cz_witness(cz,coefficients,x):
    center,gens,rows,rhs=cz
    assert len(coefficients)==len(gens)
    assert all(abs(e)<=1 for e in coefficients)
    reconstructed=tuple(center[i]+sum(g[i]*e for g,e in zip(gens,coefficients)) for i in range(4))
    return reconstructed==x and all(sum(a*e for a,e in zip(row,coefficients))==b for row,b in zip(rows,rhs))


def cz_support_numeric(cz,coordinate):
    """Floating LP diagnostic only, never a certified outer support bound."""
    import numpy as np
    from scipy.optimize import linprog
    center,gens,rows,rhs=cz
    coeff=np.asarray([float(g[coordinate]) for g in gens])
    ae=np.asarray([[float(x) for x in row] for row in rows]) if rows else None
    be=np.asarray([float(x) for x in rhs]) if rhs else None
    vals=[]
    for sign in (1,-1):
        res=linprog(sign*coeff,A_eq=ae,b_eq=be,bounds=[(-1,1)]*len(gens),method='highs')
        if not res.success:raise RuntimeError('CZ numeric LP failed: '+res.message)
        vals.append(float(center[coordinate])-sign*res.fun)
    return (vals[1],vals[0])


def velocity_floor(n,t,c):
    return c['widths'][1]+n*c['h']*radius(t)


def certified_return_velocity_bound(n,t,c):
    """Exact post-return |v_n| upper for y_p(0)=y_p(n)=0,
    y_phi(k)=0 for k=0,...,n-1, no vx measurement.
    Eliminate v0 from p_n-p0 to retain the p/v correlation:
    v_n=(p_n-p0)/(n*h)+(h/n)*sum((i+1)*a_i),
    a_i=-t*phi_i+r_i, |a_i|<=t*noise_phi+radius(t).
    Intersect this valid bound with the interval-box prior bound.
    """
    h=c['h'];np=c['noise'][0];nphi=c['noise'][2]
    derived=2*np/(n*h)+h*F(n+1,2)*(t*nphi+radius(t))
    return derived


def run_case(c,t,n,return_packet=True):
    """Frozen thrust, zero torque; zero observations, residual and true state.
    At tick 0 position/attitude/rate are observed; at 1..n-1 only attitude/rate.
    Tick n has a position return after the pre-return support audit.
    """
    assert t in (c['tmin'],c['tmax']) and n in (5,10,15)
    box=(c['center'],c['widths'])
    cz=cz_initial(c)
    x=(ZERO,)*4
    eps=[ZERO]*4
    for i in (0,2,3):
        box=box_observe(box,i,ZERO,c['noise'][i])
        cz=cz_observe(cz,i,ZERO,c['noise'][i]);eps.append(ZERO)
    assert cz_witness(cz,eps,x)
    for k in range(1,n+1):
        x=dyn(x,t,ZERO,c['h'],c['j'])
        box=box_predict(box,t,ZERO,c)
        cz=cz_predict(cz,t,ZERO,c);eps.append(ZERO)
        for i in (2,3):
            box=box_observe(box,i,ZERO,c['noise'][i])
            cz=cz_observe(cz,i,ZERO,c['noise'][i]);eps.append(ZERO)
        assert contains(box,x) and cz_witness(cz,eps,x)
    pre_box=box
    pre_cz=cz
    pf=pair_floor(n,t,c);vf=velocity_floor(n,t,c)
    assert pf<=box[1][0] and vf<=box[1][1]
    lp_p=cz_support_numeric(cz,0)
    lp_v=cz_support_numeric(cz,1)
    assert lp_p[0]<=-float(pf)+1e-7 and lp_p[1]>=float(pf)-1e-7
    assert lp_v[0]<=-float(vf)+1e-7 and lp_v[1]>=float(vf)-1e-7
    if return_packet:
        box=box_observe(box,0,ZERO,c['noise'][0])
        cz=cz_observe(cz,0,ZERO,c['noise'][0]);eps.append(ZERO)
        assert cz_witness(cz,eps,x)
    post_v=cz_support_numeric(cz,1)
    certified_v=min(pre_box[1][1],certified_return_velocity_bound(n,t,c)) if return_packet else pre_box[1][1]
    assert post_v[1]<=float(certified_v)+1e-7
    return dict(gap_ticks=n,thrust='low' if t==c['tmin'] else 'high',
                position_return=return_packet,
                exact_indistinguishable_position_floor=str(pf),
                exact_indistinguishable_velocity_floor=str(vf),
                certified_box_position_outer_halfwidth=str(pre_box[1][0]),
                certified_box_velocity_outer_halfwidth=str(pre_box[1][1]),
                numeric_CZ_position_lower=lp_p[0],numeric_CZ_position_upper=lp_p[1],
                numeric_CZ_velocity_lower=lp_v[0],numeric_CZ_velocity_upper=lp_v[1],
                numeric_CZ_constraints=len(pre_cz[2]),numeric_CZ_generators=len(pre_cz[1]),
                post_return_box_position_halfwidth=str(box[1][0]),
                post_return_box_velocity_halfwidth=str(box[1][1]),
                certified_post_return_velocity_outer_halfwidth=str(certified_v),
                certified_velocity_reduction_fraction=str(1-certified_v/pre_box[1][1]),
                post_return_numeric_CZ_velocity_lower=post_v[0],
                post_return_numeric_CZ_velocity_upper=post_v[1],
                global_position_hard_bound=str(c['hard'][0]),
                global_velocity_hard_bound=str(c['hard'][1]),
                illustrative_velocity_budget=str(F(1,4)),
                velocity_floor_exceeds_illustrative_budget=vf>F(1,4))


def run(root=ROOT):
    c=load(root)
    rows=[run_case(c,t,n) for n in (5,10,15) for t in (c['tmin'],c['tmax'])]
    return dict(status='PASS',evidence='EXACT_RATIONAL_CZ_REPRESENTATION_AND_BOX_OUTER;NUMERIC_LP_SUPPORT_ONLY',
                model='frozen four-state lateral-attitude proxy; known fixed thrust, zero torque',
                sensing='phi/omega each tick; px at tick 0 and at tick 5/10/15 return',
                rows=rows,gate_A='blocked',
                caveats=['CZ equality update is exact but LP supports are floating diagnostics, not certified bounds',
                         'Box supports and indistinguishable pair floors are exact fractions',
                         'Nominal ±0.25 m/s is not a certified tube-error budget or terminal set',
                         'Zero-observation history is one admissible history; no controller or terminal invariant set synthesized'])


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=ROOT)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args();s=json.dumps(run(args.root),ensure_ascii=False,indent=2)+'\n'
    if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(s)
    else:print(s,end='')

if __name__=='__main__':main()
