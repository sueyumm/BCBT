from numpy import copy, dot, zeros, eye, sqrt  # 2

def pivot_gauss(A, b):  # 7
    A, b = copy(A), copy(b)  # 8
    n = len(A)  # 9
    for i in range(0, n - 1):  # 10
        for j in range(i + 1, n):  # 11
            if A[j, i] > A[i, i]:  # 12
                A[[i, j], :] = A[[j, i], :]  # 13
                b[[i, j]] = b[[j, i]]  # 14
            if A[j, i] != 0.0:  # 15
                m = A[j, i] / A[i, i]  # 16
                A[j, i:n] = A[j, i:n] - m * A[i, i:n]  # 17
                b[j] = b[j] - m * b[i]  # 18
    for k in range(n - 1, -1, -1):  # 19
        b[k] = (b[k] - dot(A[k, (k + 1):n], b[(k + 1):n])) / A[k, k]  # 20
    x = b  # 21
    print(A)  # 22
    return x  # 23