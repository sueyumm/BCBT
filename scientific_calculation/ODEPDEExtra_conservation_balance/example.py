import numpy as np


def conservation_status(before, after, source=0.0, dt=1.0, tol=1e-9):
    b = np.asarray(before, dtype=float)
    a = np.asarray(after, dtype=float)
    if b.shape != a.shape:
        raise ValueError("states must have matching shape")
    if dt <= 0 or tol < 0:
        raise ValueError("invalid tolerance or time step")
    expected = float(np.sum(b) + source * dt * b.size)
    actual = float(np.sum(a))
    error = actual - expected
    if abs(error) <= tol:
        return "conserved"
    if error > 0:
        return "mass-gained"
    return "mass-lost"
def flux_balance(left_flux, right_flux, cell_volume, source=0.0):
    import numpy as np

    left = np.asarray(left_flux, dtype=float)
    right = np.asarray(right_flux, dtype=float)
    if left.shape != right.shape:
        raise ValueError("flux arrays must match")
    if cell_volume <= 0:
        raise ValueError("cell_volume must be positive")
    net = float(np.sum(left - right) + source * cell_volume * left.size)
    if abs(net) < 1e-10:
        return "balanced"
    if net > 0 and source > 0:
        return "source-driven-gain"
    if net < 0 and source < 0:
        return "sink-driven-loss"
    return "boundary-driven"


def finite_volume_boundary_flux(state, normal, boundary="wall"):
    import numpy as np

    s = np.asarray(state, dtype=float)
    n = np.asarray(normal, dtype=float)
    if s.shape != (3,) or n.shape != (2,):
        raise ValueError("state must be [rho, u, v] and normal must be two-dimensional")
    rho, u, v = s
    if rho <= 0:
        raise ValueError("density must be positive")
    normal_speed = u * n[0] + v * n[1]
    if boundary == "wall":
        return 0.0
    if boundary == "outflow":
        return rho * max(normal_speed, 0.0)
    if boundary == "inflow":
        return rho * min(normal_speed, 0.0)
    if boundary == "reflective":
        return -rho * normal_speed
    raise ValueError("unknown boundary")
