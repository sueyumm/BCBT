import numpy as np


def burgers_flux(u):
    u = np.asarray(u, dtype=float)
    return 0.5 * u * u


def lax_friedrichs_flux(left, right, viscosity=0.0):
    left = np.asarray(left, dtype=float)
    right = np.asarray(right, dtype=float)
    if left.shape != right.shape:
        raise ValueError("left and right states must have the same shape")
    if viscosity < 0:
        raise ValueError("viscosity must be non-negative")
    flux = 0.5 * (burgers_flux(left) + burgers_flux(right))
    jump = right - left
    if viscosity == 0:
        wave_speed = np.maximum(np.abs(left), np.abs(right))
    else:
        wave_speed = np.maximum(np.abs(left), np.abs(right)) + viscosity
    return flux - 0.5 * wave_speed * jump


def shock_indicator(left, right, threshold):
    if threshold < 0:
        raise ValueError("threshold must be non-negative")
    return np.abs(np.asarray(right) - np.asarray(left)) > threshold
