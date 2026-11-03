"""Exact counterexample to the abstract candidate, not a truth simulation."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
from check_causal_model import step, inputs, verify as previous


def verify():
    old=previous()
    d=F(1043,500); h=F(1,50); ell=F(5); kp=F(1); kd=F(2); P=F(3,2)
    assert d<=F(old['noise_halfwidth'][1])
    rows=[]
    for L in (5,10,15):
        c=h*(L-1)/(2*ell)-h*h*(L*L-1)/12
        factor=1-ell*L*h
        assert abs(factor)<1
        E=d*(1/ell-h*(L-1)/2)
        assert E==factor*E+(L*h-ell*h*h*L*(L-1)/2)*d
        ev=sum(E+j*h*d for j in range(L))/L
        ep=sum(j*h*E+h*h*j*(j-1)/2*d for j in range(L))/L
        assert ev==d/ell and ep==c*d
        avg=d*((1+kd/ell)/kp+c)
        threshold=d*(1+kd/ell)/(P-d*c)
        assert avg>P and threshold>kp
        rows.append({'L':L,'error_factor':str(factor),'c_L':str(c),'required_mean_height_offset':str(avg),'necessary_kp_lower_bound':str(threshold)})
    z=[F(0)]*14; w=[F(0),d]+[F(0)]*4
    first=None; before=None
    limits=[F(5),P,F(3),F(3),F(45,100),F(2)]
    for k in range(89):
        t,mu,tau=inputs(z)
        assert F(4905,1000)<=F(981,100)+t<=F(14715,1000)
        assert abs(tau)<=F(8,100) and mu==0
        assert all(z[i]==0 for i in (0,2,4,5,6,8,10,11,12,13))
        if any(abs(z[i])>limits[i] for i in range(6)):
            first=k
            assert k==88 and z[1]>P and all(abs(z[i])<=limits[i] for i in (0,2,3,4,5))
            break
        before=z
        z=step(z,w,(k+1)%5==0)
    assert first==88
    return {'status':'EXACT_ABSTRACT_CANDIDATE_COUNTEREXAMPLE_PASSED','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'model_checker_sha256':old['source_sha256'],'periodic_necessary_conditions':rows,'disturbance':list(map(str,w)),'first_domain_exit_tick':first,'state_tick_87':list(map(str,before[:6])),'state_tick_88':list(map(str,z[:6])),'height_offset_tick_88_display':float(z[1]),'all_preceding_state_and_input_constraints_checked':True,'abstract_candidate_rejected':True,'physical_aerodynamic_realizability_proved':False,'alternative_controller_impossibility_proved':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    result=verify()
    with a.output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(result['status'])
