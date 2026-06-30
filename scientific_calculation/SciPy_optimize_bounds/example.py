import numpy as np


def project_bounds(x, lower=None, upper=None):
    arr = np.asarray(x, dtype=float)
    if lower is not None:
        lo = np.asarray(lower, dtype=float)
        arr = np.maximum(arr, lo)
    if upper is not None:
        hi = np.asarray(upper, dtype=float)
        arr = np.minimum(arr, hi)
    if lower is not None and upper is not None and np.any(np.asarray(lower) > np.asarray(upper)):
        raise ValueError("lower bound exceeds upper bound")
    return arr


def bound_status(value, lower, upper, tolerance=1e-12):
    if lower > upper:
        raise ValueError("invalid bounds")
    if abs(value - lower) <= tolerance:
        return "lower"
    if abs(value - upper) <= tolerance:
        return "upper"
    if lower < value < upper:
        return "free"
    return "violated"
