import numpy as np


def tensor_symmetry_error(tensor, tol=1e-8):
    a = np.asarray(tensor, dtype=float)
    if a.ndim != 2 or a.shape[0] != a.shape[1]:
        raise ValueError("square matrix required")
    err = np.max(np.abs(a - a.T))
    if err <= tol:
        return "symmetric"
    if err <= 10 * tol:
        return "nearly-symmetric"
    return "nonsymmetric"
