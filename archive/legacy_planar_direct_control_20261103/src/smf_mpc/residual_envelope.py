"""Whole-domain partition envelope under analytic plant assumptions; float64 only."""
import numpy as np
from .neural_model import config_digest


def product(al,ah,bl,bh):
    values=np.stack((al*bl,al*bh,ah*bl,ah*bh))
    return values.min(axis=0),values.max(axis=0)


def true_acceleration_interval(lo,hi):
    """Seven coordinates: normalized five features, physical two wind velocities.

    Restricted to the frozen planar domain: |phi|<=.45; thus sin(2phi) monotone.
    """
    rxlo,rxhi=3*lo[:,0]-hi[:,5],3*hi[:,0]-lo[:,5]
    rzlo,rzhi=3*lo[:,1]-hi[:,6],3*hi[:,1]-lo[:,6]
    drag=lambda r:r*np.sqrt(r*r+.04)
    cxlo,cxhi=product(rxlo,rxhi,rzlo,rzhi)
    slo,shi=np.sin(.9*lo[:,2]),np.sin(.9*hi[:,2])
    txlo,txhi=product(slo,shi,lo[:,3],hi[:,3])
    alo=-.12*drag(rxhi)-.03*cxhi+.08*txlo
    ahi=-.12*drag(rxlo)-.03*cxlo+.08*txhi
    squarelo=np.where((rxlo<=0)&(rxhi>=0),0,np.minimum(rxlo**2,rxhi**2))
    squarehi=np.maximum(rxlo**2,rxhi**2)
    cl=np.minimum(np.cos(.45*lo[:,2]),np.cos(.45*hi[:,2]))
    ch=np.where((lo[:,2]<=0)&(hi[:,2]>=0),1,np.maximum(np.cos(.45*lo[:,2]),np.cos(.45*hi[:,2])))
    blo=-.15*drag(rzhi)+.02*squarelo*cl
    bhi=-.15*drag(rzlo)+.02*squarehi*ch
    return np.column_stack((alo,blo)),np.column_stack((ahi,bhi))


def envelope(model,config,depth=12):
    d=config['domain'];p=config['plant']
    # This certificate implementation is explicitly scoped; fail closed for a new domain.
    if d['state_lower'][2:]!=[-3,-3,-.45,-2] or d['state_upper'][2:]!=[3,3,.45,2]:raise ValueError('unsupported certificate state domain')
    if p['wind_bounds_m_s']!=[[-.5,.5],[-.5,.5]]:raise ValueError('unsupported wind domain')
    mg=p['mass_kg']*p['gravity_m_s2']
    lower=np.array([-1,-1,-1,d['input_lower'][0]/mg-1,d['input_lower'][1]/.08,-.5,-.5])
    upper=np.array([1,1,1,d['input_upper'][0]/mg-1,d['input_upper'][1]/.08,.5,.5])
    if depth<0 or depth>18:raise ValueError('partition depth outside budget')
    lo,hi=lower[None,:],upper[None,:]
    # Deterministic balanced bisection covers all cells; no difficult leaf is dropped.
    for level in range(depth):
        axis=level%7;mid=(lo[:,axis]+hi[:,axis])/2
        left_hi=hi.copy();left_hi[:,axis]=mid
        right_lo=lo.copy();right_lo[:,axis]=mid
        lo,hi=np.concatenate((lo,right_lo)),np.concatenate((left_hi,hi))
    true_lo,true_hi=true_acceleration_interval(lo,hi)
    nn_lo,nn_hi=model.interval(lo[:,:5],hi[:,:5])
    bound=np.maximum(np.abs(true_lo-nn_hi),np.abs(true_hi-nn_lo))
    # Engineering inflation, not a rigorous rounding analysis.
    bound+=1e-10*(1+bound)
    result={'kind':'CONDITIONAL_ANALYTIC_PARTITION_FLOAT64_NOT_CERTIFIED',
        'model_sha256':model.digest(),'config_sha256':config_digest(config),
        'depth':depth,'leaf_count':len(lo),'domain_lower':lower.tolist(),'domain_upper':upper.tolist(),
        'acceleration_halfwidth':bound.max(axis=0).tolist(),
        'algorithm':'balanced_midpoint_cycle_7_axes_v1','worst_leaf_indices':np.argmax(bound,axis=0).tolist()}
    return result,lo,hi,bound


def validate_envelope(certificate,model,config):
    if certificate.get('kind')!='CONDITIONAL_ANALYTIC_PARTITION_FLOAT64_NOT_CERTIFIED':raise ValueError('unsupported envelope status')
    if certificate['model_sha256']!=model.digest() or certificate['config_sha256']!=config_digest(config):raise ValueError('INVALID_MODEL_OR_CONFIG_HASH')
    bound=np.asarray(certificate['acceleration_halfwidth'])
    if bound.shape!=(2,) or not np.isfinite(bound).all() or np.any(bound<0):raise ValueError('invalid residual bound')
    return bound
