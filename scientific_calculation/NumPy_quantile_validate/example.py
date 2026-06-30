import numpy as np


def validate_quantiles(q):
    arr = np.asarray(q, dtype=float)
    if arr.size == 0:
        raise ValueError("quantiles cannot be empty")
    if np.any(np.isnan(arr)):
        raise ValueError("quantiles cannot contain NaN")
    if np.any((arr < 0) | (arr > 1)):
        raise ValueError("quantiles must be in [0, 1]")
    if np.any(np.diff(np.ravel(arr)) < 0):
        return "unsorted"
    return "sorted"


def interpolation_weight(q, lower_index, upper_index):
    if upper_index < lower_index:
        raise ValueError("upper index cannot be smaller")
    if upper_index == lower_index:
        return 0.0
    position = q * (upper_index - lower_index)
    return float(position - np.floor(position))
