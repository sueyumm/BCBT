import numpy as np#1
import numpy.linalg as la#4

def SVD_least_square_fitter(M, b):#35
    U, sigma, VT = la.svd(M)#36
    m = M.shape[1]#37
    Sigma_pinv = np.zeros(M.shape).T#38
    Sigma_pinv[:m, :m] = np.diag(1 / sigma[:m])#39

    condNum = max(sigma)/min(sigma)#40

    return VT.T @ Sigma_pinv @ U.T @ b, condNum#41