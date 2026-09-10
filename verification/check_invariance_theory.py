#!/usr/bin/env python3
"""Exact rational arithmetic for the attitude subcertificate and counterexamples.

This verifies the finite identities/inequalities in the written proof. It does
not test trajectories or certify the full six-state controller/information set.
"""
import argparse
from fractions import Fraction as F
import hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def matmul(A,B):
    return [[sum((a*b for a,b in zip(row,col)),F(0)) for col in zip(*B)] for row in A]

def matvec(A,x):return [sum((a*b for a,b in zip(row,x)),F(0)) for row in A]
def absolute(A):return [[abs(x) for x in row] for row in A]
def as_strings(x):return [str(v) for v in x]

def verify():
    config_path=ROOT/'configs/planar_baseline.json'
    c=json.loads(config_path.read_text(),parse_float=F,parse_int=F)
    assert c['plant']['dt_s']==F(1,50) and c['plant']['inertia_kg_m2']==F(1,50)
    assert c['plant']['external_process_halfwidth']==[0]*6
    assert c['sensing']['observed_noise_halfwidth']['phi']==F(1,200)
    assert c['sensing']['observed_noise_halfwidth']['omega']==F(1,100)
    assert c['sensing']['always_observed_indices']==[4,5]
    assert c['sensing']['delay_ticks']==0
    assert c['initial_set']['center'][4:]==[0,0]
    assert c['initial_set']['halfwidth'][4:]==[F(1,200),F(1,100)]
    assert c['domain']['state_lower'][4:]==[-F(9,20),-2]
    assert c['domain']['state_upper'][4:]==[F(9,20),2]
    assert c['domain']['input_lower'][1]==-F(2,25) and c['domain']['input_upper'][1]==F(2,25)
    h=F(1,50);K=[F(8,25),F(4,25)];r=F(23,25)
    M=[[F(1),h],[-K[0],F(1)-K[1]]]
    N=[[M[i][j]-(r if i==j else 0) for j in range(2)] for i in range(2)]
    assert matmul(N,N)==[[0,0],[0,0]]
    initial=[F(1,200),F(1,100)];measurement=initial
    eta=sum((a*b for a,b in zip(K,measurement)),F(0))
    H=[v+w/(1-r) for v,w in zip(initial,matvec(absolute(N),initial))]
    b=[F(0),F(1)];Nb=matvec(N,b)
    S=[eta*(abs(bi)/(1-r)+abs(ni)/(1-r)**2) for bi,ni in zip(b,Nb)]
    total=[x+y for x,y in zip(H,S)]
    torque=sum((a*b for a,b in zip(K,total)),F(0))+eta
    assert H==[F(1,80),F(1,25)] and S==[F(1,100),F(2,25)]
    assert total==[F(9,400),F(3,25)] and torque==F(37,1250)
    assert total[0]<F(9,20) and total[1]<2 and torque<F(2,25)
    # Known reference generator c+=A*c+b*mu, with tau=mu-K*(y-c).
    # Error dynamics are the same M*e+b*eta as in the regulation proof.
    reference_limits=[F(9,20)-total[0],F(2)-total[1],F(2,25)-torque]
    reference_decel=reference_limits[2]/F(1,50)
    ratio=reference_limits[1]/(h*reference_decel)
    reference_facets=(ratio.numerator+ratio.denominator-1)//ratio.denominator
    assert reference_limits==[F(171,400),F(47,25),F(63,1250)]
    assert reference_decel==F(63,25) and reference_facets==38
    reference_mu=F(1,40);reference_steps=20
    reference_final_angle=h*reference_mu*reference_steps**2
    reference_peak_rate=reference_mu*reference_steps
    reference_torque_bound=reference_mu+torque
    assert reference_final_angle==F(1,5)<reference_limits[0]
    assert reference_peak_rate==F(1,2)<reference_limits[1]
    assert reference_mu<reference_limits[2] and reference_torque_bound==F(273,5000)<F(2,25)
    # Minimum outward angle under the maximal allowed deceleration.
    angular_decel=F(2,25)/F(1,50);speed=F(2);n=25
    stop_angle=h*n*speed-h*h*angular_decel*n*(n-1)/2
    angle16=h*16*speed-h*h*angular_decel*16*15/2
    angle17=h*17*speed-h*h*angular_decel*17*16/2
    assert stop_angle==F(13,25)>F(9,20)
    assert angle16<=F(9,20)<angle17 and angle17==F(289,625)
    # Only for the independent additive acceleration BOX abstraction:
    # sin(.2)<=.2, cos(.2)>=.98 imply incompatible necessary thrust limits.
    thrust_lower=F('1.880')/F('.2')
    thrust_upper=(F('9.81')-F('2.086'))/F('.98')
    assert thrust_lower>thrust_upper
    return {
      'status':'EXACT_RATIONAL_ATTITUDE_SUBSYSTEM_IDENTITIES_PASSED',
      'scope':'Written infinite-horizon attitude proof plus exact finite arithmetic; not full-system certification',
      'control_gains':as_strings(K),'eigenvalue':str(r),'N_squared_zero':True,
      'torque_noise_halfwidth':str(eta),'initial_orbit_hull_box':as_strings(H),
      'disturbance_invariant_sum_box':as_strings(S),'invariant_set_outer_box':as_strings(total),
      'torque_upper_bound':str(torque),'torque_limit':str(F(2,25)),
      'attitude_bound_margin':str(F(9,20)-total[0]),'rate_bound_margin':str(2-total[1]),
      'torque_margin':str(F(2,25)-torque),
      'reference_tracking':{'reference_limits_angle_rate_torque':as_strings(reference_limits),
          'reference_max_deceleration':str(reference_decel),'maximum_braking_facet_index':reference_facets,
          'nonzero_reference_witness':{'mu_magnitude':str(reference_mu),'ticks_per_phase':reference_steps,
              'duration_s':str(2*h*reference_steps),'final_angle':str(reference_final_angle),'final_rate':'0',
              'peak_rate':str(reference_peak_rate),'actual_angle_absolute_bound':str(reference_final_angle+total[0]),
              'actual_rate_absolute_bound':str(reference_peak_rate+total[1]),
              'actual_torque_absolute_bound':str(reference_torque_bound)}},
      'unavoidable_exit_counterexample':{'initial_phi':'0','initial_omega':'2','stopping_displacement':str(stop_angle),
          'angle_at_16':str(angle16),'angle_at_17':str(angle17),'limit':str(F(9,20))},
      'independent_box_thrust_conflict':{'lower_necessary':str(thrust_lower),'upper_necessary':str(thrust_upper)},
      'full_six_state_invariance_proved':False,'neural_superiority_proved':False,
      'config_sha256':hashlib.sha256(config_path.read_bytes()).hexdigest(),
      'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    }

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path);a=p.parse_args()
    result=verify();payload=json.dumps(result,indent=2)+'\n'
    if a.output:
        if a.output.exists():p.error('use a new output file')
        a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(payload)
    print(payload)
