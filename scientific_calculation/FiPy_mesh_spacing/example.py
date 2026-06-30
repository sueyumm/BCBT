import numpy as np


def cell_widths(points):
    points = np.asarray(points, dtype=float)
    if points.ndim != 1:
        raise ValueError("points must be one-dimensional")
    if len(points) < 2:
        return np.array([], dtype=float)
    widths = np.diff(points)
    if np.any(widths <= 0):
        raise ValueError("points must be strictly increasing")
    return widths


def mesh_quality(points, ratio_limit=2.0):
    widths = cell_widths(points)
    if len(widths) == 0:
        return "degenerate"
    ratio = float(widths.max() / widths.min())
    if ratio <= ratio_limit:
        return "uniform"
    return "stretched"
