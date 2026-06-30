import math
import numpy as np


def symlog_transform(values, linthresh=1.0, base=10.0):
    vals = np.asarray(values, dtype=float)
    if linthresh <= 0:
        raise ValueError("linthresh must be positive")
    if base <= 1:
        raise ValueError("base must be greater than one")
    out = np.empty_like(vals)
    linear = np.abs(vals) <= linthresh
    out[linear] = vals[linear] / linthresh
    out[~linear] = np.sign(vals[~linear]) * (1.0 + np.log(np.abs(vals[~linear]) / linthresh) / math.log(base))
    return out


def choose_scale(values):
    vals = np.asarray(values, dtype=float)
    if vals.size == 0:
        raise ValueError("values cannot be empty")
    if np.all(vals > 0) and vals.max() / vals.min() > 100:
        return "log"
    if np.any(vals < 0) and np.nanmax(np.abs(vals)) > 10:
        return "symlog"
    return "linear"
