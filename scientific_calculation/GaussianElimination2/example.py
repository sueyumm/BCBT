import numpy as np#1

def SeqGauss(A):#9
    n = A.shape[0]#10
    for i in range(n-1):#11
        for j in range(i+1,n):#12
            A[j,i:] = A[j,i:]-(A[j,i]/A[i,i])*A[i,i:]#13
    return A#14
