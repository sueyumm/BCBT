import numpy as np


def nonlinear_convergence_status(residual_history, absolute_tol=1e-8, relative_tol=1e-6):
    residuals = np.asarray(residual_history, dtype=float)
    if residuals.ndim != 1 or residuals.size == 0:
        raise ValueError("residual history must be a non-empty vector")
    if absolute_tol < 0 or relative_tol < 0:
        raise ValueError("tolerances must be non-negative")
    initial = residuals[0]
    current = residuals[-1]
    if current <= absolute_tol:
        return "absolute"
    if initial > 0 and current / initial <= relative_tol:
        return "relative"
    if residuals.size >= 2 and current > residuals[-2]:
        return "diverging"
    return "iterating"


def damping_factor(residual_old, residual_new, default=1.0):
    if residual_old < 0 or residual_new < 0:
        raise ValueError("residuals must be non-negative")
    if residual_old == 0:
        return 0.0
    ratio = residual_new / residual_old
    if ratio < 0.5:
        return default
    if ratio < 1.0:
        return 0.5 * default
    return 0.25 * default
