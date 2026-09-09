"""Offline truth generator. Online filter must never import this module."""
import numpy as np
from .sensing import Observation


def aerodynamic_acceleration(x, u, wind, mass=1.0, gravity=9.81):
    rx, rz = x[2:4]-np.asarray(wind)
    phi, T = x[4], u[0]
    return np.array([-.12*rx*np.sqrt(rx*rx+.04)-.03*rx*rz+.08*np.sin(2*phi)*(T/(mass*gravity)-1),
                     -.15*rz*np.sqrt(rz*rz+.04)+.02*rx*rx*np.cos(phi)])


def step(x, u, wind, config, external=None):
    x, u, wind = np.asarray(x, dtype=float), np.asarray(u, dtype=float), np.asarray(wind, dtype=float)
    if x.shape != (6,) or u.shape != (2,) or wind.shape != (2,) or not np.isfinite(np.r_[x, u, wind]).all():
        raise ValueError('invalid plant input')
    p = config['plant']; m, J, g, h = (p[k] for k in ('mass_kg','inertia_kg_m2','gravity_m_s2','dt_s'))
    a = aerodynamic_acceleration(x, u, wind, m, g)
    dx = np.array([x[2], x[3], -u[0]*np.sin(x[4])/m+a[0],
                   u[0]*np.cos(x[4])/m-g+a[1], x[5], u[1]/J])
    ext = np.zeros(6) if external is None else np.asarray(external)
    if ext.shape != (6,) or not np.isfinite(ext).all():
        raise ValueError('invalid external process increment')
    return x+h*dx+ext


def observe(x, tick, indices, potential_noise, config):
    """Potential noise exists offline on every tick, masked before filter API."""
    names = config['state_order']; bounds = config['sensing']['observed_noise_halfwidth']
    radius = np.array([bounds[names[j]] for j in indices])
    noise = np.asarray(potential_noise)[list(indices)]
    if np.any(np.abs(noise) > 1):
        raise ValueError('unit noise exceeds bound')
    return Observation(tick, tuple(indices), np.asarray(x)[list(indices)]+radius*noise, radius)
