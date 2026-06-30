import math
from math import sin

def trapezoid2(f, a, b, n):
        calcular =(0.5)*( f(a) + f(b) )
        h = (b-a)/n
        for i in range(1, n):
            calcular += f(a + i*h)
        return h*calcular


    