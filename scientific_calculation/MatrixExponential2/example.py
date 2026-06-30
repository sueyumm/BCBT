import numpy        as np  #1
import numpy.linalg as la  #2

def med(L, t, k):#13
    [d, d] = L.shape#14
    n = 2 ** k#15
    dt = t / n#16
    I = np.identity(d)#17
    S = I + dt * L @ (I + (1 / 2) * dt * L @ (I + (1 / 3) * dt * L @ (I + (1 / 4) * dt * L)))#18
    for j in range(k):#19
        S = S @ S#20
    return (S)#21