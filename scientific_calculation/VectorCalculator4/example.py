import numpy as np  # 1

def legendre(a,b,x,y,n):  # 29
    if n == 0:  # 30
        return np.ones(len(x))  # 31
    if n == 1:  # 32
        return x  # 33
    N = len(x)  # 34
    tmp = np.zeros(N)  # 35
    P_1 = legendre(a,b,x,y,n-1)  # 36
    P_2 = legendre(a,b,x,y,n-2)  # 37
    for i in range(N):  # 38
        tmp[i] = (2.*n-1)*x[i]*P_1[i] - (n-1)*P_2[i]  # 39
        tmp[i] = tmp[i] / n  # 40
    return tmp  # 41
