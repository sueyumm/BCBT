import numpy as np


def tri_indices_count(n, k=0, upper=False):
    if n < 0:
        raise ValueError("n must be non-negative")
    count = 0
    for i in range(n):
        for j in range(n):
            if upper and j - i >= k:
                count += 1
            elif not upper and i - j >= -k:
                count += 1
    return count


def diagonal_fill(shape, value=1.0, offset=0):
    if len(shape) != 2:
        raise ValueError("shape must be two-dimensional")
    rows, cols = shape
    arr = np.zeros(shape, dtype=float)
    for i in range(rows):
        j = i + offset
        if 0 <= j < cols:
            arr[i, j] = value
    return arr
