"""Run279 exact arithmetic sanity checks; not a full posterior LP solver."""
from fractions import Fraction as F

def verify():
    h=F(1,50)
    R=F(3246383,1600000)
    eps=F(1,50)
    alpha=F(28057872,35710213)
    r=[-R]*3+[alpha*R]+[R]*11
    assert len(r)==15
    p=h*h*sum((14-i)*r[i] for i in range(15))
    v=h*sum(r)
    assert p==eps
    assert v==F(39217447,110000000)
    # Lipschitz |sin(a)-sin(b)|<=|a-b|; nominal T/m=9.81.
    delta=F(981,100)*F(1,200)
    assert delta==F(981,20000)
    # Conservative velocity radius when no position observations are applied.
    bound=15*h*(R+delta)
    assert bound==F(9974589,16000000)
    assert bound>v
    return str(p),str(v),str(delta),str(bound)

if __name__=="__main__":
    print("PASS Run279 Fraction checks:",*verify())
