import numpy as np


def triangle_area(vertices):
    pts = np.asarray(vertices, dtype=float)
    if pts.shape != (3, 2):
        raise ValueError("triangle requires three 2D vertices")
    area = 0.5 * np.cross(pts[1] - pts[0], pts[2] - pts[0])
    return float(abs(area))


def triangle_quality(vertices):
    pts = np.asarray(vertices, dtype=float)
    if pts.shape != (3, 2):
        raise ValueError("triangle requires three 2D vertices")
    edges = np.array([
        np.linalg.norm(pts[1] - pts[0]),
        np.linalg.norm(pts[2] - pts[1]),
        np.linalg.norm(pts[0] - pts[2]),
    ])
    if np.any(edges == 0):
        return "degenerate"
    area = triangle_area(pts)
    quality = 4.0 * np.sqrt(3.0) * area / np.sum(edges ** 2)
    if quality > 0.75:
        return "good"
    if quality > 0.25:
        return "usable"
    return "poor"
