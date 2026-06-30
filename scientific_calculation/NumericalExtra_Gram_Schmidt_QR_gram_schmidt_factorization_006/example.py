# Adapted from Numerical-methods-main/Gram-Schmidt QR.py::gram_schmidt_factorization

import numpy as np

def gram_schmidt_factorization(matrix):
    matrix = np.array(matrix)
    m, n = matrix.shape
    q = np.zeros((m, n))
    r = np.zeros((n, n))
    matrix = np.transpose(matrix)
    r[0][0] = np.linalg.norm(matrix[0], 2)
    q[:, 0] = matrix[0]/r[0][0]
    for i in range(1, n):
        q[:, i] = matrix[i]
        for j in range(0, i):
            r[j][i] = np.matmul(q[:, j], q[:, i])
            q[:, i] = q[:, i] - (r[j][i] * q[:, j])
        r[i][i] = np.linalg.norm(q[:, i], 2)
        q[:, i] = q[:, i] / r[i][i]
    return q, r

def system_solver(matrix, vector):
    qr_decomposition = gram_schmidt_factorization(matrix)
    q_matrix = qr_decomposition[0]
    r_matrix = qr_decomposition[1]
    redacted_vector = np.matmul(q_matrix.transpose(), np.array(vector).transpose())
    r_matrix_inverse = np.linalg.inv(r_matrix)
    x_vector = np.matmul(r_matrix_inverse, redacted_vector)
    return x_vector
