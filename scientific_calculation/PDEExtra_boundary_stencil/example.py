import numpy as np


def apply_boundary(values, mode="dirichlet", left=0.0, right=0.0):
    arr = np.asarray(values, dtype=float).copy()
    if arr.size < 2:
        raise ValueError("need at least two nodes")
    if mode == "dirichlet":
        arr[0] = left
        arr[-1] = right
    elif mode == "neumann":
        arr[0] = arr[1] - left
        arr[-1] = arr[-2] + right
    elif mode == "periodic":
        arr[0] = arr[-2]
        arr[-1] = arr[1]
    else:
        raise ValueError("unknown boundary mode")
    return arr
