import numpy as np

def gauss(A, b, n):
    for row in range(0, n - 1):
        factor = np.identity(n)

        if A[row][row] == 0:
            break
        for i in range(row + 1, n):
            factor[i][row] = -1 * A[i, row] / A[row, row]
        A = np.dot(factor, A)
        b = np.dot(factor, b)
    return A, b


def back_subsitute(U, bb):
    n = U.shape[1]
    x = np.zeros(n)
    for j in range(n - 1, -1, -1):  # loop backwards over columns
        if U[j, j] == 0:
            continue
        x[j] = bb[j] / U[j, j]
        for i in range(0, j):
            bb[i] -= U[i, j] * x[j]

    return x
