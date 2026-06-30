import numpy as np


def coerce_numeric(values, errors="raise"):
    result = []
    for value in values:
        try:
            result.append(float(value))
        except (TypeError, ValueError):
            if errors == "raise":
                raise
            if errors == "coerce":
                result.append(np.nan)
            elif errors == "ignore":
                result.append(value)
            else:
                raise ValueError("unknown error mode")
    return np.asarray(result, dtype=object if errors == "ignore" else float)


def numeric_kind(values):
    arr = np.asarray(values)
    if arr.size == 0:
        return "empty"
    if np.issubdtype(arr.dtype, np.integer):
        return "integer"
    if np.issubdtype(arr.dtype, np.floating):
        return "floating"
    return "other"
