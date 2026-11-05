"""Reproducible mechanism screen; not a quadrotor or publication novelty proof.
Run: .venv/Scripts/python.exe -m experiments.cong_mpc_screen
All LP/QP operations are floating point, not outward-rounded safety certificates.
"""
from pathlib import Path
from dataclasses import dataclass
from itertools import product, combinations
import csv, json, hashlib, platform, time
import numpy as np
import scipy
from scipy.optimize import linprog, minimize
from scipy.linalg import solve_discrete_lyapunov
import scipy.sparse as sp
import osqp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from src.outerloop.finite_memory import FloatCZ

OUT = Path("experiments/results/cong_mpc_screen")
TOL = 2e-6
SEEDS = tuple(range(8))

def dump_csv(name, rows):
    with (OUT/name).open("w", encoding="utf-8", newline="") as f:
        writer=csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)

def lp(c, A=None, b=None, eq=None, rhs=None, bounds=None):
    r=linprog(c, A_ub=A, b_ub=b, A_eq=eq, b_eq=rhs, bounds=bounds, method="highs")
    if not r.success:
        raise RuntimeError("LP failed: "+r.message)
    return r

def cz_support(z,q):
    r=z.solve(-z.generators.T@q)
    return float(q@z.center-r.fun)

def cz_predict(z,A,B,u,w):
    n=z.generators.shape[1]
    return FloatCZ(A@z.center+B*u, np.c_[A@z.generators,np.diag(w)],
                   np.c_[z.equalities,np.zeros((len(z.rhs),len(w)))], z.rhs.copy())

def cz_measure(z,C,y,v):
    n=z.generators.shape[1]
    return FloatCZ(z.center.copy(), np.c_[z.generators,np.zeros(len(C))],
                   np.vstack([np.c_[z.equalities,np.zeros(len(z.rhs))],
                              np.r_[C@z.generators,v]]),
                   np.r_[z.rhs,y-C@z.center])

def age_probe():
    rows=[]
    for M,a in product((1,2,3),(.9,1.,1.1)):
        radii=np.array([a**s*.03+.02*sum(a**j for j in range(s)) for s in range(M+1)])
        for age in range(M+1):
            reachable={age}; paths=[(age,)]
            for j in range(9):
                assert reachable=={p[-1] for p in paths}
                rows.append(dict(M=M,a=a,initial_age=age,horizon=j,
                                 reachable=";".join(map(str,sorted(reachable))),
                                 causal_bound=max(radii[list(reachable)]),
                                 uniform_bound=max(radii), oracle_all_fresh=radii[0]))
                reachable={n for s in reachable for n in ([0,s+1] if s<M else [0])}
                paths=[p+(n,) for p in paths for n in ([0,p[-1]+1] if p[-1]<M else [0])]
    dump_csv("a_age.csv",rows)
    return rows

def disturbance_probe():
    dt=.2
    A=np.array([[1,dt,.5*dt*dt],[0,1,dt],[0,0,1.]])
    B=np.array([.5*dt*dt,dt,0])
    C=np.array([1.,0,0]); w=np.array([.002,.005,.02])
    rows=[]; containment=0
    for nu,period,seed in product((.005,.02,.05),(1,2),SEEDS):
        rng=np.random.default_rng(1000+seed)
        z=FloatCZ(np.zeros(3),np.diag([.1,.2,.5]),np.empty((0,3)),np.empty(0))
        x=rng.uniform(-1,1,3)*[.1,.2,.5]
        for k in range(11):
            if k%period==0:
                z=cz_measure(z,C,float(C@x+rng.uniform(-nu,nu)),nu)
            # Known amplitude bound for disturbance; symmetric strip.
            z=cz_measure(z,np.array([0.,0,1.]),0.,.6)
            containment += int(not z.contains(x))
            if k<10:
                x=A@x+rng.uniform(-1,1,3)*w
                z=cz_predict(z,A,B,0.,w)
        lo,hi=z.bounds()
        for horizon,coordinate in product((1,3,6),(0,1)):
            q=np.linalg.matrix_power(A,horizon)[coordinate]
            qx=q.copy(); qx[2]=0
            qd=np.array([0.,0,q[2]])
            joint=(cz_support(z,q)+cz_support(z,-q))/2
            split=(cz_support(z,qx)+cz_support(z,-qx)+cz_support(z,qd)+cz_support(z,-qd))/2
            box=np.abs(q)@((hi-lo)/2)
            assert joint<=split+TOL and split<=box+TOL
            rows.append(dict(noise=nu,period=period,seed=seed,horizon=horizon,coordinate=coordinate,
                             joint_radius=joint,split_radius=split,box_radius=box,
                             reduction_vs_split=1-joint/split))
    assert containment==0
    dump_csv("b_joint.csv",rows)
    return rows, containment

def unique_dirs(rows):
    ds=[]
    for q in rows:
        q=q/np.linalg.norm(q)
        if not any(np.max(abs(q-p))<1e-10 for p in ds):
            ds.append(q)
    return np.array(ds)

A=np.array([[.75,.2],[-.1,.7]])
B=np.array([.15,.2])
W=np.array([.005,.005])
H=np.array([[1.,0],[-1.,0],[0,1.],[0,-1.],[1,1],[-1,-1.]])
H[4:]/=np.sqrt(2)
LIMIT=np.array([1.2,1.2,.8,.8,.85,.85])
HF=H[:4]
FBOUND=np.full(4,.25)
N=6
DIR=unique_dirs([row@np.linalg.matrix_power(A,j) for j in range(N+1) for row in H])
BOX=H[:4]
angles=np.arange(len(DIR))*2*np.pi/len(DIR)
UNIFORM=np.c_[np.cos(angles),np.sin(angles)]
METHODS={"horizon":DIR,"uniform":UNIFORM,"box":BOX}

@dataclass
class Poly:
    D: np.ndarray
    b: np.ndarray
    def support(self,q):
        return -lp(-q,self.D,self.b,bounds=[(None,None)]*2).fun
    def representative(self):
        r=lp([0,0,-1],np.c_[self.D,np.ones(len(self.D))],self.b,
             bounds=[(None,None),(None,None),(0,None)])
        return r.x[:2]
    def contains(self,x):
        return bool(np.max(self.D@x-self.b)<=TOL)
    def update(self,u,y=None,nu=.025):
        mat=np.c_[self.D,np.zeros((len(self.D),2))]
        bounds=[(None,None)]*2+[(-float(v),float(v)) for v in W]
        rhs=self.b.copy()
        C=np.array([1.,.4])
        if y is not None:
            row=np.r_[C@A,C]
            mat=np.vstack([mat,row,-row])
            rhs=np.r_[rhs,y+nu-C@B*u,-y+nu+C@B*u]
        new=[]
        for q in self.D:
            cost=-np.r_[q@A,q]
            new.append(q@B*u-lp(cost,mat,rhs,bounds=bounds).fun)
        return Poly(self.D,np.array(new))

class RobustMPC:
    def __init__(self):
        self.powers=[np.linalg.matrix_power(A,j) for j in range(N+1)]
        self.Phi=np.vstack(self.powers[1:])
        self.Gamma=np.zeros((2*N,N))
        for j in range(N):
            for i in range(j+1):
                self.Gamma[2*j:2*j+2,i]=self.powers[j-i]@B
        Q=np.eye(2); R=.15
        P=solve_discrete_lyapunov(A.T,Q)
        cost=sp.block_diag([Q]*(N-1)+[P]).toarray()
        self.qmap=2*self.Gamma.T@cost@self.Phi
        self.P=sp.csc_matrix(np.triu(2*(R*np.eye(N)+self.Gamma.T@cost@self.Gamma)))
        self.future=np.vstack([H@self.Gamma[2*j:2*j+2] for j in range(N)]
                              +[HF@self.Gamma[-2:]])
        self.constraint=np.vstack([np.eye(N),self.future])
        self.solver=osqp.OSQP()
        self.solver.setup(P=self.P,q=np.zeros(N),A=sp.csc_matrix(self.constraint),
                          l=np.r_[np.full(N,-.35),np.full(len(self.future),-np.inf)],
                          u=np.r_[np.full(N,.35),np.ones(len(self.future))],
                          eps_abs=1e-8,eps_rel=1e-8,max_iter=30000,
                          verbose=False,polishing=False)
    def noise_support(self,q,j):
        return sum(np.abs(q@self.powers[l])@W for l in range(j))
    def bounds(self,support):
        initial=np.array([support(q) for q in H])-LIMIT
        values=[]
        for j in range(1,N+1):
            values.extend([bound-support(q@self.powers[j])-self.noise_support(q,j)
                           for q,bound in zip(H,LIMIT)])
        values.extend([bound-support(q@self.powers[N])-self.noise_support(q,N)
                       for q,bound in zip(HF,FBOUND)])
        return initial,np.array(values)
    def solve(self,support,hat,feasible_only=False):
        initial,b=self.bounds(support)
        if max(initial)>TOL: return None
        if feasible_only:
            r=linprog(np.zeros(N),A_ub=self.future,b_ub=b,bounds=[(-.35,.35)]*N,method="highs")
            if r.status==2:return None
            if not r.success:raise RuntimeError(r.message)
            seq=r.x
        else:
            self.solver.update(q=self.qmap@hat,u=np.r_[np.full(N,.35),b])
            r=self.solver.solve(raise_error=False)
            if "infeasible" in r.info.status:return None
            if r.info.status!="solved":raise RuntimeError(r.info.status)
            seq=r.x
        if max(np.max(self.future@seq-b),np.max(abs(seq))-.35)>TOL:
            raise RuntimeError("QP/LP constraint residual")
        return seq.copy()
    def violation(self,support,seq):
        initial,b=self.bounds(support)
        return max(float(max(initial)),float(max(self.future@seq-b)),float(max(abs(seq))-.35))

def shape(theta):
    R=np.array([[np.cos(theta),-np.sin(theta)],[np.sin(theta),np.cos(theta)]])
    return R@np.array([[.24,.02,0],[-.24,0,.02]])

def vertices(poly):
    out=[]
    for i,j in combinations(range(len(poly.D)),2):
        mat=poly.D[[i,j]]
        if abs(np.linalg.det(mat))<1e-10:continue
        x=np.linalg.solve(mat,poly.b[[i,j]])
        if poly.contains(x):out.append(x)
    if not out:raise RuntimeError("No polygon vertices")
    return np.array(out)

def template_probe():
    mpc=RobustMPC(); rows=[]; gaps=[]; timing=[]
    # Verify RPI terminal condition independently.
    assert np.all(np.abs(HF@A).sum(axis=1)*.25+np.abs(HF)@W<=FBOUND+1e-12)
    grid=np.linspace(-.9,.9,15)
    for degree in range(0,180,15):
        G=shape(np.deg2rad(degree))
        exact=lambda q:float(np.abs(q@G).sum())
        polys={name:Poly(D,np.array([exact(q) for q in D])) for name,D in METHODS.items()}
        # Independent 2D vertex support verification of template LP values.
        for name,p in polys.items():
            verts=vertices(p)
            for q in DIR:
                gap=p.support(q)-exact(q)
                assert abs(p.support(q)-max(verts@q))<TOL
                assert gap>=-TOL
                if name=="horizon":assert abs(gap)<TOL
                gaps.append(dict(degree=degree,method=name,gap=gap))
        bases={}
        for name in ("exact",*METHODS):
            fun=exact if name=="exact" else polys[name].support
            tic=time.perf_counter()
            init,b=mpc.bounds(fun)
            timing.append(dict(degree=degree,method=name,ms=(time.perf_counter()-tic)*1000))
            bases[name]=(init,b)
        maps={}
        center_con=np.vstack([H]+[H@mpc.powers[j] for j in range(1,N+1)]+[HF@mpc.powers[N]])
        for cx,cy in product(grid,grid):
            c=np.array([cx,cy]); flags={}
            for name,(init,b0) in bases.items():
                initial=init+H@c
                b=b0-center_con[len(H):]@c
                if max(initial)>TOL:
                    ok=False
                else:
                    r=linprog(np.zeros(N),A_ub=mpc.future,b_ub=b,bounds=[(-.35,.35)]*N,method="highs")
                    if r.status not in (0,2):raise RuntimeError(r.message)
                    ok=r.success
                    if ok: assert max(mpc.future@r.x-b)<TOL
                flags[name]=int(ok)
                rows.append(dict(degree=degree,cx=cx,cy=cy,method=name,feasible=int(ok)))
            assert flags["exact"]==flags["horizon"]
            assert flags["uniform"]<=flags["exact"] and flags["box"]<=flags["exact"]
    dump_csv("c_grid.csv",rows); dump_csv("c_support_gaps.csv",gaps);dump_csv("c_query_timing.csv",timing)
    return rows,gaps,timing

def closed_loop_probe():
    rows=[]; summaries=[]
    G=shape(0.)
    for period,seed,method in product((1,3),SEEDS,METHODS):
        rng=np.random.default_rng(2000+seed)
        c=np.array([.7,-.5])
        x=c+G@rng.uniform(-1,1,3)
        disturbance=rng.uniform(-1,1,(30,2))*W
        noise=rng.uniform(-.025,.025,31)
        D=METHODS[method]
        poly=Poly(D,np.array([q@c+abs(q@G).sum() for q in D]))
        # k=0 measurement applied directly to the initial polytope.
        C=np.array([1.,.4]); y=float(C@x+noise[0])
        Da=np.vstack([poly.D,C,-C]); ba=np.r_[poly.b,y+.025,-y+.025]
        exact0=Poly(Da,ba)
        poly=Poly(D,np.array([exact0.support(q) for q in D]))
        mpc=RobustMPC(); failure=None; cost=0; estimates=[]
        for k in range(30):
            tic=time.perf_counter()
            hat=poly.representative()
            seq=mpc.solve(poly.support,hat)
            solve_ms=(time.perf_counter()-tic)*1000
            if seq is None:
                failure="qp_infeasible";break
            state_violation=max(H@x-LIMIT)
            if not poly.contains(x):raise RuntimeError("truth escaped template")
            if state_violation>TOL:raise RuntimeError("actual state violation")
            u=float(seq[0]); cost+=float(x@x+.15*u*u)
            xnext=A@x+B*u+disturbance[k]
            y=float(C@xnext+noise[k+1]) if (k+1)%period==0 else None
            tic=time.perf_counter(); nxt=poly.update(u,y)
            estimate_ms=(time.perf_counter()-tic)*1000
            if not nxt.contains(xnext):raise RuntimeError("next truth escaped")
            shifted=np.r_[seq[1:],0.]
            shift_v=mpc.violation(nxt.support,shifted)
            if method=="horizon" and shift_v>TOL:raise RuntimeError("direction-template shift violation")
            rows.append(dict(method=method,period=period,seed=seed,k=k,x1=x[0],x2=x[1],
                             u=u,cost_so_far=cost,estimate_ms=estimate_ms,solve_ms=solve_ms,
                             state_violation=state_violation,input_violation=abs(u)-.35,
                             shift_violation=shift_v,faces=len(D),measurement=int(y is not None),
                             representative_error=float(np.linalg.norm(x-hat))))
            x=xnext; poly=nxt
        summaries.append(dict(method=method,period=period,seed=seed,steps=k if failure else 30,
                              failure=failure,cost=cost,final_norm=float(np.linalg.norm(x))))
    dump_csv("c_closed_loop_steps.csv",rows);dump_csv("c_closed_loop_cases.csv",summaries)
    return rows,summaries

def dual_probe():
    rows=[]
    for degree in range(0,180,15):
        th=np.deg2rad(degree); R=np.array([[np.cos(th),-np.sin(th)],[np.sin(th),np.cos(th)]])
        G=R@np.array([[.24,0,.02,0],[0,.24,0,.02]])
        eq=np.array([[1.,1.,0,0]]); b=np.zeros(1)
        for idx,q in enumerate(DIR):
            tic=time.perf_counter()
            r=lp(-G.T@q,eq=eq,rhs=b,bounds=[(-1,1)]*4)
            lp_ms=(time.perf_counter()-tic)*1000
            truth=-r.fun; lamopt=-r.eqlin.marginals
            upper=lambda l:float(b@l+np.abs(G.T@q-eq.T@l).sum())
            assert abs(upper(lamopt)-truth)<TOL
            history=[np.zeros(1)]
            def obj(l):
                residual=G.T@q-eq.T@l
                den=np.sqrt(residual**2+1e-10)
                return float(b@l+den.sum()),b-eq@(residual/den)
            tic=time.perf_counter()
            result=minimize(obj,history[0],jac=True,method="L-BFGS-B",
                            callback=lambda l:history.append(l.copy()),
                            options={"maxiter":30,"gtol":1e-10,"ftol":1e-14})
            history.append(result.x)
            dual_ms=(time.perf_counter()-tic)*1000
            uppers=np.minimum.accumulate([upper(l) for l in history])
            assert np.min(uppers-truth)>-TOL
            for budget in (0,1,3,10,30):
                i=min(budget,len(uppers)-1)
                rows.append(dict(degree=degree,direction=idx,budget=budget,iterations_available=len(history)-1,
                                 exact=truth,upper=uppers[i],gap=uppers[i]-truth,
                                 full_lp_ms=lp_ms,full_30_dual_ms=dual_ms))
    dump_csv("c_dual.csv",rows)
    return rows

def sensing_probe():
    pri=np.array([[-1.,1.],[1.,1.]])
    obs=np.array([-1.3,1.])
    rows=[]
    for noise,restriction in product((0.,.03,.15,.4),("free","no_lateral")):
        for dx,dy in product((-.4,0,.4),repeat=2):
            if restriction=="no_lateral" and dx!=0:continue
            d=np.array([dx,dy])
            # Both possible trajectories must avoid the obstacle throughout the move.
            safe=True
            for p in pri:
                t=np.clip(np.dot(obs-p,d)/np.dot(d,d),0,1) if np.dot(d,d)>0 else 0
                safe &= np.linalg.norm(p+t*d-obs)>=.25-1e-12
            distance=np.linalg.norm(pri+d,axis=1)
            separation=abs(distance[0]-distance[1])
            worst=1 if separation>2*noise+1e-12 else 2
            rows.append(dict(noise=noise,restriction=restriction,dx=dx,dy=dy,safe=int(safe),
                             separation=separation,worst_hypotheses=worst,
                             worst_diameter=0. if worst==1 else 2.,energy=dx*dx+dy*dy))
    dump_csv("d_sensing.csv",rows)
    return rows

def relative_probe():
    rows=[]
    for radius,alpha in product((0.,.1,.3,.5),(1.,.5,-1.)):
        vals=[(radius*b+.05*ei)-(alpha*radius*b+.05*ej) for b,ei,ej in product((-1,1),repeat=3)]
        exact=abs(1-alpha)*radius+.1
        box=(1+abs(alpha))*radius+.1
        assert abs(max(vals)-exact)<1e-12
        rows.append(dict(common_radius=radius,alpha=alpha,joint_radius=exact,independent_radius=box,
                         required_distance_joint=.2+exact,required_distance_independent=.2+box,
                         vertices=len(vals)))
    dump_csv("e_relative.csv",rows)
    return rows

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    start=time.perf_counter()
    aa=age_probe();print("A done",flush=True)
    bb,bfail=disturbance_probe();print("B done",flush=True)
    cc,cgap,ct=template_probe();print("C grid done",flush=True)
    steps,cases=closed_loop_probe();print("C loop done",flush=True)
    dual=dual_probe();dd=sensing_probe();ee=relative_probe();print("D/E done",flush=True)
    summary={
      "scope":"mechanism screen, stable 2D mathematical MPC; no quadrotor/SITL or full-paper reproduction",
      "seeds":list(SEEDS),"float_tolerance":TOL,
      "environment":{"python":platform.python_version(),"numpy":np.__version__,"scipy":scipy.__version__,
                     "osqp":osqp.__version__,"matplotlib":matplotlib.__version__},
      "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      "A":{"rows":len(aa),"reachable_sets_cross_checked_by_exhaustive_sequences":True,
           "example":[r for r in aa if r["M"]==2 and r["a"]==1.1 and r["initial_age"]==0]},
      "B":{"posterior_cases":48,"support_queries":len(bb),"containment_failures":bfail,
           "median_gain_vs_split":float(np.median([r["reduction_vs_split"] for r in bb])),
           "min_gain_vs_split":float(min(r["reduction_vs_split"] for r in bb)),
           "max_gain_vs_split":float(max(r["reduction_vs_split"] for r in bb))},
      "C":{"faces":{m:len(d) for m,d in METHODS.items()},"center_orientation_cases":2700,
           "feasible":{m:sum(r["feasible"] for r in cc if r["method"]==m) for m in ("exact",*METHODS)},
           "max_support_gap":{m:max(r["gap"] for r in cgap if r["method"]==m) for m in METHODS},
           "closed_loop_cases":len(cases),"steps":len(steps),"case_summaries":cases,
           "shift_failures":{m:sum(r["shift_violation"]>TOL for r in steps if r["method"]==m) for m in METHODS},
           "max_measured_pipeline_ms":{m:max(r["estimate_ms"]+r["solve_ms"] for r in steps if r["method"]==m) for m in METHODS},
           "mean_measured_pipeline_ms":{m:float(np.mean([r["estimate_ms"]+r["solve_ms"] for r in steps if r["method"]==m])) for m in METHODS},
           "dual_min_gap":float(min(r["gap"] for r in dual)),
           "dual_median_gap_by_budget":{str(t):float(np.median([r["gap"] for r in dual if r["budget"]==t])) for t in (0,1,3,10,30)},
           "median_full_lp_ms":float(np.median([r["full_lp_ms"] for r in dual if r["budget"]==0])),
           "median_full_30_dual_ms":float(np.median([r["full_30_dual_ms"] for r in dual if r["budget"]==0]))},
      "D":{"discrete_prior_size":2,"tested_actions":len(dd),
           "best_safe_worst_hypotheses":[{"noise":nu,"restriction":rest,
             "worst_hypotheses":min(r["worst_hypotheses"] for r in dd if r["noise"]==nu and r["restriction"]==rest and r["safe"])}
             for nu,rest in product((0.,.03,.15,.4),("free","no_lateral"))]},
      "E":{"rows":ee,"joint_vertices_checked":sum(r["vertices"] for r in ee)},
      "elapsed_seconds":time.perf_counter()-start}
    for p in sorted(OUT.glob("*.csv")):
        summary.setdefault("csv_sha256",{})[p.name]=hashlib.sha256(p.read_bytes()).hexdigest()
    (OUT/"summary.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    fig,axs=plt.subplots(2,3,figsize=(15,8))
    aex=summary["A"]["example"]
    axs[0,0].plot([r["horizon"] for r in aex],[r["causal_bound"] for r in aex],"-o",label="Known current age")
    axs[0,0].plot([r["horizon"] for r in aex],[r["uniform_bound"] for r in aex],"--",label="Uniform")
    axs[0,0].set(title="A: future worst-case age",xlabel="Prediction step",ylabel="Error radius")
    axs[0,0].legend()
    axs[0,1].hist([100*r["reduction_vs_split"] for r in bb],bins=20,color="#237a91")
    axs[0,1].set(title="B: joint vs state/disturbance split",xlabel="Support-radius reduction (%)",ylabel="Count")
    names=["exact","horizon","uniform","box"]
    axs[0,2].bar(names,[summary["C"]["feasible"][m]/2700*100 for m in names],color=["#333333","#237a91","#a98953","#d08989"])
    axs[0,2].set(title="C: robust feasible grid samples",ylabel="Feasible (%)",ylim=(0,100))
    axs[1,0].plot([0,1,3,10,30],[summary["C"]["dual_median_gap_by_budget"][str(t)] for t in (0,1,3,10,30)],"-o")
    axs[1,0].set(title="C: standard dual bound",xlabel="Iteration budget",ylabel="Median absolute gap")
    for rest in ("free","no_lateral"):
        vals=[r for r in summary["D"]["best_safe_worst_hypotheses"] if r["restriction"]==rest]
        axs[1,1].plot([r["noise"] for r in vals],[r["worst_hypotheses"] for r in vals],"-o",label=rest)
    axs[1,1].set(title="D: active range disambiguation",xlabel="Range-noise radius",ylabel="Worst remaining hypotheses",yticks=[1,2])
    axs[1,1].legend()
    vals=[r for r in ee if r["alpha"]==1.]
    axs[1,2].plot([r["common_radius"] for r in vals],[r["joint_radius"] for r in vals],"-o",label="Joint")
    axs[1,2].plot([r["common_radius"] for r in vals],[r["independent_radius"] for r in vals],"--o",label="Independent")
    axs[1,2].set(title="E: same common error",xlabel="Common bias radius",ylabel="Relative-error radius")
    axs[1,2].legend()
    fig.suptitle("Mechanism screening: evidence of effects, not evidence of novelty",fontsize=14)
    fig.tight_layout()
    fig.savefig(OUT/"mechanisms.png",dpi=180)
    fig.savefig(OUT/"mechanisms.pdf")
    print(json.dumps({k:v for k,v in summary.items() if k not in ("C","csv_sha256")},ensure_ascii=False,indent=2))
    print(json.dumps({k:v for k,v in summary["C"].items() if k!="case_summaries"},indent=2))
if __name__=="__main__":
    main()

