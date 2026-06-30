import numpy as np

def jacobi(u, f, dx, Nx, Ny, itmax):
    x = np.zeros(Nx * Ny)
    for j in range(Ny):
        for i in range(Nx):
            x[i + j * Nx] = u[i + j * Nx]
    for it in range(itmax):
        for j in range(1, Ny - 1):
            for i in range(1, Nx - 1):
                x[i + j * Nx] = 0.25 * (x[(i - 1) + j * Nx]
                                        + x[(i + 1) + j * Nx]
                                        + x[i + (j - 1) * Nx]
                                        + x[i + (j + 1) * Nx]
                                        - dx * dx * f[i + j * Nx])
    return x