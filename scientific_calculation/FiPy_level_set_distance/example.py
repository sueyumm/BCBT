import numpy as np


def signed_distance_1d(x, interface_position):
    x = np.asarray(x, dtype=float)
    return x - interface_position


def reinitialize_level_set(phi, dx, iterations=5):
    phi = np.asarray(phi, dtype=float)
    if phi.ndim != 1:
        raise ValueError("phi must be one-dimensional")
    if dx <= 0 or iterations < 0:
        raise ValueError("invalid dx or iterations")
    out = phi.copy()
    sign = np.sign(phi)
    for _ in range(iterations):
        if len(out) < 3:
            break
        grad = np.zeros_like(out)
        grad[1:-1] = (out[2:] - out[:-2]) / (2.0 * dx)
        out -= 0.5 * dx * sign * (np.abs(grad) - 1.0)
    return out


def interface_crossed(phi):
    phi = np.asarray(phi, dtype=float)
    return bool(np.any(phi[:-1] * phi[1:] <= 0)) if len(phi) > 1 else False
