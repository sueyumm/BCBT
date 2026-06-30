# Adapted from Numerical-methods-main/bisection.py::bisection

from sympy import *

def bisection(interval, function_expression, precision=0.01):
    variable = var("x")
    function = sympify(function_expression)
    if function.subs(variable, interval[0]) * function.subs(variable, interval[1]) >= 0:
        return "this function has no roots in the given interval."
    initiation_point = interval[0]
    while interval[1] - interval[0] >= precision:
        initiation_point = (interval[0] + interval[1]) / 2
        if function.subs(variable, initiation_point) == 0.0:
            break
        if function.subs(variable, initiation_point) * function.subs(variable, interval[0]) < 0:
            interval[1] = initiation_point
        else:
            interval[0] = initiation_point
    return "The value of the root is : {}".format(initiation_point)
