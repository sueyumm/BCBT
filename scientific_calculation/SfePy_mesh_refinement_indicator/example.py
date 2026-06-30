import numpy as np


def element_error_indicator(cell_values, neighbor_values, volume, threshold):
    cell = np.asarray(cell_values, dtype=float)
    neigh = np.asarray(neighbor_values, dtype=float)
    vol = np.asarray(volume, dtype=float)
    if cell.shape != neigh.shape or cell.shape != vol.shape:
        raise ValueError("all arrays must have identical shape")
    if np.any(vol <= 0):
        raise ValueError("cell volumes must be positive")
    if threshold < 0:
        raise ValueError("threshold must be non-negative")
    error = np.abs(cell - neigh) * np.sqrt(vol)
    return error, error > threshold


def refinement_action(error, refine_tol, coarsen_tol):
    if coarsen_tol > refine_tol:
        raise ValueError("coarsen tolerance cannot exceed refine tolerance")
    if error > refine_tol:
        return "refine"
    if error < coarsen_tol:
        return "coarsen"
    return "keep"
