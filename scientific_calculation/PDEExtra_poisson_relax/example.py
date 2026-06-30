import numpy as np


def jacobi_relax_step(u, rhs, omega=1.0):
    grid = np.asarray(u, dtype=float)
    force = np.asarray(rhs, dtype=float)
    if grid.shape != force.shape or grid.ndim != 2:
        raise ValueError("u and rhs must be 2D arrays with same shape")
    if not (0 < omega <= 1.5):
        raise ValueError("omega out of range")
    out = grid.copy()
    for i in range(1, grid.shape[0] - 1):
        for j in range(1, grid.shape[1] - 1):
            candidate = 0.25 * (grid[i - 1, j] + grid[i + 1, j] + grid[i, j - 1] + grid[i, j + 1] - force[i, j])
            out[i, j] = (1 - omega) * grid[i, j] + omega * candidate
    return out
