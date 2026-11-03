"""Model-A residual dynamics in a numerical zonotope filter; no truth import."""
import numpy as np
from .zonotope_filter import ZonotopeSMF,predict_zonotope,nominal_step_and_jacobian,measurement_update
from .neural_model import features,feature_state_matrix
from .residual_envelope import validate_envelope
from .sets import Zonotope
from .sensing import ContractViolation


def local_learned_prediction(z,u,config,model,certificate,table):
    accel_bound,leaf_count=table.query(z,u)
    physical,details=predict_zonotope(z,u,config)
    _,A=nominal_step_and_jacobian(z.center,u,config)
    h=config['plant']['dt_s'];D=feature_state_matrix();s=features(z.center,u,config)
    ds=np.abs(D)@z.box.radius
    nn_remainder=model.affine_remainder(s-ds,s+ds)
    center=physical.center.copy();center[2:4]+=h*model.predict(s)
    A[2:4]+=h*model.jacobian(s)@D
    w=np.array(config['plant']['external_process_halfwidth'],dtype=float);w[2:4]+=h*accel_bound
    remainder=details['remainder_radius'].copy();remainder[2:4]+=h*nn_remainder
    linear=A@z.generators
    margin=1e-12*(1+np.abs(center)+np.abs(linear).sum(axis=1)+w+remainder)
    out=Zonotope(center,np.column_stack((linear,np.diag(w+remainder+margin))))
    return out,{'queried_leaf_count':leaf_count,'model_radius':w,'remainder_radius':remainder,'neural_remainder_radius':h*nn_remainder,
                'linear_radius':np.abs(linear).sum(axis=1)}


class LocalLearnedZonotopeSMF(ZonotopeSMF):
    def __init__(self,prior,observation,config,model,certificate,table,max_generators=60):
        validate_envelope(certificate,model,config)
        self.model,self.certificate,self.table=model,certificate,table
        super().__init__(prior,observation,config,max_generators)

    def advance(self,actual_u,observation):
        if observation.tick!=self.tick+1:raise ContractViolation('observation must correct next predicted time')
        missed=self._observation_contract(observation)
        prediction,diag=local_learned_prediction(self.zonotope,actual_u,self.config,self.model,self.certificate,self.table)
        updated=measurement_update(prediction,observation);reduced=updated.reduce(self.max_generators)
        diag.update({'prediction_radius':prediction.box.radius,'measurement_radius':updated.box.radius,'reduced_radius':reduced.box.radius,
                     'generators_before':updated.generators.shape[1],'generators_after':reduced.generators.shape[1]})
        before=np.abs(self.directions@updated.generators).sum(axis=1);after=np.abs(self.directions@reduced.generators).sum(axis=1)
        diag['reduction_mixed_width_increase']=float(2*np.max(after-before))
        self._check_domain(reduced.box)
        self.zonotope,self.box,self.tick,self.missed=reduced,reduced.box,observation.tick,missed
        self.diagnostics=diag
        return self.box
