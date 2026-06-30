import numpy as np


def small_strain_energy(strain, young_modulus, poisson_ratio, plane_stress=True):
    eps = np.asarray(strain, dtype=float)
    if eps.shape[-1] != 3:
        raise ValueError("2D strain must contain exx, eyy, exy components")
    if young_modulus <= 0:
        raise ValueError("young_modulus must be positive")
    if not -1.0 < poisson_ratio < 0.5:
        raise ValueError("poisson_ratio is outside the stable range")
    e = young_modulus
    nu = poisson_ratio
    if plane_stress:
        factor = e / (1.0 - nu ** 2)
        c11, c12, c33 = factor, factor * nu, factor * (1.0 - nu) / 2.0
    else:
        factor = e / ((1.0 + nu) * (1.0 - 2.0 * nu))
        c11 = factor * (1.0 - nu)
        c12 = factor * nu
        c33 = factor * (1.0 - 2.0 * nu) / 2.0
    exx, eyy, exy = eps[..., 0], eps[..., 1], eps[..., 2]
    return 0.5 * (c11 * exx ** 2 + 2.0 * c12 * exx * eyy + c11 * eyy ** 2 + c33 * exy ** 2)


def is_material_stable(young_modulus, poisson_ratio):
    return young_modulus > 0 and -1.0 < poisson_ratio < 0.5
