"""Run 110: verify exact k-strip support dual against primal LP."""
import numpy as np
from scipy.optimize import linprog

def primal(d,A,y,r):
    m=d.size
    R=linprog(-d,A_ub=np.vstack([A,-A]),b_ub=np.r_[y+r,-y+r],
              bounds=[(-1,1)]*m,method="highs")
    assert R.success
    return -R.fun

def dual(d,A,y,r):
    k,m=A.shape; n=2*k+m
    c=np.r_[y,r,np.ones(m)]
    rows=[]; rhs=[]
    for l in range(k):
        z=np.zeros(n); z[l]=1; z[k+l]=-1; rows.append(z); rhs.append(0)
        z=np.zeros(n); z[l]=-1; z[k+l]=-1; rows.append(z); rhs.append(0)
    for j in range(m):
        z=np.zeros(n); z[:k]=-A[:,j]; z[2*k+j]=-1; rows.append(z); rhs.append(-d[j])
        z=np.zeros(n); z[:k]= A[:,j]; z[2*k+j]=-1; rows.append(z); rhs.append( d[j])
    R=linprog(c,A_ub=np.asarray(rows),b_ub=np.asarray(rhs),
              bounds=[(None,None)]*k+[(0,None)]*(k+m),method="highs")
    assert R.success
    return R.fun

def main():
    rng=np.random.default_rng(109); errors=[]
    for _ in range(100):
        k,m=2,20
        A=rng.normal(size=(k,m)); d=rng.normal(size=m)
        y=rng.uniform(-.2,.2,size=k); r=np.array([.5,.4])
        errors.append(abs(primal(d,A,y,r)-dual(d,A,y,r)))
    mx=max(errors)
    print({"cases":len(errors),"max_abs_error":mx})
    assert mx < 1e-10

if __name__=="__main__":
    main()
