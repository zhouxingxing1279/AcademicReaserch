"""Exact algebra for theory 06; no controller simulation or invariance claim."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
from check_terminal_polytope import verify as previous

ROOT = Path(__file__).resolve().parents[1]
H, GRAV = F(1, 50), F(981, 100)

def inputs(z):
    hp, hv, c, y = z[6:8], z[8:10], z[10:12], z[12:14]
    t = -hp[1]-2*hv[1]
    mu = F(4,125)*hp[0]+F(8,125)*hv[0]-F(8,25)*c[0]-F(4,25)*c[1]
    tau = mu-F(8,25)*(y[0]-c[0])-F(4,25)*(y[1]-c[1])
    return t, mu, tau

def step(z, w, success):
    p, v, phi, omega = z[:2], z[2:4], z[4], z[5]
    hp, hv, c, y = z[6:8], z[8:10], z[10:12], z[12:14]
    t, mu, tau = inputs(z)
    pn = [p[i]+H*v[i] for i in range(2)]
    vn = [v[0]+H*(-GRAV*phi+w[0]), v[1]+H*(t+w[1])]
    phin, omegan = phi+H*omega, omega+tau
    pp = [hp[i]+H*hv[i] for i in range(2)]
    vp = [hv[0]-H*GRAV*y[0], hv[1]+H*t]
    innovation = [pn[i]+w[i+2]-pp[i] for i in range(2)]
    if success:
        pp = [pp[i]+innovation[i] for i in range(2)]
        vp = [vp[i]+5*innovation[i] for i in range(2)]
    return pn+vn+[phin,omegan]+pp+vp+[c[0]+H*c[1],c[1]+mu,phin+w[4],omegan+w[5]]

def basis(n, i):
    return [F(j==i) for j in range(n)]

def encode(x):
    if isinstance(x,F): return str(x)
    if isinstance(x,list): return [encode(a) for a in x]
    if isinstance(x,dict): return {k:encode(v) for k,v in x.items()}
    return x

def verify():
    previous()
    maps = {}
    for success in (False,True):
        columns=[step(basis(14,i),[F(0)]*6,success) for i in range(14)]
        noise=[step([F(0)]*14,basis(6,i),success) for i in range(6)]
        A=[list(row) for row in zip(*columns)]
        G=[list(row) for row in zip(*noise)]
        # Exact coefficient identities: all 20 basis vectors, not trajectory sampling.
        for j in range(20):
            z=basis(14,j) if j<14 else [F(0)]*14
            w=basis(6,j-14) if j>=14 else [F(0)]*6
            nxt=step(z,w,success)
            for i in range(14):
                assert nxt[i]==sum(A[i][k]*z[k] for k in range(14))+sum(G[i][k]*w[k] for k in range(6))
            for i in range(2):
                ep=z[i]-z[6+i]+H*(z[2+i]-z[8+i])
                ev=z[2+i]-z[8+i]+H*(w[i]+(GRAV*(z[12]-z[4]) if i==0 else 0))
                assert nxt[i]-nxt[6+i]==(-w[2+i] if success else ep)
                assert nxt[2+i]-nxt[8+i]==(ev-5*ep-5*w[2+i] if success else ev)
        maps[str(int(success))]={'A':A,'G':G}
    assert all(inputs(basis(14,i))==(0,0,0) for i in range(6))
    # A deliberately omitted position-to-velocity correction must disagree.
    z=basis(14,0);nxt=step(z,[F(0)]*6,True)
    assert nxt[2]-nxt[8]==-5 and nxt[2]-nxt[8]!=0
    edges=[]
    for r in range(5):
        for m in range(3):
            if r<4:edges.append({'from':[r,m],'to':[r+1,m],'success':False})
            else:
                edges.append({'from':[r,m],'to':[0,0],'success':True})
                if m<2:edges.append({'from':[r,m],'to':[0,m+1],'success':False})
    assert len(edges)==17
    # Enumerate no-success paths from a successful opportunity; must end before 15.
    states={(0,0)}
    for age in range(1,16):
        states={tuple(e['to']) for e in edges if tuple(e['from']) in states and not e['success']}
        assert bool(states)==(age<15)
    # Initial maps preserve true-state/measurement correlations for both branches.
    init_widths=[F(1,50),F(1,50),F(1,10),F(1,10),F(1,200),F(1,100),F(1,50),F(1,50),F(1,200),F(1,100)]
    initial={}
    for success in (False,True):
        cols=[]
        for j in range(10):
            a=basis(10,j)
            x=a[:6]
            hp=[a[i]+a[6+i] if success else F(0) for i in range(2)]
            cols.append(x+hp+[F(0)]*4+[a[4]+a[8],a[5]+a[9]])
        B=[list(row) for row in zip(*cols)]
        assert all(len(row)==10 for row in B) and len(B)==14
        # Initial angular error is the original prior, not doubled sensor error.
        phi_bound=sum(abs(B[4][j]-B[10][j])*init_widths[j] for j in range(10))
        s_bound=sum(abs(B[5][j]-B[11][j]+4*(B[4][j]-B[10][j]))*init_widths[j] for j in range(10))
        assert phi_bound==F(1,200) and s_bound==F(3,100)
        initial[str(int(success))]={'B':B,'primitive_halfwidth':init_widths,'mode':[0,0 if success else 1]}
    phi,bt,tmax=F(45,100),F(4905,1000),F(14715,1000)
    dx=F(188,100)+bt*phi+tmax*phi**3/6
    dz=F(2086,1000)+tmax*phi**2/2
    return encode({'status':'EXACT_CAUSAL_MODEL_ALGEBRA_PASSED','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'state_dimension':14,'noise_order':['dx+Rx','dz+Rz','next_npx','next_npz','next_nphi','next_nomega'],'noise_halfwidth':[dx,dz,F(1,50),F(1,50),F(1,200),F(1,100)],'maps':maps,'initial_maps':initial,'edges':edges,'initial_modes':[[0,0],[0,1]],'checks':{'input_true_state_columns_zero':True,'error_coefficient_identities':True,'omitted_correction_rejected':True,'maximum_success_gap_15':True},'full_invariance_proved':False,'candidate_gains_certified':False,'neural_advantage_proved':False})

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result=verify()
    with args.output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(result['status'])
