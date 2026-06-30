import numpy as np  # 1

def inverse_power_method(A, tolerance=1e-10, max_iterations=10000):  # 2
    n = A.shape[0]  # 3
    x = np.ones(n)  # 4
    I = np.eye(n)  # 5
    q = np.dot(x, np.dot(A, x)) / np.dot(x, x)  # 6
    p = __find_p(x)  # 7
    error = 1  # 8
    x = x / x[p]  # 9
    for _ in range(max_iterations):  # 10
        if error < tolerance:  # 11
            break  # 12
        y = np.linalg.solve(A - q * I, x)  # 13
        μ = y[p]  # 14
        p = __find_p(y)  # 15
        error = np.linalg.norm(x - y / y[p], np.inf)  # 16
        x = y / y[p]  # 17
        μ = 1. / μ + q  # 18
    return (μ, x)  # 19

def __find_p(x):  # 20
    return np.argwhere(np.isclose(np.abs(x), np.linalg.norm(x, np.inf))).min()  # 21

def __iterate(A, x, p):  # 22
    y = np.dot(A, x)  # 22
    μ = y[p]  # 23
    p = __find_p(y)  # 24
    error = np.linalg.norm(x - y / y[p], np.inf)  # 25
    x = y / y[p]  # 26
    return (error, p, μ, x)  # 27

def power_method(A, tolerance=1e-10, max_iterations=10000):  # 28

    n = A.shape[0]  # 29
    x = np.ones(n)  # 30
    p = __find_p(x)  # 31

    error = 1  # 32

    x = x / x[p]  #33

    for _ in range(max_iterations):  # 34
        if error < tolerance:  # 35
            break  # 36
        error, p, μ, x = __iterate(A, x, p)  # 37

    return (μ, x)  # 38
