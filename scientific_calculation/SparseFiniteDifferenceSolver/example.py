import numpy as np  # 1
import math as math  # 2
from scipy.linalg import lu_factor, lu_solve  # 3
from scipy import sparse  # 4
from scipy.sparse import identity  # 5
from scipy.sparse import csr_matrix  # 6
from scipy.sparse import linalg as sla  # 7
from scipy.linalg import norm  # 8


def fill(h):  # 9
    n = int(1. / h)  # 10
    A = csr_matrix((n - 1, n - 1)).toarray()  # 11
    A[0, 0] = 2  # 12
    A[0, 1] = -1  # 13
    A[n - 2, n - 2] = 2  # 14
    A[n - 2, n - 3] = -1  # 15
    for i in range(1, n - 2):  # 16
        A[i, i - 1] = -1.  # 17
        A[i, i] = 2.  # 18
        A[i, i + 1] = -1.  # 19
    return sparse.csr_matrix(A * (1 / (h ** 2)))  # 20
def fillin2Dk(h):  # 21
    n = int(1. / h)  # 22
    return sparse.kron(identity(n - 1), fill(h)) + sparse.kron(fill(h), identity(n - 1))  # 23


def fillin3Dk(h):  # 24
    n = int(1. / h)  # 25
    return sparse.kron(fill(h), sparse.kron(identity(n - 1), identity(n - 1))) + sparse.kron(identity(n - 1), sparse.kron(fill(h), identity(n - 1))) + sparse.kron(identity(n - 1), sparse.kron(identity((n - 1)), fill(h)))  # 26
def use(h):  # 27
    n = int(1. / h)  # 28
    A = csr_matrix(((n + 1) * (n + 1), (n + 1) * (n + 1)))  # 29
    for i in range(n + 1):  # 30
        A[i, i] = 1  # 31
    for i in range((n + 1) * (n + 1) - n - 1, (n + 1) * (n + 1)):  # 32
        A[i, i] = 1  # 33
    for i in range(1, n):  # 34
        A[i * (n + 1), i * (n + 1)] = 1  # 35
        A[i * (n + 1) + n, i * (n + 1) + n] = 1  # 36
    B = fillin2Dk(h)  # 37
    for y in range(1, n):  # 38
        for x in range(1, n):  # 39
            A[y * (n + 1) + x, y * (n + 1) + x] = B.tocsr()[0, 0]  # 40
            A[y * (n + 1) + x, y * (n + 1) + x + 1] = B.tocsr()[0, 0] / -4.  # 41
            A[y * (n + 1) + x, y * (n + 1) + x - 1] = B.tocsr()[0, 0] / -4.  # 42
            A[y * (n + 1) + x, y * (n + 1) + x + n + 1] = B.tocsr()[0, 0] / -4.  # 43
            A[y * (n + 1) + x, y * (n + 1) + x - n - 1] = B.tocsr()[0, 0] / -4.  # 44
    return A  # 45

t = use(1 / (2 ** 4)).toarray()  # 46
print(t)  # 47


def use2(h):  # 48
    n = int(1. / h)  # 49
    A = csr_matrix(((n + 1) * (n + 1) * (n + 1), (n + 1) * (n + 1) * (n + 1)))  # 50
    for i in range((n + 1) * (n + 1)):  # 51
        A[i, i] = 1  # 52
    for i in range((n + 1) * (n + 1) * (n + 1) - (n + 1) * (n + 1), (n + 1) * (n + 1) * (n + 1)):  # 53
        A[i, i] = 1  # 54
    for i in range(1, n):  # 55
        for x in range(n + 1):  # 56
            A[i * ((n + 1) * (n + 1)) + x, i * ((n + 1) * (n + 1)) + x] = 1  # 57
            A[i * ((n + 1) * (n + 1)) + (n + 1) * (n + 1) - (n + 1) + x, i * ((n + 1) * (n + 1)) + (n + 1) * (n + 1) - (n + 1) + x] = 1  # 58
    for i in range(1, n):  # 59
        for t in range(1, n):  # 60
            A[i * (n + 1) * (n + 1) + t * (n + 1), i * (n + 1) * (n + 1) + t * (n + 1)] = 1  # 61
            A[i * (n + 1) * (n + 1) + t * (n + 1) + n, i * (n + 1) * (n + 1) + t * (n + 1) + n] = 1  # 62
    B = fillin3Dk(h)  # 63
    for z in range(1, n):  # 64
        for y in range(1, n):  # 65
            for x in range(1, n):  # 66
                A[z * (n + 1) ** 2 + y * (n + 1) + x, z * (n + 1) ** 2 + y * (n + 1) + x] = B.tocsr()[0, 0]  # 67
                A[z * (n + 1) ** 2 + y * (n + 1) + x, z * (n + 1) ** 2 + y * (n + 1) + x - 1] = B.tocsr()[0, 0] / -6.  # 68
                A[z * (n + 1) ** 2 + y * (n + 1) + x, z * (n + 1) ** 2 + y * (n + 1) + x + 1] = B.tocsr()[0, 0] / -6.  # 69
                A[z * (n + 1) ** 2 + y * (n + 1) + x, z * (n + 1) ** 2 + y * (n + 1) + x - n - 1] = B.tocsr()[0, 0] / -6.  # 70
                A[z * (n + 1) ** 2 + y * (n + 1) + x, z * (n + 1) ** 2 + y * (n + 1) + x + n + 1] = B.tocsr()[0, 0] / -6.  # 71
                A[z * (n + 1) ** 2 + y * (n + 1) + x, z * (n + 1) ** 2 + y * (n + 1) + x - 1] = B.tocsr()[0, 0] / -6.  # 72
                A[z * (n + 1) ** 2 + y * (n + 1) + x, z * (n + 1) ** 2 + y * (n + 1) + x + (n + 1) ** 2] = B.tocsr()[0, 0] / -6.  # 73
                A[z * (n + 1) ** 2 + y * (n + 1) + x, z * (n + 1) ** 2 + y * (n + 1) + x - (n + 1) ** 2] = B.tocsr()[0, 0] / -6.  # 74
    return A  # 75

def rightside2(h):#76
    n = int(1. / h)#77
    A = csr_matrix(((n + 1) * (n + 1), 1))#78
    for i in range(n + 1):#79
        A[i, 0] = 0#80
    for i in range((n + 1) * (n + 1) - n - 1, (n + 1) * (n + 1)):#81
        A[i, 0] = math.sin((i - (n + 1) * (n + 1) + n + 1) * h)#82
    for i in range(1, n):#83
        A[i * (n + 1), 0] = 0#84
        A[i * (n + 1) + n, 0] = math.sin(i * h)#85
    for y in range(1, n):#86
        for x in range(1, n):#87
            A[y * (n + 1) + x, 0] = ((x * h) ** 2 + (y * h) ** 2) * math.sin(x * h * y * h)#88
    return A#89


g = rightside2(1 / 4.).toarray()#90


def rightside3(h):#91
    n = int(1. / h)#92
    A = csr_matrix(((n + 1) * (n + 1) * (n + 1), 1))#93
    for i in range((n + 1) ** 2):#94
        A[i, 0] = 0#95
    for z in range(1, n):#96
        for i in range(1, n):#97
            A[z * (n + 1) ** 2 + (n + 1) * i, 0] = 0#98
            A[z * (n + 1) ** 2 + (n + 1) * i + n, 0] = math.sin(z * h * i * h)#99
    for z in range(1, n):#100
        for i in range(n):#101
            A[z * (n + 1) ** 2 + i, 0] = 0#102
            A[z * (n + 1) ** 2 + i + n * (n + 1), 0] = math.sin(i * h + z * h)#103
    d = (n + 1) ** 3 - (n + 1) ** 2#104
    for y in range(n + 1):#105
        for x in range(n + 1):#106
            A[d, 0] = math.sin(x * h * y * h)#107
            d = d + 1#108
    for z in range(1, n):#109
        for y in range(1, n):#110
            for x in range(1, n):#111
                A[z * (n + 1) ** 2 + (n + 1) * y + x, 0] = math.sin(x * h * y * h * z * h) * ((x * h) ** 2 + (y * h) ** 2 + (z * h) ** 2)#112
    return A#113


s = rightside3(1 / 8.).toarray()#114


def Question2A():#115
    for p in range(2, 11):#116
        h = 1. / (2 ** p)#117
        lu = sla.splu(use(h))#118
        b = rightside2(h)#119
        x = lu.solve(b.toarray())#120
        print(norm(x - exact2(h), np.inf))#121


def Question3A():#122
    for p in range(2, 9):#123
        h = 1. / (2 ** p)#124
        lu = sla.splu(use2(h))#125
        b = rightside3(h)#126
        x = lu.solve(b.toarray())#127
        print(norm(x - exact3(h), np.inf))#128


def exact2(h):#129
    n = int(1. / h)#130
    ex = np.zeros(((n + 1) * (n + 1), 1))#131
    d = 0#132
    for y in range(n + 1):#133
        for x in range(n + 1):#134
            ex[d, 0] = math.sin(x * h * y * h)#135
            d = d + 1#136
    return ex#137


def exact3(h):#138
    n = int(1. / h)#139
    ex = np.zeros(((n + 1) * (n + 1) * (n + 1), 1))#140
    d = 0#141
    for z in range(n + 1):#142
        for y in range(n + 1):#143
            for x in range(n + 1):#144
                ex[d, 0] = math.sin(x * h * y * h * z * h)#145
                d = d + 1#146
    return ex#147













