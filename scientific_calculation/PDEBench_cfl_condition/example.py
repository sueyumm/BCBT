import numpy as np


def compute_cfl(velocity, dt, dx):
    velocity = np.asarray(velocity, dtype=float)
    if dt < 0 or dx <= 0:
        raise ValueError("invalid dt or dx")
    if velocity.size == 0:
        return 0.0
    return float(np.max(np.abs(velocity)) * dt / dx)


def choose_stable_dt(velocity, dx, max_cfl=0.5, min_dt=1e-8):
    if max_cfl <= 0 or dx <= 0:
        raise ValueError("max_cfl and dx must be positive")
    vmax = float(np.max(np.abs(np.asarray(velocity, dtype=float)))) if np.asarray(velocity).size else 0.0
    if vmax == 0:
        return min_dt
    dt = max_cfl * dx / vmax
    if dt < min_dt:
        return min_dt
    return dt


def is_stable(velocity, dt, dx, max_cfl=1.0):
    return compute_cfl(velocity, dt, dx) <= max_cfl
