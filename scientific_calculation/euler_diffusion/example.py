import numpy as np  # 1

def euler_diffusion(u, D, dt, dx, F):  # 2
    Nx = len(u)  # 3
    tmp = np.zeros(Nx)  # 4
    Ddtdx2 = D * dt / (dx * dx)  # 5
    for j in range(1, Nx - 1):  # 6
        tmp[j] = u[j] + Ddtdx2 * (u[j + 1] - 2 * u[j] + u[j - 1]) - F * dt  # 7
    return tmp  # 8