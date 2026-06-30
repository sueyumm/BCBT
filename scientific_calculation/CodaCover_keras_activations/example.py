import numpy as np


def activation(values, kind="relu", alpha=0.01):
    x = np.asarray(values, dtype=float)
    if kind == "relu":
        return np.maximum(x, 0.0)
    if kind == "leaky_relu":
        if alpha < 0:
            raise ValueError("alpha must be non-negative")
        return np.where(x >= 0, x, alpha * x)
    if kind == "sigmoid":
        return 1.0 / (1.0 + np.exp(-x))
    if kind == "tanh":
        return np.tanh(x)
    raise ValueError("unknown activation")


def activation_region(value, threshold=0.0):
    if value > threshold:
        return "active"
    if value == threshold:
        return "boundary"
    return "inactive"
