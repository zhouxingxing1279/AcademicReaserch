#!/usr/bin/env python3
"""Run276: exact full-history member defeating universal Run275 speed gate.

Only the frozen discrete four-state Euler model is certified. No MPC or RCI.
"""
from fractions import Fraction as F
import json
from pathlib import Path
import argparse

H=J=F(1,50)
T=F(981,100)
R=F(3246383,1600000)
EPS=F(1,50)
G=F(187678479,80000000)
PULSE=(F(1,25),-F(1,25),-F(1,25),F(1,25),F(0))
SUCCESS=(5,10,15,30,35,50,60,65,70,75,80,85,90)
MISSED=(20,25,40,45,55)

def q(v): return f'{v.numerator}/{v.denominator}'

def states():
    # 0..30 exactly zero; Run255 attitude pulse at 30..34.
    x={k:(F(0),)*4 for k in range(31)}
    p=v=phi=omega=F(0)
    for k in range(30,90):
        tau=PULSE[k-30] if k<35 else F(0)
        # On pulse ticks choose r=4R/5+T*sin(phi), so net a=4R/5.
        # Since |phi|<=1/1250, |r|<=4R/5+T/1250<R.
        # After pulse, phi=0 and r=R, so net a=R.
        a=F(4,5)*R if k<35 else R
        p,v,phi,omega=p+H*v,v+H*a,phi+H*omega,omega+H*tau/J
        x[k+1]=(p,v,phi,omega)
    return x

def verify():
    x=states()
    assert x[30]==(F(0),)*4
    assert x[35][2:]==(F(0),F(0))
    assert max(abs(x[k][2]) for k in range(30,35))==F(1,1250)
    assert F(4,5)*R+T/F(1250)<R
    assert x[35][0]<=EPS
    assert x[90][1]>G
    assert all(abs(p)<=5 and abs(v)<=3 and abs(phi)<=F(9,20) and abs(om)<=2 for p,v,phi,om in x.values())
    # Successful tick35 reading is zero with legal noise -p35.
    read={k:(F(0) if k==35 else x[k][0]) for k in SUCCESS}
    noise={k:read[k]-x[k][0] for k in SUCCESS}
    assert all(abs(n)<=EPS for n in noise.values())
    streak=0
    for k in range(5,91,5):
        assert (k in SUCCESS)!=(k in MISSED)
        streak=0 if k in SUCCESS else streak+1
        assert streak<=2
    # All attitude/omega observations are the true values (zero noise).
    assert all(read[k]==0 for k in (5,10,15,30,35))
    a,b=85,90
    phi0=F(1,125); omega0=F(1,100)
    def A(k): return R+T*(phi0+(k-60)*H*omega0)
    B=2*EPS/((b-a)*H)+H/(b-a)*sum((i-a+1)*A(i) for i in range(a,b))+H*sum(A(i) for i in range(b,90))
    D=(b-a)*H*(G-B)
    delta=abs(read[b]-read[a])
    assert delta>D
    assert x[90][1]==H*R*(F(4,5)*5+55)==F(59,50)*R
    return {
        'run':276,
        'scope':'constructive member of Run260 SMM fixed zero-reading prefix through tick45, with legal 50/60 successes and 65..90 all successes',
        'packet_history_5_to_90':''.join('S' if k in SUCCESS else 'M' for k in range(5,91,5)),
        'pulse_torque_30_to_34':[q(t) for t in PULSE],
        'pulse_disturbance':'r=4R/5+T*sin(phi), |r|<=4R/5+T/1250<R; exact net a=4R/5',
        'post_pulse_disturbance':'r=R, phi=0, exact net a=R for ticks35..89',
        'position_noise_tick35':q(noise[35]),
        'position_readings':{str(k):q(read[k]) for k in SUCCESS},
        'states':{str(k):[q(z) for z in x[k]] for k in (30,35,45,50,60,75,85,90)},
        'speed_gate_G':q(G),
        'speed_at_90':q(x[90][1]),
        'speed_excess':q(x[90][1]-G),
        'run275_gate_85_90':q(D),
        'actual_displacement_85_90':q(delta),
        'all_hard_state_constraints_satisfied':True,
        'all_measurement_noises_within_bounds':True,
        'all_packet_streaks_legal':True,
        'meaning':'Run275 universal speed-gate assertion is false for a true admissible observation history; no actual hard-constraint violation is shown',
        'not_certified':['full posterior','all histories','causal feedback impossibility','MPC closed loop','terminal information RCI','infinite safety','six-state physical safety','20ms WCET'],
        'gate_A':'blocked'
    }

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);a=parser.parse_args()
    s=json.dumps(verify(),sort_keys=True,indent=2,ensure_ascii=False)+'\n'
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    else:print(s,end='')
