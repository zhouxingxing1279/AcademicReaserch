#!/usr/bin/env python3
"""Run249: finite-deadline sound interval SMF + guarded receding horizon MPC.

Fixed thrust four-state Euler only. Exact rational, outward-grid-rounded set
propagation; bounded sensor strip intersection. This proves safety up to the
fixed absolute deadline under all legal bounded disturbances/measurement paths,
NOT infinite-time recursive feasibility or an invariant terminal set.
"""
from __future__ import annotations
import argparse, itertools, json, math, sys, time
from fractions import Fraction as F
from pathlib import Path

H=J=F(1,50); T=F(981,100); R=F(3246383,1600000)
U=F(2,25); P_MAX=F(5); V_MAX=F(3); PHI_MAX=F(9,20); OMEGA_MAX=F(2)
NOISE={'p':F(1,50),'phi':F(1,200),'omega':F(1,100)}
INIT={'p':(F(-1,50),F(1,50)),'v':(F(-1,10),F(1,10)),
      'phi':(F(-1,200),F(1,200)),'omega':(F(-1,100),F(1,100))}
GRID=10**10
DEADLINE=55
ACTIONS=(F(-1,25),F(0),F(1,25)) # +/-0.04 Nm
KEYS=('p','v','phi','omega')


def down(x):
    return F((x.numerator*GRID)//x.denominator,GRID)
def up(x):
    return -down(-x)
def bound(lo,hi):
    return (down(lo),up(hi))
def sin_bounds(x):
    assert abs(x)<=PHI_MAX
    if x<0:
        lo,hi=sin_bounds(-x)
        return -hi,-lo
    lo=x-x**3/6
    hi=lo+x**5/120
    return lo,hi

def step(s,tau):
    assert -U<=tau<=U
    p,v,phi,omega=(s[k] for k in KEYS)
    assert -PHI_MAX<=phi[0]<=phi[1]<=PHI_MAX
    sinlo=sin_bounds(phi[0])[0];sinhi=sin_bounds(phi[1])[1]
    return {'p':bound(p[0]+H*v[0],p[1]+H*v[1]),
            'v':bound(v[0]+H*(-T*sinhi-R),v[1]+H*(-T*sinlo+R)),
            'phi':bound(phi[0]+H*omega[0],phi[1]+H*omega[1]),
            'omega':bound(omega[0]+H/J*tau,omega[1]+H/J*tau)}

def safe(s):
    return all(-lim<=s[k][0]<=s[k][1]<=lim for k,lim in
               [('p',P_MAX),('v',V_MAX),('phi',PHI_MAX),('omega',OMEGA_MAX)])

def rollout(s,actions):
    out=dict(s)
    if not safe(out):return None
    for tau in actions:
        out=step(out,tau)
        if not safe(out):return None
    return out

def strip(s,obs):
    """Only noise-consistent observations produce a nonempty posterior."""
    out=dict(s)
    for k,y in obs.items():
        assert k in NOISE
        lo=max(out[k][0],y-NOISE[k]);hi=min(out[k][1],y+NOISE[k])
        if lo>hi:return None
        out[k]=(lo,hi)
    return out

def safety_first_actions(s,k,deadline=DEADLINE):
    """For each first input, certify that zero torque can finish the deadline.

    This first+zero-tail contract is the induction witness: after executing the
    first input, every valid measurement posterior is a subset of its predicted
    set, so zero remains a feasible fallback at the next tick.
    """
    assert 0<=k<deadline and safe(s)
    accepted={}
    for a in ACTIONS:
        next_s=step(s,a)
        tail=rollout(next_s,(F(0),)*(deadline-k-1)) if safe(next_s) else None
        if tail is not None:accepted[a]=(next_s,tail)
    return accepted

def nominal_plan_cost(s,plan):
    """Three-step grid MPC nominal objective; not a robust terminal cost."""
    p,v,phi,omega=(float(sum(s[k])/2) for k in KEYS)
    for tau in list(plan)+[F(0)]*5:
        p,v,phi,omega=(p+float(H)*v,
                         v+float(H)*(-float(T)*math.sin(phi)),
                         phi+float(H)*omega,
                         omega+float(H/J*tau))
    return 1.0*p*p+1.5*v*v+0.15*phi*phi+0.1*omega*omega+0.002*sum(float(a*a) for a in plan)

def choose(s,k,deadline=DEADLINE):
    accepted=safety_first_actions(s,k,deadline)
    if not accepted:raise RuntimeError('finite-deadline safety contract infeasible')
    plans=[]
    n=min(3,deadline-k)
    for plan in itertools.product(ACTIONS,repeat=n):
        if plan[0] not in accepted:continue
        # MPC local robust rollout for all 3 planned actions (not the tail contract)
        if rollout(s,plan) is None:continue
        plans.append((nominal_plan_cost(s,plan),tuple(abs(x) for x in plan),plan))
    assert plans
    cost,_,best=min(plans)
    return best[0],len(accepted),cost

def zero_certificate(deadline=DEADLINE):
    s=dict(INIT);bounds=[dict(s)]
    for k in range(deadline):
        s=step(s,F(0))
        assert safe(s),(k+1,s)
        bounds.append(dict(s))
    return bounds

def all_words(n):
    words=[('',0)]
    for _ in range(n):
        nxt=[]
        for word,miss in words:
            nxt.append((word+'S',0))
            if miss<2:nxt.append((word+'M',miss+1))
        words=nxt
    return [x for x,_ in words]

def replay(word,initial,r_sign=1,policy='mpc',deadline=DEADLINE):
    assert word in all_words(deadline//5)
    x=[float(initial[k]) for k in KEYS]
    s=dict(INIT);rms=0;maxv=0;viol=0;contained=0;nonzero=0;fallback=0;time_ns=0
    for k in range(deadline):
        if policy=='mpc':
            start=time.perf_counter_ns();a,choices,cost=choose(s,k,deadline)
            time_ns+=time.perf_counter_ns()-start
            fallback+=(choices==1)
        else:a=F(0)
        nonzero+=a!=0
        r=float(R)*r_sign*(1 if (k//7)%2==0 else -1)
        p,v,phi,omega=x
        x=[p+float(H)*v,v+float(H)*(-float(T)*math.sin(phi)+r),
           phi+float(H)*omega,omega+float(H/J*a)]
        predicted=step(s,a)
        obs={'phi':F(str(x[2]))+NOISE['phi']/2,'omega':F(str(x[3]))-NOISE['omega']/2}
        if (k+1)%5==0 and word[(k+1)//5-1]=='S':
            obs['p']=F(str(x[0]))+NOISE['p']/2
        s=strip(predicted,obs)
        if s is None:raise AssertionError(('inconsistent measurement',k))
        for j,key in enumerate(KEYS):
            lo,hi=s[key]
            assert float(lo)-1e-8<=x[j]<=float(hi)+1e-8,(k,key,x[j],lo,hi)
            contained+=1
        viol+=not safe(s)
        maxv=max(maxv,abs(x[1]));rms+=x[0]**2
    return {'pattern':word,'policy':policy,'r_sign':r_sign,'rmse_p':math.sqrt(rms/deadline),
            'max_abs_v':maxv,'violations':viol,'contained':contained,'nonzero_actions':nonzero,
            'only_one_safe_action_ticks':fallback,'avg_solver_ms':time_ns/1e6/deadline}

def verify(root=None):
    if root is not None:
        cfg=json.loads((Path(root)/'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics']=='defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s']))==H
        assert F(str(cfg['plant']['inertia_kg_m2']))==J
        assert F(str(cfg['plant']['gravity_m_s2']))==T
        assert F(str(cfg['domain']['input_upper'][1]))==U
        assert F(str(cfg['domain']['state_upper'][0]))==P_MAX
        assert F(str(cfg['domain']['state_upper'][2]))==V_MAX
        assert F(str(cfg['domain']['state_upper'][4]))==PHI_MAX
        assert F(str(cfg['domain']['state_upper'][5]))==OMEGA_MAX
        assert cfg['sensing']['position_period_ticks']==5
        assert cfg['sensing']['max_consecutive_missed_packets']==2
        for k,i in [('p',0),('v',2),('phi',4),('omega',5)]:
            c=F(str(cfg['initial_set']['center'][i]));w=F(str(cfg['initial_set']['halfwidth'][i]));assert INIT[k]==(c-w,c+w)
    assert R==F(3246383,1600000)
    assert all_words(3)==['SSS','SSM','SMS','SMM','MSS','MSM','MMS'] or len(all_words(3))==7
    baseline=zero_certificate()
    assert len(baseline)==DEADLINE+1
    worst={k:str(max(max(abs(row[k][0]),abs(row[k][1])) for row in baseline)) for k in KEYS}
    assert all(safe(row) for row in baseline)
    # Formal inductive property: monotonicity of step and strip. All k and
    # all posterior subsets of the predicted interval inherit the certified
    # zero-tail rollout after each accepted action. This is a finite deadline,
    # not an infinite-time recursive invariant.
    zero_candidates=safety_first_actions(dict(INIT),0)
    assert F(0) in zero_candidates
    words=['S'*11,'SMM'*3+'SS','MMS'*3+'MM']
    assert all(w in all_words(11) for w in words)
    initial=[{'p':F(0),'v':F(0),'phi':F(0),'omega':F(0)},
             {'p':F(-1,50),'v':F(-1,10),'phi':F(1,200),'omega':F(1,100)}]
    runs=[]
    for w,init,sgn in itertools.product(words,initial,(-1,1)):
        runs.append(replay(w,init,sgn,'mpc'))
        runs.append(replay(w,init,sgn,'zero'))
    mpc=[r for r in runs if r['policy']=='mpc'];base=[r for r in runs if r['policy']=='zero']
    return {'run':249,'evidence':'EXACT_OUTWARD_RATIONAL_FINITE_DEADLINE_GUARDED_OUTPUT_FEEDBACK_SIMULATION',
            'deadline_ticks':DEADLINE,'deadline_s':str(DEADLINE*H),
            'model':'frozen four-state Euler, fixed T, bounded independent lateral residual',
            'safe_zero_backup_all_initial_box':True,
            'zero_backup_max_abs':worst,
            'first_tick_safe_action_count':len(zero_candidates),
            'smf_update':'prediction, always observed noisy angle/rate, success-only noisy position; interval overapprox',
            'controller':'3-step grid MPC nominal objective; robust first-action+zero-tail safety filter',
            'safety_claim':'all initial states, all bounded residuals and noise-consistent observations and legal dropout words, up to fixed deadline; mathematical induction, not sampled trajectories',
            'safety_proof_level':'finite-deadline conditional on model and sound outward rounding',
            'replay_episodes':len(runs),'replay_total_steps':len(runs)*DEADLINE,
            'replay_smf_contained_components':sum(r['contained'] for r in runs),
            'replay_violations':sum(r['violations'] for r in runs),
            'mpc_nonzero_actions':sum(r['nonzero_actions'] for r in mpc),
            'mpc_mean_rmse_p':sum(r['rmse_p'] for r in mpc)/len(mpc),
            'zero_mean_rmse_p':sum(r['rmse_p'] for r in base)/len(base),
            'timing_measurement':'wallclock measured separately; not included in deterministic rational/simulation certificate',
            'worst_replay_max_abs_v':max(r['max_abs_v'] for r in runs),
            'general_smf_cz_recursive_mpc':False,'terminal_invariant_set':False,
            'six_state_guarantee':False,'wcet_20ms':False,'gate_A':'blocked'}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path);ap.add_argument('--output',type=Path);a=ap.parse_args()
    obj=verify(a.root);s=json.dumps(obj,sort_keys=True,indent=2,ensure_ascii=False)+'\n'
    if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(s)
    else:print(s,end='')
if __name__=='__main__':main()
