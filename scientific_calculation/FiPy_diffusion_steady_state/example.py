import numpy as np


def solve_steady_diffusion_1d(left, right, nx, source=0.0, diffusivity=1.0):
    if nx < 2:
        raise ValueError("nx must be at least 2")
    if diffusivity <= 0:
        raise ValueError("diffusivity must be positive")
    x = np.linspace(0.0, 1.0, nx)
    profile = left + (right - left) * x
    if source != 0.0:
        correction = 0.5 * source / diffusivity * x * (1.0 - x)
        profile += correction
    return profile


def boundary_flux(profile, dx, side="left"):
    profile = np.asarray(profile, dtype=float)
    if profile.ndim != 1 or len(profile) < 2:
        raise ValueError("profile must be a one-dimensional array with at least two cells")
    if dx <= 0:
        raise ValueError("dx must be positive")
    if side == "left":
        return -(profile[1] - profile[0]) / dx
    if side == "right":
        return -(profile[-1] - profile[-2]) / dx
    raise ValueError("unknown boundary side")
