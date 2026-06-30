import numpy as np
import math
from math import sin
from sympy.abc import x
import sympy

def trapezoidal_double(f, a, b, c, d, nx, ny):
    hx = (b - a)/float(nx)
    hy = (d - c)/float(ny)
    I = 0.25*(f(a, c) + f(a, d) + f(b, c) + f(b, d))
    Ix = 0
    for i in range(1, nx):
        xi = a + i*hx
        Ix += f(xi, c) + f(xi, d)
    I += 0.5*Ix
    Iy = 0
    for j in range(1, ny):
        yj = c + j*hy
        Iy += f(a, yj) + f(b, yj)
    I += 0.5*Iy
    Ixy = 0
    for i in range(1, nx):
        for j in range(1, ny):
            xi = a + i*hx
            yj = c + j*hy
            Ixy += f(xi, yj)
    I += Ixy
    I *= hx*hy
    return I