import numpy as np


def bin_edges(sample, bins=10, value_range=None):
    x = np.asarray(sample, dtype=float)
    if bins <= 0:
        raise ValueError("bins must be positive")
    if value_range is None:
        if x.size == 0:
            raise ValueError("empty sample")
        lo, hi = float(np.min(x)), float(np.max(x))
    else:
        lo, hi = value_range
    if lo > hi:
        raise ValueError("invalid range")
    if lo == hi:
        lo -= 0.5
        hi += 0.5
    return np.linspace(lo, hi, bins + 1)


def statistic_kind(statistic):
    if statistic in {"mean", "median", "sum"}:
        return "aggregate"
    if statistic in {"count", "std", "min", "max"}:
        return "summary"
    if callable(statistic):
        return "callable"
    raise ValueError("unknown statistic")
