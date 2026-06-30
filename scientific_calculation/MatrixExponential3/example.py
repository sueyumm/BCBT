import numpy        as np  #1
import numpy.linalg as la  #2

def meT(L, t, n):#22
    term_norms = []#23
    [d, d] = L.shape#24
    tLk = np.identity(d)#25
    kf = 1#26
    S = np.identity(d)#27
    for k in range(1, n):#28
        kf = k * kf#29
        tLk = t * ((tLk) @ L)#30
        S += (1 / kf) * tLk#31
        term_norms.append(la.norm((1 / kf) * tLk))#32
    return (S, max(term_norms))#33