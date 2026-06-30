import numpy as np


def residual_norm(residual, norm_type="l2"):
    residual = np.asarray(residual, dtype=float)
    if residual.size == 0:
        return 0.0
    if norm_type == "l2":
        return float(np.sqrt(np.sum(residual * residual)))
    if norm_type == "linf":
        return float(np.max(np.abs(residual)))
    if norm_type == "l1":
        return float(np.sum(np.abs(residual)))
    raise ValueError("unknown norm type")


def should_continue(residual, tolerance, iteration, max_iterations):
    if tolerance < 0 or max_iterations < 0:
        raise ValueError("invalid tolerance or iteration limit")
    if iteration >= max_iterations:
        return False
    return residual_norm(residual) > tolerance
