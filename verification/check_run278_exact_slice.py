#!/usr/bin/env python3
"""Run278: exact rational, history-compatible posterior inner slice at tick60.

Only the x45=0, phi=omega=0, tau=0, T=mg continuation is optimised.
It is a subset of the Run260 MMS posterior, not its full outer estimate.
"""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

H = J = F(1, 50)
T = F(981, 100)
R = F(3246383, 1600000)
EPS = F(1, 50)
VMAX = F(3)
PULSE = (F(1, 25), -F(1, 25), -F(1, 25), F(1, 25), F(0))
SUCCESS = (5, 10, 15, 30, 45, 60)
MISSED = (20, 25, 35, 40, 50, 55)


def history_prefix():
    """Reconstruct Run271's legal common prefix, including nonzero torque."""
    states = {k: (F(0),)*4 for k in range(31)}
    p = v = phi = omega = F(0)
    for k in range(30, 45):
        tau = PULSE[k-30] if k < 35 else F(0)
        # r=T*sin(phi) cancels lateral acceleration; bound via |sin phi|<=|phi|.
        assert T*abs(phi) <= R
        p, v, phi, omega = p+H*v, v, phi+H*omega, omega+H*tau/J
        assert p == v == 0
        assert abs(phi) <= F(9,20) and abs(omega) <= 2
        states[k+1] = (p, v, phi, omega)
    assert states[45] == (F(0),)*4
    return states


def optimal_alpha():
    """One fractional acceleration at weight 11, with final p60=+EPS."""
    a = (EPS/(H*H*R)-16)/11
    assert -1 <= a <= 1
    return a


def controls(sign):
    assert sign in (-1, 1)
    a = optimal_alpha()
    return [-sign*R]*3 + [sign*a*R] + [sign*R]*11


def continuation(sign):
    states = history_prefix()
    p,v,phi,omega = states[45]
    for k,r in enumerate(controls(sign),45):
        assert abs(r) <= R
        p,v,phi,omega = p+H*v, v+H*r, phi+H*omega, omega
        assert abs(p)<=5 and abs(v)<=VMAX and abs(phi)<=F(9,20) and abs(omega)<=2
        states[k+1]=(p,v,phi,omega)
    return states


def dual_velocity_bound():
    """Exact LP dual bound on the x45=0, zero-angle 15-step slice.

    v60=h*sum(r_i), p60=h²*sum((14-i)*r_i).
    For lambda=1/11, sum r_i <= (1/11)sum(w_i*r_i)
                                  + R*sum|1-w_i/11|
                               <= EPS/(11*h²)+72*R/11.
    """
    weights = [14-i for i in range(15)]
    dual_l1 = sum((abs(F(1)-F(w,11)) for w in weights), F(0))
    assert dual_l1 == F(72,11)
    return H*(EPS/(11*H*H)+R*dual_l1)


def velocity_diameter_after(n):
    assert isinstance(n,int) and n>=0
    return 2*dual_velocity_bound()+2*n*H*R


def first_open_loop_obstruction():
    slope=2*H*R
    ratio=(2*VMAX-2*dual_velocity_bound())/slope
    return ratio.numerator//ratio.denominator+1


def verify(root=None):
    assert ''.join('S' if k in SUCCESS else 'M' for k in range(5,61,5))=='SSSMMSMMSMMS'
    count=0
    for k in range(5,61,5):
        count=0 if k in SUCCESS else count+1
        assert count<=2
    plus,minus=continuation(+1),continuation(-1)
    assert plus[60]==(EPS,dual_velocity_bound(),F(0),F(0))
    assert minus[60]==(-EPS,-dual_velocity_bound(),F(0),F(0))
    assert plus[45]==minus[45]==(F(0),)*4
    for k in SUCCESS:
        assert abs(plus[k][0])<=EPS and abs(minus[k][0])<=EPS
    assert all(plus[k][2:]==minus[k][2:] for k in range(61))
    # The shared position reading y60=0 uses noise -p60, at both endpoints.
    assert -plus[60][0]==-EPS and -minus[60][0]==EPS
    assert dual_velocity_bound()==F(39217447,110000000)
    assert 2*dual_velocity_bound()>F(22724681,40000000)
    n=first_open_loop_obstruction()
    assert n==66 and velocity_diameter_after(n-1)<=2*VMAX<velocity_diameter_after(n)
    if root is not None:
        root=Path(root)
        cfg=json.loads((root/'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics']=='defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s']))==H
        assert F(str(cfg['plant']['inertia_kg_m2']))==J
        assert F(str(cfg['plant']['gravity_m_s2']))==T
        assert F(str(cfg['sensing']['observed_noise_halfwidth']['px']))==EPS
        assert cfg['sensing']['position_period_ticks']==5
        assert cfg['sensing']['max_consecutive_missed_packets']==2
        assert F(str(cfg['domain']['state_upper'][2]))==VMAX
        prev=json.loads((root/'results/run271_run260_membership_20261102/checks.json').read_text())
        assert prev['packet_history_ticks_5_to_60']=='SSSMMSMMSMMS'
        assert prev['tick45_true_state']==['0']*4
        assert prev['run260_membership'].startswith('constructive consistent true trajectories')
        prev277=json.loads((root/'results/run277_open_loop_diameter_20261102/checks.json').read_text())
        assert F(prev277['initial_velocity_diameter'])==F(22724681,40000000)
    return {
        'run':278,
        'parent':'Run271 genuine Run260 MMS zero-reading history and Run277 open-loop argument',
        'packet_history_ticks_5_to_60':'SSSMMSMMSMMS',
        'restriction':'x45=(0,0,0,0), phi=omega=0 and tau=0 on ticks45..59, T=9.81, r_k independently in [-R,R]',
        'scope':'exact maximum |v60| in this restricted, genuinely feasible posterior slice; lower bound on full posterior width',
        'alpha_at_tick48':str(optimal_alpha()),
        'positive_residual_ticks45_to59':[str(z) for z in controls(1)],
        'tick60_plus_state':[str(z) for z in plus[60]],
        'tick60_minus_state':[str(z) for z in minus[60]],
        'tick60_position_reading':'0',
        'tick60_noise_plus':str(-EPS),
        'tick60_noise_minus':str(EPS),
        'exact_dual_coefficient_sum':'72/11',
        'exact_restricted_max_abs_velocity':str(dual_velocity_bound()),
        'full_posterior_velocity_diameter_necessary_lower_bound':str(2*dual_velocity_bound()),
        'prior_run271_lower_bound':'22724681/40000000',
        'first_open_loop_impossible_horizon_ticks':n,
        'first_open_loop_impossible_tick':60+n,
        'diameter_after_65':str(velocity_diameter_after(65)),
        'diameter_after_66':str(velocity_diameter_after(66)),
        'proof':'LP primal witness r45..47=-R, r48=alpha*R, r49..59=+R, with alpha=(eps/(h²R)-16)/11; final p60=eps. Dual bound sum r <= eps/(11h²)+72R/11 is attained. Sign reversal yields same y60=0 via noises ±eps. With any shared observation-independent thrust and torque after tick60, identical initial angles imply identical angle trajectories and future velocity diameter Delta(n)=Delta(0)+2nhR under independent extreme residuals. Delta(65)<=6<Delta(66), so at least one world violates a hard constraint by tick126.',
        'not_proved':['full posterior exact outer enclosure','causal feedback impossibility','failure at tick125','finite horizon controller','terminal information RCI','MPC solver','infinite recursive feasibility','six-state physical safety','20ms WCET'],
        'gate_A':'blocked'
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
