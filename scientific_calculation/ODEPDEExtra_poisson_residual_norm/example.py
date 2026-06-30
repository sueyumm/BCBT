import numpy as np


def poisson_residual(u, rhs, h, norm="l2"):
    grid = np.asarray(u, dtype=float)
    force = np.asarray(rhs, dtype=float)
    if grid.shape != force.shape or grid.ndim != 2:
        raise ValueError("u and rhs must be two-dimensional arrays with equal shape")
    if min(grid.shape) < 3 or h <= 0:
        raise ValueError("invalid grid")
    residuals = []
    for i in range(1, grid.shape[0] - 1):
        for j in range(1, grid.shape[1] - 1):
            lap = (grid[i - 1, j] + grid[i + 1, j] + grid[i, j - 1] + grid[i, j + 1] - 4 * grid[i, j]) / (h * h)
            residuals.append(lap - force[i, j])
    r = np.asarray(residuals)
    if norm == "linf":
        return float(np.max(np.abs(r)))
    if norm == "l1":
        return float(np.sum(np.abs(r)))
    if norm == "l2":
        return float(np.sqrt(np.sum(r * r)))
    raise ValueError("unknown norm")
