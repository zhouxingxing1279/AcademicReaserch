"""Matched-information comparisons, adaptive stress runs and 10k trajectory audit."""
import time
import numpy as np
from src.oit_mrpi.control import TubeMPC
from src.oit_mrpi.sets import ConstrainedZonotope as CZ


def matched_information(ctrl, out, csv):
    rng = np.random.default_rng(20261107); joint=ctrl.joint
    eta=np.zeros(4); innovations=[]; ds=[np.zeros(2)]; rows=[]; snapshots=[]
    for k in range(25):
        if k:
            noise=rng.uniform(-1,1,2)
            r=(joint.Hinnovation@eta+joint.noise_innovation@noise).item()
            eta=joint.F@eta+joint.D@noise
            innovations.append(r); ds.append(eta[2:].copy())
        for window in (1,3,6):
            sets={}; timings={}
            for method in rng.permutation(['fixed_RPI','known_d_slice','ordinary_zonotope','OIT_CZ']):
                tic=time.perf_counter()
                if method=='fixed_RPI': Z=joint.S
                elif method=='known_d_slice': Z=joint.initial(ds[-1])
                else: Z=joint.window(innovations,ds,window,ordinary=method=='ordinary_zonotope')
                # Same full six-step query workload, same generator cap 256.
                directions=np.vstack([ctrl.Qdir@np.linalg.matrix_power(joint.F,i) for i in range(7)])
                supp=Z.support_many(directions)
                opp=Z.support_many(-directions)
                timings[method]=time.perf_counter()-tic
                sets[method]=(Z,supp,opp)
            for method,(Z,supp,opp) in sets.items():
                width=(supp+opp)/2
                fixed=(sets['fixed_RPI'][1]+sets['fixed_RPI'][2])/2
                for i in range(7):
                    for j,label in enumerate(('position','velocity','position_negative','velocity_negative','input','input_negative')):
                        q=6*i+j
                        rows.append(dict(k=k,window=window,method=method,horizon=i,direction=label,
                            support=supp[q],halfwidth=width[q],fixed_halfwidth=fixed[q],
                            ratio_to_fixed=width[q]/fixed[q] if fixed[q]>1e-12 else None,
                            generators=Z.g,equalities=len(Z.beq),runtime=timings[method],
                            contained=Z.point_contains(eta) if i==0 and j==0 else None,
                            budget_ms_20=timings[method]<=.020,budget_ms_50=timings[method]<=.050,
                            budget_ms_100=timings[method]<=.100))
                if method=='OIT_CZ' and window==3:
                    snapshots.append(dict(k=k,eta=eta.copy(),d=ds[-1].copy(),innovation=innovations[-1] if k else None,
                                          posterior=Z.record()))
            # Same information ordinary outer approximation must include exact window.
            assert np.max(sets['OIT_CZ'][1]-sets['ordinary_zonotope'][1]) <= 2e-7
            assert np.max(sets['OIT_CZ'][1]-sets['fixed_RPI'][1]) <= 2e-7
    csv(out/'matched_information.csv',rows)
    return {'rows':rows,'snapshots':snapshots,
            'budget_scope':'post-hoc total-query workload screens, not hard realtime or end-to-end MPC latency',
            'generator_cap':256,'same_information_ordinary_baseline':'least-squares zonotope update, same history and generators; not best possible zonotope enclosure'}


def feasible_grid(ctrl, out, csv):
    joint=ctrl.joint; innovations=[0.]*8; ds=[np.zeros(2) for _ in range(9)]
    fixed,_,_=ctrl.margins(innovations,ds,False)
    adaptive,_,_=ctrl.margins(innovations,ds,True)
    known,_,_=ctrl.margins(innovations,ds,'known_d')
    # Frozen information slice: cost/feasible-region comparison changes z while d=0.
    # y history shifts with the known nominal trajectory, retaining zero innovations.
    ordinary=np.tile(ctrl.static,(ctrl.N+1,1))
    for i in range(ctrl.window):
        Z=joint.predict(joint.window(innovations,ds,ctrl.window-i,ordinary=True),i)
        ordinary[i]=np.minimum(Z.support_many(ctrl.Qdir),ctrl.static)
    rows=[]
    for p in np.linspace(-5,5,31):
        for v in np.linspace(-3,3,25):
            z=np.array([p,v])
            for method,margins in [('fixed_RPI',fixed),('known_d_only',known),('ordinary_zonotope',ordinary),('OIT_CZ_compatible',adaptive)]:
                tic=time.perf_counter(); seq,status,residual=ctrl.solve(z,margins)
                rows.append(dict(p=p,v=v,method=method,feasible=seq is not None,status=status,
                                 runtime_mpc=time.perf_counter()-tic,residual=residual,
                                 nominal_cost=ctrl.cost(z,seq) if seq is not None else None))
    csv(out/'feasible_grid.csv',rows)
    return rows


def adaptive_runs(ctrl,out,csv):
    rows=[]; snapshots=[]; failures=[]; summaries=[]
    initial_states=[(3.8,.0),(-3.8,0.),(1.5,1.),(-1.5,-1.)]
    for seed in range(12):
        rng=np.random.default_rng(20261200+seed)
        omega=rng.uniform(-1,1,(30,2))
        if seed==0: omega[:]=1.
        if seed==1: omega[:]=np.c_[(-1.)**np.arange(30),-(-1.)**np.arange(30)]
        for adaptive in (False,'known_d',True):
            method=('known_d_only' if adaptive=='known_d' else
                    'OIT_CZ_compatible' if adaptive else 'fixed_RPI')
            summary_method='known_d_only' if adaptive=='known_d' else 'adaptive' if adaptive else 'fixed'
            z=np.array(initial_states[seed%4]); hat=z.copy(); x=z.copy()
            innovations=[]; ds=[hat-z]; previous=None; casecost=0.; localfail=0
            for k in range(30):
                margin,tube,settime=ctrl.margins(innovations,ds,adaptive)
                tic=time.perf_counter(); seq,status,residual=ctrl.solve(z,margin)
                qptime=time.perf_counter()-tic
                if seq is None:
                    failures.append(dict(seed=seed,adaptive=adaptive,k=k,reason=status)); localfail+=1; break
                shift_violation=0.; support_shift=0.
                if previous is not None:
                    shift_violation=ctrl.feasible(z,previous['shift'],margin)[1]
                    support_shift=float(np.max(margin[:-1]-previous['margins'][1:]))
                    if shift_violation>2e-6 or support_shift>2e-7:
                        failures.append(dict(seed=seed,adaptive=adaptive,k=k,reason='shift',
                                             residual=shift_violation,support_shift=support_shift));localfail+=1
                eta=np.r_[x-hat,hat-z]
                contained=(tube[0] if adaptive else ctrl.joint.S).point_contains(eta)
                u=float(seq[0]+(ctrl.K@(hat-z)).item())
                violation=max(float(np.max(ctrl.Hx@x-ctrl.hx)),abs(u)-1)
                if not contained or violation>2e-6:
                    failures.append(dict(seed=seed,adaptive=adaptive,k=k,reason='containment_or_constraint',
                                         contained=contained,violation=violation));localfail+=1
                casecost+=float(x@x+.1*u*u)
                shifted=ctrl.shifted(z,seq)
                nextz=ctrl.sys.A@z+ctrl.sys.B.ravel()*seq[0]
                descent=ctrl.cost(nextz,shifted)-ctrl.cost(z,seq)+z@z+.1*seq[0]**2
                rows.append(dict(seed=seed,method=method,k=k,
                    p=x[0],velocity=x[1],p_nominal=z[0],v_nominal=z[1],u=u,
                    p_hat=hat[0],v_hat=hat[1],runtime_set=settime,runtime_mpc=qptime,
                    runtime_total=settime+qptime,solver=status,max_constraint_violation=violation,
                    shift_violation=shift_violation,support_shift=support_shift,descent=descent,
                    sample_contained=contained,current_position_margin=margin[0,0],
                    next_position_margin=margin[1,0],next_input_margin=margin[1,4]))
                snapshots.append(dict(seed=seed,method=summary_method,k=k,
                    x_true=x.copy(),x_nominal=z.copy(),hat_x=hat.copy(),u=u,
                    Xhat_definition='hat_x + projection_epsilon(posterior_joint_CZ)',
                    posterior_joint_CZ=tube[0].record() if adaptive else {'template':'fixed_joint_RPI'},
                    tube=[t.record() if i<ctrl.window else {'template':'fixed_joint_RPI'}
                          for i,t in enumerate(tube)] if adaptive else {'template':'fixed_joint_RPI'},
                    margins=margin.copy()))
                xp=ctrl.sys.A@x+ctrl.sys.B.ravel()*(u+.05*omega[k,0])
                predictor=ctrl.sys.A@hat+ctrl.sys.B.ravel()*u
                r=float((ctrl.sys.C@xp).item()+.1*omega[k,1]-(ctrl.sys.C@predictor).item())
                hp=predictor+ctrl.L.ravel()*r
                previous={'shift':shifted,'margins':margin}
                x,hat,z=xp,hp,nextz;innovations.append(r);ds.append(hat-z)
            summaries.append(dict(seed=seed,method=summary_method,cost=casecost,
                                  steps=k+1,failures=localfail))
        print('closedloop seed',seed,flush=True)
    csv(out/'closedloop_detailed.csv',rows);csv(out/'closedloop_summary.csv',summaries)
    return {'rows':rows,'snapshots':snapshots,'failures':failures,'summaries':summaries}


def monte_carlo_fast_branch(ctrl,out,trajectories=10000,steps=30):
    """10k fully simulated output-feedback trajectories with an exact MPC shortcut.

    When the unconstrained optimum is feasible under the fixed RPI envelope,
    it is also the optimum of the adaptive problem (its constraints are weaker).
    Therefore no QP/LP is needed on this branch. Otherwise the actual adaptive
    tube and QP are computed. Noise samples and initial states are never changed
    to make the shortcut pass. Missing explicit sets are serialized losslessly
    as the RPI template plus innovation/d history and the window algorithm.
    """
    rng=np.random.default_rng(20261108)
    initial=rng.uniform(-1,1,(trajectories,2))*[.8,.25]
    x=initial.copy();hat=initial.copy();z=initial.copy();eta=np.zeros((trajectories,4))
    xs=np.empty((trajectories,steps+1,2));zs=xs.copy();hats=xs.copy()
    inputs=np.empty((trajectories,steps));noiseall=rng.uniform(-1,1,(trajectories,steps,2))
    innovation_history=np.empty((trajectories,steps))
    xs[:,0]=x;zs[:,0]=z;hats[:,0]=hat
    static=np.tile(ctrl.static,(ctrl.N+1,1))
    b0=ctrl.bounds(np.zeros(2),static)
    bmap=np.vstack([np.zeros((2*ctrl.N,2)),ctrl.Xmap,ctrl.Tmap])
    feasibility_map=ctrl.constraint@ctrl.optmap+bmap
    failures=0;maxviolation=-np.inf;maxplan=-np.inf;maxshift=-np.inf;maxdynamics=0.
    shortcut_count=0; adaptive_solves=0; adaptive_tubes=0; previous_shift=None
    first_margins=None; branches=[]
    tic=time.perf_counter()
    for k in range(steps):
        plan_res=np.max(z@feasibility_map.T-b0,axis=1)
        initial_res=np.max(z@ctrl.Hx.T+ctrl.static[:4]-ctrl.hx,axis=1)
        bad=np.flatnonzero(np.maximum(plan_res,initial_res)>2e-8)
        seq=z@ctrl.optmap.T;cache={}
        def get_margin(j):
            nonlocal adaptive_tubes,first_margins
            if j not in cache:
                if k==0 and first_margins is not None:
                    cache[j]=first_margins
                else:
                    mh,_,_=ctrl.margins(innovation_history[j,:k].tolist(),
                                       (hats[j,:k+1]-zs[j,:k+1]).tolist(),True)
                    cache[j]=mh;adaptive_tubes+=1
                    if k==0: first_margins=mh
            return cache[j]
        for j in bad:
            mh=get_margin(j);ss,status,res=ctrl.solve(z[j],mh)
            if ss is None:
                raise RuntimeError(f'Adaptive MC failure trajectory={j}, k={k}, status={status}')
            seq[j]=ss;plan_res[j]=res;initial_res[j]=np.max(ctrl.Hx@z[j]+mh[0,:4]-ctrl.hx)
            adaptive_solves+=int(status!='exact_unconstrained')
            branches.append(dict(trajectory=int(j),k=k,branch=status,residual=res))
        shortcut_count+=trajectories-len(bad)+sum(v['k']==k and v['branch']=='exact_unconstrained' for v in branches)
        if previous_shift is not None:
            shift_res=np.max(previous_shift@ctrl.constraint.T+z@bmap.T-b0,axis=1)
            for j in np.flatnonzero(np.maximum(shift_res,initial_res)>2e-7):
                mh=get_margin(j);shift_res[j]=ctrl.feasible(z[j],previous_shift[j],mh)[1]
            maxshift=max(maxshift,float(max(shift_res)))
            failures+=int(np.count_nonzero(shift_res>2e-6))
        nominal=seq[:,0]
        u=nominal+(hat-z)@ctrl.K.ravel()
        violation=np.maximum(np.max(x@ctrl.Hx.T-ctrl.hx,axis=1),np.abs(u)-1)
        failures+=int(np.count_nonzero(violation>2e-7))
        maxviolation=max(maxviolation,float(max(violation)))
        maxplan=max(maxplan,float(max(plan_res)),float(max(initial_res)))
        xp=x@ctrl.sys.A.T+(u+.05*noiseall[:,k,0])[:,None]*ctrl.sys.B.ravel()
        zp=z@ctrl.sys.A.T+nominal[:,None]*ctrl.sys.B.ravel()
        predicted=hat@ctrl.sys.A.T+u[:,None]*ctrl.sys.B.ravel()
        r=xp[:,0]+.1*noiseall[:,k,1]-predicted[:,0]
        hp=predicted+r[:,None]*ctrl.L.ravel()
        eta_expected=eta@ctrl.joint.F.T+noiseall[:,k]@ctrl.joint.D.T
        eta=np.c_[xp-hp,hp-zp]
        maxdynamics=max(maxdynamics,float(np.max(abs(eta-eta_expected))))
        terminal= z@ctrl.Phi[-2:].T+seq@ctrl.Gamma[-2:].T
        shifted=np.c_[seq[:,1:],terminal@ctrl.K.ravel()]
        previous_shift=shifted
        innovation_history[:,k]=r
        inputs[:,k]=u;x,hat,z=xp,hp,zp
        xs[:,k+1]=x;zs[:,k+1]=z;hats[:,k+1]=hat
    terminal_violation=float(np.max(xs[:,-1]@ctrl.Hx.T-ctrl.hx))
    failures+=int(np.count_nonzero(np.max(xs[:,-1]@ctrl.Hx.T-ctrl.hx,axis=1)>2e-7))
    # Each row is an independent complete disturbance/noise sequence.
    np.savez_compressed(out/'monte_carlo_10000.npz',x_true=xs,x_nominal=zs,hat_x=hats,u=inputs,
                        disturbances_and_sensor_noise_unit=noiseall,initial=initial,
                        innovations=innovation_history,window=ctrl.window,
                        tube_template_c=ctrl.joint.S.c,tube_template_G=ctrl.joint.S.G)
    return dict(trajectories=trajectories,steps=steps,state_transitions=trajectories*steps,
                constraint_failures=failures,max_constraint_violation=max(maxviolation,terminal_violation),
                max_plan_residual=maxplan,max_shift_residual=maxshift,
                max_joint_dynamics_residual=maxdynamics,runtime=time.perf_counter()-tic,
                exact_unconstrained_shortcuts=shortcut_count,online_QP_solves=adaptive_solves,
                adaptive_tube_computations=adaptive_tubes,explicit_adaptive_branches=branches,
                initial_error='zero; robust disturbance/sensor noise independent and uniformly sampled',
                set_storage='lossless reconstruction: stored S, innovation prefix, d=hat_x-z prefix, window; see reconstruct_mc_sets',
                scope='adaptive MPC; exact unconstrained shortcut after fixed-envelope feasibility; actual adaptive QP otherwise')


def reconstruct_mc_sets(archive,trajectory,k,ctrl=None):
    """Recover the saved information set and full adaptive tube at any time."""
    if ctrl is None: ctrl=TubeMPC()
    a=np.load(archive)
    r=a['innovations'][trajectory,:k].tolist()
    ds=(a['hat_x'][trajectory,:k+1]-a['x_nominal'][trajectory,:k+1]).tolist()
    tube=ctrl.joint.compatible_tube(r,ds,int(a['window']),ctrl.N)
    from src.oit_mrpi.sets import linear_map
    Xhat=linear_map(np.c_[np.eye(2),np.zeros((2,2))],tube[0]).translate(a['hat_x'][trajectory,k])
    return Xhat,tube
