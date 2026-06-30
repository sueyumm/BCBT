import numpy as np#1

def PivotGauss(A):#15
    n = A.shape[0]#16
    for i in range(n-1):#17
        k = [j for j in range(i,n) if A[j,i]==np.max(A[i:,i])][0]#18
        A[[i,k],:]=A[[k,i],:]#19
        for j in range(i+1,n):#20
            A[j,i:] = A[j,i:]-(A[j,i]/A[i,i])*A[i,i:]#21
    return A#22
