"""Tangent affine enclosure with exact scalar tanh residual extrema (float64)."""
import numpy as np
from .neural_model import ResidualMLP


class AffineResidualMLP(ResidualMLP):
    def affine_box(self, lo, hi):
        lo, hi = np.asarray(lo, dtype=float), np.asarray(hi, dtype=float)
        if lo.shape != hi.shape or lo.shape[-1] != 5 or np.any(lo > hi):
            raise ValueError('invalid input box')
        center = (lo + hi) / 2
        radius = (hi - lo) / 2
        generators = radius[..., :, None] * np.eye(5)
        error = np.zeros_like(center)
        for layer in range(3):
            W, b = self.arrays[2*layer:2*layer+2]
            center = center @ W.T + b
            generators = np.einsum('ij,...jk->...ik', W, generators)
            error = error @ np.abs(W).T
            if layer == 2:
                break
            width = np.abs(generators).sum(axis=-1) + error
            lower, upper = center-width, center+width
            value = np.tanh(center)
            slope = 1-value*value
            # q(z)=tanh(z)-tanh(c)-sech²(c)(z-c).
            # q'(z)=0 at z=+/-|c|; endpoints and these points suffice.
            def residual(z):
                return np.tanh(z)-value-slope*(z-center)
            remainder = np.maximum(np.abs(residual(lower)), np.abs(residual(upper)))
            for critical in (np.abs(center), -np.abs(center)):
                remainder = np.maximum(remainder, np.where(
                    (lower <= critical) & (critical <= upper), np.abs(residual(critical)), 0))
            error = slope*error + remainder
            generators = slope[..., :, None]*generators
            center = value
        # Engineering margin, not directed-rounding certification.
        error += 1e-12*(1+np.abs(center)+np.abs(generators).sum(axis=-1)+error)
        return center, generators, error

    def interval(self, lo, hi):
        center, generators, error = self.affine_box(lo, hi)
        width = np.abs(generators).sum(axis=-1)+error
        old_lo, old_hi = super().interval(lo, hi)
        return np.maximum(old_lo, center-width), np.minimum(old_hi, center+width)

    def affine_remainder(self, lo, hi):
        return self.affine_box(lo, hi)[2]
