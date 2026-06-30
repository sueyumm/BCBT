import numpy        as np  #1
import numpy.linalg as la  #2

def conditionNumber(M):#3
    return la.norm(M)*la.norm(la.inv(M))#4

def mee(L, t):#5
    [d, d] = L.shape#6
    lam, R = la.eig(L)#7
    d_elamt = np.zeros([d, d])#8
    for j in range(d):#9
        d_elamt[j, j] = np.exp(lam[j] * t)#10
    conN = conditionNumber(R)#11
    return (R @ d_elamt @ la.inv(R), conN)#12