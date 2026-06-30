import numpy as np


def chemotaxis_flux(cells, chemoattractant, sensitivity, dx):
    cells = np.asarray(cells, dtype=float)
    chemoattractant = np.asarray(chemoattractant, dtype=float)
    if cells.shape != chemoattractant.shape:
        raise ValueError("cells and chemoattractant must have the same shape")
    if sensitivity < 0 or dx <= 0:
        raise ValueError("invalid sensitivity or dx")
    if len(cells) < 2:
        return np.zeros_like(cells)
    grad_c = np.gradient(chemoattractant, dx)
    return -sensitivity * cells * grad_c


def update_cell_density(cells, flux, dx, dt):
    cells = np.asarray(cells, dtype=float)
    flux = np.asarray(flux, dtype=float)
    if cells.shape != flux.shape:
        raise ValueError("cells and flux must have the same shape")
    if dx <= 0 or dt < 0:
        raise ValueError("invalid dx or dt")
    divergence = np.gradient(flux, dx)
    updated = cells - dt * divergence
    return np.maximum(updated, 0.0)
