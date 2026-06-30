import numpy as np


def nanmean_with_min_count(values, min_count=1):
    arr = np.asarray(values, dtype=float)
    if min_count < 0:
        raise ValueError("min_count must be non-negative")
    mask = ~np.isnan(arr)
    count = int(mask.sum())
    if count < min_count:
        return np.nan
    if count == 0:
        return np.nan
    return float(arr[mask].mean())


def nanarg_extreme(values, mode="max"):
    arr = np.asarray(values, dtype=float)
    if arr.size == 0 or np.all(np.isnan(arr)):
        raise ValueError("all values are NaN")
    if mode == "max":
        return int(np.nanargmax(arr))
    if mode == "min":
        return int(np.nanargmin(arr))
    raise ValueError("mode must be 'max' or 'min'")
