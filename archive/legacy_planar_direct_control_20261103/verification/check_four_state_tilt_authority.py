#!/usr/bin/env python3
"""Run245: exact rational, finite-horizon shared tilt authority and SMF gate.

Model: frozen four-state explicit Euler, fixed thrust T=9.81, residual
r_x in [-R,R], uncertain initial four-state box. The open-loop torque
sequence is causal for every legal success/miss history, but is NOT an
infinite-horizon backup, MPC, or terminal invariant controller.

All formal comparisons use fractions and alternating Taylor bounds for sin.
Float simulation is explicitly a sanity check only.
"""
from __future__ import annotations
import argparse
import json
import math
from fractions import Fraction as F
from pathlib import Path

H=J=F(1,50)
T=F(981,100)
R=F(47,25)+F(243,16000)*T
TAU_MAX=F(2,25)
P_MAX=F(5)
V_MAX=F(3)
PHI_MAX=F(45,100)
OMEGA_MAX=F(2)
POSITION_NOISE=F(1,50)
PHI_NOISE=F(1,200)
OMEGA_NOISE=F(1,100)
PACKET_PERIOD=5
MAX_MISSES=2
RISE_TICKS=12
FALL_TICKS=12
HOLD_TICKS=6
HORIZON=RISE_TICKS+FALL_TICKS+HOLD_TICKS
TORQUES=(TAU_MAX,)*RISE_TICKS+(-TAU_MAX,)*FALL_TICKS+(F(0),)*HOLD_TICKS
INIT={'p':(F(-1,50),F(1,50)),
      'v':(F(-1,10),F(1,10)),
      'phi':(F(-1,200),F(1,200)),
      'omega':(F(-1,100),F(1,100))}


def sin_bounds(x):
    """Sound rational [lower,upper] for sin(x), |x|<=0.45."""
    assert abs(x)<=PHI_MAX
    if x<0:
        lo,hi=sin_bounds(-x)
        return -hi,-lo
    low=x-x**3/F(6)
    high=low+x**5/F(120)
    assert low<=high
    return low,high


def interval_sin(l,u):
    """Monotone sine on [-0.45,0.45]."""
    assert l<=u and -PHI_MAX<=l<=u<=PHI_MAX
    return sin_bounds(l)[0],sin_bounds(u)[1]


def step_interval(state,tau):
    """Conservative independent-interval propagation with correct Euler order."""
    p,v,phi,omega=(state[k] for k in ('p','v','phi','omega'))
    sl,su=interval_sin(*phi)
    next_p=(p[0]+H*v[0],p[1]+H*v[1])
    next_v=(v[0]+H*(-T*su-R),v[1]+H*(-T*sl+R))
    next_phi=(phi[0]+H*omega[0],phi[1]+H*omega[1])
    next_omega=(omega[0]+H/J*tau,omega[1]+H/J*tau)
    return dict(p=next_p,v=next_v,phi=next_phi,omega=next_omega)


def envelope():
    state=dict(INIT)
    rows=[{'tick':0,'bounds':state}]
    for k,tau in enumerate(TORQUES,1):
        state=step_interval(state,tau)
        rows.append({'tick':k,'bounds':state})
    return rows


def intersect(a,b):
    lo=max(a[0],b[0]);hi=min(a[1],b[1])
    if lo>hi: return None
    return lo,hi


def measurement_update(state,observations):
    """Sound interval SMF update: no measurement -> no strip.

    Each observed value is compatible with a bounded-error sensor.
    Does not assert nonemptiness for arbitrary incompatible observations.
    """
    out=dict(state)
    for key,(value,noise) in observations.items():
        z=intersect(out[key],(value-noise,value+noise))
        if z is None:return None
        out[key]=z
    return out


def packet_paths():
    """Enumerate legal finite success/miss words, first packet at tick5.

    For every 5-tick opportunity the next symbol is unknown at control time.
    Consecutive misses may not exceed two. The open-loop action is identical
    across all words; enumeration is a combinatorial cross-check only.
    """
    words=[('',0)]
    for _ in range(HORIZON//PACKET_PERIOD):
        new=[]
        for word,misses in words:
            new.append((word+'S',0))
            if misses<MAX_MISSES:new.append((word+'M',misses+1))
        words=new
    return [w for w,_ in words]


def float_sanity(word='SMMSSS'):
    """Single numeric trajectory and noisy SMF replay; not a proof."""
    assert word in packet_paths()
    p,v,phi,omega=0.01,-0.06,0.002,-0.004
    state=dict(INIT)
    max_gap=0
    for k,tau in enumerate(TORQUES,1):
        r=float(R)*(1 if k%3 else -1)
        p,v,phi,omega=(p+float(H)*v,
                         v+float(H)*(-float(T)*math.sin(phi)+r),
                         phi+float(H)*omega,
                         omega+float(H/J*tau))
        state=step_interval(state,tau)
        observations={'phi':(F(str(phi))+PHI_NOISE/2,PHI_NOISE),
                      'omega':(F(str(omega))-OMEGA_NOISE/2,OMEGA_NOISE)}
        if k%PACKET_PERIOD==0 and word[k//PACKET_PERIOD-1]=='S':
            observations['p']=(F(str(p))+POSITION_NOISE/2,POSITION_NOISE)
        state=measurement_update(state,observations)
        assert state is not None
        for key,val in [('p',p),('v',v),('phi',phi),('omega',omega)]:
            lo,hi=state[key]
            assert float(lo)-1e-10<=val<=float(hi)+1e-10,(k,key,val,lo,hi)
            max_gap=max(max_gap,float(hi-lo))
    return {'pattern':word,'final_truth':[p,v,phi,omega],
            'final_smf_bounds':{k:[float(x) for x in bounds] for k,bounds in state.items()},
            'maximum_interval_width_sanity':max_gap}


def verify(root=None):
    if root is not None:
        cfg=json.loads((Path(root)/'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics']=='defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s']))==H
        assert F(str(cfg['plant']['inertia_kg_m2']))==J
        assert F(str(cfg['plant']['gravity_m_s2']))==T
        assert cfg['sensing']['position_period_ticks']==PACKET_PERIOD
        assert cfg['sensing']['max_consecutive_missed_packets']==MAX_MISSES
        assert cfg['sensing']['always_observed_indices']==[4,5]
        assert cfg['sensing']['position_indices']==[0,1]
        assert F(str(cfg['sensing']['observed_noise_halfwidth']['px']))==POSITION_NOISE
        assert F(str(cfg['sensing']['observed_noise_halfwidth']['phi']))==PHI_NOISE
        assert F(str(cfg['sensing']['observed_noise_halfwidth']['omega']))==OMEGA_NOISE
        assert F(str(cfg['domain']['state_upper'][0]))==P_MAX
        assert F(str(cfg['domain']['state_upper'][2]))==V_MAX
        assert F(str(cfg['domain']['state_upper'][4]))==PHI_MAX
        assert F(str(cfg['domain']['state_upper'][5]))==OMEGA_MAX
        assert F(str(cfg['domain']['input_upper'][1]))==TAU_MAX
        assert F(str(cfg['domain']['input_lower'][1]))==-TAU_MAX
        assert F(str(cfg['domain']['input_lower'][0]))<=T<=F(str(cfg['domain']['input_upper'][0]))
        for key,idx in [('p',0),('v',2),('phi',4),('omega',5)]:
            center=F(str(cfg['initial_set']['center'][idx]));half=F(str(cfg['initial_set']['halfwidth'][idx]))
            assert INIT[key]==(center-half,center+half)
    assert R==F(3246383,1600000)
    assert len(TORQUES)==HORIZON==30
    rows=envelope()
    max_abs={key:max(max(abs(b[key][0]),abs(b[key][1])) for row in rows for b in [row['bounds']])
             for key in INIT}
    for key,limit in [('p',P_MAX),('v',V_MAX),('phi',PHI_MAX),('omega',OMEGA_MAX)]:
        assert max_abs[key]<limit,(key,max_abs[key],limit)
    assert max(abs(tau) for tau in TORQUES)==TAU_MAX
    min_phi=rows[24]['bounds']['phi'][0]
    max_phi=rows[24]['bounds']['phi'][1]
    assert min_phi>0
    net_acceleration_margin=T*sin_bounds(min_phi)[0]-R
    assert net_acceleration_margin>0
    margins=[]
    for row in rows[24:]:
        pmin=row['bounds']['phi'][0]
        m=T*sin_bounds(pmin)[0]-R
        assert m>0
        margins.append(m)
    baseline=dict(INIT)
    for _ in range(HORIZON):
        baseline=step_interval(baseline,F(0))
    positive_velocity_upper_improvement=baseline['v'][1]-rows[30]['bounds']['v'][1]
    assert positive_velocity_upper_improvement>0
    tilt_worst_abs_v=max(abs(z) for z in rows[30]['bounds']['v'])
    baseline_worst_abs_v=max(abs(z) for z in baseline['v'])
    assert tilt_worst_abs_v>baseline_worst_abs_v
    words=packet_paths()
    assert len(words)==44
    assert all('MMM' not in w for w in words)
    return {'run':245,'base_run':244,
            'evidence':'EXACT_RATIONAL_FINITE_HORIZON_SHARED_TILT_AND_SMF_CONTAINMENT',
            'scope':'frozen four-state Euler, fixed T, full configured initial horizontal/attitude prior box, all independent r_x in [-R,R], all admissible 5-tick success/miss histories; open-loop shared torque',
            'horizon_ticks':HORIZON,'horizon_seconds':str(H*HORIZON),
            'torque_schedule_Nm':[str(x) for x in TORQUES],
            'residual_halfwidth_m_s2':str(R),
            'initial_box':{k:[str(x) for x in bounds] for k,bounds in INIT.items()},
            'max_abs_bounds':{k:str(v) for k,v in max_abs.items()},
            'bounds_at_tick24':{k:[str(x) for x in v] for k,v in rows[24]['bounds'].items()},
            'bounds_at_tick30':{k:[str(x) for x in v] for k,v in rows[30]['bounds'].items()},
            'strict_minimum_tilt_at_tick24_rad':str(min_phi),
            'strict_maximum_tilt_at_tick24_rad':str(max_phi),
            'strict_positive_acceleration_reversal_margin_at_tick24_m_s2':str(net_acceleration_margin),
            'strict_min_acceleration_reversal_margin_ticks24_to30_m_s2':str(min(margins)),
            'zero_torque_baseline_tick30_bounds':{k:[str(x) for x in v] for k,v in baseline.items()},
            'positive_velocity_upper_improvement_vs_zero_torque_at_tick30_m_s':str(positive_velocity_upper_improvement),
            'worst_absolute_velocity_tilt_at_tick30_m_s':str(tilt_worst_abs_v),
            'worst_absolute_velocity_zero_torque_at_tick30_m_s':str(baseline_worst_abs_v),
            'legal_packet_words_six_opportunities':len(words),
            'packet_words':words,
            'smf_update_semantics':'prior propagation by interval inclusion, success position strip intersection, always observed angle/rate strip intersection; true state remains contained by induction for noise-consistent observations; no arbitrary-observation nonempty claim',
            'float_sanity_only':float_sanity(),
            'finite_horizon_robust_state_and_input_constraints':True,
            'all_legal_packet_histories_covered_by_open_loop_policy':True,
            'persistent_tilt_at_tick24':True,
            'general_output_feedback_invariant_terminal_set_proved':False,
            'robust_recursive_feasibility_proved':False,
            'mpc_optimization_implemented':False,
            'six_state_safety_proved':False,
            'gate_A':'blocked',
            'limitations':['The open-loop tilt ramp does not use posterior feedback; SMF strips are sound but interval outer approximations may be conservative.',
                           'Only a finite 30-tick maneuver is certified; no repeatable backup, robust stability or recursive terminal invariant set.',
                           'Angle/rate are initially uncertain and may drift during zero-torque hold; +R acceleration reversal does not imply robustness to -R or switching residuals.',
                           'Fixed thrust horizontal model, not coupled vertical six-state model or thrust scheduling.',
                           'No online MPC optimization or 20ms worst-case runtime guarantee.']}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--root',type=Path)
    p.add_argument('--output',type=Path)
    a=p.parse_args()
    s=json.dumps(verify(a.root),ensure_ascii=False,indent=2,sort_keys=True)+'\n'
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(s)
    else:print(s,end='')

if __name__=='__main__':main()
