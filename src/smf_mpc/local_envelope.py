"""Online complete-cover lookup; no analytic truth or simulator access."""
import hashlib
import numpy as np
from .residual_envelope import validate_envelope
from .neural_model import features,feature_state_matrix

def table_digest(lo,hi,bound):
    return hashlib.sha256(b''.join(np.asarray(a,dtype='<f8').tobytes() for a in (lo,hi,bound))).hexdigest()

class LocalEnvelope:
    def __init__(self,certificate,model,config,lo,hi,bound):
        self.global_bound=validate_envelope(certificate,model,config)
        self.lo,self.hi,self.bound=[np.array(a,dtype=float,copy=True) for a in (lo,hi,bound)]
        depth=certificate['depth']
        if not isinstance(depth,int) or not 0<=depth<=18:raise ValueError('invalid partition depth')
        lower=np.asarray(certificate['domain_lower']);upper=np.asarray(certificate['domain_upper'])
        p=config['plant'];d=config['domain'];mg=p['mass_kg']*p['gravity_m_s2']
        expected_lo=np.array([d['state_lower'][2]/3,d['state_lower'][3]/3,d['state_lower'][4]/.45,d['input_lower'][0]/mg-1,d['input_lower'][1]/.08,*np.array(p['wind_bounds_m_s'])[:,0]])
        expected_hi=np.array([d['state_upper'][2]/3,d['state_upper'][3]/3,d['state_upper'][4]/.45,d['input_upper'][0]/mg-1,d['input_upper'][1]/.08,*np.array(p['wind_bounds_m_s'])[:,1]])
        if not np.array_equal(lower,expected_lo) or not np.array_equal(upper,expected_hi):raise ValueError('domain mismatch')
        a,b=lower[None,:],upper[None,:]
        for level in range(depth):
            j=level%7;mid=(a[:,j]+b[:,j])/2;left=b.copy();left[:,j]=mid;right=a.copy();right[:,j]=mid
            a,b=np.concatenate((a,right)),np.concatenate((left,b))
        if not np.array_equal(a,self.lo) or not np.array_equal(b,self.hi):raise ValueError('incomplete or reordered partition')
        if self.bound.shape!=(len(a),2) or not np.isfinite(self.bound).all() or np.any(self.bound<0):raise ValueError('invalid bounds')
        if not np.array_equal(self.bound.max(axis=0),self.global_bound):raise ValueError('global bound mismatch')
        if table_digest(self.lo,self.hi,self.bound)!=certificate['table_sha256']:raise ValueError('table hash mismatch')
        for x in (self.lo,self.hi,self.bound):x.flags.writeable=False
        self.lower,self.upper,self.config=lower,upper,config

    def query(self,z,u):
        s=features(z.center,u,self.config);r=np.abs(feature_state_matrix())@z.box.radius
        lo=np.r_[s-r,self.lower[5:]];hi=np.r_[s+r,self.upper[5:]]
        if not np.isfinite(lo).all() or not np.isfinite(hi).all() or np.any(lo<self.lower) or np.any(hi>self.upper):raise ValueError('query outside validated domain')
        selected=np.all(self.hi>=lo,axis=1)&np.all(self.lo<=hi,axis=1)
        if not selected.any():raise ValueError('uncovered query')
        return self.bound[selected].max(axis=0),int(selected.sum())
