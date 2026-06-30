import numpy as np


def select_box_bounds(nx, ny, x_bound=None, y_bound=None):
    if nx <= 0 or ny <= 0:
        raise ValueError("grid dimensions must be positive")
    x0, x1 = 0, nx
    y0, y1 = 0, ny
    if x_bound is not None:
        if x_bound < 0:
            raise ValueError("x_bound must be non-negative")
        x1 = min(nx, x_bound)
    if y_bound is not None:
        if y_bound < 0:
            raise ValueError("y_bound must be non-negative")
        y1 = min(ny, y_bound)
    mask = np.zeros((nx, ny), dtype=bool)
    mask[x0:x1, y0:y1] = True
    return mask


def count_boundary_cells(mask):
    if mask.ndim != 2:
        raise ValueError("mask must be two-dimensional")
    if mask.size == 0:
        return 0
    boundary = np.zeros_like(mask, dtype=bool)
    boundary[0, :] = mask[0, :]
    boundary[-1, :] = mask[-1, :]
    boundary[:, 0] |= mask[:, 0]
    boundary[:, -1] |= mask[:, -1]
    return int(boundary.sum())
