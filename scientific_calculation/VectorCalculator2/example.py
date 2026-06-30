import numpy as np  # 1

def bsc(b, c):  # 30
    n = len(b)  # 31
    sub = np.zeros(n)  # 32
    for p in range(n):  # 33
        sub[p] = b[p] - c[p]  # 34
    return sub  # 35