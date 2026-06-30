import numpy as np


def upwind_advection_step(u, velocity, dx, dt, periodic=True):
    u = np.asarray(u, dtype=float)
    if u.ndim != 1:
        raise ValueError("u must be one-dimensional")
    if dx <= 0 or dt < 0:
        raise ValueError("invalid grid spacing or time step")
    if len(u) < 2:
        return u.copy()
    cfl = abs(velocity) * dt / dx
    if cfl > 1.0:
        raise ValueError("CFL condition violated")
    out = u.copy()
    if velocity >= 0:
        left = np.roll(u, 1) if periodic else np.r_[u[0], u[:-1]]
        out -= cfl * (u - left)
    else:
        right = np.roll(u, -1) if periodic else np.r_[u[1:], u[-1]]
        out -= cfl * (right - u)
    return out


def total_variation(u):
    u = np.asarray(u, dtype=float)
    if u.ndim != 1:
        raise ValueError("u must be one-dimensional")
    if len(u) < 2:
        return 0.0
    return float(np.abs(np.diff(u)).sum())
