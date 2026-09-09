"""Offline shared-variable affine difference bounds for the frozen analytic plant."""
import numpy as np
from .residual_envelope import envelope

class Form:
    def __init__(self,c,g,e):self.c,self.g,self.e=c,g,e
    @property
    def radius(self):return np.abs(self.g).sum(axis=-1)+self.e
    def __add__(self,b):
        if not isinstance(b,Form):return Form(self.c+b,self.g,self.e)
        return Form(self.c+b.c,self.g+b.g,self.e+b.e)
    __radd__=__add__
    def __mul__(self,b):
        if not isinstance(b,Form):return Form(self.c*b,self.g*b,self.e*abs(b))
        return Form(self.c*b.c,self.c[:,None]*b.g+b.c[:,None]*self.g,
                    np.abs(self.c)*b.e+np.abs(b.c)*self.e+self.radius*b.radius)
    __rmul__=__mul__
    def smooth(self,value,derivative,second_max):
        return Form(value(self.c),derivative(self.c)[:,None]*self.g,
                    np.abs(derivative(self.c))*self.e+.5*second_max*self.radius**2)

def analytic_affine(lo,hi):
    c=(lo+hi)/2;r=(hi-lo)/2;forms=[]
    for j in range(7):
        g=np.zeros((len(c),7));g[:,j]=r[:,j];forms.append(Form(c[:,j],g,np.zeros(len(c))))
    vx,vz,phi,t,torque,wx,wz=forms
    rx=3*vx+(-1)*wx;rz=3*vz+(-1)*wz
    drag=lambda v:v.smooth(lambda x:x*np.sqrt(x*x+.04),lambda x:(2*x*x+.04)/np.sqrt(x*x+.04),2.)
    sn=(.9*phi).smooth(np.sin,np.cos,1.)
    cs=(.45*phi).smooth(np.cos,lambda x:-np.sin(x),1.)
    return [-.12*drag(rx)+(-.03)*(rx*rz)+.08*(sn*t),-.15*drag(rz)+.02*(rx*rx*cs)]

def joint_envelope(model,config,depth=14):
    cert,lo,hi,old=envelope(model,config,depth)
    truth=analytic_affine(lo,hi)
    nc,ng,ne=model.affine_box(lo[:,:5],hi[:,:5]);ng=np.pad(ng,((0,0),(0,0),(0,2)))
    tc=np.stack([f.c for f in truth],axis=1);tg=np.stack([f.g for f in truth],axis=1);te=np.stack([f.e for f in truth],axis=1)
    bound=np.abs(tc-nc)+np.abs(tg-ng).sum(axis=-1)+te+ne
    bound+=1e-10*(1+bound);bound=np.minimum(bound,old)
    cert.update(algorithm='shared_affine_difference_intersection_v1',acceleration_halfwidth=bound.max(axis=0).tolist(),worst_leaf_indices=np.argmax(bound,axis=0).tolist())
    return cert,lo,hi,bound
