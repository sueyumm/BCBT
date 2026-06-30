import numpy as np


def remove_nan_1d(values, overwrite_input=False):
    arr = np.asarray(values, dtype=float)
    if arr.ndim != 1:
        raise ValueError("values must be one-dimensional")
    if overwrite_input:
        arr = arr.copy()
    mask = np.isnan(arr)
    if not mask.any():
        return arr
    if mask.all():
        return np.asarray([], dtype=float)
    return arr[~mask]


def nan_policy(values):
    arr = np.asarray(values, dtype=float)
    if arr.size == 0:
        return "empty"
    if np.isnan(arr).all():
        return "all-nan"
    if np.isnan(arr).any():
        return "some-nan"
    return "clean"
