import numpy as np


def outer_edges(values, value_range=None):
    arr = np.asarray(values, dtype=float)
    if arr.size == 0 and value_range is None:
        raise ValueError("cannot infer edges from empty values")
    if value_range is not None:
        first, last = value_range
    else:
        first, last = float(np.nanmin(arr)), float(np.nanmax(arr))
    if not np.isfinite(first) or not np.isfinite(last):
        raise ValueError("edges must be finite")
    if first > last:
        raise ValueError("left edge cannot exceed right edge")
    if first == last:
        first -= 0.5
        last += 0.5
    return first, last


def bin_count_rule(values, rule="sqrt"):
    n = len(values)
    if n == 0:
        return 1
    if rule == "sqrt":
        return int(np.ceil(np.sqrt(n)))
    if rule == "sturges":
        return int(np.ceil(np.log2(n) + 1))
    raise ValueError("unknown bin rule")
