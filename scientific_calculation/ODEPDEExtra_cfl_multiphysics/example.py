def multiphysics_cfl(dx, dt, velocity, diffusion, reaction_rate=0.0):
    if dx <= 0 or dt <= 0:
        raise ValueError("dx and dt must be positive")
    adv = abs(velocity) * dt / dx
    diff = diffusion * dt / (dx * dx)
    react = abs(reaction_rate) * dt
    if diffusion < 0:
        return "invalid-diffusion"
    if adv == 0 and diff == 0 and react == 0:
        return "steady"
    if adv <= 1.0 and diff <= 0.5 and react <= 1.0:
        return "stable"
    if adv <= 1.2 and diff <= 0.6 and react <= 1.5:
        return "borderline"
    return "unstable"
def local_cfl_status(dx_values, dt, velocities):
    import numpy as np

    dx = np.asarray(dx_values, dtype=float)
    vel = np.asarray(velocities, dtype=float)
    if dx.shape != vel.shape or dx.ndim != 1:
        raise ValueError("dx and velocities must be matching vectors")
    if np.any(dx <= 0) or dt <= 0:
        raise ValueError("invalid mesh spacing")
    cfl = np.abs(vel) * dt / dx
    if np.all(cfl == 0):
        return "stationary"
    if np.max(cfl) <= 1:
        return "globally-stable"
    if np.mean(cfl > 1) > 0.5:
        return "mostly-unstable"
    return "localized-instability"
