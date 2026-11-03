"""Run213: exact three-packet support integrated into causal backup at reachable tick 192.

All safety decisions use Fraction. The result is a one-dimensional historical
OUTER refinement, not a CZ posterior or a recursive-feasibility certificate.
"""
from __future__ import annotations
import argparse
import json
import time
from fractions import Fraction as Q
from pathlib import Path
import check_reachable_smf_backup_rollout as m
import check_nominal_short_mpc as base
import check_two_stage_causal_backup as prior
import check_attitude_viability_guard as guard
import check_three_packet_velocity_support as support

Z=Q(0)

def replay_snapshot(return_tracker=False):
    """Replay exactly the Run210 positive_high baseline; collect legal observations."""
    x=(Z,)*4;box=m.initial_box();prev_p=box[0];accels=[]
    positions={};attitudes={};thrusts={}
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
            prev_p=box[0];accels=[]
        assert all(lo<=v<=hi for (lo,hi),v in zip(box,x))
    assert base.interval(box,m.TMAX)[0] is None
    interval=support.measurement_support([positions[i] for i in (150,165,180)],
                    [attitudes[i] for i in range(150,191)],
                    [thrusts[i] for i in range(150,191)])
    if return_tracker:return box,x,interval,prev_p,accels
    return box,x,interval

def evaluate(box,t):
    start=time.perf_counter()
    backup=prior.two_stage_audit(box,t)
    backup_seconds=time.perf_counter()-start
    g=guard.guard_interval(box,8)
    feasible=backup['feasible'] and max(Q(backup['lower']),g[0])<=min(Q(backup['upper']),g[1]) if backup['feasible'] else False
    return {'two_stage_feasible':backup['feasible'],
            'two_stage_reason':backup['reason'],
            'two_stage_interval':([backup['lower'],backup['upper']] if backup['feasible'] else None),
            'eight_tick_guard_interval':[str(g[0]),str(g[1])],
            'combined_admissible':feasible,
            'two_stage_wall_seconds':round(backup_seconds,6)}

def rollout_from_snapshot(steps=220,refine=True):
    """Counterfactual from same actual prefix, same feedback and observations.

    Only change is a history-consistent velocity intersection before tick 192.
    This is a deterministic numerical replay, not a robust all-histories proof.
    """
    box,x,historical,prev_p,accels=replay_snapshot(return_tracker=True)
    if refine:
        box=(box[0],m.intersect(box[1],historical),box[2],box[3])
    accepted=191;first_refusal=None;u192=None
    for k in range(191,steps):
        t=m.thrust('positive_high',k)
        allowed,reason=base.interval(box,t)
        if allowed is None:
            first_refusal={'tick':k+1,'reason':reason};break
        u=max(allowed[0],min(allowed[1],m.proposed(box)-Q(1,5)*m.mid(box[3])))
        if k==191:u192=u
        old_phi=box[2]
        accels.append(m.add(m.scale(old_phi,-t),(-m.rad(t),m.rad(t))))
        x=m.step(x,t,u,m.residual('positive_high',k,t))
        box=m.predict(box,t,u)
        packet=(k+1)%15==0
        box=m.observe(box,x,packet,m.measurement_noise('positive_high',k))
        if packet:
            box=(box[0],m.intersect(box[1],m.velocity_from_packets(prev_p,box[0],accels)),box[2],box[3])
            prev_p=box[0];accels=[]
        assert all(lo<=v<=hi for (lo,hi),v in zip(box,x))
        assert all(abs(v)<=lim for v,lim in zip(x,m.LIMITS))
        accepted+=1
    return {'accepted_ticks':accepted,'first_refusal':first_refusal,
            'selected_torque_tick192':str(u192) if u192 is not None else None,
            'checked_state_containment':True,'observed_hard_violations':0}

def run():
    box,truth,historical=replay_snapshot()
    tightened=m.intersect(box[1],historical)
    new_box=(box[0],tightened,box[2],box[3])
    assert tightened[0]>box[1][0]
    assert all(a<=v<=b for (a,b),v in zip(new_box,truth))
    old=evaluate(box,m.TMAX)
    new=evaluate(new_box,m.TMAX)
    baseline=rollout_from_snapshot(refine=False)
    refined=rollout_from_snapshot(refine=True)
    return {'run':213,'scenario':'positive_high','tick':192,
        'history':'position packets 150,165,180; attitude observations 150..190',
        'old_velocity_interval':list(map(str,box[1])),
        'historical_outer_interval':list(map(str,historical)),
        'intersected_velocity_interval':list(map(str,tightened)),
        'lower_improvement_exact':str(tightened[0]-box[1][0]),
        'truth_contained':True,
        'original_box_audit':old,'historical_refined_box_audit':new,
        'baseline_220_tick_rollout':baseline,'refined_220_tick_rollout':refined,
        'gate_A':'blocked',
        'evidence':'exact Fraction deterministic reachable replay and causal backup re-audit',
        'limitations':['Only a velocity interval intersection; no joint CZ posterior',
            'The backup resets all coordinates to an independent box',
            'The audit guarantees at most next-step finite backup if admitted, not recursive feasibility',
            'One deterministic reachable history; not all possible measurement histories']}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path)
    args=ap.parse_args();out=json.dumps(run(),indent=2,ensure_ascii=False)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(out)
    else:print(out,end='')
if __name__=='__main__':main()
