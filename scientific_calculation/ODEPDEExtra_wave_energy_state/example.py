import numpy as np


def wave_energy(u, velocity, dx):
    arr = np.asarray(u, dtype=float)
    vel = np.asarray(velocity, dtype=float)
    if arr.shape != vel.shape or arr.ndim != 1:
        raise ValueError("u and velocity must be matching one-dimensional arrays")
    if dx <= 0:
        raise ValueError("dx must be positive")
    grad = np.diff(arr) / dx
    kinetic = 0.5 * np.sum(vel * vel) * dx
    potential = 0.5 * np.sum(grad * grad) * dx
    total = kinetic + potential
    if total == 0:
        return "rest"
    if kinetic > 4.0 * potential:
        return "kinetic-dominated"
    if potential > 4.0 * kinetic:
        return "gradient-dominated"
    return "balanced"
def wave_packet_location(amplitude, threshold=0.5):
    import numpy as np

    a = np.asarray(amplitude, dtype=float)
    if a.ndim != 1 or a.size < 3:
        raise ValueError("amplitude must be a one-dimensional wave packet")
    active = np.flatnonzero(np.abs(a) >= threshold)
    if active.size == 0:
        return "quiet"
    center = float(np.mean(active))
    if center < a.size / 3:
        return "left-moving"
    if center > 2 * a.size / 3:
        return "right-moving"
    if active.size > a.size / 2:
        return "broad"
    return "centered"
