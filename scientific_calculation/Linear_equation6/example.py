import numpy as np

def partial_pivot(a, b, n):
    for k in range(0, n - 1):
        mat = np.zeros((n, n))
        np.fill_diagonal(mat, 1)
        maximum = a[k, k]
        p = k
        for i in range(k, n):
            if a[i, k] > maximum:
                maximum = a[i, k]
                p = i
        if p != k:
            temp = np.array(a[k, :])
            temp2 = np.array(a[p, :])
            a[k] = temp2
            a[p] = temp
            tt = np.array(b[k])
            tt2 = np.array(b[p])
            b[k] = tt2
            b[p] = tt

        if a[k, k] == 0:
            raise RuntimeError("singular matrix")
        for i in range(k + 1, n):
            mat[i, k] = -1 * a[i, k] * 1.0 / a[k, k]
        a = np.dot(mat, a)
        b = np.dot(mat, b)

    return a, b


def back_subsitute(U, bb):
    n = U.shape[1]
    x = np.zeros(n)
    for j in range(n - 1, -1, -1):  # loop backwards over columns
        if U[j, j] == 0:
            raise RuntimeError("singular matrix")

        x[j] = bb[j] / U[j, j]
        for i in range(0, j):
            bb[i] -= U[i, j] * x[j]

    return x
