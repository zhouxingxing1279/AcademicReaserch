from fractions import Fraction as F
from itertools import product

def feasible(T,P,V,A,Xp,Xv,U):
    # Exact common-causal one-step robust feasible input interval.
    lo,hi=-U,U
    for radius,coef,limit in ((P+T*V+T*T*A/2,T*T/2,Xp),(V+T*A,T,Xv)):
        if coef:
            lo=max(lo,(-limit+radius)/coef)
            hi=min(hi,(limit-radius)/coef)
        elif radius>limit: return None
    return (lo,hi) if lo<=hi else None

def main():
    T=F(1,10); P=F(1,5); A=F(1,2); Xp=F(1,4); Xv=F(1); U=F(2)
    for V in [F(1,10),F(2,5),F(1)]:
        interval=feasible(T,P,V,A,Xp,Xv,U)
        for p,v,w in product([-P,P],[-V,V],[-A,A]):
            if interval is not None:
                u=(interval[0]+interval[1])/2
                assert abs(p+T*v+T*T*(u+w)/2)<=Xp
                assert abs(v+T*(u+w))<=Xv
        assert (interval is not None)==(P+T*V+T*T*A/2<=Xp and V+T*A<=Xv)
        print('V=',str(V),'feasible_interval=',interval)
    assert feasible(T,P,F(1),A,Xp,Xv,U) is None
    print('PASS exact rational vertex assertions; no random sampling')
if __name__=='__main__': main()
