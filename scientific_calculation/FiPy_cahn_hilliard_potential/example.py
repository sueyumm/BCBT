import numpy as np


def chemical_potential(phi, gradient_penalty=1.0):
    phi = np.asarray(phi, dtype=float)
    if gradient_penalty < 0:
        raise ValueError("gradient_penalty must be non-negative")
    bulk = phi**3 - phi
    if phi.ndim == 1 and len(phi) >= 3:
        laplace = np.zeros_like(phi)
        laplace[1:-1] = phi[:-2] - 2.0 * phi[1:-1] + phi[2:]
        return bulk - gradient_penalty * laplace
    return bulk


def phase_separated(phi, threshold=0.8):
    if threshold <= 0:
        raise ValueError("threshold must be positive")
    phi = np.asarray(phi, dtype=float)
    return bool(np.any(phi > threshold) and np.any(phi < -threshold))
