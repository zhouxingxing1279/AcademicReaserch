#!/usr/bin/env python3
"""Run203: exact three-tick hard-constraint admission, NOT terminal RCI.

Uses Run202 rational *outer* boxes at a fixed-thrust, zero-observation
history. After the packet outcome the controller sees the posterior, chooses
one torque, then applies zero torque for two ticks. Current thrust is visible;
the next two thrusts range independently over the full physical interval.
No position packet is scheduled in these three ticks for the audited modes.
"""
from __future__ import annotations
import argparse
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ZERO = Q(0)


def residual_radius(t):
    return Q(47, 25) + Q(243, 16000) * t


def contract(root=ROOT):
    c = json.loads((root/'configs/planar_baseline.json').read_text(), parse_float=Q)
    graph = c['mpc']['ancillary_rci_contract']
    assert c['state_order'] == ['px','pz','vx','vz','phi','omega']
    assert graph['disturbance_graph']['physical_residual_halfwidth']['r_x'] == '47/25 + (243/16000) * actual_thrust'
    assert c['sensing']['always_observed_indices'] == [4,5]
    assert c['sensing']['position_period_ticks'] == 5
    assert c['sensing']['max_consecutive_missed_packets'] == 2
    assert graph['mode_graph']['mode_count'] == 15
    assert graph['mode_graph']['control_precedes_successor_edge'] is True
    edges = {(int(a), int(b), s) for a,b,s in graph['mode_graph']['edges']}
    expected = {(i,i+1,'miss') for i in range(14)} | {(4,0,'success'),(9,0,'success'),(14,0,'success')}
    assert edges == expected
    return dict(h=c['plant']['dt_s'], j=c['plant']['inertia_kg_m2'],
                tmin=c['domain']['input_lower'][0], tmax=c['domain']['input_upper'][0],
                tau_max=c['domain']['input_upper'][1],
                limits=tuple(c['domain']['state_upper'][i] for i in (0,2,4,5)),
                sigma_p=c['sensing']['observed_noise_halfwidth']['px'],
                sigma_phi=c['sensing']['observed_noise_halfwidth']['phi'],
                sigma_omega=c['sensing']['observed_noise_halfwidth']['omega'],
                edges=edges)


def load_rows(root=ROOT):
    d=json.loads((root/'results/four_state_conditional_smf_20261030/checks.json').read_text())
    assert d['status']=='PASS' and len(d['rows'])==6
    return {(int(r['gap_ticks']),r['thrust']):r for r in d['rows']}


def packet_branches(n,c):
    """Packet is observed BEFORE the next decision; no clairvoyant policy."""
    before={5:4,10:9,15:14}[n]
    options=[]
    for src,dst,kind in sorted(c['edges']):
        if src==before:
            options.append((kind,dst))
    return options


def initial_box(row,kind,c):
    # Only exact rational Run202 bounds are used. Floating CZ LP is excluded.
    if kind=='success':
        rp=c['sigma_p']
        rv=Q(row['certified_post_return_velocity_outer_halfwidth'])
    elif kind=='miss':
        rp=Q(row['certified_box_position_outer_halfwidth'])
        rv=Q(row['certified_box_velocity_outer_halfwidth'])
    else: raise ValueError(kind)
    assert rp>0 and rv>0
    return (rp,rv,c['sigma_phi'],c['sigma_omega'])


def dynamics(x,t,tau,c):
    p,v,phi,omega=x;h=c['h'];j=c['j']
    return (p+h*v, v-h*t*phi, phi+h*omega, omega+h*tau/j)


def propagate(z,t,tau,c):
    """Exact generator propagation, with a new independent residual each tick."""
    center,gens=z
    nxt=dynamics(center,t,tau,c)
    gs=tuple(dynamics(g,t,ZERO,c) for g in gens)
    gs=gs+((ZERO,c['h']*residual_radius(t),ZERO,ZERO),)
    return nxt,gs


def support_abs(z):
    center,gens=z
    return tuple(abs(center[i])+sum(abs(g[i]) for g in gens) for i in range(4))


def reachable_bounds(radii,t0,tau0,c):
    """Worst coordinate |x| for ticks 1..3, all T1/T2 endpoints.

    The four-state frozen dynamics make every generator and center affine in
    each future thrust separately (phi/omega do not depend on thrust). Thus
    each coordinate support is convex in (T1,T2); maximum over the thrust
    rectangle is attained at an endpoint pair. No sampling is used.
    """
    assert abs(tau0)<=c['tau_max'] and c['tmin']<=t0<=c['tmax']
    worst=[[ZERO]*4 for _ in range(3)]
    for t1,t2 in itertools.product((c['tmin'],c['tmax']),repeat=2):
        z=((ZERO,)*4,tuple(tuple(radii[i] if j==i else ZERO for j in range(4)) for i in range(4)))
        for k,(t,tau) in enumerate(((t0,tau0),(t1,ZERO),(t2,ZERO))):
            z=propagate(z,t,tau,c)
            bounds=support_abs(z)
            for i in range(4):worst[k][i]=max(worst[k][i],bounds[i])
    return tuple(tuple(v) for v in worst)


def admitted(bounds,c,velocity_limit=None):
    limits=list(c['limits'])
    if velocity_limit is not None:limits[1]=velocity_limit
    return all(all(b<=limit for b,limit in zip(row,limits)) for row in bounds)


def closed_form_v3(radii,t0,t1,t2,tau0,c):
    """Exact v3 support for symmetric box; check against generator method."""
    _,rv,rphi,rom=radii;h=c['h'];j=c['j']
    return (rv+h*((t0+t1+t2)*rphi+h*(t1+2*t2)*rom+
                  residual_radius(t0)+residual_radius(t1)+residual_radius(t2))+
            h**3*t2*abs(tau0)/j)


def zero_torque_counterexample(c):
    """Admissible trajectory disproving perpetual zero-torque hard safety.

    Start at the origin, choose high thrust and maximal positive residual;
    position packets may report their true nonzero positions. No assumption
    of perpetual zero observations is made after the initial packet.
    """
    x=(ZERO,)*4
    for tick in range(1,200):
        x=dynamics(x,c['tmax'],ZERO,c)
        x=(x[0],x[1]+c['h']*residual_radius(c['tmax']),x[2],x[3])
        if any(abs(v)>bound for v,bound in zip(x,c['limits'])):
            return dict(first_violation_tick=tick,
                        state=[str(v) for v in x],
                        violated_coordinates=[i for i,(v,bound) in enumerate(zip(x,c['limits'])) if abs(v)>bound],
                        thrust=str(c['tmax']),torque='0',residual=str(residual_radius(c['tmax'])))
    raise AssertionError('counterexample not found within 199 ticks')


def run(root=ROOT):
    c=contract(root); rows=load_rows(root)
    grid=tuple(c['tau_max']*Q(k,2) for k in (-2,-1,0,1,2))
    data=[]
    for n in (5,10,15):
        for thrust in ('low','high'):
            t0=c['tmin'] if thrust=='low' else c['tmax']
            r=rows[(n,thrust)]
            for branch,mode in packet_branches(n,c):
                radii=initial_box(r,branch,c)
                candidates=[]
                for tau in grid:
                    bounds=reachable_bounds(radii,t0,tau,c)
                    assert bounds[2][1]>=closed_form_v3(radii,t0,c['tmax'],c['tmax'],tau,c)
                    candidates.append(dict(torque=str(tau),
                        hard_admissible=admitted(bounds,c),
                        diagnostic_v065_admissible=admitted(bounds,c,Q(13,20)),
                        v3_abs_outer=str(bounds[2][1])))
                zero=next(z for z in candidates if z['torque']=='0')
                zb=reachable_bounds(radii,t0,ZERO,c)
                data.append(dict(gap_ticks=n,thrust=thrust,packet=branch,
                    successor_mode=mode,
                    zero_torque_hard_admissible=zero['hard_admissible'],
                    zero_torque_v065_admissible=zero['diagnostic_v065_admissible'],
                    zero_torque_final_position=str(zb[2][0]),
                    zero_torque_final_velocity=str(zb[2][1]),
                    zero_torque_horizon_peaks=[str(max(b[i] for b in zb)) for i in range(4)],
                    admissible_torque_candidates=sum(x['hard_admissible'] for x in candidates)))
    return dict(status='PASS',evidence='EXACT_RATIONAL_THREE_TICK_OUTER_REACHABILITY',
        scope='four-state proxy; zero observation history; fixed historical thrust; future thrust T1/T2 arbitrary; one chosen torque then zero torque',
        hard_limits=[str(x) for x in c['limits']],
        torque_grid=[str(x) for x in grid],
        diagnostic_velocity_limit='13/20 (not an original hard or certified terminal bound)',
        rows=data,zero_torque_perpetual_counterexample=zero_torque_counterexample(c),
        gate_A='blocked',
        caveats=['Run202 rational boxes outer-bound actual posterior; joint CZ correlations discarded',
            'Endpoint exactness applies only to frozen affine thrust dependence and fixed torque sequence',
            'No position packet within next 3 ticks on audited modes',
            'The branch is observed before the next torque choice; this is not a pre-edge common-policy certificate',
            'Finite-horizon hard admissibility does not imply a backup invariant set, recursive MPC feasibility or six-state safety'])


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=ROOT)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args();s=json.dumps(run(args.root),ensure_ascii=False,indent=2)+'\n'
    if args.output:args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(s)
    else:print(s,end='')

if __name__=='__main__':main()
