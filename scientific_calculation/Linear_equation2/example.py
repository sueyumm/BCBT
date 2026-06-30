from numpy import copy, dot, zeros, eye, sqrt  # 2

def lu_decomposition_doolittle(A, b):  # 24
    A, b = copy(A), copy(b)  # 25
    n = len(A)  # 26
    L = eye(n)  # 27
    U = zeros((n, n))  # 28
    for k in range(n):  # 29
        for j in range(k, n):  # 30
            s = 0  # 31
            for t in range(0, k):  # 32
                s += L[k, t] * U[t, j]  # 33
            U[k, j] = A[k, j] - s  # 34
        for i in range(k + 1, n):  # 35
            s = 0  # 36
            for t in range(0, k):  # 37
                s += L[i, t] * U[t, k]  # 38
            L[i, k] = (A[i, k] - s) / U[k, k]  # 39

    y = zeros(n)  # 40
    for i in range(n):  # 41
        s = 0  # 42
        for j in range(0, i):  # 43
            s += L[i, j] * y[j]  # 44
        y[i] = b[i] - s  # 45

    x = zeros(n)  # 46
    for i in reversed(range(n)):  # 47
        s = 0  # 48
        for j in range(i + 1, n):  # 49
            s += U[i, j] * x[j]  # 50
        x[i] = (y[i] - s) / U[i, i]  # 51

    return x  # 52