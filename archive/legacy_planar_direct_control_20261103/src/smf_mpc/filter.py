"""Causal physics-only box SMF; has no truth/wind/current-state input."""
import numpy as np
from .sets import Box, trig_range
from .sensing import ContractViolation


class OutOfDomain(ValueError):
    pass


def residual_halfwidth(config):
    """Conservative ANALYTIC formula in real arithmetic; numerical evaluation only.

    Global |a*| bound relative to the zero residual predictor, not a learned
    residual certificate. Uses coefficient assumptions from the benchmark.
    """
    d, p = config['domain'], config['plant']
    wind = np.asarray(p['wind_bounds_m_s'])
    rx, rz = [max(abs(d['state_lower'][j+2]-wind[j, 1]),
                  abs(d['state_upper'][j+2]-wind[j, 0])) for j in range(2)]
    Tdev = max(abs(t/(p['mass_kg']*p['gravity_m_s2'])-1) for t in (d['input_lower'][0], d['input_upper'][0]))
    accel = np.array([.12*rx*np.sqrt(rx*rx+.04)+.03*rx*rz+.08*Tdev,
                      .15*rz*np.sqrt(rz*rz+.04)+.02*rx*rx])
    w = np.array(p['external_process_halfwidth'], dtype=float)
    w[2:4] += p['dt_s']*accel
    return w


def predict(box, actual_u, config):
    d, p = config['domain'], config['plant']
    domain = Box(d['state_lower'], d['state_upper'])
    u = np.asarray(actual_u, dtype=float)
    if not domain.encloses(box) or not Box(d['input_lower'], d['input_upper']).contains(u):
        raise OutOfDomain('OUT_OF_DOMAIN: predictor evaluation')
    m, J, g, h = (p[k] for k in ('mass_kg','inertia_kg_m2','gravity_m_s2','dt_s'))
    if u[0] < 0:
        raise ValueError('negative thrust unsupported')
    lo, hi = box.lower, box.upper
    sl, sh = trig_range(lo[4], hi[4], 'sin'); cl, ch = trig_range(lo[4], hi[4], 'cos')
    flo = np.array([lo[2], lo[3], -u[0]*sh/m, u[0]*cl/m-g, lo[5], u[1]/J])
    fhi = np.array([hi[2], hi[3], -u[0]*sl/m, u[0]*ch/m-g, hi[5], u[1]/J])
    w = residual_halfwidth(config)
    # Engineering numerical allowance, deliberately NOT called outward rounding.
    low, high = lo+h*flo-w, hi+h*fhi+w
    margin = 1e-12*(1+np.maximum(np.abs(low), np.abs(high)))
    return Box(low-margin, high+margin)


def update(box, observation):
    lo, hi = box.lower.copy(), box.upper.copy()
    for j, value, radius in zip(observation.indices, observation.values, observation.noise_radius):
        lo[j], hi[j] = max(lo[j], value-radius), min(hi[j], value+radius)
    return Box(lo, hi)


class BoxSMF:
    def __init__(self, prior, observation, config):
        if observation.tick != 0:
            raise ContractViolation('initial observation must have tick zero')
        self.config = config
        self.domain = Box(config['domain']['state_lower'], config['domain']['state_upper'])
        self.tick = 0
        self.missed = 0
        self.missed = self._observation_contract(observation)
        self.box = update(prior, observation)
        self._check_domain(self.box)

    def _observation_contract(self, obs):
        sense = self.config['sensing']
        always = set(sense['always_observed_indices'])
        position = set(sense['position_indices'])
        received = set(obs.indices)
        if received not in (always, always | position):
            raise ContractViolation('unexpected measured state channels')
        arrived = position <= received
        opportunity = obs.tick % sense['position_period_ticks'] == 0
        if arrived and not opportunity:
            raise ContractViolation('unexpected position packet timing')
        missed = (0 if arrived else self.missed+1) if opportunity else self.missed
        if missed > sense['max_consecutive_missed_packets']:
            raise ContractViolation('TOO_MANY_MISSING_PACKETS')
        bounds = sense['observed_noise_halfwidth']
        expected = [bounds[self.config['state_order'][j]] for j in obs.indices]
        if not np.array_equal(obs.noise_radius, expected):
            raise ContractViolation('measurement bound differs from configured contract')
        return missed

    def _check_domain(self, box):
        if not self.domain.encloses(box):
            raise OutOfDomain('OUT_OF_DOMAIN: posterior cannot support next prediction')

    def advance(self, actual_u, observation):
        if observation.tick != self.tick+1:
            raise ContractViolation('observation must correct next predicted time')
        missed = self._observation_contract(observation)
        prior = predict(self.box, actual_u, self.config)
        posterior = update(prior, observation)
        self._check_domain(posterior)
        self.box, self.tick, self.missed = posterior, observation.tick, missed
        return posterior
