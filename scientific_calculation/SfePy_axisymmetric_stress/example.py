import numpy as np


def axisymmetric_strain(radial_displacement, radius):
    u = np.asarray(radial_displacement, dtype=float)
    r = np.asarray(radius, dtype=float)
    if u.ndim != 1 or r.ndim != 1 or len(u) != len(r):
        raise ValueError("displacement and radius must be one-dimensional arrays of equal length")
    if len(u) < 2:
        raise ValueError("at least two radial samples are required")
    if np.any(r <= 0):
        raise ValueError("axisymmetric radius values must be positive")
    radial = np.gradient(u, r)
    hoop = u / r
    return radial, hoop


def von_mises_axisymmetric(radial_stress, hoop_stress, axial_stress=0.0):
    sr = np.asarray(radial_stress, dtype=float)
    sh = np.asarray(hoop_stress, dtype=float)
    sz = np.asarray(axial_stress, dtype=float)
    if sr.shape != sh.shape:
        raise ValueError("radial and hoop stresses must have the same shape")
    if sz.shape == ():
        sz = np.full_like(sr, float(sz))
    if sz.shape != sr.shape:
        raise ValueError("axial stress must be scalar or match stress shape")
    vm2 = 0.5 * ((sr - sh) ** 2 + (sh - sz) ** 2 + (sz - sr) ** 2)
    vm2 = np.maximum(vm2, 0.0)
    return np.sqrt(vm2)
