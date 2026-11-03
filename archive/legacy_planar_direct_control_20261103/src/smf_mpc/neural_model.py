"""Small float64 residual MLP with explicit gradients and interval bounds."""
import hashlib,json
import numpy as np

SHAPES=((32,5),(32,),(32,32),(32,),(2,32),(2,))


class ResidualMLP:
    def __init__(self, arrays):
        self.arrays=tuple(np.array(a,dtype=float,copy=True) for a in arrays)
        if tuple(a.shape for a in self.arrays)!=SHAPES or not all(np.isfinite(a).all() for a in self.arrays):
            raise ValueError('invalid MLP weights')
        for a in self.arrays:a.flags.writeable=False

    @classmethod
    def initialize(cls, seed=61001):
        rng=np.random.default_rng(seed)
        return cls([rng.normal(0,.2,size=s) if len(s)==2 else np.zeros(s) for s in SHAPES])

    @classmethod
    def from_vector(cls, vector):
        out=[];start=0
        for shape in SHAPES:
            n=int(np.prod(shape));out.append(np.asarray(vector)[start:start+n].reshape(shape));start+=n
        if start!=len(vector):raise ValueError('invalid vector size')
        return cls(out)

    def vector(self):return np.concatenate([a.ravel() for a in self.arrays])

    def digest(self):
        return hashlib.sha256(self.vector().astype('<f8').tobytes()).hexdigest()

    def to_dict(self):return {'architecture':[5,32,32,2],'activation':'tanh_tanh_linear','arrays':[a.tolist() for a in self.arrays],'weights_sha256':self.digest()}

    @classmethod
    def from_dict(cls, data):
        if data['architecture']!=[5,32,32,2] or data['activation']!='tanh_tanh_linear':raise ValueError('model architecture mismatch')
        model=cls(data['arrays'])
        if model.digest()!=data['weights_sha256']:raise ValueError('model hash mismatch')
        return model

    def predict(self, x):
        W1,b1,W2,b2,W3,b3=self.arrays
        h1=np.tanh(np.asarray(x)@W1.T+b1);h2=np.tanh(h1@W2.T+b2)
        return h2@W3.T+b3

    def loss_gradient(self,x,y):
        W1,b1,W2,b2,W3,b3=self.arrays
        h1=np.tanh(x@W1.T+b1);h2=np.tanh(h1@W2.T+b2);err=h2@W3.T+b3-y
        dy=2*err/len(x);gW3=dy.T@h2;gb3=dy.sum(axis=0)
        d2=(dy@W3)*(1-h2*h2);gW2=d2.T@h1;gb2=d2.sum(axis=0)
        d1=(d2@W2)*(1-h1*h1);gW1=d1.T@x;gb1=d1.sum(axis=0)
        return float(np.sum(err*err)/len(x)),np.concatenate([a.ravel() for a in (gW1,gb1,gW2,gb2,gW3,gb3)])

    def jacobian(self,x):
        W1,b1,W2,b2,W3,b3=self.arrays
        h1=np.tanh(W1@x+b1);h2=np.tanh(W2@h1+b2)
        return W3@((1-h2*h2)[:,None]*(W2@((1-h1*h1)[:,None]*W1)))

    def interval(self,lo,hi):
        lo,hi=np.asarray(lo),np.asarray(hi)
        for layer in range(3):
            W,b=self.arrays[2*layer:2*layer+2];pos,neg=np.maximum(W,0),np.minimum(W,0)
            lo,hi=lo@pos.T+hi@neg.T+b,hi@pos.T+lo@neg.T+b
            if layer<2:lo,hi=np.tanh(lo),np.tanh(hi)
        return lo,hi

    def directional_second_bound(self,lo,hi,radius):
        """Bound |d² a(s0+t*delta)/dt²| for |delta|<=radius, whole input box."""
        lo,hi=np.asarray(lo),np.asarray(hi)
        first=np.asarray(radius);second=np.zeros_like(first)
        for layer in range(3):
            W,b=self.arrays[2*layer:2*layer+2];pos,neg=np.maximum(W,0),np.minimum(W,0)
            lo,hi=pos@lo+neg@hi+b,pos@hi+neg@lo+b
            first,second=np.abs(W)@first,np.abs(W)@second
            if layer<2:
                nearest=np.where(lo>0,lo,np.where(hi<0,hi,0.))
                d1=1-np.tanh(nearest)**2
                tlo,thi=np.tanh(lo),np.tanh(hi)
                g=lambda t:2*np.abs(t)*(1-t*t)
                d2=np.maximum(g(tlo),g(thi));critical=1/np.sqrt(3)
                crosses=((tlo<=critical)&(thi>=critical))|((tlo<=-critical)&(thi>=-critical))
                d2=np.where(crosses,4/(3*np.sqrt(3)),d2)
                second=d2*first*first+d1*second;first=d1*first
                lo,hi=tlo,thi
        return second


def features(x,u,config):
    p=config['plant']
    return np.array([x[2]/3,x[3]/3,x[4]/.45,u[0]/(p['mass_kg']*p['gravity_m_s2'])-1,u[1]/.08])


def feature_state_matrix():
    D=np.zeros((5,6));D[0,2]=1/3;D[1,3]=1/3;D[2,4]=1/.45
    return D


def config_digest(config):
    return hashlib.sha256(json.dumps(config,sort_keys=True,separators=(',',':')).encode()).hexdigest()
