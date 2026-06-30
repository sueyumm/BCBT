import numpy as np


def normalize_coefficient(coeff, cells):
    arr = np.asarray(coeff, dtype=float)
    if arr.ndim == 0:
        return np.full(cells, float(arr))
    if arr.shape == (cells,):
        return arr.copy()
    if arr.shape == (1, cells):
        return arr.reshape(cells)
    if arr.size == 0:
        raise ValueError("empty coefficient")
    raise ValueError("coefficient shape mismatch")
