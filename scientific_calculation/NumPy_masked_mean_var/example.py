import numpy as np


def masked_mean(values, mask=None):
    arr = np.asarray(values, dtype=float)
    if mask is None:
        mask_arr = np.zeros(arr.shape, dtype=bool)
    else:
        mask_arr = np.asarray(mask, dtype=bool)
    if mask_arr.shape != arr.shape:
        raise ValueError("mask shape must match values")
    valid = arr[~mask_arr]
    if valid.size == 0:
        return np.nan
    return float(valid.mean())


def masked_variance(values, mask=None, ddof=0):
    arr = np.asarray(values, dtype=float)
    mean = masked_mean(arr, mask)
    if np.isnan(mean):
        return np.nan
    valid = arr if mask is None else arr[~np.asarray(mask, dtype=bool)]
    if valid.size - ddof <= 0:
        raise ValueError("degrees of freedom are not positive")
    return float(((valid - mean) ** 2).sum() / (valid.size - ddof))
