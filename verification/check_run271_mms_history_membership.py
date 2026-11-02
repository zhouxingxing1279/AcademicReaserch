#!/usr/bin/env python3
"""Run271: exact rational membership of Run270 two-truth witness in Run260 MMS history.

Proof uses the exact real choice r_k=T*sin(phi_k), whose cancellation is
symbolic; Fraction is used for all remaining dynamics and inequalities.
No floating-point sine evaluation is used or needed. Not a controller.
"""
from fractions import Fraction as F
import json
import argparse
from pathlib import Path

H=J=F(1,50)
T=F(981,100)
R=F(3246383,1600000)
U=F(2,25)
EPS_P=F(1,50)
PULSE=(F(1,25),-F(1,25),-F(1,25),F(1,25),F(0))
# Actual Run254/259/260 packet word through 60 for MMS at 35/40/45.
SUCCESS=(0,5,10,15,30,45,60)
MISS=(20,25,35,40,50,55)


def angular_history():
    phi=omega=F(0)
    rows={0:(phi,omega)}
    for k in range(60):
        tau=PULSE[k-30] if 30<=k<35 else F(0)
        assert abs(tau)<=U
        phi,omega=phi+H*omega,omega+H/J*tau
        rows[k+1]=(phi,omega)
        assert abs(phi)<=F(9,20) and abs(omega)<=2
    return rows


def certificate(root=None):
    assert set(SUCCESS).isdisjoint(MISS)
    assert SUCCESS[1:5]==(5,10,15,30)
    assert ''.join('S' if k in SUCCESS else 'M' for k in (35,40,45))=='MMS'
    assert ''.join('S' if k in SUCCESS else 'M' for k in (45,50,55,60))=='SMMS'
    packet_ticks=sorted(set(SUCCESS)|set(MISS))
    assert packet_ticks==list(range(0,61,5))
    assert 'MMM' not in ''.join('S' if k in SUCCESS else 'M' for k in packet_ticks)
    ang=angular_history()
    assert [(str(ang[k][0]),str(ang[k][1])) for k in (30,31,32,33,34,35)]==[
        ('0','0'),('0','1/25'),('1/1250','0'),('1/1250','-1/25'),('0','0'),('0','0')]
    assert all(ang[k]==(F(0),F(0)) for k in range(35,61))
    active=[k for k in range(30,45) if ang[k][0]]
    assert active==[32,33]
    # Exact real disturbance r_k=T*sin(phi_k) cancels -T*sin(phi_k).
    # |r_k|<=T*|phi_k| <= 981/125000 < R by |sin z|<=|z|.
    max_cancel_bound=max(T*abs(ang[k][0]) for k in range(30,45))
    assert max_cancel_bound==F(981,125000) and max_cancel_bound<R
    # With this admissible r, p=v=0 for ticks 0..52. The two continuations
    # use +/-R on ticks 53..59, and no other process disturbance.
    paths={}
    for sign in (-1,1):
        p=v=F(0)
        states={0:(p,v)}
        for k in range(60):
            if k<53:
                # r=0 while phi=0; on ticks32,33 choose r=T*sin(phi).
                # The exact cancellation yields a_k=-T*sin(phi)+r=0.
                assert k not in (32,33) or ang[k][0]==F(1,1250)
                acceleration=F(0)
            else:
                assert ang[k][0]==0
                acceleration=sign*R
            p,v=p+H*v,v+H*acceleration
            states[k+1]=(p,v)
            assert abs(p)<=5 and abs(v)<=3
        assert all(states[k]==(F(0),F(0)) for k in range(53))
        assert states[45]==(F(0),F(0))
        assert states[60]==(sign*F(68174043,4000000000),sign*F(22724681,80000000))
        # All successful packet readings y=0. At tick60 choose noise=-p60.
        for tick in SUCCESS:
            assert abs(states[tick][0])<=EPS_P
        paths[sign]=states
    assert paths[1][60][1]-paths[-1][60][1]==F(22724681,40000000)
    assert paths[1][60][0]-paths[-1][60][0] <= 2*EPS_P
    # Run260 SMM is a DIFFERENT packet word: 45=M and 50 must be S.
    assert ''.join('S' if k in (35,) else 'M' for k in (35,40,45))=='SMM'
    assert (45 in SUCCESS) and (45 not in MISS)
    if root is not None:
        cfg=json.loads((Path(root)/'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics']=='defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s']))==H
        assert F(str(cfg['plant']['inertia_kg_m2']))==J
        assert F(str(cfg['plant']['gravity_m_s2']))==T
        assert cfg['sensing']['position_period_ticks']==5
        assert cfg['sensing']['max_consecutive_missed_packets']==2
        assert F(str(cfg['sensing']['observed_noise_halfwidth']['px']))==EPS_P
        assert F(str(cfg['sensing']['observed_noise_halfwidth']['phi']))==F(1,200)
        assert F(str(cfg['sensing']['observed_noise_halfwidth']['omega']))==F(1,100)
        old260=json.loads((Path(root)/'results/run260_conditional_shared_bridge_20261102/checks.json').read_text())
        assert old260['starting_packet_patterns']==['SMM','MMS']
        for key,value in zip(('p','v','phi','omega'),(F(0),)*4):
            lo,hi=(F(q) for q in old260['branches']['MMS']['tick45_outer'][key])
            assert lo<=value<=hi
        for sign in (-1,1):
            for key,value in zip(('p','v','phi','omega'),(*paths[sign][60],*ang[60])):
                lo,hi=(F(q) for q in old260['branches']['MMS']['tick60_outer'][key])
                assert lo<=value<=hi
        old270=json.loads((Path(root)/'results/run270_recovered_packet_fiber_20261102/checks.json').read_text())
        assert F(old270['post_success_velocity_diameter_floor'])==paths[1][60][1]-paths[-1][60][1]
        assert [F(q) for q in old270['post_success_plus_state']]==[*paths[1][60],*ang[60]]
        assert [F(q) for q in old270['post_success_minus_state']]==[*paths[-1][60],*ang[60]]
    return {
        'run':271,
        'claim':'Run270 two true trajectories are members of one actual Run260 MMS-history observation fiber; not SMM',
        'packet_success_ticks':list(SUCCESS),
        'packet_miss_ticks':list(MISS),
        'angular_pulse_tau_ticks_30_to_34':[str(x) for x in PULSE],
        'angular_states_ticks_30_to_35':{str(k):[str(x) for x in ang[k]] for k in range(30,36)},
        'exact_canceling_process_disturbance':'r_k=T*sin(phi_k) for k=30..44; zero otherwise until tick52',
        'nonzero_cancel_ticks':active,
        'max_cancel_disturbance_absolute_upper_bound':str(max_cancel_bound),
        'allowed_disturbance_absolute_bound':str(R),
        'two_paths_process_disturbance_ticks_53_to_59':'opposite +/-R',
        'true_state_tick45_both_paths':['0','0','0','0'],
        'true_states_tick60_plus':[str(x) for x in (*paths[1][60],*ang[60])],
        'true_states_tick60_minus':[str(x) for x in (*paths[-1][60],*ang[60])],
        'successful_position_readings':'zero at all success ticks; choose noise=-p_k; zero except tick60',
        'angular_readings':'true phi,omega each tick with zero noise; ticks31..33 are not all zero',
        'post_success_velocity_diameter_lower_bound_m_s':str(paths[1][60][1]-paths[-1][60][1]),
        'evidence':'symbolic exact cancellation, Fraction angular recurrence and per-tick constraints; existential history membership',
        'not_certified':['all Run260 observation fibers','SMM packet branch','arbitrary causal control','15-tick feedback return','terminal information RCI','MPC solver','infinite recursive feasibility','six-state physical safety'],
        'gate_A':'blocked'
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root',type=Path)
    ap.add_argument('--output',type=Path)
    a=ap.parse_args()
    data=json.dumps(certificate(a.root),indent=2,sort_keys=True,ensure_ascii=False)+'\n'
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(data)
    else: print(data,end='')

if __name__=='__main__': main()
