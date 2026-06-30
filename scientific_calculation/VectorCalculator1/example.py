import numpy as np  # 1

def Au(A, u):  # 23
    n = len(u)  # 24
    tmp = np.zeros(n)  # 25
    for q in range(n):  # 26
        for p in range(n):  # 27
            tmp[q] = tmp[q] + A[p, q] * u[p]  # 28
    return tmp  # 29