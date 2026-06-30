import numpy as np


def pivot_strategy(matrix, column, tol=1e-12):
    a = np.asarray(matrix, dtype=float)
    if column < 0 or column >= a.shape[1]:
        raise ValueError("bad column")
    candidates = np.abs(a[column:, column])
    if candidates.size == 0:
        return "empty"
    row = int(np.argmax(candidates)) + column
    if abs(a[row, column]) <= tol:
        return "singular"
    if row == column:
        return "no-swap"
    return "swap"
