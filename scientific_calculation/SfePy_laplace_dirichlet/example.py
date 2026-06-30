import numpy as np


def laplace_residual_2d(u, dx=1.0, dy=1.0, source=None):
    arr = np.asarray(u, dtype=float)
    if arr.ndim != 2:
        raise ValueError("u must be a two-dimensional grid")
    if arr.shape[0] < 3 or arr.shape[1] < 3:
        raise ValueError("grid must contain at least one interior node")
    if dx <= 0 or dy <= 0:
        raise ValueError("grid spacing must be positive")
    rhs = 0.0 if source is None else np.asarray(source, dtype=float)
    interior = (
        (arr[2:, 1:-1] - 2.0 * arr[1:-1, 1:-1] + arr[:-2, 1:-1]) / dx ** 2
        + (arr[1:-1, 2:] - 2.0 * arr[1:-1, 1:-1] + arr[1:-1, :-2]) / dy ** 2
    )
    return interior - rhs


def impose_dirichlet(u, value, side):
    arr = np.array(u, dtype=float, copy=True)
    if arr.ndim != 2:
        raise ValueError("u must be two-dimensional")
    if side == "left":
        arr[:, 0] = value
    elif side == "right":
        arr[:, -1] = value
    elif side == "bottom":
        arr[0, :] = value
    elif side == "top":
        arr[-1, :] = value
    else:
        raise ValueError("unknown side")
    return arr
