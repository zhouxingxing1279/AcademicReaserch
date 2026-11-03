"""Run212: exact three-packet, measurement-consistent velocity support.

A 41-step window [150,191] uses position packets at 150,165,180 and
attitude measurements at every step 150..190. This is a rigorous OUTER
interval of the measurement-consistent velocity set, not an exact CZ or an
infinite-horizon safety certificate. All calculations use Fraction.
"""
from fractions import Fraction as Q
import json
from pathlib import Path

H=Q(1,50)
N=15
EXTENSION=11
SIGMA_P=Q(1,50)
SIGMA_PHI=Q(1,200)
TMAX=Q(2943,200)


def rad(t):
    return Q(47,25)+Q(243,16000)*t


def identity_weights():
    """v_191 = 5/3*p_150 - 20/3*p_165 + 5*p_180 + sum w_i*a_(150+i)."""
    c=(Q(5,3),-Q(20,3),Q(5))
    assert sum(c)==0
    assert c[1]*N*H+c[2]*2*N*H==1
    w=[]
    for i in range(2*N+EXTENSION):
        p15=H*H*(N-1-i) if i<N else Q(0)
        p30=H*H*(2*N-1-i) if i<2*N else Q(0)
        w.append(H-c[1]*p15-c[2]*p30)
    return c,tuple(w)


def measurement_support(position_packets,attitude_observations,thrusts):
    """Guaranteed outer support, with independent bounded noise/residuals.

    The true plant may impose MORE constraints (attitude dynamics, initial
    conditions, past observations); relaxing them cannot invalidate inclusion.
    The known input torque cancels from the velocity/position identity.
    """
    c,w=identity_weights()
    assert len(position_packets)==3 and len(attitude_observations)==len(w)==len(thrusts)
    center=sum((a*p for a,p in zip(c,position_packets)),Q(0))
    center+=sum((wi*(-t*y) for wi,t,y in zip(w,thrusts,attitude_observations)),Q(0))
    radius=SIGMA_P*sum(map(abs,c),Q(0))
    radius+=sum((abs(wi)*(t*SIGMA_PHI+rad(t)) for wi,t in zip(w,thrusts)),Q(0))
    return center-radius,center+radius


def replay_positive_high():
    """Optional full-repository integration; never substitute a synthetic history."""
    import check_nominal_short_mpc as base
    m=base.m
    x=(Q(0),)*4
    box=m.initial_box()
    prev_p=box[0]
    accels=[]
    positions={}
    attitudes={}
    thrusts={}
    for k in range(191):
        t=m.thrust('positive_high',k)
        if 150<=k<=190:
            attitudes[k]=x[2]+m.measurement_noise('positive_high',k)[2]
            thrusts[k]=t
        allowed,reason=base.interval(box,t)
        assert allowed is not None,(k+1,reason)
        u=max(allowed[0],min(allowed[1],m.proposed(box)-Q(1,5)*m.mid(box[3])))
        old_phi=box[2]
        accels.append(m.add(m.scale(old_phi,-t),(-m.rad(t),m.rad(t))))
        x=m.step(x,t,u,m.residual('positive_high',k,t))
        box=m.predict(box,t,u)
        packet=(k+1)%15==0
        box=m.observe(box,x,packet,m.measurement_noise('positive_high',k))
        if packet:
            positions[k+1]=x[0]+m.measurement_noise('positive_high',k)[0]
            box=(box[0],m.intersect(box[1],m.velocity_from_packets(prev_p,box[0],accels)),box[2],box[3])
            prev_p=box[0]
            accels=[]
        assert all(lo<=v<=hi for (lo,hi),v in zip(box,x))
    assert base.interval(box,m.TMAX)[0] is None
    lo,hi=measurement_support([positions[i] for i in (150,165,180)],
                              [attitudes[i] for i in range(150,191)],
                              [thrusts[i] for i in range(150,191)])
    assert lo<=x[1]<=hi
    assert box[1][0]<lo, 'No strictly improved lower bound on this replay'
    return {'run':212,'tick':192,'old_outer_velocity_lower':str(box[1][0]),
            'new_three_packet_velocity_lower':str(lo),
            'new_three_packet_velocity_upper':str(hi),
            'actual_velocity':str(x[1]),
            'strict_lower_improvement':str(lo-box[1][0]),
            'old_lower_is_excluded_by_relaxed_history':True,
            'evidence':'exact rational three-packet measurement-consistency OUTER support',
            'gate_A':'blocked',
            'limitations':['uses observed position packets at 150,165,180 and attitude observations 150..190',
                           'relaxes joint attitude dynamics and past history; not exact CZ',
                           'does not establish backup admission or recursive feasibility']}


def main():
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    result=replay_positive_high()
    content=json.dumps(result,indent=2,ensure_ascii=False)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(content)
    else:
        print(content,end='')

if __name__=='__main__':
    main()
