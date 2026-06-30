import numpy as np


def factorize_values(values, sort=False, missing_value=None):
    uniques = []
    codes = []
    for value in values:
        if value == missing_value:
            codes.append(-1)
            continue
        if value not in uniques:
            uniques.append(value)
        codes.append(uniques.index(value))
    if sort:
        ordered = sorted(uniques)
        remap = {old: ordered.index(value) for old, value in enumerate(uniques)}
        codes = [-1 if code == -1 else remap[code] for code in codes]
        uniques = ordered
    return np.asarray(codes, dtype=int), uniques


def rank_method(values, method="average"):
    arr = np.asarray(values, dtype=float)
    order = np.argsort(arr)
    ranks = np.empty(arr.size, dtype=float)
    for rank, index in enumerate(order, start=1):
        ranks[index] = rank
    if method == "ordinal":
        return ranks
    if method != "average":
        raise ValueError("unknown rank method")
    for value in np.unique(arr):
        mask = arr == value
        if mask.sum() > 1:
            ranks[mask] = ranks[mask].mean()
    return ranks
