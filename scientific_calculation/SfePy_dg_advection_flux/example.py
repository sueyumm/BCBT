import numpy as np


def numerical_flux(left_state, right_state, normal, velocity, scheme="upwind"):
    left = np.asarray(left_state, dtype=float)
    right = np.asarray(right_state, dtype=float)
    n = np.asarray(normal, dtype=float)
    v = np.asarray(velocity, dtype=float)
    if left.shape != right.shape:
        raise ValueError("left and right states must have the same shape")
    if n.shape != v.shape:
        raise ValueError("normal and velocity must have the same dimension")
    speed = float(np.dot(v, n))
    if scheme == "central":
        state = 0.5 * (left + right)
    elif scheme == "upwind":
        state = left if speed >= 0.0 else right
    else:
        raise ValueError("unknown flux scheme")
    return speed * state


def apply_limiter(values, lower=None, upper=None):
    vals = np.asarray(values, dtype=float)
    if lower is not None and upper is not None and lower > upper:
        raise ValueError("lower limit cannot exceed upper limit")
    if lower is not None:
        vals = np.maximum(vals, lower)
    if upper is not None:
        vals = np.minimum(vals, upper)
    return vals
