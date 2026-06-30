def choose_time_step(error, dt, safety=0.9, order=2, min_dt=1e-6, max_dt=1.0):
    if dt <= 0 or min_dt <= 0 or max_dt <= 0 or min_dt > max_dt:
        raise ValueError("invalid time-step bounds")
    if error < 0:
        raise ValueError("error must be non-negative")
    if error == 0:
        return min(max_dt, 2.0 * dt), "grow"
    factor = safety * error ** (-1.0 / (order + 1))
    proposed = dt * factor
    if proposed < min_dt:
        return min_dt, "min-clamped"
    if proposed > max_dt:
        return max_dt, "max-clamped"
    if proposed < 0.75 * dt:
        return proposed, "shrink"
    if proposed > 1.25 * dt:
        return proposed, "grow"
    return proposed, "keep"
def stiffness_regime(jacobian, dt):
    import numpy as np

    j = np.asarray(jacobian, dtype=float)
    if j.ndim != 2 or j.shape[0] != j.shape[1]:
        raise ValueError("jacobian must be a square matrix")
    eig = np.linalg.eigvals(j)
    spectral_radius = float(np.max(np.abs(eig))) if eig.size else 0.0
    if spectral_radius == 0:
        return "nonstiff"
    if spectral_radius * dt > 10:
        return "stiff"
    if np.any(np.real(eig) > 0):
        return "unstable-growth"
    return "mild"
