import numpy as np  # 1
import random  # 2

PI = 2.*np.arcsin(1)  # 3

def trap(func, a, b, N):  # 4
    h = (b-a) / (N-1)  # 5
    S = 0.5*(func(a) + func(b))  # 6
    x = a + h  # 7
    for j in range(1,N-1):  # 8
        S = S + func(x)  # 9
        x = x + h  # 10
    S = S*h  # 11
    return S  # 12

def trap_d(x, y):  # 13
    N = len(x)  # 14
    h = (x[N-1]-x[0]) / (N-1)  # 15
    S = 0.5*(y[0] + y[N-1])  # 16
    for j in range(1,N-1):  # 17
        S = S + y[j]  # 18
    S = S*h  # 19
    return S  # 20

def lin(x):  # 21
    return x  # 22

def quad(x):  # 23
    return x*x  # 24

def cub(x):  # 25
    return x*x*x  # 26

def quar(x):  # 27
    return x*x*x*x  # 28

def inregion(x, y, z):  # 29
    return x ** 2 + y ** 2 + z ** 2 <= 1  # 30

def legendre(a, b, x, y, n):  # 31
    if n == 0:  # 32
        return np.ones(len(x))  # 33
    if n == 1:  # 34
        return x  # 35
    N = len(x)  # 36
    tmp = np.zeros(N)  # 37
    P_1 = legendre(a, b, x, y, n-1)  # 38
    P_2 = legendre(a, b, x, y, n-2)  # 39
    for i in range(N):  # 40
        tmp[i] = (2.*n-1)*x[i]*P_1[i] - (n-1)*P_2[i]  # 41
        tmp[i] = tmp[i] / n  # 42
    return tmp  # 43

def multiply(A, B):  # 44
    N = len(A)  # 45
    tmp = np.zeros(N)  # 46
    for i in range(N):  # 47
        tmp[i] = A[i]*B[i]  # 48
    return tmp  # 49

def gauss_leg(a, b, N):  # 50
    x = np.zeros(N)  # 51
    w = np.zeros(N)  # 52
    eps = 1.e-14  # 53
    m = (N+1) >> 1  # 54
    xm = 0.5*(b+a)  # 55
    xl = 0.5*(b-a)  # 56
    for i in range(m):  # 57
        z = np.cos(PI*(i+0.75)/(N+0.5))  # 58
        z1 = z + 1.  # 59
        while (abs(z-z1) > eps):  # 60
            p1 = 1.  # 61
            p2 = 0.  # 62
            for j in range(N):  # 63
                p3 = p2  # 64
                p2 = p1  # 65
                p1 = ((2.*j+1) * z * p2 - j * p3) / (j+1)  # 66
            pp = N * (z * p1 - p2) / (z * z - 1.)  # 67
            z1 = z  # 68
            z = z1 - p1 / pp  # 69
        x[i] = xm - xl*z  # 70
        x[N-1-i] = xm + xl*z  # 71
        w[i] = 2.*xl / ((1.-z*z) * pp*pp)  # 72
        w[N-1-i] = w[i]  # 73
    return [x, w]  # 74

def gauss_quad(func, x, w):  # 75
    N = len(x)  # 76
    I = 0  # 77
    for i in range(N):  # 78
        I = I + w[i]*func(x[i])  # 79
    return I  # 80

def monte_carlo_1d(func, a, b, N):  # 81
    f = 0  # 82
    f2 = 0  # 83
    L = b-a  # 84
    for i in range(N):  # 85
        x = a + random.random()*L  # 86
        f = f + func(x)  # 87
        f2 = f2 + func(x)*func(x)  # 88
    f = f / N  # 89
    f2 = f2 / N  # 90
    I = f / L  # 91
    S = np.sqrt((f2 - f*f) / N) * L  # 92
    return [I, S]  # 93

def monte_carlo_3d(func, a, b, inregion, N):  # 94
    f = 0  # 95
    f2 = 0  # 96
    Lx = b[0]-a[0]  # 97
    Ly = b[1]-a[1]  # 98
    Lz = b[2]-a[2]  # 99
    for i in range(N):  # 100
        x = a[0] + random.random()*Lx  # 101
        y = a[1] + random.random()*Ly  # 102
        z = a[2] + random.random()*Lz  # 103
        if inregion(x, y, z):  # 104
            f = f + func(x, y, z)  # 105
            f2 = f2 + func(x, y, z)*func(x, y, z)  # 106
    f = f / N  # 107
    f2 = f2 / N  # 108
    I = f * Lx*Ly*Lz  # 109
    S = np.sqrt((f2-f*f) / N) * Lx*Ly*Lz  # 110
    return [I, S]  # 111

def sphere(x, y, z):  # 112
    if x*x + y*y + z*z <= 1:  # 113
        return True  # 114
    else:  # 115
        return False  # 116

def torus(x, y, z):  # 117
    if z*z + pow((np.sqrt(x*x+y*y)-3), 2) <= 1:  # 118
        return True  # 119
    else:  # 120
        return False  # 121

def density(x, y, z):  # 122
    return 1.  # 123

def xmoment(x, y, z):  # 124
    return x  # 125

def ymoment(x, y, z):  # 126
    return y  # 127

def zmoment(x, y, z):  # 128
    return z  # 129

def exponential(beta):  # 130
    tmp = random.random()  # 131
    if tmp == 0:  # 132
        tmp = random.random()  # 133
    else:  # 134
        return -np.log(tmp)/beta  # 135