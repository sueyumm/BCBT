import numpy as np
import copy
import scipy
import scipy.linalg as linalg
import scipy.io as input

def jakobi(A, b, numberOfIteration):
    dimension = len(A)
    x = [0] * dimension
    p = [0] * dimension
    sum = 0.0

    for i in range(numberOfIteration):
        for k in range(dimension):
            for j in range(dimension):
                if j == k or A[k, k] == 0 :
                    continue
                else:
                    sum += (A[k, j] * p[j])
            x[k] = (b[k] - sum) / A[k, k]
            sum = 0
        p = copy.copy(x)
    return p