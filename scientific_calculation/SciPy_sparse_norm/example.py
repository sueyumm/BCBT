import numpy as np


def sparse_vector_norm(data, ord=2):
    values = np.asarray(data, dtype=float)
    if values.size == 0:
        return 0.0
    if ord == 1:
        return float(np.abs(values).sum())
    if ord == 2:
        return float(np.sqrt((values ** 2).sum()))
    if ord == np.inf:
        return float(np.abs(values).max())
    if ord <= 0:
        raise ValueError("ord must be positive")
    return float((np.abs(values) ** ord).sum() ** (1.0 / ord))


def matrix_norm_kind(ord):
    if ord in (None, "fro"):
        return "frobenius"
    if ord in (1, -1):
        return "column"
    if ord in (np.inf, -np.inf):
        return "row"
    raise ValueError("unsupported matrix norm")
