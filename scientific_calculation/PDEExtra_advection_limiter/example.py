import numpy as np


def flux_limiter(r, kind="minmod"):
    if kind == "minmod":
        return max(0.0, min(1.0, r))
    if kind == "superbee":
        return max(0.0, min(2.0 * r, 1.0), min(r, 2.0))
    if kind == "vanleer":
        return (r + abs(r)) / (1.0 + abs(r))
    raise ValueError("unknown limiter")


def limited_advection_step(u, cfl, kind="minmod"):
    arr = np.asarray(u, dtype=float)
    if arr.ndim != 1 or arr.size < 3:
        raise ValueError("u must be one-dimensional with at least 3 cells")
    if cfl < 0 or cfl > 1:
        raise ValueError("cfl must be in [0, 1]")
    out = arr.copy()
    for i in range(1, arr.size - 1):
        denom = arr[i + 1] - arr[i]
        r = 0.0 if abs(denom) < 1e-12 else (arr[i] - arr[i - 1]) / denom
        phi = flux_limiter(r, kind)
        slope = phi * (arr[i + 1] - arr[i])
        out[i] = arr[i] - cfl * (arr[i] - arr[i - 1]) - 0.5 * cfl * (1 - cfl) * slope
    return out
