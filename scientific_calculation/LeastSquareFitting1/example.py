from scipy.linalg import cho_factor, cho_solve#2

def cholesky_least_square_fitter(M, b):#27
    c, low = cho_factor(M.T @ M)#28
    return cho_solve((c, low), M.T @ b)#29