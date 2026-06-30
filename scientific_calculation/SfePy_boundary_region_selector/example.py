import numpy as np


def select_boundary_nodes(points, axis, value, tolerance=1e-12):
    pts = np.asarray(points, dtype=float)
    if pts.ndim != 2:
        raise ValueError("points must be a two-dimensional coordinate array")
    if axis < 0 or axis >= pts.shape[1]:
        raise ValueError("axis is outside point dimension")
    if tolerance < 0:
        raise ValueError("tolerance must be non-negative")
    return np.abs(pts[:, axis] - value) <= tolerance


def classify_boundary(point, xlim, ylim, tolerance=1e-12):
    x, y = np.asarray(point, dtype=float)
    if abs(x - xlim[0]) <= tolerance:
        return "left"
    if abs(x - xlim[1]) <= tolerance:
        return "right"
    if abs(y - ylim[0]) <= tolerance:
        return "bottom"
    if abs(y - ylim[1]) <= tolerance:
        return "top"
    return "interior"
