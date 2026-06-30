import numpy as np


def heat_step(u, alpha, dt, dx, boundary="dirichlet"):
    arr = np.asarray(u, dtype=float)
    if arr.ndim != 1 or arr.size < 3:
        raise ValueError("u must be a one-dimensional grid with at least 3 nodes")
    if alpha < 0 or dt <= 0 or dx <= 0:
        raise ValueError("invalid discretisation")
    r = alpha * dt / (dx * dx)
    if r > 0.5:
        raise ValueError("unstable explicit heat step")
    out = arr.copy()
    for i in range(1, arr.size - 1):
        out[i] = arr[i] + r * (arr[i - 1] - 2.0 * arr[i] + arr[i + 1])
    if boundary == "dirichlet":
        out[0] = arr[0]
        out[-1] = arr[-1]
    elif boundary == "neumann":
        out[0] = out[1]
        out[-1] = out[-2]
    elif boundary == "periodic":
        out[0] = out[-2]
        out[-1] = out[1]
    else:
        raise ValueError("unknown boundary")
    return out
