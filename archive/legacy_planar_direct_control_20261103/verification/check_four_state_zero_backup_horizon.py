#!/usr/bin/env python3
"""Run250: sharp zero-torque robust safe horizon for Run249 frozen 4-state plant.

This proves a MAXIMUM horizon only for the FIXED ZERO-TORQUE BACKUP, not
impossibility of other causal/full-state feedback or terminal invariance.
Exact Fraction sine Taylor bounds and outward 1e-10 grid enclosure.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

H=J=F(1,50)
T=F(981,100)
R=F(3246383,1600000)
U=F(2,25)
P_MAX=F(5)
V_MAX=F(3)
PHI_MAX=F(9,20)
OMEGA_MAX=F(2)
GRID=10**10
INITIAL={'p':(F(-1,50),F(1,50)), 'v':(F(-1,10),F(1,10)),
         'phi':(F(-1,200),F(1,200)), 'omega':(F(-1,100),F(1,100))}
LIMITS={'p':P_MAX,'v':V_MAX,'phi':PHI_MAX,'omega':OMEGA_MAX}
ZERO_SAFE_LAST_TICK=67
ZERO_FIRST_UNSAFE_TICK=68


def sin_bounds(x):
    """Alternating Taylor enclosure on [-0.45,0.45], exact rationals."""
    assert -PHI_MAX<=x<=PHI_MAX
    if x<0:
        lo,hi=sin_bounds(-x)
        return -hi,-lo
    lo=x-x**3/6
    return lo,lo+x**5/120


def down(x):
    return F((x.numerator*GRID)//x.denominator,GRID)


def up(x):
    return -down(-x)


def step_zero(box):
    """Sound outward interval image of all states, all independent |r|<=R."""
    p,v,phi,omega=(box[k] for k in ('p','v','phi','omega'))
    assert -PHI_MAX<=phi[0]<=phi[1]<=PHI_MAX
    sin_lo=sin_bounds(phi[0])[0]
    sin_hi=sin_bounds(phi[1])[1]
    return {'p':(down(p[0]+H*v[0]),up(p[1]+H*v[1])),
            'v':(down(v[0]-H*(T*sin_hi+R)),up(v[1]+H*(R-T*sin_lo))),
            'phi':(down(phi[0]+H*omega[0]),up(phi[1]+H*omega[1])),
            'omega':omega}


def safe(box):
    return all(-lim<=box[key][0]<=box[key][1]<=lim for key,lim in LIMITS.items())


def uniform_zero_prefix(n):
    """All initial states and disturbance words; return intervals at ticks 0..n."""
    rows=[dict(INITIAL)]
    for _ in range(n):
        rows.append(step_zero(rows[-1]))
    return rows


def physical_corner_negative(n):
    """ONE actual admissible corner, zero torque, r=-R; outward v enclosure.

    The corner is (p,v,phi,omega)=(-.02,-.1,+.005,+.01). phi and omega
    are EXACT under zero torque; v upper/lower are rational sine enclosures.
    No independent interval corner is treated as a physical trajectory.
    """
    p=(F(-1,50),F(-1,50))
    v=(F(-1,10),F(-1,10))
    phi,omega=F(1,200),F(1,100)
    rows=[(p,v,phi,omega)]
    for _ in range(n):
        sl,sh=sin_bounds(phi)
        p=(down(p[0]+H*v[0]),up(p[1]+H*v[1]))
        v=(down(v[0]-H*(R+T*sh)),up(v[1]-H*(R+T*sl)))
        phi+=H*omega
        rows.append((p,v,phi,omega))
    return rows


def verify(root=None):
    if root is not None:
        cfg=json.loads((Path(root)/'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics']=='defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s']))==H
        assert F(str(cfg['plant']['inertia_kg_m2']))==J
        assert F(str(cfg['plant']['gravity_m_s2']))==T
        assert F(str(cfg['domain']['input_upper'][1]))==U
        for key,i in [('p',0),('v',2),('phi',4),('omega',5)]:
            assert F(str(cfg['domain']['state_upper'][i]))==LIMITS[key]
            c=F(str(cfg['initial_set']['center'][i]))
            w=F(str(cfg['initial_set']['halfwidth'][i]))
            assert INITIAL[key]==(c-w,c+w)
        assert cfg['sensing']['position_period_ticks']==5
        assert cfg['sensing']['max_consecutive_missed_packets']==2
        import sys
        sys.path.insert(0,str(Path(root)/'verification'))
        import check_four_state_shielded_smf_mpc as prior
        assert prior.DEADLINE==55
        assert prior.INIT==INITIAL
        assert prior.R==R and prior.U==U
        for k in (1,55,67):
            assert uniform_zero_prefix(k)[-1]==prior.zero_certificate(k)[-1]
    assert R==F(47,25)+F(243,16000)*T
    boxes=uniform_zero_prefix(ZERO_FIRST_UNSAFE_TICK)
    assert len(boxes)==69
    assert all(safe(b) for b in boxes[:ZERO_SAFE_LAST_TICK+1])
    assert not safe(boxes[ZERO_FIRST_UNSAFE_TICK])
    assert boxes[ZERO_FIRST_UNSAFE_TICK]['v'][0]<-V_MAX
    witness=physical_corner_negative(ZERO_FIRST_UNSAFE_TICK)
    assert len(witness)==69
    assert all(abs(phi)<PHI_MAX and abs(omega)<OMEGA_MAX for _,_,phi,omega in witness)
    assert all(max(map(abs,p))<P_MAX and max(map(abs,v))<V_MAX for p,v,_,_ in witness[:ZERO_SAFE_LAST_TICK+1])
    p68,v68,phi68,omega68=witness[-1]
    assert v68[1]<-V_MAX
    assert boxes[ZERO_FIRST_UNSAFE_TICK]['v'][0]<=v68[0]<=v68[1]<=boxes[ZERO_FIRST_UNSAFE_TICK]['v'][1]
    margin=-V_MAX-v68[1]
    assert margin>0
    assert safe(boxes[55])
    assert not safe(boxes[68])
    # From tick55, simply restarting a new 55-tick ZERO backup is invalid.
    # No statement about other torque policies or full-information viability.
    return {'run':250,'base_run':249,
            'evidence':'EXACT_RATIONAL_SHARP_UNIFORM_ZERO_BACKUP_HORIZON',
            'model':'frozen four-state Euler, fixed T=9.81N, |r|<=R, tau=0',
            'zero_backup_last_uniformly_safe_tick':ZERO_SAFE_LAST_TICK,
            'zero_backup_first_unsafe_tick':ZERO_FIRST_UNSAFE_TICK,
            'run249_original_deadline_tick':55,
            'run249_zero_backup_terminal_not_repeatable_for_55_more_ticks':True,
            'uniform_tick55_velocity_box':list(map(str,boxes[55]['v'])),
            'uniform_tick67_velocity_box':list(map(str,boxes[67]['v'])),
            'uniform_tick68_velocity_box':list(map(str,boxes[68]['v'])),
            'true_initial_corner':['-1/50','-1/10','1/200','1/100'],
            'true_adverse_disturbance':'r=-R for ticks 0..67',
            'true_control':'tau=0 for ticks 0..67',
            'true_tick68_velocity_enclosure':list(map(str,v68)),
            'true_tick68_pitch_exact':str(phi68),
            'true_tick68_rate_exact':str(omega68),
            'strict_velocity_violation_margin_lower_bound_m_s':str(margin),
            'no_other_policy_impossibility_claim':True,
            'full_information_viability_of_tick55_corner_unknown':True,
            'smf_terminal_invariance_proved':False,
            'general_recursive_feasibility_proved':False,
            'wcet_20ms_proved':False,'gate_A':'blocked'}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',type=Path)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    s=json.dumps(verify(args.root),sort_keys=True,indent=2,ensure_ascii=False)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(s)
    else:print(s,end='')

if __name__=='__main__':main()
