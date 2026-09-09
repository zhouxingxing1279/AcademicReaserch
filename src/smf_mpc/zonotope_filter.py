"""Nonlinear nominal-physics zonotope SMF, using numerical outer bounds.

No neural model, no truth import, no certified floating-point arithmetic.
"""
import numpy as np
from scipy.optimize import linprog
from .filter import BoxSMF, OutOfDomain, residual_halfwidth
from .sets import Box, Zonotope, EmptySet, trig_range
from .sensing import ContractViolation


class NumericalFailure(RuntimeError):
    pass


def lp_witness(matrix, rhs, tolerance=1e-8):
    """Numerical feasibility in the unit box; uncertainty is never silently accepted."""
    # Equivalent positive row scaling avoids mixing metres and milliradians.
    scale = np.maximum(np.maximum(np.max(np.abs(matrix),axis=1),np.abs(rhs)),1e-12)
    result = linprog(np.zeros(matrix.shape[1]), A_eq=matrix/scale[:,None], b_eq=rhs/scale,
                     bounds=[(-1, 1)]*matrix.shape[1], method='highs',
                     options={'primal_feasibility_tolerance':1e-9, 'dual_feasibility_tolerance':1e-9})
    if result.status == 2:
        return False
    if not result.success:
        raise NumericalFailure(f'LP status {result.status}: {result.message}')
    if (np.max(np.abs(matrix@result.x-rhs)) > tolerance or
            np.max(np.abs(result.x)) > 1+tolerance):
        raise NumericalFailure('LP witness outside residual/coefficient tolerance')
    return True


def contains(z, point):
    return lp_witness(z.generators, np.asarray(point)-z.center)


def nominal_step_and_jacobian(x, u, config):
    p = config['plant']
    m, J, g, h = (p[k] for k in ('mass_kg','inertia_kg_m2','gravity_m_s2','dt_s'))
    x, u = np.asarray(x), np.asarray(u)
    phi, T = x[4], u[0]
    f = x+h*np.array([x[2],x[3],-T*np.sin(phi)/m,T*np.cos(phi)/m-g,x[5],u[1]/J])
    A = np.eye(6); A[0,2] = A[1,3] = A[4,5] = h
    A[2,4], A[3,4] = -h*T*np.cos(phi)/m, -h*T*np.sin(phi)/m
    return f, A


def predict_zonotope(z, actual_u, config):
    box = z.box; d, p = config['domain'], config['plant']
    u = np.asarray(actual_u)
    if not Box(d['state_lower'],d['state_upper']).encloses(box):
        raise OutOfDomain('OUT_OF_DOMAIN: zonotope predictor evaluation')
    if not Box(d['input_lower'],d['input_upper']).contains(u) or u[0] < 0:
        raise OutOfDomain('OUT_OF_DOMAIN: applied input')
    f, A = nominal_step_and_jacobian(z.center, u, config)
    # Only phi-phi second derivatives are nonzero for this fixed-input model.
    sin_bound = max(abs(v) for v in trig_range(box.lower[4],box.upper[4],'sin'))
    cos_bound = max(abs(v) for v in trig_range(box.lower[4],box.upper[4],'cos'))
    remainder = np.zeros(6)
    factor = .5*p['dt_s']*u[0]/p['mass_kg']*box.radius[4]**2
    remainder[2:4] = factor*np.array([sin_bound,cos_bound])
    w = residual_halfwidth(config)
    linear_generators = A@z.generators
    margin = 1e-12*(1+np.abs(f)+np.abs(linear_generators).sum(axis=1)+w+remainder)
    prediction = Zonotope(f,np.column_stack((linear_generators,np.diag(w+remainder+margin))))
    return prediction, {'linear_radius':np.abs(linear_generators).sum(axis=1),
                        'model_radius':w, 'remainder_radius':remainder, 'roundoff_margin':margin}


def measurement_update(z, observation):
    C = np.eye(6)[list(observation.indices)]
    noise = np.diag(observation.noise_radius)
    if not lp_witness(np.column_stack((C@z.generators,noise)),observation.values-C@z.center):
        raise EmptySet('EMPTY_SET: numerical strip consistency LP')
    return z.strip(C,observation.values,observation.noise_radius)


class ZonotopeSMF(BoxSMF):
    """Reuse observation/domain contracts, not box prediction or recentering.

    Per-step state is committed only after all checks, so failed updates are atomic.
    """
    def __init__(self, prior, observation, config, max_generators=30):
        if observation.tick != 0 or max_generators < 6:
            raise ValueError('invalid initial tick or generator budget')
        self.config = config
        self.domain = Box(config['domain']['state_lower'],config['domain']['state_upper'])
        self.tick, self.missed, self.max_generators = 0,0,max_generators
        missed = self._observation_contract(observation)
        z = measurement_update(Zonotope(prior.center,np.diag(prior.radius)),observation).reduce(max_generators)
        self._check_domain(z.box)
        self.zonotope,self.box,self.missed = z,z.box,missed
        scale = np.asarray(config['training']['state_width_scale'])
        basis = np.diag(1/scale)
        self.directions = np.array([(basis[i]+sign*basis[j])/np.sqrt(2)
                                    for i in range(6) for j in range(i+1,6) for sign in (-1,1)])
        self.diagnostics = {}

    def advance(self, actual_u, observation):
        if observation.tick != self.tick+1:
            raise ContractViolation('observation must correct next predicted time')
        missed = self._observation_contract(observation)
        prediction, diag = predict_zonotope(self.zonotope,actual_u,self.config)
        updated = measurement_update(prediction,observation)
        reduced = updated.reduce(self.max_generators)
        diag.update({'prediction_radius':prediction.box.radius,'measurement_radius':updated.box.radius,
                     'reduced_radius':reduced.box.radius,
                     'generators_before':updated.generators.shape[1],
                     'generators_after':reduced.generators.shape[1]})
        support_before = np.abs(self.directions@updated.generators).sum(axis=1)
        support_after = np.abs(self.directions@reduced.generators).sum(axis=1)
        diag['reduction_mixed_width_increase'] = float(2*np.max(support_after-support_before))
        self._check_domain(reduced.box)
        self.zonotope,self.box,self.tick,self.missed = reduced,reduced.box,observation.tick,missed
        self.diagnostics = diag
        return self.box
