import numpy as np


def reaction_diffusion_update(u, reaction_rate, diffusivity, dx, dt, carrying_capacity=1.0):
    u = np.asarray(u, dtype=float)
    if u.ndim != 1:
        raise ValueError("u must be one-dimensional")
    if carrying_capacity <= 0:
        raise ValueError("carrying_capacity must be positive")
    if reaction_rate < 0 or diffusivity < 0:
        raise ValueError("rates must be non-negative")
    if len(u) < 3:
        reaction = reaction_rate * u * (1.0 - u / carrying_capacity)
        return u + dt * reaction
    alpha = diffusivity * dt / (dx * dx)
    if alpha > 0.5:
        raise ValueError("unstable diffusion coefficient")
    laplace = np.zeros_like(u)
    laplace[1:-1] = u[:-2] - 2 * u[1:-1] + u[2:]
    reaction = reaction_rate * u * (1.0 - u / carrying_capacity)
    updated = u + dt * reaction + alpha * laplace
    return np.maximum(updated, 0.0)


def has_extinction(u, eps=1e-8):
    if eps < 0:
        raise ValueError("eps must be non-negative")
    return bool(np.all(np.asarray(u) <= eps))
