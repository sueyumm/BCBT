import numpy as np


def poisson_residual(u, rhs, dx):
    u = np.asarray(u, dtype=float)
    rhs = np.asarray(rhs, dtype=float)
    if u.shape != rhs.shape:
        raise ValueError("u and rhs must have the same shape")
    if u.ndim != 2:
        raise ValueError("u must be two-dimensional")
    if dx <= 0:
        raise ValueError("dx must be positive")
    residual = np.zeros_like(u)
    if min(u.shape) < 3:
        return rhs - residual
    laplace = (
        u[:-2, 1:-1]
        + u[2:, 1:-1]
        + u[1:-1, :-2]
        + u[1:-1, 2:]
        - 4.0 * u[1:-1, 1:-1]
    ) / (dx * dx)
    residual[1:-1, 1:-1] = rhs[1:-1, 1:-1] - laplace
    return residual


def converged(residual, tolerance):
    if tolerance < 0:
        raise ValueError("tolerance must be non-negative")
    norm = float(np.linalg.norm(np.asarray(residual, dtype=float)))
    return norm <= tolerance
