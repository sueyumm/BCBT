import numpy as np


def apply_boundary_1d(values, left=None, right=None, mode="dirichlet"):
    values = np.asarray(values, dtype=float).copy()
    if values.ndim != 1:
        raise ValueError("values must be one-dimensional")
    if values.size == 0:
        return values
    if mode == "dirichlet":
        if left is not None:
            values[0] = left
        if right is not None:
            values[-1] = right
    elif mode == "neumann":
        if len(values) > 1 and left is not None:
            values[0] = values[1] - left
        if len(values) > 1 and right is not None:
            values[-1] = values[-2] + right
    else:
        raise ValueError("unsupported boundary mode")
    return values


def boundary_is_fixed(left=None, right=None):
    return left is not None or right is not None
