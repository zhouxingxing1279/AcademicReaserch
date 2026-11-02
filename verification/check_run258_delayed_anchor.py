#!/usr/bin/env python3
"""Run258: exact-rational delayed position anchor across one missed packet.

A sound p-v projection for a specific Run254 history, not a full H-rep/CZ
filter or a recursively invariant terminal information set.
"""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

from check_run255_posterior_bridge import (
    H, J, T, R, NOISE, PULSE, LIMIT, posterior30, bridge, step,
    sin_bounds, safe,
)
from check_run256_interval_information_limit import observe
from check_run257_correlated_position_velocity import (
    acceleration_bounds, success_velocity,
)


def velocity_from_position_anchor(y, anchor, accelerations):
    """Sound projection using Euler p/v dynamics over n steps.

    v_end=(p_end-p_anchor)/(n*h) + h*sum((i+1)/n*a_i).
    Every acceleration is enclosed independently, hence this is an outer
    interval and not necessarily the exact correlated posterior.
    """
    n = len(accelerations)
    if n < 1:
        raise ValueError('positive horizon required')
    lo = ((y - NOISE['p'] - anchor[1]) / (n * H)
          + H * sum(F(i+1, n)*a[0] for i,a in enumerate(accelerations)))
    hi = ((y + NOISE['p'] - anchor[0]) / (n * H)
          + H * sum(F(i+1, n)*a[1] for i,a in enumerate(accelerations)))
    return lo, hi


def uniform_anchor_width(anchor, accelerations):
    n = len(accelerations)
    return ((anchor[1]-anchor[0]+2*NOISE['p'])/(n*H)
            + H*sum(F(i+1,n)*(hi-lo)
                    for i,(lo,hi) in enumerate(accelerations)))


def meet(a,b):
    return max(a[0],b[0]), min(a[1],b[1])


def branch_at_35(success):
    s30=posterior30()
    rows=bridge(s30,5)
    a30=acceleration_bounds(rows)
    obs={'phi':F(0),'omega':F(0)}
    if success:
        obs['p']=F(0)
    s35=observe(rows[-1],obs)
    assert s35 is not None
    if success:
        s35=dict(s35)
        s35['v']=success_velocity(F(0),rows)
        assert s35['v'][0]<=s35['v'][1]
    return s30,s35,a30


def predict_35_to_40(s35):
    rows=[dict(s35)]
    for _ in range(5):
        nxt=observe(step(rows[-1],F(0)),{'phi':F(0),'omega':F(0)})
        assert nxt is not None
        rows.append(nxt)
    return rows,acceleration_bounds(rows)


def branch_at_40(success35,success40):
    s30,s35,a30=branch_at_35(success35)
    rows,a35=predict_35_to_40(s35)
    s40=dict(rows[-1])
    if success40:
        s40=observe(s40,{'p':F(0)})
        assert s40 is not None
        s40['v']=meet(s40['v'],velocity_from_position_anchor(F(0),s30['p'],a30+a35))
        if success35:
            s40['v']=meet(s40['v'],velocity_from_position_anchor(F(0),s35['p'],a35))
        assert s40['v'][0]<=s40['v'][1]
    return s40,a30+a35


def physical_zero_witness():
    """p30=v30=phi30=omega30=0; r=0; pulse then zero torque.

    Exact rational Taylor sine enclosures; this witness has successful
    position readings y35=y40=0 and phi/omega zero at ticks35..40.
    """
    p0=p1=v0=v1=phi=omega=F(0)
    out={}
    for k in range(30,40):
        slo,shi=sin_bounds(phi)
        p0,p1,v0,v1,phi,omega=(p0+H*v0,p1+H*v1,
                              v0-H*T*shi,v1-H*T*slo,
                              phi+H*omega,
                              omega+H/J*(PULSE[k-30] if k<35 else F(0)))
        assert abs(phi)<=LIMIT['phi'] and abs(omega)<=LIMIT['omega']
        if k+1 in (35,40):
            out[str(k+1)]={'p':[str(p0),str(p1)],'phi':str(phi),'omega':str(omega)}
            assert -NOISE['p']<=p0<=p1<=NOISE['p']
            assert phi==omega==0
    return out


def verify(root=None):
    s30=posterior30()
    assert s30['p']==(-F(1,50),F(1,50))
    branches={}
    a10=None
    for b35 in (True,False):
        for b40 in (True,False):
            label=('S' if b35 else 'M')+('S' if b40 else 'M')
            s40,acc=branch_at_40(b35,b40)
            assert safe(s40)
            branches[label]={
                'tick40_velocity':[str(x) for x in s40['v']],
                'tick40_velocity_width':str(s40['v'][1]-s40['v'][0]),
                'tick40_position':[str(x) for x in s40['p']],
            }
            if b40:
                assert s40['v'][1]-s40['v'][0] <= uniform_anchor_width(s30['p'],acc)
                if a10 is None:a10=acc
                else:assert acc==a10
    width=uniform_anchor_width(s30['p'],a10)
    assert F(branches['MS']['tick40_velocity_width']) == width
    assert F(branches['SS']['tick40_velocity_width']) == width
    assert F(branches['SM']['tick40_velocity_width']) < F(branches['MM']['tick40_velocity_width'])
    assert width < F(9,10)
    assert F(branches['MM']['tick40_velocity_width']) > F(7,2)
    witness=physical_zero_witness()
    if root is not None:
        root=Path(root)
        cfg=json.loads((root/'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics']=='defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s']))==H
        assert F(str(cfg['plant']['gravity_m_s2']))==T
        assert F(str(cfg['plant']['inertia_kg_m2']))==J
        assert cfg['sensing']['position_period_ticks']==5
        assert cfg['sensing']['max_consecutive_missed_packets']==2
        assert cfg['sensing']['observed_noise_halfwidth']['px']==float(NOISE['p'])
    return {
        'run':258,
        'evidence':'EXACT_RATIONAL_DELAYED_TWO_POSITION_ANCHOR_PROJECTION',
        'start':'Run254 SSSMMS all-zero readings through tick30',
        'control':'Run255 pulse ticks30-34, zero torque ticks35-39',
        'attitude_measurements':'phi=omega=0 at ticks35..40; earlier readings consistent with Run257',
        'position_branches':'S=success zero reading, M=miss at ticks35 and40',
        'branches':branches,
        'all_nonempty_tick40_success_readings_velocity_width_upper':str(width),
        'ten_step_acceleration_bound_count':len(a10),
        'zero_reading_physical_witness':witness,
        'scope':'sound 10-step delayed p30-p40 kinematic strip for one history, no exact posterior, no complete CZ/H-rep filter or arbitrary-history terminal certificate',
        'full_posterior_recursive_filter':False,
        'terminal_information_invariance_proved':False,
        'recursive_feasibility_proved':False,
        'gate_A':'blocked',
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',type=Path)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    s=json.dumps(verify(args.root),indent=2,sort_keys=True,ensure_ascii=False)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(s)
    else:print(s,end='')


if __name__=='__main__':main()
