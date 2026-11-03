"""Run211 finite-horizon nominal MPC search inside exact Run208/210 first-action admissibility.

Open-loop candidate sequences are scored ONLY for performance, using a frozen
current-thrust nominal plant. Their future safety is NOT certified. The applied
first torque is independently certified by Run208's exact backup and Run210's
necessary braking guard. No terminal RCI or recursive-feasibility claim.
"""
from __future__ import annotations
import itertools
import time
from fractions import Fraction as Q
import check_reachable_smf_backup_rollout as m
import check_attitude_viability_guard as g
import check_two_stage_causal_backup as prior
Z=Q(0)

def interval(box,t,horizon=8):
 c=prior.two_stage_audit(box,t)
 if not c['feasible']:return None,'two_stage_refusal'
 gl,gh=g.guard_interval(box,horizon)
 lo=max(Q(c['lower']),gl);hi=min(Q(c['upper']),gh)
 return ((lo,hi),None) if lo<=hi else (None,'necessary_viability_guard_refusal')

def nominal_score(x,t,first,second,third,weights=(2,10,2,1),terminal=4,effort=0.02):
 """8-step nominal cost with piecewise-constant future torque blocks."""
 p,v,phi,om=map(float,x);T=float(t);h=float(m.H);J=float(m.J)
 torques=[float(first)]+[float(second)]*3+[float(third)]*4
 cost=0.
 for k,u in enumerate(torques):
  p,v,phi,om=p+h*v,v-h*T*phi,phi+h*om,om+h*u/J
  if any(abs(z)>float(lim)+1e-12 for z,lim in zip((p,v,phi,om),m.LIMITS)):
   return float("inf")
  stage=sum(w*(z/lim)**2 for w,z,lim in zip(weights,(p,v,phi,om),map(float,m.LIMITS)))
  cost+=(terminal if k==7 else 1)*stage+effort*(u/float(m.UMAX))**2
 return cost

def select(box,t,grid=7,weights=(2,10,2,1),terminal=4,effort=0.02):
 allowed,reason=interval(box,t)
 if allowed is None:return None,{'reason':reason}
 lo,hi=allowed
 anchor=max(lo,min(hi,m.proposed(box)-Q(1,5)*m.mid(box[3])))
 firsts=sorted({anchor}|{max(lo,min(hi,Q(round(float(lo+(hi-lo)*Q(i,grid-1))*10000),10000))) for i in range(grid)})
 center=tuple(m.mid(z) for z in box)
 best=None
 for u0 in firsts:
  for u1,u2 in itertools.product((-m.UMAX,Z,m.UMAX),repeat=2):
   cost=nominal_score(center,t,u0,u1,u2,weights,terminal,effort)
   # Tie-breaking favors baseline to avoid spurious changes in flat objectives.
   key=(cost,float(abs(u0-anchor)),float(u0),float(u1),float(u2))
   if best is None or key<best[0]:best=(key,u0,u1,u2)
 if best[0][0]==float("inf"):
  # No nominally feasible 8-step plan in this finite grid. Never treat
  # this as robust infeasibility; revert to the independently certified anchor.
  u0,u1,u2=anchor,Z,Z
  nominal_feasible=False
 else:
  _,u0,u1,u2=best
  nominal_feasible=True
 assert lo<=u0<=hi
 return u0,{'reason':'admitted','intervened':u0!=anchor,'first_candidates':len(firsts),
            'total_plans':len(firsts)*9,'nominal_cost':None if not nominal_feasible else best[0][0],
            'nominal_plan_feasible':nominal_feasible,
            'planned_u1':float(u1),'planned_u2':float(u2),'anchor':str(anchor)}

def rollout(scenario,steps=200,optimized=True,grid=7,weights=(2,10,2,1),terminal=4,effort=0.02):
 x=(Z,)*4;box=m.initial_box();prev_p=box[0];accels=[]
 accepted=0;first_refusal=None;interventions=0;maxstate=[Z]*4
 decision=0.;trace=[];sum_p2=0.;sum_v2=0.;max_halfwidth=[Z]*4
 nominal_infeasible=0;success_packets=0;position_unobserved=0
 for k in range(steps):
  assert all(lo<=v<=hi for (lo,hi),v in zip(box,x))
  t=m.thrust(scenario,k);start=time.perf_counter()
  if optimized:u,meta=select(box,t,grid,weights,terminal,effort)
  else:
   allowed,reason=interval(box,t)
   if allowed is None:u=None;meta={'reason':reason}
   else:
    u=max(allowed[0],min(allowed[1],m.proposed(box)-Q(1,5)*m.mid(box[3])))
    meta={'reason':'admitted','intervened':False}
  decision+=time.perf_counter()-start
  if u is None:first_refusal={'tick':k+1,'reason':meta['reason']};break
  interventions+=meta['intervened']
  nominal_infeasible+=meta.get('nominal_plan_feasible') is False
  if k+1 in (1,30,60,90,120,150,180,190,191,192,193,200):
   trace.append({'tick':k+1,'state':list(map(float,x)),'torque':float(u),
                 'nominal_cost':meta.get('nominal_cost')})
  old_phi=box[2]
  accels.append(m.add(m.scale(old_phi,-t),(-m.rad(t),m.rad(t))))
  x=m.step(x,t,u,m.residual(scenario,k,t));box=m.predict(box,t,u)
  packet=(k+1)%15==0
  box=m.observe(box,x,packet,m.measurement_noise(scenario,k))
  if packet:
   box=(box[0],m.intersect(box[1],m.velocity_from_packets(prev_p,box[0],accels)),box[2],box[3]);prev_p=box[0];accels=[]
  success_packets+=packet;position_unobserved+=not packet
  assert all(lo<=v<=hi for (lo,hi),v in zip(box,x))
  assert all(abs(v)<=lim for v,lim in zip(x,m.LIMITS))
  accepted+=1;sum_p2+=float(x[0])**2;sum_v2+=float(x[1])**2
  for i,v in enumerate(x):
   maxstate[i]=max(maxstate[i],abs(v))
   max_halfwidth[i]=max(max_halfwidth[i],(box[i][1]-box[i][0])/2)
 return {'accepted_ticks':accepted,'first_refusal':first_refusal,
         'interventions':interventions,'max_abs_state':list(map(float,maxstate)),
         'rms_position_m':(sum_p2/accepted)**0.5 if accepted else None,
         'rms_velocity_m_s':(sum_v2/accepted)**0.5 if accepted else None,
         'max_posterior_halfwidth':list(map(float,max_halfwidth)),
         'successful_position_packets':success_packets,'position_unobserved_ticks':position_unobserved,
         'containment_checks_passed':4*accepted,'observed_hard_violations':0,
         'nominal_grid_infeasible_ticks':nominal_infeasible,
         'mean_decision_ms':round(1000*decision/(accepted+(first_refusal is not None)),3) if accepted or first_refusal else None,
         'decision_wall_seconds':round(decision,4),'trace':trace}

def capture_baseline_refusal(scenario='positive_high',steps=200):
    """Replay the Run210 controller and return the first refused *outer box*."""
    x=(Z,)*4;box=m.initial_box();prev_p=box[0];accels=[]
    for k in range(steps):
        t=m.thrust(scenario,k);allowed,reason=interval(box,t)
        if allowed is None:return k+1,box,x,reason
        u=max(allowed[0],min(allowed[1],m.proposed(box)-Q(1,5)*m.mid(box[3])))
        old_phi=box[2]
        accels.append(m.add(m.scale(old_phi,-t),(-m.rad(t),m.rad(t))))
        x=m.step(x,t,u,m.residual(scenario,k,t));box=m.predict(box,t,u)
        packet=(k+1)%15==0
        box=m.observe(box,x,packet,m.measurement_noise(scenario,k))
        if packet:
            box=(box[0],m.intersect(box[1],m.velocity_from_packets(prev_p,box[0],accels)),box[2],box[3])
            prev_p=box[0];accels=[]
        assert all(lo<=v<=hi for (lo,hi),v in zip(box,x))
    return None,box,x,None

def refusal_box_witness():
    """Exact counterexample for the box-reset certificate, NOT plant viability.

    A joint endpoint of an outer box may be unreachable under past measurement
    history. For that endpoint and the legal fixed TMAX, r=-rad(TMAX) history,
    u=-UMAX at every step maximizes future velocity over all torque sequences.
    """
    tick,box,truth,reason=capture_baseline_refusal()
    assert tick==192 and reason=='two_stage_refusal'
    corner=(box[0][0],box[1][0],box[2][1],box[3][1])
    s=corner;vel=[]
    for _ in range(5):
        s=m.step(s,m.TMAX,-m.UMAX,-m.rad(m.TMAX))
        vel.append(s[1])
    assert vel[-1]<-m.LIMITS[1]
    return {'tick':tick,'outer_box_corner':list(map(str,corner)),
            'actual_state_approx':list(map(float,truth)),
            'corner_velocity_5_steps_max_under_fixed_adverse_history':str(vel[-1]),
            'corner_velocity_5_steps_approx':float(vel[-1]),
            'velocity_limit_lower':str(-m.LIMITS[1]),
            'excess_approx':float(-m.LIMITS[1]-vel[-1]),
            'interpretation':'outer_box_certificate obstruction; joint corner NOT verified reachable'}

def run(steps=200,grid=7,weights=(2,10,2,1),terminal=4,effort=0.02):
    rows=[]
    for s in ('positive_high','alternating_high','switch_positive'):
        rows.append({'scenario':s,
                     'run210_baseline':rollout(s,steps,False,grid,weights,terminal,effort),
                     'nominal_8step_candidate_mpc':rollout(s,steps,True,grid,weights,terminal,effort)})
    common=[]
    if steps>=80:
        for s in ('positive_high','alternating_high','switch_positive'):
            common.append({'scenario':s,'prefix_ticks':80,
                           'baseline':rollout(s,80,False,grid,weights,terminal,effort),
                           'optimized':rollout(s,80,True,grid,weights,terminal,effort)})
    return {'run':'211','common_prefix_80':common,'scope':'four-state Euler proxy; exact first-action admission; deterministic reachable histories',
            'evidence':'NEGATIVE_FINITE_CANDIDATE_NOMINAL_MPC_PLUS_EXACT_OUTER_BOX_OBSTRUCTION',
            'candidate_first_grid':grid,'candidate_future_blocks':9,
            'nominal_prediction_steps':8,'weights':weights,'terminal_multiplier':terminal,
            'effort_weight':effort,'rows':rows,'refusal_box_witness':refusal_box_witness(),
            'gate_A':'blocked','limitations':[
                'Only first torque passes Run208 exact finite backup and Run210 necessary guard',
                'Open-loop nominal future plan is not robustly feasible or executed',
                'No terminal invariant set, recursive feasibility or stability guarantee',
                'The box corner may be inconsistent with the complete observation history',
                'Candidate grid is not a continuous optimum; floating scores never certify safety',
                'Deterministic traces do not cover all disturbances, noise and thrust schedules']}

def main():
    import argparse,json
    from pathlib import Path
    p=argparse.ArgumentParser()
    p.add_argument('--steps',type=int,default=200)
    p.add_argument('--output',type=Path)
    a=p.parse_args()
    data=json.dumps(run(a.steps),indent=2,ensure_ascii=False)+'\n'
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(data)
    else:print(data,end='')
if __name__=='__main__':main()
