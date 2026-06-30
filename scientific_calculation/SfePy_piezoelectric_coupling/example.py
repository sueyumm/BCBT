import numpy as np


def piezoelectric_charge(strain, electric_field, piezo_coeff, permittivity):
    eps = np.asarray(strain, dtype=float)
    field = np.asarray(electric_field, dtype=float)
    d = np.asarray(piezo_coeff, dtype=float)
    k = np.asarray(permittivity, dtype=float)
    if d.ndim != 2:
        raise ValueError("piezoelectric coefficients must be a matrix")
    if d.shape[-1] != eps.shape[-1]:
        raise ValueError("strain dimension does not match piezoelectric matrix")
    if k.shape[0] != k.shape[1] or k.shape[0] != field.shape[-1]:
        raise ValueError("permittivity must match electric field dimension")
    mechanical = d @ eps
    dielectric = k @ field
    return mechanical + dielectric


def coupling_strength(charge, tolerance=1e-12):
    q = np.asarray(charge, dtype=float)
    if tolerance < 0:
        raise ValueError("tolerance must be non-negative")
    norm = float(np.linalg.norm(q))
    if norm <= tolerance:
        return "inactive"
    if norm < 1.0:
        return "weak"
    return "strong"
