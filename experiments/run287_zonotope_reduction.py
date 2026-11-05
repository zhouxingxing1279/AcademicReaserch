"""Run287: 12-state synthetic hover zonotope-SMF reduction benchmark; not MPC."""
import time
import numpy as np
from scipy.linalg import expm
DT=.02
A=np.zeros((12,12)); B=np.zeros((12,4))
for i in range(3):
    A[i,i+3]=1; A[6+i,9+i]=1; B[9+i,1+i]=1
A[3,7]=9.81; A[4,6]=-9.81; B[5,0]=1
E=np.zeros((16,16)); E[:12,:12]=A; E[:12,12:]=B
F=expm(E*DT); AD=F[:12,:12]; BD=F[:12,12:]
INITIAL=np.array([.02]*3+[.04]*3+[.015]*3+[.025]*3)
PROC=np.array([.0002]*3+[.001]*3+[.0001]*3+[.0005]*3)
MEAS=np.array([.01,.01,.01,.008]); IDX=[0,1,2,8]
def reduce(G,q):
    if G.shape[1]<=q: return G
    keep=np.argsort(-np.linalg.norm(G,axis=0),kind='stable')[:q]
    discard=np.ones(G.shape[1],dtype=bool); discard[keep]=False
    return np.column_stack((G[:,keep],np.diag(np.abs(G[:,discard]).sum(axis=1))))
def run(q,seed=285):
    rng=np.random.default_rng(seed); truth=rng.uniform(-INITIAL,INITIAL)
    c=np.zeros(12); G=np.diag(INITIAL); maxwidth=0.; failures=0; peak=0
    t0=time.perf_counter()
    for k in range(1,301):
        u=np.array([.1*np.sin(.02*k),.02*np.cos(.03*k),.015*np.sin(.04*k),.01*np.cos(.01*k)])
        truth=AD@truth+BD@u+rng.uniform(-PROC,PROC)
        c=AD@c+BD@u; G=np.column_stack((AD@G,np.diag(PROC)))
        if k%5==0 and (k//5)%3!=2:
            y=truth[IDX]+rng.uniform(-MEAS,MEAS)
            for j,i in enumerate(IDX):
                v=G[i,:]; z=G@v; lam=z/(v@v+MEAS[j]**2)
                c=c+lam*(y[j]-c[i])
                G=np.column_stack((G-np.outer(lam,v),lam[:,None]*MEAS[j]))
        if q is not None: G=reduce(G,q)
        peak=max(peak,G.shape[1]); width=2*np.abs(G).sum(axis=1)
        maxwidth=max(maxwidth,float(width[0]))
        failures+=int(np.any(np.abs(truth-c)>width/2+1e-8))
    return dict(q=q,maximum_x_width=round(maxwidth,6),final_x_width=round(float(width[0]),6),peak_generators=peak,failures=failures,elapsed_s=round(time.perf_counter()-t0,4))
if __name__=='__main__':
    for q in [12,24,48,96,None]: print(run(q))
    rng=np.random.default_rng(9)
    for q in [12,24,48]:
        G=rng.normal(size=(12,100)); H=reduce(G,q)
        for _ in range(100):
            x=G@rng.uniform(-1,1,100)
            assert np.all(np.abs(x)<=np.abs(H).sum(axis=1)+1e-10)
    print('reduction enclosure checks PASS')
