import numpy as np#1

def Solve(U,b):#2
    n = len(b)#3
    x = np.zeros((n,1))#4
    x[-1] = b[-1]/U[-1,-1]#5
    for i in range(n-2,-1,-1):#6
        x[i] = (b[i]-np.dot(U[i,i+1:],x[i+1:]))/U[i,i]#7
    return x#8