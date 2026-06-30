import numpy as np  # 1
import sympy as sp  # 2

np.set_printoptions(precision=3, suppress=True)  # 3


def PhiValue(f, args, x, s, alpha):  # 4
    n = x.shape[0]  # 5
    subs_list = [(args[i], x[i, 0] + alpha * s[i, 0]) for i in range(n)]  # 6
    phi = np.array(f.subs(subs_list), dtype=float)[0, 0]  # 7
    return phi  # 8


def GoldenSection(f, args, x, s, R):  # 9
    b = R  # 10
    a = 0  # 11
    tau = (5 ** 0.5 - 1) / 2  # 12
    alpha1 = a + (1 - tau) * (b - a)  # 13
    phi1 = PhiValue(f, args, x, s, alpha1)  # 14
    alpha2 = a + tau * (b - a)  # 15
    phi2 = PhiValue(f, args, x, s, alpha2)  # 16
    while (b - a) > 1e-7:  # 17
        if phi1 > phi2:  # 18
            a = alpha1  # 19
            alpha1 = alpha2  # 20
            phi1 = phi2  # 21
            alpha2 = a + tau * (b - a)  # 22
            phi2 = PhiValue(f, args, x, s, alpha2)  # 23
        else:  # 24
            b = alpha2  # 25
            alpha2 = alpha1  # 26
            phi2 = phi1  # 27
            alpha1 = a + (1 - tau) * (b - a)  # 28
            phi1 = PhiValue(f, args, x, s, alpha1)  # 29
    return (a + b) / 2  # 30


def CGLineSearch(f, args, x0):  # 31
    df = sp.Matrix([f.diff(t) for t in args])  # f的梯度#32
    n = x0.shape[0]  # 33
    x = x0  # 34
    subs_list = [(args[i], x0[i, 0]) for i in range(n)]  # 35
    g = np.array(df.subs(subs_list), dtype=float)  # 梯度在x0处的值#36
    s = -g  # 初始方向为负梯度方向#37
    gk = np.sum(g * g)  # 38
    alpha = 1  # 39
    k = 0  # 40
    print('k = 0: ')  # 41
    print('x =\n', x0)  # 42
    print('gradient f = ', df)  # 43
    print('g =\n', g)  # 44
    print('s =\n', s)  # 45
    while gk > 1e-7 and k < 1000:  # 46
        alpha = GoldenSection(f, args, x, s, 2 * alpha)  # 黄金分割法求一维极小化问题，求出步长#47
        x = x + alpha * s  # 更新x#48
        subs_list = [(args[i], x[i, 0]) for i in range(n)]  # 49
        g = np.array(df.subs(subs_list), dtype=float)  # 更新梯度g#50
        gk1 = np.sum(g * g)  # 51
        beta = gk1 / gk  # 52
        gk = gk1  # 53
        s = -g + beta * s  # 更新方向s#54
        k = k + 1  # 55
        print('\nk = ', k)  # 56
        print('x =\n', x)  # 57
        print('alpha = %.3f' % alpha)  # 58
        print('g =\n', g)  # 59
        print('beta = %.3f' % beta)  # 60
        print('s = \n', s)  # 61
    return x, k  # 62
