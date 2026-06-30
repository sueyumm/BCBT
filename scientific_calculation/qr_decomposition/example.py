import numpy as np  # 6

def qr(A):  # 7
    m, n = A.shape  # 8
    Q = np.eye(m)  # 9
    for i in range(n - (m == n)):  # 10
        H = np.eye(m)  # 11
        H[i:, i:] = make_householder(A[i:, i])  # 12
        Q = np.dot(Q, H)  # 13
        A = np.dot(H, A)  # 14
    return Q, A  # 15


def make_householder(a):  # 16
    v = a / (a[0] + np.copysign(np.linalg.norm(a), a[0]))  # 17
    v[0] = 1  # 18
    H = np.eye(a.shape[0])  # 19
    H -= (2 / np.dot(v, v)) * np.dot(v[:, None], v[None, :])  # 20
    return H  # 21


# task 1: show qr decomp of wp example
a = np.array(((  # 22
    (12, -51, 4),  # 23
    (6, 167, -68),  # 24
    (-4, 24, -41),  # 25
)))  # 26

q, r = qr(a)  # 27
print('q:\n', q.round(6))  # 28
print('r:\n', r.round(6))  # 29


# task 2: use qr decomp for polynomial regression example
def polyfit(x, y, n):  # 30
    return lsqr(x[:, None] ** np.arange(n + 1), y.T)  # 31


def lsqr(a, b):  # 32
    q, r = qr(a)  # 33
    _, n = r.shape  # 34
    return np.linalg.solve(r[:n, :], np.dot(q.T, b)[:n])  # 35


x = np.array((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10))  # 36
y = np.array((1, 6, 17, 34, 57, 86, 121, 162, 209, 262, 321))  # 37

print('\npolyfit:\n', polyfit(x, y, 2))  # 38
