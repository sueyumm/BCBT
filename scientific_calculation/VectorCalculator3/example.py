import numpy as np  # 1

def norm2(u):  # 36
    n = len(u)  # 37
    norm = 0  # 38
    for p in range(n):  # 39
        norm = norm + u[p] * u[p]  # 40
    return np.sqrt(norm)  # 41