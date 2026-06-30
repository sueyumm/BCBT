from numpy import copy, dot, zeros, eye, sqrt  # 2
from numpy import tril, triu, linalg  # 3
from numpy import array, random, inf, nan  # 4

def check_symmetric_and_positive_definite_matrix(A):  # 1
    if not (A.T == A).all():  # 2
        print('A must be symmetric and positive definite matrix')  # 3
        return False  # 4

    values = linalg.eigvals(A)  # 5
    if any(values < 0):  # 6
        print('A must be symmetric and positive definite matrix')  # 7
        return False # 8

    return True # 9


def lu_decomposition_cholesky(A, b):  # 10
    A, b = copy(A), copy(b)  # 11

    if not check_symmetric_and_positive_definite_matrix(A):  # 12
        return nan  # 13

    n = len(A)  # 14
    L = eye(n)  # 15

    for j in range(n):  # 16
        s = 0  # 17
        for k in range(j):  # 18
            s += L[j, k] ** 2  # 19
        L[j, j] = sqrt(A[j, j] - s)  # 20

        for i in range(j + 1, n):  # 21
            s = 0  # 22
            for k in range(j):  # 23
                s += L[i, k] * L[j, k]  # 24
            L[i, j] = (A[i, j] - s) / L[j, j]  # 25

    y = zeros(n)  # 26

    for i in range(n):  # 27
        s = 0  # 28
        for j in range(0, i):  # 29
            s += L[i, j] * y[j]  # 30
        y[i] = (b[i] - s) / L[i, i]  # 31

    x = zeros(n)  # 32
    for i in reversed(range(n)):  # 33
        s = 0  # 34
        for j in range(i + 1, n):  # 35
            s += L[j, i] * x[j]  # 36
        x[i] = (y[i] - s) / L[i, i]  # 37

    return x  # 38
