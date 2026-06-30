# Adapted from TheAlgorithms/Python matrix utilities.


def matrix_bandwidth(nonzero_positions, size):
    if size <= 0:
        raise ValueError("invalid size")
    lower = 0
    upper = 0
    for row, col in nonzero_positions:
        if row < 0 or col < 0 or row >= size or col >= size:
            raise ValueError("position outside matrix")
        if row >= col:
            lower = max(lower, row - col)
        else:
            upper = max(upper, col - row)
    if lower == 0 and upper == 0:
        return "diagonal"
    if lower <= 1 and upper <= 1:
        return "tridiagonal"
    if max(lower, upper) <= size // 2:
        return "banded"
    return "wide"
