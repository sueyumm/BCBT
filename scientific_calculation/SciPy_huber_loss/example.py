import numpy as np


def huber_loss(residuals, delta=1.0):
    r = np.asarray(residuals, dtype=float)
    if delta <= 0:
        raise ValueError("delta must be positive")
    abs_r = np.abs(r)
    quadratic = abs_r <= delta
    out = np.empty_like(abs_r)
    out[quadratic] = 0.5 * abs_r[quadratic] ** 2
    out[~quadratic] = delta * (abs_r[~quadratic] - 0.5 * delta)
    return out


def robust_region(residual, delta):
    if delta <= 0:
        raise ValueError("delta must be positive")
    if abs(residual) <= delta:
        return "quadratic"
    return "linear"
