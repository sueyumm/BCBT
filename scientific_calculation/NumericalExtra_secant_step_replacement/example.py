# Adapted from arash79/Numerical-methods root-finding routines.


def secant_step_status(x0, x1, f0, f1, tolerance=1e-8):
    if tolerance <= 0:
        raise ValueError("invalid tolerance")
    denominator = f1 - f0
    if abs(f1) <= tolerance:
        return "converged"
    if abs(denominator) <= tolerance:
        return "flat"
    x2 = x1 - f1 * (x1 - x0) / denominator
    if abs(x2 - x1) <= tolerance:
        return "small-step"
    if x2 < min(x0, x1) or x2 > max(x0, x1):
        return "outside"
    return "inside"
