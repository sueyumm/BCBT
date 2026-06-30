# Adapted from Numerical-methods-main/4th order runge-kutta.py::runge_method

from sympy import *

def runge_method(function_expression, x_0, y_0, x, h):
    first_variable = var("x")
    second_variable = var("y")
    function = sympify(function_expression)
    iteration_count = int((x - x_0) / h)
    y = y_0
    for i in range(1, iteration_count + 1):
        k1 = h * function.subs([(first_variable, x_0), (second_variable, y)])
        k2 = h * function.subs([(first_variable, x_0 + 0.5 * h), (second_variable, y + 0.5 + k1)])
        k3 = h * function.subs([(first_variable, x_0 + 0.5 * h), (second_variable, y + 0.5 + k2)])
        k4 = h * function.subs([(first_variable, x_0 + h), (second_variable, y + k3)])
        y = y + (1.0 / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        x_0 = x_0 + h
    return y
