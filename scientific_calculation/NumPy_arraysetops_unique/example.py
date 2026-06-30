import numpy as np


def unique_1d(values, return_counts=False, drop_nan=False):
    arr = np.asarray(values)
    if arr.ndim != 1:
        arr = arr.ravel()
    seen = []
    counts = []
    for value in arr:
        if drop_nan and isinstance(value, float) and np.isnan(value):
            continue
        if value in seen:
            counts[seen.index(value)] += 1
        else:
            seen.append(value)
            counts.append(1)
    uniques = np.asarray(seen)
    if return_counts:
        return uniques, np.asarray(counts, dtype=int)
    return uniques


def set_operation(left, right, op="intersect"):
    a, b = set(left), set(right)
    if op == "intersect":
        return sorted(a & b)
    if op == "union":
        return sorted(a | b)
    if op == "difference":
        return sorted(a - b)
    raise ValueError("unknown operation")
