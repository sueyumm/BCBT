import numpy as np


def quadratic_bezier(points, t):
    pts = np.asarray(points, dtype=float)
    if pts.shape != (3, 2):
        raise ValueError("quadratic bezier requires three 2D control points")
    if np.any((np.asarray(t) < 0) | (np.asarray(t) > 1)):
        raise ValueError("parameter t must be in [0, 1]")
    t = np.asarray(t, dtype=float)[..., None]
    return (1 - t) ** 2 * pts[0] + 2 * (1 - t) * t * pts[1] + t ** 2 * pts[2]


def curve_flatness(points):
    pts = np.asarray(points, dtype=float)
    if pts.shape != (3, 2):
        raise ValueError("quadratic bezier requires three 2D control points")
    chord = pts[2] - pts[0]
    if np.allclose(chord, 0.0):
        return float(np.linalg.norm(pts[1] - pts[0]))
    area2 = abs(np.cross(chord, pts[1] - pts[0]))
    return float(area2 / np.linalg.norm(chord))
