import numpy as np
import scipy
import scipy.io as input
import scipy.linalg as linalg

def LUFactorization(B):
    dimension = len(B)  # my matrix dimension is 3x3
    U = B.copy()
    L = np.identity(dimension)

    for k in range(dimension - 1):
        for i in range(k + 1, dimension):
            ratio = U[i, k] / U[k, k]
            for j in range(dimension):
                U[i, j] = U[i, j] - ratio*U[k, j]
            L[i, k] = ratio
    return L, U

def ULFactorization(A):
    P = np.eye(len(A))
    P = np.flipud(P) #in order to get permutation matrice
    B = np.matmul(np.matmul(P, A),P)  #B = PAP^T
    bL, bU = LUFactorization(B)
    U = np.matmul(np.matmul(P, bL), np.transpose(P)) #myU = PLP^T
    L = np.matmul(np.matmul(P, bU), np.transpose(P)) #myL = PUP^T
    return P, U, L

def forward_sub(U, b):
    dimension = len(b)
    y = np.zeros_like(b).reshape(dimension, 1)
    for i in reversed(range(len(b))):
        s = np.matmul(U[i], y[:dimension])
        y[i] = b[i] - s[0]
    return y

def backward_sub(L, y):
    dimension = len(y)
    x = np.zeros_like(y)
    for i in range(len(y)):
        s = np.matmul(L[i], x[:dimension])
        x[i] = (y[i] - s[0]) / L[i, i]
    return x.flatten()  # just for make x array to one dimesional