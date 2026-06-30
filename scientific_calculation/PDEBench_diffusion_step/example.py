import numpy as np


def explicit_diffusion_step(u, diffusivity, dx, dt, boundary="neumann"):
    u = np.asarray(u, dtype=float)
    if u.ndim != 1:
        raise ValueError("u must be one-dimensional")
    if diffusivity < 0 or dx <= 0 or dt < 0:
        raise ValueError("invalid physical parameters")
    alpha = diffusivity * dt / (dx * dx)
    if alpha > 0.5:
        raise ValueError("unstable explicit diffusion step")
    if len(u) < 3:
        return u.copy()
    out = u.copy()
    out[1:-1] = u[1:-1] + alpha * (u[:-2] - 2 * u[1:-1] + u[2:])
    if boundary == "dirichlet":
        out[0] = 0.0
        out[-1] = 0.0
    elif boundary == "neumann":
        out[0] = out[1]
        out[-1] = out[-2]
    else:
        raise ValueError("unknown boundary condition")
    return out


def diffusion_energy(u):
    u = np.asarray(u, dtype=float)
    return float(np.dot(u, u))
