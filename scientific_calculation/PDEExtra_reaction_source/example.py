import numpy as np


def reaction_source(u, rate, carrying_capacity=1.0):
    arr = np.asarray(u, dtype=float)
    if carrying_capacity <= 0:
        raise ValueError("carrying_capacity must be positive")
    source = rate * arr * (1.0 - arr / carrying_capacity)
    if rate == 0:
        return np.zeros_like(arr)
    if rate > 0:
        return np.maximum(source, -abs(rate) * carrying_capacity)
    return np.minimum(source, abs(rate) * carrying_capacity)
