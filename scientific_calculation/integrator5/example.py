import math
from math import sin


  
def givenFunction(x, y):  
   return (math.sin(x+y))/(x+y)


def doubleIntegral(h, k, lx, ux, ly, uy):  

    z = [[None for i in range(50)] 
               for j in range(50)] 
    ax = [None] * 50

    nx = round((ux - lx) / h + 1)  
    ny = round((uy - ly) / k + 1) 

    for i in range(0, nx):  
        for j in range(0, ny):  
            z[i][j] = givenFunction(lx + i * h,  
                                    ly + j * k)  

    for i in range(0, nx):  
        ax[i] = 0
        for j in range(0, ny):  
              
            if j == 0 or j == ny - 1:  
                ax[i] += z[i][j]  
            elif j % 2 == 0: 
                ax[i] += 2 * z[i][j]  
            else: 
                ax[i] += 4 * z[i][j]  
          
        ax[i] *= (k / 3)  
      
    answer = 0

    for i in range(0, nx):  
        if i == 0 or i == nx - 1:  
            answer += ax[i]  
        elif i % 2 == 0: 
            answer += 2 * ax[i]  
        else: 
            answer += 4 * ax[i]  
      
    answer *= (h / 3)  
  
    return answer  

    
    
