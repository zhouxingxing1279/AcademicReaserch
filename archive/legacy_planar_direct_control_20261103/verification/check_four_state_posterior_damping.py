#!/usr/bin/env python3
"""Run243: causal two-packet velocity interval and fixed-mode damping pulse.

Proof scope: frozen lateral four-state Euler, fixed thrust, known initial
attitude (phi,omega)=(0,0) and exact commanded torque history. Schur tests
are for noiseless, disturbance-free, *unsaturated* local linearization.
No general SMF/MPC/RCI certificate is claimed.
"""
from __future__ import annotations
import argparse
import json
import math
from fractions import Fraction as F
from pathlib import Path

H = J = F(1,50)
T = F(981,100)
R = F(47,25) + F(243,16000)*T
NOISE = F(1,50)
TAU_MAX = F(2,25)
A = B = F(1,2)  # Nm/m and Nm/(m/s), respectively
SHAPE = (1,)*3 + (-1,)*6 + (1,)*3 + (0,)*3
MODES = (5,10,15)
PULSE = len(SHAPE)


def response_per_unit():
    """Exact Euler attitude sequence for tau_j=u*SHAPE[j], u=1."""
    phi=omega=F(0)
    angles=[]; rates=[]
    for s in SHAPE:
        angles.append(phi); rates.append(omega)
        phi,omega=phi+H*omega,omega+(H/J)*s
    assert phi==omega==0
    return angles,rates


def response_coefficients():
    angles,_=response_per_unit()
    alpha=H*T*sum(angles,F(0))
    beta=H*H*T*sum(((PULSE-1-j)*angles[j] for j in range(PULSE)),F(0))
    return alpha,beta


def macro_jacobian(n):
    """Map from just after previous pulse to just after next pulse.

    n free steps; at successful packet use u=A*p_n+B*v_n;
    pulse starts immediately after packet, no future observation is read.
    """
    if n not in MODES: raise ValueError('unsupported mode')
    al,be=response_coefficients()
    l=PULSE*H
    # Bpulse=[[1-be*A,l-be*B],[-al*A,1-al*B]], Pn=[[1,n*H],[0,1]]
    return ((1-be*A,(1-be*A)*n*H+l-be*B),
            (-al*A,1-al*B-al*A*n*H))


def det2(m):return m[0][0]*m[1][1]-m[0][1]*m[1][0]
def tr2(m):return m[0][0]+m[1][1]


def jury(n):
    m=macro_jacobian(n);d=det2(m);t=tr2(m)
    return (1-d,1-t+d,1+t+d)


def velocity_radius(total_ticks):
    """Exact halfwidth for the two-packet reconstructed *current* velocity.

    y_N-y_0 is noisy; a_j is the known attitude acceleration, and r_j is
    an arbitrary independent residual in [-R,R]. The exact error is
    H/N*sum_{j=0}^{N-1}(j+1)*r_j+(eta_0-eta_N)/(N*H).
    """
    if not isinstance(total_ticks,int) or total_ticks<1:
        raise ValueError('positive integer packet gap required')
    N=total_ticks
    return H*R*F(N+1,2)+2*NOISE/(N*H)


def reconstruct_velocity(y_old,y_new,accelerations):
    """Center of the rigorous velocity interval, given known a_j sequence.

    Fraction inputs permit exact algebra. The same function works for
    real floating accelerations in a numerical trajectory, but only the
    Fraction certificate is an exact proof.
    """
    N=len(accelerations)
    if N==0: raise ValueError('empty observation gap')
    dp=H*H*sum(((N-1-j)*accelerations[j] for j in range(N)),F(0))
    dv=H*sum(accelerations,F(0))
    return (y_new-y_old-dp)/(N*H)+dv


def known_accelerations(pulse_amplitude,n):
    """Actual deterministic -T*sin(phi) for a pulse then n free steps.

    Float values are for numerical sanity checks; they are NOT used in the
    exact Schur/SMF-radius certificate.
    """
    if n not in MODES:raise ValueError('unsupported mode')
    phi=omega=0.0; arr=[]
    for s in SHAPE+(0,)*n:
        arr.append(-float(T)*math.sin(phi))
        phi,omega=phi+float(H)*omega,omega+float(H/J)*float(pulse_amplitude)*s
    assert abs(phi)<1e-12 and abs(omega)<1e-12
    return arr


def simulate_zero_noise(modes=(5,10,15)*25,p0=0.01,v0=0.05):
    """End-to-end *deterministic* causal two-packet closed-loop sanity run.

    First two packets are 5 ticks apart, with zero torque (warm-up).
    Subsequent pulses use only current position and reconstructed velocity;
    each next packet arrives after the pulse and n free steps. No MPC.
    """
    h=float(H); t=float(T)
    p=float(p0);v=float(v0);phi=omega=0.0
    y_prev=p
    # Initial passive interval, so first velocity is inferred, not given.
    for _ in range(5):p+=h*v
    y=p
    vhat=(y-y_prev)/(5*h)
    assert abs(vhat-v)<1e-12
    max_torque=0.0;max_p=abs(p);max_v=abs(v);max_phi=0.0;max_omega=0.0
    errors=[]; last_amp=0.0
    for n in modes:
        raw=float(A)*y+float(B)*vhat
        u=max(-float(TAU_MAX),min(float(TAU_MAX),raw))
        max_torque=max(max_torque,abs(u));last_amp=u
        old_y=y;acc=[];phip=omegap=0.0
        for s in SHAPE+(0,)*n:
            # Independent predictor uses ONLY known previous reset and applied u.
            acc.append(-t*math.sin(phip))
            aa=-t*math.sin(phi)
            p,v,phi,omega=p+h*v,v+h*aa,phi+h*omega,omega+u*s
            phip,omegap=phip+h*omegap,omegap+u*s
            max_p=max(max_p,abs(p));max_v=max(max_v,abs(v))
            max_phi=max(max_phi,abs(phi));max_omega=max(max_omega,abs(omega))
        assert abs(phip-phi)<1e-12 and abs(omegap-omega)<1e-12
        assert abs(phi)<1e-10 and abs(omega)<1e-10
        y=p
        # Same actual known attitude acceleration history; no hidden v read.
        vhat=float(reconstruct_velocity(old_y,y,acc))
        errors.append(abs(vhat-v))
    return {'cycles':len(modes),'final_p':p,'final_v':v,'max_torque':max_torque,
            'max_p':max_p,'max_v':max_v,'max_phi':max_phi,
            'max_omega':max_omega,'max_velocity_reconstruction_error':max(errors,default=0.0),
            'last_amplitude':last_amp,'zero_noise_zero_disturbance_only':True}


def verify(root=None):
    if root is not None:
        cfg=json.loads((Path(root)/'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics']=='defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s']))==H
        assert F(str(cfg['plant']['inertia_kg_m2']))==J
        assert F(str(cfg['plant']['gravity_m_s2']))==T
        assert F(str(cfg['sensing']['observed_noise_halfwidth']['px']))==NOISE
        assert cfg['sensing']['position_period_ticks']==5
        assert cfg['sensing']['max_consecutive_missed_packets']==2
        assert cfg['sensing']['position_indices']==[0,1]
        assert cfg['sensing']['always_observed_indices']==[4,5]
        assert F(str(cfg['domain']['input_upper'][1]))==TAU_MAX
        assert F(str(cfg['domain']['input_lower'][1]))==-TAU_MAX
    al,be=response_coefficients()
    assert al==F(26487,125000) and be==F(79461,2500000)
    assert PULSE*H*al==2*be
    assert max(abs(x) for x in response_per_unit()[0])==F(9,50)
    # At macro start |p|<=0.02, |v|<=0.1 and no disturbance during n free ticks,
    # |u|<=0.5*(0.02+0.3*0.1)+0.5*0.1=0.075<0.08.
    local_u=A*(F(1,50)+max(MODES)*H*F(1,10))+B*F(1,10)
    assert local_u==F(3,40)<TAU_MAX
    angles,rates=response_per_unit()
    local_phi=local_u*max(abs(x) for x in angles)
    local_omega=local_u*max(abs(x) for x in rates)
    local_v=F(1,10)+H*T*local_u*sum((abs(x) for x in angles),F(0))
    local_p=F(1,50)+(max(MODES)+PULSE)*H*local_v
    assert local_p<F(5) and local_v<F(3)
    assert local_phi<F(9,20) and local_omega<F(2)
    modes=[]
    for n in MODES:
        m=macro_jacobian(n);d=det2(m);t=tr2(m);j=jury(n)
        assert d==F(4549721,5000000)<1 and all(x>0 for x in j)
        modes.append({'free_ticks':n,'packet_gap_ticks':n+PULSE,
                      'jacobian':[[str(v) for v in row] for row in m],
                      'trace':str(t),'determinant':str(d),
                      'jury_margins':[str(x) for x in j],
                      'velocity_interval_halfwidth_m_s':str(velocity_radius(n+PULSE)),
                      'fixed_mode_schur_certified':True})
    sim=simulate_zero_noise()
    assert sim['max_torque']<=float(TAU_MAX)
    assert sim['max_velocity_reconstruction_error']<1e-10
    return {'run':243,'evidence':'EXACT_RATIONAL_FIXED_MODE_JURY_AND_TWO_PACKET_VELOCITY_INTERVAL',
            'base_run':242,'scope':'Frozen four-state Euler lateral channel, fixed T, exactly known initial zero attitude and applied torque; successful noisy position packets separated by 20/25/30 ticks',
            'pulse_shape':list(SHAPE),'position_gain':str(A),'velocity_gain':str(B),
            'alpha_per_unit_torque':str(al),'beta_per_unit_torque':str(be),
            'local_macro_start_p_abs_m':str(F(1,50)),
            'local_macro_start_v_abs_m_s':str(F(1,10)),
            'local_unsaturated_torque_bound_Nm':str(local_u),
            'local_one_macro_state_bounds':{'p_m':str(local_p),'v_m_s':str(local_v),
                                            'phi_rad':str(local_phi),'omega_rad_s':str(local_omega)},
            'modes':modes,
            'velocity_interval_derivation':'v_N-vhat_N=H/N*sum((j+1)*r_j)+(eta_old-eta_new)/(N*H); |r_j|<=R, |eta|<=NOISE',
            'residual_halfwidth_m_s2':str(R),
            'packet_noise_halfwidth_m':str(NOISE),
            'zero_noise_deterministic_simulation':sim,
            'fixed_mode_local_schur_certified':True,
            'arbitrary_switching_schur_certified':False,
            'robust_input_and_state_invariance_certified':False,
            'full_smf_mpc_closed_loop_certified':False,
            'gate_A':'blocked_for_output_feedback_SMF_MPC',
            'limitations':['Schur applies to no-noise/no-disturbance unsaturated local dynamics only; not robust safety',
                           'Two-packet velocity interval assumes exact known attitude history from a zero attitude reset; real noisy angle sensing not handled',
                           'No common Lyapunov certificate for arbitrary 5/10/15 mode switching',
                           'Worst-case two-packet velocity halfwidth can be much larger than admissible local unsaturated feedback range',
                           'Simulation is deterministic sanity evidence only; no general SMF posterior, online MPC, recursive terminal set, six-state proof or 20ms worst-case bound']}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--root',type=Path)
    p.add_argument('--output',type=Path)
    a=p.parse_args()
    s=json.dumps(verify(a.root),indent=2,sort_keys=True,ensure_ascii=False)+'\n'
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True)
        a.output.write_text(s)
    else:print(s,end='')

if __name__=='__main__':main()
