import numpy as np


def covariance_inputs(x, y=None, rowvar=True):
    x_arr = np.asarray(x, dtype=float)
    if x_arr.ndim == 0:
        raise ValueError("x must contain at least one observation")
    if x_arr.ndim == 1:
        x_arr = x_arr.reshape(1, -1) if rowvar else x_arr.reshape(-1, 1)
    elif not rowvar:
        x_arr = x_arr.T

    if y is None:
        return x_arr

    y_arr = np.asarray(y, dtype=float)
    if y_arr.ndim == 1:
        y_arr = y_arr.reshape(1, -1) if rowvar else y_arr.reshape(-1, 1)
    elif not rowvar:
        y_arr = y_arr.T
    if x_arr.shape[1] != y_arr.shape[1]:
        raise ValueError("x and y must contain the same number of observations")
    return np.concatenate([x_arr, y_arr], axis=0)


def covariance_normalization(count, ddof=1, frequency_weights=None):
    if count <= 0:
        raise ValueError("count must be positive")
    if ddof < 0:
        raise ValueError("ddof must be non-negative")
    if frequency_weights is None:
        factor = count - ddof
    else:
        weights = np.asarray(frequency_weights, dtype=float)
        if np.any(weights < 0):
            raise ValueError("weights must be non-negative")
        factor = weights.sum() - ddof
    if factor <= 0:
        raise ValueError("normalization factor must be positive")
    return float(factor)
