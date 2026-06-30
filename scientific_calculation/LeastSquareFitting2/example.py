import scipy.linalg as linalg#3

def QR_least_square_fitter(M,b):#30
    Q, R = linalg.qr(M)#31
    b_prime = Q.T @ b#32
    m = M.shape[1]#33
    return linalg.solve(R[:m,], b_prime[:m])#34