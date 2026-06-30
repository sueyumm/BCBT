import numpy as np


def piecewise_coefficient(points, center, inner_value, outer_value, radius):
    pts = np.asarray(points, dtype=float)
    c = np.asarray(center, dtype=float)
    if pts.ndim != 2 or c.ndim != 1 or pts.shape[1] != c.size:
        raise ValueError("points and center dimensions do not match")
    if radius < 0:
        raise ValueError("radius must be non-negative")
    dist = np.linalg.norm(pts - c, axis=1)
    coeff = np.full(pts.shape[0], outer_value, dtype=float)
    coeff[dist <= radius] = inner_value
    return coeff


def harmonic_average(left, right):
    left = np.asarray(left, dtype=float)
    right = np.asarray(right, dtype=float)
    if np.any(left <= 0) or np.any(right <= 0):
        raise ValueError("coefficients must be positive")
    if left.shape != right.shape:
        raise ValueError("coefficient arrays must have equal shape")
    return 2.0 * left * right / (left + right)
