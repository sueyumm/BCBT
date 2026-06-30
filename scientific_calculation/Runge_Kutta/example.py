# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 12:24:44 2022

@author: muham
"""

def dydx(x,y):
    return y-x

def myRungeKutta(x0, y0, x, h):
    
    n = (int)((x-x0)/h)     
    
    for i in range(1,n+1): 
        
        k1 = dydx(x0, y0)
        k2 = dydx(x0 + h*0.5, y0 + (k1*h)*0.5)
        k3 = dydx(x0 + h*0.5, y0 + (k2*h)*0.5)
        k4 = dydx(x0 + h, y0 + (k3*h))
        
        y0 = y0 + (1.0 / 6.0)*(k1 + 2 * k2 + 2 * k3 + k4)*h
        x0 = x0 + h
    
    return y0

x0 = 0
y = 0
x = 20
h = 0.1
print ("The value of y(", x, ") is:", myRungeKutta(x0, y, x, h))