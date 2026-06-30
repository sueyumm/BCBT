import numpy as np


def anisotropy_strength(theta, epsilon=0.05, symmetry=4):
    if symmetry <= 0:
        raise ValueError("symmetry must be positive")
    if epsilon < 0:
        raise ValueError("epsilon must be non-negative")
    theta = np.asarray(theta, dtype=float)
    return 1.0 + epsilon * np.cos(symmetry * theta)


def anisotropic_mobility(grad_x, grad_y, epsilon=0.05):
    grad_x = np.asarray(grad_x, dtype=float)
    grad_y = np.asarray(grad_y, dtype=float)
    if grad_x.shape != grad_y.shape:
        raise ValueError("gradient components must have the same shape")
    theta = np.arctan2(grad_y, grad_x)
    strength = anisotropy_strength(theta, epsilon=epsilon)
    zero_gradient = (grad_x == 0) & (grad_y == 0)
    if np.any(zero_gradient):
        strength = strength.copy()
        strength[zero_gradient] = 1.0
    return strength
