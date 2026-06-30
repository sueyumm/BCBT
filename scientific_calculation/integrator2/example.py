import numpy as np#6

def MonteCarlo_double(f, g, x0, x1, y0, y1, n):#7
    x = np.random.uniform(x0, x1, n)#14
    y = np.random.uniform(y0, y1, n)#15
    f_mean = 0#17
    num_inside = 0
    for i in range(len(x)):#19
        for j in range(len(y)):#20
            if g(x[i], y[j]) >= 0:#21
                num_inside += 1#22
                f_mean += f(x[i], y[j])#23
    f_mean = f_mean/float(num_inside)#24
    area = num_inside/float(n**2)*(x1 - x0)*(y1 - y0)#25
    return area*f_mean#26
