# Adapted from Numerical-methods-main/householder qr decomposition.py::householder_qr_decomposition

import numpy as np

def householder_qr_decomposition(matrix):
    matrix = np.array(matrix)
    m, n = matrix.shape
    matrix_copy = matrix.copy()
    q = np.identity(m)

    def householder_transformation(column_vector):
        vector = column_vector / (column_vector[0] + np.copysign(np.linalg.norm(column_vector), column_vector[0]))
        vector[0] = 1
        tau_value = 2 / np.matmul(np.transpose(vector), vector)
        return vector, tau_value

    for j in range(n):
        v, tau = householder_transformation(matrix_copy[j:, j, np.newaxis])
        householder = np.identity(m)
        householder[j:, j:] -= tau * (np.matmul(v, np.transpose(v)))
        matrix_copy = np.matmul(householder, matrix_copy)
        q = np.matmul(householder, q)
    q = np.transpose(q)
    r = np.triu(matrix_copy[:n])
    return q, r

def system_solver(matrix, vector):
    qr_decomposition = householder_qr_decomposition(matrix)  # decomposing matrix to Q and R
    q_matrix = qr_decomposition[0]
    r_matrix = qr_decomposition[1]
    redacted_vector = np.matmul(q_matrix.transpose(), np.array(vector).transpose())  # fourth step
    r_matrix_inverse = np.linalg.inv(r_matrix)
    x_vector = np.matmul(r_matrix_inverse, redacted_vector)  # fifth step
    return x_vector
