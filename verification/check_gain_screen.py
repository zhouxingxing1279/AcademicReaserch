"""Exact necessary-condition screen and sufficient observer bound, not safety."""
import argparse, hashlib, json
from fractions import Fraction as F
from pathlib import Path
from check_terminal_obstruction import verify as previous


def verify():
    previous()
    D=F(572143,160000); eps=F(1,50); h=F(1,50)
    kp,kd,ell=F(5),F(3),F(9,2)
    def coefficients(gain,L):
        a=abs(1-gain*L*h)
        b=h*sum(abs(1-gain*h*j) for j in range(L))
        assert a<1
        return a,b,(D*b+2*gain*eps)/(1-a)
    old=max(coefficients(F(5),L)[2] for L in (5,10,15))
    new=max(coefficients(ell,L)[2] for L in (5,10,15))
    assert old==F(13,50)*D+F(2,5)
    assert new==F(41,225)*D+F(2,5)
    assert old-new==F(7,90)*D>0
    rows=[]
    for L in (5,10,15):
        # Verify every coefficient of the lifted error map independently by recurrence.
        for idx in range(L+3):
            E=F(idx==0); n0=F(idx==1); n1=F(idx==2)
            w=[F(idx==j+3) for j in range(L)]
            ep,ev=-n0,E
            for value in w:
                ep,ev=ep+h*ev,ev+h*value
            corrected=ev-ell*ep-ell*n1
            formula=(1-ell*L*h)*E+h*sum((1-ell*h*(L-1-j))*w[j] for j in range(L))+ell*(n0-n1)
            assert corrected==formula
        a,b,r=coefficients(ell,L)
        slack=new-(a*new+D*b+2*ell*eps)
        assert slack>=0
        c=h*(L-1)/(2*ell)-h*h*(L*L-1)/12
        avg=D*((1+kd/ell)/kp+c)
        assert avg<F(3,2)
        rows.append({'L':L,'a':str(a),'b':str(b),'individual_R':str(r),'invariance_slack':str(slack),'constant_disturbance_mean_height':str(avg)})
    startup=[]
    for q in (5,10):
        a,b,_=coefficients(ell,q)
        bound=a*F(1,10)+ell*(F(1,50)+eps)+D*b
        assert bound<=new
        startup.append({'first_packet_tick':q,'velocity_error_bound':str(bound)})
    assert F(1,10)<=new
    jury=[h*h*kp,h*kd-h*h*kp,4-2*h*kd+h*h*kp]
    assert jury==[F(1,500),F(29,500),F(1941,500)] and min(jury)>0
    # Dropping signs would underestimate the L=15 forcing coefficient.
    signed=h*sum(1-ell*h*j for j in range(15))
    assert signed<coefficients(ell,15)[1]
    return {'status':'EXACT_GAIN_SCREEN_AND_OBSERVER_BOUND_PASSED','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'candidate':{'kp':str(kp),'kd':str(kd),'vertical_observer_gain':str(ell)},'D':str(D),'epsilon':str(eps),'rows':rows,'old_R':str(old),'new_R':str(new),'old_R_display':float(old),'new_R_display':float(new),'startup':startup,'jury_slacks':list(map(str,jury)),'lifted_error_coefficients_checked':True,'negative_control_signed_sum_rejected':True,'observer_bound_is_global_minimum':False,'hard_constraints_certified':False,'full_six_state_invariance_certified':False,'neural_advantage_proved':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    result=verify()
    with args.output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(result['status'])
