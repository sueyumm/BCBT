import numpy as np


def poroelastic_pressure_increment(volumetric_strain, biot_alpha, storage, dt):
    eps_v = np.asarray(volumetric_strain, dtype=float)
    if storage <= 0:
        raise ValueError("storage must be positive")
    if not 0.0 <= biot_alpha <= 1.0:
        raise ValueError("biot_alpha must be in [0, 1]")
    if dt <= 0:
        raise ValueError("time step must be positive")
    return -biot_alpha * eps_v / (storage * dt)


def coupled_residual(displacement_residual, pressure_residual, coupling_weight=1.0):
    ru = np.asarray(displacement_residual, dtype=float)
    rp = np.asarray(pressure_residual, dtype=float)
    if coupling_weight < 0:
        raise ValueError("coupling weight must be non-negative")
    if ru.size == 0 and rp.size == 0:
        return 0.0
    norm_u = float(np.linalg.norm(ru))
    norm_p = float(np.linalg.norm(rp))
    if norm_u == 0.0:
        return coupling_weight * norm_p
    if norm_p == 0.0:
        return norm_u
    return norm_u + coupling_weight * norm_p
