#!/usr/bin/env python3
"""Run242: exact rational local-instability obstruction for repeated Run241 pulses.

Fixed n zero-torque ticks followed by a 15-tick observation-conditioned pulse.
This is NOT a general output-feedback or RCI impossibility theorem.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

H=J=F(1,50)
T=F(981,100)
GAIN=F(2,3)
SHAPE=(1,)*3+(-1,)*6+(1,)*3+(0,)*3
MODES=(5,10,15)

def angle_coefficients():
    phi=omega=F(0)
    angles=[]
    for s in SHAPE:
        angles.append(phi)
        phi,omega=phi+H*omega,omega+H/J*GAIN*s
    assert phi==omega==0
    return angles

def coefficients():
    angles=angle_coefficients()
    N=len(SHAPE)
    alpha=H*T*sum(angles,F(0))
    beta=H*H*T*sum(((N-1-j)*angles[j] for j in range(N)),F(0))
    return alpha,beta

def pulse_jacobian(n):
    if n not in MODES: raise ValueError('unsupported macrocycle mode')
    alpha,beta=coefficients()
    duration=len(SHAPE)*H
    # n free Euler steps then y=p_n and 15 pulse steps, with phi=omega=0.
    return ((1-beta,(1-beta)*n*H+duration),(-alpha,1-alpha*n*H))

def det2(m):
    return m[0][0]*m[1][1]-m[0][1]*m[1][0]

def trace2(m):
    return m[0][0]+m[1][1]

def verify(root=None):
    if root is not None:
        cfg=json.loads((Path(root)/'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics']=='defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s']))==H
        assert F(str(cfg['plant']['inertia_kg_m2']))==J
        assert F(str(cfg['plant']['gravity_m_s2']))==T
        assert cfg['sensing']['position_period_ticks']==5
        assert cfg['sensing']['max_consecutive_missed_packets']==2
        assert cfg['sensing']['position_indices']==[0,1]
    alpha,beta=coefficients()
    assert alpha==F(8829,62500)
    assert beta==F(26487,1250000)
    assert sum(SHAPE)==0 and angle_coefficients()[-1]==0
    det=1-beta+len(SHAPE)*H*alpha
    assert det==F(1276487,1250000)>1
    modes=[]
    for n in MODES:
        m=pulse_jacobian(n)
        tr=trace2(m)
        disc=tr*tr-4*det2(m)
        assert det2(m)==det and disc<0 and tr>0
        modes.append({'pre_pulse_zero_ticks':n,'macrocycle_ticks':n+len(SHAPE),
                      'jacobian':[[str(x) for x in row] for row in m],
                      'trace':str(tr),'determinant':str(det2(m)),
                      'discriminant':str(disc),'complex_pair_modulus_squared':str(det),
                      'both_eigenvalues_outside_unit_circle':True})
    return {'run':242,'evidence':'EXACT_RATIONAL_JACOBIAN_LOCAL_INSTABILITY_CERTIFICATE',
            'base_run':241,'pulse_ticks':len(SHAPE),'alpha':str(alpha),'beta':str(beta),
            'determinant':str(det),'determinant_minus_one':str(det-1),
            'modes':modes,
            'conclusion':'Noiseless disturbance-free repeated fixed n-zero-ticks plus Run241 pulse is locally unstable at hover; not a stabilizing terminal backup',
            'scope':'Frozen four-state Euler, fixed thrust, true angle and rate zero at each macrocycle boundary, noiseless success measurement y=p, zero process residual; fixed n in {5,10,15}',
            'nonlinear_justification':'The exact sine map is C1 and has this Jacobian at hover; an eigenvalue outside the unit disk implies local instability of the fixed point',
            'recursive_invariance_ruled_out':False,
            'arbitrary_causal_controller_ruled_out':False,
            'smf_mpc_closed_loop_certified':False,
            'gate_A':'blocked_for_output_feedback_SMF_MPC',
            'limitations':['Only this unmodified repeated fixed macrocycle, not arbitrary switching/measurement-conditioned strategies',
                           'Local instability does not rule out a bounded non-attractive invariant set',
                           'Disturbances/noise set to zero only for a valid necessary stability test',
                           'No general SMF posterior, MPC optimizer, terminal set, or six-state certificate']}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--root',type=Path)
    p.add_argument('--output',type=Path)
    a=p.parse_args()
    result=json.dumps(verify(a.root),indent=2,sort_keys=True,ensure_ascii=False)+'\n'
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(result)
    else: print(result,end='')

if __name__=='__main__': main()
